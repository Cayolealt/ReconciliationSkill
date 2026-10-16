# -*- coding: utf-8 -*-
"""Gráficos de reconciliação — três formas que fazem trabalho que tabela não faz.

    1. waterfall_cadeia .......... onde o metal entra e sai ao longo da cadeia de valor
    2. tendencia ................. fator mês a mês, com referência e faixa, para ver TENDÊNCIA
    3. overbreak_underbreak ...... barras divergentes que expõem a reconciliação ilusória

Cada uma renderiza em dois destinos, porque servem a usos diferentes:

    saida="png"   -> arquivo estático de alta resolução, para embutir no relatório paginado
    saida="html"  -> SVG embutido com hover, legenda, tabela de dados e modo escuro,
                     para o painel que a pessoa abre e navega

**Pergunte ao usuário qual destino ele quer antes de gerar** — os dois são legítimos e
servem a coisas distintas. Se ele quiser os dois, gere os dois.

Cores vêm de `paleta.py`, que é o único arquivo a trocar para adotar outra identidade
visual. A paleta atual está validada (ver cabeçalho de paleta.py).

Regras que este módulo respeita e que não devem ser afrouxadas:
  - um eixo só; nunca dois eixos y
  - cor segue a entidade, nunca o ranking; ordem fixa das séries
  - legenda sempre presente com 2+ séries, e rótulo direto com até 4
  - texto em tinta, nunca na cor da série
  - grade e eixos recessivos
"""
from __future__ import annotations

import html
import math
from typing import Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from paleta import CATEGORICA, DIVERGENTE, CROMO, serie
from tema import aplicar_matplotlib, ESCALA, TRACO, FIGURA, FONTE_CSS

MESES_ABREV = {"janeiro":"jan","fevereiro":"fev","março":"mar","abril":"abr","maio":"mai",
               "junho":"jun","Julho":"jul","julho":"jul","Agosto":"ago","agosto":"ago",
               "setembro":"set","outubro":"out","novembro":"nov","dezembro":"dez"}


def _fmt_mil(v, _=None):
    if abs(v) >= 1000: return f"{v:,.0f}".replace(",", ".")
    if abs(v) >= 10:   return f"{v:,.0f}"
    return f"{v:,.1f}".replace(".", ",")


def _mpl(modo):
    """Delega ao tema: um único lugar governa fonte, escala, traço e espaçamento."""
    return aplicar_matplotlib(modo)


# ══════════════════════════════════════════════════ 1. WATERFALL
def waterfall_cadeia(nos: Sequence[tuple], titulo: str, unidade: str = "t Cu",
                     saida: str = "png", arquivo: str = "waterfall.png",
                     modo: str = "claro", subtitulo: str = "") -> str:
    """Waterfall do metal contido ao longo da cadeia de valor.

    nos: sequência de (rótulo, valor, tipo) onde tipo é 'total' (barra ancorada no zero)
         ou 'delta' (incremento flutuante entre o total anterior e o próximo).
         Passe apenas os nós que existem — nó ausente não vira zero.

    Por que waterfall: a pergunta é "onde o metal entra e sai", que é polaridade
    decomposta, não magnitude. Barra simples por nó responderia a pergunta errada.
    """
    c = _mpl(modo); d = DIVERGENTE[modo]
    rot = [n[0] for n in nos]; val = [n[1] for n in nos]; tip = [n[2] for n in nos]

    base, acum = [], 0.0
    for v, t in zip(val, tip):
        if t == "total":
            base.append(0.0); acum = v
        else:
            base.append(acum if v >= 0 else acum + v); acum += v

    fig, ax = plt.subplots(figsize=FIGURA["waterfall"], dpi=200)
    for i,(v,t,b) in enumerate(zip(val,tip,base)):
        cor = c["eixo"] if t=="total" else (d["positivo"] if v>=0 else d["negativo"])
        ax.bar(i, abs(v) if t=="delta" else v, bottom=b, width=0.62,
               color=cor, edgecolor=c["superficie"], linewidth=1.6, zorder=3)
        topo = (b+abs(v)) if t=="delta" else v
        txt = _fmt_mil(v) if t=="total" else f"{'+' if v>=0 else '-'}{_fmt_mil(abs(v))}"
        ax.text(i, topo + max(map(abs,val))*0.022, txt, ha="center", va="bottom",
                fontsize=ESCALA["marca"], color=c["tinta"], zorder=4,
                fontweight="bold" if t=="total" else "normal")
    # conectores
    for i in range(len(nos)-1):
        y = (base[i]+abs(val[i])) if tip[i]=="delta" else val[i]
        ax.plot([i+0.31, i+1-0.31], [y,y], color=c["eixo"], lw=0.9, ls=(0,(3,3)), zorder=2)

    ax.set_xticks(range(len(rot)))
    ax.set_xticklabels(["\n".join(_quebra(r, 13)) for r in rot], fontsize=7.6)
    ax.set_ylabel(unidade, fontsize=ESCALA["eixo_rot"])
    ax.yaxis.set_major_formatter(FuncFormatter(_fmt_mil))
    ax.grid(axis="x", visible=False)
    ax.axhline(0, color=c["eixo"], lw=0.9)
    ax.set_title(titulo, fontsize=ESCALA["titulo"], color=c["tinta"], loc="left", pad=18, fontweight="bold")
    if subtitulo:
        ax.text(0,1.035, subtitulo, transform=ax.transAxes, fontsize=ESCALA["subtitulo"], color=c["tinta2"])
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=d["positivo"], label="acréscimo"),
                       Patch(color=d["negativo"], label="perda"),
                       Patch(color=c["eixo"], label="nó da cadeia")],
              frameon=False, fontsize=8, loc="upper right", ncol=3,
              bbox_to_anchor=(1.0,1.16))
    fig.tight_layout(); fig.savefig(arquivo, bbox_inches="tight"); plt.close(fig)
    return arquivo


