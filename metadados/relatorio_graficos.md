# Relatório de auditoria — gráficos e tabelas

Projeto: `projeto-pesquisa-resultados`
Material analisado: `resultados_para_analise.zip` (108 PNGs, `analises_completas.py`, `analises_completas_sem_outputs.ipynb`) e `Cópia_de_Resultados.ipynb` (com saídas).

**Status: proposta para aprovação. Nada foi movido, renomeado ou apagado.** Os arquivos originais estão intactos. Os dados e resultados estatísticos não foram alterados. A seção 8 lista as decisões que dependem de você.

---

## Como a auditoria foi feita

| Verificação | Método |
|---|---|
| Duplicatas exatas | Hash MD5 dos 108 arquivos |
| O que cada gráfico mostra | Título lido por OCR em cada imagem + leitura do código das células |
| Gráfico ↔ código | O nome `celula_NNN_saida_MM.png` indica a célula (NNN, contando de 1 no `analises_completas_sem_outputs.ipynb`) e a ordem da saída (MM). Confirmei isso comparando a contagem de saídas por célula e o título lido por OCR. |
| Versões semelhantes | Comparação linha a linha das funções de plotagem + conferência visual de pares (`pac_imunossup`, `evolucao`, painel `061`) |

**Numeração das células.** `celula_NNN` corresponde ao índice **NNN−1** (base 0) no `analises_completas_sem_outputs.ipynb`. No `Cópia_de_Resultados.ipynb` (que não tem a célula-selo do Colab), a mesma célula está no índice **NNN−2** (base 0).

**Limite desta análise.** Não tenho os dados originais (`original.csv` e os CSVs sintéticos), então não recalculei nada. Dizer que dois gráficos "mostram os mesmos dados" vem do código, que usa os mesmos DataFrames e a mesma função de frequência, mais a conferência visual de pares. Não comparei pixel a pixel gráficos de layouts diferentes.

---

## 1. Quantidade total de gráficos analisados

**108 arquivos PNG, dos quais 95 são únicos** (hashes distintos).

---

## 2. Duplicações exatas

**13 pares idênticos byte a byte**, ou seja, 13 arquivos redundantes.

| Original (mantido) | Cópia idêntica | Variável / épocas | Por que existe |
|---|---|---|---|
| `celula_019_saida_01` | `celula_026_saida_01` | nu_idade_n / 50 | A célula 026 chamou de novo a função já definida na 019 |
| `celula_019_saida_02` | `celula_026_saida_02` | nu_idade_n / 300 | idem |
| `celula_019_saida_03` | `celula_030_saida_01` | cs_sexo / 50 | idem (célula 030) |
| `celula_019_saida_04` | `celula_030_saida_02` | cs_sexo / 300 | idem |
| `celula_019_saida_11` | `celula_029_saida_01` | cs_raca / 50 | idem (célula 029) |
| `celula_019_saida_12` | `celula_029_saida_02` | cs_raca / 300 | idem |
| `celula_019_saida_17` | `celula_028_saida_01` | resultado_exa_lab / 50 | idem (célula 028) |
| `celula_019_saida_18` | `celula_028_saida_02` | resultado_exa_lab / 300 | idem |
| `celula_019_saida_19` | `celula_027_saida_01` | evolucao / 50 | idem (célula 027) |
| `celula_019_saida_20` | `celula_027_saida_02` | evolucao / 300 | idem |
| `celula_019_saida_27` | `celula_025_saida_01` | regiao / 50 | idem (célula 025) |
| `celula_019_saida_28` | `celula_025_saida_02` | regiao / 300 | idem |
| `celula_060_saida_06` | `celula_060_saida_07` | regiao (original) | **Bug no código:** `variaveis + ['regiao']`, e `regiao` já estava na lista, então a figura foi gerada duas vezes |

O mesmo bug `variaveis + ["regiao"]` aparece na célula 039, que gera as tabelas de preservação (seção 7).

---

## 3. Gráficos semelhantes (não duplicados)

O notebook tem **três gerações** da mesma comparação "original × 5 modelos sintéticos":

