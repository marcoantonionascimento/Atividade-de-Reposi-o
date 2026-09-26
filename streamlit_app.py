import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Sinalização Ferroviária",
    page_icon="🚆",
    layout="wide"
)


# ============================================================
# TÍTULO
# ============================================================

st.title("🚆 Análise de Sinalização Ferroviária")

st.write(
    "Dashboard para análise dos dados de headway, "
    "aspecto dos sinais, velocidade permitida e tempo "
    "de ocupação do circuito."
)


# ============================================================
# CARREGAR DATASET
# ============================================================

@st.cache_data
def carregar_dados():
    return pd.read_csv("dataset_sinalizacao_ferroviaria.csv")


df = carregar_dados()


# ============================================================
# INFORMAÇÕES DO DATASET
# ============================================================

st.subheader("📊 Dataset")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Registros", len(df))

with col2:
    st.metric("Linhas", df["linha"].nunique())

with col3:
    st.metric("Blocos", df["id_bloco"].nunique())


# ============================================================
# VISUALIZAR DADOS
# ============================================================

with st.expander("Visualizar dados"):
    st.dataframe(df)


# ============================================================
# FILTRO
# ============================================================

st.sidebar.header("Filtros")

tipos = st.sidebar.multiselect(
    "Tipo de sinalização",
    options=df["tipo_sinalizacao"].unique(),
    default=df["tipo_sinalizacao"].unique()
)

df_filtrado = df[
    df["tipo_sinalizacao"].isin(tipos)
]


# ============================================================
# GRÁFICO 1 - DISPERSÃO
# ============================================================

st.subheader(
    "1. Velocidade Permitida x Tempo de Ocupação"
)

st.write(
    "Relação entre a velocidade permitida pelo sinal "
    "e o tempo de ocupação do circuito."
)

fig1, ax1 = plt.subplots(figsize=(10, 6))

sns.scatterplot(
    data=df_filtrado,
    x="velocidade_permitida_kmh",
    y="tempo_ocupacao_circuito_seg",
    hue="tipo_sinalizacao",
    ax=ax1
)

ax1.set_xlabel("Velocidade Permitida (km/h)")
ax1.set_ylabel("Tempo de Ocupação (segundos)")
ax1.set_title(
    "Velocidade Permitida x Tempo de Ocupação"
)

ax1.grid(True, alpha=0.3)

st.pyplot(fig1)


# ============================================================
# GRÁFICO 2 - BOXPLOT
# ============================================================

st.subheader(
    "2. Distribuição do Headway"
)

st.write(
    "Comparação da distribuição do headway "
    "entre os tipos de sinalização."
)

fig2, ax2 = plt.subplots(figsize=(10, 6))

sns.boxplot(
    data=df_filtrado,
    x="tipo_sinalizacao",
    y="headway_seg",
    ax=ax2
)

ax2.set_xlabel("Tipo de Sinalização")
ax2.set_ylabel("Headway (segundos)")
ax2.set_title(
    "Distribuição do Headway por Tipo de Sinalização"
)

ax2.grid(True, axis="y", alpha=0.3)

st.pyplot(fig2)



# ============================================================
# RESUMO ESTATÍSTICO
# ============================================================

st.subheader("📈 Resumo Estatístico")

variaveis = [
    "headway_seg",
    "velocidade_permitida_kmh",
    "tempo_ocupacao_circuito_seg"
]

st.dataframe(
    df_filtrado[variaveis].describe()
)
