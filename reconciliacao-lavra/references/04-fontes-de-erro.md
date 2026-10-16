# Fontes de erro, faixas esperadas e QA/QC

> "A reconciliação de qualquer dado é uma atividade inútil a menos que boa prática seja usada ao
> longo de toda a cadeia de valor" — Fouet et al. (2009).

## Tabela mestra de fontes de erro

(Fouet et al., 2009, Tabela 14, a partir de Morley, 2008; reproduzida em Morley, 2014, Tabela 3.)

"Faixa normal" = limite de acurácia normalmente esperado para a estimativa.
"Faixa comum" = faixas de erro **efetivamente encontradas** em minas — indicam a escala do erro
que pode (e costuma) ocorrer.

| Fonte de erro | Faixa normal | Faixa comum | Comentário | Estratégia de redução |
|---|---|---|---|---|
| Acurácia da metodologia de estimativa do modelo de controle de teor | ±10% | até ±50% | Varia muito com o entendimento da geologia e o método de estimativa escolhido | Reconciliação contínua e revisão da qualidade de amostragem, densidade e metodologia de estimativa |
| Erros de despacho (origem/destino errados) | <5 registros errados/semana | 1 a 10 erros/dia | Sistemas eletrônicos ajudam muito — mas só com monitoramento constante | Revisão turno a turno pela operação com assinatura; correção pelos despachantes no próprio sistema |
| Fatores de caminhão | ±15% | 15% a 30% | Frequentemente números empíricos não validados há muito tempo | Compilação mensal do despacho contra balança de correia ou topografia |
| Células de carga dos caminhões | ±5% | ±20% | Quando a célula falha, é comum manter o caminhão em produção — passa-se a usar fator de caminhão | Manutenção e calibração regulares |
| Estimativas de densidade (incl. densidade in situ) | ±5% | ±10% | Densidade é frequentemente um número empírico usado por mina, geologia, topografia e despacho para converter volume em massa | Plotagem rotineira de topografia × despacho × balança; ensaio anual de densidade em laboratório |
| Fatores de empolamento (pilhas) | ±5% | ±10% | Inclui fatores de conversão de densidade in situ para densidade de pilha e alguma compactação | Uso de dispositivos de medição de densidade de pilha |
| Fatores de caçamba de carregadeira | ±15% | 15% a 30% | Números empíricos não validados | Compilação mensal do despacho contra resultados de balança de correia |
| Medições de balança de correia (weightometer) | < ±5% | ±20% | Balanças mal posicionadas, mal conservadas e raramente calibradas dão massas espúrias | Manutenção e calibração regulares para operar dentro da tolerância de projeto |
| **Erros de amostragem de teor de cabeça** | **±10%** | **±20% até 200%** | Amostradores automáticos são notoriamente difíceis de projetar, instalar e manter. Plantas de alta vazão tornam quase impossível manter regime de amostragem estatisticamente adequado | Instalação e manutenção adequadas do amostrador automático; adesão estrita aos protocolos; **reconciliar contra metal produzido em vez de teor de cabeça** |
| Erros de volume de topografia | ±10% | ±10% | Tendência recente de usar GPS para levantamento pode reduzir a precisão do cálculo de superfície | Levantamento de superfície com teodolito; sobrevoos aéreos de rotina para calibrar |

**Uso prático desta tabela**: ao encontrar um desvio, comparar sua magnitude com a faixa esperada
da fonte de dado envolvida. Um desvio de 15% em uma relação que passa por fator de caminhão está
dentro da faixa "comum" desse erro — pode ser problema de medição, não de geologia. É assim que se
separa o **sinal** (o resultado verdadeiro da reconciliação) do **ruído** (erro de medição)
— distinção explicitamente recomendada em Morley & Moller (2005).

## Variáveis que influenciam a reconciliação, por disciplina

(Pitard, 2001, apud Morley, 2003 e Chieregati, 2023, Tabela 3.)

**Modelo geológico**
- efeito pepita in situ real
- erros de amostragem e sub-amostragem
- erros analíticos
- erros de estimativa
- rejeição excessiva de outliers (top cut)
- resultados da metodologia de estimativa
- suposições de densidade do minério
- definição dos limites do minério

**Modelo de controle de teor**
- efeito pepita in situ
- erros de amostragem e sub-amostragem
- erros analíticos
- furos de desmonte paralelos à mineralização
- metodologia de krigagem / cálculo de média
- contorno do teor do minério
- métodos de amostragem não acurados

**Lavra**
- modelo de lavra paralelo ao invés de cruzar a mineralização
- deslocamento dos limites da mineralização pelo desmonte (*blast movement*)
- métodos de amostragem não acurados
- métodos de transporte por caminhão não acurados
- perda de finos
- estimativa de massa
- diluição

