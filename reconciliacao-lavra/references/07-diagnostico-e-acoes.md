# Diagnóstico de desvios e ações corretivas

O objetivo deste arquivo é transformar um número de reconciliação em uma **hipótese testável** e
uma **ação**. Regra de ouro: os indicadores apontam a diferença; não resolvem o problema.

## Fluxo de diagnóstico

```
1. Isolar o elo    → qual relação intermediária está fora de controle?
2. Testar o dado   → o desvio cabe dentro da faixa de erro esperada da medição envolvida?
3. Testar a escala → o desvio está sendo medido numa escala apropriada ao modelo?
4. Testar a tendência → é ponto isolado ou 3+ períodos no mesmo sentido?
5. Levantar hipóteses de causa raiz (tabela abaixo)
6. Verificar contra a realidade física (o que aconteceu na mina no período?)
7. Definir ação SMART e monitorar o mesmo indicador para validar
```

**Passo 6 é obrigatório e frequentemente pulado.** Fouet et al. (2009): é importante que um
engenheiro de minas ou geólogo com conhecimento do que ocorre na cava (ou na subterrânea) no dia a
dia revise a reconciliação mensal e o balanço de massa para garantir que os números refletem o que
de fato aconteceu.

Exemplo de aplicação do passo 6 (Fouet et al., 2009): se a massa calculada por topografia de uma
pilha ROM é maior que a soma das massas dos blocos que a topografia estimou terem sido lavrados e
enviados a ela, as explicações possíveis são —

| Explicação | Solução correspondente |
|---|---|
| Erro no cálculo topográfico | Acionar a topografia para corrigir o cálculo |
| Material de outros blocos foi lavrado e enviado à pilha (escavação no piso ou em blocos vizinhos) | Atribuir ao material adicional um teor de controle de teor conforme sua origem e registrar, para reconciliação futura, que material daquela origem já foi lavrado |
| Estéril foi enviado à pilha (diluição) | Atribuir ao material adicional um teor de estéril apropriado |

## Tabela de diagnóstico por indicador

| Indicador fora de controle | Onde o problema provavelmente está | Hipóteses de causa raiz | Verificações e ações |
|---|---|---|---|
| **GM / Recurso → Controle de teor** | Conhecimento do corpo de minério | Interpretação geológica; espaçamento de sondagem insuficiente; wireframing restringindo indevidamente a estimativa; top cut excessivo; método de estimativa inadequado; viés entre RC e diamantada; densidade | Comparar RC × DD por par de amostras; revisar parâmetros de krigagem; testar estimativa sem hard boundary de wireframe; **sondagem de infill** (caso Antamina: adensamento reduziu o espaçamento e alinhou longo e curto prazo); revisar classificação de recurso e escala de reporte |
| **MP / Controle de teor → Plano (STMP)** | Tradução do modelo em plano executável | Diluição planejada mal parametrizada; premissas de recuperação de minério; design de polígonos/realces não aderente ao modelo; restrições operacionais não refletidas | Revisar fatores modificadores aplicados no planejamento; revisão por pares dos designs antes de escavar; documentar árvore de decisão de tipo de material |
| **MO / Plano → Produção de lavra** | **Execução da lavra** | Sobrelavra/sublavra; diluição operacional; perda de minério; erro de despacho (origem/destino); movimento do desmonte não corrigido nos polígonos; escavação imprecisa no contato; controle visual mudando limites | Compliance to plan espacial; CMS/levantamento de piso; ajuste pós-desmonte dos polígonos; revisão turno a turno do despacho; **ajustar prática de lavra nos contatos minério/estéril para controlar overbreak** (caso minério de ferro) |
| **Produção de lavra → Alimentação da usina** | **Medição e manuseio**, não geologia | Fatores de caminhão desatualizados; células de carga com falha; balança de correia descalibrada; fator de caçamba; manuseio e remanuseio de pilhas; latência de pilha; perdas em transporte | Health check de despacho; validação mensal do fator de caminhão contra balança/topografia; calibração de balança de correia; verificar se retomada de pilha foi somada ao basculamento direto |
| **PR / Alimentação → Produção da usina** | Processo/metalurgia | Rendimento e recuperação; material para rejeito; retenção de metal em moinho e bombas (Au); erro de amostragem de teor de cabeça; erro de umidade; calibração de balanças | Precisão de amostragem por estação de amostragem; revisar posicionamento das balanças para cobrir alimentação, produto e rejeito (grosso e fino); reconciliar contra **metal produzido** em vez de teor de cabeça |
| **Produção da usina → Embarque** | Logística | Degradação de produto; mudança de umidade; perdas em ferrovia e estocagem em porto; má alocação de material no porto | Correção de fundição/refino sistematicamente >1% exige auditoria adicional |
| **MR bom, mas GM e MO divergindo em sentidos opostos** | **Reconciliação ilusória** | Erros que se cancelam | Nunca aceitar. Investigar cada elo isoladamente; ver `01-fundamentos.md` |
| **Todos os indicadores bons, mas há minério no bota-fora** | Seleção de minério | Classificação incorreta minério/estéril; teor de corte operacional inadequado; contatos não visíveis sem amostragem adequada | Inspecionar pilhas de estéril; auditar classificação de tipo de material; considerar analisar o controle de teor **antes** de projetar o desmonte |
| **Reconciliação "de classe mundial" mas metas atingidas de forma suspeita** | *High grading* | Modelo subestimando qualidade → material de qualidade indo para estéril; planejadores e produção mirando zonas de alto teor para bater metas e bônus | Caso 2 de Hargreaves & Morley (2014). Verificar aderência espacial ao plano e destino do material marginal |

