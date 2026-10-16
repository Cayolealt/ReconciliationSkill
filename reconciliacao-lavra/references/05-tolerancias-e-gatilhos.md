# Tolerâncias, gatilhos de ação e confiança na reconciliação

## A resposta honesta sobre "qual o limite aceitável?"

Não existe resposta universal. Fouet et al. (2009) são explícitos:

> "Infelizmente isto é algo que não pode ser generalizado. Você reage quando um fator desvia 10%,
> dois desvios-padrão, ou outro valor estatisticamente válido? Igualmente válido seria reagir quando
> uma tendência de três ou mais desvios similares é registrada. Cada mina terá seu próprio nível de
> ruído a filtrar; padrões aparecerão com o tempo e cada site precisará trabalhar seus gatilhos de
> ação conforme as variáveis locais."

A faixa aceitável depende de: complexidade geológica, commodity, método de lavra, precisão dos
sistemas de medição e **categoria do recurso** (Inferido × Indicado × Medido). Ao responder ao
usuário sobre tolerância, **nunca inventar um número**: apresentar as referências abaixo como ponto
de partida e recomendar que a mina estabeleça seus próprios gatilhos a partir do histórico e de
análise estatística.

## Faixas de referência da literatura

### Acurácia esperada por etapa da cadeia (Crawford, 2004)

Do fluxograma geral de reconciliação de mina até venda:

| Ponto de balanço | Acurácia esperada |
|---|---|
| Minério lavrado (massa, teor, unidades de metal) | ±5% a 10% |
| Diluição — estéril (massa, teor, unidades de metal) | ±5% a 10% |
| Perdas de minério (massa, teor, unidades de metal) | ±5% a 10% |
| Estéril | ±5% |
| Minério estocado em pilha | ±5% a 10% |
| **Minério moído (massa, teor, unidades de metal)** | **±2% a 5%** |
| Rejeito | ±2% a 5% |
| **Concentrado — embarque, fundição (massa, teor, umidade, metal)** | **±0,5% a 1%** |
| Perdas de produto | ±0,5% a 1% |

**Critério global de Crawford (2004)**: dependendo da commodity e do método de lavra, uma
reconciliação completa deve dar conta de perdas, diluição e produção com **não mais que 7% a 12% ao
ano**. Erros acima dessa faixa devem ser analisados para determinar e corrigir suas causas.
"Os melhores operadores insistirão em reconciliação ainda mais apertada."

### Faixas normais dos dados de entrada

A tabela mestra de fontes de erro em `04-fontes-de-erro.md` é a outra referência quantitativa: se
uma relação desvia dentro da faixa "normal" da fonte de dado que a domina, o desvio pode ser ruído
de medição, não sinal geológico ou operacional.

### Escala e agregação (Schofield, Moore & Carswell, 2013)

A correlação entre modelo de recursos e modelo de controle de teor é **pobre no painel individual e
melhora progressivamente com o volume agregado**. No caso Macraes:

- painel de 25×25×2,5 m (~2.000 t): correlação ruim
- 50×50×5 m (~15.000 t): melhor
- 100×200×20 m (~400.000 t, ≈1 mês de lavra): há **20% de chance de o pacote resultar em déficit de
  20% ou pior**
- pacotes agregados até ~1.000.000 t (2-3 meses): estimativas bem menos erráticas

**Implicação direta**: cobrar aderência mensal de um modelo de recursos em escala de bloco é
tecnicamente incorreto. Ao avaliar um desvio, sempre perguntar **em que escala** ele está sendo
medido e se essa escala é adequada ao modelo em questão.

## Regra de reação — tendência, não ponto isolado

> "O foco não deve estar em reagir a cada ponto de dado que cai fora do limite. O verdadeiro poder do
> sistema está em identificar e investigar **tendências ao longo do tempo**. Uma variância mensal
> isolada pode ser ruído estatístico; três meses consecutivos de variância negativa no mesmo
> indicador apontam para um problema sistêmico." (JORC guidelines / Fouet et al., 2009.)

Padrões a procurar (Morley & Arvidson, 2017):
- **tendências** que indicam que parte do processo está em risco;
- **oscilações ou comportamento periódico** que refletem mudança planejada ou não planejada no processo;
- outro comportamento **"irregular"** que indique problema ou oportunidade.

