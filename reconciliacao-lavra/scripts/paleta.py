# -*- coding: utf-8 -*-
"""Paleta da skill de reconciliação — instância de referência, validada.

Para adotar a identidade visual da sua empresa, **troque apenas os valores deste
arquivo** e revalide o contraste e a separação para daltonismo. Se você tiver a skill
`dataviz` disponível, o validador dela faz isso:

    node scripts/validate_palette.js "<hex,hex,...>" --mode light  --surface <sua superfície clara>
    node scripts/validate_palette.js "<hex,hex,...>" --mode dark   --surface <sua superfície escura>

Nenhum outro arquivo precisa mudar: `graficos.py` consome apenas os papéis definidos aqui.

Estado da validação desta instância (superfícies #fcfcfb / #1a1a19):
  4 séries categóricas, pares adjacentes .... PASS claro e escuro
      (claro: WARN de contraste em aqua e amarelo -> regra de alívio: rótulos diretos, aplicada)
  2 categorias, todos os pares ............. PASS claro e escuro
"""

CATEGORICA = {  # ordem FIXA — nunca ciclar, nunca reordenar por ranking
    "claro": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
              "#e87ba4", "#008300", "#4a3aa7", "#e34948"],
    "escuro": ["#3987e5", "#d95926", "#199e70", "#c98500",
               "#d55181", "#008300", "#9085e9", "#e66767"],
}

# Divergente para incremento/decremento no waterfall: azul (ganho) <-> vermelho (perda)
DIVERGENTE = {
    "claro":  {"positivo": "#2a78d6", "negativo": "#d03b3b", "neutro": "#f0efec"},
    "escuro": {"positivo": "#3987e5", "negativo": "#e66767", "neutro": "#383835"},
}

# Status — reservado, nunca reutilizado como série. Sempre com ícone + rótulo.
STATUS = {"bom": "#0ca30c", "atencao": "#fab219", "grave": "#ec835a", "critico": "#d03b3b"}

CROMO = {
    "claro": {"superficie": "#fcfcfb", "plano": "#f9f9f7", "tinta": "#0b0b0b",
              "tinta2": "#52514e", "mudo": "#898781", "grade": "#e1e0d9",
              "eixo": "#c3c2b7", "borda": "rgba(11,11,11,0.10)"},
    "escuro": {"superficie": "#1a1a19", "plano": "#0d0d0d", "tinta": "#ffffff",
               "tinta2": "#c3c2b7", "mudo": "#898781", "grade": "#2c2c2a",
               "eixo": "#383835", "borda": "rgba(255,255,255,0.10)"},
}

FONTE = 'system-ui, -apple-system, "Segoe UI", sans-serif'


def serie(i, modo="claro"):
    """Cor da i-ésima série. Estoura de propósito acima de 8: a 9ª série não existe —
    agrupe em 'Outros', facete, ou use múltiplos pequenos."""
    cores = CATEGORICA[modo]
    if i >= len(cores):
        raise ValueError("mais de 8 séries: agrupe em 'Outros' ou use múltiplos pequenos "
                         "em vez de gerar uma cor nova")
    return cores[i]