# ══════════════════════════════════════════════════ 2. TENDÊNCIA
def tendencia(series: dict, titulo: str, saida: str = "png", arquivo: str = "tendencia.png",
              modo: str = "claro", referencia: float = 1.0, faixa: float = 0.10,
              rotulo_faixa: str = "", subtitulo: str = "") -> str:
    """Fator mês a mês por entidade, com linha de referência e faixa.

    series: {"nome da entidade": {"mês": valor, ...}} — ordem de inserção define a cor,
            e a cor segue a entidade mesmo que o conjunto filtrado mude.

    A faixa NÃO é a tolerância da operação a menos que o usuário a tenha definido.
    Passe `rotulo_faixa` deixando claro de onde ela vem.
    """
    c = _mpl(modo)
    nomes = list(series.keys())
    if len(nomes) > 4:
        raise ValueError("mais de 4 séries numa linha do tempo: use múltiplos pequenos "
                         "ou agrupe — rótulo direto deixa de caber e a leitura cai")
    meses = list(dict.fromkeys([m for s in series.values() for m in s.keys()]))
    x = range(len(meses))

    fig, ax = plt.subplots(figsize=FIGURA["tendencia"], dpi=200)
    if faixa:
        ax.axhspan(referencia-faixa, referencia+faixa, color=c["grade"], zorder=1)

    ax.axhline(referencia, color=c["eixo"], lw=1.2, zorder=2)

    for i, nome in enumerate(nomes):
        cor = serie(i, modo)
        ys = [series[nome].get(m) for m in meses]
        xs = [j for j,v in enumerate(ys) if v is not None]
        vs = [v for v in ys if v is not None]
        ax.plot(xs, vs, color=cor, lw=TRACO["linha_serie"], zorder=4, solid_capstyle="round")
        ax.scatter(xs, vs, s=TRACO["marcador"], color=cor, edgecolor=c["superficie"], lw=1.6, zorder=5)
        # rótulo direto (obrigatório: cumpre a regra de alívio do contraste e evita cor-só)
        ax.annotate(nome, (xs[-1], vs[-1]), textcoords="offset points", xytext=(9,0),
                    fontsize=ESCALA["serie"], color=c["tinta2"], va="center", fontweight="bold")

    ax.set_xticks(list(x)); ax.set_xticklabels([MESES_ABREV.get(m,m[:3]) for m in meses], fontsize=8.4)
    ax.set_ylabel("fator (metal)", fontsize=ESCALA["eixo_rot"])
    ax.set_xlim(-0.4, len(meses)-1+1.9)
    ax.grid(axis="x", visible=False)
    ax.set_title(titulo, fontsize=ESCALA["titulo"], color=c["tinta"], loc="left", pad=18, fontweight="bold")
    if subtitulo:
        ax.text(0,1.035, subtitulo, transform=ax.transAxes, fontsize=ESCALA["subtitulo"], color=c["tinta2"])
    if rotulo_faixa:
        ax.text(0, -0.155, rotulo_faixa, transform=ax.transAxes, fontsize=7.4, color=c["mudo"])
    fig.tight_layout(); fig.savefig(arquivo, bbox_inches="tight"); plt.close(fig)
    return arquivo


