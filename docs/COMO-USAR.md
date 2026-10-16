# Como usar

## O acionamento

A skill dispara por linguagem natural. Você não precisa chamá-la pelo nome, nem usar a palavra
"reconciliação". Estes pedidos acionam:

- "o MCF caiu de 0,94 pra 0,79 em 3 meses, o que pode ser?"
- "analisa esse relatório de produção"
- "por que a mina não bate com a usina?"
- "calcula o overbreak desses realces"
- "preciso estruturar o código de reconciliação da nossa operação"
- "a planta reportou 8% menos massa que o despacho"
- "monta o relatório de fechamento do mês"

## A entrevista — e por que ela existe

Antes de calibrar qualquer cadeia, a skill levanta cinco coisas. Não é burocracia: cada uma muda
o que pode ser calculado e como o resultado deve ser lido.

**1. Qual é o fluxo de minério?** Da frente ao produto, na ordem real, com pilhas, remanuseio,
silo, britagem e embarque. Nó que a operação não tem sai da cadeia — não vira zero.

**2. Já existe uma cadeia de valor definida?** Se existe, ela manda. **Os nomes dos fatores podem
ser outros** na sua casa, e a skill usa os seus, mapeando para a nomenclatura descritiva só quando
for preciso comparar com literatura ou entre sites.

**3. Quais variáveis são medidas e quais são estimadas** — nó a nó, massa e teor separadamente.

> Esta é a pergunta que governa tudo. **Reconciliação compara medido com medido.** Um elo entre
> duas estimativas precisa ser rotulado como comparação de modelos, não como reconciliação.

**4. Em que base reportar?** Normalmente metal contido / produto final, mas varia. A skill pergunta
em vez de assumir, e se assumir, diz que assumiu.

**5. Quais são os gatilhos e tolerâncias?** Se não houver, ela usa as faixas da literatura **citando
a fonte** e recomenda formalizar — nunca apresenta limite de artigo como se fosse limite da operação.

## A validação da base

Antes de calcular, a skill roda `validar_base.py` e leva os achados a você. O que ela procura:

| Verificação | Por que importa |
|---|---|
| Cobertura temporal desigual entre nós | Comparar o total anual de um nó presente em 9 meses com outro em 5 produz desvio inteiramente artificial |
| Lançamento por evento misturado com fluxo mensal | Escaneamento e desmonte são lançados quando o evento ocorre, não mês a mês |
| Reconciliado × não reconciliado | O que é reconciliado primeiro não é amostra aleatória |
| Cadeia incompleta por realce | Indicadores sobre subconjuntos diferentes sem que isso fique visível |
| Nós integralmente vazios | Todo indicador que depende deles é não calculável — sem proxy |
| Massa negativa | Ajuste de inventário somado ao fluxo físico subestima a produção |
| Teor carimbado | Valor fixo em todos os registros é parâmetro, não medição |
| Metal não fecha com massa × teor | Unidade de teor ou base de umidade erradas |
| Quedas abruptas entre nós | Perda real ou erro de preenchimento |

**Nenhuma incoerência é decidida automaticamente.** Cada achado vem com as opções — incluir,
excluir, tratar à parte — e o impacto de cada uma em massa e metal, para a decisão ser informada.
A decisão entra na seção de premissas do relatório.

## Usando os scripts direto

### Cálculo

```python
from reconciliacao import No, cadeia_padrao, overbreak_underbreak

nos = {
  "box_model_lt":   No("Recurso LP",    massa=710677,  teor=1.586, teor_unidade="%", metal_unidade="t"),
  "box_model_st":   No("Recurso CP",    massa=758972,  teor=1.585, teor_unidade="%", metal_unidade="t"),
  "stope_st_model": No("Reserva Op CP", massa=1111476, teor=1.070, teor_unidade="%", metal_unidade="t"),
  "grade_control":  No("Escaneamento",  massa=1112808, teor=1.073, teor_unidade="%", metal_unidade="t"),
}
r = cadeia_padrao(nos, base="metal")
# r["indicadores"]      -> {"GM": 1.067, "MP": 0.989, "MO": 1.004, "Mrec": None, ...}
# r["nao_calculaveis"]  -> {"Mrec": "nó ausente: ore_reported", ...}
```

Nó ausente **nomeia qual nó falta** em vez de virar zero ou proxy.

```python
ob = overbreak_underbreak(volume_projetado=1000, volume_lavrado=1050, volume_em_projeto=960,
                          area_parede_exposta=400)
# ob["overbreak_pct"], ob["underbreak_pct"], ob["ELOS_m"], ob["alerta"]
```

O `alerta` dispara quando sobrelavra e sublavra quase se cancelam — o caso em que o líquido esconde
diluição por estéril **e** perda de minério ao mesmo tempo.

### Validação de base

```bash
python scripts/validar_base.py   # como biblioteca:
```
```python
from validar_base import validar_producao, relatorio_texto
achados = validar_producao(df, col_no="MOVIMENTACAO", col_entidade="MINA", col_periodo="MÊS",
                           col_massa="MASSA", col_metal="METAL", col_teor="TEOR")
print(relatorio_texto(achados))
```

### Planilhas

```bash
python scripts/normalizar_entrada.py --arquivo producao.xlsx --listar
python scripts/normalizar_entrada.py --arquivo producao.xlsx --aba <aba> --mapa mapa.json --out dados.json
```

O `--listar` inspeciona abas e colunas e **sugere** o mapeamento — que deve ser conferido antes de
calcular. Reconciliação com dado mal lido é pior que nenhuma.

### Gráficos e diagrama

```python
from graficos import waterfall_cadeia, tendencia, overbreak_underbreak, painel_html
from diagrama import cadeia_valor

waterfall_cadeia(nos, "título", "t", arquivo="wf.png")   # PNG para relatório paginado
painel_html("painel.html", "título", "lead", figuras)     # painel navegável, hover + tabela
cadeia_valor(faixas, indicadores, "título", arquivo="cadeia.svg")  # fluxograma
```

A skill **pergunta qual destino** você quer antes de gerar — PNG estático, painel HTML, ou os dois.

**Regra de dimensionamento:** nenhum texto abaixo de 6 pt na página final. Um fluxograma de onze
nós não cabe legível num A4 — e a resposta não é diminuir a fonte, é mudar o destino: página de
tamanho diferente no mesmo PDF (encarte A3 paisagem), versão condensada no corpo com a completa em
encarte, ou painel HTML com zoom. O parâmetro `escala_texto` de `cadeia_valor()` existe para isso.

## Adaptando a identidade visual

```
scripts/paleta.py   →  cor
scripts/tema.py     →  tipografia, escala, espaçamento, raio, traço, proporção
```

Trocar esses dois adapta PNG, painel HTML e corpo do PDF de uma vez. Depois de trocar a paleta,
**revalide**:

```bash
node <caminho-da-skill-dataviz>/scripts/validate_palette.js "<hex,hex,...>" --mode light --surface <sua-superfície>
```

A paleta atual é a instância de referência, validada para separação em daltonismo e contraste em
claro e escuro.

## Formatos de saída

| Situação | Saída |
|---|---|
| Pergunta conceitual ou diagnóstico | Resposta direta, com fontes |
| Relatório formal para circular | `.docx` ou `.pdf` a partir do template |
| Números para continuar analisando | `.xlsx` com as tabelas |
| Consulta recorrente | Painel HTML |
| Rascunho de código de prática | `.docx` ou markdown |

O relatório sai em **português** por padrão.
