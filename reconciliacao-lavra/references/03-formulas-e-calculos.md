# Fórmulas e cálculos

Todos os cálculos determinísticos desta seção estão implementados em `scripts/reconciliacao.py`.
**Use o script em vez de fazer aritmética manualmente** — ele evita erro de sinal, aplica a
convenção correta de denominador e faz a ponderação por massa dos teores.

## Convenção fundamental: quem vai no denominador

(Morley & Arvidson, 2017; Parker, 2011.)

A cadeia de valor é lida **da esquerda para a direita** e **o nó mais antigo é sempre o denominador**.

Duas formas equivalentes de expressar o mesmo resultado:

**Como fator (razão):**
```
fator = nó_posterior / nó_anterior          (1,00 = sem variação)
```

**Como variação percentual:**
```
variação % = (nó_posterior − nó_anterior) / nó_anterior = (nó_posterior / nó_anterior) − 1
```

Interpretação:
- Fator > 1,00 (variação "+"): o nó posterior é **maior** que o anterior — ganho ao longo da cadeia.
- Fator < 1,00 (variação "−"): perda ao longo da cadeia.

**Um resultado "+" não é necessariamente bom.** Uma relação que consistentemente mostra +25%
significa que o nó anterior (geralmente o modelo ou o plano) está **subestimando** sistematicamente
o resultado medido. Isso não é um bom resultado: exige ação para melhorar a qualidade do modelo/plano
ou corrigir problemas de medição/amostragem, de modo a reduzir a variação (Morley & Arvidson, 2017).

Exemplo (Morley & Arvidson, 2017, Tabela 1): orçamento 4.974.000 t de minério; usina recebeu
5.172.960 t. Variação = (5.172.960 − 4.974.000)/4.974.000 = **+4%**.

## As três grandezas — sempre reportar as três

Para cada relação, reportar **massa, teor e metal contido**:

```
fator_massa  = massa_posterior / massa_anterior
fator_teor   = teor_posterior  / teor_anterior      ← teores SEMPRE ponderados por massa
fator_metal  = metal_posterior / metal_anterior ≈ fator_massa × fator_teor
```

onde `metal = massa × teor` (ajustar unidade: para g/t → onças, `oz = massa_t × teor_g/t / 31,1035`;
a apostila da Chieregati usa a simplificação 1 oz = 30 g em exercícios — **não** usar essa
simplificação em relatório real).

Regra crítica: **o teor de um agregado é a média ponderada pela massa**, nunca a média aritmética
dos teores dos blocos/períodos. Fouet et al. (2009) usam explicitamente "*depleted mass averaged
grade*" em todas as fórmulas.

Nota de preferência (Fouet et al., 2009, tabela de fontes de erro): quando o erro de amostragem de
teor de cabeça é grande, **reconciliar contra metal produzido é mais confiável do que contra teor
de cabeça**.

## Fórmulas por relação padronizada

Fonte: Fouet et al. (2009), Tabelas 3-21. "Depleções" (*depletions*) = massa e teor do modelo
estimados dentro de um volume lavrado específico e levantado por topografia, para o período reconciliado.

| Relação | Massa | Teor |
|---|---|---|
| Recurso → Reserva | depleções reserva / depleções recurso | teor pond. reserva / teor pond. recurso |
| Recurso → Controle de teor | depleções CT / depleções recurso | teor pond. CT / teor pond. recurso |
| Reserva → Controle de teor | depleções CT / depleções reserva | teor pond. CT / teor pond. reserva |
| Recurso → Produção de lavra | produção de lavra / depleções recurso | teor produção / teor pond. recurso |
| Reserva → Produção de lavra | produção de lavra / depleções reserva | teor produção / teor pond. reserva |
| Controle de teor → Produção de lavra | produção de lavra / depleções CT | teor produção / teor pond. CT |
| Produção de lavra → Alimentação usina | alimentação usina / produção de lavra | teor amostrado alimentação / teor produção |
| Controle de teor → Alimentação usina | alimentação usina / depleções CT | teor amostrado alimentação / teor pond. CT |
| Alimentação usina → Produção usina | produção usina / alimentação usina | teor amostrado produto / teor amostrado alimentação |
| Produção usina → Embarque | embarcado / produção usina | teor amostrado embarque / teor amostrado produto |
| Reserva → Embarque | embarcado / depleções reserva | teor amostrado embarque / teor pond. reserva |

