# Cadeia de valor da mineração e as relações de reconciliação

## Os nós da cadeia

A cadeia de valor é uma progressão linear em que cada etapa agrega valor sobre a anterior e segue
o material desde a identificação até o produto vendido (Morley, 2014). Cada **nó** é
simultaneamente um ponto de agregação de valor e um **ponto de coleta de dado**.

```
Recurso → Reserva → Plano (LOM / 5 anos / Orçamento / STMP) → Controle de teor →
Perfuração e desmonte → Lavra (despacho + topografia) → Pilhas / ROM →
Alimentação da usina → Produção da usina (+ rejeito) → Transporte → Embarque / Venda
```

Nem toda mina tem todos os nós. **A operação adota apenas os nós e relações para os quais consegue
registrar e medir as entradas** (Fouet et al., 2009). Uma mina sem modelo de controle de teor não
reporta as relações que dependem dele; uma mina sem modelo de reserva separado usa o modelo de
recursos como base.

### Definições dos modelos (Fouet et al., 2009, ancoradas no JORC)

- **Modelo de recursos**: localização, quantidade, teor, características geológicas e continuidade
  conhecidas, estimadas ou interpretadas a partir de evidência geológica específica.
- **Modelo de reservas**: modelo de recursos com **fatores modificadores** aplicados (diluição,
  perdas de lavra, fatores econômicos), que depletam o recurso e fornecem uma estimativa recuperável
  mais provável.
- **Modelo de controle de teor (modelo de lavra)**: modelo de recursos ao qual foram aplicadas etapas
  adicionais de definição para localizar geologia, massa e teor **para fins de lavra** — tipicamente
  via mapeamento/topografia detalhados e amostragem adensada (furos de desmonte, trincheiras, RC
  dedicado em cava; sondagem diamantada, furos de leque ou *sludge* em subterrânea), logados e
  analisados antes da lavra.

Mineralizações contínuas, sub-horizontais ou estratiformes (bauxita, carvão) com baixa
variabilidade horizontal muitas vezes **não** justificam um modelo de controle de teor separado —
usa-se o modelo de reserva como modelo de lavra.

## Regra de nomenclatura

**Nunca use F1, F2, R1, G3, M4 como nomenclatura primária.** Esses códigos alfanuméricos são
locais, mudam de mina para mina e de empresa para empresa, e produzem conclusões erradas quando
resultados são comparados entre sites. O 'F2' da BMA compara reservas de carvão ao modelo de controle
de teor; o mesmo par na Rio Tinto se chama 'R2' (Fouet et al., 2009).

**Convenção correta** (Morley, 2014; Morley & Arvidson, 2017):

> "nome da fonte de dado mais antiga" **para** "nome da fonte posterior com que é comparada"

Exemplos: *Modelo de recursos para modelo de reservas*; *Controle de teor para produção de lavra*;
*Produção de lavra para alimentação da usina*.

Empresas com códigos legados podem mantê-los internamente e **mapeá-los** para a nomenclatura
padrão no reporte externo. Ver tabela de mapeamento em `anexo-codigos-legados.md`.

## Relações padronizadas (Fouet et al., 2009; Morley, 2014; Morley & Arvidson, 2017)

### 1. Reconciliação de modelo geológico (modelo × modelo)
Testa o conhecimento do corpo de minério e as conversões entre modelos. **Espacial + temporal.**

- Modelo de recursos para modelo de reservas
- Modelo de recursos para modelo de controle de teor (lavra)
- Modelo de reservas para modelo de controle de teor (lavra)

### 2. Reconciliação de modelo geológico × "reais"
Liga os modelos aos resultados medidos. **Temporal.**

- Modelo de recursos para produção de lavra / alimentação da usina / produção da usina
- Modelo de reservas (plano LOM) para produção de lavra / alimentação da usina / produção da usina / embarque

> As relações partindo do **recurso** só devem ser reportadas para governança quando a operação
> **não** produz um modelo de reservas separado e planeja sobre o recurso não modificado. Ainda
> assim entregam valor ao geólogo de recursos para entender suas interpretações e estimativas
> (Fouet et al., 2009).

### 3. Reconciliação de lavra
Foco na execução. **Temporal** (a compliance to plan é espacial + temporal).

