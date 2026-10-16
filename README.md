# reconciliacao-lavra

Uma **skill do Claude** para reconciliação de lavra (*mine reconciliation* / MVCR), construída sobre a
literatura técnica da área — Fouet, Morley, Arvidson, Chieregati, Crawford, Schofield.

Ela não é um conjunto de fórmulas. É um conjunto de **comportamentos**: decompor antes de concluir,
separar sinal de ruído, reagir a tendência e não a ponto, nunca aplicar fator para fechar o número,
e dizer com todas as letras o que os dados não permitem afirmar.

```
Sem a skill  ████████████░░░░░░░░  61%   (14/23 critérios)
Com a skill  ████████████████████  100%  (23/23 critérios)
```

---

## O que ela faz

Quatro modos de trabalho, que se combinam:

| Modo | Para quê |
|---|---|
| **Consultoria metodológica** | Quais fatores existem, o que cada um responde, como mapear erros, como montar a cadeia de valor — sempre com a fonte citada |
| **Cálculo e relatório** | Lê planilha, PDF ou texto colado, valida a base, calcula em massa/teor/metal, decompõe a cadeia, diagnostica e monta o relatório |
| **Diagnóstico de desvio** | "O MCF caiu de 0,94 para 0,79" → decompõe em elos, ordena hipóteses, diz o que verificar em cada uma |
| **Construir o processo** | Conduz pelo guia do código de prática, capítulo a capítulo, e devolve o documento com as lacunas marcadas |

### Os indicadores

Cadeia de referência completa, com oito indicadores:

**GM** (modelo geológico) · **MP** (planejamento) · **MO** (operação de lavra) · **Mrec** (reconciliação
de mina) · **PC** (controle de planta) · **PO** (operação de planta) · **PR** (recuperação) ·
**MCF** (ponta a ponta)

Mais: *compliance to plan* espacial e temporal, sobrelavra e sublavra como **nós da cadeia** (não
métricas derivadas), diluição, recuperação de minério, ajuste de pilha, densidade aparente,
fator de caminhão, cobertura de reconciliação.

> Estrutura de referência da cadeia: **Joscil Spitzner Galvão (2020, rev. 2023)**, baseada em
> **Ana Carolina Chieregati (2011)**.

---

## Instalação

**1. Baixe o pacote**

Pegue `reconciliacao-lavra.skill` em [Releases](../../releases) — ou empacote o diretório você mesmo:

```bash
zip -r reconciliacao-lavra.skill reconciliacao-lavra/ -x "*__pycache__*"
```

**2. Instale**

- **Claude (app / Cowork):** anexe o arquivo `.skill` numa conversa e clique em **Save skill**.
- **Claude Code:** copie o diretório `reconciliacao-lavra/` para `~/.claude/skills/`.

**3. Dependências dos scripts** (só se for usar os cálculos e gráficos)

```bash
pip install pandas openpyxl matplotlib reportlab cairosvg pypdf
```

---

## Como usar

A skill é acionada por linguagem natural — não precisa chamar pelo nome. Estes pedidos disparam:

```
"o MCF caiu de 0,94 pra 0,79 em 3 meses, o que pode ser?"
"analisa esse relatório de produção e me diz onde está o problema do mês"
"por que a mina não bate com a usina?"
"preciso estruturar o código de reconciliação da nossa operação"
"calcula o overbreak desses realces a partir do CMS"
```

**Antes de calcular, ela vai perguntar** — e isso é de propósito:

1. Qual é o fluxo de minério?
2. Já existe uma cadeia de valor definida? Os nomes dos fatores são outros?
3. **Quais variáveis são medidas e quais são estimadas?**
4. Em que base reportar — metal, massa ou teor?
5. Quais são os gatilhos e tolerâncias da operação?

A terceira é a que mais importa: **reconciliação compara medido com medido.** Comparar duas
estimativas dá a diferença entre dois modelos, não um resultado de reconciliação.

Guia completo em **[docs/COMO-USAR.md](docs/COMO-USAR.md)**.

---

## O comparativo

Três casos de teste reais, cada um rodado **com a skill** e **sem** (mesmo prompt, mesmo modelo).

| Caso de teste | Com skill | Sem skill |
|---|:---:|:---:|
| Ler relatório gerencial de produção e diagnosticar | **9/9** | 6/9 |
| Diagnosticar MCF em queda | **7/7** | 5/7 |
| Estruturar código de prática | **7/7** | 3/7 |
| **Total** | **23/23 (100%)** | **14/23 (61%)** |

**O que o modelo sozinho já faz bem:** analisa produção razoavelmente, decompõe em elos, lista
hipóteses plausíveis, não sugere fraudar o número.

**O que ele não faz sem a skill:**

- **Citar fonte** — 0/3 nos baselines, 3/3 com a skill. A assertiva mais discriminante do conjunto.
  Conselho correto mas não rastreável não sustenta decisão de governança.
- **Distinguir cobertura de fator** — ler "taxa de reconciliação de 29%" como desempenho quando
  significa que 29% da produção foi reconciliada.
- **Conferir o dado antes de calcular** — mostrar o que entendeu e pedir confirmação.
- **Cobrir governança** — champion, dono sênior, accountability, o alerta de que planilha não é
  banco de dados. O baseline não cobre nada disso (3/7 no caso do código de prática).

Análise completa, com as respostas lado a lado: **[docs/COMPARATIVO.md](docs/COMPARATIVO.md)**.

---

## Os princípios

Os nove que governam tudo na skill:

