# Template — Relatório de Reconciliação de Lavra

Estrutura padrão do relatório. Preencher com os dados do período; **remover seções que não se
aplicam** em vez de deixá-las vazias, e declarar explicitamente o que faltou.
Toda fórmula ou faixa de referência citada leva a fonte (autor, ano).

---

# Relatório de Reconciliação — {SITE} — {PERÍODO}

**Emitido em:** {data} · **Responsável:** {nome/função} · **Aprovação:** {gestão sênior}
**Escopo:** {sites incluídos} · **Base:** {massa seca/úmida; unidades de teor e metal}

## 1. Sumário executivo

Três a cinco frases. O que aconteceu, qual o elo crítico, qual a ação principal, qual a
materialidade. Sem jargão desnecessário — este bloco é lido pela gestão.

| Indicador | Resultado | Status | Tendência (12 m) |
|---|---|---|---|
| MR — Reconciliação mina | {x,xx} | 🟢/🟠/🔴 | ↗/→/↘ |
| PR — Reconciliação planta | {x,xx} | | |
| MCF | {x,xx} | | |
| Compliance to plan | {xx%} | | |

## 2. Dados de entrada e sua confiabilidade

| Fonte de dado | Origem/sistema | Período | QA/QC aplicado | Transformações | Limitação conhecida |
|---|---|---|---|---|---|

Declarar aqui, sem rodeios:
- o que estava **faltando** e como foi tratado;
- premissas assumidas (densidade, fator de caminhão, umidade, latência de pilha);
- qualquer dado que não pôde ser validado.

## 3. Resultados por relação de reconciliação

Usar a **nomenclatura descritiva** ("Fonte A para Fonte B"), nunca F1/R2/M3 como nome primário.
Reportar sempre **massa, teor e metal**.

| Relação | Massa | Teor | Metal | Status |
|---|---|---|---|---|
| Modelo de recursos para modelo de controle de teor | | | | |
| Modelo de controle de teor para produção de lavra | | | | |
| Produção de lavra para alimentação da usina | | | | |
| Alimentação da usina para produção da usina | | | | |

### 3.1 Indicadores pró-ativos

| Indicador | O que mede | Resultado | Status |
|---|---|---|---|
| GM | Modelo de longo prazo → curto prazo | | |
| MP | Curto prazo → planejamento | | |
| MO | Planejamento → operação | | |
| MM | Curto prazo → operação (MP × MO) | | |
| MR | Longo prazo → alimentação da usina | | |
| PR | Alimentação → produtos da usina | | |
| MCF | Longo prazo → produtos (MR × PR) | | |

**Elo crítico do período:** {indicador} — {por quê}.

> Verificação obrigatória de reconciliação ilusória: indicadores intermediários divergindo em
> sentidos opostos com um agregado próximo de 1,00 devem ser sinalizados aqui, mesmo que o MCF
> pareça bom.

## 4. Compliance to plan (espacial e temporal)

| Categoria | Volume (m³) | % |
|---|---|---|
| Lavrado em plano | | |
| Planejado não lavrado | | |
| Lavrado não planejado | | |
| **Compliance** | | **{xx%}** |

Narrativa: onde e por que a lavra saiu do plano no período.

## 5. Sobrelavra e sublavra

| Painel/realce | Vol. projetado | Vol. lavrado | Sobrelavra | Sublavra | ELOS (m) | Impacto |
|---|---|---|---|---|---|---|

Reportar sempre os dois **separadamente** — o líquido esconde diluição por estéril combinada com
perda de minério.

## 6. Diluição, recuperação de minério e perdas

| Métrica | Planejado | Realizado | Desvio |
|---|---|---|---|
| Recuperação de minério (massa) | | | |
| Diluição (massa) | | | |
| Diluição (teor) | | | |
| Perda de minério | | | |

## 7. Análise e diagnóstico

Para cada indicador fora de controle:

**{Indicador} — {resultado}**
- **O que o número diz:** …
- **Escala e ruído:** o desvio cabe dentro da faixa de erro esperada da fonte de dado dominante?
  (referência: {fonte, ano})
- **É tendência?** {n} períodos consecutivos no mesmo sentido.
- **Hipóteses de causa raiz:** …
- **Verificação contra a realidade física do período:** {o que de fato aconteceu na mina}
- **Confiança na conclusão:** alta / média / baixa — e por quê.

## 8. Ações

| # | Ação (SMART) | Causa que endereça | Responsável | Prazo | Valor estimado | Status |
|---|---|---|---|---|---|---|

Registrar explicitamente que a ação nasceu da análise de reconciliação, para permitir o rastreio
posterior do valor gerado.

## 9. Confiança no próprio processo de reconciliação

Autoavaliação (Arvidson, 2015): {nota %}. Critérios com menor pontuação e o que está sendo feito.

## 10. Limitações e premissas

Lista honesta do que este relatório **não** consegue afirmar com os dados disponíveis.

## 11. Fontes metodológicas

Referências usadas para fórmulas, faixas e critérios deste relatório.
