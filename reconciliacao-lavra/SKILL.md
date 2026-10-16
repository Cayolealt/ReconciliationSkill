---
name: reconciliacao-lavra
description: Reconciliação de lavra (mine reconciliation / MVCR) com base na literatura técnica — Fouet, Morley, Arvidson, Chieregati, Crawford, Schofield. Use sempre que o usuário falar em reconciliação, MCF, mine call factor, fatores F1/F2/R1/G1/M1, Previsto x Reportado x Reconciliado, mine-to-mill, overbreak/underbreak, sobrelavra, diluição, perda de minério, compliance to plan, aderência ao plano, controle de teor versus usina, fechamento mensal de produção de mina, variância entre modelo e usina, código de prática de reconciliação, ou cadeia de valor da mineração — e também quando ele trouxer dados de produção de mina/usina para comparar, pedir para calcular ou interpretar desvios entre modelo, plano, lavra e usina, montar relatório de reconciliação, ou perguntar por que a mina não bate com a usina, mesmo sem usar a palavra "reconciliação".
---

# Reconciliação de lavra

Reconciliação é a comparação entre uma **estimativa** (modelo de recursos, de reservas, de controle
de teor, plano) e uma **medição** (topografia, despacho, balança, produção da usina) em dois pontos
da cadeia de valor, e a análise da variância entre elas.

Esta skill existe porque reconciliação feita errado é pior que não fazer: um número "bonito" pode
esconder dois erros graves que se cancelam, e um fator aplicado ao modelo para "fechar" o mês
mascara exatamente o problema que precisava ser resolvido. O trabalho aqui é sempre **diagnóstico**,
nunca cosmético.

## Princípios que governam tudo nesta skill

1. **Pró-ativa, não reativa.** O objetivo nunca é gerar um fator para corrigir estimativas, e sim
   permitir ajustes de processo para que os resultados fiquem dentro de limites aceitáveis. Aplicar
   fator ou retrocalcular medição produz um resultado perfeito que esconde o problema real e deve
   ser desencorajado (Fouet et al., 2009; Morley, 2003).
2. **Nomenclatura descritiva.** "Modelo de controle de teor para produção de lavra", nunca "F2" ou
   "M1" como nome primário — os códigos alfanuméricos significam coisas diferentes em cada empresa.
3. **O nó mais antigo é sempre o denominador.** Convenção universal de cálculo (Morley & Arvidson,
   2017). Um resultado consistentemente "+" não é bom: significa que o modelo subestima.
4. **Decompor antes de concluir.** Fatores ponta-a-ponta servem para reportar, não para
   diagnosticar. Sempre quebrar em elos intermediários e checar reconciliação ilusória.
5. **Reconciliação compara medido com medido.** Este é o princípio que decide se um número tem
   sentido. Comparar uma estimativa com outra estimativa produz a diferença entre dois modelos, não
   um resultado de reconciliação; comparar estimativa com medição testa o modelo — que é o objetivo
   — mas só se o lado medido for de fato medido. Antes de calcular qualquer relação, saber **quais
   variáveis são mensuradas e quais são estimadas** em cada nó, e dizer isso no resultado.
6. **Sinal versus ruído.** Antes de atribuir um desvio à geologia ou à operação, verificar se ele
   cabe dentro da faixa de erro esperada das medições envolvidas.
7. **Tendência, não ponto.** Um mês fora da faixa pode ser ruído; três períodos no mesmo sentido é
   problema sistêmico.
8. **Rastreabilidade.** Toda fórmula, faixa ou critério apresentado leva a fonte (autor, ano).
   Reconciliação é assunto de governança — o número precisa ser defensável.
9. **Honestidade sobre limitação.** Dizer claramente o que os dados não permitem afirmar é parte do
   trabalho, não uma falha dele. Nunca preencher lacuna com número inventado.

## Como navegar as referências

Leia apenas o que a tarefa exige — não carregue tudo de uma vez.