| Geração | Célula(s) | Layout | Títulos | Épocas | Variáveis | Imagens |
|---|---|---|---|---|---|---|
| **G1 (legada)** | 014 | 3×6, tudo numa figura | Inglês | 50+100+300 | 14, **inclui `sg_uf_not`**, sem `regiao` | 14 |
| G1 | 024 | 3×6 | Inglês | 50+100+300 | `regiao` (complemento) | 1 |
| **G2 (legada)** | 017 | 2×6 | Inglês | 50+300 | as mesmas 14 da G1 | 14 |
| **G3 (legada)** | 022 | 1×6 | Inglês | 100 | 14, sem `sg_uf_not`, **com `regiao`** | 14 |
| **G4 (atual)** | 019 | 2×3, uma figura por época | Português | 50 e 300 | 14, com `regiao`, sem `sg_uf_not` | 28 |
| G4 | 031 | 2×3 | Português | 100 | as mesmas 14 | 14 |
| Pôster | 062 | 3×2, formato pôster | Português | 50, 300 | `nu_idade_n` (50 e 300), `cs_sexo` (300) | 3 |

Ou seja, para a mesma variável e época existem de 2 a 4 versões. Veja a matriz de cobertura na seção 6.

### Diferenças de conteúdo (não só de layout) entre as gerações

Estas são as razões pelas quais **não tratei as gerações como duplicatas**:

1. **`nan` e `Ignorado` separados × fundidos.**
   - G1, G2, G3 e a célula 024 usam `.astype(str).value_counts()` e mostram `Ignorado` e `nan` como barras separadas.
   - G4 e o pôster usam `.replace("nan","Ignorado")` e juntam as duas.
   - Conferi visualmente em `evolucao` (painel Original). Na G1, `Ignorado` ≈ 14% e `nan` ≈ 20,6%, que bate com a tabela descritiva (13,68% e 20,64%). Na G4 há uma barra só de ≈ 34%.
   - O efeito aparece em **`evolucao`** e, em escala mínima, **`regiao`** (2 NA no original). Não verifiquei, variável a variável, se os modelos sintéticos também têm `nan` nas demais.
2. **Base do percentual no painel `061` (e nos gráficos 060).**
   - O painel `061` usa `value_counts(normalize=True)` sem tratar NaN, então os NaN saem do denominador. Em `evolucao`, "Cura" aparece ≈ 79% (2216 de 2814).
   - Na G4, "Cura" é 62,5% (2216 de 3546, com NaN fundido em `Ignorado`).
   - Os gráficos `060` mostram contagem absoluta, não percentual.
3. **Idade (`nu_idade_n`).** G1 a G3 não filtram a idade dos sintéticos. O pôster filtra 18–115 também nos sintéticos. Na prática os histogramas só exibem de 18 a 116, então a diferença visual é pequena. Os bins diferem por uma aresta: `range(18,116)` na G1–G3 e `np.arange(18,117)` na G4.
4. **Categoria `2` em `pac_imunossup`.** Existe só no `mappings_for_order` da G4. Visualmente não mudou os gráficos que conferi.
5. **Conferência feita:** em `pac_imunossup` / RGAN 50 épocas, G1 e G4 mostram as mesmas barras (≈ 10 / 2 / 40 / 42 / 7%). Quando não há `nan`, a diferença é só de layout.

### Gráficos que foram regerados após reorganização de layout
- G1 → G2 → G4: mesma análise, três reorganizações.
- G3 → G4 (célula 031): o painel de 100 épocas foi refeito no layout 2×3 com títulos em português.
- 062: regeração em formato pôster de três figuras que já existiam na G4 (`019_01`, `019_02`, `019_04`). Layout 3×2, e filtra a idade também nos sintéticos.
- 024 e 025: reexecuções pontuais (024 é a G1 só para `regiao`; 025 é duplicata exata da G4).

---

## 4. Gráficos selecionados para o site — **50 gráficos**

| Grupo | Arquivos | Qtd | Justificativa |
|---|---|---|---|
| Comparações 50 épocas | `celula_019_saida_*` (ímpares) | 14 | Layout padronizado, títulos em português, fontes legíveis, todas as 14 variáveis incluindo `regiao` |
| Comparações 300 épocas | `celula_019_saida_*` (pares) | 14 | idem; permite o par 50 × 300 variável a variável |
| Comparações 100 épocas | `celula_031_saida_01..14` | 14 | Mesmo layout da G4, completa o trio 50/100/300 |
| Distribuição dos dados originais | `celula_060_saida_01..06` | 6 | Distribuição por variável (idade, sexo, raça/cor, resultado, evolução, região); mostra contagem absoluta e o `nan` separado |
| Painel demográfico original | `celula_061_saida_01` | 1 | Visão resumida em % dos dados originais |
| UF de notificação | `celula_014_saida_04` | 1 | **Única** versão de `sg_uf_not` com 50, 100 e 300 épocas; ver decisão D3 |

