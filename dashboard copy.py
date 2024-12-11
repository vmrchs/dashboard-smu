import pandas as pd
import streamlit as st
import plotly.express as px 

logo = ('./logo_cism.png')

st.set_page_config(
    page_title="SMU - Painel de Adesão",
    page_icon=":bar_chart:",
    layout="wide"
    )

st.image(logo, width=300)
st.title("SMU - Painel de Adesão")
st.markdown("_Prototype v0.41_")

def load_data(path: str):
    data = pd.read_csv(path, sep=";")
    ## espaço para pequenas limpezas
    return data

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
# print(df[["terms_agreement", "convite_big_five_complete", "status_pesquisa"]])

st.sidebar.header('Filtros')
# Sidebar - Seleção de curso
unique_curso = df['curso'].unique()
selected_curso = st.sidebar.multiselect('Curso', unique_curso, unique_curso)

# Sidebar - Seleção de Filial
unique_filial = df['filial'].unique()
selected_filial = st.sidebar.multiselect('Filial', unique_filial, unique_filial)


with st.expander("Data Preview"):
    st.dataframe(df)

# Filtro de curso
# Filtra os dados com base no curso selecionado
df_filtrado = df[df["curso"].isin(selected_curso)]
# Filtra os dados com base no filial
df_filtrado =  df[df["filial"].isin(selected_filial)]

# Criar o gráfico com os dados filtrados
# Filtro de semestre

# Filtro por Filial

# Formatar as datas
df_filtrado['convite_big_five_timestamp'] = pd.to_datetime(df_filtrado['convite_big_five_timestamp'], errors="coerce", dayfirst=True)
df_filtrado["dates_formatted"] = df_filtrado['convite_big_five_timestamp'].dt.strftime('%Y-%m-%d')

# Contar as datas
date_counts = df_filtrado["dates_formatted"].value_counts().reset_index()
date_counts.columns = ["date", "count"]
date_counts = date_counts.sort_values("date")

# Página com número total de respostas por curso e por filial

# Página com o total de repostas por semestre

# Gráfico pizza de status de resposta da população 
# Contar a frequência de cada valor em 'status_pesquisa'
status_counts = df_filtrado["status_pesquisa"].value_counts().reset_index()
status_counts.columns = ["status_pesquisa", "count"]

# Criar o gráfico de pizza
pizza = px.pie(
    status_counts,
    values="count",
    names="status_pesquisa",
    title="Distribuição do Status da Pesquisa",
    color_discrete_sequence=px.colors.qualitative.Set3,  # Escolhe uma paleta de cores
)

st.plotly_chart(pizza)

# Barras verticais com respostas por dia
fig = px.bar(date_counts, x="date", y="count", 
             title=f"Respostas completas por dia {selected_curso}", 
             labels={"date": "Date", "count": "Count"},
             template="plotly_white")

st.plotly_chart(fig, use_container_width=True)