| Arquivo | Quando ler |
|---|---|
| `references/00-fontes.md` | Sempre que precisar citar; diz o que cada fonte resolve |
| `references/01-fundamentos.md` | Conceitos, tipos de reconciliação, reativa × pró-ativa, reconciliação ilusória, alinhamento JORC, alavancagem financeira do erro |
| `references/10-cadeia-padrao.md` | **A cadeia padrão da skill.** Leia antes de montar qualquer cadeia: os oito indicadores (GM, MP, MO, Mrec, PC, PO, PR, MCF), os nós por faixa, os dois regimes de controle de minério, e as fontes de variação e pontos de amostragem por elo |
| `references/02-cadeia-de-valor.md` | Escolher qual relação responde à pergunta; nomenclatura; mapeamento de processos e SIPOC |
| `references/03-formulas-e-calculos.md` | **Antes de qualquer cálculo.** Fórmulas por relação, indicadores pró-ativos, diluição, overbreak/underbreak, compliance to plan, pilhas, densidade, fator de caminhão |
| `references/04-fontes-de-erro.md` | Interpretar magnitude de desvio; QA/QC por nó; teoria de amostragem; health check de despacho |
| `references/05-tolerancias-e-gatilhos.md` | Perguntas sobre "qual o limite aceitável"; semáforo; ranking de confiança |
| `references/06-codigo-de-pratica.md` | Construir ou revisar o código de prática da mina |
| `references/07-diagnostico-e-acoes.md` | Interpretar um desvio; tabela de causa raiz por indicador; casos documentados |
| `references/08-pilhas-e-estoques.md` | Qualquer coisa envolvendo pilha, estoque, latência, densidade aparente |
| `references/09-orcamento-e-ciclo-mensal.md` | Orçamento anual, variações mensais, ciclo de fechamento |
| `references/anexo-codigos-legados.md` | Usuário chegou com F1/R2/G3/M1/I2 e é preciso traduzir |
| `references/artigos/` | PDFs originais, para detalhe que a extração não cobre (ler por faixa de páginas) |

## Scripts

**Não faça a aritmética à mão.** `scripts/reconciliacao.py` aplica a convenção de denominador,
pondera teores por massa e evita erro de sinal.

```bash
python scripts/reconciliacao.py --autoteste            # valida as fórmulas contra a literatura
python scripts/reconciliacao.py --exemplo              # exemplo verificado (Chieregati, 2023)
python scripts/reconciliacao.py --input dados.json --out resultados.json
```

`cadeia_padrao(nos)` calcula os oito indicadores da cadeia de referência e diz **qual nó falta**
em cada indicador que não fecha — nó ausente nunca vira zero nem proxy. Aceita `pares=` para
sobrescrever a definição de qualquer indicador conforme o código de prática do site.

`scripts/validar_base.py` roda as verificações de incoerência **antes** do cálculo:
`validar_producao()` para base temporal, `validar_realces()` para base espacial,
`relatorio_texto()` para apresentar. Todo achado sai com as opções e o impacto de cada uma, e
com `decisao_do_usuario=True` — nenhuma verificação decide sozinha.

`diagrama_cadeia()` em `graficos.py` desenha a cadeia com os indicadores calculados sobre ela,
marcando nó ausente como tracejado e indicador não calculável com o nome do nó que falta.

Funções disponíveis como biblioteca: `fator`, `cadeia`, `cadeia_padrao`, `indicadores_proativos`,
`diluicao_recuperacao`, `overbreak_underbreak`, `compliance_to_plan`, `ajuste_pilha`,
`densidade_aparente`, `empolamento`, `fator_caminhao`, `media_ponderada`, `agregar`, `semaforo`,
`tendencia`. Formato de entrada em `assets/exemplo_entrada.json`.

`scripts/tema.py` governa tipografia, escala, espaçamento, raio, traço e proporção; `paleta.py`
governa cor. **Trocar esses dois é tudo o que a identidade visual de uma empresa exige** — os três
destinos leem de lá, então uma mudança vale para gráfico, painel e corpo do PDF de uma vez.
`registrar_fonte_pdf()` casa a fonte do relatório com a dos gráficos.

`scripts/diagrama.py` desenha o fluxograma da cadeia em SVG. Motor separado de propósito:
matplotlib é excelente do básico ao complexo em gráfico estatístico e é o teto do diagrama;
SVG dá gradiente, sombra, canto e faixa em camadas, renderiza nativo no painel e converte para
PNG de alta resolução. Cada motor no que ele é bom.

`scripts/graficos.py` gera as três formas que fazem trabalho que tabela não faz, em dois destinos.
`scripts/paleta.py` é o **único** arquivo a trocar para adotar outra identidade visual — a paleta
atual é a instância de referência validada.