**Regra do polígono único** (relações modelo × modelo): as depleções dos dois modelos devem ser
geradas com **o mesmo polígono de topografia** (levantamento in-pit / CMS), senão não é comparação
espacial verdadeira. Se o dado de controle de teor não estiver dentro do pacote de modelagem, é
essencial garantir que os dados dos dois modelos representam a mesma área depletada.

**Regra de calibração para latência de pilha**: nas relações que terminam em alimentação ou
produção da usina, recomenda-se calibrar os números do modelo para o tempo de residência em pilha.
Nas que terminam em produção da usina, calibrar também para a recuperação/yield metalúrgico esperado.

**Fonte da produção de lavra**: dados de despacho para o material que sai da cava, **corrigidos por
topografia**. Se os teores não foram amostrados, os teores estimados vêm do modelo de controle de
teor para os blocos lavrados.

## Modelo de indicadores pró-ativos (Chieregati, 2023)

Modelo compacto, ideal para dashboard e para diagnóstico rápido em português.

```
MODELO DE      MODELO DE      PLANEJA-      OPERAÇÃO      ALIMENTAÇÃO     PRODUTOS
LONGO PRAZO    CURTO PRAZO    MENTO         (lavrado)     DA USINA        DA USINA
     └── GM ──────┘  └── MP ──────┘  └── MO ──────┘            └─── PR ────┘
     └────────── MR (reconciliação mina) ──────────┘
     └──────────────────── MCF ─────────────────────────────────────────┘
```

| Indicador | Nome | Cálculo | O que responde |
|---|---|---|---|
| **GM** | Geological Model / Modelo | curto prazo / longo prazo | O modelo de longo prazo prevê bem o de curto prazo? Testa conhecimento do corpo de minério |
| **MP** | Mine to Plan | planejamento / curto prazo | O planejamento traduz fielmente o modelo de curto prazo? Captura diluição planejada |
| **MO** | Mine Operation | operação (lavrado) / planejamento | A operação executou o plano? Captura diluição operacional, perda de minério, sobrelavra |
| **MM** | Mine to Mill | operação / curto prazo = MP × MO | Efeito combinado de planejamento + execução |
| **MR** | Mine Reconciliation | alimentação da usina / longo prazo = GM × MP × MO | Desempenho acumulado de modelagem + planejamento + lavra. **Meta: o mais próximo de 100%** |
| **PR** | Plant Reconciliation | produtos da usina / alimentação da usina | Desempenho e recuperação da usina |
| **MCF** | Mine Call Factor | produtos / longo prazo = **MR × PR** | Fator global. Só reportar; nunca aplicar às estimativas |

Nomenclatura equivalente na síntese JORC: MI (Model Indicator) ≈ GM, PI (Planning Indicator) ≈ MP,
OI (Operation Indicator) ≈ MO, MR e PR iguais.

### Exemplo numérico verificado (Chieregati, 2023, mina de ouro subterrânea)

| Nó | Massa (t) | Teor (g/t) | Metal (oz) |
|---|---|---|---|
| Modelo longo prazo | 70.000 + 10.000 | 2,76 | 7.100 |
| Modelo curto prazo | 56.000 + 8.000 + 16.000 = 80.000 | 2,55 | 6.560 |
| Planejamento | 56.000 + 8.000 + 11.000 = 75.000 | 2,70 | 6.510 |
| Operação (= alimentação usina) | 57.000 + 14.000 + 4.000 = 75.000 | 2,42 | 5.840 |
| Produtos da usina | — | — | 5.040 |
| Rejeito | 74.999 | 0,33 | 800 |

