# Reconciliação, orçamento anual e variações mensais

Como a reconciliação alimenta o planejamento de negócio e como lidar com a oscilação mês a mês.

## Como a reconciliação sustenta o orçamento anual

A cadeia de planos é **aninhada**, ganhando detalhe conforme se aproxima da execução
(Morley & Arvidson, 2017; Morley, 2014b):

```
Plano de LOM  →  Plano de negócio 5 anos  →  Ano 1 = ORÇAMENTO  →  STMP (rolante, ~3 meses)  →  execução turno a turno
```

O orçamento anual, anunciado aos acionistas no início do ano, é **o compromisso da empresa com o
mercado**. Investidores e analistas o usam para avaliar o desempenho financeiro; a gestão sênior é
avaliada pela capacidade de entregá-lo.

A reconciliação contribui para o orçamento em quatro frentes:

**1. Calibração dos fatores modificadores.** A reconciliação mede os valores **realizados** de
diluição, perda de minério e recuperação metalúrgica contra os valores estimados. Isso dá base
empírica para refinar esses fatores na próxima estimativa de reserva e no próximo orçamento — em vez
de repetir premissas de estudo de viabilidade nunca validadas (JORC guidelines; Fouet et al., 2009).

**2. Calibração dos parâmetros de conversão física.** Fatores de caminhão, densidades por tipo de
material, fatores de empolamento e fatores de caçamba entram como premissas no sequenciamento e na
estimativa de custo. Fouet et al. (2009): "em base anual, os fatores de caminhão são importantes
como entrada no processo de sequenciamento do planejamento de mina. Conforme a lavra avança para
áreas novas e mais profundas, **não é válido assumir que os fatores de caminhão permanecerão
consistentes**."

**3. Realismo das taxas e da capacidade.** O histórico de reconciliação diz se a mina consegue
entregar o que o plano promete — o que a mina de fato lavra por período, com que diluição, e com que
recuperação a usina processa. O caso Damang mostra o custo de ignorar isso: a subestimativa da
tonelagem econômica no estudo de viabilidade levou à construção de uma usina descasada da capacidade
da mina, obrigando a operar com teor de corte muito mais alto e a estocar grandes tonelagens de
minério lucrativo (Schofield et al., 2013).

**4. Confiança para decisão de investimento.** Vários anos de reconciliação mine-to-mill favorável
foram exatamente o que sustentou a decisão da Macraes de expandir a produção para mineralização
*stockwork* de baixo teor em período de preço de ouro desfavorável (Schofield et al., 2013).

E o inverso: um sistema de reconciliação robusto e pró-ativo **transforma a reconciliação de
auditoria histórica em ferramenta preditiva de gestão**, melhorando a acurácia do planejamento
operacional, do orçamento e do forecast, e fornecendo base confiável para o plano de LOM e o
cumprimento do orçamento anual (JORC guidelines, conclusão).

## Reconciliar contra o orçamento E contra o STMP

São perguntas diferentes e **as duas precisam ser respondidas** (Morley & Arvidson, 2017):

| Contra o quê | Pergunta | Métrica | Frequência de reporte |
|---|---|---|---|
| **Orçamento anual** | Estamos entregando o que prometemos ao mercado? | Relações de reconciliação em massa, teor, produto; acumulado no ano | Mensal, com acumulado |
| **STMP** | Lavramos onde e quando planejamos? | **Compliance to plan** espacial + temporal (ver `03-formulas-e-calculos.md`) | Mensal, com acumulado no período orçamentário |

Se o STMP estiver alinhado ao orçamento anual, o acumulado da compliance mostra a aderência ao
plano anual. Nas palavras dos autores, compliance to plan é rotineiramente **uma das métricas de
pior desempenho em qualquer mina** — e portanto uma das maiores oportunidades de valor.

Nota: quando movimentações de pilha não estão orçadas, a relação "orçamento para entregue à mina" e
"orçamento para contabilizado na usina" precisam do ajuste de pilha descrito em
`03-formulas-e-calculos.md`.

## Como lidar com variações mensais

Este é o ponto onde a maioria das operações erra — reagindo a ruído ou ignorando sinal.

### 1. Escolher o período certo antes de interpretar

