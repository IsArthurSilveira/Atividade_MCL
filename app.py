import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

st.set_page_config(
    page_title="S.O.R.O. - Sistema Organizacional para Registros de Ocorrencias",
    page_icon=None,
    layout="wide"
)
# ...existing code...

# Rodapé com créditos
st.markdown("""
<hr style='margin-top:2.5rem;margin-bottom:0.5rem;'>
<div style='text-align:center; color:#1565c0; font-size:1.1rem;'>
Desenvolvido por alunos da turma de TADS 044:<br>
<b>Arthur Silveira, Maíra Lourenço, Manoel Olímpio, Matheus Willian, Victor Gomes e Victoria Zambom</b>
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

st.set_page_config(
    page_title="S.O.R.O. - Sistema Organizacional para Registros de Ocorrencias",
    page_icon=None,
    layout="wide"
)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dados_soro.csv")
        if 'data_hora' in df.columns:
            df['data_hora'] = pd.to_datetime(df['data_hora'])
        return df
    except Exception as e:
        st.error(f"Erro ao ler CSV: {e}")
        return pd.DataFrame()

df = load_data()

df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
cols_numericas = ['latitude', 'longitude', 'tempo_resposta', 'qtd_total_vitimas', 'incendio_consumo_agua']
for col in cols_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['incendio_consumo_agua'] = df['incendio_consumo_agua'].fillna(0)

# Filtros como botão expansível no topo
with st.expander("Filtros", expanded=False):
    bairros = df['bairro'].dropna().unique()
    bairro_sel = st.multiselect("Bairro:", bairros, default=bairros)
df_filtrado = df[df['bairro'].isin(bairro_sel)]

st.title("S.O.R.O. - Sistema Organizacional para Registros de Ocorrencias")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de Ocorrências", len(df_filtrado))
c2.metric("Vítimas Registradas", int(df_filtrado["qtd_total_vitimas"].sum()))
c3.metric("Tempo Médio Resposta", f"{df_filtrado['tempo_resposta'].mean():.1f} min")
c4.metric("Consumo Água (Incêndio)", f"{df_filtrado['incendio_consumo_agua'].sum():,.0f} L")

st.divider()

aba1, aba2, aba3, aba4 = st.tabs(["Visão Geral", "Incêndios", "Data Science & ML", "Salvamento & Praias"])

# Paleta de tons de azul (mas fundo branco)
azul_palette = ["#0d47a1", "#1976d2", "#2196f3", "#64b5f6", "#bbdefb", "#1565c0", "#42a5f5", "#90caf9"]

# Forçar fundo branco e layout simples
st.markdown(
    """
    <style>
    body, .stApp, .main, .block-container, .css-18e3th9, .css-1d391kg {
        background-color: #fff !important;
        color: #111 !important;
    }
    .stTabs [data-baseweb=\"tab\"] {
        background: #fff !important;
        color: #111 !important;
    }
    .stButton>button, .stMultiSelect, .stExpander {
        background: #fff !important;
        color: #111 !important;
        border-radius: 6px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with aba1:
    colA, colB = st.columns(2)
    with colA:
        st.subheader("Distribuição por Tipo (Rosquinha)")
        fig_pie = px.pie(df_filtrado, names="tipo_ocorrencia", hole=0.4, title="Frequência Relativa dos Casos",
            color_discrete_sequence=azul_palette, template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)
    with colB:
        st.subheader("Mapa de Calor (Distribuição Espacial)")
        st.map(df_filtrado, latitude="latitude", longitude="longitude")

    st.subheader("Comparação de Distribuição (Boxplot)")
    st.markdown("Comparativo da variação do **Tempo de Resposta** entre os diferentes tipos de ocorrência.")
    fig_box = px.box(df_filtrado, x="tipo_ocorrencia", y="tempo_resposta", 
                     color="tipo_ocorrencia", points="all",
                     title="Distribuição de Tempo por Tipo",
                     color_discrete_sequence=azul_palette, template="plotly_white")
    st.plotly_chart(fig_box, use_container_width=True)
    
    st.subheader("Distribuição Temporal (Gráfico de Linha)")
    df_tempo = df_filtrado.groupby(df_filtrado["data_hora"].dt.date).size().reset_index(name="Qtd")
    fig_linha = px.line(df_tempo, x="data_hora", y="Qtd", markers=True, title="Evolução Temporal dos Casos",
                        color_discrete_sequence=azul_palette, template="plotly_white")
    st.plotly_chart(fig_linha, use_container_width=True)

with aba2:
    st.markdown("### Análise Específica de Incêndios")
    df_fogo = df_filtrado[df_filtrado["tipo_ocorrencia"] == "Incêndio"]

    if df_fogo.empty:
        st.warning("Nenhum incêndio nos filtros selecionados.")
    else:
        c5, c6 = st.columns(2)
        with c5:
            causas = df_fogo["subtipo_ocorrencia"].value_counts().reset_index()
            causas.columns = ["Causa", "Quantidade"]
            fig_causa = px.bar(causas, x="Causa", y="Quantidade", title="Ranking de Causas", color="Quantidade",
                              color_continuous_scale=azul_palette, template="plotly_white")
            st.plotly_chart(fig_causa, use_container_width=True)
        with c6:
            saz = df_fogo.groupby(df_fogo["data_hora"].dt.month_name()).size().reset_index(name="Qtd")
            fig_mes = px.bar(saz, x="data_hora", y="Qtd", title="Sazonalidade (Mês)",
                            color_discrete_sequence=azul_palette, template="plotly_white")
            st.plotly_chart(fig_mes, use_container_width=True)
        
        st.info("Sistema de Recomendação Ativo")
        causas_lista = causas["Causa"].tolist()
        for i, causa in enumerate(causas_lista):
            if i < 3: 
                if "Gás" in causa:
                    st.error(f"Risco Crítico: {causa} -> Ação: Fiscalizar instalações prediais no Centro.")
                elif "Vegetação" in causa or "Fogos" in causa:
                    st.warning(f"Risco Sazonal: {causa} -> Ação: Monitoramento preventivo (Drones).")

with aba3:
    st.header("Inteligência Artificial Aplicada")
    st.markdown("Análise avançada utilizando algoritmos de **Clusterização** e **Regressão**.")

    col_ml1, col_ml2 = st.columns(2)

    with col_ml1:
        st.subheader("1. Clusterização (Agrupamento)")
        st.markdown("O algoritmo K-Means agrupou as ocorrências baseadas em Tempo de Resposta e Consumo de Água.")
        
        df_cluster = df_filtrado[['tempo_resposta', 'incendio_consumo_agua']].dropna()
        if len(df_cluster) > 3:
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            df_cluster['Cluster'] = kmeans.fit_predict(df_cluster)
            df_cluster['Cluster'] = df_cluster['Cluster'].astype(str) # Para virar cor discreta
            
            fig_cluster = px.scatter(df_cluster, x="tempo_resposta", y="incendio_consumo_agua", 
                                     color="Cluster", size_max=15,
                                     title="Grupos de Ocorrências (Clusters)",
                                     labels={"tempo_resposta": "Tempo (min)", "incendio_consumo_agua": "Água (L)"},
                                     color_discrete_sequence=azul_palette, template="plotly_white")
            st.plotly_chart(fig_cluster, use_container_width=True)
        else:
            st.warning("Dados insuficientes para Clusterização.")

    with col_ml2:
        st.subheader("2. Regressão (Tendência)")
        st.markdown("Visualização da correlação entre Tempo e Consumo com linha de tendência (OLS).")
        
        df_reg = df_filtrado[df_filtrado['incendio_consumo_agua'] > 0]
        if not df_reg.empty:
            fig_reg = px.scatter(df_reg, x="tempo_resposta", y="incendio_consumo_agua", 
                                 trendline="ols",
                                 title="Regressão: Tempo x Consumo de Água",
                                 color="tipo_ocorrencia",
                                 color_discrete_sequence=azul_palette, template="plotly_white")
            st.plotly_chart(fig_reg, use_container_width=True)
        else:
            st.warning("Sem dados de consumo de água para regressão.")

    st.divider()

    st.subheader("3. Modelo Preditivo (Fatores de Influência)")
    st.markdown("Modelo treinado para identificar quais variáveis mais influenciam no consumo de recursos.")
    
    treinar = st.button("Treinar Modelo Preditivo")
    
    if treinar:
        df_ml_train = df[df["tipo_ocorrencia"] == "Incêndio"].dropna(subset=["incendio_grupo", "incendio_consumo_agua", "bairro"])
        
        if len(df_ml_train) < 5:
            st.warning("Dados insuficientes para treinar a IA.")
        else:
            le_bairro = LabelEncoder()
            le_grupo = LabelEncoder()
            df_ml_train["bairro_cod"] = le_bairro.fit_transform(df_ml_train["bairro"])
            df_ml_train["grupo_cod"] = le_grupo.fit_transform(df_ml_train["incendio_grupo"])
            
            X = df_ml_train[["bairro_cod", "grupo_cod", "tempo_resposta"]]
            y = df_ml_train["incendio_consumo_agua"]
            
            modelo = RandomForestRegressor(n_estimators=100, random_state=42)
            modelo.fit(X, y)
            
            st.success("Modelo treinado com sucesso!")
            
            imp = pd.DataFrame({"Fator": ["Bairro", "Tipo de Incêndio", "Tempo de Resposta"], "Peso": modelo.feature_importances_})
            fig_imp = px.bar(imp, x="Peso", y="Fator", orientation='h', title="Fatores Determinantes nos Tipos de Caso",
                             color_discrete_sequence=azul_palette, template="plotly_white")
            st.plotly_chart(fig_imp, use_container_width=True)

with aba4:
    st.markdown("### Monitoramento de Praias (Shark Monitor)")
    df_praia = df_filtrado[df_filtrado['tipo_ocorrencia'] == 'Salvamento']
    
    if df_praia.empty:
        st.info("Nenhuma ocorrência de salvamento na área selecionada.")
    else:
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.subheader("Perfil de Risco (Gênero)")
            fig_gen = px.pie(df_praia, names='genero', title="Vítimas por Gênero", 
                             color='genero', color_discrete_sequence=azul_palette, template="plotly_white")
            st.plotly_chart(fig_gen, use_container_width=True)
            
        with col_p2:
            st.subheader("Tipos de Incidente")
            dados_praia = df_praia['subtipo_ocorrencia'].value_counts().reset_index()
            dados_praia.columns = ['Tipo', 'Qtd']
            fig_bar_praia = px.bar(dados_praia, x='Qtd', y='Tipo', orientation='h', title="Ranking de Ocorrências",
                                   color_discrete_sequence=azul_palette, template="plotly_white")
            st.plotly_chart(fig_bar_praia, use_container_width=True)
        
        qtd_tubarao = df_praia['subtipo_ocorrencia'].str.contains("Tubarão", case=False).sum()
        if qtd_tubarao > 0:
            st.error(f"ALERTA MÁXIMO: {qtd_tubarao} incidente(s) com Tubarão registrado(s)!")