```
GM  = 6.560 / 7.100 = 0,92
MP  = 6.510 / 6.560 = 0,99
MO  = 5.840 / 6.510 = 0,90     ← indicador crítico deste sistema
MM  = MP × MO = 0,89
MR  = GM × MM = 5.840 / 7.100 = 0,82
PR  = 5.040 / 5.840 = 0,86
MCF = MR × PR = 0,82 × 0,86 = 0,71   (= 5.040 / 7.100 ✓)
```

Leitura: o MCF de 0,71 sozinho não diz nada acionável. Decomposto, **MO = 0,90 é o elo crítico**
— o problema está na execução da lavra, não no modelo geológico (GM = 0,92 é razoável) nem no
planejamento (MP = 0,99 é excelente). PR = 0,86 é a segunda frente. Este é exatamente o raciocínio
que a skill deve reproduzir em todo relatório.

Do mesmo exemplo:
```
recuperação de minério (massa) = 71.000 / 75.000 = 95%
diluição (massa)               =  4.000 / 75.000 =  5%
diluição (teor)                = (2,70 − 2,42) / 2,70 = 12%
```

## Cobertura de reconciliação (≠ fator de reconciliação)

Métrica de **progresso do processo**, não de desempenho da mina:

```
cobertura de reconciliação = metal (ou massa) já reconciliado / metal (ou massa) reportado no período
```

Responde "quanto da produção do período já passou efetivamente pelo processo de reconciliação".
É legítima e útil — mede se o processo está conseguindo acompanhar a produção — e conversa
diretamente com o ranking de confiança (`05-tolerancias-e-gatilhos.md`).

**Cuidado de nomenclatura, obrigatório.** Chamar essa métrica de "taxa de reconciliação" é perigoso:
qualquer leitor fora da equipe técnica vai interpretar "taxa de reconciliação de 29%" como uma mina
entregando 29% do previsto — quando na verdade significa que 29% da produção já foi reconciliada.
Nomear como **"cobertura de reconciliação"** ou **"% da produção reconciliada"**, e nunca exibi-la na
mesma tabela ou no mesmo eixo que um fator de reconciliação sem rótulo que as distinga.

Ao encontrar dois valores diferentes de "metal reconciliado" no mesmo relatório, verificar se um
deles é o metal reconciliado **do subconjunto já processado** (numerador da cobertura) e o outro é o
metal reconciliado **do total** — são coisas diferentes e ambas podem estar corretas. Perguntar como
cada um é montado em vez de deduzir: a aritmética costuma admitir mais de uma explicação.

### A cobertura qualifica todo resultado que a acompanha

Um fator de reconciliação calculado sobre 30% da produção do período **não é o fator do período**.
Ele é o fator daquela fração, e a fração pode não ser representativa — normalmente não é, porque o
que é reconciliado primeiro costuma ser o que tem levantamento pronto, o que teve problema, ou o
que é mais fácil, e nenhum desses é uma amostra aleatória da produção.

Regras que decorrem disso:

- **Reportar sempre o par (resultado, cobertura).** "MR = 0,93 sobre 100% da produção" e
  "MR = 0,93 sobre 31% da produção" são afirmações de força muito diferente.
- **Não consolidar coberturas diferentes sem ressalva.** Somar um site reconciliado a 15% com outro
  a 90% produz um consolidado cuja cobertura efetiva é ponderada e cujo significado é ambíguo.
- **Não comparar períodos com coberturas diferentes** como se fosse tendência. Uma "melhora" pode
  ser só mudança na fração reconciliada.
- **Tratar a cobertura baixa como achado, não como contexto.** Se apenas parte da produção é
  reconciliada, perguntar o que trava o resto: levantamento pendente, dado de laboratório atrasado,
  falta de gente, realce ainda em lavra. Cobertura crescente ao longo do tempo é um dos sinais mais
  claros de sistema de reconciliação amadurecendo — e conversa direto com os critérios do ranking de
  confiança (`05-tolerancias-e-gatilhos.md`).

## Diluição e recuperação de minério

