#!/usr/bin/env python3
"""
Normaliza dados de reconciliação vindos de planilhas para o JSON que reconciliacao.py consome.

Os dados de reconciliação chegam em formatos muito variados (uma aba por site, colunas em
português ou inglês, teores em % ou g/t, massas em t ou kt, cabeçalhos em linhas quaisquer).
Este script faz a leitura tolerante e mostra o que entendeu, para que o mapeamento possa ser
conferido ANTES de qualquer cálculo — reconciliação com dado mal lido é pior que nenhuma.

Uso:
    python normalizar_entrada.py --arquivo producao.xlsx --listar
    python normalizar_entrada.py --arquivo producao.xlsx --aba <aba> --mapa mapa.json --out dados.json

O `mapa.json` associa colunas do arquivo aos campos do modelo, por exemplo:
    {"nome": "Etapa", "massa": "Massa (t)", "teor": "Cu (%)", "teor_unidade": "%",
     "metal_unidade": "t"}
"""
from __future__ import annotations

import argparse
import json
import sys

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    print("pandas não instalado. Rode: pip install pandas openpyxl --break-system-packages",
          file=sys.stderr)
    raise

# sinônimos comuns encontrados em planilhas de produção brasileiras e internacionais
SINONIMOS = {
    "nome": ["etapa", "no", "nó", "node", "fonte", "origem", "estagio", "estágio",
             "descricao", "descrição", "item", "modelo"],
    "massa": ["massa", "massa (t)", "tonelagem", "toneladas", "ton", "t", "tonnes",
              "tonnage", "massa umida", "massa seca", "massa (kt)"],
    "teor": ["teor", "teor (%)", "grade", "cu (%)", "au (g/t)", "teor cu", "teor au",
             "teor medio", "teor médio", "%cu", "g/t"],
    "metal": ["metal", "metal contido", "contained metal", "onças", "oncas", "oz",
              "cu contido", "au contido", "metal (t)"],
}


def _norm(s: str) -> str:
    return str(s).strip().lower().replace("_", " ")


def sugerir_mapa(colunas) -> dict:
    """Sugere um mapeamento coluna -> campo com base em sinônimos. Sempre revisar."""
    sugestao = {}
    normalizadas = {_norm(c): c for c in colunas}
    for campo, alternativas in SINONIMOS.items():
        for alt in alternativas:
            if alt in normalizadas:
                sugestao[campo] = normalizadas[alt]
                break
        else:
            for chave, original in normalizadas.items():
                if any(alt in chave for alt in alternativas):
                    sugestao[campo] = original
                    break
    return sugestao


def listar(arquivo: str) -> None:
    if arquivo.lower().endswith((".xlsx", ".xlsm", ".xls")):
        xl = pd.ExcelFile(arquivo)
        print(f"Abas em {arquivo}:")
        for aba in xl.sheet_names:
            df = xl.parse(aba, nrows=8)
            print(f"\n--- {aba} ({len(df.columns)} colunas) ---")
            print(df.head(8).to_string())
            print("Mapa sugerido:", json.dumps(sugerir_mapa(df.columns), ensure_ascii=False))
    else:
        df = pd.read_csv(arquivo, nrows=8, sep=None, engine="python")
        print(df.head(8).to_string())
        print("Mapa sugerido:", json.dumps(sugerir_mapa(df.columns), ensure_ascii=False))


def converter(arquivo: str, aba: str | None, mapa: dict, site: str | None,
              periodo: str | None, escala_massa: float = 1.0) -> dict:
    if arquivo.lower().endswith((".xlsx", ".xlsm", ".xls")):
        df = pd.read_excel(arquivo, sheet_name=aba or 0)
    else:
        df = pd.read_csv(arquivo, sep=None, engine="python")

    nos = []
    for _, linha in df.iterrows():
        nome = linha.get(mapa.get("nome", ""), None)
        if pd.isna(nome):
            continue
        no = {"nome": str(nome).strip()}
        for campo in ("massa", "teor", "metal"):
            col = mapa.get(campo)
            if col and col in df.columns and not pd.isna(linha[col]):
                valor = float(linha[col])
                if campo == "massa":
                    valor *= escala_massa
                no[campo] = valor
        no["teor_unidade"] = mapa.get("teor_unidade", "g/t")
        no["metal_unidade"] = mapa.get("metal_unidade", "oz")
        nos.append(no)

    return {"site": site, "periodo": periodo, "nos": nos,
            "_origem": {"arquivo": arquivo, "aba": aba, "mapa": mapa,
                        "escala_massa": escala_massa}}


def main():
    p = argparse.ArgumentParser(description="Normaliza planilhas para o formato de reconciliacao.py")
    p.add_argument("--arquivo", required=True)
    p.add_argument("--aba")
    p.add_argument("--mapa", help="arquivo JSON com o mapeamento coluna->campo")
    p.add_argument("--site")
    p.add_argument("--periodo")
    p.add_argument("--escala-massa", type=float, default=1.0,
                   help="multiplicador de massa (ex.: 1000 se a planilha está em kt)")
    p.add_argument("--listar", action="store_true", help="inspeciona abas, colunas e sugere mapa")
    p.add_argument("--out")
    a = p.parse_args()

    if a.listar:
        listar(a.arquivo)
        return

    mapa = json.load(open(a.mapa, encoding="utf-8")) if a.mapa else {}
    if not mapa:
        df = (pd.read_excel(a.arquivo, sheet_name=a.aba or 0)
              if a.arquivo.lower().endswith((".xlsx", ".xlsm", ".xls"))
              else pd.read_csv(a.arquivo, sep=None, engine="python"))
        mapa = sugerir_mapa(df.columns)
        print(f"AVISO: usando mapa sugerido automaticamente: {mapa}", file=sys.stderr)
        print("Confirme com o usuário antes de usar os resultados.", file=sys.stderr)

    saida = converter(a.arquivo, a.aba, mapa, a.site, a.periodo, a.escala_massa)
    texto = json.dumps(saida, indent=2, ensure_ascii=False)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(texto)
        print(f"salvo em {a.out}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