### Tabelas selecionadas (fonte: saídas do notebook)

| Tabela | Célula (arquivo) | Estado |
|---|---|---|
| Preservação por variável, com baseline "Real" (KS, Jensen-Shannon, Cramér's V; 50/100/300) | 044 | Completa (36 linhas × 3 tabelas) |
| Utilidade (Accuracy, Precision, Recall, F1, pMSE; 15 combinações modelo × época) | 049 | Completa |
| Privacidade (Record Matching, Hold-out Distinguishing, Distance) | 053 | Completa |
| Tabela final (utilidade + privacidade) | 054 | Completa |
| Descritiva dos dados originais (frequência/percentual) | 056 | Texto, completa |
| Valores NA e Shapiro-Wilk da idade | 058–059 | Texto, completo (W = 0,6537; p < 0,001) |

---

## 5. Gráficos fora da galeria, com justificativa — **58 gráficos**

Todos permanecem na pasta de brutos. Nenhum será apagado.

| Grupo | Qtd | Arquivos | Justificativa |
|---|---|---|---|
| **Duplicatas exatas** | 13 | ver seção 2 | Idênticos aos selecionados; **decisão certa** |
| **Legados semelhantes (G1)** | 13 | `celula_014_saida_*` (exceto `_04`) | Mesmo conteúdo da G4 em layout antigo, mas **com `nan` separado de `Ignorado`**; ver D1 |
| **Legados semelhantes (G2)** | 14 | `celula_017_saida_*` | Mesma situação; a `017_04` (UF) está coberta pela `014_04` |
| **Legados semelhantes (G3)** | 14 | `celula_022_saida_*` | Painéis de 100 épocas em 1×6; substituídos pela `031` |
| **Legado 024** | 1 | `celula_024_saida_01` | `regiao` em 3×6; substituído pela `019_27/28` e `031_14` |
| **Pôster** | 3 | `celula_062_saida_01..03` | Mesmo conteúdo de `019_01`, `019_02` e `019_04`, em layout pôster; ver D4 |

**Os 45 legados e pôsteres são recomendações, não descartes definitivos**: a exclusão da galeria depende das decisões D1, D3 e D4. Só as 13 duplicatas exatas estão decididas.

---

## 6. Organização final proposta

### Cobertura das comparações (variável × época; entre parênteses, as células com versão)

| Variável | 50 | 100 | 300 |
|---|---|---|---|
| nu_idade_n | **019**, 014, 017, 062 | **031**, 014, 022 | **019**, 014, 017, 062 |
| cs_sexo | **019**, 014, 017 | **031**, 014, 022 | **019**, 014, 017, 062 |
| comp_sexual, orienta_sexual, ident_genero, ist_ativa, pac_imunossup, local_cont, transm, hiv | **019**, 014, 017 | **031**, 014, 022 | **019**, 014, 017 |
| cs_raca, resultado_exa_lab, evolucao | **019**, 014, 017 | **031**, 014, 022 | **019**, 014, 017 |
| regiao | **019**, 024 | **031**, 022, 024 | **019**, 024 |
| sg_uf_not | **014**, 017 | **014** (única) | **014**, 017 |

Em negrito: a versão proposta para a galeria. As duplicatas exatas (025–030) foram omitidas desta tabela.

### Estrutura de pastas

```
projeto-pesquisa-resultados/
├── bruto/                                  ← cópia intacta do ZIP + notebooks
│   ├── graficos_originais/                 ← os 108 PNGs com os nomes atuais
│   ├── analises_completas.py
│   ├── analises_completas_sem_outputs.ipynb
│   └── Cópia_de_Resultados.ipynb
├── selecionados/
│   ├── graficos/
│   │   ├── comparacoes/50ep/               ← 14
│   │   ├── comparacoes/100ep/              ← 14
│   │   ├── comparacoes/300ep/              ← 14
│   │   ├── comparacoes/multi-epocas-legado/← 1 (UF)
│   │   └── original/                       ← 7
│   └── tabelas/                            ← CSVs das tabelas completas (seção 7)
├── metadados/
│   ├── inventario_graficos.csv             ← 108 linhas: origem, célula, função, hash, status, nome proposto
│   └── relatorio_graficos.md
└── site/                                   ← só após aprovação (Etapa 5)
```

### Nomenclatura padronizada

| Tipo | Padrão | Exemplo |
|---|---|---|
| Comparação por época | `comparacao__{variavel}__{epocas}ep__todos-modelos.png` | `comparacao__cs_sexo__300ep__todos-modelos.png` |
| Comparação multi-época (legado) | `comparacao__{variavel}__50-100-300ep__todos-modelos__legado-en.png` | `comparacao__sg_uf_not__50-100-300ep__todos-modelos__legado-en.png` |
| Distribuição original | `original__distribuicao__{variavel}__contagem.png` | `original__distribuicao__evolucao__contagem.png` |
| Painel original | `original__painel-demografico__percentual.png` | — |
| Tabelas | `tabela__{analise}__{epocas}ep.csv` | `tabela__preservacao__300ep.csv` |

O mapeamento arquivo original → nome proposto está na coluna `nome_proposto` de `inventario_graficos.csv`.

**Limite da organização "por modelo".** Todos os gráficos de comparação mostram os cinco modelos mais o original no mesmo painel. Não existe nenhum arquivo de um modelo isolado. A navegação por modelo no site só pode ser feita **por filtro e destaque** do painel correspondente, a menos que os gráficos sejam regerados no Colab com os dados (ver D6).

### Relação entre cada gráfico e o código que o gerou

| Arquivos | Célula de definição da função | Célula que gera as saídas | Função / código |
|---|---|---|---|
| `014_saida_01..14` | 014 | 014 | `plot_variable_comparison(v)` em loop sobre `variaveis` (a lista da célula 009, com `sg_uf_not`) |
| `017_saida_01..14` | 016 | 017 | `plot_variable_comparison_filtered_epochs(v)` — versão 1 (2×6) |
| `019_saida_01..28` | 019 | 019 | A mesma função, **redefinida** (2×3, `.replace("nan","Ignorado")`); 14 variáveis × {50, 300} |
| `022_saida_01..14` | 021 | 022 | `plot_variable_comparison_100_epochs(v)` (1×6) |
| `024_saida_01` | 014 | 024 | `plot_variable_comparison('regiao')` |
| `025`–`030` (12 arquivos) | 019 | 025–030 | Chamadas individuais da versão 2: regiao, nu_idade_n, evolucao, resultado_exa_lab, cs_raca, cs_sexo |
| `031_saida_01..14` | 031 | 031 | `plot_variable_comparison_100(v)` (2×3, 100 épocas) |
| `060_saida_01..07` | — (código inline) | 060 | histograma da idade + `barplot` de frequência por variável, dados originais |
| `061_saida_01` | — (código inline) | 061 | painel 2×3 dos dados originais (em %, NaN fora do denominador) |
| `062_saida_01..03` | 062 | 062 | `plot_variable_comparison_poster(var, dfs, epocas)` |

O número da saída (`_saida_MM`) segue a ordem de `variaveis` na hora da execução. As listas diferem entre células (`sg_uf_not` só aparece até a 017; `regiao` só a partir da 019), o que confirmei lendo o título de cada imagem. O mapa completo, arquivo a arquivo, está em `inventario_graficos.csv`.

---

## 7. Tabelas: estado e problemas

| Célula | Conteúdo | Observação |
|---|---|---|
| 040, 041, 042 | Preservação 50 / 100 / 300 (KS, χ², JS, Cramér's V; 14 variáveis × 5 modelos) | **Só 10 de 75 linhas visíveis** na saída do notebook (truncada pelo pandas). Há **uma linha de `regiao` duplicada por modelo** (75 linhas em vez de 70) |
| 044 | Preservação "NOVO" (KS, JS, Cramér's V) com baseline "Real"; 6 variáveis | Completa (36 linhas × 3). Os valores coincidem com a versão antiga para os modelos que conferi |
| 045, 046 | `display` das tabelas de 50 e 300 | **Repetições idênticas** (verificado por valor) das tabelas de 044 |
| 049 | Utilidade (Accuracy, Precision, Recall, F1, pMSE) | Completa, 15 linhas |
| 050 | AUC e PR-AUC por variável | **Só 10 de 84 linhas visíveis.** 84 = 14 × 6, mas são 15 combinações modelo × época; não consegui ver qual falta |
| 053 | Privacidade | Completa, 15 linhas |
| 054 | Utilidade + privacidade | Completa, 15 × 10 |

**Consequência:** as tabelas completas de preservação (040–042) e de AUC (050) **não são recuperáveis** a partir das saídas salvas. Para colocá-las no site preciso do CSV de cada uma, o que exige reexecutar essas células no Colab (com `to_csv`). Isso não altera nenhum cálculo.

### Pontos nos resultados que merecem sua confirmação antes da publicação

Não são alterações minhas; são leituras das próprias tabelas e figuras:

- **MedGAN:** Accuracy, Precision, Recall e F1 são exatamente **0,0000 nas três épocas** (célula 049), e o Hold-out Distinguishing é 1,0000 (célula 053). O resultado exatamente zero em tudo sugere um problema de rótulos no cálculo da utilidade, e não desempenho ruim, mas isso é hipótese minha e não consegui verificar sem os dados.
- **MedGAN, `pac_imunossup`:** os gráficos mostram uma categoria **"Outro"**, que não existe no original (visível em `014_09` e `019_15`). Não verifiquei se ocorre em outras variáveis.
- **Evolução com as épocas:** o desempenho não melhora de forma monótona de 50 para 300 épocas em todos os modelos. Por exemplo, TableGAN tem KS da idade de 0,2462 (50), 0,5159 (100) e 0,8817 (300), e Accuracy de 0,78 (100) e 0,68 (300). Vale conferir se é esperado antes de montar a narrativa "50 × 300".

---

## 8. Decisões que preciso de você

| # | Decisão | Opções | Minha recomendação |
|---|---|---|---|
| **D1** | Como tratar `nan` × `Ignorado` | (a) manter só a G4, que junta os dois; (b) incluir também as versões legadas, que separam | Depende da sua intenção científica. Se `nan` (campo não preenchido) e `Ignorado` (categoria "ignorado" do sistema) são distintos, **só as versões legadas mostram isso**, e então **eu manteria a `014` completa** na galeria como alternativa. |
| **D2** | Base do percentual em `evolucao` e `regiao` | (a) rotular no site "NaN fora do denominador" no painel `061`; (b) manter só os gráficos com NaN fundido | (a), com legenda explícita, porque são informações diferentes |
| **D3** | `sg_uf_not` (UF) só existe no layout legado em inglês; para 100 épocas só na `014_04` | (a) manter `014_04` como está; (b) regerar no Colab no layout atual | (a) por ora; (b) se a UF for relevante no artigo |
| **D4** | Pôsteres `062` | (a) fora da galeria; (b) manter como seção "formato pôster" | (a), por duplicarem o conteúdo da G4 |
| **D5** | Tabelas truncadas (040–042, 050) | Reexecutar as células no Colab salvando CSV, ou omitir essas tabelas do site | Reexecutar e salvar; sem isso o site fica sem as tabelas de preservação completas |
| **D6** | Navegação "por modelo" | (a) filtro/destaque sobre o painel dos 5 modelos; (b) regerar gráficos por modelo no Colab | (a) para a primeira versão |

---

## 9. Plano da Etapa 5 (o site), a executar só após sua aprovação

- Site estático, sem backend, alimentado por um `manifest.json` gerado de `inventario_graficos.csv` e dos CSVs das tabelas.
- **Navegação:** modelo (filtro), épocas (50 / 100 / 300), variável e tipo de análise.
- **Comparação 50 × 300:** os dois painéis da mesma variável lado a lado (pares `019` ímpar/par).
- **Tabelas:** ordenáveis, com filtro por modelo e época.
- **Itens pendentes** (D1–D6) identificados com um aviso visível, até serem resolvidos.
- Nenhum valor é recalculado nem reescrito; os PNGs e tabelas entram exatamente como estão.

---

## Arquivos entregues

- `relatorio_graficos.md` — este relatório
- `inventario_graficos.csv` — 108 linhas, com a origem de cada gráfico e o status proposto

Colunas do inventário: `arquivo`, `md5`, `celula_arquivo`, `celula_idx0_notebook_sem_outputs`, `celula_definicao_funcao`, `funcao`, `layout`, `tamanho_px`, `epocas`, `variavel`, `modelos_no_grafico`, `idioma_titulo`, `tipo_analise`, `titulo_lido_por_ocr`, `identico_a`, `status_proposto`, `nome_proposto`, `pasta_proposta`.