# ══════════════════════════════════════════════════ 3. OVERBREAK × UNDERBREAK
def overbreak_underbreak(dados: dict, titulo: str, saida: str = "png",
                         arquivo: str = "obub.png", modo: str = "claro",
                         unidade: str = "t", subtitulo: str = "") -> str:
    """Barras divergentes: sublavra à esquerda, sobrelavra à direita, cada lado
    aberto em minério e estéril.

    dados: {"overbreak_minerio":t, "overbreak_esteril":t,
            "underbreak_minerio":t, "underbreak_esteril":t}

    Esta é a forma que mata a reconciliação ilusória: as duas barras grandes em
    sentidos opostos e o líquido minúsculo no meio ficam evidentes de imediato,
    o que um indicador líquido esconde por construção.
    Cor = tipo de material (identidade, categórica). Lado = sobrelavra/sublavra (posição).
    """
    c = _mpl(modo)
    cor_min, cor_est = serie(0, modo), serie(1, modo)
    ob_m, ob_e = dados["overbreak_minerio"], dados["overbreak_esteril"]
    ub_m, ub_e = dados["underbreak_minerio"], dados["underbreak_esteril"]
    liquido = (ob_m+ob_e) - (ub_m+ub_e)

    fig, ax = plt.subplots(figsize=FIGURA["divergente"], dpi=200)
    y_ob, y_ub = 1.0, 0.0
    ax.barh(y_ob, ob_m, height=0.46, color=cor_min, zorder=3,
            edgecolor=c["superficie"], linewidth=1.6)
    ax.barh(y_ob, ob_e, left=ob_m, height=0.46, color=cor_est, zorder=3,
            edgecolor=c["superficie"], linewidth=1.6)
    ax.barh(y_ub, -ub_m, height=0.46, color=cor_min, zorder=3,
            edgecolor=c["superficie"], linewidth=1.6)
    ax.barh(y_ub, -ub_e, left=-ub_m, height=0.46, color=cor_est, zorder=3,
            edgecolor=c["superficie"], linewidth=1.6)

    esc = max(ob_m+ob_e, ub_m+ub_e)
    for y, tot, sinal in [(y_ob, ob_m+ob_e, 1), (y_ub, -(ub_m+ub_e), -1)]:
        ax.text(tot + sinal*esc*0.02, y, _fmt_mil(abs(tot)), va="center",
                ha="left" if sinal>0 else "right", fontsize=9, fontweight="bold",
                color=c["tinta"], zorder=4)
    for y, seg, off, lab in [(y_ob, ob_m, ob_m/2, "minério"), (y_ob, ob_e, ob_m+ob_e/2, "estéril"),
                             (y_ub, ub_m, -ub_m/2, "minério"), (y_ub, ub_e, -(ub_m+ub_e/2), "estéril")]:
        if seg > esc*0.09:
            ax.text(off, y, _fmt_mil(seg), va="center", ha="center", fontsize=8,
                    color="#ffffff", zorder=5, fontweight="bold")

    ax.axvline(0, color=c["eixo"], lw=1.1, zorder=2)
    ax.set_yticks([y_ub, y_ob]); ax.set_yticklabels(["Sublavra\n(underbreak)","Sobrelavra\n(overbreak)"],
                                                    fontsize=8.8, color=c["tinta"])
    ax.set_xlabel(f"massa ({unidade})", fontsize=ESCALA["eixo_rot"])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_: _fmt_mil(abs(v))))
    ax.set_xlim(-esc*1.22, esc*1.22); ax.set_ylim(-0.55, 1.62)
    ax.grid(axis="y", visible=False)
    ax.set_title(titulo, fontsize=ESCALA["titulo"], color=c["tinta"], loc="left", pad=18, fontweight="bold")
    sub = subtitulo or f"líquido: {_fmt_mil(liquido)} {unidade} — é isso que um indicador agregado enxerga"
    ax.text(0, 1.055, sub, transform=ax.transAxes, fontsize=ESCALA["subtitulo"], color=c["tinta2"])
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=cor_min, label="minério"), Patch(color=cor_est, label="estéril")],
              frameon=False, fontsize=8.2, loc="upper right", ncol=2, bbox_to_anchor=(1.0,1.19))
    fig.tight_layout(); fig.savefig(arquivo, bbox_inches="tight"); plt.close(fig)
    return arquivo


