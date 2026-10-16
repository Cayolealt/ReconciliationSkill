#!/usr/bin/env python3
"""
Cálculos determinísticos de reconciliação de lavra.

Implementa as fórmulas de references/03-formulas-e-calculos.md, seguindo a convenção
padronizada da indústria (Fouet et al., 2009; Morley, 2014; Morley & Arvidson, 2017;
Chieregati, 2023): a cadeia de valor é lida da esquerda para a direita e o NÓ MAIS ANTIGO
É SEMPRE O DENOMINADOR.

Use este módulo em vez de fazer a aritmética à mão: ele aplica a convenção correta de
denominador, pondera teores por massa e evita erro de sinal.

Uso como biblioteca:
    from reconciliacao import No, fator, indicadores_proativos
    a = No("Modelo de curto prazo", massa=80000, teor=2.55)
    b = No("Operação", massa=75000, teor=2.42)
    print(fator(a, b))

Uso como CLI:
    python reconciliacao.py --exemplo            # roda o exemplo verificado da literatura
    python reconciliacao.py --autoteste          # valida as fórmulas
    python reconciliacao.py --input dados.json --out resultados.json
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field, asdict
from typing import Iterable, Sequence

OZ_TROY_G = 31.1034768  # gramas por onça troy


# ---------------------------------------------------------------- nós e utilidades

@dataclass
class No:
    """Um nó da cadeia de valor: massa (t), teor e, opcionalmente, metal contido.

    teor_unidade: 'g/t', '%', 'ppm' etc. Serve para o cálculo de metal e para o relatório.
    Se `metal` não for informado, é calculado a partir de massa e teor.
    """
    nome: str
    massa: float | None = None
    teor: float | None = None
    metal: float | None = None
    teor_unidade: str = "g/t"
    metal_unidade: str = "oz"

    def __post_init__(self):
        if self.metal is None and self.massa is not None and self.teor is not None:
            self.metal = metal_contido(self.massa, self.teor, self.teor_unidade,
                                       self.metal_unidade)


def metal_contido(massa_t: float, teor: float, teor_unidade: str = "g/t",
                  metal_unidade: str = "oz") -> float:
    """Metal contido a partir de massa (t) e teor.

    g/t + oz  -> onças troy;  g/t + kg -> kg;  % + t -> toneladas de metal;
    ppm tratado como g/t.
    """
    u = teor_unidade.strip().lower()
    m = metal_unidade.strip().lower()
    if u in ("g/t", "gpt", "ppm", "g/ton"):
        gramas = massa_t * teor
        if m in ("oz", "onca", "onça", "oz troy"):
            return gramas / OZ_TROY_G
        if m == "kg":
            return gramas / 1000.0
        if m in ("g", "grama"):
            return gramas
    if u in ("%", "pct", "percent"):
        return massa_t * teor / 100.0  # toneladas de metal
    raise ValueError(f"combinação de unidades não suportada: teor={teor_unidade}, metal={metal_unidade}")


def media_ponderada(valores: Sequence[float], pesos: Sequence[float]) -> float:
    """Média ponderada por massa. NUNCA usar média aritmética para agregar teores."""
    if len(valores) != len(pesos):
        raise ValueError("valores e pesos devem ter o mesmo comprimento")
    soma_pesos = sum(pesos)
    if soma_pesos == 0:
        raise ValueError("soma dos pesos é zero")
    return sum(v * p for v, p in zip(valores, pesos)) / soma_pesos


def agregar(nos: Iterable[No], nome: str = "Agregado") -> No:
    """Soma massas e metal e recalcula o teor como média ponderada por massa."""
    nos = list(nos)
    massa = sum(n.massa for n in nos if n.massa is not None)
    metal = sum(n.metal for n in nos if n.metal is not None)
    teor = media_ponderada([n.teor for n in nos], [n.massa for n in nos]) if massa else None
    ref = nos[0]
    return No(nome, massa=massa, teor=teor, metal=metal,
              teor_unidade=ref.teor_unidade, metal_unidade=ref.metal_unidade)


def _razao(posterior: float | None, anterior: float | None) -> float | None:
    if posterior is None or anterior is None:
        return None
    if anterior == 0:
        return None
    return posterior / anterior


# ---------------------------------------------------------------- fatores / relações

def fator(anterior: No, posterior: No) -> dict:
    """Fator e variação % de uma relação de reconciliação.

    O nó ANTERIOR na cadeia de valor é sempre o denominador (Morley & Arvidson, 2017).
    Retorna fatores e variações para massa, teor e metal.

    Leitura: fator > 1,00 (variação '+') = o nó posterior é maior que o anterior.
    Um '+' consistente NÃO é bom: significa que o modelo/plano subestima sistematicamente.
    """
    f_massa = _razao(posterior.massa, anterior.massa)
    f_teor = _razao(posterior.teor, anterior.teor)
    f_metal = _razao(posterior.metal, anterior.metal)
    return {
        "relacao": f"{anterior.nome} para {posterior.nome}",
        "anterior": {"nome": anterior.nome, "massa": anterior.massa,
                     "teor": anterior.teor, "metal": anterior.metal},
        "posterior": {"nome": posterior.nome, "massa": posterior.massa,
                      "teor": posterior.teor, "metal": posterior.metal},
        "fator_massa": f_massa,
        "fator_teor": f_teor,
        "fator_metal": f_metal,
        "var_massa_pct": None if f_massa is None else (f_massa - 1) * 100,
        "var_teor_pct": None if f_teor is None else (f_teor - 1) * 100,
        "var_metal_pct": None if f_metal is None else (f_metal - 1) * 100,
    }


def cadeia(nos: Sequence[No]) -> list[dict]:
    """Fatores de todos os elos consecutivos de uma cadeia de nós."""
    return [fator(nos[i], nos[i + 1]) for i in range(len(nos) - 1)]


def indicadores_proativos(longo_prazo: No, curto_prazo: No, planejamento: No,
                          operacao: No, alimentacao_usina: No | None = None,
                          produtos_usina: No | None = None,
                          base: str = "metal") -> dict:
    """Modelo de indicadores pró-ativos (Chieregati, 2023).

    GM  = curto prazo / longo prazo         (modelo geológico)
    MP  = planejamento / curto prazo        (mine to plan)
    MO  = operação / planejamento           (mine operation)
    MM  = MP x MO = operação / curto prazo  (mine to mill)
    MR  = alimentação da usina / longo prazo = GM x MM   (reconciliação mina)
    PR  = produtos / alimentação da usina   (reconciliação planta)
    MCF = MR x PR = produtos / longo prazo  (mine call factor)

    base: 'metal' (recomendado), 'massa' ou 'teor'.
    Se alimentacao_usina for None, assume-se que a operação alimentou a usina diretamente.
    """
    if base not in ("metal", "massa", "teor"):
        raise ValueError("base deve ser 'metal', 'massa' ou 'teor'")
    v = lambda n: None if n is None else getattr(n, base)

    alim = alimentacao_usina if alimentacao_usina is not None else operacao

    gm = _razao(v(curto_prazo), v(longo_prazo))
    mp = _razao(v(planejamento), v(curto_prazo))
    mo = _razao(v(operacao), v(planejamento))
    mm = None if (mp is None or mo is None) else mp * mo
    mr = _razao(v(alim), v(longo_prazo))
    pr = _razao(v(produtos_usina), v(alim)) if produtos_usina is not None else None
    mcf = None if (mr is None or pr is None) else mr * pr

    ind = {"GM": gm, "MP": mp, "MO": mo, "MM": mm, "MR": mr, "PR": pr, "MCF": mcf}
    # o elo crítico é o indicador ELEMENTAR (não composto) mais distante de 1,00
    elementares = {k: x for k, x in ind.items()
                   if x is not None and k in ("GM", "MP", "MO", "PR")}
    critico = (max(elementares, key=lambda k: abs(elementares[k] - 1))
               if elementares else None)
    return {
        "base": base,
        "indicadores": ind,
        "indicador_critico": critico,
        "nota": ("O indicador crítico é o elo com maior afastamento de 1,00. "
                 "Um MCF próximo de 1,00 com indicadores intermediários divergindo em "
                 "sentidos opostos indica RECONCILIAÇÃO ILUSÓRIA — investigar cada elo."),
    }


# ---------------------------------------------------------------- diluição, lavra, espacial

def cobertura_reconciliacao(reconciliado: float, reportado: float) -> dict:
    """% da produção do período que já passou pelo processo de reconciliação.

    NÃO é um fator de reconciliação. Nomear a saída como 'cobertura' ou '% da produção
    reconciliada' — chamar de 'taxa de reconciliação' induz o leitor a ler 29% como uma mina
    entregando 29% do previsto.
    """
    c = _razao(reconciliado, reportado)
    return {"reconciliado": reconciliado, "reportado": reportado, "cobertura": c,
            "rotulo_seguro": "% da produção reconciliada",
            "aviso": ("Não exibir na mesma tabela ou eixo que fatores de reconciliação "
                      "sem rótulo que as distinga.")}


def cadeia_padrao(nos: dict, base: str = "metal", pares: dict | None = None) -> dict:
    """Indicadores da cadeia de valor padrão da skill (ver references/10-cadeia-padrao.md).

    Modelo de Joscil Spitzner Galvão (2020, atualização 2023), baseado em
    Ana Carolina Chieregati (2011).

    `nos` é {nome_do_no: No}. Só entram nos indicadores os nós que existirem — nó ausente
    NÃO vira zero e NÃO é substituído por proxy; o indicador correspondente sai como
    não calculável, com o motivo.

    `pares` permite sobrescrever a definição de qualquer indicador para a operação
    específica: {"PC": ("no_anterior", "no_posterior"), ...}. Use isso sempre que o código
    de prática do site definir os nós de forma diferente — sobretudo na faixa da planta,
    onde PC, PO e PR admitem mais de uma definição legítima.
    """
    padrao = {
        "GM":   ("box_model_lt", "box_model_st"),
        "MP":   ("box_model_st", "stope_st_model"),
        "MO":   ("stope_st_model", "grade_control"),
        "Mrec": ("grade_control", "ore_reported"),
        "PC":   ("ore_reported", "head_grade"),
        "PO":   ("head_grade", "feed_grade"),
        "PR":   ("feed_grade", "concentrate"),
        "MCF":  ("box_model_lt", "concentrate"),
    }
    defs = dict(padrao); defs.update(pares or {})
    if base not in ("metal", "massa", "teor"):
        raise ValueError("base deve ser 'metal', 'massa' ou 'teor'")

    out, faltando = {}, {}
    for ind, (a, b) in defs.items():
        na, nb = nos.get(a), nos.get(b)
        ausentes = [n for n, o in ((a, na), (b, nb)) if o is None]
        if ausentes:
            out[ind] = None
            faltando[ind] = f"nó ausente: {', '.join(ausentes)}"
            continue
        va, vb = getattr(na, base), getattr(nb, base)
        r = _razao(vb, va)
        out[ind] = r
        if r is None:
            faltando[ind] = f"valor nulo ou zero em {a} ou {b} na base '{base}'"

    calculados = {k: v for k, v in out.items() if v is not None and k != "MCF"}
    critico = max(calculados, key=lambda k: abs(calculados[k] - 1)) if calculados else None
    return {
        "modelo": "Galvão (2020, rev. 2023), baseado em Chieregati (2011)",
        "base": base,
        "definicoes": {k: f"{a} para {b}" for k, (a, b) in defs.items()},
        "indicadores": out,
        "nao_calculaveis": faltando,
        "indicador_critico": critico,
        "nota": ("Overbreak e underbreak são nós desta cadeia, não métricas derivadas: "
                 "reporte-os separadamente com overbreak_underbreak(), nunca pelo líquido. "
                 "Um indicador agregado próximo de 1,00 com elos divergindo em sentidos "
                 "opostos é reconciliação ilusória."),
    }


def diluicao_recuperacao(massa_minerio_planejada: float, massa_minerio_recuperada: float,
                         massa_esteril_como_minerio: float, massa_total_lavrada: float,
                         teor_previsto: float | None = None,
                         teor_realizado: float | None = None) -> dict:
    """Diluição (massa e teor), recuperação de minério e perda de minério."""
    out = {
        "recuperacao_minerio_massa": _razao(massa_minerio_recuperada, massa_minerio_planejada),
        "diluicao_massa": _razao(massa_esteril_como_minerio, massa_total_lavrada),
    }
    r = out["recuperacao_minerio_massa"]
    out["perda_minerio"] = None if r is None else 1 - r
    if teor_previsto not in (None, 0) and teor_realizado is not None:
        out["diluicao_teor"] = (teor_previsto - teor_realizado) / teor_previsto
    else:
        out["diluicao_teor"] = None
    return out


def overbreak_underbreak(volume_projetado: float, volume_lavrado: float,
                         volume_em_projeto: float,
                         area_parede_exposta: float | None = None) -> dict:
    """Sobrelavra e sublavra a partir da comparação 3D projetado x lavrado.

    volume_em_projeto = interseção (lavrado ∩ projetado).
    Sobrelavra e sublavra podem se compensar em massa e destruir valor em teor —
    por isso são SEMPRE reportadas separadamente, nunca só o líquido.
    """
    if volume_em_projeto > min(volume_projetado, volume_lavrado) + 1e-9:
        raise ValueError("volume_em_projeto não pode exceder o projetado nem o lavrado")
    sobre = volume_lavrado - volume_em_projeto
    sub = volume_projetado - volume_em_projeto
    out = {
        "volume_projetado": volume_projetado,
        "volume_lavrado": volume_lavrado,
        "volume_em_projeto": volume_em_projeto,
        "volume_sobrelavra": sobre,
        "volume_sublavra": sub,
        "volume_liquido": volume_lavrado - volume_projetado,
        "overbreak_pct": _razao(sobre, volume_projetado),
        "underbreak_pct": _razao(sub, volume_projetado),
        "ELOS_m": _razao(sobre, area_parede_exposta) if area_parede_exposta else None,
    }
    out["alerta"] = None
    if sobre > 0 and sub > 0 and abs(out["volume_liquido"]) < 0.1 * volume_projetado:
        out["alerta"] = ("Sobrelavra e sublavra coexistem e quase se cancelam em volume: "
                         "o líquido esconde diluição por estéril E perda de minério. "
                         "Reportar os dois separadamente.")
    return out


def compliance_to_plan(lavrado_em_plano: float, planejado_nao_lavrado: float,
                       lavrado_nao_planejado: float) -> dict:
    """Compliance to plan espacial+temporal (Morley & Arvidson, 2017). Volumes em m³."""
    denom = lavrado_em_plano + planejado_nao_lavrado + lavrado_nao_planejado
    return {
        "lavrado_em_plano": lavrado_em_plano,
        "planejado_nao_lavrado": planejado_nao_lavrado,
        "lavrado_nao_planejado": lavrado_nao_planejado,
        "compliance": None if denom == 0 else lavrado_em_plano / denom,
    }


# ---------------------------------------------------------------- pilhas e medição

def ajuste_pilha(origem: float, enviado_a_pilhas: float, retomado_de_pilhas: float,
                 alimentacao_usina: float) -> dict:
    """Relação 'origem para alimentação da usina' ajustada por movimentação de pilha."""
    base = origem - enviado_a_pilhas + retomado_de_pilhas
    f = _razao(alimentacao_usina, base)
    return {"origem_ajustada": base, "fator": f,
            "variacao_pct": None if f is None else (f - 1) * 100}


def densidade_aparente(massa_t: float, volume_m3: float, base_umidade: str = "úmida") -> dict:
    """Densidade aparente = massa / volume. Sempre declarar a base de umidade."""
    return {"densidade_t_por_m3": _razao(massa_t, volume_m3),
            "base_umidade": base_umidade}


def empolamento(volume_in_situ: float, fator_empolamento: float,
                densidade_in_situ: float) -> dict:
    """Efeito do desmonte: massa conserva, volume aumenta, densidade aparente cai."""
    massa = volume_in_situ * densidade_in_situ
    volume_solto = volume_in_situ * (1 + fator_empolamento)
    return {"massa_t": massa, "volume_solto_m3": volume_solto,
            "densidade_aparente_solta": massa / volume_solto}


def fator_caminhao(massa_total_por_tipo: float, numero_carregamentos: int) -> float:
    """Fator de caminhão por tipo de material = massa total / nº de carregamentos."""
    if numero_carregamentos == 0:
        raise ValueError("número de carregamentos é zero")
    return massa_total_por_tipo / numero_carregamentos


# ---------------------------------------------------------------- semáforo

def semaforo(valor: float, limite_monitorar: float, limite_acao: float,
             referencia: float = 1.0) -> dict:
    """Classifica um fator em verde / laranja / vermelho.

    limites em fração do desvio absoluto em relação à referência (ex.: 0.05 = 5%).
    Os limites DEVEM vir da operação; as faixas da literatura são apenas ponto de partida
    (ver references/05-tolerancias-e-gatilhos.md).
    """
    desvio = abs(valor - referencia)
    if desvio <= limite_monitorar:
        status, acao = "verde", "Manter"
    elif desvio <= limite_acao:
        status, acao = "laranja", "Monitorar"
    else:
        status, acao = "vermelho", "Ação necessária"
    return {"valor": valor, "desvio_abs": desvio, "status": status, "acao": acao}


def tendencia(serie: Sequence[float], referencia: float = 1.0,
              n_consecutivos: int = 3) -> dict:
    """Detecta n períodos consecutivos do mesmo lado da referência.

    Uma variância isolada pode ser ruído; 3+ períodos no mesmo sentido apontam problema
    sistêmico (Fouet et al., 2009).
    """
    if not serie:
        return {"alerta": False, "motivo": "série vazia"}
    sinais = [1 if v > referencia else (-1 if v < referencia else 0) for v in serie]
    corrida, melhor, sinal_atual = 0, 0, 0
    for s in sinais:
        if s != 0 and s == sinal_atual:
            corrida += 1
        else:
            sinal_atual, corrida = s, (1 if s != 0 else 0)
        melhor = max(melhor, corrida)
    ultimo = sinais[-1]
    corrida_final = 0
    for s in reversed(sinais):
        if s == ultimo and s != 0:
            corrida_final += 1
        else:
            break
    return {
        "n_periodos": len(serie),
        "maior_corrida_mesmo_sinal": melhor,
        "corrida_atual": corrida_final,
        "sentido_atual": "acima" if ultimo > 0 else ("abaixo" if ultimo < 0 else "neutro"),
        "alerta": corrida_final >= n_consecutivos,
        "motivo": (f"{corrida_final} períodos consecutivos "
                   f"{'acima' if ultimo > 0 else 'abaixo'} da referência"
                   if corrida_final >= n_consecutivos else
                   "sem corrida suficiente para caracterizar tendência sistêmica"),
    }


# ---------------------------------------------------------------- entrada JSON / CLI

def _no_de_dict(d: dict) -> No:
    return No(nome=d["nome"], massa=d.get("massa"), teor=d.get("teor"),
              metal=d.get("metal"), teor_unidade=d.get("teor_unidade", "g/t"),
              metal_unidade=d.get("metal_unidade", "oz"))


def processar(entrada: dict) -> dict:
    """Processa um dicionário de entrada. Estrutura esperada:

    {
      "site": "<nome do site>",
      "periodo": "2026-08",
      "nos": [{"nome": "...", "massa": 1000, "teor": 1.2, "teor_unidade": "%"}, ...],
      "indicadores_proativos": {"longo_prazo": "...", "curto_prazo": "...",
                                "planejamento": "...", "operacao": "...",
                                "alimentacao_usina": "...", "produtos_usina": "..."},
      "compliance": {"lavrado_em_plano": 1400, "planejado_nao_lavrado": 200,
                     "lavrado_nao_planejado": 700},
      "overbreak": {"volume_projetado": ..., "volume_lavrado": ..., "volume_em_projeto": ...},
      "limites": {"monitorar": 0.05, "acao": 0.10}
    }
    """
    nos = [_no_de_dict(d) for d in entrada.get("nos", [])]
    por_nome = {n.nome: n for n in nos}
    lim = entrada.get("limites", {"monitorar": 0.05, "acao": 0.10})

    resultado = {"site": entrada.get("site"), "periodo": entrada.get("periodo"),
                 "nos": [asdict(n) for n in nos]}

    if len(nos) >= 2:
        elos = cadeia(nos)
        for e in elos:
            if e["fator_metal"] is not None:
                e["semaforo_metal"] = semaforo(e["fator_metal"], lim["monitorar"], lim["acao"])
        resultado["relacoes"] = elos

    ip = entrada.get("indicadores_proativos")
    if ip:
        try:
            resultado["indicadores_proativos"] = indicadores_proativos(
                longo_prazo=por_nome[ip["longo_prazo"]],
                curto_prazo=por_nome[ip["curto_prazo"]],
                planejamento=por_nome[ip["planejamento"]],
                operacao=por_nome[ip["operacao"]],
                alimentacao_usina=por_nome.get(ip.get("alimentacao_usina", "")),
                produtos_usina=por_nome.get(ip.get("produtos_usina", "")),
                base=ip.get("base", "metal"),
            )
        except KeyError as exc:
            resultado["indicadores_proativos"] = {"erro": f"nó não encontrado: {exc}"}

    if entrada.get("compliance"):
        resultado["compliance_to_plan"] = compliance_to_plan(**entrada["compliance"])
    if entrada.get("overbreak"):
        resultado["overbreak_underbreak"] = overbreak_underbreak(**entrada["overbreak"])
    if entrada.get("pilhas"):
        resultado["ajuste_pilha"] = ajuste_pilha(**entrada["pilhas"])
    if entrada.get("serie_mensal"):
        resultado["tendencia"] = tendencia(entrada["serie_mensal"])

    return resultado


# ---------------------------------------------------------------- exemplo e autoteste

def exemplo_chieregati() -> dict:
    """Exemplo verificado da literatura (Chieregati, 2023) — mina de ouro subterrânea."""
    lp = No("Modelo de longo prazo", massa=80000, teor=2.76, metal=7100)
    cp = No("Modelo de curto prazo", massa=80000, teor=2.55, metal=6560)
    pl = No("Planejamento", massa=75000, teor=2.70, metal=6510)
    op = No("Operação (lavrado)", massa=75000, teor=2.42, metal=5840)
    pu = No("Produtos da usina", metal=5040)
    return indicadores_proativos(lp, cp, pl, op, alimentacao_usina=op, produtos_usina=pu)


def autoteste() -> bool:
    ok = True

    def check(nome, obtido, esperado, tol=0.005):
        nonlocal ok
        bom = obtido is not None and abs(obtido - esperado) <= tol
        ok = ok and bom
        print(f"  [{'OK ' if bom else 'FALHA'}] {nome}: {obtido:.4f} (esperado ~{esperado})")

    print("Exemplo Chieregati (2023), base metal:")
    ind = exemplo_chieregati()["indicadores"]
    check("GM", ind["GM"], 0.92)
    check("MP", ind["MP"], 0.99)
    check("MO", ind["MO"], 0.90)
    check("MM", ind["MM"], 0.89)
    check("MR", ind["MR"], 0.82)
    check("PR", ind["PR"], 0.86)
    check("MCF", ind["MCF"], 0.71)

    print("Diluição/recuperação do mesmo exemplo:")
    d = diluicao_recuperacao(75000, 71000, 4000, 75000, 2.70, 2.42)
    check("recuperação de minério", d["recuperacao_minerio_massa"], 0.95)
    check("diluição (massa)", d["diluicao_massa"], 0.0533)
    check("diluição (teor)", d["diluicao_teor"], 0.1037)

    print("Compliance to plan (Morley & Arvidson, 2017):")
    check("caso 100%", compliance_to_plan(1600, 0, 0)["compliance"], 1.00)
    check("caso 61%", compliance_to_plan(1400, 200, 700)["compliance"], 0.6087)

    print("Variação orçamento -> usina (Morley & Arvidson, 2017, Tabela 1):")
    a = No("Orçamento", massa=4974000, teor=3.45)
    b = No("Usina recebido", massa=5172960, teor=3.64)
    check("variação de massa %", fator(a, b)["var_massa_pct"], 4.0, tol=0.05)

    print("Empolamento (Morley & Arvidson, 2017):")
    e = empolamento(370.4, 0.35, 2.7)
    check("densidade aparente solta", e["densidade_aparente_solta"], 2.0, tol=0.01)

    print("Sobrelavra/sublavra:")
    o = overbreak_underbreak(1000, 1000, 900)
    check("overbreak %", o["overbreak_pct"], 0.10)
    check("underbreak %", o["underbreak_pct"], 0.10)
    assert o["alerta"] is not None, "deveria alertar compensação"
    print("  [OK ] alerta de compensação sobrelavra/sublavra disparado")

    print("Média ponderada:")
    check("teor ponderado", media_ponderada([2.0, 4.0], [1000, 3000]), 3.5)

    print("Tendência:")
    t = tendencia([0.95, 0.94, 0.93])
    assert t["alerta"], "deveria alertar tendência"
    print("  [OK ] 3 períodos consecutivos abaixo -> alerta")

    print("\nRESULTADO:", "TODOS OS TESTES PASSARAM" if ok else "HÁ FALHAS")
    return ok


def main():
    p = argparse.ArgumentParser(description="Cálculos de reconciliação de lavra")
    p.add_argument("--input", help="arquivo JSON de entrada")
    p.add_argument("--out", help="arquivo JSON de saída")
    p.add_argument("--exemplo", action="store_true", help="roda o exemplo da literatura")
    p.add_argument("--autoteste", action="store_true", help="valida as fórmulas")
    a = p.parse_args()

    if a.autoteste:
        raise SystemExit(0 if autoteste() else 1)
    if a.exemplo:
        print(json.dumps(exemplo_chieregati(), indent=2, ensure_ascii=False))
        return
    if not a.input:
        p.error("informe --input, --exemplo ou --autoteste")

    with open(a.input, encoding="utf-8") as fh:
        entrada = json.load(fh)
    resultado = processar(entrada)
    texto = json.dumps(resultado, indent=2, ensure_ascii=False)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(texto)
        print(f"resultados salvos em {a.out}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
