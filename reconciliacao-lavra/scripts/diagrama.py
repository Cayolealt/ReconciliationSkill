# -*- coding: utf-8 -*-
"""Fluxograma da cadeia de valor em SVG.

Motor separado do de gráficos de propósito: matplotlib é biblioteca de plotagem e é
excelente do básico ao complexo em gráfico estatístico, mas é o teto do diagrama —
lá se desenha caixa por caixa com primitivas. SVG dá gradiente, sombra, canto e faixa
em camadas de graça, renderiza nativo no painel HTML, e converte para PNG de alta
resolução para o relatório paginado. Cada motor no que ele é bom; `tema.py` e
`paleta.py` são o que fazem os dois parecerem a mesma coisa.

    from diagrama import cadeia_valor
    cadeia_valor(faixas, indicadores, "título", arquivo="cadeia.svg")   # SVG
    cadeia_valor(faixas, indicadores, "título", arquivo="cadeia.png")   # PNG via cairosvg

Estrutura de referência da cadeia: Joscil Spitzner Galvão (2020, rev. 2023), baseada em
Ana Carolina Chieregati (2011). Passe o crédito em `credito` ao reproduzir o modelo.
"""
from __future__ import annotations

import html

from paleta import CROMO, CATEGORICA, DIVERGENTE
from tema import DIAGRAMA as D, ESCALA, FONTE_CSS


def _mil(v):
    if v is None: return "sem dado"
    if abs(v) >= 1000: return f"{v:,.0f}".replace(",", ".")
    if abs(v) >= 10:   return f"{v:,.0f}"
    return f"{v:,.1f}".replace(".", ",")


def _quebra(txt, n=17, maxl=3):
    out, linha = [], ""
    for w in str(txt).split():
        if len(linha + " " + w) <= n or not linha:
            linha = (linha + " " + w).strip()
        else:
            out.append(linha); linha = w
    out.append(linha)
    return out[:maxl]


