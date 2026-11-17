#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/caioanjos/projeto-pesquisa-resultados/blob/main/analises_completas.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# Dados originais

# In[5]:


from google.colab import drive
drive.mount('/content/drive')


# In[6]:


import os

pasta = "/content/drive/MyDrive/DadosSinteticos"

print("Pasta encontrada:", os.path.exists(pasta))

if os.path.exists(pasta):
    print("\nArquivos disponíveis:")
    for arquivo in os.listdir(pasta):
        print(arquivo)


# In[ ]:


import os
import pandas as pd
pasta = "/content/drive/MyDrive/DadosSinteticos"

print(f"Content of RGAN_50_epocas.csv (first 5 lines):\n")
with open(os.path.join(pasta, "RGAN_50_epocas.csv"), 'r', encoding='utf-8') as f:
    for _ in range(5):
        print(f.readline(), end='')

print(f"\nContent of medgan50.csv (first 5 lines):\n")
with open(os.path.join(pasta, "medgan50.csv"), 'r', encoding='utf-8') as f:
    for _ in range(5):
        print(f.readline(), end='')


# In[ ]:


get_ipython().system('ls "/content/drive/MyDrive/DadosSinteticos"')


# In[ ]:


original  = pd.read_csv(os.path.join(pasta, "original.csv"), sep=";", encoding="utf-8")

rgan50    = pd.read_csv(os.path.join(pasta, "RGAN_50_epocas.csv"), sep=",", encoding="utf-8")
rgan100   = pd.read_csv(os.path.join(pasta, "RGAN_100_epocas.csv"), sep=",", encoding="utf-8")
rgan300   = pd.read_csv(os.path.join(pasta, "RGAN_300_epocas.csv"), sep=",", encoding="utf-8")

ct50      = pd.read_csv(os.path.join(pasta, "ct50.csv"), sep=",", encoding="utf-8")
ct100     = pd.read_csv(os.path.join(pasta, "ct100.csv"), sep=",", encoding="utf-8")
ct300     = pd.read_csv(os.path.join(pasta, "ct300.csv"), sep=",", encoding="utf-8")

table50   = pd.read_csv(os.path.join(pasta, "table50.csv"), sep=";", encoding="utf-8")
table100  = pd.read_csv(os.path.join(pasta, "table100.csv"), sep=";", encoding="utf-8")
table300  = pd.read_csv(os.path.join(pasta, "table300.csv"), sep=";", encoding="utf-8")

medgan50  = pd.read_csv(os.path.join(pasta, "medgan50.csv"), sep=",", encoding="utf-8")
medgan100 = pd.read_csv(os.path.join(pasta, "medgan100.csv"), sep=",", encoding="utf-8")
medgan300 = pd.read_csv(os.path.join(pasta, "medgan300.csv"), sep=",", encoding="utf-8")

medb50    = pd.read_csv(os.path.join(pasta, "medb50.csv"), sep=",", encoding="utf-8")
medb100   = pd.read_csv(os.path.join(pasta, "medb100.csv"), sep=",", encoding="utf-8")
medb300   = pd.read_csv(os.path.join(pasta, "medb300.csv"), sep=",", encoding="utf-8")


# In[ ]:


arquivo = os.path.join(pasta, "original.csv")

with open(arquivo, "r", encoding="utf-8") as f:
    for i in range(5):
        print(f.readline())


# In[ ]:


import numpy as np
import pandas as pd
import os

pasta = "/content/drive/MyDrive/DadosSinteticos"
original  = pd.read_csv(os.path.join(pasta, "original.csv"), sep=";", encoding="utf-8")

variaveis = [
    "cs_sexo",
    "comp_sexual",
    "nu_idade_n",
    "sg_uf_not",
    "orienta_sexual",
    "ident_genero",
    "cs_raca",
    "ist_ativa",
    "pac_imunossup",
    "resultado_exa_lab",
    "evolucao",
    "local_cont",
    "transm",
    "hiv"
]


uf_code_to_name_map = (
    original.dropna(subset=['co_uf_res', 'sg_uf_not'])
    .astype({'co_uf_res': int})
    .drop_duplicates(subset=['co_uf_res'])
    .set_index('co_uf_res')['sg_uf_not']
    .to_dict()
)

def recategorize_data(df_input):

    df = df_input.copy()

    cols_to_keep = [
        "cs_sexo","comp_sexual","nu_idade_n","sg_uf_not",
        "orienta_sexual","ident_genero","cs_raca","ist_ativa",
        "pac_imunossup","resultado_exa_lab",
        "evolucao","local_cont","transm","hiv"
    ]

    available_cols = [c for c in cols_to_keep if c in df.columns]
    df = df[available_cols]

    mappings = {
        'cs_sexo': {'1': 'Masculino', '2': 'Feminino', '3': 'Intersexo', '9': 'Ignorado', '0': np.nan},
        'comp_sexual': {'1': 'RelHomens', '2': 'RelMulheres', '3': 'RelHomensMulheres', '9': 'Ignorado', '0': np.nan},
        'orienta_sexual': {'1': 'Heterossexual', '2': 'Homossexual', '3': 'Bissexual', '4': 'Outra', '7': 'Ignorado', '9': 'Ignorado', '0': np.nan},
        'ident_genero': {'1': 'MulherCis', '2': 'HomemCis', '3': 'MulherTrans', '4': 'HomemTrans', '5': 'Travesti', '6': 'NãoBinário', '7': 'Ignorado', '9': 'Ignorado', '0': np.nan},
        'cs_raca': {'1': 'Branca', '2': 'Preta', '3': 'Amarela', '4': 'Parda', '5': 'Indígena', '9': 'Ignorado', '0': np.nan},
        'ist_ativa': {'1': 'Sim', '2': 'Não', '9': 'Ignorado', '0': np.nan},
        'pac_imunossup': {'1': 'SimPorDoenca', '2': 'SimPorMedicacao', '3': 'SimCausaDesc', '4': 'Nao', '9': 'Ignorado', '0': np.nan},
        'resultado_exa_lab': {'1': 'Detectavel', '2': 'Inconclusivo', '3': 'NaoDetectavel', '4': 'Pendente', '9': 'Ignorado', '0': np.nan},
        'evolucao': {'1': 'ObitoPorMPX', '2': 'Cura', '3': 'ObitoOutraCausa', '4': 'Tratamento', '9': 'Ignorado', '0': np.nan},
        'local_cont': {'1': 'Domicilio', '2': 'Vizinhanca', '3': 'Trabalho', '4': 'Escola', '5': 'Hospital', '6': 'EventoSemContatoSexual', '7': 'EventoComContatoSexual', '8': 'Outro', '9': 'Ignorado', '0': np.nan},
        'transm': {'1': 'Animal', '2': 'DrogasIntravenosasTransfusao', '3': 'CuidadoDeSaude', '4': 'Vertical', '5': 'Laboratorio', '6': 'Sexual', '7': 'MaterialContam', '8': 'Desconhecida', '9': 'Ignorado', '0': np.nan},
        'hiv': {'1': 'Sim', '2': 'Não', '9': 'Ignorado', '0': np.nan}
    }

    for col, m in mappings.items():
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('.0', '', regex=False)
            df[col] = df[col].replace(m)

    regiao_map = {
        'AC':'Norte','AP':'Norte','AM':'Norte','PA':'Norte','RO':'Norte','RR':'Norte','TO':'Norte',
        'AL':'Nordeste','BA':'Nordeste','CE':'Nordeste','MA':'Nordeste','PB':'Nordeste','PE':'Nordeste','PI':'Nordeste','RN':'Nordeste','SE':'Nordeste',
        'DF':'Centro-Oeste','GO':'Centro-Oeste','MT':'Centro-Oeste','MS':'Centro-Oeste',
        'ES':'Sudeste','MG':'Sudeste',
        'RJ':'Sudeste','SP':'Sudeste',
        'PR':'Sul','RS':'Sul','SC':'Sul'
    }

    if 'sg_uf_not' in df.columns:
        df['sg_uf_not'] = df['sg_uf_not'].astype(str).replace('nan', np.nan)

        numeric_sg_uf_not = pd.to_numeric(df['sg_uf_not'], errors='coerce')

        if numeric_sg_uf_not.notna().any():
            df['sg_uf_not'] = numeric_sg_uf_not.map(uf_code_to_name_map).fillna(df['sg_uf_not'])

        df["regiao"] = df["sg_uf_not"].map(regiao_map)
    else:
        df["regiao"] = np.nan

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].replace('nan', np.nan)

    return df