1. **Pró-ativa, não reativa.** Nunca gerar fator para corrigir estimativa — ajustar processo para
   o resultado cair dentro de limites aceitáveis.
2. **Nomenclatura descritiva.** "Modelo de controle de teor para produção de lavra", nunca "F2" —
   códigos alfanuméricos significam coisas diferentes em cada empresa.
3. **O nó mais antigo é sempre o denominador.** Um "+" consistente não é bom: significa que o
   modelo subestima.
4. **Decompor antes de concluir.** Fator ponta-a-ponta reporta, não diagnostica.
5. **Reconciliação compara medido com medido.**
6. **Sinal versus ruído.** O desvio cabe na faixa de erro esperada daquela medição?
7. **Tendência, não ponto.** Três períodos no mesmo sentido é problema sistêmico.
8. **Rastreabilidade.** Toda fórmula e faixa leva a fonte.
9. **Honestidade sobre limitação.** Dizer o que os dados não permitem afirmar é parte do trabalho.

E alguns comportamentos duros que decorrem deles:

> **Sobrelavra e sublavra sempre separados, nunca o líquido** — eles se compensam em volume
> enquanto destroem valor em teor.
>
> **Todo resultado sai acompanhado da sua cobertura** — um fator sobre 15% da produção não é
> comparável a um sobre 100%.
>
> **Nunca inferir controle faltante pelo formato do relatório** — perguntar onde a grandeza é
> medida antes de dizer que falta verificação.
>
> **Nenhuma incoerência na base é decidida sozinha** — levar as opções ao usuário com o impacto
> de cada uma.

---

## Estrutura

```
reconciliacao-lavra/
├── SKILL.md                       362 linhas — princípios, roteamento, modos, comportamentos
├── references/                    12 arquivos, ~1.800 linhas de metodologia extraída e citada
│   ├── 00-fontes.md               bibliografia e o que cada fonte resolve
│   ├── 01-fundamentos.md          tipos, reativa × pró-ativa, reconciliação ilusória, JORC
│   ├── 02-cadeia-de-valor.md      relações padronizadas, pontos de medição, SIPOC
│   ├── 03-formulas-e-calculos.md  fórmulas, indicadores, cobertura, overbreak, compliance
│   ├── 04-fontes-de-erro.md       tabela mestra de erros, QA/QC por nó, teoria de amostragem
│   ├── 05-tolerancias-e-gatilhos.md faixas, semáforo, ranking de confiança
│   ├── 06-codigo-de-pratica.md    os 5 elementos, templates, accountability
│   ├── 07-diagnostico-e-acoes.md  fluxo de 7 passos, causa raiz, casos documentados
│   ├── 08-pilhas-e-estoques.md    estratégia, modelagem, ajustes
│   ├── 09-orcamento-e-ciclo-mensal.md orçamento anual, variações mensais
│   ├── 10-cadeia-padrao.md        a cadeia de referência, oito indicadores
│   └── anexo-codigos-legados.md   F1/R2/G3/M1/I2 → nomenclatura descritiva
├── scripts/                       7 módulos, ~1.900 linhas
│   ├── reconciliacao.py           cálculos determinísticos + `--autoteste`
│   ├── validar_base.py            detecção de incoerências antes do cálculo
│   ├── normalizar_entrada.py      leitura tolerante de planilhas
│   ├── graficos.py                waterfall, tendência, divergente · PNG e painel HTML
│   ├── diagrama.py                fluxograma da cadeia em SVG
│   ├── paleta.py                  cor — validada, trocável
│   └── tema.py                    tipografia, escala, espaçamento, traço — trocável
├── assets/
│   ├── template_relatorio.md      11 seções
│   ├── guia_codigo_de_pratica.docx roteiro do modo "construir o processo"
│   └── exemplo_entrada.json
└── evals/evals.json               casos de teste
```

### Os cálculos são verificados contra a literatura

```bash
python scripts/reconciliacao.py --autoteste
```

Valida GM/MP/MO/MM/MR/PR/MCF contra o exemplo numérico de Chieregati (2023), *compliance to plan*
contra os dois casos de Morley & Arvidson (2017), empolamento, diluição, recuperação de minério e
sobrelavra/sublavra. **Todos passam** — e é isso que separa um número confiável de um plausível.

---

## Identidade visual

Trocar **dois arquivos** adapta tudo à identidade da sua empresa:

- `scripts/paleta.py` — cor (validada para daltonismo e contraste; revalide a sua)
- `scripts/tema.py` — tipografia, escala, espaçamento, raio, traço, proporção

Os três destinos — PNG do relatório, painel HTML e corpo do PDF — leem desses dois. Uma mudança
vale para todos de uma vez.

---

## Sobre as referências bibliográficas

Os artigos originais **não estão neste repositório** — são material protegido por direito autoral.
O que está aqui é o **conteúdo operacional extraído** (fórmulas, faixas, critérios, definições),
com citação de autor e ano em cada caso, no formato que a literatura técnica usa normalmente.

A bibliografia completa está em [`references/00-fontes.md`](reconciliacao-lavra/references/00-fontes.md).
Para usar a skill com os PDFs disponíveis para consulta direta, coloque-os em
`reconciliacao-lavra/references/artigos/`.

---

## Licença

[MIT](LICENSE) para o código e a documentação deste repositório.

Não se aplica aos artigos de terceiros citados, nem à estrutura da cadeia de valor de referência,
cujo crédito é de Joscil Spitzner Galvão (2020, rev. 2023) e Ana Carolina Chieregati (2011).
