# Exemplos

## `exemplo_entrada.json`

Formato de entrada do `reconciliacao.py`. Os números são o exemplo numérico verificado de
**Chieregati (2023)** — mina de ouro subterrânea — que também serve de caso de teste do
`--autoteste`.

```bash
python ../reconciliacao-lavra/scripts/reconciliacao.py --input exemplo_entrada.json
```

Saída esperada (base metal):

```
GM  = 0,924     modelo de longo prazo -> curto prazo
MP  = 0,992     curto prazo -> planejamento
MO  = 0,897     planejamento -> operação      <- elo crítico
MM  = 0,890     MP x MO
MR  = 0,823     longo prazo -> alimentação da usina
PR  = 0,863     alimentação -> produtos
MCF = 0,710     MR x PR
```

**A leitura que importa:** o MCF de 0,71 sozinho não diz nada acionável. Decomposto, aparecem
**duas frentes distintas**:

- **PR = 0,86** é o indicador mais distante de 1,00 — e é o que o script aponta como crítico pela
  regra do maior afastamento. É problema de planta: recuperação e perdas no processo.
- **MO = 0,90** é o elo crítico **do lado da mina** — execução de lavra. O modelo geológico
  (GM = 0,92) é razoável e o planejamento (MP = 0,99) é excelente, então o problema de mina não
  está na estimativa nem no plano: está na execução.

Donos diferentes, ações diferentes, e nenhuma das duas visível no MCF agregado.

É exatamente esse raciocínio que a skill reproduz em todo relatório, e é o motivo pelo qual fator
ponta-a-ponta serve para reportar e não para diagnosticar.

## Verificando os cálculos

```bash
python ../reconciliacao-lavra/scripts/reconciliacao.py --autoteste
```

Valida contra a literatura: indicadores de Chieregati (2023), *compliance to plan* dos dois casos
de Morley & Arvidson (2017), empolamento, diluição, recuperação de minério, sobrelavra/sublavra,
média ponderada e detecção de tendência.