## Padrões de causa raiz documentados nos casos

**Caso Damang (ouro, Gana) — Schofield et al. (2013).** Reconciliação controle de teor → usina
deteriorou de −5% para −15% ao longo de 18 meses; chegou a haver investigação policial por furto.
A resposta da gestão foi *cortar os teores das amostras de controle de teor para baixar a previsão*
— tratando o sintoma. Quando o corte foi descontinuado, a reconciliação estabilizou. A causa real
foi **problema de amostragem** (amostragem em condições úmidas em áreas alagadas) e furos de
controle de teor mal locados no período inicial. Além disso, o modelo de viabilidade — fortemente
restringido por wireframe geológico — subestimou gravemente a tonelagem econômica, levando à
construção de uma usina descasada da capacidade da mina.

**Lições**: (a) ajustar o modelo para "fechar" o número é a resposta errada; (b) quando a
reconciliação piora, investigar **qualidade de amostragem e locação de furos** antes de mudar o
método de estimativa; (c) reconciliação ruim pode ter origem em decisão de projeto muito anterior.

**Caso CSA (cobre subterrâneo, Austrália) — Schofield et al. (2013).** Reconciliação semanal
introduzida para testar a mudança de interpretação 2D para 3D e os fatores de diluição/correção de
longo prazo, corrigindo também variações de densidade aparente entre domínios. Revelou que:
superestimativa de teor de cobre estava associada a superestimativa de massa em realces de baixa
densidade; a diluição real era menor que a estimada; o wireframing 3D reduziu o erro mas ainda
superestimava realces de alto teor com histogramas fortemente assimétricos. A adoção de MIK trouxe
definição bem melhor dos contatos e **+10% de massa de minério nos realces**.

**Lição**: em subterrânea, densidade aparente por domínio e método de estimativa adequado à
assimetria do teor são causas de primeira ordem — e reconciliação de alta frequência (semanal, por
realce) é o instrumento para detectá-las.

**Caso Sishen (minério de ferro, África do Sul) — Morley & Moller (2005).** Ganhos concretos após
sistema unificado: descoberta de que os caminhões estavam sendo **sub**carregados (a percepção era
de sobrecarga) → aumento de produção com a mesma frota; controle de remanuseio (*double handling*)
entre pilhas → redução de custo; padronização de convenções de nomes de bloco → correlação de massa
de minério entre topografia, despacho e usina passou a ficar **rotineiramente abaixo de 2% de
diferença**.

