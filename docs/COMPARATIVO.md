# Comparativo: com e sem a skill

## Método

Três casos de teste, cada um rodado duas vezes com o **mesmo prompt** e o **mesmo modelo**: uma vez
com a skill carregada, outra sem skill nenhuma. Cada caso foi avaliado contra assertivas objetivas
definidas antes da execução.

Isso mede uma coisa específica: **se a skill aciona o comportamento certo**. Não mede se a resposta
é boa para a sua operação — isso só a revisão humana diz.

## Resultado

| Caso de teste | Com skill | Sem skill |
|---|:---:|:---:|
| Ler relatório gerencial de produção e diagnosticar | **9/9** | 6/9 |
| Diagnosticar MCF em queda sem mudança de modelo | **7/7** | 5/7 |
| Estruturar código de prática de reconciliação | **7/7** | 3/7 |
| **Total** | **23/23 (100%)** | **14/23 (61%)** |

Delta: **+39 pontos percentuais**.

## O que o modelo sozinho já faz bem

Vale registrar, porque a skill não precisa ensinar o que já funciona:

- Analisa um relatório de produção de forma competente (6/9 no caso 1).
- Decompõe o MCF em elos e argumenta corretamente que, com o modelo congelado, a causa está entre
  o modelo e o produto.
- Lista hipóteses plausíveis e ordenadas, com testes discriminantes.
- **Não sugere fraudar o número.** O baseline do caso 2 recomendou explicitamente não aplicar MCF
  como fator corretivo antes do diagnóstico.

## O que ele não faz sem a skill

### 1. Citar fonte — 0/3 nos baselines, 3/3 com a skill

A assertiva mais discriminante do conjunto inteiro. Os baselines dão conselho correto e **não
rastreável**: nenhuma faixa de tolerância, nenhum critério, nenhuma definição vem com autor e ano.

Reconciliação é assunto de governança. Um número que não se consegue defender numa auditoria não
sustenta decisão — e a diferença entre "±10% é a faixa normal" e "±10% é a faixa normal
(Fouet et al., 2009, Tab. 14, a partir de Morley, 2008)" é a diferença entre opinião e evidência.

### 2. Distinguir cobertura de fator

O baseline do caso 1 tratou uma métrica chamada "taxa de reconciliação: 29,49%" como se fosse
desempenho da mina. Ela significava que **29,49% da produção já tinha passado pelo processo de
reconciliação** — cobertura, não fator.

A skill confirma qual das duas é antes de interpretar, e impõe que as duas nunca dividam tabela,
eixo ou nome. Além disso: **todo resultado sai acompanhado da sua cobertura**, porque um fator
calculado sobre 15% da produção não é comparável a um sobre 100% — e a fração reconciliada
primeiro raramente é amostra aleatória.

### 3. Conferir o dado antes de calcular

O baseline calcula direto. A skill mostra o que entendeu — nó a nó, grandeza, unidade, base de
umidade, período — e pede confirmação antes de rodar número.

No caso 1, a execução com skill foi além do que o próprio autor do teste tinha feito: recalculou o
teor a partir de `metal ÷ massa` em vez de usar o teor impresso, porque os dois decimais do
relatório propagam erro ao multiplicar de volta, e sinalizou que a **base de umidade não estava
declarada em lugar nenhum do documento**.

### 4. Cobrir governança — 3/7 contra 7/7

O maior delta do conjunto. No caso do código de prática, o baseline produziu um sumário de seções
razoável e **não cobriu**:

- **Accountability** — quem responde por cada etapa.
- **Reconciliation champion e dono sênior** — e por que o champion sozinho não basta: em cortes,
  ele costuma ser um dos primeiros a sair, e o processo inteiro colapsa junto.
- **Planilha não é banco de dados** — estudos indicam 80-90% de chance de erro material em qualquer
  planilha acima de 1 MB (Panko, 2000).

São exatamente os elementos que fazem o sistema sobreviver à rotatividade. Pitard (2001) observa
que resultados aparecem em até um ano — mas que em três a cinco anos a mudança de pessoal faz o
sistema falhar ou se perder. O que o baseline entregou funciona enquanto quem o montou estiver lá.

## As assertivas

### Caso 1 — ler relatório gerencial

1. Separa massa de teor por site
2. Identifica que a perda do mês é de teor, não de massa
3. Distingue cobertura de fator de reconciliação
4. Qualifica os resultados pela cobertura
5. Não afirma que falta controle volumétrico sem perguntar onde a massa é medida
6. Mostra o que entendeu dos dados para conferência
7. Cita fontes com autor e ano
8. Aponta ausência de nó de modelo na cadeia
9. Não sugere aplicar fator ou ajustar modelo para fechar

### Caso 2 — diagnosticar MCF em queda

1. Recusa diagnosticar pelo agregado e exige decomposição
2. Hipóteses ordenadas com o que verificar em cada
3. Pergunta o que aconteceu fisicamente na mina no período
4. Alerta contra ajustar modelo ou aplicar fator
5. Menciona reconciliação ilusória
6. Menciona a regra de tendência de três períodos
7. Cita fontes com autor e ano

### Caso 3 — estruturar código de prática

1. Começa por mapeamento de fluxo e pontos de medição, não pela lista de fatores
2. Cobre os cinco elementos obrigatórios
3. Nomenclatura descritiva em vez de F1/F2
4. Define champion e dono sênior
5. Alerta que planilha não é banco de dados
6. Trata tolerâncias e gatilhos
7. Cita fontes com autor e ano

## Limitações desta avaliação

**Amostra pequena.** Três casos, uma execução cada. Suficiente para ver o padrão, insuficiente
para estimar variância.

**Assertivas binárias.** Medem presença de comportamento, não qualidade do resultado. Um output
pode marcar 9/9 e ainda estar errado sobre a operação específica.

**O avaliador escreveu a skill.** As assertivas vieram do mesmo processo que definiu os
comportamentos — viés inevitável. O contrapeso é que elas são objetivamente verificáveis e estão
listadas acima, para qualquer pessoa conferir.

**Um falso negativo foi corrigido à mão** no caso 1 com skill: o regex não capturou a frase
"A mina entregou a tonelagem e não entregou o teor", que satisfaz a assertiva 2.

## Reproduzindo

Os casos estão em [`reconciliacao-lavra/evals/evals.json`](../reconciliacao-lavra/evals/evals.json).
Para rodar, use a skill `skill-creator` do Claude, que executa com e sem skill em paralelo e gera
o comparativo.