**Usina**
- retenção de metal dentro do moinho / bombas / sumps (particularmente ouro)
- métodos de análise não acurados
- ciclos do processo desconhecidos ou mal interpretados
- calibração dos medidores de massa e de fluxo
- sub-amostragem de laboratório inadequada
- **reconciliação calculada para períodos curtos demais**

## Erros que não são "má prática de lavra"

Morley & Moller (2005) alertam para não confundir estas fontes de erro de medição com diluição ou
perda de minério reais:

- problemas de precisão/acurácia de amostragem
- erros de topografia, particularmente em pilhas
- modelagem de teor de pilhas
- minério retido em pontos de carregamento e passagens internas de minério (orepasses)
- estimativa de estoques associados a sublevel/block caving
- erros de cálculo de volume em realces com sobrepasso ou parcialmente obstruídos
- estimativa de estoques de minério in-pit

**Problema específico de subterrânea** (Chieregati, 2023, a partir de Dominy, Glass & Minnitt, 2022):
até 50 cm de material fragmentado pode permanecer dentro da mina após a lavra. Em minas de ouro o
problema é maior porque sulfetos e ouro grosso liberado se perdem no desmonte e na lavra; maximizar
a fragmentação para otimizar a moagem agrava isso. Um estudo provou que **18,7% do ouro estimado na
reserva permanecia dentro de galerias e realces após a lavra**; recuperá-lo elevou o MCF de 77,8%
para 96,4%, com lucro de US$ 1,4 milhão no projeto de recuperação.

## Por que a usina é (geralmente) a referência

(Crawford, 2004; Chieregati, 2023.)

Os valores da usina são geralmente considerados mais acurados que os da mina — e por isso o MCF é
aplicado às estimativas dos modelos, não aos valores da usina:

1. A amostragem na usina ocorre **após a cominuição**, o que minimiza o problema de distribuição
   granulométrica das amostras.
2. Os fluxos de produto podem ser amostrados mais facilmente em intervalos regulares.
3. Sistemas modernos com analisadores on-stream, cortadores automáticos e controle de processo
   permitem controle sem precedentes dos fluxos.
4. Há múltiplas verificações possíveis dentro da usina, permitindo balanço de massas superior —
   que é, na prática, uma reconciliação interna.

**Mas a usina não é imune.** Causas típicas de erro em balanço de usina: calibração inadequada de
balanças, erros de amostragem de umidade, amostragem insuficiente, protocolos analíticos ruins,
retenção de metal em sumps (particularmente ouro), e furto. A usina opera com estimativa
"balanceada" do teor de alimentação, retrocalculado como rejeito + produtos — grandes erros de
estimativa nesse ajuste indicam problema de amostragem ou de processo.

## QA/QC por nó da cadeia

(Morley & Arvidson, 2017, Tabela 7 — Arvidson, 2015.)

| Nó | Tipo de dado | Protocolo típico de QA/QC |
|---|---|---|
| **Recurso** | Amostras e análises de sondagem | Duplicatas de campo, repetições analíticas, análises de checagem em laboratório independente, materiais de referência certificados, comparação entre técnicas analíticas |
| | Descrição geológica (logging) | Comparação do logging com geoquímica e resultados geofísicos |
| | Mapeamento geológico | Revisão independente das interpretações; checagem de volumes |
| | Interpretação / modelo geológico | Valores de campo lógicos; comparação de volume contra wireframes |
| | Modelo de blocos | Análise dos parâmetros de krigagem; inspeção visual dos resultados |
| | Estimativa de teor | Auditorias independentes |
| | Estimativa de recursos | Comparação com estimativas anteriores e entre recurso e reserva |
| **Reserva** | Design de cava | Comparação entre design, furos e modelo de recursos |
| | Sequenciamento de mina | Revisão por pares quanto a praticabilidade e exequibilidade |
| | Beneficiamento | Validação do desempenho em amostras de volume, planta piloto ou planta em escala |
| | Fatores modificadores | Auditorias independentes, incluindo validação de licenças |
| | Reserva de minério | Comparação com estimativas anteriores e processo de aprovação/assinatura |
| **Orçamento** | Metas mensais de movimentação | Controle de versão nas planilhas de orçamento |
| | Teores mensais de minério e produto | Armazenamento centralizado e controle de acesso |
| | Quantidades mensais de produto | Alinhamento entre planos de lavra e metas de orçamento |
| **Controle de teor** | Amostragem, logging, mapeamento, interpretação, modelo, estimativa | Mesmos protocolos do recurso |
| | Design de polígonos de minério | Revisão por pares e aprovação antes de escavar |
| | Classificação de tipo de material | Árvore de decisão documentada |
| | Monitoramento de movimento do desmonte | Ajuste pós-desmonte dos polígonos para o movimento do fogo |
| **Lavra** | Carregamento | Toda informação necessária disponível antes de escavar; inspeção visual durante a lavra |
| | Transporte | Origens compatíveis com a classificação de tipo de material |
| | Despacho (origem, destino, massa, teor) | Destinos existem e são compatíveis com o tipo de material; massa por caminhão compatível com a capacidade; massas calculadas por balança de caminhão ou fatores validados; teores vêm do controle de teor |
| | Volumes de topografia | Levantamentos conferidos em dobro e reconciliados mensalmente |
| | Gestão de pilhas | Massas de pilha baseadas em ensaios de densidade aparente solta; teores rastreados e controlados por estratégia disciplinada de construção e retomada |
| **Processamento** | Massa e teor alimentados; massa/volume e teor de rejeito | Massas medidas por balanças de correia regularmente calibradas e certificadas |
| | Quantidade e teor dos produtos | Amostras de minério, rejeito e produto sujeitas a protocolos de QA/QC adequados; processo de balanço de massas transparente, documentado, reportado rotineiramente e assinado por metalurgista sênior todo mês |

