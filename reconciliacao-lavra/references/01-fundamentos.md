# Fundamentos da reconciliação

## O que é

Reconciliação é a **comparação entre uma estimativa e uma medição em dois pontos diferentes da
sequência de lavra**, e a medida da variância entre elas (Fouet et al., 2009).

- **Estimativa**: modelo de recursos, modelo de reservas, modelo de controle de teor, plano de lavra, orçamento.
- **Medição**: levantamento topográfico/CMS, registros de movimentação de material (despacho),
  balança de correia, produção oficial da usina.

Em português (Chieregati, 2023): "comparação entre uma estimativa (modelo de recursos, modelo de
reservas, modelo de controle de teor) e uma medição (produção oficial da usina de beneficiamento
ou da metalurgia)". Resumida em três palavras: **medir, controlar e melhorar** (Noppé, 2004).

## Por que existe — os quatro objetivos

Morley (2003), reproduzidos por Chieregati (2023):

1. Medir o desempenho da operação frente às metas.
2. Confirmar a acurácia das estimativas de massa e teor.
3. Garantir que a avaliação dos ativos minerais é acurada.
4. Fornecer indicadores de desempenho (KPIs), em especial para o controle de teor.

O princípio central: **"todos os modelos estão errados; a pergunta prática é o quão errados eles
precisam estar para deixar de ser úteis"** (Box & Draper, 1987 apud Morley, 2014). Reconciliamos
para **calibrar** modelos contra resultados reais e melhorar continuamente a qualidade das previsões.
A reconciliação aponta o quão errado o modelo está; cabe ao profissional decidir qual ação tomar.

A reconciliação é o **"hub" de referência** sobre o qual o desempenho de todos os sistemas de uma
operação mineira pode ser julgado (Blucher, 2002 apud Morley, 2014).

## Os três tipos de reconciliação

| Tipo | Definição | Exemplo prático | Para que serve |
|---|---|---|---|
| **Espacial** | Comparação 3D (X, Y, Z) baseada em localização geográfica | Comparar o contato minério/estéril interpretado no modelo de blocos contra o contato real levantado após a lavra (hanging wall, CMS de realce) | Garantir que "maçãs sejam comparadas com maçãs". Isola variância de erro de interpretação geológica ou de prática de lavra (sobrelavra), sem o efeito de suavização temporal |
| **Temporal** | Comparação ao longo da sequência de lavra por intervalo de tempo (turno, dia, semana, mês, ano) | Comparar massa e teor previstos pelo plano do mês contra a massa e teor medidos na usina no mesmo mês | Rastrear tendências. Discrepâncias geográficas de curto prazo "suavizam" em períodos mais longos (efeito volume-variância) |
| **Física** | Foco em metal contido, parâmetros de qualidade, volumes | Comparar metal contido previsto na reserva para uma área contra o metal produzido e contabilizado pela usina/metalurgia daquela área | Rastrear o produto físico pela cadeia. Combinada com dados temporais, é a medida definitiva de desempenho do ativo |

A reconciliação **temporal é a mais comum**, mas sem o componente espacial não se responde à
pergunta *"lavramos onde e quando planejamos lavrar?"* (Morley & Arvidson, 2017) — ver
`03-formulas-e-calculos.md`, seção *Compliance to plan*.

## Reativa × Pró-ativa — a distinção mais importante da skill

### Reconciliação reativa (prática comum, **não** é boa prática)

Calcula-se um fator ao final do período — classicamente o *mine call factor* (MCF) — e aplica-se
esse fator às estimativas futuras para "corrigir" a previsão. Exemplo: se historicamente a usina
produziu 10% mais ouro que o previsto pelo modelo, aplica-se MCF de 110% às onças previstas.

Por que é problemática:

- Trata o sintoma sem diagnosticar a causa (JORC guidelines).
- **"O ato de aplicar um fator, ou retrocalcular uma medição, produz um resultado perfeito que
  esconde qualquer problema real que a mina esteja enfrentando, e por isso essa prática deve ser
  desencorajada"** (Fouet et al., 2009).
- Mascara falhas sistêmicas graves, que aparecem depois — geralmente no pior momento.
- Pode contaminar decisões operacionais: um MCF de 80% pode levar o geólogo a baixar o corte
  superior do modelo de controle de teor ou a subir o teor de corte na lavra, apenas para "fechar"
  o número (Chieregati, 2023). Esse é talvez o uso mais inoportuno da reconciliação.

### Reconciliação pró-ativa ("prognosticação")

Introduzida por Morley (2003). Coleta e analisa continuamente medições-chave usadas para calibrar
estimativas críticas, em processo iterativo. Quando ocorrem variações, elas são **analisadas** e
uma **ação corretiva** é tomada para que estimativa e medição voltem a se alinhar — mudanças em
protocolos de amostragem, equipamentos, metodologias de estimativa, práticas de lavra.