# ══════════════════════════════════════════════════ PAINEL HTML
_CSS = ("""
.viz{color-scheme:light;--sup:#fcfcfb;--plano:#f9f9f7;--tinta:#0b0b0b;--tinta2:#52514e;
--mudo:#898781;--grade:#e1e0d9;--eixo:#c3c2b7;--borda:rgba(11,11,11,.10);
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--pos:#2a78d6;--neg:#d03b3b;
font-family:__FONTE__;background:var(--plano);
color:var(--tinta);padding:22px;max-width:1080px;margin:0 auto}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])) .viz{color-scheme:dark;
--sup:#1a1a19;--plano:#0d0d0d;--tinta:#fff;--tinta2:#c3c2b7;--mudo:#898781;--grade:#2c2c2a;
--eixo:#383835;--borda:rgba(255,255,255,.10);--s1:#3987e5;--s2:#d95926;--s3:#199e70;
--s4:#c98500;--pos:#3987e5;--neg:#e66767}}
:root[data-theme="dark"] .viz{color-scheme:dark;--sup:#1a1a19;--plano:#0d0d0d;--tinta:#fff;
--tinta2:#c3c2b7;--mudo:#898781;--grade:#2c2c2a;--eixo:#383835;--borda:rgba(255,255,255,.10);
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--pos:#3987e5;--neg:#e66767}
.viz h1{font-size:20px;margin:0 0 4px;font-weight:700}
.viz .lead{color:var(--tinta2);font-size:13px;margin:0 0 22px;line-height:1.5}
.viz figure{background:var(--sup);border:1px solid var(--borda);border-radius:10px;
padding:16px 18px 12px;margin:0 0 20px}
.viz figcaption{font-size:15px;font-weight:700;margin-bottom:2px}
.viz .sub{font-size:12px;color:var(--tinta2);margin-bottom:12px;line-height:1.45}
.viz svg{display:block;width:100%;height:auto;overflow:visible}
.viz .leg{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--tinta2);
margin:10px 0 0;align-items:center}
.viz .leg i{width:11px;height:11px;border-radius:3px;display:inline-block;margin-right:6px;
vertical-align:-1px}
.viz details{margin-top:10px;font-size:12px}
.viz summary{cursor:pointer;color:var(--tinta2);padding:4px 0}
.viz table{border-collapse:collapse;margin-top:8px;font-size:11.5px;width:100%}
.viz th,.viz td{border-bottom:1px solid var(--grade);padding:5px 8px;text-align:right}
.viz th:first-child,.viz td:first-child{text-align:left}
.viz th{color:var(--tinta2);font-weight:600}
.viz .tip{position:fixed;pointer-events:none;background:var(--sup);color:var(--tinta);
border:1px solid var(--borda);border-radius:7px;padding:7px 10px;font-size:12px;
box-shadow:0 4px 14px rgba(0,0,0,.14);opacity:0;transition:opacity .1s;z-index:9;
line-height:1.45;white-space:nowrap}
.viz .hit{fill:transparent;cursor:crosshair}
.viz .zoomwrap{position:relative;overflow:auto;border:1px solid var(--borda);
border-radius:8px;background:var(--sup);padding:8px}
.viz .zoomwrap svg{width:auto;max-width:none;transform-origin:0 0;transition:transform .12s}
.viz .zoomctl{display:flex;gap:6px;align-items:center;margin:8px 0 2px;font-size:12px;
color:var(--tinta2)}
.viz .zoomctl button{font:inherit;font-weight:600;color:var(--tinta);background:var(--plano);
border:1px solid var(--borda);border-radius:6px;padding:3px 10px;cursor:pointer;line-height:1.4}
.viz .zoomctl button:hover{background:var(--grade)}
.viz .zoomctl span{color:var(--mudo)}
.viz .nota{font-size:11.5px;color:var(--mudo);margin-top:14px;line-height:1.5}
""".replace("__FONTE__", FONTE_CSS))