## Health check de dados de despacho

(Morley & Arvidson, 2017.)

Focos:
- **Tipo de material × tipo de destino**: verificar classificações incorretas — número de
  ocorrências e massa afetada.
- **Acurácia da massa**: o tamanho do caminhão e/ou o fator de caminhão são compatíveis com as
  massas que o sistema registra?
- **Completude de cada carregamento**: todos os registros contêm origem, destino, massa e
  informação de qualidade? Há origens/destinos inválidos, teores negativos, tipos de material
  faltando?

Exemplo real de patologia detectável: análise de carga mínima e máxima por caminhão de uma frota
idêntica revelou não só grande variação de carga (problema de carregamento) mas também que **o
sistema de despacho estava truncando toda carga acima de 250 t para exatamente 250 t** — enviesando
as massas reportadas e mascarando sobrecarga.

Boa prática: os despachantes rodam seus próprios relatórios de erro **ao final de cada turno** e
corrigem imediatamente.

## Teoria de amostragem — o mínimo necessário

(Chieregati, 2023, cap. 1, a partir de Gy e Pitard. Detalhe completo em `references/artigos/`.)

- **Heterogeneidade é a única fonte de todos os erros de amostragem** (Gy, 1998).
- Precisão ≠ acurácia. **Precisão** = dispersão em torno da média (variância do erro, s²SE).
  **Acurácia** = proximidade da média das amostras ao valor real do lote (média do erro, mSE ≈ 0).
- **Representatividade**: r²SE = m²SE + s²SE ≤ valor padrão aceitável. Uma amostra é representativa
  se for **acurada (não enviesada) E precisa (suficientemente reprodutível)**.
- **Amostra correta**: qualquer fragmento do lote tem a mesma probabilidade de ser selecionado.
  Essa condição garante estruturalmente o não-enviesamento. É teoricamente impossível demonstrar
  ausência de viés — por isso qualquer amostrador ou procedimento suspeito de ser incorreto deve
  ser eliminado.
- **Erro fundamental de amostragem (FSE)** — único erro que nunca é zero. Fórmula de Gy:
  `s²FSE = c·f·g·l·d³ · (1/M_S − 1/M_L)`
  com d = d95 (abertura que retém ≤5%); f = fator forma (~0,5 para a maioria dos minerais; 0,2 para
  ouro; 0,1 para laminares); g = fator granulometria (0,25 não calibrado, 0,55 calibrado, 0,75
  naturalmente calibrado); l = fator liberação; c = fator mineralógico (≈ δ_M/a_L quando a_L < 10%).
  Permite calcular a **massa mínima de amostra**.
- Decomposição: TSE = HFE + IME; IME = IDE + IEE + IPE; OEE = TSE + AE.
- Distribuição da variância do erro global (Grigorieff, 2002): **80% amostragem, 15% preparação,
  5% análise química**.
- **Amostragem manual com pá não é método probabilístico** — não se pode estimar sua precisão,
  logo não é método confiável.
- **Amostragem de furo de desmonte**: vantagens (espaçamento pequeno, alta densidade por tonelada,
  sem custo adicional de perfuração), mas recuperação pobre, segregação de partículas por tamanho e
  densidade, e **perda de finos** — principal causa de viés, podendo sub ou superestimar o teor
  (Snowden, 1993). Solução demonstrada no caso brasileiro (Chieregati et al., 2007): amostrador
  setorial estacionário com cúpula, perfuração sem excesso de água.
