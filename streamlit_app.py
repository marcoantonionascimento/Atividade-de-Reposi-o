import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Sinalização Ferroviária",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

    /* Fundo geral */
    .stApp {
        background-color: #080d14;
        color: #e8edf5;
    }

    /* Área principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b111a;
        border-right: 1px solid #1c2a3a;
    }

    section[data-testid="stSidebar"] * {
        color: #dbe5f2;
    }

    /* Título principal */
    .titulo {
        background: linear-gradient(
            135deg,
            #111c2b 0%,
            #0b1420 100%
        );

        border: 1px solid #20344b;
        border-radius: 12px;

        padding: 28px 32px;
        margin-bottom: 25px;

        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }

    .titulo h1 {
        color: #f3f6fa;
        font-size: 42px;
        font-weight: 700;
        margin: 0;
    }

    .titulo p {
        color: #9fb3ca;
        font-size: 17px;
        margin-top: 8px;
        margin-bottom: 0;
    }

    /* Títulos das seções */
    .secao {
        color: #dce8f7;
        font-size: 23px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 15px;
        border-left: 4px solid #2878d7;
        padding-left: 12px;
    }

    /* Cards */
    .card {
        background: linear-gradient(
            145deg,
            #101a27,
            #0b131e
        );

        border: 1px solid #1d3045;
        border-radius: 10px;

        padding: 20px;

        min-height: 115px;

        box-shadow: 0 5px 20px rgba(0,0,0,0.20);
    }

    .card-title {
        color: #91a7bf;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .card-value {
        color: #f0f4f9;
        font-size: 28px;
        font-weight: 700;
    }

    /* Painéis dos gráficos */
    .painel {
        background-color: #0d1621;
        border: 1px solid #1c2d40;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 20px;
    }

    .painel h3 {
        color: #e7edf5;
        font-size: 18px;
        margin-bottom: 5px;
    }

    .painel p {
        color: #899db4;
        font-size: 13px;
    }

    /* Texto */
    p, label {
        color: #aabbd0;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #111c29;
        border-color: #263a50;
    }

    /* Tabela */
    .stDataFrame {
        border: 1px solid #203246;
    }

    /* Divisórias */
    hr {
        border-color: #1b2b3d;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CARREGAMENTO DO DATASET
# ============================================================

@st.cache_data
def carregar_dados():
    return pd.read_csv("dataset_sinalizacao_ferroviaria.csv")


df = carregar_dados()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="color:#eef3f8;">
            Sinalização Ferroviária
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### Filtros")

    tipos = sorted(df["tipo_sinalizacao"].dropna().unique())

    tipos_selecionados = st.multiselect(
        "Tipo de sinalização",
        tipos,
        default=tipos
    )

    aspectos = sorted(df["aspecto_sinal"].dropna().unique())

    aspectos_selecionados = st.multiselect(
        "Aspecto do sinal",
        aspectos,
        default=aspectos
    )

    # Aplicação dos filtros
    df_filtrado = df[
        df["tipo_sinalizacao"].isin(tipos_selecionados)
        & df["aspecto_sinal"].isin(aspectos_selecionados)
    ]

    st.markdown("---")

    st.markdown("### Informações do dataset")

    st.write(f"Registros: **{len(df_filtrado):,}**")
    st.write(
        f"Linhas: **{df_filtrado['linha'].nunique()}**"
    )
    st.write(
        f"Blocos: **{df_filtrado['id_bloco'].nunique()}**"
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            color:#71869d;
            font-size:13px;
            line-height:1.6;
        ">
        Análise de dados aplicada à sinalização ferroviária,
        considerando headway, velocidade permitida,
        ocupação dos circuitos e aspectos dos sinais.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <div class="titulo">

        <h1>Sinalização Ferroviária</h1>

        <p>
        Dashboard de análise de headway, velocidade,
        ocupação dos circuitos e aspectos dos sinais.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# VISÃO GERAL
# ============================================================

st.markdown(
    '<div class="secao">Visão geral</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)


# Valores
total_registros = len(df_filtrado)

total_linhas = df_filtrado["linha"].nunique()

total_blocos = df_filtrado["id_bloco"].nunique()

headway_medio = df_filtrado["headway_seg"].mean()

velocidade_media = df_filtrado[
    "velocidade_permitida_kmh"
].mean()


def card(coluna, titulo, valor):

    with coluna:

        st.markdown(
            f"""
            <div class="card">

                <div class="card-title">
                    {titulo}
                </div>

                <div class="card-value">
                    {valor}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


card(
    col1,
    "Registros",
    f"{total_registros:,}".replace(",", ".")
)

card(
    col2,
    "Linhas",
    total_linhas
)

card(
    col3,
    "Blocos",
    total_blocos
)

card(
    col4,
    "Headway médio",
    f"{headway_medio:.1f} s"
)

card(
    col5,
    "Velocidade média",
    f"{velocidade_media:.1f} km/h"
)


# ============================================================
# GRÁFICOS
# ============================================================

st.markdown(
    '<div class="secao">Análise dos dados</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ============================================================
# GRÁFICO 1
# ============================================================

with col1:

    st.markdown(
        """
        <div class="painel">

        <h3>
        Velocidade permitida x tempo de ocupação
        </h3>

        <p>
        Relação entre a velocidade autorizada pelo sinal
        e o tempo de ocupação do circuito.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(7, 5))

    fig.patch.set_facecolor("#0d1621")
    ax.set_facecolor("#0d1621")

    sns.scatterplot(
        data=df_filtrado,
        x="velocidade_permitida_kmh",
        y="tempo_ocupacao_circuito_seg",
        hue="tipo_sinalizacao",
        palette="deep",
        s=45,
        alpha=0.75,
        ax=ax
    )

    ax.set_xlabel(
        "Velocidade permitida (km/h)",
        color="#aabbd0"
    )

    ax.set_ylabel(
        "Tempo de ocupação (s)",
        color="#aabbd0"
    )

    ax.tick_params(colors="#91a7bf")

    for spine in ax.spines.values():
        spine.set_color("#26394d")

    ax.grid(
        alpha=0.15,
        color="#789"
    )

    legend = ax.legend(
        title="Tipo de sinalização"
    )

    legend.get_frame().set_facecolor("#101b29")
    legend.get_frame().set_edgecolor("#263a50")

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# GRÁFICO 2
# ============================================================

with col2:

    st.markdown(
        """
        <div class="painel">

        <h3>
        Distribuição do headway
        </h3>

        <p>
        Comparação da distribuição do intervalo entre
        a passagem de trens.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(7, 5))

    fig.patch.set_facecolor("#0d1621")
    ax.set_facecolor("#0d1621")

    sns.boxplot(
        data=df_filtrado,
        x="tipo_sinalizacao",
        y="headway_seg",
        palette="deep",
        ax=ax
    )

    ax.set_xlabel(
        "Tipo de sinalização",
        color="#aabbd0"
    )

    ax.set_ylabel(
        "Headway (segundos)",
        color="#aabbd0"
    )

    ax.tick_params(colors="#91a7bf")

    for spine in ax.spines.values():
        spine.set_color("#26394d")

    ax.grid(
        axis="y",
        alpha=0.15
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# GRÁFICO 3
# ============================================================

st.markdown(
    """
    <div class="painel">

    <h3>
    Aspectos dos sinais por tipo de sinalização
    </h3>

    <p>
    Quantidade de ocorrências dos diferentes aspectos
    dos sinais.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

tabela_aspectos = pd.crosstab(
    df_filtrado["tipo_sinalizacao"],
    df_filtrado["aspecto_sinal"]
)

fig, ax = plt.subplots(figsize=(12, 5))

fig.patch.set_facecolor("#0d1621")
ax.set_facecolor("#0d1621")

tabela_aspectos.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    colormap="viridis"
)

ax.set_xlabel(
    "Tipo de sinalização",
    color="#aabbd0"
)

ax.set_ylabel(
    "Quantidade de ocorrências",
    color="#aabbd0"
)

ax.tick_params(colors="#91a7bf")

for spine in ax.spines.values():
    spine.set_color("#26394d")

ax.grid(
    axis="y",
    alpha=0.15
)

legend = ax.legend(
    title="Aspecto do sinal"
)

legend.get_frame().set_facecolor("#101b29")
legend.get_frame().set_edgecolor("#263a50")

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# ESTATÍSTICAS
# ============================================================

st.markdown(
    '<div class="secao">Resumo estatístico</div>',
    unsafe_allow_html=True
)

colunas_numericas = [
    "headway_seg",
    "velocidade_permitida_kmh",
    "tempo_ocupacao_circuito_seg"
]

estatisticas = df_filtrado[
    colunas_numericas
].describe().T

estatisticas = estatisticas.rename(
    columns={
        "count": "Quantidade",
        "mean": "Média",
        "std": "Desvio padrão",
        "min": "Mínimo",
        "25%": "25%",
        "50%": "Mediana",
        "75%": "75%",
        "max": "Máximo"
    }
)

estatisticas = estatisticas.round(2)

st.dataframe(
    estatisticas,
    use_container_width=True
)


# ============================================================
# DADOS
# ============================================================

with st.expander("Visualizar dados do dataset"):

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        height=400
    )