```
diluição (massa)  = massa de estéril enviada como minério / massa total lavrada como minério
diluição (teor)   = (teor previsto − teor realizado) / teor previsto
recuperação (massa) = massa de minério planejado efetivamente recuperada / massa de minério planejada
perda de minério  = 1 − recuperação de minério
```

Diluição e perda de minério são **fatores modificadores** do JORC: a reconciliação mede seus valores
realizados contra os estimados no estudo, dando base empírica para refinar reservas futuras.

## Sobrelavra e sublavra (overbreak / underbreak)

Conceito **espacial** — comparação 3D entre o sólido projetado e o sólido efetivamente lavrado
(CMS em realce subterrâneo, levantamento de banco/piso em cava).

> **Onde procurar sobrelavra quando a massa é pesada em balança.** Se a massa lavrada é pesada
> diretamente, sobrelavra e sublavra **não** aparecem como diferença entre massa reportada e
> reconciliada — a massa reportada já é a massa real. A comparação correta é **massa/volume de
> projeto × massa pesada**, cruzada com o teor: sobrelavra = massa pesada acima do projeto **com**
> queda de teor (diluição por encaixante); sublavra = massa pesada abaixo do projeto. Ver
> `references/02-cadeia-de-valor.md`, seção sobre pontos de medição.

```
volume_sobrelavra (overbreak)  = volume lavrado FORA do sólido projetado
volume_sublavra  (underbreak)  = volume do sólido projetado NÃO lavrado
volume_em_projeto              = interseção (lavrado ∩ projetado)

ELOS (Equivalent Linear Overbreak/Slough) = volume_sobrelavra / área da parede exposta   [m]

overbreak %  = volume_sobrelavra / volume_projetado
underbreak % = volume_sublavra   / volume_projetado
```

Consequências a avaliar sempre (Chieregati, 2023, Exercício 3):
- **Sobrelavra** → diluição por estéril de encaixante, queda do teor alimentado, massa extra
  movimentada e processada sem receita associada, risco geotécnico, aumento de custo por onça/tonelada.
- **Sublavra** → perda de minério (fica no maciço, muitas vezes irrecuperável), massa abaixo do
  plano, sub-utilização da usina; **não aparece na equação de reconciliação usual**, porque o metal
  não medido na usina nunca é contabilizado.

Sobrelavra e sublavra podem coexistir no mesmo realce e **se compensar em massa** enquanto destroem
valor em teor — mais um caso de reconciliação ilusória. Reportar sempre os dois separadamente,
nunca só o líquido.

## Compliance to plan (Morley & Arvidson, 2017)

Comparar massa, teor e produto **não** responde "lavramos onde e quando planejamos". Isso exige
comparação **espacial** (volumes em 3D) e **temporal** (por mês) contra o plano de curto prazo (STMP).

Três categorias, obtidas por comparação 3D entre superfície topográfica existente, superfície
planejada e superfície como lavrada:

| Categoria | Descrição |
|---|---|
| **Lavrado em plano** (*mined in plan*) | Lavrado na área planejada e no mês planejado |
| **Lavrado não planejado** (*mined not planned*) | Lavrado, mas fora da área planejada para o mês |
| **Planejado não lavrado** (*planned not mined*) | Planejado, mas não lavrado no mês planejado |

```
compliance to plan = lavrado_em_plano / (lavrado_em_plano + planejado_não_lavrado + lavrado_não_planejado)
```

Exemplos: 1600/(1600+0+0) = **100%**; 1400/(1400+200+700) = **61%**.

Reportar mensalmente **e** acumulado no ano/período orçamentário. Se o STMP estiver alinhado ao
orçamento anual, o acumulado mostra a aderência ao plano anual. Nos autores, esta é **rotineiramente
uma das métricas de pior desempenho em qualquer mina — e por isso uma grande oportunidade de valor**.

## Ajuste por pilhas de estoque

Quando há movimentação de pilha não orçada, ajustar o nó de origem antes de calcular a relação
(Morley & Arvidson, 2017):