**Lição**: convenções de nomenclatura inconsistentes entre topografia, despacho e usina são uma
causa banal e muito comum de reconciliação ruim. Verificar sempre antes de procurar causa geológica.

**Caso brasileiro de ouro (Chieregati et al., 2007).** Sequência iterativa de mudanças no protocolo
de amostragem de furos de desmonte: (1) substituição de amostragem manual com pá por amostrador
setorial → menor variância; (2) vedação de borracha sobre a cúpula → menor viés por perda de finos;
(3) mais incrementos na britagem → estimativa mais confiável; (4) exclusão da vedação + aumento da
água de perfuração → **piorou** (lavagem de finos aumentou o erro de extração); (5) reinserção da
vedação e perfuração sem água → melhores estimativas e menor variância.

**Lição**: o passo 4 é o mais instrutivo — uma mudança bem-intencionada (mais água para reduzir
geração de finos) violou a condição de amostra correta e piorou tudo. Toda ação corretiva deve ser
**medida** contra o mesmo indicador antes de ser considerada bem-sucedida.

**Caso Macraes (ouro, Nova Zelândia) — Schofield et al. (2013).** Substituição de estimativa
poligonal por **simulação condicional** no controle de teor; migração de blocos pequenos com
wireframes de teor para painéis grandes com MIK recuperável no recurso; redução da proporção de
mineralização restringida por wireframe para ~50%; revisão do esquema de classificação. Resultado:
estimativas anuais de controle de teor passaram a ficar a poucos por cento do retrocálculo da usina,
e a confiança acumulada no histórico de reconciliação sustentou a decisão de expandir a lavra para
mineralização de baixo teor em período de preço desfavorável.

**Lição**: reconciliação favorável e consistente é **ativo de decisão de investimento**, não apenas
controle retroativo.

## O ciclo de melhoria contínua

(JORC guidelines / Fouet et al., 2009; Morley, 2003.)

1. **Medir e reportar** — calcular e reportar consistentemente as variâncias de massa, teor e metal
   para cada indicador, com a nomenclatura padronizada. Parte da rotina mensal e trimestral.
2. **Identificar desvios** — sinalizar sistematicamente indicadores fora dos limites acordados ou
   com tendência consistente ao longo de vários períodos.
3. **Diagnosticar a causa** — usar o framework para isolar o estágio da operação onde a variância se
   origina, e a tabela de fontes de erro para orientar a investigação.
4. **Implementar ação corretiva** — direcionada à causa identificada.
5. **Validar e repetir** — continuar medindo o indicador relevante para verificar se a ação
   resolveu e trouxe o processo de volta ao controle.

### Os dez passos para a prognosticação (Morley, 2003)

1. identificar as principais fontes de dados;
2. automatizar a captura desses dados;
3. estabelecer regras de negócio para validação;
4. armazenar os dados em um único banco de dados comercial;
5. estabelecer uma interface que permita análise eficiente;
6. pesquisar tendências e padrões nos dados;
7. investigar essas tendências e padrões buscando causas e efeitos;
8. usar essa informação para estabelecer e testar hipóteses;
9. desenvolver uma base de conhecimento que permita prever o desempenho futuro;
10. modificar constantemente a base de conhecimento por meio de análises adicionais.

### Do dado à previsão

(Morley, 2003.) Dado → Informação → Conhecimento → Previsão. Exemplo:

| Dado | Informação | Conhecimento | Previsão |
|---|---|---|---|
| Coletar dados de tipo de material e de vazão do britador | Para cada tipo de material, correlacionar a vazão média correspondente | A análise mostra que um tipo específico tem vazão média igual à metade da ótima | A vazão cairá se esse material for alimentado ao britador; não cairá se ele for blendado |

Esta é a essência da prognosticação: a análise dos dados da reconciliação fornece entendimento do
impacto das decisões operacionais sobre a usina e o metal produzido — e esse entendimento é usado
para manter a variância entre estimativa e realidade dentro de limites aceitáveis.