# In[ ]:


original


# In[ ]:


arquivo = os.path.join(pasta, "original.csv")

with open(arquivo, "r", encoding="utf-8") as f:
    for i in range(5):
        print(f.readline())


# Visualização

# In[ ]:


df_names_to_process = {
    'original': original,
    'rgan50': rgan50,
    'rgan100': rgan100,
    'rgan300': rgan300,
    'ct50': ct50,
    'ct100': ct100,
    'ct300': ct300,
    'table50': table50,
    'table100': table100,
    'table300': table300,
    'medgan50': medgan50,
    'medgan100': medgan100,
    'medgan300': medgan300,
    'medb50': medb50,
    'medb100': medb100,
    'medb300': medb300
}

for name, df_obj in df_names_to_process.items():
    if 'sg_uf_not' in df_obj.columns:
        df_obj['sg_uf_not'] = df_obj['sg_uf_not'].astype(str).str.replace('.0', '', regex=False)

    for col in variaveis:
        if col not in df_obj.columns:
            df_obj[col] = np.nan
    globals()[name] = recategorize_data(df_obj)


# In[ ]:


import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns
import itertools

cores = {
    "Original": "black",
    "RGAN": "red",
    "CTGAN": "green",
    "TableGAN": "gold",
    "MedGAN": "hotpink",
    "MedBGAN": "purple"
}

mappings_for_order = {
    'cs_sexo': ['Masculino', 'Feminino', 'Intersexo', 'Ignorado'],
    'comp_sexual': ['RelHomens', 'RelMulheres', 'RelHomensMulheres', 'Ignorado'],
    'orienta_sexual': ['Heterossexual', 'Homossexual', 'Bissexual', 'Outra', 'Ignorado'],
    'ident_genero': ['MulherCis', 'HomemCis', 'MulherTrans', 'HomemTrans', 'Travesti', 'NãoBinário', 'Ignorado'],
    'cs_raca': ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena', 'Ignorado'],
    'ist_ativa': ['Sim', 'Não', 'Ignorado'],
    'pac_imunossup': ['SimPorDoenca', 'SimPorMedicacao', 'SimCausaDesc', 'Nao', 'Ignorado'],
    'resultado_exa_lab': ['Detectavel', 'Inconclusivo', 'NaoDetectavel', 'Pendente', 'Ignorado'],
    'evolucao': ['ObitoPorMPX', 'Cura', 'ObitoOutraCausa', 'Tratamento', 'Ignorado'],
    'local_cont': ['Domicilio', 'Vizinhanca', 'Trabalho', 'Escola', 'Hospital', 'EventoSemContatoSexual', 'EventoComContatoSexual', 'Outro', 'Ignorado'],
    'transm': ['Animal', 'DrogasIntravenosasTransfusao', 'CuidadoDeSaude', 'Vertical', 'Laboratorio', 'Sexual', 'MaterialContam', 'Desconhecida', 'Ignorado'],
    'hiv': ['Sim', 'Não', 'Ignorado']
}

regiao_order = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

for col_name, order_list in mappings_for_order.items():
    if 'Ignorado' in order_list or any(val == 'nan' for val in order_list):
        if 'nan' not in order_list:
            mappings_for_order[col_name].append('nan')
    else:
        mappings_for_order[col_name].append('nan')

regiao_order.append('nan')
mappings_for_order['regiao'] = regiao_order


