# -*- coding: utf-8 -*-
"""Validação de base de reconciliação — encontra incoerências ANTES do cálculo.

Reconciliação com dado inconsistente é pior que nenhuma: produz um número com aparência
de resultado e sem lastro. Este módulo procura os problemas que mais aparecem em base de
produção e de reconciliação por realce, e devolve cada achado com o impacto em massa e
metal, para que a decisão do que fazer seja informada.

**Nenhuma verificação decide sozinha o que fazer.** Toda incoerência sai com
`decisao_do_usuario=True` — leve ao usuário, apresente as opções (incluir, excluir, tratar
à parte) com o impacto de cada uma, e registre a escolha na seção de premissas do relatório.

Uso:
    from validar_base import validar_producao, validar_realces, relatorio_texto
    achados = validar_producao(df, col_no="MOVIMENTACAO", col_entidade="MINA",
                               col_periodo="MÊS", col_massa="MASSA", col_metal="METAL",
                               col_teor="TEOR")
    print(relatorio_texto(achados))
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

import pandas as pd
import numpy as np


@dataclass
class Achado:
    codigo: str
    gravidade: str          # "bloqueia" | "atencao" | "informa"
    titulo: str
    detalhe: str
    impacto: dict = field(default_factory=dict)
    opcoes: list = field(default_factory=list)
    decisao_do_usuario: bool = True


def _n(s): return pd.to_numeric(s, errors="coerce")


# ─────────────────────────────────────────────── base de produção (temporal)
def validar_producao(df: pd.DataFrame, col_no: str, col_entidade: str, col_periodo: str,
                     col_massa: str, col_metal: str | None = None,
                     col_teor: str | None = None,
                     par_reconciliacao: tuple[str, str] = ("REPORTADO", "RECONCILIADO"),
                     ordem_periodos: list | None = None) -> list[Achado]:
    a: list[Achado] = []
    d = df.copy()
    d[col_massa] = _n(d[col_massa])
    if col_metal: d[col_metal] = _n(d[col_metal])

    # 1. cobertura temporal desigual entre nós
    cob = (d[d[col_massa] > 0].groupby([col_entidade, col_no])[col_periodo]
           .nunique().reset_index(name="n_periodos"))
    for ent, g in cob.groupby(col_entidade):
        mx = g.n_periodos.max()
        parciais = g[g.n_periodos < mx]
        if len(parciais):
            a.append(Achado(
                "COBERTURA_TEMPORAL", "bloqueia",
                f"{ent}: nós com cobertura temporal diferente",
                "Comparar o total de um nó presente em {} períodos com outro presente em menos "
                "produz desvio artificial. Restrinja cada relação aos períodos em que os DOIS nós "
                "existem.".format(mx),
                impacto={"nos_parciais": {r[col_no]: f"{r.n_periodos}/{mx} períodos"
                                          for _, r in parciais.iterrows()}},
                opcoes=["restringir cada par aos períodos comuns (recomendado)",
                        "comparar totais assumindo o desvio artificial (não recomendado)",
                        "excluir o nó parcial da análise"]))

    # 2. lançamento por evento misturado com fluxo mensal
    for ent, g in cob.groupby(col_entidade):
        mx = g.n_periodos.max()
        evento = g[g.n_periodos <= max(2, mx // 3)]
        if len(evento):
            a.append(Achado(
                "ESCOPO_EVENTO", "atencao",
                f"{ent}: nós que parecem lançamento por evento, não fluxo mensal",
                "Nós que aparecem em pouquíssimos períodos concentrando massa alta costumam ser "
                "lançados quando o evento ocorre (escaneamento, desmonte), e não mês a mês. "
                "Não servem para reconciliação temporal.",
                impacto={"nos": {r[col_no]: f"{r.n_periodos}/{mx} períodos"
                                 for _, r in evento.iterrows()}},
                opcoes=["tratar como reconciliação espacial, fora da série temporal (recomendado)",
                        "confirmar com a operação se o lançamento é mensal",
                        "excluir da análise"]))

    # 3. reconciliado × não reconciliado
    rep, rec = par_reconciliacao
    if {rep, rec} <= set(d[col_no].unique()):
        base = col_metal or col_massa
        piv = d[d[col_no].isin([rep, rec])].pivot_table(
            index=col_entidade, columns=col_no, values=base, aggfunc="sum")
        if {rep, rec} <= set(piv.columns):
            piv["cobertura"] = piv[rec] / piv[rep]
            fora = piv[(piv["cobertura"] < 0.999) | (piv["cobertura"] > 1.001)]
            if len(fora):
                a.append(Achado(
                    "COBERTURA_RECONCILIACAO", "atencao",
                    "Cobertura de reconciliação parcial ou divergente",
                    "A parcela reconciliada difere da reportada. Se for cobertura parcial, os "
                    "indicadores calculados valem só para essa fração e NÃO representam a operação. "
                    "Confirme se é cobertura (quanto já foi reconciliado) ou fator (quanto mudou).",
                    impacto={str(i): {"reportado": round(r[rep], 1), "reconciliado": round(r[rec], 1),
                                      "razao": round(r["cobertura"], 4)}
                             for i, r in fora.iterrows()},
                    opcoes=["reportar cada indicador junto da sua cobertura (recomendado)",
                            "restringir a análise à parcela reconciliada",
                            "aguardar a reconciliação fechar antes de concluir"]))

    # 4. teor carimbado (parâmetro fixo, não medição)
    if col_teor:
        d[col_teor] = _n(d[col_teor])
        for ent, g in d[d[col_teor] > 0].groupby(col_entidade):
            if g[col_teor].nunique() == 1 and len(g) > 20:
                a.append(Achado(
                    "TEOR_CARIMBADO", "bloqueia",
                    f"{ent}: teor idêntico em todos os registros",
                    f"Teor fixo em {g[col_teor].iloc[0]:g} nos {len(g)} registros. Isso é parâmetro, "
                    "não medição — qualquer indicador de teor dessa entidade é vazio por construção, "
                    "e o princípio de comparar medido com medido não se sustenta aqui.",
                    impacto={"registros": int(len(g)), "massa": float(g[col_massa].sum())},
                    opcoes=["excluir a entidade dos indicadores de teor (recomendado)",
                            "confirmar se é premissa provisória e datar",
                            "manter, sinalizando no relatório que o teor não é medido"]))

    # 5. metal não fecha com massa x teor
    if col_metal and col_teor:
        m = d[(d[col_massa] > 0) & (d[col_metal] > 0) & (d[col_teor] > 0)].copy()
        if len(m):
            esperado = m[col_massa] * m[col_teor] / 100.0
            erro = (m[col_metal] - esperado).abs() / m[col_metal].replace(0, np.nan)
            ruins = m[erro > 0.01]
            if len(ruins):
                a.append(Achado(
                    "METAL_NAO_FECHA", "bloqueia",
                    "Metal não fecha com massa x teor",
                    f"{len(ruins)} de {len(m)} registros com divergência acima de 1% entre o metal "
                    "reportado e massa x teor. Verifique a unidade do teor (% ou g/t) e a base "
                    "de umidade antes de qualquer cálculo.",
                    impacto={"registros_afetados": int(len(ruins)),
                             "massa_afetada": float(ruins[col_massa].sum())},
                    opcoes=["corrigir a unidade e recalcular",
                            "usar o metal reportado e ignorar o teor",
                            "usar massa x teor e ignorar o metal reportado"]))

    # 6. valores negativos e nulos onde não deveriam existir
    neg = d[d[col_massa] < 0]
    if len(neg):
        a.append(Achado(
            "MASSA_NEGATIVA", "atencao", "Massa negativa em alguns registros",
            "Massa negativa costuma ser ajuste de inventário ou estorno. Se for ajuste, precisa "
            "estar identificado como tal e não somado ao fluxo físico.",
            impacto={"registros": int(len(neg)), "massa_total": float(neg[col_massa].sum()),
                     "nos": sorted(neg[col_no].astype(str).unique().tolist())[:8]},
            opcoes=["tratar como ajuste, fora do fluxo (recomendado)",
                    "somar ao fluxo", "excluir"]))
    return a


# ─────────────────────────────────────────────── base por realce (espacial)
def validar_realces(df: pd.DataFrame, col_id: str, col_status_lavra: str | None,
                    col_status_recon: str | None, cols_cadeia: dict,
                    col_entidade: str | None = None) -> list[Achado]:
    """cols_cadeia: {"nome legível do nó": "coluna de massa"} na ordem da cadeia."""
    a: list[Achado] = []
    d = df[df[col_id].notna()].copy()
    for c in cols_cadeia.values():
        d[c] = _n(d[c]).fillna(0)

    # 1. cadeia incompleta por realce
    nos = list(cols_cadeia)
    presenca = pd.DataFrame({n: d[cols_cadeia[n]] > 0 for n in nos})
    completos = presenca.all(axis=1)
    if (~completos).any():
        faltas = {n: int((~presenca[n]).sum()) for n in nos if (~presenca[n]).any()}
        a.append(Achado(
            "CADEIA_INCOMPLETA", "bloqueia",
            "Realces sem cadeia completa",
            f"{int((~completos).sum())} de {len(d)} realces não têm todos os nós preenchidos. "
            "Os indicadores só podem ser calculados sobre o subconjunto completo, e esse "
            "subconjunto precisa ser declarado junto do resultado.",
            impacto={"realces_completos": int(completos.sum()), "realces_total": int(len(d)),
                     "cobertura": round(float(completos.mean()), 3),
                     "nos_vazios_em_n_realces": faltas},
            opcoes=["calcular sobre o subconjunto completo e declarar a cobertura (recomendado)",
                    "preencher os nós faltantes antes de calcular",
                    "calcular por nó, aceitando bases diferentes por indicador"]))

    # 2. nó integralmente vazio
    vazios = [n for n in nos if (d[cols_cadeia[n]] > 0).sum() == 0]
    if vazios:
        a.append(Achado(
            "NO_VAZIO", "bloqueia", "Nós da cadeia integralmente vazios",
            "Estes nós existem na estrutura mas não têm nenhum valor. Todo indicador que dependa "
            "deles é não calculável — não substitua por proxy.",
            impacto={"nos": vazios},
            opcoes=["reportar os indicadores dependentes como não calculáveis (recomendado)",
                    "preencher a base antes de calcular"]))

    # 3. lavrado × reconciliado
    if col_status_lavra and col_status_recon:
        cr = d.groupby([col_status_lavra, col_status_recon]).size().reset_index(name="n")
        pend = cr[(cr[col_status_lavra].astype(str).str.contains("Lavrado", case=False, na=False)) &
                  (~cr[col_status_recon].astype(str).str.contains("^Reconciliado$", case=False,
                                                                  na=False, regex=True))]
        if len(pend):
            a.append(Achado(
                "LAVRADO_NAO_RECONCILIADO", "atencao",
                "Realces lavrados que não estão reconciliados",
                "Realce já lavrado e ainda não reconciliado é produção fora da equação. Se for "
                "parcela relevante, os indicadores do período estão calculados sobre uma amostra "
                "que não é aleatória — o que é reconciliado primeiro costuma ser o que tem "
                "levantamento pronto ou o que deu problema.",
                impacto={f"{r[col_status_lavra]} / {r[col_status_recon]}": int(r.n)
                         for _, r in pend.iterrows()},
                opcoes=["incluir, sinalizando a cobertura (recomendado)",
                        "excluir e calcular só sobre os reconciliados",
                        "tratar os parciais à parte"]))
        if col_status_recon in d:
            sem = d[d[col_status_recon].isna()]
            if len(sem):
                a.append(Achado(
                    "STATUS_AUSENTE", "atencao", "Realces sem status de reconciliação",
                    "Sem status não há como saber se entram na análise.",
                    impacto={"realces": sorted(sem[col_id].astype(str).tolist())[:12],
                             "total": int(len(sem))},
                    opcoes=["classificar antes de calcular (recomendado)",
                            "tratar como não reconciliado", "excluir"]))

    # 4. monotonia suspeita: nó posterior menor que anterior sem explicação
    for i in range(len(nos) - 1):
        ant, pos = nos[i], nos[i + 1]
        both = (d[cols_cadeia[ant]] > 0) & (d[cols_cadeia[pos]] > 0)
        if both.sum() == 0: continue
        queda = d[both & (d[cols_cadeia[pos]] < d[cols_cadeia[ant]] * 0.5)]
        if len(queda):
            a.append(Achado(
                "QUEDA_ABRUPTA", "informa",
                f"Queda acima de 50% de '{ant}' para '{pos}'",
                "Pode ser real (perda de minério, mudança de escopo) ou erro de preenchimento. "
                "Vale conferir realce a realce antes de consolidar.",
                impacto={"realces": sorted(queda[col_id].astype(str).tolist())[:10],
                         "total": int(len(queda))},
                opcoes=["conferir os realces listados (recomendado)",
                        "aceitar como real", "excluir da consolidação"]))
    return a


# ─────────────────────────────────────────────── apresentação
def relatorio_texto(achados: list[Achado]) -> str:
    if not achados:
        return "Nenhuma incoerência encontrada nas verificações aplicadas."
    ordem = {"bloqueia": 0, "atencao": 1, "informa": 2}
    rot = {"bloqueia": "BLOQUEIA O CÁLCULO", "atencao": "ATENÇÃO", "informa": "INFORMATIVO"}
    linhas = [f"{len(achados)} achado(s). Nenhum foi decidido automaticamente — "
              "leve ao usuário antes de calcular.\n"]
    for a in sorted(achados, key=lambda x: ordem.get(x.gravidade, 9)):
        linhas.append(f"[{rot.get(a.gravidade, a.gravidade)}] {a.titulo}  ({a.codigo})")
        linhas.append(f"   {a.detalhe}")
        if a.impacto:
            linhas.append(f"   impacto: {a.impacto}")
        for o in a.opcoes:
            linhas.append(f"     - {o}")
        linhas.append("")
    return "\n".join(linhas)


def como_dict(achados: list[Achado]) -> list[dict]:
    return [asdict(a) for a in achados]
