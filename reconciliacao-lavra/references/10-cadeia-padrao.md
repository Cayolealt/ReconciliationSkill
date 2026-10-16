# A cadeia de valor padrão da skill

Esta é a **cadeia de referência** que a skill assume quando o usuário não define outra. Ela vem do
esquema *Proposed Reconciliation System*, criado por **Joscil Spitzner Galvão (2020, atualização
2023), baseado em Ana Carolina Chieregati (2011)**. Sempre credite essa origem ao apresentar o
modelo. O esquema gráfico original não é distribuído com a skill; a descrição abaixo é suficiente
para montar e calcular a cadeia.

Por que ela substitui o modelo compacto GM/MP/MO/MM/MR/PR: aquele agrega toda a usina em um único
indicador (PR) e trata sobrelavra e sublavra como métricas derivadas. Esta cadeia **decompõe a
planta em três indicadores** e trata **overbreak e underbreak como nós de primeira classe** da
reserva — que é o que efetivamente se mede em operação subterrânea, e o que permite flagrar a
reconciliação ilusória sem cálculo extra.

## Os oito indicadores

| Sigla | Nome | Faixa da cadeia |
|---|---|---|
| **GM** | Geological Model | Modelo de blocos de longo prazo (orçamento) ↔ modelo de blocos de curto prazo |
| **MP** | Mine Planning | Modelo de blocos → modelos de realce (LT/orçamento e ST), via conversão recurso-reserva |
| **MO** | Mine Operation | Modelo de realce ST → o que foi efetivamente lavrado, via overbreak e underbreak |
| **Mrec** | Mine Reconciliation | Controle de teor (geologia) → minério reportado da mina para a planta |
| **PC** | Plant Control | Pilha antes da britagem e teor de cabeça na britagem secundária |
| **PO** | Plant Operation | Pilha de homogeneização e silo → teor de alimentação do moinho |
| **PR** | Plant Recovery | Alimentação do moinho → concentrado embarcado |
| **MCF** | Mine Call Factor | Ponta a ponta, do modelo de longo prazo ao embarque |

## Os nós, por faixa

### Faixa RECURSO
- **Box (Solid) Model LT (Budget)** — modelo de blocos de longo prazo, base do orçamento
- **Box (Solid) Model ST** — modelo de blocos de curto prazo

### Faixa RESERVA
- **Stope LT Model LT (Budget)** — modelo de realce de longo prazo, orçamento
- **Stope ST Model ST** — modelo de realce de curto prazo
- **Stope ST Model ST** (segundo estágio, já na faixa de execução)
- **Underbreak** — nó, não métrica derivada
- **Overbreak** — nó, não métrica derivada
- **Grade Control (Geology)** — controle de teor da geologia

### Faixa CONTROLE DE PLANTA
- **Stock Pile Before Crushing** — pilha antes da britagem
- **Head Grade (Secondary Crushing)** — teor de cabeça na britagem secundária
- **Homogenization Pile** — pilha de homogeneização
- **Ore Silo** — silo de minério
- **Feed Grade (Mill)** — teor de alimentação do moinho
- **Concentrate Shipment** — concentrado embarcado

## Os dois regimes de controle de minério

O esquema separa explicitamente dois regimes, e essa separação é o que evita misturar problema de
mina com problema de planta:

- **ORE CONTROL (HEAD GRADE) — MINE TO PLANT**: cobre de Mrec até o teor de cabeça na britagem
  secundária. É o regime que responde "o que a mina entregou".
- **ORE CONTROL (FEED GRADE) — PLANT TO SHIPMENT**: cobre da alimentação do moinho ao embarque.
  É o regime que responde "o que a planta fez com o que recebeu".

## Fontes de variação e pontos de amostragem

O esquema nomeia, para cada elo, **de onde vem a variação** — e essa é a parte que a maioria dos
sistemas de reconciliação omite. Ao montar a cadeia de uma operação, preencha esta lista com os
equivalentes locais; um elo sem fonte de variação identificada é um elo que não se consegue
diagnosticar.

**Fontes de variação (modelagem e planejamento):**
- Resource LT to Reserve Conversion — conversão recurso LP para reserva
- Stope Project Variation — variação de projeto de realce
- Resource ST to Reserve Conversion — conversão recurso CP para reserva
- Stope Planned Dilution — diluição planejada do realce
- Operational Factors (Topographic Survey) — fatores operacionais, levantamento topográfico

**Pontos de amostragem (medição):**
- Geology Grade Control — controle de teor da geologia
- Ore Reported (Mine to the Plant) — minério reportado da mina para a planta
- Secondary Crushing Sampling — amostragem na britagem secundária
- Plant Control — controle de planta
- Mill Feed Grade Sampling — amostragem do teor de alimentação do moinho
- Mill and Tailing Sampling — amostragem de moinho e rejeito
- Shipped Concentrate Sampling — amostragem do concentrado embarcado

A herança de Chieregati aparece aqui: **cada nó de medição tem um protocolo de amostragem nomeado**.
Isso é o que torna a cadeia auditável — sem protocolo declarado por ponto, a variância medida não
tem como ser atribuída a causa (ver `04-fontes-de-erro.md`).

## Como usar esta cadeia

1. **Mapear os nós que a operação realmente tem.** Nem toda mina tem silo, pilha de homogeneização
   ou britagem secundária. Nó ausente sai da cadeia; não vira zero e não é substituído por proxy.
2. **Declarar onde cada grandeza é medida** em cada nó presente (ver `02-cadeia-de-valor.md`,
   seção de pontos de medição). Massa pesada, contada ou calculada? Teor amostrado ou modelado?
3. **Nomear a fonte de variação de cada elo.** Use as listas acima como ponto de partida.
4. **Calcular apenas os indicadores cujos dois nós existem e são medidos.** Os demais são
   reportados como não calculáveis, com o motivo — nunca aproximados.
5. **Reportar overbreak e underbreak separadamente**, como nós, nunca pelo líquido.

## Convenção de cálculo

Vale a mesma de sempre (Morley & Arvidson, 2017): a cadeia é lida da esquerda para a direita e o
**nó mais antigo é sempre o denominador**. Massa, teor e metal são reportados juntos.

> **Confirmar com o usuário antes de assumir:** o esquema mostra a *faixa* que cada indicador
> cobre, mas a definição exata de numerador e denominador de cada um pertence ao código de prática
> da operação. Ao usar esta cadeia pela primeira vez em um site, confirme com o responsável quais
> são os dois nós exatos de GM, MP, MO, Mrec, PC, PO e PR naquela operação — sobretudo na faixa da
> planta, onde PC, PO e PR podem ser definidos de mais de uma forma legítima.
