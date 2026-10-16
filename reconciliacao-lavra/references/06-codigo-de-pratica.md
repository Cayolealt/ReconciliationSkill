# Código de Prática de Reconciliação — como construir

Fonte primária: Morley (2014), complementado por Hargreaves & Morley (2014) e Morley & Arvidson (2017).
**`assets/guia_codigo_de_pratica.docx` é o guia estruturante deste modo.** Ele contém a estrutura
completa do que um código de reconciliação precisa ter, capítulo a capítulo, com os campos a
preencher. Quando o usuário pedir ajuda para construir ou revisar o processo de reconciliação
dele, **abra esse arquivo e conduza por ele** — a estrutura de capítulos é o roteiro da conversa,
não um anexo de consulta.

Se a operação **já tiver** um código ou rascunho próprio, preencher e evoluir a estrutura
existente é sempre melhor que impor outra: o código precisa refletir o fluxo real daquela mina.
Use o guia para checar o que está faltando, não para substituir o que já existe.

## O que é e por que importa

Um Código de Prática é um documento de alto nível, "definidor de padrão", que estabelece princípios
que passam a fazer parte dos sistemas e procedimentos da mina ou da empresa. Ele define o que são
práticas e metodologias aceitáveis.

O problema que ele resolve (Blucher, 2002, apud Morley, 2014): práticas ruins de reconciliação
prosperam onde

- o sistema existe como um conjunto de planilhas mal integradas, evoluídas para atender ao
  requisito específico de seu autor, que ninguém mais entende e que só o desenvolvedor consegue
  operar — crescendo, ficando pesadas e sendo continuamente ajustadas sem que os destinatários da
  informação saibam que mudanças foram feitas;
- **nenhuma pessoa tem responsabilidade global** pela implementação ou pela entrega dos resultados,
  e os chefes de departamento que geram os dados não se veem como coproprietários do processo.

Objetivo do código: **permitir que qualquer pessoa entenda as práticas usadas naquele site e saiba
quem é responsável por elas** — e que essas práticas sobrevivam à rotatividade de pessoal.

Pitard (2001) conclui que resultados significativos podem ser obtidos em até um ano após implantar
um sistema de reconciliação. **Mas é comum que, após três a cinco anos, mudanças de pessoal e outros
problemas façam o sistema falhar, ser abandonado ou simplesmente se perder.** O código documentado
com accountability embutida nos critérios de desempenho do site é o que faz o ganho durar.

## Os cinco elementos obrigatórios

Um código de reconciliação deve (Morley, 2014):

1. identificar as **relações-chave de reconciliação**;
2. identificar as **fontes de dado** e registrar as atividades de coleta, validação e armazenamento;
3. definir claramente qualquer **pós-processamento** feito sobre os dados de entrada;
4. definir claramente os **cálculos** usados para derivar os resultados;
5. documentar **frequência de reporte, gráficos padrão e usuários finais** dos resultados.

Hargreaves & Morley (2014) acrescentam explicitamente: **faixas de erro e tolerâncias dos dados** e
**accountabilities**.

## Elemento 1 — Relações-chave

Apresentar de forma **gráfica** (cadeia de valor com os nós e as setas de relação) **e tabular**
(seção do processo × nome padronizado da relação). Usar a nomenclatura descritiva
("Fonte A para Fonte B") — ver `02-cadeia-de-valor.md`. Empresas com códigos legados mapeiam-nos
para a nomenclatura padrão.

Também definir explicitamente **quais planos entram na reconciliação** (Morley & Arvidson, 2017):
LOM, plano de negócio de 5 anos, orçamento, forecast, plano de curto prazo (STMP). Planos mais
longos e mais curtos são aninhados, ganhando detalhe conforme se aproximam da execução. É preciso
reconciliar contra **os dois extremos**:

- **Orçamento** — o compromisso da empresa com o mercado, anunciado no início do ano. Investidores e
  analistas avaliam o desempenho financeiro por ele; gestão sênior e investidores focam na
  capacidade de entregar esse compromisso.
- **STMP** — o plano que a mina efetivamente executa. Para responder "lavramos onde e quando
  planejamos?" é essencial reconciliar a atividade real de lavra contra o STMP em base **espacial e
  temporal**.

## Elemento 2 — Coleta e validação de dados

Template (Morley, 2014, Tabela 2) — uma linha por fonte de dado:

| Nome do dado | Fonte e tipo | Periodicidade | QA/QC | Transformações | Comentário |
|---|---|---|---|---|---|
| Controle de teor | Modelo de controle de teor — massa, tipo de material, teores | Diário ou "conforme projetado" | Controle de versão, revisão por pares e assinatura | Cálculo de metal contido | Dado necessário bloco a bloco |
| Plano de curto prazo | Planejamento — volume/massa, tipo de material | Diário/semanal/mensal | Controle de versão, revisão por pares e assinatura | Aplicação de densidade para converter volume em massa | Pode conter informação de teor |
| Orçamento/forecast | Planejamento — volume/massa, tipo de material, teor | Mensal | Controle de versão, revisão por pares e assinatura | Aplicação de densidade | |
| Despacho | Sistema de despacho da operação — origem, destino, tipo de material, contagem de caminhões, massa | Resumos por turno | Validação de origem e destino, validação de volume por caminhão | Aplicação de fator de caminhão para converter contagem em massa | Massas coletadas por células de carga ou contagem |
| Levantamento de pilhas | Topografia — volume | Semanal/mensal (processo de fim de mês) | Validação contra resultados de despacho, revisão por pares e assinatura | Aplicação de densidade | Deve incluir dedos de ROM e pilhas de médio teor; pode incluir pilhas de estéril |
| Massa de britagem | Usina — massa | Resumos por turno e mensal | Procedimentos de calibração de balança de correia | Balanço metalúrgico mensal pode alterar resultados já reportados | Medição em material britado |
| Teor de cabeça | Usina — teores | Resumos por turno e mensal | Balanço metalúrgico | Balanço metalúrgico mensal pode alterar resultados já reportados | |

Para cada fonte, documentar também **limitações e erros inerentes** — usar a tabela de faixas de
erro de `04-fontes-de-erro.md` como anexo do código.

Princípios de dado (Morley, 2003; Morley & Moller, 2005; Morley & Arvidson, 2017):
- automatizar a captura sempre que possível (PLCs, despacho eletrônico, SCADA/LIMS);
- validar o mais perto possível do ponto de captura, com regras de negócio documentadas;
- capturar com frequência e incrementalmente, não em um esforço massivo de fim de mês;
- **guardar sempre o dado bruto junto com o processado, com trilha de auditoria** do que foi feito,
  para permitir reprocessar depois;
- **planilha não é banco de dados** — estudos indicam que qualquer planilha acima de 1 MB tem 80-90%
  de chance de conter erros que afetam significativamente as conclusões (Panko, 2000). Usar banco de
  dados comercial (SQL Server, Oracle, PostgreSQL);
- correções devem ser feitas **na aplicação que gera o dado**, por quem a usa rotineiramente;
- fonte única e centralizada; se houver múltiplos bancos, ligá-los para manter consistência.

## Elemento 3 e 4 — Metodologias e cálculos

Template por relação (Morley, 2014, Tabela 4; Morley & Arvidson, 2017, Tabela 2) — **um bloco destes
para cada relação de reconciliação do site**:

```
Nome:            Produção de lavra para alimentação da usina
Dados requeridos: Produção de lavra — dados de despacho do material saindo da cava,
                  corrigidos por topografia.
                  SCADA para dados de produção da usina e resultados de amostragem do LIMS.
Frequência:      Mensal.
Accountability:  Owner — gerente de produção.
                 Executado por — engenheiro de produção de curto prazo.
Cálculo:         Massa = alimentação da usina / produção de lavra.
                 Teor  = teor amostrado da alimentação / teor da produção de lavra
                         (estimado ou amostrado).
Propósito:       Fornece medida da efetividade das estimativas da lavra real, a partir de
                 fontes de alimentação direta (cava e/ou subterrânea) mais pilhas, até o material
                 recebido.
Comentários:     Reconciliação temporal.
                 Este fator evidencia problemas com fatores de caminhão ou calibração de
                 balanças de correia.
                 A estocagem afeta a reconciliação pelo impacto no material que chega ao moinho.
                 Material retomado de pilha deve ser incluído junto com o material de basculamento
                 direto ao reconciliar o entregue contra o recebido pela usina.
```

## Elemento 5 — Relatórios

Documentar, por relatório: **propósito**, **frequência**, **papel/departamento responsável pela
geração e emissão**, **público-alvo** e **meio de distribuição**. Incluir uma "visão helicóptero"
(miniatura) de cada relatório padrão.

Tipos de relatório de um sistema maduro (Riske et al., 2007, Telfer):

| Tipo | Descrição |
|---|---|
| Reconciliação | Reserva (plano) / controle de teor / usina (real) |
| Depleção da cava por: | tipo de material, faixa de datas, destino, controle de teor |
| Movimentação de material | Comparações de massa por: transporte, britagem |
| Alimentação do britador por: | alimentação direta, remanuseio |
| Rastreio de pilhas | Massa e teor disponíveis |
| Engenharia | Massa por equipamento; produção por fase (desempenho contra plano) |

