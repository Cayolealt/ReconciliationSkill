# Pilhas de estoque — estratégia, modelagem e reconciliação

Pilhas são o **maior impedimento prático a uma reconciliação completa** (Crawford, 2004), porque
introduzem atraso: material lavrado em um período só é processado meses ou anos depois. Mas
pilhas bem geridas **agregam valor significativo** e por isso fazem parte da cadeia de valor
(Morley & Arvidson, 2017).

## Estratégia de pilhas — definir antes de tentar reconciliar

Uma estratégia de estocagem esclarece tanto as atividades quanto **como reconciliar a movimentação
de material através das pilhas**. Boa prática: fazer isso em nível de site, cobrindo todas as pilhas
e suas inter-relações. A estratégia deve cobrir: propósito primário, eficiência e projeto,
implementação/execução.

### Os quatro propósitos (Jupp, Howard & Everett, 2013, apud Morley & Arvidson, 2017)

| Propósito | Descrição | Considerações de projeto |
|---|---|---|
| **Armazenar** (*storing*) | Material que não atende à blenda corrente; taxa de lavra maior que a capacidade da usina; estoque de emergência; estéril que se espera vir a ser econômico (pilhas de baixo teor) | Vida longa: garantir que a localização não atrapalhe expansão futura (esterilizar a área por sondagem; considerar parede final da cava e infraestrutura futura). **Criar um modelo 3D "ore control model da pilha" enquanto ela é construída** — poupa gerações futuras de adivinhar as propriedades do material retomado ou de sondar a pilha |
| **Amortecer** (*buffering*) | Solução de curto prazo para flutuações de produção ou de processo (manutenção de escavadeira, parada de britador) | Curta duração; localizar perto do britador ou manter em estado britado entre britador e usina. **Girar com frequência** |
| **Blendar por característica** | Separar material para escolher blendas específicas na alimentação do britador (ex.: separar material deletério para dosar em menor quantidade; separar material de menor dureza para blendar com alimentação direta de áreas mais duras e maximizar vazão) | Tipicamente no pátio de ROM, perto do britador. Girar com frequência |
| **Blendar para homogeneizar** | Criar pilha blendada/homogeneizada e processo de retomada para reduzir variação de teor e de outras características na alimentação | Exige disciplina de planejamento de curto prazo, controle de teor e produção. Pilhas menores e de giro rápido são melhores que uma grande com zonas desconhecidas. Idealmente: uma sendo retomada, uma concluída (buffer) e uma sendo construída |

## Regras de execução

- Manter o foco no propósito primário de cada pilha.
- **Manter pilhas pequenas e girá-las com frequência** (exceto pilhas de baixo teor / longo prazo).
  Isso reduz drasticamente os erros de arredondamento e cumulativos inerentes à soma e subtração de
  dados com as faixas de erro conhecidas.
- Saber e registrar o que entra e onde. Construir modelo 3D para pilhas de longo prazo.
- Usar modelo aritmético de retomada (LIFO ou FIFO) para pilhas de curto prazo.
- **Dado de despacho acurado é crítico** — garante que o material certo vai ao destino certo e
  permite modelar a retomada.
- Volume: coletado mensalmente (crescentemente semanal ou diário). Topografia por teodolito,
  laser scanning ou drone.
- Densidade: necessária para converter volume em massa — ver `03-formulas-e-calculos.md`.

## Modelagem de pilhas

| Método | Como funciona | Quando usar | Risco |
|---|---|---|---|
| **Média aritmética ponderada** | Assume que a média ponderada por massa de tudo que entrou representa o teor de cada tonelada que sai | Pilha construída a um tamanho projetado e **totalmente retomada dentro do período reconciliado** (ex.: pilha de homogeneização) | Erros sérios se houver variabilidade significativa de teor ou de características geometalúrgicas — assume distribuição homogênea |
| **Aritmético sequencial / genealógico (FIFO, LIFO)** | Aplica lógica que reconhece a sequência de construção da pilha e as massas ponderadas dentro dela | Pilhas de curto prazo | Melhor que média simples, mas ainda sem componente espacial |
| **Modelo espacial 3D** | "Ore control model da pilha", construído com dados de controle de teor **enquanto a pilha é construída**. Automático (pacotes de simulação, para granéis e stacker-reclaimers) ou manual (ferramentas de pacote de mineração) | Pilhas de longo prazo e pilhas críticas para blendagem | **Tentar construir o modelo 3D depois que a pilha já foi construída, por sondagem ou amostragem por concha, introduz viés significativo e representação errônea do material retomado** |

