
```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Dashboard de Sinalização Ferroviária",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown("""
<style>

    /* Fundo principal */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Cabeçalho */
    .main-header {
        background: linear-gradient(
            135deg,
            #172033 0%,
            #26364f 100%
        );
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    .main-header h1 {
        margin: 0;
        font-size: 36px;
    }

    .main-header p {
        margin-top: 8px;
        font-size: 16px;
        color: #d9e1ec;
    }

    /* Cartões */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e1e5eb;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        text-align: center;
    }

    .metric-title {
        color: #687386;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #172033;
        font-size: 28px;
        font-weight: bold;
    }

    /* Seções */
    .section-title {
        color: #172033;
        font-size: 24px;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #687386;
        margin-bottom: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #172033;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CARREGAR DATASET
# ============================================================

@st.cache_data
def carregar_dados():
    return pd.read_csv("dataset_sinalizacao_ferroviaria.csv")


df = carregar_dados()


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown("""
<div class="main-header">

    <h1>🚆 Sinalização Ferroviária</h1>

    <p>
        Dashboard de análise de headway, velocidade,
        ocupação dos circuitos e aspectos dos sinais.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚆 Controle")

st.sidebar.markdown("---")

st.sidebar.subheader("Filtros")

tipos_disponiveis = sorted(
    df["tipo_sinalizacao"].dropna().unique()
)

tipos_selecionados = st.sidebar.multiselect(
    "Tipo de sinalização",
    options=tipos_disponiveis,
    default=tipos_disponiveis
)

aspectos_disponiveis = sorted(
    df["aspecto_sinal"].dropna().unique()
)

aspectos_selecionados = st.sidebar.multiselect(
    "Aspecto do sinal",
    options=aspectos_disponiveis,
    default=aspectos_disponiveis
)


# ============================================================
# APLICAR FILTROS
# ============================================================

df_filtrado = df[
    df["tipo_sinalizacao"].isin(tipos_selecionados)
    &
    df["aspecto_sinal"].isin(aspectos_selecionados)
]


# ============================================================
# INDICADORES
# ============================================================

st.markdown(
    '<div class="section-title">📊 Visão geral</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Resumo dos dados selecionados pelos filtros.'
    '</div>',
    unsafe_allow_html=True
)


total_registros = len(df_filtrado)

total_linhas = df_filtrado["linha"].nunique()

total_blocos = df_filtrado["id_bloco"].nunique()

headway_medio = df_filtrado["headway_seg"].mean()

velocidade_media = df_filtrado["velocidade_permitida_kmh"].mean()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Registros</div>
        <div class="metric-value">{total_registros:,}</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Linhas</div>
        <div class="metric-value">{total_linhas}</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Blocos</div>
        <div class="metric-value">{total_blocos}</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Headway médio</div>
        <div class="metric-value">{headway_medio:.1f}s</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# GRÁFICO 1
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔎 1. Velocidade x Tempo de Ocupação'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Relação entre a velocidade permitida e o tempo '
    'de ocupação do circuito.'
    '</div>',
    unsafe_allow_html=True
)


fig1, ax1 = plt.subplots(figsize=(11, 5.5))

sns.scatterplot(
    data=df_filtrado,
    x="velocidade_permitida_kmh",
    y="tempo_ocupacao_circuito_seg",
    hue="tipo_sinalizacao",
    s=55,
    alpha=0.7,
    ax=ax1
)

ax1.set_xlabel(
    "Velocidade permitida (km/h)",
    fontsize=11
)

ax1.set_ylabel(
    "Tempo de ocupação (segundos)",
    fontsize=11
)

ax1.set_title(
    "Velocidade permitida x tempo de ocupação",
    fontsize=15,
    fontweight="bold"
)

ax1.grid(
    True,
    linestyle="--",
    alpha=0.25
)

sns.despine()

plt.tight_layout()

st.pyplot(fig1, use_container_width=True)


# ============================================================
# GRÁFICO 2
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📦 2. Distribuição do Headway'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Distribuição do intervalo de tempo entre trens '
    'por tipo de sinalização.'
    '</div>',
    unsafe_allow_html=True
)


fig2, ax2 = plt.subplots(figsize=(11, 5.5))

sns.boxplot(
    data=df_filtrado,
    x="tipo_sinalizacao",
    y="headway_seg",
    ax=ax2
)

ax2.set_xlabel(
    "Tipo de sinalização",
    fontsize=11
)

ax2.set_ylabel(
    "Headway (segundos)",
    fontsize=11
)

ax2.set_title(
    "Distribuição do headway por tipo de sinalização",
    fontsize=15,
    fontweight="bold"
)

ax2.grid(
    True,
    axis="y",
    linestyle="--",
    alpha=0.25
)

sns.despine()

plt.tight_layout()

st.pyplot(fig2, use_container_width=True)


# ============================================================
# GRÁFICO 3
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🚦 3. Aspectos dos Sinais'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Quantidade de sinais verdes, amarelos e vermelhos '
    'por tipo de sinalização.'
    '</div>',
    unsafe_allow_html=True
)


contagem = pd.crosstab(
    df_filtrado["tipo_sinalizacao"],
    df_filtrado["aspecto_sinal"]
)


fig3, ax3 = plt.subplots(figsize=(11, 5.5))


# Garantir uma ordem lógica dos sinais quando disponíveis
ordem_aspectos = [
    aspecto
    for aspecto in ["Verde", "Amarelo", "Vermelho"]
    if aspecto in contagem.columns
]

# Caso o dataset use outra capitalização,
# mantém as colunas existentes
outras_colunas = [
    coluna
    for coluna in contagem.columns
    if coluna not in ordem_aspectos
]

contagem = contagem[
    ordem_aspectos + outras_colunas
]


contagem.plot(
    kind="bar",
    stacked=True,
    ax=ax3
)


ax3.set_xlabel(
    "Tipo de sinalização",
    fontsize=11
)

ax3.set_ylabel(
    "Quantidade de ocorrências",
    fontsize=11
)

ax3.set_title(
    "Aspectos dos sinais por tipo de sinalização",
    fontsize=15,
    fontweight="bold"
)

ax3.tick_params(
    axis="x",
    rotation=0
)

ax3.grid(
    True,
    axis="y",
    linestyle="--",
    alpha=0.25
)

ax3.legend(
    title="Aspecto do sinal"
)

sns.despine()

plt.tight_layout()

st.pyplot(fig3, use_container_width=True)


# ============================================================
# TABELA ESTATÍSTICA
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📈 4. Resumo estatístico'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Estatísticas descritivas das principais variáveis.'
    '</div>',
    unsafe_allow_html=True
)


variaveis = [
    "headway_seg",
    "velocidade_permitida_kmh",
    "tempo_ocupacao_circuito_seg"
]


resumo = df_filtrado[variaveis].describe().round(2)


st.dataframe(
    resumo,
    use_container_width=True
)


# ============================================================
# DADOS
# ============================================================

with st.expander("📋 Visualizar dataset completo"):

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")

st.caption(
    "Dashboard desenvolvido para análise do dataset "
    "de sinalização ferroviária."
)
```