```
"origem" para alimentação da usina =
    ( alimentação_usina / (origem − material_enviado_a_pilhas + material_retomado_de_pilhas) ) − 1
```
Teores/qualidades derivados por este cálculo devem ser **ponderados por massa**.

Relações tipicamente impactadas por pilhas: recurso→alimentação, reserva→alimentação,
controle de teor→alimentação, orçamento→entregue à mina, orçamento→contabilizado na usina.

## Densidade aparente de pilhas (Morley & Arvidson, 2017)

```
volume × densidade aparente = massa
```

Ao desmontar, a **massa se conserva mas o volume aumenta** (vazios entre fragmentos), logo a
densidade aparente cai. Exemplo: bloco in situ de 370,4 m³ a 2,7 g/cm³ = 1000 t. Com empolamento
de 35%: 1,35 × 370,4 = 500 m³ → densidade aparente = 1000/500 = **2,0 g/cm³**. Quanto maior o
fragmento, maior o volume e menor a densidade aparente.

**Melhor método** (pilha de material desmontado): pesar caminhões em balança rodoviária ao construir
uma pilha nova; após concluída, levantar topograficamente; densidade = massa/volume (base úmida).
Alternativa sem balança rodoviária: usar balanças de caminhão (VIMS) ou contagem × fator de caminhão.

**Pilha de minério britado**: massa via balança de correia pós-britagem (entradas) menos balança de
saída da pilha, até a data do levantamento; volume por topografia; densidade = massa/volume.

Boa prática: trabalhar em **base seca** e aplicar fatores de umidade sazonais; **sempre indicar a
base de umidade** do resultado. Proporções variáveis de tipos de material também alteram a densidade
de pilhas mistas.

## Fatores de caminhão (Fouet et al., 2009; Morley & Arvidson, 2017)

Razão que converte um carregamento (ou contagem de caminhão) em toneladas.

**Por balança rodoviária:**
```
massa por caminhão por tipo de material = peso do caminhão carregado − peso do caminhão vazio
fator de caminhão (por tipo de material) = massa total por tipo / número total de carregamentos
```

**Por dados de balança de caminhão (VIMS)**: agrupar dados de despacho por tipo de caminhão e tipo
de material e calcular a massa média.

Regras:
- Manter fatores **diferentes por tipo de caminhão E por tipo de material** onde densidade ou
  umidade variam significativamente. É boa prática da indústria.
- Variáveis que afetam: hábito de carregamento do operador, granulometria do desmonte, mudança de
  densidade entre tipos de material, estação (chuva/seca → umidade).
- Um Cat 777 com caçamba de borracha tem fator diferente de um com caçamba metálica (volumes diferentes).
- **Validar mensalmente** contra balança de correia/topografia; **calibrar anual ou semestralmente**
  passando caminhões vazios e carregados em balança rodoviária. Plotar tendência de 12 meses para
  detectar deriva (descalibração de balança, mudança de hábito de carregamento, mudança de densidade).
- Magnitude do risco: **um erro de 4% no fator de caminhão em uma operação de 100 Mt/a gera erro
  anualizado de 4 Mt.**

## Verificações obrigatórias antes de reportar qualquer número

1. Os teores foram ponderados por massa? (nunca média aritmética)
2. Os dois lados da comparação representam **o mesmo material** — mesmo polígono, mesmo período,
   mesma base de umidade, mesmo tipo de material?
3. Os blocos foram reconciliados **como foram efetivamente lavrados**, e não como foram projetados?
   (Fouet et al., 2009: controle visual durante a lavra muda os limites de tipo de material — analisar
   só o projeto de controle de teor contra o despacho pode levar à conclusão errada de que material
   foi para o destino errado, quando na verdade a estimativa original é que estava errada.)
4. A latência de pilha foi tratada? (residência > 1-2 dias exige tratamento)
5. As massas de despacho foram corrigidas por topografia?
6. Metal contido fecha? (`massa × teor` consistente com o metal reportado em cada nó)