Vantagem do modelo espacial: fornece teor e informação geometalúrgica durante a retomada — tipo de
informação equivalente à que o controle de teor fornece durante a lavra.

## Ajustes de pilha

(Fouet et al., 2009.) Erros inerentes de estimativa e arredondamento na média aritmética fazem os
saldos de pilha se dessincronizarem da realidade. Prática ordinária: **levantar as pilhas
mensalmente e usar os volumes medidos para ajustar (calibrar) as massas**.

Gatilhos adicionais de ajuste:
- o cálculo reporta massa **negativa**;
- a pilha está visivelmente vazia mas o sistema ainda mostra inventário;
- levantamentos ad-hoc de pilha;
- amostragem de pilha para delinear teor.

Prática geral: ajustar as massas mensalmente com base nos volumes medidos, mas **aceitar os teores
médios da pilha**. Em pilhas de longo prazo isso pode gerar erros compostos na média ponderada de
teor. Onde pilhas muito grandes são construídas e retomadas simultaneamente, o problema é sério:
os cálculos podem reportar teores médios irrealisticamente elevados e, portanto, um inventário de
metal ou produto **que não existe**.

## Estratégias por tipo de pilha (Crawford, 2004)

- **Pilhas de britador**: normalmente pequenas; podem ser ignoradas em muitos casos, sobretudo em
  reconciliação trimestral ou mais longa. Quando ficam grandes, rastrear como inventário ou esvaziar
  no fim do ciclo contábil (geralmente mensal).
- **Pilhas de minério grosso**: idem, sobretudo se a porção ativa (acima do ponto de retomada) for
  pequena. Limpar o pátio ao final de cada período é a solução ideal.
- **Barracão de concentrado**: pode representar percentual substancial da produção mensal,
  especialmente com grandes inventários para frete marítimo. A massa disponível costuma ser
  rastreada e alguns operadores mantêm política de rotação de inventário; onde há estimativa, fazer
  esforço para limpar o barracão periodicamente, de preferência no fechamento do período.
- **Material em trânsito / aguardando fundição e refino**: funciona como outro inventário, mas os
  mecanismos de amostragem no carregamento costumam ser bons e os compradores apontam discrepâncias
  rapidamente. Correção de fundição normalmente pequena; se sistematicamente ≥1%, exigir auditoria.
- **Pilhas de longo prazo (grandes volumes de baixo teor)**: dois métodos complementares —
  (a) assumir que o valor estimado pela mina está correto e carregar os inventários, depletando
  conforme necessário (**cuidado: pilhas costumam ter menos massa do que o esperado quando finalmente
  processadas**); (b) **melhor método** — segregar as pilhas por faixa de teor e reconciliar não
  contra o teor de corte de baixo teor, mas apenas contra o material efetivamente alimentado ao
  moinho, ignorando as pilhas na reconciliação. Funciona melhor com teores de corte relativamente
  constantes ao longo do tempo; cortes variáveis exigem registro cuidadoso.
- **Rastreio por GPS**: operadores com estocagem de longo prazo estão construindo pilhas mantendo
  registro exato da localização de cada carga por GPS — permitindo previsão razoável do teor das
  pilhas por posição.

## Casos especiais

**Heap leach** (Crawford, 2004): o último ponto de estimativa confiável é o modelo de furo de
desmonte. Depois de colocado na pilha, o operador depende das determinações de teor de cada célula e
de premissas de recuperação; há defasagem considerável do início da lixiviação até o enxágue,
frequentemente 120 dias ou mais, e a produção pode continuar mesmo após interrompida a lixiviação
ativa. **Não há forma rigorosa de reconciliar heap leach** além da comparação do rendimento de ouro
ao longo do tempo contra os valores previstos.

**Subterrânea** (Crawford, 2004): pilhas menores, mas **medição acurada das dimensões dos realces é
difícil na melhor das hipóteses e perigosa na pior**. Pacotes de software modernos lidam melhor com
volumes 3D complexos, mas obter a informação do mundo real continua problemático. Fora isso, o
processo é comparável ao de operação a céu aberto. Ver também sobrelavra/sublavra em
`03-formulas-e-calculos.md` e ELOS via CMS.

**Minerais não metálicos e carvão** (Crawford, 2004): carvão é normalmente mais tolerante que minas
de metal; a reconciliação costuma ser conferida anualmente em vez de mensal ou trimestralmente.
Empresas de carvão bem geridas apresentam uma "análise de recuperação" documentando massa e qualidade
previstas contra a recuperação real.
