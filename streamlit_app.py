import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(
    page_title='Análise dos dados do Ensino Superior',
    page_icon=':bar_chart:',
    layout='wide'
)

@st.cache_data
def get_data(path):
    DATA_FILENAME = Path(__file__).parent/path
    data_df = pd.read_csv(DATA_FILENAME)

    return data_df

df_faixa_etaria = get_data('data/tabela_doc_faixa_etaria.csv')
df_cor_raca = get_data('data/tabela_doc_cor_raca.csv')
df_sexo = get_data('data/tabela_doc_sexo.csv')

def pegar_frequencias(
    df: pd.DataFrame,
    coluna: str,
    nome_coluna_1: str,
    nome_coluna_2: str
) -> tuple[pd.Series, pd.DataFrame]:
    """
    Calcula a frequência dos valores de uma coluna em um DataFrame, 
    cria um DataFrame com índice resetado e renomeia as colunas.

    Parâmetros:
    - df: DataFrame onde a coluna está presente.
    - coluna: Nome da coluna para calcular a frequência.
    - nome_coluna_1: Nome para a primeira coluna do DataFrame de resultado (ex: categorias).
    - nome_coluna_2: Nome para a segunda coluna do DataFrame de resultado (ex: frequências).

    Retorna:
    - frequencia_total: Série com a frequência dos valores (ordenada pelo índice).
    - frequencia_index: DataFrame com índice resetado e colunas renomeadas.
    """

    frequencia_total = df[coluna].value_counts().sort_index()
    frequencia_index = frequencia_total.reset_index()
    frequencia_index.columns = [nome_coluna_1, nome_coluna_2]

    return frequencia_total, frequencia_index

'''
# Análise dos dados do ensino superior

texto de apresentação
'''

''
''

with st.sidebar:
    st.header("Filtros")
    st.subheader("Teste")
    ufs = st.multiselect("Selecione uma UF:", 
                       options=df_faixa_etaria['UF'].unique(),
                       placeholder="Escolha uma ou mútiplas UF",
                       default=df_faixa_etaria["UF"].unique())

if ufs:
    df_faixa_etaria_filtrado = df_faixa_etaria[df_faixa_etaria["UF"].isin(ufs)]
    df_cor_raca_filtrado = df_cor_raca[df_cor_raca["UF"].isin(ufs)]
    df_sexo_filtrado = df_sexo[df_sexo["UF"].isin(ufs)]
else:
    df_faixa_etaria_filtrado = df_faixa_etaria
    df_cor_raca_filtrado = df_cor_raca
    df_sexo_filtrado = df_sexo

frequencia_faixa_etaria, frequencia_df_faixa_etaria = pegar_frequencias(
    df_faixa_etaria_filtrado,
    "FAIXA_ETARIA",
    "Faixa Etária",
    "Frequência"
)

frequencia_cor_raca, frequencia_df_cor_raca = pegar_frequencias(
    df_cor_raca_filtrado,
    "FAIXA_ETARIA",
    "Cor_Raca",
    "Frequência"
    )

frequencia_sexo, frequencia_df_sexo = pegar_frequencias(
    df_sexo_filtrado,
    "SEXO",
    "Sexo",
    "Frequência"
)

frequencia_df_sexo['Percentual'] = frequencia_df_sexo['Frequência'] / frequencia_df_sexo['Frequência'].sum() * 100
frequencia_df_sexo['Percentual_str'] = frequencia_df_sexo['Percentual'].map(lambda x: f"{x:.1f}%")

faixa_etaria_barra = alt.Chart(frequencia_df_faixa_etaria).mark_bar(orient='horizontal').encode(
    x=alt.X("Frequência"),
    y=alt.Y("Faixa Etária", sort='-x'),
    tooltip=["Faixa Etária", "Frequência"],
    color=alt.Color("Faixa Etária", legend=None),
).properties(
    title=alt.TitleParams(
        text="Distribuição de Docentes por Faixa Etária",
        anchor='middle',
        fontSize=20
    ),
    height=835
).interactive()

cor_raca_barra = alt.Chart(frequencia_df_cor_raca).mark_bar(orient='vertical').encode(
    x=alt.X("Cor_Raca", sort='-y', axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Frequência"),
    tooltip=["Cor_Raca", "Frequência"],
    color=alt.Color("Cor_Raca", legend=None)
).properties(
    title=alt.TitleParams(
        text="Distribuição de Docentes por Cor e Raça",
        anchor='middle',
        fontSize=20
    ),

    width=600,
    height=400
).interactive()

sexo_barra=alt.Chart(frequencia_df_sexo).mark_arc(innerRadius=100).encode(
    theta=alt.Theta(field="Frequência", type="quantitative"),
    color=alt.Color(field="Sexo", type="nominal", scale=alt.Scale(
        domain=["FEM", "MASC"],
        range=["#ff69b4", "#1f77b4"]
    )),
    tooltip=["Sexo", "Frequência"]
).properties(
    title=alt.TitleParams(
        text="Distribuição de Docentes por Sexo",
        anchor='middle',
        fontSize=20,
    ),

).interactive()

texto_central = alt.Chart(frequencia_df_sexo).mark_text(
    text=f'{frequencia_df_sexo["Frequência"].sum()}', 
    fontSize=50,
    fontWeight='bold',
    color='white'
).encode()

texto_fatia = alt.Chart(frequencia_df_sexo).mark_text(
    radius=120, size=13, fontWeight="bold", color="white"
).encode(
    theta=alt.Theta(field="Frequência", type="quantitative", stack="center"),
    text='Percentual_str:N',
    order=alt.Order('Frequência', sort='descending')
)

sexo_pizza = sexo_barra + texto_central + texto_fatia


col_esquerda, col_direita = st.columns([1, 2], gap="large")

with col_esquerda:
    st.altair_chart(sexo_pizza, use_container_width=True)
    st.markdown("---")
    st.altair_chart(cor_raca_barra, use_container_width=True)
    
with col_direita:
    st.altair_chart(faixa_etaria_barra, use_container_width=True)
    