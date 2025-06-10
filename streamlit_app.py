import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(
    page_title='Análise dos dados do Ensino Superior',
    page_icon=':superhero:',
)

@st.cache_data
def get_data(path):
    DATA_FILENAME = Path(__file__).parent/path
    data_df = pd.read_csv(DATA_FILENAME)

    return data_df

df_faixa_etaria = get_data('data/tabela_doc_faixa_etaria.csv')
df_cor_raca = get_data('data/tabela_doc_cor_raca.csv')

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
else:
    df_faixa_etaria_filtrado = df_faixa_etaria

frequencia_faixa_etaria, frequencia_df_faixa_etaria = pegar_frequencias(
    df_faixa_etaria_filtrado,
    "FAIXA_ETARIA",
    "Faixa Etária",
    "Frequência"
)

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

    width=600,
    height=400
).interactive()

st.altair_chart(faixa_etaria_barra, use_container_width=True)