> "Os indicadores apenas apontam uma diferença; eles não resolvem o problema. É preciso intervenção
> humana para isso. Se os sites não conseguem ou não querem interrogar a variância reportada pelos
> fatores, estão perdendo tempo ao reportá-los." (Fouet et al., 2009.)

## Semáforo de status (Morley & Arvidson, 2017)

Classificação usada nos dashboards MVCR da Anglo American, aplicada a resultados trimestrais e
anualizados:

| Cor | Status | Significado | Ação |
|---|---|---|---|
| 🟢 Verde | Processo controlado | Dentro dos limites acordados | **Manter** |
| 🟠 Laranja | Tendência de sair do controle | Algo pode estar saindo de controle | **Monitorar** |
| 🔴 Vermelho | Processo fora de controle | Relação saiu de controle | **Ação necessária** |

O relatório deve incluir, para todo resultado laranja ou vermelho: conclusões, recomendações e a
**lista de ações** planejadas ou em andamento. Gráficos mostram tendência mês a mês em janela móvel
de 12 meses.

## Ranking de confiança na reconciliação (Arvidson, 2015, apud Morley & Arvidson, 2017)

Autoavaliação qualitativa que mede **o quanto se pode confiar no próprio processo de reconciliação**
— não o resultado, mas a maturidade do sistema. Reportar rotineiramente junto com os indicadores.

| # | Critério | Peso |
|---|---|---|
| 1 | Champion designado e gerindo ativamente o processo | 10% |
| 2 | Nós e relações mapeados e acordados | 10% |
| 3 | Sistemas de medição instalados em todos os nós | 10% |
| 4 | QA/QC das medições (dado demonstradamente de qualidade aceitável) | 20% |
| 5 | Gestão de dados e reporte em sistema de banco de dados comercial | 20% |
| 6 | Workshop multifuncional realizado para discutir resultados e acordar ações | 10% |
| 7 | Ações em dia | 10% |
| 8 | Relatório mensal formalmente aprovado pela gestão sênior | 10% |

Escala por critério: 1 = 0% completo · 2 = 25% · 3 = 50% · 4 = 75% · 5 = 100% completo.
Nota final = Σ (escore/5 × peso). Exemplo do artigo: escores 5,5,5,5,4,4,5,4 → **rating 92%**.

Note que **40% do peso está em qualidade de dado e sistema de gestão de dados** — coerente com o
princípio de que reconciliação sem dado confiável é atividade inútil.

Uso na skill: quando o usuário pedir avaliação de maturidade, ou quando um relatório precisar
contextualizar seus próprios resultados, aplicar este ranking e reportar a nota junto com a
trajetória (o artigo mostra uma mina indo de "sem sistema de reconciliação" a 92% em 12 meses).

## Como um site deve estabelecer seus próprios gatilhos

Sequência recomendada, sintetizada das fontes:

1. Reunir o histórico da relação (mínimo 12-24 meses, na granularidade em que será monitorada).
2. Caracterizar o ruído: média e desvio-padrão da variação; identificar sazonalidade (chuva/seca
   afeta umidade, fator de caminhão, densidade).
3. Comparar a dispersão observada com a faixa "normal" esperada das fontes de dado que dominam a
   relação (`04-fontes-de-erro.md`) e com as faixas de Crawford (2004) por etapa.
4. Definir limite de **monitoramento** (laranja) e de **ação** (vermelho) — tipicamente limites de
   controle estatístico, mas ajustados ao que a operação consegue efetivamente medir.
5. Definir a **regra de tendência** (ex.: 3 períodos consecutivos do mesmo lado, mesmo dentro do
   limite, dispara investigação).
6. Documentar tudo no Código de Prática (`06-codigo-de-pratica.md`) e revisar anualmente.
7. Registrar tolerâncias **diferentes por relação, por site e por categoria de recurso** — não usar
   um único número para tudo.

**Ao gerar relatórios**: se a mina ainda não tem gatilhos formalizados, dizer isso explicitamente no
relatório, usar as faixas da literatura como referência provisória (citando a fonte) e recomendar a
formalização. Nunca apresentar um limite de literatura como se fosse o limite oficial da operação.
