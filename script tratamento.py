import pandas as pd
import streamlit as st
import plotly.express as px 


def load_data(path: str):
    data = pd.read_csv(path, sep=";")
    ## espaço para pequenas limpezas
    return data

df = load_data("./dados_smu_raw.csv")

def criar_coluna_status_pesquisa(df):
    def determinar_status(row):
        # Verifica se a célula em 'terms_agreement' está vazia ou é NaN
        if pd.isna(row["terms_agreement"]) or row["terms_agreement"] == "":
            return "Não respondeu à pesquisa"
        elif row["terms_agreement"] == 0:
            return "Recusou participação"
        elif row["terms_agreement"] == 1 and row["convite_big_five_complete"] == 0:
            return "Aceitou e começou a responder"
        elif row["terms_agreement"] == 1 and row["convite_big_five_complete"] == 2:
            return "Terminou a pesquisa"
        else:
            return "Indefinido"

    # Aplicar a lógica linha por linha
    df["status_pesquisa"] = df.apply(determinar_status, axis=1)
    return df

# Carregar os dados
df = load_data("./dados_smu_raw.csv")

# Criar a nova coluna com a lógica
df = criar_coluna_status_pesquisa(df)

# Exibir o DataFrame atualizado
print(df[["terms_agreement", "convite_big_five_complete", "status_pesquisa"]])