Assim as estimativas viram **previsões** e passam a servir de base para decisão.

> O principal objetivo de qualquer sistema de reconciliação **não** deveria ser gerar uma lista de
> fatores para corrigir estimativas, mas permitir ajustes nos processos de modo que os resultados
> estejam sempre dentro de limites aceitáveis (Chieregati, 2023; Morley, 2003).

### As duas escolas sobre balanço

Fouet et al. (2009) descrevem duas escolas na indústria:

1. Todo material deve ser contabilizado de modo que entradas e saídas se equilibrem; onde há
   variância, ela é ajustada/fatorada para fechar (*mass balance*).
2. **O erro de estimativa inerente aos diferentes tipos de dado torna impossível que todas as
   entradas e saídas se equilibrem. Por isso usa-se uma faixa de variação para definir resultados
   aceitáveis e, onde a variância cai fora dessa faixa, analisa-se a causa com o objetivo de
   reduzi-la.**

**A escola 2 é a boa prática da indústria** e é a que esta skill adota. A escola 1 pode ser
necessária para fechamento contábil/financeiro mensal, mas não deve governar a reconciliação técnica.

## Reconciliação ilusória — a armadilha a vigiar sempre

Erros cometidos em um ponto do processo podem ser compensados por erros em outro ponto, produzindo
uma reconciliação aparentemente excelente (Crawford, 2004; Chieregati, 2023).

Exemplo numérico (JORC guidelines, a partir das faixas de erro de Morley, 2008): um protocolo de
amostragem de teor de cabeça enviesado superestimando o teor em 25% (dentro da faixa "comumente
observada" de ±20% a 200%) somado a um modelo de controle de teor subestimando o teor em 25%
(dentro da faixa de até ±50%) produz um fator "modelo para metal" próximo de 1,00 — a ilusão
perfeita de um sistema robusto, mascarando duas falhas graves que se cancelam.

**Consequência para a skill**: um indicador global próximo de 1,00 **nunca** é evidência suficiente
de saúde. É obrigatório decompor a cadeia em relações intermediárias (ver `02-cadeia-de-valor.md`)
e verificar se cada elo isolado está em controle. Sempre sinalizar isso ao usuário quando o
indicador agregado for bom mas os intermediários divergirem em sentidos opostos.

Um segundo modo de ilusão (Chieregati, 2023): minério classificado incorretamente como estéril e
mandado para o bota-fora **não é medido na usina** e portanto não entra na equação de reconciliação.
É possível ter excelente reconciliação entre teor estimado e teor produzido enquanto quantidades
substanciais de minério são descartadas. Ver também Hargreaves & Morley (2014), caso 2: mina com
reconciliação "de classe mundial" que estava, na prática, fazendo *high grading* e esterilizando reserva.

## Reconciliação e o JORC

(Fonte: JORC guidelines — síntese derivada de Fouet et al., 2009.)

- **Transparência**: exige reporte claro e inequívoco das variâncias entre estimado e real.
- **Materialidade**: as variâncias medidas são quase sempre informação material — afetam a
  avaliação que investidores fazem das Reservas reportadas.
- **Competência**: o sistema pró-ativo é ferramenta-chave da Pessoa Competente, fornecendo o
  feedback que valida premissas e refina parâmetros de estimativa.
- Reconciliação é o teste operacional das definições do JORC: valida as "razoáveis perspectivas de
  extração econômica" do Recurso e mede a acurácia real dos Fatores Modificadores (diluição, perda
  de minério, recuperação metalúrgica) aplicados na conversão para Reserva.
- A **acurácia esperada varia com a categoria** (Inferido / Indicado / Medido; Provável / Provado).
  A faixa aceitável de variância deve ser diferente conforme a categoria do recurso reconciliado.
- Recurso Inferido **não** pode ser convertido em Reserva (JORC, cláusula 21).

## Alavancagem financeira do erro

(JORC guidelines, derivado de Parker, 2012. Exemplo de mina de cobre, teor de plano 0,60% Cu.)

| Teor de cabeça (% Cu) | Δ do plano | Fluxo de caixa anual pré-imposto (M$) | Δ do plano | VPL @8% (M$) | Δ do plano | Payback (anos) |
|---|---|---|---|---|---|---|
| 0,60 (plano) | 0% | 169,0 | 0% | 554,3 | 0% | 5 |
| 0,57 (erro 5%) | −5% | 144,0 | −15% | 388,1 | −30% | 6 |
| 0,54 (erro 10%) | −10% | 119,1 | −30% | 222,0 | −60% | 7 |

Razão da alavancagem: a receita é diretamente ligada ao teor, enquanto muitos custos (lavra,
moagem, G&A) são fixos por tonelada movimentada. **Um erro de 5-10% no teor corrói 30-60% do VPL.**
Usar esta tabela para dimensionar a materialidade de um desvio ao comunicar com gestão.