| Função | Responde | Quando usar |
|---|---|---|
| `waterfall_cadeia` | onde a massa (ou o metal) entra e sai ao longo da cadeia | sempre que houver 3+ nós; é o gráfico que faz o interlocutor ver a perda em segundos |
| `tendencia` | é ponto isolado ou tendência? | sempre que houver 3+ períodos; com linha de referência e faixa |
| `overbreak_underbreak` | as duas perdas se cancelam? | sempre que houver sobrelavra e sublavra — é a forma que mata a reconciliação ilusória visualmente |

```python
from graficos import waterfall_cadeia, tendencia, overbreak_underbreak, painel_html
waterfall_cadeia(nos, "título", "t", arquivo="wf.png")        # PNG para o relatório paginado
painel_html("painel.html", "título", "lead", figuras)          # painel navegável com hover e tabela
```

`scripts/normalizar_entrada.py` lê planilhas de produção (xlsx/csv), inspeciona abas e colunas e
sugere o mapeamento para o formato de cálculo:

```bash
python scripts/normalizar_entrada.py --arquivo producao.xlsx --listar
python scripts/normalizar_entrada.py --arquivo producao.xlsx --aba <aba> --mapa mapa.json --out dados.json
```

## A cadeia padrão

Quando o usuário não define outra, a skill assume a cadeia de **Joscil Spitzner Galvão (2020,
rev. 2023), baseada em Ana Carolina Chieregati (2011)** — documentada em
`references/10-cadeia-padrao.md`, com o esquema original em `assets/`. **Credite essa origem**
ao apresentar o modelo.

Oito indicadores: **GM** (modelo geológico) · **MP** (planejamento) · **MO** (operação de lavra) ·
**Mrec** (reconciliação de mina) · **PC** (controle de planta) · **PO** (operação de planta) ·
**PR** (recuperação de planta) · **MCF** (ponta a ponta).

Duas coisas nessa cadeia mudam a prática e não devem ser simplificadas de volta:

**A planta se decompõe em três indicadores, não um.** PC, PO e PR separam o que a planta recebeu,
o que ela fez com isso e quanto recuperou. Um PR único agrega os três e perde poder diagnóstico
exatamente onde ele é mais barato de obter.

**Overbreak e underbreak são nós da reserva, não métricas derivadas.** É assim que se mede em
lavra subterrânea e é o que faz a reconciliação ilusória aparecer sem cálculo extra.

Antes de calcular numa operação nova, **confirme com o responsável quais são os dois nós exatos
de cada indicador ali** — sobretudo PC, PO e PR, que admitem mais de uma definição legítima. O
esquema define a faixa que cada indicador cobre; a definição precisa pertence ao código de prática
do site.

## O que perguntar antes de calibrar qualquer cadeia

**Nem toda mina tem esses fatores ou essa cadeia.** A cadeia padrão é ponto de partida, não
gabarito. Antes de aplicá-la, levante com o usuário — em uma rodada curta, não num questionário:

1. **Qual é o fluxo de minério?** Da frente ao produto: o que existe, em que ordem, onde há pilha,
   remanuseio, silo, britagem, embarque. Nó que a operação não tem sai da cadeia.
2. **Já existe uma cadeia de valor definida?** Se existe, ela manda. **Os nomes dos fatores podem
   ser outros** — pergunte quais são e use os nomes da casa, mapeando para a nomenclatura
   descritiva só quando for necessário comparar com literatura ou entre sites.
3. **Quais variáveis são mensuradas e quais são estimadas**, nó a nó, para massa e para teor
   separadamente. Esta pergunta governa tudo: reconciliação compara medido com medido, e um elo
   entre duas estimativas precisa ser rotulado como comparação de modelos, não como reconciliação.
4. **Em que base os indicadores são reportados?** Normalmente **metal contido / produto final**,
   mas **sempre pergunte** — algumas operações trabalham em massa, outras em teor, outras nas três.
   Assuma metal apenas se o usuário não tiver preferência, e diga que assumiu.
5. **Quais são os gatilhos e tolerâncias da operação?** Se não houver, use as faixas da literatura
   citando a fonte e recomende formalizar (`05-tolerancias-e-gatilhos.md`).

## Validação da base — antes de qualquer número

Reconciliação com dado inconsistente é pior que nenhuma. **Rode `scripts/validar_base.py` antes de
calcular** e apresente o resultado ao usuário. O que procurar:

- realces, fogos ou períodos **reconciliados × não reconciliados** — e qual fração da produção cada
  grupo representa;
- **dados faltantes**: nós vazios, meses ausentes, colunas preenchidas só em parte da série;
- **nós com cobertura temporal diferente** — comparar o total anual de um nó que existe em 9 meses
  com outro que existe em 5 produz desvio inteiramente artificial;
- **fechamentos que não batem**: soma das partes contra o total, `massa x teor` contra o metal
  reportado, saldo de pilha contra movimentação;
- **valores carimbados**: teor idêntico em todos os registros de uma frente indica parâmetro fixo,
  não medição — e qualquer indicador de teor dali é vazio por construção;
- **escopos incompatíveis**: lançamento por evento (escaneamento, desmonte) misturado com fluxo
  mensal.

**Ao encontrar uma incoerência, não decida sozinho: pergunte ao usuário o que fazer** — incluir na
análise, excluir, ou tratar à parte. Apresente o impacto de cada opção (quanta massa e metal entram
ou saem) para que a escolha seja informada. Registre a decisão no relatório, na seção de premissas.

## Modos de trabalho

Identifique qual dos quatro o pedido é. Eles se combinam com frequência.

### A. Consultoria metodológica
"O que preciso para reconciliar?", "quais fatores existem e o que cada um responde?", "como mapear
os erros?", "como montar a cadeia de valor?", "isso é boa prática?"

Responder a partir das referências, citando a fonte. Quando a pergunta for ampla, começar pelo mapa
de "qual relação responde qual pergunta" (`02-cadeia-de-valor.md`) em vez de despejar a lista de
fatores. Se o usuário estiver estruturando o sistema do zero, os dez passos da prognosticação
(`07-diagnostico-e-acoes.md`) são o roteiro.

### B. Cálculo e relatório a partir de dados
Dados de produção, teor, volumes, topografia, planilhas, PDFs ou imagens de relatórios.

Sequência:

1. **Ler e conferir o dado antes de calcular.** Identificar cada nó, a grandeza, a unidade, a base
   de umidade, o período, o site. Usar `normalizar_entrada.py --listar` para planilhas.
   **Mostrar ao usuário o que foi entendido e confirmar o mapeamento** antes de rodar números —
   reconciliação com dado mal lido é pior que nenhuma. Para PDF e imagem, transcrever os valores
   e apresentá-los para conferência.
2. **Rodar as verificações obrigatórias** de `03-formulas-e-calculos.md`: teores ponderados por
   massa? Mesmo material dos dois lados (mesmo polígono, período, base, tipo)? Blocos reconciliados
   como foram lavrados e não como projetados? Latência de pilha tratada? Despacho corrigido por
   topografia? Metal fecha com massa × teor?
3. **Calcular com o script**, em massa, teor e metal.
4. **Decompor** — nunca entregar só o agregado. Identificar o elo crítico e checar reconciliação
   ilusória.
5. **Interpretar** com `04-fontes-de-erro.md` (o desvio é sinal ou ruído?) e
   `05-tolerancias-e-gatilhos.md` (o que é limite da operação × o que é referência de literatura).
6. **Diagnosticar** com `07-diagnostico-e-acoes.md` e propor ações SMART.
7. **Montar o relatório** seguindo `assets/template_relatorio.md`.

### C. Diagnóstico de um desvio específico
"O MCF caiu para 0,78, o que houve?", "a usina reportou 8% menos massa que o despacho."

Seguir o fluxo de 7 passos de `07-diagnostico-e-acoes.md`. O passo mais pulado e mais importante é
confrontar o número com **o que de fato aconteceu na mina no período** — mudança de sequência,
frente indisponível, chuva, parada de usina, desvio de material. Perguntar isso ao usuário.

Ao apresentar hipóteses, ordenar da mais provável para a menos, e dizer o que **verificaria** para
confirmar cada uma. Não afirmar causa raiz sem evidência.

### D. Construir o processo de reconciliação do usuário
Este é um objetivo central da skill, não um extra: ajudar quem ainda não tem um processo a montar
um, e quem já tem a fechar as lacunas.