- Modelo de controle de teor para produção de lavra ← **medida direta da execução de lavra**
- Modelo de controle de teor para alimentação da usina
- Modelo de controle de teor para produção da usina
- Plano de lavra (STMP) para produção de lavra
- Produção de lavra para alimentação da usina
- Produção de lavra para embarque

### 4. Reconciliação de usina
- Alimentação da usina para produção da usina

### 5. Reconciliação de ferrovia/embarque
- Produção da usina para embarque

## Qual relação responde a qual pergunta

Este é o mapa de diagnóstico. Use-o para escolher a relação certa antes de calcular qualquer coisa.

| Pergunta de negócio | Relação | O que um desvio significa |
|---|---|---|
| O modelo de recursos superestimou o metal? | Recurso para controle de teor | Interpretação geológica inicial, parâmetros de estimativa, amostragem de recursos, espaçamento de sondagem |
| Os fatores modificadores da reserva são realistas? | Recurso para reserva; Reserva para controle de teor | Premissas de diluição e perda de lavra conservadoras ou otimistas demais |
| A reserva estava superestimando a produção — diluição e recuperação? | Reserva para produção de lavra | Combinação de acurácia do modelo, prática de lavra e sistema de medição |
| Lavramos onde e quando planejamos? | Plano de lavra (STMP) para produção de lavra + *compliance to plan* espacial | Sequenciamento, disponibilidade de frente, mudança de prioridade, prática de lavra |
| As taxas de produção programadas foram atingidas? | Plano/orçamento para produção de lavra | Execução, disponibilidade de equipamento |
| A lavra está diluindo ou perdendo minério? | Controle de teor para produção de lavra | Precisão da escavação, sobrelavra/sublavra, diluição não planejada, perda de minério |
| Há perda entre a mina e a usina? | Produção de lavra para alimentação da usina | **Fatores de caminhão, calibração de balança de correia, manuseio de pilhas ROM, perdas em transporte** |
| A usina recuperou como previsto? | Alimentação da usina para produção da usina | Rendimento (yield), eficiência metalúrgica, material para rejeito |
| Perdemos produto entre a usina e o cliente? | Produção da usina para embarque | Degradação de produto, mudança de umidade, perdas em ferrovia/estocagem em porto, má alocação no porto |
| Desempenho ponta-a-ponta do ativo | Reserva para produção da usina / para embarque ("model to market") | Efeito cumulativo de tudo. **Bom para reportar, ruim para diagnosticar** |

## Regra do poder diagnóstico

Fatores ponta-a-ponta (recurso → produção da usina) são **poderosos para reporte-resumo e fracos
para diagnóstico**, porque agregam múltiplas fontes de variância. Sempre que possível, quebre em
elos menores.

Caso explícito (Fouet et al., 2009): a relação *controle de teor para alimentação da usina* é
historicamente confusa porque a maioria das minas opera pilhas in-pit e ROM entre os dois pontos.
**A boa prática é quebrá-la em "controle de teor para produção de lavra" + "produção de lavra para
alimentação da usina"**, permitindo rastrear o fluxo e isolar imprecisão de escavação de problemas
de medição/manuseio.

## Antes de escolher os fatores: mapear onde cada grandeza é REALMENTE medida

Esta é a etapa mais pulada e a que mais invalida diagnóstico. A lista padronizada de relações diz
o que *pode* ser reconciliado; **o fluxo de minério da mina específica diz o que faz sentido
reconciliar ali**. Duas minas com a mesma lista de fatores podem ter fatores que significam coisas
completamente diferentes, porque medem em pontos diferentes.

Levantar, nó a nó, **como cada grandeza chega ali**:

| Nó | Massa: pesada, contada, calculada por volume×densidade, ou estimada? | Teor: amostrado (como?) ou vindo de modelo? | Quem mede | Erro esperado |
|---|---|---|---|---|
| Modelo de recursos | estimada (blocos) | modelado | geologia de recursos | ver `04-fontes-de-erro.md` |
| Modelo de controle de teor | estimada (blocos) | modelado a partir de amostragem de curto prazo | geologia de mina | |
| Planejamento / STMP | volume × densidade | herdado do modelo | planejamento | |
| Lavra / produção | **pesada em balança? contagem × fator de caminhão? topografia × densidade?** | herdado do modelo, ou amostrado | operação / topografia | |
| Retomada de pilha | quase sempre **estimada ou por fator**, raramente pesada | modelo de pilha (aritmético, FIFO/LIFO ou 3D) | operação | |
| Alimentação da usina | balança de correia | amostrador automático | usina | |
| Produção da usina | balança / balanço metalúrgico | amostrado + balanço | usina | |

