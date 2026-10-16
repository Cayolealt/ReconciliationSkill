# -*- coding: utf-8 -*-
"""Tema visual da skill — o que faz gráfico, fluxograma e relatório parecerem um sistema só.

`paleta.py` governa COR (e é validada). Este arquivo governa todo o resto: tipografia,
escala, espaçamento, raio, espessura de traço e proporção. Os três destinos leem daqui —
PNG do relatório, painel HTML e o corpo do PDF — de modo que uma mudança aqui vale para tudo.

**Para adotar a identidade visual da empresa, troque `paleta.py` e este arquivo. Só.**

Princípios que os valores abaixo materializam:
  · escala tipográfica com poucos degraus, para hierarquia clara sem ruído
  · respiro generoso: densidade é o inimigo de leitura confortável
  · grade e eixo recessivos — o dado é o que deve ter contraste, não a moldura
  · rótulo direto perto da marca em vez de legenda distante, sempre que couber
  · complexidade se resolve com múltiplos pequenos, nunca acumulando séries num eixo
"""

# ── Tipografia ────────────────────────────────────────────────────────────────
# Carlito é metricamente compatível com Calibri: sai igual em qualquer máquina e dá
# ao documento aparência de peça corporativa, não de saída automática de script.
FONTE = "Carlito"
FONTE_FALLBACK = ["Carlito", "Calibri", "DejaVu Sans", "sans-serif"]
FONTE_CSS = 'Carlito, Calibri, system-ui, -apple-system, "Segoe UI", sans-serif'
FONTE_PDF = "Helvetica"          # base do reportlab; ver registrar_fonte_pdf()

# Escala tipográfica — poucos degraus, proporção ~1,2
ESCALA = {
    "titulo":     14.0,
    "subtitulo":   9.0,
    "eixo_rot":    9.0,   # rótulo do eixo
    "eixo_val":    8.5,   # números do eixo
    "marca":       8.5,   # valor sobre a marca
    "serie":       9.0,   # rótulo direto da série
    "legenda":     8.5,
    "nota":        7.5,
    "credito":     7.0,
}
PESO_TITULO = "bold"

# ── Espaçamento e proporção ───────────────────────────────────────────────────
FIGURA = {                    # (largura, altura) em polegadas, por forma
    "waterfall":  (10.4, 4.9),
    "tendencia":  (10.4, 4.6),
    "divergente": (10.4, 3.5),
    "faceta":     (3.3, 2.5),  # por painel de múltiplo pequeno
}
DPI = 200
PAD_TITULO = 18               # respiro entre título e área de plotagem
PAD_SUBTITULO = 0.045         # fração da altura dos eixos
MARGEM_ROTULO = 0.022         # folga do valor acima da marca, fração da escala

# ── Marcas ────────────────────────────────────────────────────────────────────
TRACO = {
    "linha_serie":  2.0,
    "marcador":     26,       # área do ponto
    "borda_marca":  1.6,      # anel na cor da superfície, separa marcas adjacentes
    "grade":        0.6,
    "eixo":         0.9,
    "referencia":   1.2,
}
RAIO = 3                      # canto arredondado da extremidade da barra
LARGURA_BARRA = 0.62          # fração do passo
GAP_MARCA = 2                 # px de superfície entre marcas adjacentes

# ── Diagrama (fluxograma da cadeia) ──────────────────────────────────────────
DIAGRAMA = {
    "no_largura":    150,
    "no_altura":     78,
    "no_raio":       9,
    "no_gap":        18,
    "faixa_pad":     16,
    "faixa_raio":    12,
    "ind_rx":        52,      # raio horizontal da elipse do indicador
    "ind_ry":        30,
    "traco_no":      1.4,
    "traco_faixa":   1.0,
    "sombra":        True,    # sombra suave sob nós e indicadores
    "gradiente":     True,    # gradiente sutil no preenchimento das faixas
}

# ── Aplicação ─────────────────────────────────────────────────────────────────
def aplicar_matplotlib(modo="claro"):
    """Configura o matplotlib com o tema. Chame antes de criar qualquer figura."""
    import matplotlib.pyplot as plt
    from paleta import CROMO
    c = CROMO[modo]
    plt.rcParams.update({
        "figure.facecolor": c["superficie"], "axes.facecolor": c["superficie"],
        "savefig.facecolor": c["superficie"], "savefig.dpi": DPI,
        "text.color": c["tinta"], "axes.labelcolor": c["tinta2"],
        "xtick.color": c["mudo"], "ytick.color": c["mudo"],
        "axes.edgecolor": c["eixo"], "grid.color": c["grade"],
        "font.family": "sans-serif", "font.sans-serif": FONTE_FALLBACK,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.linewidth": TRACO["grade"], "axes.axisbelow": True,
        "axes.titlesize": ESCALA["titulo"], "axes.labelsize": ESCALA["eixo_rot"],
        "xtick.labelsize": ESCALA["eixo_val"], "ytick.labelsize": ESCALA["eixo_val"],
        "legend.fontsize": ESCALA["legenda"], "legend.frameon": False,
        "xtick.major.size": 0, "ytick.major.size": 0,
    })
    return c


def registrar_fonte_pdf():
    """Registra Carlito no reportlab para o corpo do relatório casar com os gráficos.

    Devolve o nome da família a usar, ou 'Helvetica' se a fonte não for encontrada —
    nunca falha, porque um relatório sem a fonte ideal ainda é um relatório.
    """
    import glob
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping
    achados = {}
    for var, alvo in [("Regular", ""), ("Bold", "-Bold"),
                      ("Italic", "-Italic"), ("BoldItalic", "-BoldItalic")]:
        for pad in (f"/usr/share/fonts/**/Carlito-{var}.ttf",):
            g = glob.glob(pad, recursive=True)
            if g: achados[var] = g[0]
    if "Regular" not in achados:
        return "Helvetica"
    try:
        pdfmetrics.registerFont(TTFont("Carlito", achados["Regular"]))
        for var, nome, b, i in [("Bold","Carlito-Bold",1,0), ("Italic","Carlito-Italic",0,1),
                                ("BoldItalic","Carlito-BoldItalic",1,1)]:
            if var in achados:
                pdfmetrics.registerFont(TTFont(nome, achados[var]))
                addMapping("Carlito", b, i, nome)
        addMapping("Carlito", 0, 0, "Carlito")
        return "Carlito"
    except Exception:
        return "Helvetica"