Formato recomendado de dashboard (Morley & Arvidson, 2017): declarar a relação com a **descrição
completa dos nós**; semáforo verde/laranja/vermelho para resultados trimestrais e anualizados;
gráficos de tendência mês a mês em janela móvel de 12 meses; e sempre conclusões, recomendações e
lista de ações.

## Elemento 6 — Accountability e governança

**Champion de reconciliação** — ponto único de responsabilidade (Blucher, 2002; Morley & Arvidson, 2017):

- normalmente um geólogo sênior de mina, engenheiro de qualidade ou gerente de recursos minerais;
- é o "guardião do processo": garante que o código entre na integração de novos funcionários,
  recomenda atualizações e assegura que os processos rodem no dia a dia e mês a mês;
- **coordena e preside a reunião mensal multifuncional** em que os resultados são discutidos e as
  ações prioritárias são acordadas;
- deve ter capacidade de influenciar a gestão sênior e de cobrar dos donos de cada área a qualidade
  do seu dado e a tempestividade das suas ações;
- perfil ideal: assume a propriedade do sistema, usa o sistema na rotina diária, tem apoio da gestão
  (político e orçamentário), tem o respeito dos pares e entende o processo de reconciliação.

**Dono sênior do código** — gerente de nível superior (gerente técnico, geólogo-chefe, gerente de
recursos minerais) com responsabilidade final por aprovar mudanças e garantir aderência.
Necessário porque, "em tempos de racionalizações irracionais, o champion costuma ser um dos
primeiros a ser cortado, resultando em colapso completo do processo".

**Revisão do código**: definir processo e frequência de revisão programada (anual ou bienal) e o
procedimento para solicitar e implementar alterações.

**Características críticas de um sistema de reconciliação** (Blucher, 2002, apud Morley, 2014):

- o objetivo principal é permitir a otimização contínua de todas as partes-chave da operação,
  levando ao melhor aproveitamento possível dos recursos;
- **todos os participantes** (fornecedores de entrada e destinatários de saída) devem entender os
  conceitos, os objetivos, as entradas requeridas, a lógica e a gama de saídas do sistema;
- os stakeholders devem aceitar que são **coproprietários do todo** — o sucesso depende de abordagem
  unificada e cooperativa;
- o sistema deve ser capaz de se adaptar a circunstâncias em mudança, mas alterações em parâmetros
  fundamentais de design só ocorrem após consulta a todos os stakeholders;
- cada participante é responsável pela qualidade e pela tempestividade das suas próprias entradas;
- os resultados são função de numerosos compromissos e devem ser aceitos como **a melhor
  aproximação, não como absolutos**;
- o retorno aos usuários deve estar em formato que eles possam usar para seus próprios fins;
- a responsabilidade global deve ser focada em um indivíduo ou posição única.

## Elemento 7 — Rastreio de valor

(Morley & Arvidson, 2017.) Para demonstrar o valor da reconciliação e sustentar o investimento:

1. registrar explicitamente que a **ação nasceu da análise de reconciliação**;
2. reportar o **benefício em valor** após a implementação.

Ações devem seguir **SMART** (específica, mensurável, atingível, com recurso, com prazo), e o
champion é responsável por rastreá-las até a entrega.

Exemplos reais de iniciativas nascidas de reconciliação (Anglo American):
- melhoria da definição de minério no controle de teor → aumento do volume de minério entregue à usina;
- identificação de problemas de compliance to plan → mudanças na produção para retornar ao plano;
- identificação de valores incongruentes de densidade aparente → correção de massas mal reportadas;
- remoção de erros em wireframes do modelo → correção da classificação de tipos de material.

Ordens de grandeza medidas (Hargreaves & Morley, 2014, 9 minas, 5 países, benefício em 12 meses):
melhorias de 0,5-2,0% em geologia e modelagem; 0,5-3% em planejamento; 0,5-9,0% em controle de teor;
0,3-2,0% em lavra e desmonte; 0,1-3,0% em carga e transporte; 0,3-24,0% na usina. Benefício por site:
**US$ 4,5 M a US$ 94 M**.

## Anexos recomendados do código

(A partir do esqueleto em português de `references/artigos/` e de Morley, 2014.)

- Anexo A: Diagrama da cadeia de valor da mina, com os nós e relações monitoradas.
- Anexo B: Diagramas de mapeamento de processos (matriz de raias/colunas e SIPOCs detalhados).
- Anexo C: Exemplos de relatórios de reconciliação (visões helicóptero + especificações).
- Anexo D: Termos e definições.
- Anexo E: Tabela de faixas de erro por fonte de dado e tolerâncias/gatilhos acordados por relação.
- Anexo F: Ranking de confiança da reconciliação e resultado da última autoavaliação.