def plot_variable_comparison(variable_name):
    fig, axs = plt.subplots(3, 6, figsize=(30, 15), sharey=False)
    fig.suptitle(f"Comparison for {variable_name}", fontsize=20, fontweight="bold", y=1.02)

    epoch_groups = {
        "50 épocas": [rgan50, ct50, table50, medgan50, medb50],
        "100 épocas": [rgan100, ct100, table100, medgan100, medb100],
        "300 épocas": [rgan300, ct300, table300, medgan300, medb300]
    }

    gan_names = ["RGAN", "CTGAN", "TableGAN", "MedGAN", "MedBGAN"]

    for i, (epoch_label, gan_dfs) in enumerate(epoch_groups.items()):
        current_dfs = [original] + gan_dfs
        current_names = ["Original"] + gan_names

        for j, (df_to_plot, model_name) in enumerate(zip(current_dfs, current_names)):
            ax = axs[i, j]
            ax.set_title(f"{model_name} ({epoch_label if model_name != 'Original' else ''})")

            if model_name == 'Original':
                df_to_plot = recategorize_data(df_to_plot.copy())

                df_to_plot = df_to_plot[
                    (df_to_plot['nu_idade_n'] >= 18) &
                    (df_to_plot['nu_idade_n'] <= 115)
                ].copy()


            if variable_name == 'nu_idade_n':
                numeric_age = pd.to_numeric(df_to_plot[variable_name], errors='coerce').dropna()
                bins = range(18, 116, 1)
                decade_ticks = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
                decade_labels = ['20', '30', '40', '50', '60', '70', '80', '90', '100', '110']

                sns.histplot(x=numeric_age, ax=ax, bins=bins, kde=False, color=cores[model_name])

                ax.set_xticks(decade_ticks)
                ax.set_xticklabels(decade_labels, rotation=45, ha='right')
                ax.set_ylabel("Contagem")
                ax.set_xlabel("Idade")

            else:
                if variable_name not in df_to_plot.columns:
                    ax.text(0.5, 0.5, 'Data Missing', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                    ax.set_xticks([])
                    ax.set_yticks([])
                    continue

                freq = (
                    df_to_plot[variable_name]
                    .astype(str)
                    .value_counts(normalize=True)
                    .mul(100)
                )

                order_list = None
                if variable_name in mappings_for_order:
                    order_list = [cat for cat in mappings_for_order[variable_name] if cat in freq.index.tolist()]
                    for cat_in_data in freq.index.tolist():
                        if cat_in_data not in order_list:
                            order_list.append(cat_in_data)
                else:
                    order_list = sorted(freq.index.tolist())
                    if 'nan' in order_list:
                        order_list.remove('nan')
                        order_list.append('nan')

                if order_list is not None:
                    freq = freq.reindex(order_list, fill_value=0)

                sns.barplot(
                    x=freq.index,
                    y=freq.values,
                    ax=ax,
                    order=order_list,
                    color=cores[model_name]
                )

                ax.tick_params(axis="x", rotation=45, labelsize=8)
                ax.tick_params(axis="y", labelsize=8)

                ax.set_ylim(0, 100)
                ax.set_yticks([0, 20, 40, 60, 80, 100])
                ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
                ax.yaxis.set_major_formatter(PercentFormatter())

    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.show()

for variable in variaveis:
    plot_variable_comparison(variable)


# Apenas 50 e 300 Épocas

# In[ ]:


def plot_variable_comparison_filtered_epochs(variable_name):
    fig, axs = plt.subplots(2, 6, figsize=(30, 10), sharey=False) # 2 rows for 50 and 300 epoch groups
    fig.suptitle(f"Comparison for {variable_name} (50 and 300 Epochs)", fontsize=20, fontweight="bold", y=1.02)

    filtered_epoch_groups = {
        "50 épocas": [rgan50, ct50, table50, medgan50, medb50],
        "300 épocas": [rgan300, ct300, table300, medgan300, medb300]
    }

    gan_names = ["RGAN", "CTGAN", "TableGAN", "MedGAN", "MedBGAN"]

    row_idx = 0
    for epoch_label, gan_dfs in filtered_epoch_groups.items():
        current_dfs = [original] + gan_dfs
        current_names = ["Original"] + gan_names

        for j, (df_to_plot, model_name) in enumerate(zip(current_dfs, current_names)):
            ax = axs[row_idx, j]
            ax.set_title(f"{model_name} ({epoch_label if model_name != 'Original' else ''})")

            # Apply preprocessing to 'original' data within the plotting function
            if model_name == 'Original':
                df_to_plot = recategorize_data(df_to_plot.copy())

                df_to_plot = df_to_plot[
                    (df_to_plot['nu_idade_n'] >= 18) &
                    (df_to_plot['nu_idade_n'] <= 115)
                ].copy()


            if variable_name == 'nu_idade_n':
                numeric_age = pd.to_numeric(df_to_plot[variable_name], errors='coerce').dropna()
                bins = range(18, 116, 1)
                decade_ticks = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
                decade_labels = ['20', '30', '40', '50', '60', '70', '80', '90', '100', '110']

                sns.histplot(x=numeric_age, ax=ax, bins=bins, kde=False, color=cores[model_name])

                ax.set_xticks(decade_ticks)
                ax.set_xticklabels(decade_labels, rotation=45, ha='right')
                ax.set_ylabel("Contagem")
                ax.set_xlabel("Idade")

            else:
                if variable_name not in df_to_plot.columns:
                    ax.text(0.5, 0.5, 'Data Missing', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                    ax.set_xticks([])
                    ax.set_yticks([])
                    continue

                freq = (
                    df_to_plot[variable_name]
                    .astype(str)
                    .value_counts(normalize=True)
                    .mul(100)
                )

                order_list = None
                if variable_name in mappings_for_order:
                    order_list = [cat for cat in mappings_for_order[variable_name] if cat in freq.index.tolist()]
                    for cat_in_data in freq.index.tolist():
                        if cat_in_data not in order_list:
                            order_list.append(cat_in_data)
                else:
                    order_list = sorted(freq.index.tolist())
                    if 'nan' in order_list:
                        order_list.remove('nan')
                        order_list.append('nan')

                if order_list is not None:
                    freq = freq.reindex(order_list, fill_value=0)

                sns.barplot(
                    x=freq.index,
                    y=freq.values,
                    ax=ax,
                    order=order_list,
                    color=cores[model_name]
                )

                ax.tick_params(axis="x", rotation=45, labelsize=8)
                ax.tick_params(axis="y", labelsize=8)

                # Fixed y-axis for categorical plots
                ax.set_ylim(0, 100)
                ax.set_yticks([0, 20, 40, 60, 80, 100])
                ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
                ax.yaxis.set_major_formatter(PercentFormatter())
        row_idx += 1

    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.show()


# In[ ]:


for variable in variaveis:
    plot_variable_comparison_filtered_epochs(variable)


# ###Refazendo a visualização

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

cores = {
    "Original": "black",
    "RGAN": "red",
    "CTGAN": "green",
    "TableGAN": "gold",
    "MedGAN": "hotpink",
    "MedBGAN": "purple"
}

mappings_for_order = {
    'cs_sexo': ['Masculino', 'Feminino', 'Intersexo', 'Ignorado'],
    'comp_sexual': ['RelHomens', 'RelMulheres', 'RelHomensMulheres', 'Ignorado'],
    'orienta_sexual': ['Heterossexual', 'Homossexual', 'Bissexual', 'Outra', 'Ignorado'],
    'ident_genero': ['MulherCis', 'HomemCis', 'MulherTrans', 'HomemTrans', 'Travesti', 'NãoBinário', 'Ignorado'],
    'cs_raca': ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena', 'Ignorado'],
    'ist_ativa': ['Sim', 'Não', 'Ignorado'],
    'pac_imunossup': ['SimPorDoenca', '2', 'SimPorMedicacao', 'SimCausaDesc', 'Nao', 'Ignorado'],
    'resultado_exa_lab': ['Detectavel', 'Inconclusivo', 'NaoDetectavel', 'Pendente', 'Ignorado'],
    'evolucao': ['ObitoPorMPX', 'Cura', 'ObitoOutraCausa', 'Tratamento', 'Ignorado'],
    'local_cont': ['Domicilio', 'Vizinhanca', 'Trabalho', 'Escola', 'Hospital', 'EventoSemContatoSexual', 'EventoComContatoSexual', 'Outro', 'Ignorado'],
    'transm': ['Animal', 'DrogasIntravenosasTransfusao', 'CuidadoDeSaude', 'Vertical', 'Laboratorio', 'Sexual', 'MaterialContam', 'Desconhecida', 'Ignorado'],
    'hiv': ['Sim', 'Não', 'Ignorado']
}

regiao_order = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

for col_name, order_list in mappings_for_order.items():
    if 'Ignorado' in order_list or any(val == 'nan' for val in order_list):
        if 'nan' not in order_list:
            mappings_for_order[col_name].append('nan')
    else:
        mappings_for_order[col_name].append('nan')

regiao_order.append('nan')
mappings_for_order['regiao'] = regiao_order

def plot_variable_comparison_filtered_epochs(variable_name):
    epoch_groups = {
        "50 épocas": [
            original,
            rgan50,
            ct50,
            table50,
            medgan50,
            medb50
        ],

        "300 épocas": [
            original,
            rgan300,
            ct300,
            table300,
            medgan300,
            medb300
        ]
    }

    model_names = [
        "Original",
        "RGAN",
        "CTGAN",
        "TableGAN",
        "MedGAN",
        "MedBGAN"
    ]

    original_plot = recategorize_data(original.copy())

    if "nu_idade_n" in original_plot.columns:

        original_plot["nu_idade_n"] = pd.to_numeric(
            original_plot["nu_idade_n"],
            errors="coerce"
        )

        original_plot = original_plot[
            (original_plot["nu_idade_n"] >= 18) &
            (original_plot["nu_idade_n"] <= 115)
        ].copy()

    for epoch_label, dfs in epoch_groups.items():

        fig, axs = plt.subplots(
            2,
            3,
            figsize=(20, 12),
            sharey=False
        )

        fig.suptitle(
            f"Comparação da variável: {variable_name} ({epoch_label})",
            fontsize=22,
            fontweight="bold",
            y=0.995
        )

        current_dfs = [
            original_plot if i == 0 else dfs[i]
            for i in range(6)
        ]

        for j, (df_to_plot, model_name) in enumerate(
            zip(current_dfs, model_names)
        ):
            local_row = j // 3
            local_col = j % 3

            ax = axs[local_row, local_col]

            if model_name == "Original":

                ax.set_title(
                    "Original",
                    fontsize=20,
                    fontweight="bold"
                )

            else:

                ax.set_title(
                    model_name,
                    fontsize=20,
                    fontweight="bold"
                )

            if variable_name == "nu_idade_n":

                if variable_name not in df_to_plot.columns:

                    ax.text(
                        0.5,
                        0.5,
                        "Dados não disponíveis",
                        ha="center",
                        va="center",
                        transform=ax.transAxes
                    )

                    ax.set_axis_off()

                    continue


                numeric_age = pd.to_numeric(
                    df_to_plot[variable_name],
                    errors="coerce"
                ).dropna()


                bins = np.arange(18, 117, 1)


                sns.histplot(
                    x=numeric_age,
                    ax=ax,
                    bins=bins,
                    kde=False,
                    color=cores[model_name]
                )


                ax.set_xticks([
                    20, 30, 40, 50, 60,
                    70, 80, 90, 100, 110
                ])


                ax.set_xticklabels([
                    "20", "30", "40", "50", "60",
                    "70", "80", "90", "100", "110"
                ])


                ax.set_xlabel("Idade")
                ax.set_ylabel("Contagem")

            else:

                if variable_name not in df_to_plot.columns:

                    ax.text(
                        0.5,
                        0.5,
                        "Dados não disponíveis",
                        ha="center",
                        va="center",
                        transform=ax.transAxes
                    )

                    ax.set_axis_off()

                    continue

                freq = (
                    df_to_plot[variable_name]
                    .astype(str)
                    .replace("nan", "Ignorado")
                    .value_counts(normalize=True)
                    .mul(100)
                )

                if variable_name in mappings_for_order:

                    order_list = [
                        cat
                        for cat in mappings_for_order[variable_name]
                        if cat in freq.index
                    ]

                    for cat in freq.index:

                        if cat not in order_list:
                            order_list.append(cat)

                else:

                    order_list = sorted(freq.index.tolist())

                freq = freq.reindex(
                    order_list,
                    fill_value=0
                )

                sns.barplot(
                    x=freq.index,
                    y=freq.values,
                    ax=ax,
                    order=order_list,
                    color=cores[model_name]
                )

                ax.set_xlabel("")

                ax.set_ylabel("Percentual")

                ax.set_ylim(0, 100)

                ax.set_yticks([
                    0, 20, 40, 60, 80, 100
                ])

                ax.yaxis.set_major_formatter(
                    PercentFormatter()
                )


                ax.tick_params(
                    axis="x",
                    rotation=45,
                    labelsize=12
                )

                ax.tick_params(
                    axis="y",
                    labelsize=12
                )

        plt.tight_layout(
            rect=[0, 0, 1, 0.97],
            h_pad=4
        )

        plt.show()

variaveis = [
    "nu_idade_n",
    "cs_sexo",
    "comp_sexual",
    "orienta_sexual",
    "ident_genero",
    "cs_raca",
    "ist_ativa",
    "pac_imunossup",
    "resultado_exa_lab",
    "evolucao",
    "local_cont",
    "transm",
    "hiv",
    "regiao"
]

for variavel in variaveis:
    plot_variable_comparison_filtered_epochs(variavel)


# ### Apenas 100 Épocas

# In[ ]:


def plot_variable_comparison_100_epochs(variable_name):
    fig, axs = plt.subplots(1, 6, figsize=(30, 5), sharey=False)
    fig.suptitle(f"Comparison for {variable_name} (100 Epochs)", fontsize=20, fontweight="bold", y=1.02)

    filtered_epoch_groups = {
        "100 épocas": [rgan100, ct100, table100, medgan100, medb100],
    }

    gan_names = ["RGAN", "CTGAN", "TableGAN", "MedGAN", "MedBGAN"]

    epoch_label = "100 épocas"
    gan_dfs = filtered_epoch_groups[epoch_label]

    current_dfs = [original] + gan_dfs
    current_names = ["Original"] + gan_names

    for j, (df_to_plot, model_name) in enumerate(zip(current_dfs, current_names)):
        ax = axs[j] # Usa j diretamente para as colunas em uma única linha
        ax.set_title(f"{model_name} ({epoch_label if model_name != 'Original' else ''})")

        if model_name == 'Original':
            df_to_plot = recategorize_data(df_to_plot.copy())

            df_to_plot = df_to_plot[
                (df_to_plot['nu_idade_n'] >= 18) &
                (df_to_plot['nu_idade_n'] <= 115)
            ].copy()


        if variable_name == 'nu_idade_n':
            numeric_age = pd.to_numeric(df_to_plot[variable_name], errors='coerce').dropna()
            bins = range(18, 116, 1)
            decade_ticks = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
            decade_labels = ['20', '30', '40', '50', '60', '70', '80', '90', '100', '110']

            sns.histplot(x=numeric_age, ax=ax, bins=bins, kde=False, color=cores[model_name])

            ax.set_xticks(decade_ticks)
            ax.set_xticklabels(decade_labels, rotation=45, ha='right')
            ax.set_ylabel("Contagem")
            ax.set_xlabel("Idade")

        else:
            if variable_name not in df_to_plot.columns:
                ax.text(0.5, 0.5, 'Data Missing', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])
                continue

            freq = (
                df_to_plot[variable_name]
                .astype(str)
                .value_counts(normalize=True)
                .mul(100)
            )

            order_list = None
            if variable_name in mappings_for_order:
                order_list = [cat for cat in mappings_for_order[variable_name] if cat in freq.index.tolist()]
                for cat_in_data in freq.index.tolist():
                    if cat_in_data not in order_list:
                        order_list.append(cat_in_data)
            else:
                order_list = sorted(freq.index.tolist())
                if 'nan' in order_list:
                    order_list.remove('nan')
                    order_list.append('nan')

            if order_list is not None:
                freq = freq.reindex(order_list, fill_value=0)

            sns.barplot(
                x=freq.index,
                y=freq.values,
                ax=ax,
                order=order_list,
                color=cores[model_name]
            )

            ax.tick_params(axis="x", rotation=45, labelsize=8)
            ax.tick_params(axis="y", labelsize=8)

            ax.set_ylim(0, 100)
            ax.set_yticks([0, 20, 40, 60, 80, 100])
            ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
            ax.yaxis.set_major_formatter(PercentFormatter())

    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.show()


# In[ ]:


for variable in variaveis:
    plot_variable_comparison_100_epochs(variable)


# In[ ]:


# regiao
if 'regiao' not in variaveis:
    variaveis.append('regiao')
print(f"Lista de variáveis atualizada: {variaveis}")


# In[ ]:


plot_variable_comparison('regiao')


# In[ ]:


plot_variable_comparison_filtered_epochs('regiao')


# In[ ]:


plot_variable_comparison_filtered_epochs('nu_idade_n')


# In[ ]:


plot_variable_comparison_filtered_epochs('evolucao')


# In[ ]:


plot_variable_comparison_filtered_epochs('resultado_exa_lab')


# In[ ]:


plot_variable_comparison_filtered_epochs('cs_raca')


# In[ ]:


plot_variable_comparison_filtered_epochs('cs_sexo')


# In[ ]:


def plot_variable_comparison_100(variable_name):
    dfs = [
        original,
        rgan100,
        ct100,
        table100,
        medgan100,
        medb100
    ]

    model_names = [
        "Original",
        "RGAN",
        "CTGAN",
        "TableGAN",
        "MedGAN",
        "MedBGAN"
    ]

    original_plot = recategorize_data(original.copy())

    if "nu_idade_n" in original_plot.columns:

        original_plot["nu_idade_n"] = pd.to_numeric(
            original_plot["nu_idade_n"],
            errors="coerce"
        )

        original_plot = original_plot[
            (original_plot["nu_idade_n"] >= 18) &
            (original_plot["nu_idade_n"] <= 115)
        ].copy()

    fig, axs = plt.subplots(
        2,
        3,
        figsize=(20, 12),
        sharey=False
    )

    fig.suptitle(
        f"Comparação da variável: {variable_name} (100 épocas)",
        fontsize=22,
        fontweight="bold",
        y=0.995
    )

    current_dfs = [
        original_plot if i == 0 else dfs[i]
        for i in range(6)
    ]

    for j, (df_to_plot, model_name) in enumerate(
        zip(current_dfs, model_names)
    ):

        local_row = j // 3
        local_col = j % 3

        ax = axs[local_row, local_col]

        ax.set_title(
            model_name,
            fontsize=20,
            fontweight="bold"
        )

        if variable_name == "nu_idade_n":

            if variable_name not in df_to_plot.columns:

                ax.text(
                    0.5,
                    0.5,
                    "Dados não disponíveis",
                    ha="center",
                    va="center",
                    transform=ax.transAxes
                )

                ax.set_axis_off()
                continue

            numeric_age = pd.to_numeric(
                df_to_plot[variable_name],
                errors="coerce"
            ).dropna()

            bins = np.arange(18, 117, 1)

            sns.histplot(
                x=numeric_age,
                ax=ax,
                bins=bins,
                kde=False,
                color=cores[model_name]
            )

            ax.set_xticks([
                20, 30, 40, 50,
                60, 70, 80, 90,
                100, 110
            ])

            ax.set_xticklabels([
                "20", "30", "40", "50", "60",
                "70", "80", "90", "100", "110"
            ])

            ax.set_xlabel("Idade")
            ax.set_ylabel("Contagem")

        else:

            if variable_name not in df_to_plot.columns:

                ax.text(
                    0.5,
                    0.5,
                    "Dados não disponíveis",
                    ha="center",
                    va="center",
                    transform=ax.transAxes
                )

                ax.set_axis_off()
                continue

            freq = (
                df_to_plot[variable_name]
                .astype(str)
                .replace("nan", "Ignorado")
                .value_counts(normalize=True)
                .mul(100)
            )

            if variable_name in mappings_for_order:

                order_list = [
                    cat
                    for cat in mappings_for_order[variable_name]
                    if cat in freq.index
                ]

                for cat in freq.index:

                    if cat not in order_list:
                        order_list.append(cat)

            else:

                order_list = sorted(
                    freq.index.tolist()
                )

            freq = freq.reindex(
                order_list,
                fill_value=0
            )

            sns.barplot(
                x=freq.index,
                y=freq.values,
                ax=ax,
                order=order_list,
                color=cores[model_name]
            )

            ax.set_xlabel("")
            ax.set_ylabel("Percentual")

            ax.set_ylim(0, 100)

            ax.set_yticks([
                0, 20, 40, 60, 80, 100
            ])

            ax.yaxis.set_major_formatter(
                PercentFormatter()
            )

            ax.tick_params(
                axis="x",
                rotation=45,
                labelsize=12
            )

            ax.tick_params(
                axis="y",
                labelsize=9
            )

    plt.tight_layout(
        rect=[0, 0, 1, 0.97],
        h_pad=4
    )

    plt.show()

variaveis = [
    "nu_idade_n",
    "cs_sexo",
    "comp_sexual",
    "orienta_sexual",
    "ident_genero",
    "cs_raca",
    "ist_ativa",
    "pac_imunossup",
    "resultado_exa_lab",
    "evolucao",
    "local_cont",
    "transm",
    "hiv",
    "regiao"
]

for variavel in variaveis:
    plot_variable_comparison_100(variavel)


# In[ ]:


print(rgan100["sg_uf_not"].head())
print(rgan100["sg_uf_not"].unique())


# Cálculo das métricas

# In[ ]:


from scipy.stats import ks_2samp, chi2_contingency
from scipy.spatial.distance import jensenshannon
from scipy.spatial.distance import cdist
from scipy.stats.contingency import association

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

import warnings
warnings.filterwarnings("ignore")


# In[ ]:


from scipy.stats import ks_2samp
help(ks_2samp)


# In[ ]:


get_ipython().run_line_magic('pinfo2', 'ks_2samp')


# In[ ]:


original = recategorize_data(original)

datasets = {
    "RGAN50": recategorize_data(rgan50),
    "RGAN100": recategorize_data(rgan100),
    "RGAN300": recategorize_data(rgan300),

    "CTGAN50": recategorize_data(ct50),
    "CTGAN100": recategorize_data(ct100),
    "CTGAN300": recategorize_data(ct300),

    "TableGAN50": recategorize_data(table50),
    "TableGAN100": recategorize_data(table100),
    "TableGAN300": recategorize_data(table300),

    "MedGAN50": recategorize_data(medgan50),
    "MedGAN100": recategorize_data(medgan100),
    "MedGAN300": recategorize_data(medgan300),

    "MedBGAN50": recategorize_data(medb50),
    "MedBGAN100": recategorize_data(medb100),
    "MedBGAN300": recategorize_data(medb300),
}


# Preservação

# In[ ]:


from scipy.stats import ks_2samp, chi2_contingency
from scipy.stats.contingency import association
from scipy.spatial.distance import jensenshannon

grupos = {
    "50 épocas": {
        "RGAN": datasets["RGAN50"],
        "CTGAN": datasets["CTGAN50"],
        "TableGAN": datasets["TableGAN50"],
        "MedGAN": datasets["MedGAN50"],
        "MedBGAN": datasets["MedBGAN50"],
    },

    "100 épocas": {
        "RGAN": datasets["RGAN100"],
        "CTGAN": datasets["CTGAN100"],
        "TableGAN": datasets["TableGAN100"],
        "MedGAN": datasets["MedGAN100"],
        "MedBGAN": datasets["MedBGAN100"],
    },

    "300 épocas": {
        "RGAN": datasets["RGAN300"],
        "CTGAN": datasets["CTGAN300"],
        "TableGAN": datasets["TableGAN300"],
        "MedGAN": datasets["MedGAN300"],
        "MedBGAN": datasets["MedBGAN300"],
    }
}

tabelas = {}

for epoca, modelos in grupos.items():

    resultados = []

    for modelo, sintetico in modelos.items():

        for coluna in variaveis + ["regiao"]:

            if coluna not in sintetico.columns:
                continue

            # Variável numérica
            if coluna == "nu_idade_n":

                real = pd.to_numeric(original[coluna], errors="coerce").dropna()
                fake = pd.to_numeric(sintetico[coluna], errors="coerce").dropna()

                ks = ks_2samp(real, fake).statistic

                bins = np.arange(18,117)

                h_real,_ = np.histogram(real,bins=bins,density=True)
                h_fake,_ = np.histogram(fake,bins=bins,density=True)

                h_real += 1e-10
                h_fake += 1e-10

                js = jensenshannon(h_real,h_fake)**2

                resultados.append({
                    "Modelo": modelo,
                    "Variável": coluna,
                    "KS": ks,
                    "Qui-quadrado": np.nan,
                    "Jensen-Shannon": js,
                    "Cramer's V": np.nan
                })

            # Variáveis categóricas
            else:

                real = original[coluna].fillna("NA")
                fake = sintetico[coluna].fillna("NA")

                categorias = sorted(
                    set(real.unique()).union(set(fake.unique()))
                )

                freq_real = real.value_counts().reindex(categorias, fill_value=0)
                freq_fake = fake.value_counts().reindex(categorias, fill_value=0)

                tabela = np.vstack([freq_real, freq_fake])

                chi2,_,_,_ = chi2_contingency(tabela)

                p_real = freq_real/freq_real.sum()
                p_fake = freq_fake/freq_fake.sum()

                js = jensenshannon(p_real,p_fake)**2

                cramerv = association(tabela, method="cramer")

                resultados.append({
                    "Modelo": modelo,
                    "Variável": coluna,
                    "KS": np.nan,
                    "Qui-quadrado": chi2,
                    "Jensen-Shannon": js,
                    "Cramer's V": cramerv
                })

    tabelas[epoca] = pd.DataFrame(resultados).round(4)


# In[ ]:


display(tabelas["50 épocas"])


# In[ ]:


display(tabelas["100 épocas"])


# In[ ]:


display(tabelas["300 épocas"])


# ##NOVO

# In[ ]:


import pandas as pd
import numpy as np

from scipy.stats import ks_2samp
from scipy.stats.contingency import association
from scipy.spatial.distance import jensenshannon

from sklearn.model_selection import train_test_split


# ============================================================
# 1. VARIÁVEIS UTILIZADAS
# ============================================================

variaveis = [
    "nu_idade_n",
    "cs_sexo",
    "cs_raca",
    "resultado_exa_lab",
    "evolucao",
    "regiao"
]


# ============================================================
# 2. SEPARAÇÃO DOS DADOS REAIS PARA O BASELINE
# ============================================================

real_1, real_2 = train_test_split(
    original,
    test_size=0.50,
    random_state=42
)


# ============================================================
# 3. CÁLCULO DAS MÉTRICAS DE DISTRIBUIÇÃO
# ============================================================

def calcular_metricas_distribuicao(real_df, sintetico_df):

    resultados = []

    for coluna in variaveis:

        # Verifica se a variável existe nos dois conjuntos
        if coluna not in real_df.columns or coluna not in sintetico_df.columns:
            continue


        # ----------------------------------------------------
        # VARIÁVEL NUMÉRICA: IDADE
        # ----------------------------------------------------

        if coluna == "nu_idade_n":

            real_col = pd.to_numeric(
                real_df[coluna],
                errors="coerce"
            ).dropna()

            fake_col = pd.to_numeric(
                sintetico_df[coluna],
                errors="coerce"
            ).dropna()


            # KS
            ks = ks_2samp(
                real_col,
                fake_col
            ).statistic


            # Jensen-Shannon
            bins = np.arange(18, 117)

            h_real, _ = np.histogram(
                real_col,
                bins=bins
            )

            h_fake, _ = np.histogram(
                fake_col,
                bins=bins
            )

            # Evita divisão por zero
            h_real = h_real.astype(float) + 1e-10
            h_fake = h_fake.astype(float) + 1e-10

            # Transformação em distribuição de probabilidade
            p_real = h_real / h_real.sum()
            p_fake = h_fake / h_fake.sum()

            js = jensenshannon(
                p_real,
                p_fake
            ) ** 2


            resultados.append({
                "Variável": coluna,
                "KS": ks,
                "Jensen-Shannon": js,
                "Cramer's V": np.nan
            })


        # ----------------------------------------------------
        # VARIÁVEIS CATEGÓRICAS
        # ----------------------------------------------------

        else:

            real_col = (
                real_df[coluna]
                .fillna("NA")
                .astype(str)
            )

            fake_col = (
                sintetico_df[coluna]
                .fillna("NA")
                .astype(str)
            )


            # Todas as categorias existentes nos dois conjuntos
            categorias = sorted(
                set(real_col.unique()).union(
                    set(fake_col.unique())
                )
            )


            # Frequências
            freq_real = (
                real_col
                .value_counts()
                .reindex(
                    categorias,
                    fill_value=0
                )
            )

            freq_fake = (
                fake_col
                .value_counts()
                .reindex(
                    categorias,
                    fill_value=0
                )
            )


            # ------------------------------------------------
            # Jensen-Shannon
            # ------------------------------------------------

            p_real = (
                freq_real /
                freq_real.sum()
            )

            p_fake = (
                freq_fake /
                freq_fake.sum()
            )

            js = jensenshannon(
                p_real,
                p_fake
            ) ** 2


            # ------------------------------------------------
            # V de Cramér
            # ------------------------------------------------

            tabela = np.vstack([
                freq_real.values,
                freq_fake.values
            ])

            cramerv = association(
                tabela,
                method="cramer"
            )


            resultados.append({
                "Variável": coluna,
                "KS": np.nan,
                "Jensen-Shannon": js,
                "Cramer's V": cramerv
            })


    return pd.DataFrame(resultados)


# ============================================================
# 4. MODELOS POR ÉPOCA
# ============================================================

grupos = {

    "50 épocas": {
        "RGAN": datasets["RGAN50"],
        "CTGAN": datasets["CTGAN50"],
        "TableGAN": datasets["TableGAN50"],
        "MedGAN": datasets["MedGAN50"],
        "MedBGAN": datasets["MedBGAN50"]
    },

    "100 épocas": {
        "RGAN": datasets["RGAN100"],
        "CTGAN": datasets["CTGAN100"],
        "TableGAN": datasets["TableGAN100"],
        "MedGAN": datasets["MedGAN100"],
        "MedBGAN": datasets["MedBGAN100"]
    },

    "300 épocas": {
        "RGAN": datasets["RGAN300"],
        "CTGAN": datasets["CTGAN300"],
        "TableGAN": datasets["TableGAN300"],
        "MedGAN": datasets["MedGAN300"],
        "MedBGAN": datasets["MedBGAN300"]
    }
}


# ============================================================
# 5. CÁLCULO DAS MÉTRICAS
# ============================================================

tabelas = {}


for epoca, modelos in grupos.items():

    resultados = []


    # --------------------------------------------------------
    # REAL VS. REAL
    # --------------------------------------------------------

    baseline = calcular_metricas_distribuicao(
        real_1,
        real_2
    )

    baseline["Modelo"] = "Real"

    resultados.append(
        baseline
    )


    # --------------------------------------------------------
    # REAL VS. SINTÉTICO
    # --------------------------------------------------------

    for modelo, sintetico in modelos.items():

        metricas = calcular_metricas_distribuicao(
            original,
            sintetico
        )

        metricas["Modelo"] = modelo

        resultados.append(
            metricas
        )


    # --------------------------------------------------------
    # TABELA FINAL
    # --------------------------------------------------------

    tabela_final = pd.concat(
        resultados,
        ignore_index=True
    )


    tabela_final = tabela_final[
        [
            "Modelo",
            "Variável",
            "KS",
            "Jensen-Shannon",
            "Cramer's V"
        ]
    ]


    tabelas[epoca] = tabela_final.round(4)


# ============================================================
# 6. EXIBIÇÃO DAS TABELAS
# ============================================================

for epoca, tabela in tabelas.items():

    print("\n" + "=" * 70)
    print(epoca)
    print("=" * 70)

    display(tabela)


# In[ ]:


display(tabelas["50 épocas"])


# In[ ]:


display(tabelas["300 épocas"])


# Utilidade

# In[ ]:


def calcular_utilidade(real,sintetico,target="hiv"):

    comum = list(set(real.columns).intersection(sintetico.columns))

    real = real[comum].copy()
    sintetico = sintetico[comum].copy()

    real = real.fillna("NA")
    sintetico = sintetico.fillna("NA")

    dados = pd.concat([real,sintetico])

    for c in dados.columns:
        le = LabelEncoder()
        dados[c] = le.fit_transform(dados[c].astype(str))

    real_enc = dados.iloc[:len(real)]
    syn_enc = dados.iloc[len(real):]

    X_train = syn_enc.drop(columns=[target])
    y_train = syn_enc[target]

    X_test = real_enc.drop(columns=[target])
    y_test = real_enc[target]

    modelo = LogisticRegression(max_iter=1000)

    modelo.fit(X_train,y_train)

    pred = modelo.predict(X_test)

    acc = accuracy_score(y_test,pred)
    prec = precision_score(y_test,pred,average="weighted")
    rec = recall_score(y_test,pred,average="weighted")
    f1 = f1_score(y_test,pred,average="weighted")

    proba = modelo.predict_proba(X_test)

    pmse = np.mean((proba.max(axis=1)-0.5)**2)

    return acc,prec,rec,f1,pmse


# In[ ]:


utilidade=[]

for nome,df in datasets.items():

    acc,prec,rec,f1,pmse = calcular_utilidade(original,df)

    utilidade.append([
        nome,
        acc,
        prec,
        rec,
        f1,
        pmse
    ])

utilidade=pd.DataFrame(utilidade,
columns=[
    "Modelo",
    "Accuracy",
    "Precision",
    "Recall",
    "F1",
    "pMSE"
])

utilidade


# In[ ]:


from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score

resultados_auc = []

for nome_modelo, sintetico in datasets.items():

    print(f"Calculando {nome_modelo}...")

    for alvo in variaveis:

        if alvo not in sintetico.columns:
            continue

        # Mantém apenas colunas existentes nos dois conjuntos
        colunas = [c for c in variaveis if c in sintetico.columns]

        real = original[colunas].copy()
        fake = sintetico[colunas].copy()

        real = real.dropna(subset=[alvo])
        fake = fake.dropna(subset=[alvo])

        if len(real) == 0 or len(fake) == 0:
            continue

        X_train = fake.drop(columns=[alvo])
        y_train = fake[alvo].astype(str)

        X_test = real.drop(columns=[alvo])
        y_test = real[alvo].astype(str)

        # Mantém apenas classes presentes nos dois conjuntos
        classes = sorted(set(y_train).intersection(set(y_test)))

        if len(classes) < 2:
            continue

        y_train = y_train[y_train.isin(classes)]
        X_train = X_train.loc[y_train.index]

        y_test = y_test[y_test.isin(classes)]
        X_test = X_test.loc[y_test.index]

        le = LabelEncoder()

        y_train = le.fit_transform(y_train)
        y_test = le.transform(y_test)

        pre = ColumnTransformer(
            transformers=[
                (
                    "cat",
                    Pipeline([
                        ("imp", SimpleImputer(strategy="most_frequent")),
                        ("oh", OneHotEncoder(handle_unknown="ignore"))
                    ]),
                    X_train.columns.tolist()
                )
            ]
        )

        clf = Pipeline([
            ("prep", pre),
            ("modelo", LogisticRegression(max_iter=1000))
        ])

        clf.fit(X_train, y_train)

        proba = clf.predict_proba(X_test)

        try:

            if len(le.classes_) == 2:

                auc = roc_auc_score(y_test, proba[:,1])

                pr_auc = average_precision_score(y_test, proba[:,1])

            else:

                auc = roc_auc_score(
                    y_test,
                    proba,
                    multi_class="ovr",
                    average="weighted"
                )

                pr_auc = average_precision_score(
                    pd.get_dummies(y_test),
                    proba,
                    average="weighted"
                )

        except:

            auc = np.nan
            pr_auc = np.nan

        resultados_auc.append({
            "Modelo": nome_modelo,
            "Variável": alvo,
            "AUC": auc,
            "PR-AUC": pr_auc
        })

auc_pr_auc = pd.DataFrame(resultados_auc).round(4)

display(auc_pr_auc)


# Privacidade

# In[ ]:


def preparar(df):

    df=df.copy()

    for c in df.columns:
        df[c]=df[c].astype(str)
    return pd.get_dummies(df).astype(int)


def privacidade(real,sintetico):

    A=preparar(real)
    B=preparar(sintetico)

    A,B=A.align(B,join="outer",axis=1,fill_value=0)

    dist=cdist(A.values,B.values)

    menor=dist.min(axis=1)

    record_matching=(menor==0).mean()

    distance=menor.mean()

    X=pd.concat([A,B])

    y=np.concatenate([
        np.zeros(len(A)),
        np.ones(len(B))
    ])

    X_train,X_test,y_train,y_test=train_test_split(
        X,y,test_size=0.3,random_state=42
    )

    modelo=LogisticRegression(max_iter=1000)

    modelo.fit(X_train,y_train)

    pred=modelo.predict(X_test)

    disting=accuracy_score(y_test,pred)

    return record_matching,disting,distance


# In[ ]:


priv=[]

for nome,df in datasets.items():

    rm,hsd,dcr = privacidade(original,df)

    priv.append([
        nome,
        rm,
        hsd,
        dcr
    ])

priv=pd.DataFrame(priv,
columns=[
    "Modelo",
    "Record Matching",
    "Hold-out Distinguishing",
    "Distance Real Data"
])

priv


# In[ ]:


final = utilidade.merge(priv,on="Modelo")

final = final.round(4)

final


# Descritiva dos dados reais

# In[ ]:


import pandas as pd
import numpy as np

# Variáveis utilizadas na análise
variaveis_descritivas = variaveis + ['regiao']

preprocessed_original = recategorize_data(original.copy())

preprocessed_original = preprocessed_original[
    (preprocessed_original['nu_idade_n'] >= 18) &
    (preprocessed_original['nu_idade_n'] <= 115)
].copy()


#categóricas

tabelas_categoricas = {}

for col in variaveis_descritivas:
    if col in preprocessed_original.columns and col != 'nu_idade_n':

        freq_abs = preprocessed_original[col].value_counts(dropna=False)

        freq_rel = (
            preprocessed_original[col]
            .value_counts(dropna=False, normalize=True)
            .mul(100)
        )

        tabela = pd.DataFrame({
            'Frequência': freq_abs,
            'Percentual (%)': freq_rel.round(2)
        })

        tabela.index = tabela.index.astype(str)

        tabelas_categoricas[col] = tabela

        print("\n" + "="*60)
        print(f"VARIÁVEL: {col}")
        print("="*60)
        print(tabela)


#descritivas da idade

idade = pd.to_numeric(
    preprocessed_original['nu_idade_n'],
    errors='coerce'
).dropna()

estatisticas_idade = pd.DataFrame({
    'Média': [idade.mean()],
    'Mediana': [idade.median()],
    'Desvio-padrão': [idade.std()],
    'Variância': [idade.var()],
    'Mínimo': [idade.min()],
    'Q1': [idade.quantile(0.25)],
    'Q3': [idade.quantile(0.75)],
    'Máximo': [idade.max()],
    'N válido': [idade.count()],
    'N ausente': [preprocessed_original['nu_idade_n'].isna().sum()]
})

print("\n" + "="*60)
print("ESTATÍSTICAS DESCRITIVAS - IDADE")
print("="*60)

print(estatisticas_idade.round(2))


# ### Frequência de Valores NA e Não NA por Variável

# In[ ]:


original_recategorized = recategorize_data(original.copy())

original_recategorized = original_recategorized[
    (original_recategorized['nu_idade_n'] >= 18) &
    (original_recategorized['nu_idade_n'] <= 115)
].copy()


print("Frequência de Valores NA e Não NA nas Variáveis Selecionadas (Após pré-processamento)")


for col in variaveis:
    if col in original_recategorized.columns:
        na_count = original_recategorized[col].isna().sum()
        not_na_count = original_recategorized[col].count()
        total_count = len(original_recategorized)

        na_percentage = (na_count / total_count) * 100
        not_na_percentage = (not_na_count / total_count) * 100

        print(f"\nVariável: {col}")
        print(f"  NA: {na_count} ({na_percentage:.2f}%%)")
        print(f"  Não NA: {not_na_count} ({not_na_percentage:.2f}%%)")
    else:
        print(f"\nVariável: {col} não encontrada no dataset.")


# In[ ]:


from scipy.stats import shapiro

#teste shapiro-wilk pra idade

idade = pd.to_numeric(
    original['nu_idade_n'],
    errors='coerce'
).dropna()

idade_teste = idade.sample(
    min(len(idade), 5000),
    random_state=42
)

stat, p_value = shapiro(idade_teste)

print("="*60)
print("TESTE DE SHAPIRO-WILK - IDADE")
print("="*60)

print(f"Estatística W: {stat:.4f}")
print(f"p-valor: {p_value:.6f}")

if p_value < 0.05:
    print("Resultado: rejeita-se H0. A distribuição não apresenta normalidade.")
else:
    print("Resultado: não se rejeita H0. Não há evidências suficientes contra a normalidade.")


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

preprocessed_original = recategorize_data(original)

preprocessed_original = preprocessed_original[
    (preprocessed_original['nu_idade_n'] >= 18) &
    (preprocessed_original['nu_idade_n'] <= 115)
].copy()


idade = pd.to_numeric(
    preprocessed_original['nu_idade_n'],
    errors='coerce'
).dropna()

plt.figure(figsize=(10, 6))

sns.histplot(
    x=idade,
    bins=range(18, 116, 1),
    kde=False,
    color='black'
)

plt.title(
    'Distribuição da Idade - Dados Originais Pré-processados',
    fontsize=16,
    fontweight='bold'
)

plt.xlabel('Idade')
plt.ylabel('Frequência')

plt.xticks(
    [20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
)

plt.tight_layout()
plt.show()

variaveis_categoricas = [
    col for col in variaveis + ['regiao']
    if col in preprocessed_original.columns and col != 'nu_idade_n'
]

for col in variaveis_categoricas:

    frequencia = (
        preprocessed_original[col]
        .astype(str)
        .value_counts(dropna=False)
    )

    order_list = None
    if col in mappings_for_order:
        order_list = [cat for cat in mappings_for_order[col] if cat in frequencia.index.tolist()]
        for cat_in_data in frequencia.index.tolist():
            if cat_in_data not in order_list:
                order_list.append(cat_in_data)
    else:
        order_list = frequencia.index.tolist()

    if 'nan' in order_list:
        order_list.remove('nan')
        order_list.append('nan')

    frequencia = frequencia.reindex(order_list, fill_value=0)

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(
        x=frequencia.index,
        y=frequencia.values,
        color='black'
    )

    plt.title(
        f'Distribuição de {col} - Dados Originais Pré-processados',
        fontsize=15,
        fontweight='bold'
    )

    plt.xlabel(col)
    plt.ylabel('Frequência')

    plt.xticks(
        rotation=45,
        ha='right'
    )

    plt.tight_layout()
    plt.show()


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

preprocessed_original = recategorize_data(original)

preprocessed_original = preprocessed_original[
    (preprocessed_original['nu_idade_n'] >= 18) &
    (preprocessed_original['nu_idade_n'] <= 115)
].copy()


fig, axes = plt.subplots(2, 3, figsize=(20, 10))

sexo = preprocessed_original['cs_sexo'].value_counts(normalize=True) * 100

sns.barplot(
    x=sexo.index,
    y=sexo.values,
    color='black',
    ax=axes[0, 0]
)

axes[0, 0].set_title('Sexo', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('')
axes[0, 0].set_ylim(0, 100)
axes[0, 0].set_yticks([0, 20, 40, 60, 80, 100])
axes[0, 0].set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
axes[0, 0].tick_params(axis='x', rotation=45)

raca = preprocessed_original['cs_raca'].value_counts(normalize=True) * 100

sns.barplot(
    x=raca.index,
    y=raca.values,
    color='black',
    ax=axes[0, 1]
)

axes[0, 1].set_title('Raça/Cor', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('')
axes[0, 1].set_ylabel('')
axes[0, 1].set_ylim(0, 100)
axes[0, 1].set_yticks([0, 20, 40, 60, 80, 100])
axes[0, 1].set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
axes[0, 1].tick_params(axis='x', rotation=45)

resultado = (
    preprocessed_original['resultado_exa_lab']
    .value_counts(normalize=True) * 100
)

sns.barplot(
    x=resultado.index,
    y=resultado.values,
    color='black',
    ax=axes[0, 2]
)

axes[0, 2].set_title(
    'Resultado do exame',
    fontsize=14,
    fontweight='bold'
)

axes[0, 2].set_xlabel('')
axes[0, 2].set_ylabel('')
axes[0, 2].set_ylim(0, 100)
axes[0, 2].set_yticks([0, 20, 40, 60, 80, 100])
axes[0, 2].set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
axes[0, 2].tick_params(axis='x', rotation=45)

evolucao = (
    preprocessed_original['evolucao']
    .value_counts(normalize=True) * 100
)

sns.barplot(
    x=evolucao.index,
    y=evolucao.values,
    color='black',
    ax=axes[1, 0]
)

axes[1, 0].set_title(
    'Evolução',
    fontsize=14,
    fontweight='bold'
)

axes[1, 0].set_xlabel('')
axes[1, 0].set_ylabel('')
axes[1, 0].set_ylim(0, 100)
axes[1, 0].set_yticks([0, 20, 40, 60, 80, 100])
axes[1, 0].set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
axes[1, 0].tick_params(axis='x', rotation=45)

idade = pd.to_numeric(
    preprocessed_original['nu_idade_n'],
    errors='coerce'
).dropna()

sns.histplot(
    idade,
    bins=range(18, 116, 1),
    kde=False,
    color='black',
    ax=axes[1, 1]
)

axes[1, 1].set_title(
    'Idade',
    fontsize=14,
    fontweight='bold'
)

axes[1, 1].set_xlabel('Idade')
axes[1, 1].set_ylabel('')

axes[1, 1].set_xticks(
    [20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
)

regiao = (
    preprocessed_original['regiao']
    .value_counts(normalize=True) * 100
)

sns.barplot(
    x=regiao.index,
    y=regiao.values,
    color='black',
    ax=axes[1, 2]
)

axes[1, 2].set_title(
    'Região',
    fontsize=14,
    fontweight='bold'
)

axes[1, 2].set_xlabel('')
axes[1, 2].set_ylabel('')
axes[1, 2].set_ylim(0, 100)
axes[1, 2].set_yticks([0, 20, 40, 60, 80, 100])
axes[1, 2].set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
axes[1, 2].tick_params(axis='x', rotation=45)

plt.tight_layout()

plt.show()


# In[ ]:


def plot_variable_comparison_poster(variable_name, dfs, epochs):

    model_names = [
        "Original",
        "RGAN",
        "CTGAN",
        "TableGAN",
        "MedGAN",
        "MedBGAN"
    ]

    original_plot = recategorize_data(original.copy())

    if variable_name == "nu_idade_n":

        original_plot["nu_idade_n"] = pd.to_numeric(
            original_plot["nu_idade_n"],
            errors="coerce"
        )

        original_plot = original_plot[
            (original_plot["nu_idade_n"] >= 18) &
            (original_plot["nu_idade_n"] <= 115)
        ].copy()

    current_dfs = [
        original_plot if i == 0 else dfs[i]
        for i in range(6)
    ]

    fig, axs = plt.subplots(
        3, 2,
        figsize=(12, 15),
        sharey=False
    )

    fig.suptitle(
        f"Comparação da variável: {variable_name} ({epochs} épocas)",
        fontsize=20,
        fontweight="bold"
    )

    for j, (df_to_plot, model_name) in enumerate(
        zip(current_dfs, model_names)
    ):

        ax = axs[j // 2, j % 2]

        ax.set_title(
            model_name,
            fontsize=16,
            fontweight="bold"
        )

        if variable_name not in df_to_plot.columns:

            ax.text(
                0.5, 0.5,
                "Dados não disponíveis",
                ha="center",
                va="center",
                transform=ax.transAxes
            )

            ax.set_axis_off()
            continue

        if variable_name == "nu_idade_n":

            numeric_age = pd.to_numeric(
                df_to_plot[variable_name],
                errors="coerce"
            ).dropna()

            numeric_age = numeric_age[
                (numeric_age >= 18) &
                (numeric_age <= 115)
            ]

            bins = np.arange(18, 117, 1)

            sns.histplot(
                x=numeric_age,
                ax=ax,
                bins=bins,
                kde=False,
                color=cores[model_name]
            )

            ax.set_xticks([
                20, 30, 40, 50, 60,
                70, 80, 90, 100, 110
            ])

            ax.set_xlabel("Idade")
            ax.set_ylabel("Contagem")

        else:

            freq = (
                df_to_plot[variable_name]
                .astype(str)
                .replace("nan", "Ignorado")
                .value_counts(normalize=True)
                .mul(100)
            )

            if variable_name in mappings_for_order:

                order_list = [
                    cat for cat in mappings_for_order[variable_name]
                    if cat in freq.index
                ]

                for cat in freq.index:
                    if cat not in order_list:
                        order_list.append(cat)

            else:
                order_list = sorted(freq.index.tolist())

            freq = freq.reindex(
                order_list,
                fill_value=0
            )

            sns.barplot(
                x=freq.index,
                y=freq.values,
                ax=ax,
                order=order_list,
                color=cores[model_name]
            )

            ax.set_xlabel("")
            ax.set_ylabel("Percentual")
            ax.set_ylim(0, 100)

            ax.set_yticks([0, 20, 40, 60, 80, 100])

            ax.yaxis.set_major_formatter(
                PercentFormatter()
            )

            ax.tick_params(
                axis="x",
                rotation=45,
                labelsize=12
            )

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# Idade - 50 épocas
dfs_50 = [
    original,
    rgan50,
    ct50,
    table50,
    medgan50,
    medb50
]

plot_variable_comparison_poster(
    "nu_idade_n",
    dfs_50,
    50
)


# Dados - 300 épocas
dfs_300 = [
    original,
    rgan300,
    ct300,
    table300,
    medgan300,
    medb300
]

# Idade - 300 épocas
plot_variable_comparison_poster(
    "nu_idade_n",
    dfs_300,
    300
)

# Sexo - 300 épocas
plot_variable_comparison_poster(
    "cs_sexo",
    dfs_300,
    300
)


# In[ ]:


import os
import matplotlib.pyplot as plt

pasta_exportacao = "/content/resultados/graficos"
os.makedirs(pasta_exportacao, exist_ok=True)

figuras = plt.get_fignums()

for i, numero in enumerate(figuras, start=1):
    fig = plt.figure(numero)

    fig.savefig(
        os.path.join(pasta_exportacao, f"grafico_{i:03d}.png"),
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

print(f"Total de gráficos exportados: {len(figuras)}")


# In[ ]:


import os
import matplotlib.pyplot as plt

pasta_brutos = "/content/resultados/brutos/graficos"
os.makedirs(pasta_brutos, exist_ok=True)

figuras = plt.get_fignums()

for numero in figuras:
    figura = plt.figure(numero)

    nome = f"grafico_{numero:03d}.png"

    figura.savefig(
        os.path.join(pasta_brutos, nome),
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

print(f"Total de figuras exportadas: {len(figuras)}")


# ## 10. Auditoria, seleção e organização dos gráficos
# 
# O repositório poderá conter gráficos duplicados, versões antigas, alterações de layout e resultados que foram gerados durante diferentes etapas de organização do notebook.
# 
# Antes de construir a galeria definitiva, realize uma auditoria visual e estrutural de todos os gráficos.
# 
# ### Identificação de duplicações
# 
# 1. Identifique arquivos visualmente idênticos.
# 2. Identifique gráficos que representam a mesma análise, mas possuem diferenças de organização, disposição, tamanho ou apresentação.
# 3. Agrupe as versões semelhantes.
# 4. Compare títulos, legendas, eixos, escalas, cores e legibilidade.
# 5. Identifique a versão visualmente mais adequada para publicação.
# 
# ### Seleção
# 
# - Não exclua arquivos originais.
# - Não considere gráficos diferentes como duplicados apenas porque possuem títulos semelhantes.
# - Preserve gráficos que apresentem informações distintas.
# - Priorize versões com títulos, legendas e eixos mais claros.
# - Não altere resultados científicos para melhorar a aparência.
# - Não invente dados nem reconstrua resultados sem acesso aos dados originais.
# 
# ### Organização
# 
# Organize os gráficos selecionados em categorias, considerando:
# 
# - Modelo utilizado;
# - Quantidade de épocas;
# - Variável analisada;
# - Tipo de análise;
# - Comparações entre modelos;
# - Distribuições e demais visualizações.
# 
# Utilize nomes descritivos para os arquivos selecionados.
# 
# ### Relatório de auditoria
# 
# Crie um arquivo chamado `relatorio_graficos.md` contendo:
# 
# - Quantidade total de arquivos encontrados;
# - Quantidade de duplicações exatas;
# - Grupos de gráficos semelhantes;
# - Versões escolhidas;
# - Arquivos mantidos fora da galeria;
# - Justificativa das escolhas;
# - Gráficos que necessitam de confirmação humana.
# 
# Quando houver dúvida sobre qual versão deve ser utilizada, não escolha arbitrariamente. Apresente as alternativas para aprovação.
# 
# ### Resultado final
# 
# A galeria do site deverá apresentar apenas os gráficos selecionados e organizados, mantendo os arquivos originais preservados em uma pasta separada.