**`assets/guia_codigo_de_pratica.docx` é o roteiro.** Ele traz, capítulo a capítulo, tudo o que um
código de reconciliação precisa ter. Conduza a conversa por ele: fundamentos, cadeia de valor,
mapeamento de fluxo de minério e movimentação de material (matriz e SIPOC), relações-chave,
coleta e validação de dados, metodologias e cálculos, relatórios, responsabilidade e governança,
anexos. Preencha com o que o usuário responder e devolva o documento com as lacunas explicitamente
marcadas — um código com campo em branco identificado vale mais que um texto genérico completo.

Usar `06-codigo-de-pratica.md`. Se a operação já tiver um código ou rascunho próprio, **preencher e
evoluir a estrutura existente** em vez de impor outra — o código precisa refletir o fluxo real
daquela mina. Se não tiver, `references/artigos/Procedimento_reconciliacao.docx` traz um esqueleto em
português como ponto de partida. Cobrir os elementos obrigatórios: relações-chave, coleta e validação
de dados, metodologias e cálculos, relatórios, accountability, tolerâncias, rastreio de valor.

## Formato de saída

Perguntar ou inferir. Padrões:

| Situação | Saída |
|---|---|
| Pergunta conceitual ou de diagnóstico | Resposta direta na conversa, com fontes |
| Relatório formal para circular | `.docx` (skill docx) ou `.pdf` (skill pdf), a partir do template |
| Números para o usuário continuar analisando | `.xlsx` (skill xlsx) com as tabelas de relações e indicadores |
| Dashboard ou painel para consulta recorrente | Página HTML persistida como artifact |
| Gráficos | PNG estático dentro do relatório paginado, painel HTML navegável, ou os dois |
| Rascunho de código de prática | `.docx` ou markdown, conforme o uso |

Quando o formato não estiver claro e houver mais de um razoável, perguntar em uma linha antes de
produzir. O relatório sai **em português** por padrão.

## Gráficos

Reconciliação tem três formas que comunicam o que tabela nenhuma comunica: o **waterfall da cadeia**
(onde o metal e a massa entram e saem), a **tendência com referência e faixa** (é ponto ou é
tendência?) e as **barras divergentes de sobrelavra e sublavra** (as duas perdas se cancelam?).
A terceira é a mais importante desta skill: ela mata a reconciliação ilusória visualmente, o que
nenhum parágrafo consegue fazer com a mesma força.

**Antes de desenhar qualquer gráfico, carregue a skill `dataviz`.** Ela traz o procedimento
(forma primeiro, cor por último), o validador de paleta que deve ser executado em vez de julgado
a olho, as especificações de marca e o catálogo de antipadrões. Os scripts desta skill já seguem
essas regras; qualquer gráfico novo também deve seguir.

**Pergunte ao usuário qual destino ele quer** antes de gerar — PNG estático para o relatório
paginado, painel HTML navegável com hover e tabela de dados, ou os dois. Os dois são legítimos e
servem a usos diferentes: o PNG é para o documento que circula e é arquivado; o painel é para
quem vai explorar. Se o usuário não indicar e o contexto não decidir, pergunte em uma linha.

Regras que não se afrouxam, mesmo sob pressão de prazo: um eixo só, nunca dois eixos y; a cor
segue a entidade e nunca o ranking, de modo que um filtro não repinte as séries que sobraram;
legenda sempre presente com duas ou mais séries, com rótulo direto até quatro; texto em tinta,
nunca na cor da série; grade e eixos recessivos. Acima de quatro séries numa linha do tempo,
agrupe em "Outros" ou use múltiplos pequenos em vez de gerar cor nova.

**Dimensione o desenho pelo destino, não o contrário.** A regra é dura: **nenhum texto abaixo de
6 pt na página final**. Um fluxograma de onze nós não fica legível reduzido à largura de um A4 —
e a resposta não é diminuir a fonte, é mudar o destino. As saídas legítimas, em ordem de
preferência: página em tamanho diferente no mesmo PDF (o relatório não precisa ser todo A4 —
um encarte A3 paisagem resolve e é prática editorial normal); versão condensada no corpo com a
completa em encarte; painel HTML com zoom, onde a largura é livre. O parâmetro `escala_texto` de
`cadeia_valor()` existe para isso: 1,0 no painel, ~1,75 quando o desenho for reduzido para uma
página. Calcule a legibilidade final antes de aceitar o desenho.

