
import pandas as pd
import sys

data_file = sys.argv[1]

# data_file = "./data/HIST_PAINEL_COVIDBR_13mai2021.csv"
data_file = "./data/HIST_PAINEL_COVIDBR_2022_Parte1_21fev2022.csv"
# data_file = "./data/HIST_PAINEL_COVIDBR_2022_Parte1_22fev2022.csv"

df = pd.read_csv(data_file, sep=";")
df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]
df_brasil = df[df["regiao"]=="Brasil"]
df_states.to_csv("./data/df_states.csv")
df_brasil.to_csv("./data/df_brasil.csv")