_JS = """
(function(){var t=document.createElement('div');t.className='tip';document.body.appendChild(t);
document.querySelectorAll('.viz [data-tip]').forEach(function(el){
 el.addEventListener('pointerenter',function(e){t.innerHTML=el.getAttribute('data-tip');t.style.opacity=1});
 el.addEventListener('pointermove',function(e){t.style.left=(e.clientX+14)+'px';
   t.style.top=(e.clientY-10)+'px'});
 el.addEventListener('pointerleave',function(){t.style.opacity=0});});
document.querySelectorAll('.viz .zoomwrap').forEach(function(w){
 var svg=w.querySelector('svg'); if(!svg) return;
 var base=w.clientWidth-18, nat=svg.viewBox.baseVal.width||base, z=Math.min(1,base/nat);
 var ctl=w.parentNode.querySelector('.zoomctl'), lab=ctl&&ctl.querySelector('span');
 function ap(){svg.style.transform='scale('+z+')';
  svg.style.height=(svg.viewBox.baseVal.height*z)+'px';
  if(lab) lab.textContent=Math.round(z*100)+'%';}
 if(ctl){ctl.querySelector('[data-z="+"]').onclick=function(){z=Math.min(3,z*1.25);ap()};
  ctl.querySelector('[data-z="-"]').onclick=function(){z=Math.max(.2,z/1.25);ap()};
  ctl.querySelector('[data-z="fit"]').onclick=function(){z=Math.min(1,(w.clientWidth-18)/nat);ap()};
  ctl.querySelector('[data-z="1"]').onclick=function(){z=1;ap()};}
 ap();});})();
"""


def _tabela_html(cab, linhas):
    th = "".join(f"<th>{html.escape(str(c))}</th>" for c in cab)
    tr = "".join("<tr>"+"".join(f"<td>{html.escape(str(c))}</td>" for c in l)+"</tr>"
                 for l in linhas)
    return f"<details><summary>Ver dados em tabela</summary><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></details>"