### Consequências práticas da resposta

**Se a massa é pesada em balança em todos os pontos exceto a retomada de pilha** (arranjo comum em
operações com balança rodoviária ou balança de correia bem instrumentada), então:

- A massa reportada **é** a massa medida. Não há correção de massa a fazer entre reportado e
  reconciliado — e o fato de `massa_reportada == massa_reconciliada` **não** é sinal de que falta
  verificação volumétrica. É consequência do arranjo de medição.
- O trabalho de reconciliação de massa se concentra em: **calibração das balanças**, e
  **a retomada de pilha**, que é o único ponto onde a massa é estimada e portanto o único que pode
  gerar divergência sistemática.
- A reconciliação de **teor** passa a ser o trabalho principal, porque é ali que a estimativa
  (modelo) encontra a medição (amostragem).
- **Sobrelavra e sublavra continuam existindo fisicamente**, mas não aparecem como diferença entre
  massa reportada e reconciliada. Aparecem como: massa pesada acima da massa de projeto **somada a**
  queda de teor (sobrelavra/diluição), ou massa pesada abaixo da massa de projeto (sublavra/perda).
  A comparação correta é **projeto (CMS/design) × massa pesada**, não reportado × reconciliado.

**Se a massa vem de contagem de caminhão × fator**, o cenário inverte: a massa passa a ser a maior
fonte de erro (faixa comum 15-30%, `04-fontes-de-erro.md`) e a validação mensal do fator de caminhão
contra balança ou topografia vira prioridade.

**Se a massa vem de topografia × densidade**, o erro de volume (±10%) e a densidade (±5-10%) dominam,
e a reconciliação precisa de ensaio de densidade por tipo de material.

### Regra

Nunca inferir a saúde do processo a partir do formato do relatório. Antes de dizer que um controle
está faltando, **perguntar onde a grandeza é medida**. Um número que não se move pode significar que
o controle não existe — ou que ele é desnecessário porque a grandeza é medida diretamente.

## Mapeamento de fluxo de minério e processos

(Morley, 2014; Hargreaves & Morley, 2014 — método que também alimenta o Código de Prática.)

O mapeamento tem dois elementos:

**1. A matriz.** Raias horizontais = **quem** (papéis/disciplinas); colunas verticais = **o quê**
(atividades/processos). O mapa "flui" do canto superior esquerdo ao inferior direito.

- Raias típicas: geologia de recursos, planejamento de mina, geologia de mina, topografia,
  operação de mina, processamento.
- Colunas típicas: modelagem geológica; modelagem e estimativa de recursos; planejamento/design/
  sequenciamento de longo prazo; planejamento de médio e curto prazo; controle de teor;
  perfuração e desmonte; lavra; estocagem e beneficiamento.
- Marcar no mapa: fontes de dado, pontos de decisão, relatórios/saídas, **pontos de reconciliação
  existentes** e **pontos de reconciliação propostos**.
- A maioria das minas cabe em uma única folha A0.

**2. O checklist SIPOC** (Supplier, Input, Process, Output, Customer) — preenche o "como" de cada
caixa da matriz:

- **Fornecedor (Supplier)**: de onde vem a informação necessária?
- **Entrada (Input)**: quais entradas são necessárias para completar o processo?
- **Processo (Process)**: o que é efetivamente feito com o dado e como? Há pontos de decisão ou
  laços de controle de qualidade?
- **Saída (Output)**: qual o resultado? Mais dado, um modelo, um relatório?
- **Cliente (Customer)**: para onde vai a saída? De quem este processo se torna fornecedor?

> "O benefício está na jornada de descoberta associada a desenhar o mapa de processos, mais do que
> no mapa acabado" (Morley, 2014). O valor vem das conversas com todos os envolvidos — quebra os
> silos técnicos e esclarece pontos que o próprio pessoal do site nunca teve tempo de questionar.

Uma sessão de mapeamento tipicamente leva **4-5 dias por site** com um time multidisciplinar
(geólogo de recursos + engenheiro de minas + metalurgista + um generalista) e identifica
**60 a 100 oportunidades acionáveis por site** (Hargreaves & Morley, 2014). Priorizar por
valor × facilidade de execução em um *heat map*; atribuir valor em US$ ou metal equivalente a cada
iniciativa.