def cadeia_valor(faixas: list, indicadores: list, titulo: str, arquivo: str,
                 unidade: str = "t", subtitulo: str = "", credito: str = "",
                 modo: str = "claro", escala_png: float = 2.4,
                 escala_texto: float = 1.0) -> str:
    """Desenha a cadeia com os indicadores calculados sobre ela.

    escala_texto: multiplicador da tipografia do diagrama. Use 1.0 no painel HTML, onde a
            largura é livre; use ~1.7 quando o desenho for reduzido para caber na largura de
            uma página — sem isso o rótulo do nó cai abaixo de 4 pt e deixa de ser legível.
            A regra: texto final na página nunca abaixo de 6 pt.

    faixas: [{"nome":"RECURSO", "nos":[{"rot":..., "valor":float|None, "nota":str}]}]
            valor None desenha o nó como ausente — nunca como zero.
    indicadores: [{"sigla":"GM","valor":float|None,"de":(f,i),"para":(f,j),"motivo":str}]
            valor None => não calculável; `motivo` nomeia o nó que falta.
    """
    c = CROMO[modo]
    E = {k: v * escala_texto for k, v in ESCALA.items()}
    NW = D["no_largura"]; NH = D["no_altura"]*max(1.0, escala_texto*0.92); GAP = D["no_gap"]
    PAD, FR = D["faixa_pad"], D["faixa_raio"]

    # ── geometria
    ft = max(1.0, escala_texto)
    y_titulo, y_sub = 34*ft, 58*ft
    y_ind = 112*ft
    y_faixa = y_ind + D["ind_ry"]*ft + 78*ft
    y_no = y_faixa + 30*ft
    H = y_no + NH + 84*ft

    x, pos, faixas_geo = PAD + 4, {}, []
    for fi, f in enumerate(faixas):
        x0 = x
        for ni, no in enumerate(f["nos"]):
            pos[(fi, ni)] = (x + NW / 2, y_no)
            x += NW + GAP
        faixas_geo.append((x0 - PAD, (x - GAP) + PAD - (x0 - PAD), f["nome"]))
        x += 34
    W = x + PAD

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" font-family=\'{FONTE_CSS}\'>')
    # defs: sombra e gradientes
    s.append('<defs>')
    s.append('<filter id="sh" x="-30%" y="-30%" width="160%" height="180%">'
             '<feDropShadow dx="0" dy="1.5" stdDeviation="2.2" flood-opacity="0.13"/></filter>')
    s.append('<filter id="shi" x="-40%" y="-40%" width="180%" height="200%">'
             '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.16"/></filter>')
    s.append(f'<linearGradient id="gno" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{c["superficie"]}"/>'
             f'<stop offset="1" stop-color="{c["plano"]}"/></linearGradient>')
    s.append(f'<linearGradient id="gfaixa" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{c["grade"]}" stop-opacity="0.55"/>'
             f'<stop offset="1" stop-color="{c["grade"]}" stop-opacity="0.18"/></linearGradient>')
    s.append(f'<linearGradient id="gind" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{c["superficie"]}"/>'
             f'<stop offset="1" stop-color="{c["plano"]}"/></linearGradient>')
    s.append('</defs>')
    s.append(f'<rect width="{W}" height="{H}" fill="{c["superficie"]}"/>')

    # ── título
    s.append(f'<text x="{PAD+4}" y="{y_titulo}" font-size="{E["titulo"]+4.5}" '
             f'font-weight="700" fill="{c["tinta"]}">{html.escape(titulo)}</text>')
    if subtitulo:
        for k, ln in enumerate(_quebra(subtitulo, 150, 2)):
            s.append(f'<text x="{PAD+4}" y="{y_sub+k*15*ft}" font-size="{E["subtitulo"]+1.5}" '
                     f'fill="{c["tinta2"]}">{html.escape(ln)}</text>')

    # ── faixas
    for fx, fw, nome in faixas_geo:
        s.append(f'<rect x="{fx}" y="{y_faixa}" width="{fw}" height="{NH+60*ft}" rx="{FR}" '
                 f'fill="url(#gfaixa)" stroke="{c["eixo"]}" stroke-width="{D["traco_faixa"]}"/>')
        s.append(f'<text x="{fx+12}" y="{y_faixa+19*ft}" font-size="{E["legenda"]+0.5}" '
                 f'font-weight="700" fill="{c["tinta2"]}" letter-spacing="0.6">'
                 f'{html.escape(nome)}</text>')

    # ── nós
    for fi, f in enumerate(faixas):
        for ni, no in enumerate(f["nos"]):
            cx, cy = pos[(fi, ni)]
            x0 = cx - NW / 2
            ausente = no.get("valor") is None
            fill = "url(#gno)" if not ausente else c["grade"]
            stroke = c["eixo"] if not ausente else c["mudo"]
            dash = "" if not ausente else ' stroke-dasharray="5 3"' 
            filt = ' filter="url(#sh)"' if (D["sombra"] and not ausente) else ''
            s.append(f'<rect x="{x0}" y="{cy}" width="{NW}" height="{NH}" rx="{D["no_raio"]}" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="{D["traco_no"]}"{dash}{filt}/>')
            linhas = _quebra(no["rot"], 19, 2)
            for k, ln in enumerate(linhas):
                s.append(f'<text x="{cx}" y="{cy+17*ft+k*12.5*ft}" text-anchor="middle" '
                         f'font-size="{E["nota"]+0.7}" font-weight="600" '
                         f'fill="{c["tinta"] if not ausente else c["mudo"]}">{html.escape(ln)}</text>')
            s.append(f'<text x="{cx}" y="{cy+NH-19*ft}" text-anchor="middle" '
                     f'font-size="{E["titulo"]-1}" font-weight="{700 if not ausente else 400}" '
                     f'fill="{c["tinta"] if not ausente else c["mudo"]}">{_mil(no.get("valor"))}</text>')
            if no.get("nota"):
                for k, ln in enumerate(_quebra(no["nota"], 30, 2)):
                    s.append(f'<text x="{cx}" y="{cy+NH+13*ft+k*10*ft}" text-anchor="middle" '
                             f'font-size="{E["credito"]}" fill="{c["mudo"]}">'
                             f'{html.escape(ln)}</text>')

    # ── indicadores
    for ind in indicadores:
        xa, ya = pos[ind["de"]]; xb, _ = pos[ind["para"]]
        xm = (xa + xb) / 2
        calc = ind.get("valor") is not None
        cor = c["tinta"] if calc else c["mudo"]
        rx = max(D["ind_rx"]*ft, len(ind["sigla"]) * E["titulo"] * 0.34 + 14)
        tracejado = "" if calc else " stroke-dasharray='4 3'"
        seta = "setac" if calc else "setan"
        opac = 0.85 if calc else 0.45
        for xt in (xa, xb):
            s.append(f'<path d="M {xm} {y_ind+D["ind_ry"]*ft} C {xm} {y_ind+D["ind_ry"]*ft+34}, '
                     f'{xt} {ya-40}, {xt} {ya-5}" fill="none" stroke="{cor}" '
                     f'stroke-width="1.2" opacity="{opac}"{tracejado} '
                     f'marker-end="url(#{seta})"/>')
        filt = ' filter="url(#shi)"' if (D["sombra"] and calc) else ''
        fill_ind = "url(#gind)" if calc else c["grade"]
        tracejado_ind = "" if calc else " stroke-dasharray='5 3'"
        s.append(f'<ellipse cx="{xm}" cy="{y_ind}" rx="{rx}" ry="{D["ind_ry"]*ft}" '
                 f'fill="{fill_ind}" stroke="{cor}" '
                 f'stroke-width="{1.6 if calc else 1.1}"{tracejado_ind}{filt}/>')
        s.append(f'<text x="{xm}" y="{y_ind-3*ft}" text-anchor="middle" font-size="{E["titulo"]}" '
                 f'font-weight="700" fill="{cor}">{html.escape(ind["sigla"])}</text>')
        val_txt = (f'{ind["valor"]:.3f}'.replace(".", ",")) if calc else "n/d"
        s.append(f'<text x="{xm}" y="{y_ind+15*ft}" text-anchor="middle" '
                 f'font-size="{E["serie"]+1}" font-weight="{700 if calc else 400}" '
                 f'fill="{cor}">{val_txt}</text>')
        if not calc and ind.get("motivo"):
            s.append(f'<text x="{xm}" y="{y_ind+D["ind_ry"]*ft+15}" text-anchor="middle" '
                     f'font-size="{E["credito"]}" fill="{c["mudo"]}">'
                     f'{html.escape(ind["motivo"])}</text>')

    # marcadores de seta
    s.insert(2, f'<defs>'
                f'<marker id="setac" markerWidth="7" markerHeight="7" refX="5.5" refY="3" '
                f'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{c["tinta"]}"/></marker>'
                f'<marker id="setan" markerWidth="7" markerHeight="7" refX="5.5" refY="3" '
                f'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{c["mudo"]}"/></marker>'
                f'</defs>')

    # ── rodapé
    if credito:
        s.append(f'<text x="{PAD+4}" y="{H-16}" font-size="{E["credito"]}" '
                 f'fill="{c["mudo"]}" font-style="italic">{html.escape(credito)}</text>')
    s.append(f'<text x="{W-PAD-4}" y="{H-16}" text-anchor="end" '
             f'font-size="{E["credito"]}" fill="{c["mudo"]}">valores em {unidade}</text>')
    s.append('</svg>')
    svg = "".join(s)

    if arquivo.lower().endswith(".svg"):
        open(arquivo, "w", encoding="utf-8").write(svg)
    else:
        try:
            import cairosvg
        except ImportError:
            # Sem cairosvg (ou sem a biblioteca de sistema Cairo): entrega o SVG e avisa,
            # em vez de falhar. O SVG abre em qualquer navegador e converte depois.
            alternativo = arquivo.rsplit(".", 1)[0] + ".svg"
            open(alternativo, "w", encoding="utf-8").write(svg)
            print(f"[aviso] cairosvg indisponível — PNG não gerado; SVG salvo em {alternativo}. "
                  "Instale com `pip install cairosvg` (requer a biblioteca Cairo do sistema).")
            return alternativo
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=arquivo,
                         scale=escala_png, background_color=c["superficie"])
    return arquivo


def svg_bruto(faixas, indicadores, titulo, **kw) -> str:
    """Devolve o SVG como string, para embutir direto no painel HTML."""
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
        p = f.name
    cadeia_valor(faixas, indicadores, titulo, arquivo=p, **kw)
    txt = open(p, encoding="utf-8").read(); os.unlink(p)
    return txt