def _svg_waterfall(nos, unidade):
    W,H,ML,MR,MT,MB = 940,300,66,20,16,58
    pw,ph = W-ML-MR, H-MT-MB
    val=[n[1] for n in nos]; tip=[n[2] for n in nos]
    base=[];acum=0.0
    for v,t in zip(val,tip):
        if t=="total": base.append(0.0); acum=v
        else: base.append(acum if v>=0 else acum+v); acum+=v
    topos=[(b+abs(v)) if t=="delta" else v for v,t,b in zip(val,tip,base)]
    ymax=max(topos+[0])*1.12; ymin=min(base+[0])
    esc=lambda y:MT+ph-(y-ymin)/(ymax-ymin)*ph
    bw=pw/len(nos)*0.6; step=pw/len(nos)
    p=[f'<line x1="{ML}" y1="{esc(0):.1f}" x2="{W-MR}" y2="{esc(0):.1f}" stroke="var(--eixo)" stroke-width="1"/>']
    for i,(r,v,t) in enumerate(nos):
        x=ML+step*i+(step-bw)/2; y0=esc(base[i]); y1=esc(topos[i])
        cor="var(--eixo)" if t=="total" else ("var(--pos)" if v>=0 else "var(--neg)")
        txt=_fmt_mil(v) if t=="total" else f"{'+' if v>=0 else '-'}{_fmt_mil(abs(v))}"
        p.append(f'<rect x="{x:.1f}" y="{min(y0,y1):.1f}" width="{bw:.1f}" '
                 f'height="{max(abs(y1-y0),2):.1f}" rx="3" fill="{cor}" '
                 f'stroke="var(--sup)" stroke-width="2" data-tip="<b>{html.escape(r)}</b><br>{txt} {unidade}"/>')
        p.append(f'<text x="{x+bw/2:.1f}" y="{min(y0,y1)-6:.1f}" text-anchor="middle" '
                 f'font-size="10.5" fill="var(--tinta)" font-weight="{700 if t=="total" else 400}">{txt}</text>')
        for k,ln in enumerate(_quebra(r,15)):
            p.append(f'<text x="{x+bw/2:.1f}" y="{MT+ph+16+k*11:.1f}" text-anchor="middle" '
                     f'font-size="9.5" fill="var(--mudo)">{html.escape(ln)}</text>')
        if i<len(nos)-1:
            p.append(f'<line x1="{x+bw:.1f}" y1="{y1:.1f}" x2="{ML+step*(i+1)+(step-bw)/2:.1f}" '
                     f'y2="{y1:.1f}" stroke="var(--eixo)" stroke-width="1" stroke-dasharray="3 3"/>')
    p.append(f'<text x="{ML-8}" y="{MT+8}" text-anchor="end" font-size="9.5" fill="var(--mudo)">{unidade}</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img">{"".join(p)}</svg>'


def _quebra(txt,n):
    out,linha=[],""
    for w in txt.split():
        if len(linha+" "+w)<=n or not linha: linha=(linha+" "+w).strip()
        else: out.append(linha); linha=w
    out.append(linha); return out[:2]


def _svg_tendencia(series, meses, referencia, faixa):
    W,H,ML,MR,MT,MB=940,290,52,104,14,40
    pw,ph=W-ML-MR,H-MT-MB
    vals=[v for s in series.values() for v in s.values() if v is not None]
    ymin,ymax=min(vals+[referencia-faixa])*0.97,max(vals+[referencia+faixa])*1.03
    ex=lambda i:ML+(pw/(max(len(meses)-1,1)))*i
    ey=lambda v:MT+ph-(v-ymin)/(ymax-ymin)*ph
    p=[f'<rect x="{ML}" y="{ey(referencia+faixa):.1f}" width="{pw}" '
       f'height="{abs(ey(referencia-faixa)-ey(referencia+faixa)):.1f}" fill="var(--grade)"/>',
       f'<line x1="{ML}" y1="{ey(referencia):.1f}" x2="{ML+pw}" y2="{ey(referencia):.1f}" '
       f'stroke="var(--eixo)" stroke-width="1.2"/>']
    for i,m in enumerate(meses):
        p.append(f'<text x="{ex(i):.1f}" y="{MT+ph+18}" text-anchor="middle" font-size="10" '
                 f'fill="var(--mudo)">{MESES_ABREV.get(m,m[:3])}</text>')
    for k,(nome,s) in enumerate(series.items()):
        cor=f"var(--s{k+1})"
        pts=[(ex(i),ey(s[m])) for i,m in enumerate(meses) if s.get(m) is not None]
        if not pts: continue
        p.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" '
                 f'fill="none" stroke="{cor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        for i,m in enumerate(meses):
            v=s.get(m)
            if v is None: continue
            p.append(f'<circle cx="{ex(i):.1f}" cy="{ey(v):.1f}" r="4" fill="{cor}" '
                     f'stroke="var(--sup)" stroke-width="1.8" data-tip="<b>{html.escape(nome)}</b><br>'
                     f'{MESES_ABREV.get(m,m)}: {v:.3f}".replace(".",",")/>')
        p.append(f'<text x="{pts[-1][0]+10:.1f}" y="{pts[-1][1]+4:.1f}" font-size="11" '
                 f'font-weight="600" fill="var(--tinta2)">{html.escape(nome)}</text>')
    for v in [ymin,referencia,ymax]:
        p.append(f'<text x="{ML-8}" y="{ey(v)+3:.1f}" text-anchor="end" font-size="9.5" '
                 f'fill="var(--mudo)">{("%.2f"%v).replace(".",",")}</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img">{"".join(p)}</svg>'


def _svg_obub(d, unidade):
    W,H,MC,MT=940,190,470,20
    ob_m,ob_e=d["overbreak_minerio"],d["overbreak_esteril"]
    ub_m,ub_e=d["underbreak_minerio"],d["underbreak_esteril"]
    esc=max(ob_m+ob_e,ub_m+ub_e); k=360/esc; bh=42
    p=[f'<line x1="{MC}" y1="{MT-6}" x2="{MC}" y2="{H-24}" stroke="var(--eixo)" stroke-width="1.2"/>']
    def barra(y,segs,sinal):
        off=0
        for val,cor,lab in segs:
            w=val*k; x=MC+off*sinal if sinal>0 else MC-(off+val)*k
            x = MC+off*k if sinal>0 else MC-(off+val)*k
            p.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w,1):.1f}" height="{bh}" rx="3" '
                     f'fill="{cor}" stroke="var(--sup)" stroke-width="2" '
                     f'data-tip="<b>{lab}</b><br>{_fmt_mil(val)} {unidade}"/>')
            if w>52: p.append(f'<text x="{x+w/2:.1f}" y="{y+bh/2+4}" text-anchor="middle" '
                              f'font-size="10.5" font-weight="700" fill="#fff">{_fmt_mil(val)}</text>')
            off+=val
        tot=sum(s[0] for s in segs)
        tx=MC+tot*k+10 if sinal>0 else MC-tot*k-10
        p.append(f'<text x="{tx:.1f}" y="{y+bh/2+5}" text-anchor="{"start" if sinal>0 else "end"}" '
                 f'font-size="12.5" font-weight="700" fill="var(--tinta)">{_fmt_mil(tot)}</text>')
    barra(MT,[(ob_m,"var(--s1)","Sobrelavra · minério"),(ob_e,"var(--s2)","Sobrelavra · estéril")],1)
    barra(MT+bh+26,[(ub_m,"var(--s1)","Sublavra · minério"),(ub_e,"var(--s2)","Sublavra · estéril")],-1)
    p.append(f'<text x="{MC+8}" y="{MT-9}" font-size="11" fill="var(--tinta2)" font-weight="600">SOBRELAVRA →</text>')
    p.append(f'<text x="{MC-8}" y="{MT+bh+18}" font-size="11" fill="var(--tinta2)" '
             f'font-weight="600" text-anchor="end">← SUBLAVRA</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img">{"".join(p)}</svg>'


def painel_html(arquivo: str, titulo: str, lead: str, figuras: list) -> str:
    """Painel HTML autocontido com os gráficos em SVG, hover, legenda e tabela de dados.

    figuras: lista de dicts com {tipo, titulo, sub, dados, legenda, tabela, nota}
             tipo em {"waterfall","tendencia","obub"}
    """
    partes=[]
    for f in figuras:
        if f["tipo"]=="waterfall":
            svg=_svg_waterfall(f["dados"]["nos"], f["dados"].get("unidade","t"))
        elif f["tipo"]=="tendencia":
            svg=_svg_tendencia(f["dados"]["series"], f["dados"]["meses"],
                               f["dados"].get("referencia",1.0), f["dados"].get("faixa",0.10))
        elif f["tipo"]=="diagrama":
            svg=f["dados"]["svg"]
        else:
            svg=_svg_obub(f["dados"], f["dados"].get("unidade","t"))
        leg="".join(f'<span><i style="background:{c}"></i>{html.escape(n)}</span>'
                    for n,c in f.get("legenda",[]))
        tab=_tabela_html(*f["tabela"]) if f.get("tabela") else ""
        nota=f'<p class="nota">{f["nota"]}</p>' if f.get("nota") else ""
        if f["tipo"]=="diagrama":
            corpo=('<div class="zoomctl"><button data-z="-">&minus;</button>'
                   '<button data-z="+">+</button><button data-z="fit">ajustar</button>'
                   '<button data-z="1">100%</button><span></span>'
                   '<em style="font-style:normal;color:var(--mudo);margin-left:6px">'
                   'arraste para percorrer</em></div>'
                   f'<div class="zoomwrap">{svg}</div>')
        else:
            corpo=svg
        partes.append(f'<figure><figcaption>{html.escape(f["titulo"])}</figcaption>'
                      f'<p class="sub">{f.get("sub","")}</p>{corpo}'
                      f'<div class="leg">{leg}</div>{tab}{nota}</figure>')
    doc=(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
         f'<meta name="viewport" content="width=device-width,initial-scale=1">'
         f'<title>{html.escape(titulo)}</title><style>{_CSS}</style></head><body>'
         f'<div class="viz"><h1>{html.escape(titulo)}</h1><p class="lead">{lead}</p>'
         f'{"".join(partes)}</div><script>{_JS}</script></body></html>')
    open(arquivo,"w",encoding="utf-8").write(doc)
    return arquivo


# ══════════════════════════════════════════════════ 4. DIAGRAMA DA CADEIA
def diagrama_cadeia(faixas: list, indicadores: list, titulo: str, unidade: str = "t",
                    arquivo: str = "cadeia.png", modo: str = "claro", subtitulo: str = "",
                    credito: str = "") -> str:
    """Esquema da cadeia de valor com os indicadores calculados sobre ela.

    Estrutura de referência: Joscil Spitzner Galvão (2020, rev. 2023), baseado em
    Ana Carolina Chieregati (2011) — ver references/10-cadeia-padrao.md.
    Passe o crédito em `credito` sempre que reproduzir o modelo.

    faixas: [{"nome": "RECURSO", "nos": [{"rot": "...", "valor": 11272.0, "nota": "opcional"},
                                          {"rot": "...", "valor": None}]}, ...]
             valor None desenha o nó como ausente — nunca como zero.
    indicadores: [{"sigla":"GM", "valor":1.067, "de":(faixa,i), "para":(faixa,j),
                   "motivo":"..."}]  valor None => não calculável, e `motivo` diz qual nó falta.
    """
    c = _mpl(modo)
    from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrow
    n_faixas = len(faixas)
    largura_total = sum(len(f["nos"]) for f in faixas)
    fig, ax = plt.subplots(figsize=(max(11.5, largura_total*1.6), 5.3), dpi=200)
    ax.set_xlim(0, largura_total*1.55 + 0.35*n_faixas + 1.0); ax.set_ylim(0.2, 7.9)
    ax.axis("off"); ax.grid(False)

    Y_NO, H_NO = 1.55, 1.35
    Y_IND = 4.75
    pos = {}
    x = 0.35
    for fi, f in enumerate(faixas):
        x0 = x
        for ni, no in enumerate(f["nos"]):
            w = 1.35
            ausente = no.get("valor") is None
            cor_fundo = c["superficie"] if not ausente else c["grade"]
            cor_borda = c["eixo"] if not ausente else c["mudo"]
            ax.add_patch(FancyBboxPatch((x, Y_NO), w, H_NO, boxstyle="round,pad=0.03,rounding_size=0.08",
                         facecolor=cor_fundo, edgecolor=cor_borda,
                         linewidth=1.3 if not ausente else 1.0,
                         linestyle="-" if not ausente else (0,(3,2)), zorder=3))
            for k, ln in enumerate(_quebra(no["rot"], 15)):
                ax.text(x+w/2, Y_NO+H_NO-0.24-k*0.24, ln, ha="center", va="center",
                        fontsize=7.1, color=c["tinta"] if not ausente else c["mudo"],
                        zorder=4, fontweight="bold")
            txt = _fmt_mil(no["valor"]) if not ausente else "sem dado"
            ax.text(x+w/2, Y_NO+0.30, txt, ha="center", va="center", fontsize=8.6,
                    color=c["tinta"] if not ausente else c["mudo"], zorder=4,
                    fontweight="bold" if not ausente else "normal")
            if no.get("nota"):
                ax.text(x+w/2, Y_NO-0.26, no["nota"], ha="center", va="top", fontsize=6.3,
                        color=c["mudo"], zorder=4)
            pos[(fi, ni)] = (x+w/2, Y_NO, Y_NO+H_NO)
            x += w + 0.2
        ax.add_patch(FancyBboxPatch((x0-0.16, Y_NO-0.62), (x-0.2)-x0+0.32, H_NO+1.0,
                     boxstyle="round,pad=0.02,rounding_size=0.1", facecolor="none",
                     edgecolor=c["eixo"], linewidth=1.0, zorder=2))
        ax.text(x0-0.10, Y_NO+H_NO+0.24, f["nome"], fontsize=8.2, color=c["tinta2"],
                fontweight="bold", va="bottom")
        x += 0.5

    # indicadores
    for ind in indicadores:
        xa = pos[ind["de"]][0]; xb = pos[ind["para"]][0]
        xm = (xa+xb)/2
        calc = ind.get("valor") is not None
        cor = c["tinta"] if calc else c["mudo"]
        ax.add_patch(Ellipse((xm, Y_IND), 1.5, 0.92,
                     facecolor=c["superficie"] if calc else c["grade"],
                     edgecolor=cor, linewidth=1.4 if calc else 1.0,
                     linestyle="-" if calc else (0,(3,2)), zorder=5))
        ax.text(xm, Y_IND+0.16, ind["sigla"], ha="center", va="center", fontsize=11,
                fontweight="bold", color=cor, zorder=6)
        ax.text(xm, Y_IND-0.22, (f"{ind['valor']:.3f}".replace(".",",") if calc else "n/d"),
                ha="center", va="center", fontsize=9.2, color=cor, zorder=6,
                fontweight="bold" if calc else "normal")
        if not calc and ind.get("motivo"):
            ax.text(xm, Y_IND-0.72, ind["motivo"], ha="center", va="top", fontsize=6.2,
                    color=c["mudo"], zorder=6)
        for xt in (xa, xb):
            ax.annotate("", xy=(xt, pos[ind["de"]][2]+0.06), xytext=(xm, Y_IND-0.46),
                        arrowprops=dict(arrowstyle="-|>", color=cor, lw=1.0,
                                        linestyle="-" if calc else (0,(2,2)),
                                        shrinkA=2, shrinkB=2), zorder=4)

    ax.text(0.35, 7.62, titulo, fontsize=13.5, fontweight="bold", color=c["tinta"], va="top")
    if subtitulo:
        ax.text(0.35, 7.02, subtitulo, fontsize=8.6, color=c["tinta2"], va="top")
    if credito:
        ax.text(0.35, 0.42, credito, fontsize=6.8, color=c["mudo"], va="bottom", style="italic")
    ax.text(largura_total*1.55 + 0.35*n_faixas + 0.9, 0.42, f"valores em {unidade}", fontsize=7,
            color=c["mudo"], va="bottom", ha="right")
    fig.tight_layout(); fig.savefig(arquivo, bbox_inches="tight"); plt.close(fig)
    return arquivo
