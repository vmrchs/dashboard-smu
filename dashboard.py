import pandas as pd
import streamlit as st
import plotly.express as px 

logo = './logo_cism.png'

st.set_page_config(
    page_title="SMU - Painel de Adesão",
    page_icon=":bar_chart:",
    layout="wide"
)

st.image(logo, width=300)
st.title("SMU - Painel de Adesão")
st.markdown("_Prototype v0.41_")

def load_data(path: str):
    return pd.read_csv(path, sep=";")

def criar_coluna_status_pesquisa(df):
    def determinar_status(row):
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

    df["status_pesquisa"] = df.apply(determinar_status, axis=1)
    return df

# Carregar e processar os dados
df = load_data("./dados_smu_raw.csv")
df = criar_coluna_status_pesquisa(df)

# Sidebar - Filtros
st.sidebar.header('Filtros')
selected_curso = st.sidebar.multiselect('Curso', df['curso'].unique(), df['curso'].unique())
selected_filial = st.sidebar.multiselect('Filial', df['filial'].unique(), df['filial'].unique())

# Exibir prévia de dados
with st.expander("Data Preview"):
    st.dataframe(df)

# Filtragem
df_filtrado = df[df['curso'].isin(selected_curso) & df['filial'].isin(selected_filial)]

# Formatação das datas
df_filtrado['convite_big_five_timestamp'] = pd.to_datetime(df_filtrado['convite_big_five_timestamp'], errors="coerce", dayfirst=True)
df_filtrado["dates_formatted"] = df_filtrado['convite_big_five_timestamp'].dt.strftime('%Y-%m-%d')

# Contagem de respostas por data
date_counts = df_filtrado['dates_formatted'].value_counts().reset_index()
date_counts.columns = ['date', 'count']
date_counts = date_counts.sort_values('date')

# Contagem de status de pesquisa
status_counts = df_filtrado['status_pesquisa'].value_counts().reset_index()
status_counts.columns = ['status_pesquisa', 'count']

# Gráfico de pizza de status de resposta
pizza = px.pie(
    status_counts,
    values='count',
    names='status_pesquisa',
    title='Distribuição do Status da Pesquisa',
    color_discrete_sequence=px.colors.qualitative.Set3,
)
st.plotly_chart(pizza, use_container_width=True)

# Gráfico de barras de respostas por dia
fig = px.bar(
    date_counts, 
    x='date', 
    y='count', 
    title=f'Respostas completas por dia {", ".join(selected_curso)}', 
    labels={'date': 'Date', 'count': 'Count'},
    template='plotly_white'
)
st.plotly_chart(fig, use_container_width=True)