**Toda faixa de tolerância desenhada precisa dizer de onde vem.** Se a operação não formalizou
gatilhos, rotule a faixa como referência de literatura com a fonte, nunca como se fosse o limite
da operação — o gráfico é lido por quem não vai ler a nota de rodapé.

## Comportamentos obrigatórios

**Dados faltando de um site ou período.** Gerar o que for possível com o que existe, e declarar
explicitamente na seção de limitações: qual site/período faltou, o que isso impede de afirmar, e o
que seria necessário. Nunca interpolar, estimar por analogia com outro site, ou omitir a ausência.
Se a ausência invalidar a conclusão principal, dizer isso no sumário executivo, não em rodapé.

**Tolerâncias.** Se a operação não tem gatilhos formalizados, dizer isso, usar as faixas da
literatura como referência provisória **citando a fonte**, e recomendar a formalização. Nunca
apresentar limite de literatura como se fosse o limite oficial da operação, e nunca inventar um
número de tolerância.

**Nunca inferir controle faltante a partir do formato do relatório.** Antes de dizer que um
controle está ausente, **perguntar onde a grandeza é medida**. Um número que não se move pode
significar que o controle não existe — ou que ele é desnecessário porque a grandeza é medida
diretamente. Exemplo real: massa reportada idêntica à reconciliada não indica falta de verificação
volumétrica quando toda a massa é pesada em balança; indica que o único ponto de massa estimada é a
retomada de pilha, e é lá que a verificação precisa estar. Mapear os pontos de medição
(`02-cadeia-de-valor.md`) é **pré-requisito** para escolher quais relações fazem sentido na mina.

**Cobertura × fator.** "% da produção já reconciliada" e "fator de reconciliação" são métricas
diferentes e nunca devem dividir tabela, eixo ou nome. Se o usuário tiver uma métrica chamada "taxa
de reconciliação", confirmar qual das duas ela é antes de interpretar.

**Todo resultado de reconciliação sai acompanhado da sua cobertura.** Um fator calculado sobre 15%
da produção não é comparável a um calculado sobre 100%, não deve ser consolidado com ele sem
ressalva, e não sustenta a mesma conclusão. Quando a cobertura for parcial, dizer no corpo do
resultado — não em nota de rodapé — sobre que fração ele foi calculado, e tratar a própria cobertura
como achado: por que só essa fração foi reconciliada, e o que está travando o resto.

**Produção da planta.** A usina é geralmente a referência mais acurada (amostragem pós-cominuição,
fluxos amostráveis, balanço interno) — mas não é imune. Tratar a usina como referência **e**
verificar suas próprias fontes de erro (calibração de balança, amostragem de teor de cabeça, umidade,
retenção de metal). Quando o erro de teor de cabeça for suspeito, reconciliar contra **metal
produzido** em vez de teor.

**Overbreak e underbreak.** Sempre reportados **separadamente**, nunca só o líquido — eles se
compensam em volume enquanto destroem valor em teor. Sublavra não aparece na equação usual de
reconciliação porque o metal que ficou no maciço nunca é medido; sinalizar isso quando for o caso.

**Nomear as entidades como elas aparecem no dado.** Minas, realces, painéis, projetos e frentes
entram no relatório com o nome que têm na base do usuário. Não anonimizar, não substituir por rótulos
genéricos ("Frente 1", "Site A") e não pedir permissão para usar um nome que já está no arquivo que o
usuário enviou — o relatório é interno à operação dele e rótulo genérico só dificulta a ação. Esta
skill é genérica; os relatórios que ela produz não são.

**Múltiplos sites ou frentes.** Reconciliar **por site** por padrão; consolidar apenas se pedido e
sempre mantendo a abertura por site visível. Métodos de lavra, corpos de minério e fontes de erro
diferem entre subterrânea e céu aberto, e entre depósitos — não misturar tolerâncias nem diagnósticos
de operações que só compartilham o dono.

**Ao encontrar um resultado bom.** Verificar se é bom de verdade. Um MCF perto de 1,00 com
indicadores intermediários divergindo em sentidos opostos é reconciliação ilusória, e minério indo
para o bota-fora não aparece em nenhum indicador. Reportar essa checagem explicitamente.

**Ao encontrar um resultado ruim.** Não sugerir ajustar o modelo, cortar teores ou aplicar fator
para fechar o número. Essa foi exatamente a resposta errada no caso Damang
(`07-diagnostico-e-acoes.md`). A resposta é investigar a causa.