- A reconciliação temporal **depende** de que as discrepâncias geográficas de curto prazo "suavizem"
  ao longo de períodos mais longos (efeito volume-variância). Um mês pode não ser suficiente
  (Fouet et al., 2009).
- "Reconciliação calculada para períodos curtos demais" é listada explicitamente como **causa de
  variância da usina** (Pitard, 2001).
- Dado gerado regularmente ao longo de períodos longos gera conjuntos maiores, que suavizam
  anomalias de curto prazo e refletem tendências com mais acurácia (Riske et al., 2007).
- **Referência quantitativa de escala** (Macraes, Schofield et al., 2013): para pacotes de ~400.000 t
  (≈1 mês de lavra) há **20% de chance de déficit de 20% ou pior** em relação ao modelo de recursos.
  Para pacotes de ~1.000.000 t (2-3 meses), as estimativas são bem menos erráticas. Ou seja: **um
  desvio mensal grande contra o modelo de recursos pode ser estatisticamente esperado, não uma falha.**

Regra prática para a skill: **reportar mensalmente, interpretar trimestral/anualmente**, e sempre
declarar a escala junto do resultado.

### 2. Separar ruído de sinal

- Comparar a magnitude do desvio com a faixa de erro esperada das fontes de dado que dominam aquela
  relação (`04-fontes-de-erro.md`).
- Distinguir explicitamente **erro de medição** de **má prática de lavra** — a lista de erros que
  "não são má prática de lavra" está em `04-fontes-de-erro.md` (Morley & Moller, 2005).
- Considerar sazonalidade: estação chuvosa/seca altera umidade, densidade aparente e fator de
  caminhão. Aplicar fatores de umidade sazonais e sempre declarar a base (seca ou úmida).

### 3. Reagir a tendência, não a ponto

Uma variância mensal isolada pode ser ruído estatístico; **três meses consecutivos de variância no
mesmo sentido no mesmo indicador apontam problema sistêmico** (JORC guidelines; Fouet et al., 2009,
que sugerem "reagir quando uma tendência de três ou mais desvios similares é registrada").

Gráficos de tendência em **janela móvel de 12 meses** com semáforo trimestral e anualizado
(Morley & Arvidson, 2017) são o formato que operacionaliza isso.

### 4. Não "fechar" o número

Jamais aplicar fator, retrocalcular medição ou cortar teores do modelo para fazer o mês fechar.
Isso produz um resultado perfeito que esconde o problema real (Fouet et al., 2009) e é exatamente o
erro cometido no caso Damang. Se houver exigência contábil de balanço de metal mensal, mantê-la
**separada** do reporte técnico de reconciliação.

### 5. Fechar o ciclo mensalmente com as pessoas certas

(Morley & Arvidson, 2017.) O champion reúne mensalmente o grupo multifuncional (geologia,
planejamento, operação, topografia, usina) para:

- discutir os resultados;
- **acordar a análise e as conclusões** tiradas dos dados;
- priorizar as ações de melhoria, no formato SMART;
- registrar que a ação nasceu da reconciliação, para rastrear o valor gerado.

O relatório mensal deve ser **formalmente aprovado pela gestão sênior** — é um dos oito critérios do
ranking de confiança (`05-tolerancias-e-gatilhos.md`).

### 6. Rever o mês contra a realidade física

Antes de fechar, um geólogo ou engenheiro que acompanha a cava/subterrânea no dia a dia deve revisar
a reconciliação e o balanço de massa do mês para confirmar que os números refletem o que de fato
aconteceu (Fouet et al., 2009). Mudanças de sequência, frentes indisponíveis, eventos de chuva,
paradas de usina e desvios de material explicam boa parte das variações mensais e devem constar como
**narrativa** ao lado dos números.

## Custo de fazer errado

Quando se pergunta quanto custa refazer um procedimento executado incorretamente, a resposta usual é
"o dobro". Estudos indicam que o custo total de realizar um procedimento pela segunda vez varia de
**8 a 14 vezes o custo original** (Harry & Schroeder, 2000, apud Chieregati, 2023). É um dos
argumentos mais fortes para investir em qualidade de dado e em reconciliação pró-ativa em vez de
correções retroativas.
