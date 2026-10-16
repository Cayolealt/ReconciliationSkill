# Anexo — mapeamento de códigos legados para a nomenclatura padronizada

Use esta tabela quando o usuário chegar com códigos alfanuméricos (F1, R2, G3, M1, P1, T1, I1…)
vindos de um relatório, planilha ou norma de empresa. **Sempre traduzir para a nomenclatura
descritiva antes de calcular ou comparar qualquer coisa entre sites** — o mesmo código significa
coisas diferentes em empresas diferentes.

## Fouet et al. (2009), Tabela 1 — BMA × Rio Tinto

| Comparação reportada | Código BMA | Código Rio Tinto |
|---|---|---|
| Modelo de reservas / modelo de recursos | — | R1 |
| Modelo de lavra (controle de teor) / modelo de recursos | — | R3 |
| Produção de minério / modelo de recursos | — | G1 |
| Alimentação da usina / modelo de recursos | — | G2 |
| Produto da usina / modelo de recursos | — | G3 |
| Modelo de controle de teor / reservas de carvão | **F1** | R2 |
| Produção de minério / modelo de reservas | — | G4 |
| Alimentação da usina / modelo de reservas | — | G5 |
| Produto da usina / modelo de reservas | — | G6 |
| Vendas / reservas comercializáveis | **F3** | — |
| Produção ROM / modelo de controle de teor | **R1** | M1 |
| Modelo de controle de teor / alimentação da usina | **F2** | M3 |
| Produto da usina / modelo de controle de teor | — | M4 |
| Alimentação da usina / produção ROM | **R2** | M2 |
| Produto da usina / alimentação da usina | **R3** | P1 |
| Vendas de carvão / carvão produto | **R4** | T1 |

**A armadilha clássica**: o `F2` da BMA compara reservas de carvão ao modelo de controle de teor,
enquanto na Rio Tinto essa mesma comparação se chama `R2`. E o `F1` da Rio Tinto de 2006 não é o
`F1` da BMA. Fora dessas duas empresas há dezenas de outros códigos com o mesmo significado.

## Famílias de fatores da Rio Tinto (2009)

| Família | Escopo | Tipo |
|---|---|---|
| **R** (R1, R2, R3) | Relações entre modelo de recursos, modelo de reservas e modelo de controle de teor | Espacial |
| **G** (G1-G3 a partir do recurso; G4-G6 a partir da reserva) | Do modelo até in-pit/ROM, alimentação e produto final | Temporal (espacial se o minério tem fonte única) |
| **M** (M1-M4) | Controle de teor ↔ lavra ↔ entregue à usina. M1 e M2 rastreiam o fluxo de material e a acurácia da escavação; M3 combina os dois; M4 mede todas as perdas até o produto final | Temporal |
| **P** (P1) | Perdas através da usina. Só um fator, porque cada usina é diferente e o balanço metalúrgico já cobre a área | Temporal |
| **T** (T1) | Perdas no transporte do site até o porto | Temporal |

Unidades de negócio sem modelo de controle de teor não reportam M1, M3 e M4 — usam G4, G5 e G6 como
equivalentes.

## Famílias de fatores da BMA (2004, guia BTRAK)

- **Fatores F** — exigidos para reporte de governança.
- **Fatores R** — reconciliação de bloco e de painel, usada para orientar estimativas futuras de
  recurso e reserva e habilitar melhoria de negócio operacional:
  - **R1**: eficiência do processo de lavra — modelo de controle de teor × produção ROM;
  - **R2**: material rejeitado no britador — massa e qualidade da alimentação da usina × carvão ROM;
  - **R3**: eficiência do processo de lavagem do carvão (yield) — alimentação × produto da usina;
  - **R4**: eficiência do sistema de distribuição e perdas de transporte/estocagem.

## Indicadores I1-I5 (Chieregati, 2023)

Notação usada na apostila, equivalente ao modelo GM/MP/MO/PR:

| Código | Compara | Equivalente |
|---|---|---|
| **I1** | Produção prevista pelo modelo de longo prazo × prevista pelo modelo de curto prazo | GM |
| **I2** | Produção prevista pelo modelo de curto prazo × o que foi efetivamente lavrado | MM (ou MP × MO) |
| **I3** | O que foi lavrado × alimentação da usina | Produção de lavra → alimentação da usina |
| **I4** | Alimentação da usina × produtos da usina | PR |
| **I5** | Indicador combinado de reconciliação mina | MR |

## Outros fatores citados na literatura

| Fator | Definição |
|---|---|
| **MCF** (mine call factor) | Diferença entre a produção prevista pelos modelos e a produção registrada na usina. Historicamente aplicado às estimativas — **prática desencorajada** |
| **Fator model to mine** e **fator mine to mill** | Juras (2002), apud Chieregati (2023): multiplicados entre si, resultam no mesmo MCF |
| **SCF** (mine production to plant head) e **PCF** | Citados em Hargreaves & Morley (2014) como o foco típico — e insuficiente — na ponta de execução da cadeia |
| Fator de recursos e reservas, fator de volume | Fatores clássicos citados por Chieregati (2023) |

## Como conduzir a tradução com o usuário

1. Perguntar **quais são exatamente os dois nós comparados** — não aceitar o código como definição.
2. Confirmar a direção (quem é numerador, quem é denominador).
3. Confirmar a grandeza (massa, teor, metal) e a base (seca/úmida, tipo de material).
4. Renomear na nomenclatura descritiva e seguir com esse nome no relatório, mantendo o código
   legado entre parênteses na primeira menção, se for útil para o leitor do site.
