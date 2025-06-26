import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(
    page_title='Análise dos dados do ensino superior do Brasil',
    page_icon=':male-detective:',
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
df_escolaridade = get_data('data/tabela_doc_escol.csv')
df_tprede = get_data('data/tabela_tp_rede.csv')
df_acesso_internet = get_data('data/tabela_acesso_internet.csv')
df_repositorio_inst = get_data('data/tabela_repositorio_inst.csv')
df_repo = get_data('data/tabela_uf.csv')
df_uf = get_data('data/tabela_uf.csv')
df_turnos = get_data('data/qtd_total_vaga.csv')
df_concluintes = get_data('data/qtd_total_concluintes.csv')

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
# Análise dos dados do ensino superior do Brasil :bar_chart:

A educação é a base para a formação de bons profissionais. 
Com isso em mente, este dashboard tem como objetivo analisar os dados das universidades e 
cursos que integram a Região Integrada de Desenvolvimento do Distrito Federal e Entorno (RIDE).
'''

''
''
#TO DO: Filtro por cor e raca
#TO DO: Filtro por nível de escolaridade
with st.sidebar:
    st.header("Filtros Gerais")
    ufs = st.multiselect("Unidades Federativas que Integram o RIDE:", 
                       options=sorted(df_faixa_etaria['UF'].unique()),
                       placeholder="Escolha mútiplas UF")     
    if ufs:
        df_faixa_etaria_filtrado = df_faixa_etaria[df_faixa_etaria["UF"].isin(ufs)]
        df_cor_raca_filtrado = df_cor_raca[df_cor_raca["UF"].isin(ufs)]
        df_sexo_filtrado = df_sexo[df_sexo["UF"].isin(ufs)]
        df_escol_filtrado = df_escolaridade[df_escolaridade["UF"].isin(ufs)]
        df_tprede_filtrado = df_tprede[df_tprede["UF"].isin(ufs)]
        df_acesso_internet_filtrado = df_acesso_internet[df_acesso_internet["UF"].isin(ufs)]
        df_repositorio_inst_filtrado = df_repositorio_inst[df_repositorio_inst["UF"].isin(ufs)]
        df_uf_filtrado = df_uf[df_uf["UF"].isin(ufs)]
        df_turnos_filtrado = df_turnos[df_turnos["UF"].isin(ufs)]
        df_concluintes_filtrado = df_concluintes[df_concluintes["UF"].isin(ufs)]

    else:
        df_faixa_etaria_filtrado = df_faixa_etaria
        df_cor_raca_filtrado = df_cor_raca
        df_sexo_filtrado = df_sexo
        df_escol_filtrado = df_escolaridade
        df_tprede_filtrado = df_tprede
        df_acesso_internet_filtrado = df_acesso_internet
        df_repositorio_inst_filtrado = df_repositorio_inst
        df_uf_filtrado = df_uf
        df_turnos_filtrado = df_turnos
        df_concluintes_filtrado = df_concluintes

    ies = st.multiselect("Instituições de Ensino Superior:",
                         options=sorted(df_faixa_etaria_filtrado["NO_IES"].unique()),
                         placeholder="Escolha mútiplas IES")
    if ies:
        df_faixa_etaria_filtrado = df_faixa_etaria[df_faixa_etaria["NO_IES"].isin(ies)]
        df_cor_raca_filtrado = df_cor_raca[df_cor_raca["NO_IES"].isin(ies)]
        df_sexo_filtrado = df_sexo[df_sexo["NO_IES"].isin(ies)]
        df_escol_filtrado = df_escolaridade[df_escolaridade["NO_IES"].isin(ies)]
        df_acesso_internet_filtrado = df_acesso_internet[df_acesso_internet["NO_IES"].isin(ies)]
        df_tprede_filtrado = df_tprede[df_tprede["NO_IES"].isin(ies)]
        df_repositorio_inst_filtrado = df_repositorio_inst[df_repositorio_inst["NO_IES"].isin(ies)]
        df_turnos_filtrado = df_turnos[df_turnos["NO_IES"].isin(ies)]
        df_uf_filtrado = df_uf[df_uf["NO_IES"].isin(ies)]
        df_concluintes_filtrado = df_concluintes[df_concluintes["NO_IES"].isin(ies)]

    st.markdown("---")
    st.subheader("Filtro por Número de Concluintes")

    contagens = df_concluintes_filtrado['CURSO'].value_counts()
    if not contagens.empty:
        min_concluintes = int(contagens.min())
        max_concluintes = int(contagens.max())
        cursos_qtd_selecionada = st.slider(
            "Filtre cursos pelo nº de concluintes:",
            min_value=min_concluintes,
            max_value=max_concluintes,
            value=(min_concluintes, max_concluintes)
        )
        cursos_para_manter = contagens[
            (contagens >= cursos_qtd_selecionada[0]) & (contagens <= cursos_qtd_selecionada[1])
        ].index
        df_concluintes_filtrado = df_concluintes_filtrado[
            df_concluintes_filtrado['CURSO'].isin(cursos_para_manter)
        ]
    cor_raca_conc = st.multiselect(
        "Cor e Raça",
        options=sorted(df_concluintes["RAÇA"].unique()),
        placeholder="Escolha múltiplas Cores e Raças")
    if cor_raca_conc:
        df_concluintes_filtrado = df_concluintes_filtrado[df_concluintes_filtrado['RAÇA'].isin(cor_raca_conc)]

    st.markdown("---")
    st.markdown("Filtro por Frequência de Vagas")

    contagens_turnos = df_turnos_filtrado["CURSO"].value_counts()
    if not contagens_turnos.empty:
        min_freq = int(contagens_turnos.min())
        max_freq = int(contagens_turnos.max())
        freq_selecionada = st.slider(
            "Filtrar cursos pela frequência de turnos/ofertas:",
            min_value=min_freq,
            max_value=max_freq,
            value=(min_freq, max_freq)
        )
        cursos_para_manter = contagens_turnos[
            (contagens_turnos >= freq_selecionada[0]) & (contagens_turnos <= freq_selecionada[1])
        ].index
        df_turnos_filtrado = df_turnos_filtrado[
            df_turnos_filtrado['CURSO'].isin(cursos_para_manter)
        ]
    turnos_opt = st.multiselect(
        "Turnos",
        options=sorted(df_turnos["TURNO"].unique()),
        placeholder="Escolha mútiplos turnos"
    )
    if turnos_opt:
        df_turnos_filtrado = df_turnos[df_turnos["TURNO"].isin(turnos_opt)]

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

frequencia_escol, frequencia_df_escol = pegar_frequencias(
    df_escol_filtrado,
    "ESCOLARIDADE",
    "Escolaridade",
    "Frequência"
)

frequencia_tprede, frequencia_df_tprede = pegar_frequencias(
    df_tprede_filtrado,
    "TP_REDE",
    "Tipo de rede",
    "Frequência"
)

frequencia_acesso_internet, frequencia_df_acesso_internet = pegar_frequencias(
    df_acesso_internet_filtrado,
    "IN_SERVICO_INTERNET",
    "Acesso a Internet",
    "Frequência"
)

frequencia_repositorio, frequencia_df_repositorio = pegar_frequencias(
    df_repositorio_inst_filtrado,
    "IN_REPOSITORIO_INSTITUCIONAL",
    "Repositório Acadêmico",
    "Frequência"
)

frequencia_uf, frequencia_df_uf = pegar_frequencias(
    df_uf_filtrado,
    "UF",
    "Unidade Federativa",
    "Frequência"
)

frequencia_turnos, frequencia_df_turnos = pegar_frequencias(
    df_turnos_filtrado,
    "TURNO",
    "Turno",
    "Frequência"
)

frequencia_turno_cursos, frequencia_df_turno_cursos = pegar_frequencias(
    df_turnos_filtrado,
    "CURSO",
    "Curso",
    "Frequência"
)

frequencia_concluintes, frequencia_df_concluintes = pegar_frequencias(
    df_concluintes_filtrado,
    "CURSO",
    "Curso",
    "Frequência"
)

frequencia_raca_conc, frequencia_df_raca_conc = pegar_frequencias(
    df_concluintes_filtrado,
    "RAÇA",
    "Raça",
    "Frequência"
)

frequencia_df_sexo['Percentual'] = frequencia_df_sexo['Frequência'] / frequencia_df_sexo['Frequência'].sum() * 100
frequencia_df_sexo['Percentual_str'] = frequencia_df_sexo['Percentual'].map(lambda x: f"{x:.1f}%")

frequencia_df_uf['Percentual'] = frequencia_df_uf['Frequência'] / frequencia_df_uf['Frequência'].sum() * 100
frequencia_df_uf['Percentual_str'] = frequencia_df_uf['Percentual'].map(lambda x: f"{x:.1f}%")

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
).interactive().configure_axisY(
    labelFontSize=15
).configure_axisX(
    labelFontSize=15
)

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
).interactive().configure_axisY(
    labelFontSize=20
).configure_axisX(
    labelFontSize=13
)

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
    radius=120, size=14, fontWeight="bold", color="white"
).encode(
    theta=alt.Theta(field="Frequência", type="quantitative", stack="center"),
    text='Percentual_str:N',
    order=alt.Order('Frequência', sort='descending')
)

sexo_pizza = (sexo_barra + 
              texto_central + 
              texto_fatia)


barra_escolaridade = alt.Chart(frequencia_df_escol).mark_bar(orient="vertical").encode(
    x=alt.X("Escolaridade", sort="-y", axis=alt.Axis(labelAngle=45)),
    y=alt.Y("Frequência"),
    tooltip=["Escolaridade", "Frequência"],
    color=alt.Color("Escolaridade", legend=None)
).properties(
    title=alt.TitleParams(
        text="Nivel de escolaridade dos docentes",
        anchor="middle",
        fontSize=20
    ),
    height=400
).interactive().configure_axisY(
    labelFontSize=20
).configure_axisX(
    labelFontSize=15
)

barra_tprede = alt.Chart(frequencia_df_tprede).mark_bar(orient="vertical").encode(
    x=alt.X("Tipo de rede", sort='-y', axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Frequência"),
    tooltip=["Tipo de rede", "Frequência"],
    color=alt.Color("Tipo de rede", legend=None)
).properties(
    title=alt.TitleParams("Tipos de rede",
        anchor="middle",
        fontSize=20
    ),
    width=900,
    height=500
).configure_axisX(
    labelFontSize=15
).configure_axisY(
    labelFontSize=20
)

barra_acesso_internet = alt.Chart(frequencia_df_acesso_internet).mark_bar(orient="horizontal").encode(
    x=alt.X("Frequência"),
    y=alt.Y("Acesso a Internet", sort='-y'),
    tooltip=["Frequência", "Acesso a Internet"],
    color=alt.Color("Acesso a Internet", legend=None)
).properties(
    title=alt.TitleParams("Universidades com acesso a internet",
            anchor="middle")
).configure_axisX(
    labelFontSize=15
).configure_axisY(
    labelFontSize=12
)

barra_repositorio = alt.Chart(frequencia_df_repositorio).mark_bar(orient="horizontal").encode(
    x=alt.X("Frequência"),
    y=alt.Y("Repositório Acadêmico", sort="-y"),
    tooltip=["Frequência", "Repositório Acadêmico"],
    color=alt.Color("Repositório Acadêmico", legend=None)
).properties(
    title=alt.TitleParams("Universidades no repositorio",
                          anchor="middle")
).configure_axisX(
    labelFontSize=15
).configure_axisY(
    labelFontSize=12
)


pizza_uf = alt.Chart(frequencia_df_uf).mark_arc(innerRadius=100).encode(
    theta=alt.Theta(field="Frequência", type="quantitative"),
    color=alt.Color(field="Unidade Federativa", type="nominal", scale=alt.Scale(
        domain=["DF", "GO", "MG"],
        range=['#4c78a8', '#f58518', '#e45756']))
).properties(
    title=alt.TitleParams("Universidades por Unidade Federativa",
                          anchor="middle")
)

texto_central_uf = alt.Chart(frequencia_df_uf).mark_text(
    text=f'{frequencia_df_uf["Frequência"].sum()}',
    fontSize=50,
    fontWeight='bold',
    color='white'
).encode()

texto_fatia_uf = alt.Chart(frequencia_df_uf).mark_text(
    radius=120, size=14, fontWeight="bold", color="white"
).encode(
    theta=alt.Theta(field="Frequência", type="quantitative", stack="center"),
    text='Percentual_str:N',
    order=alt.Order('Frequência', sort='descending')
)

grafico_final_uf = (pizza_uf 
                    + texto_central_uf 
                    + texto_fatia_uf)

vagas_barra = alt.Chart(frequencia_df_turnos).mark_bar(orient="horizontal").encode(
    x=alt.X("Frequência"),
    y=alt.Y("Turno", sort="-x"),
    tooltip=["Frequência", "Turno"],
    color=alt.Color("Turno", legend=None)
)

concluintes_bar = alt.Chart(frequencia_df_concluintes).mark_bar(orient="vertical").encode(
    x=alt.X("Curso", sort="-y", axis=alt.Axis(labelAngle=45)),
    y=alt.Y("Frequência"),
    tooltip=["Curso", "Frequência"],
    color=alt.Color("Curso", legend=None)
).properties(
    title=alt.TitleParams("Total de concluintes por curso",
                          anchor="middle")
).configure_axisX(
    labelFontSize=15
).configure_axisY(
    labelFontSize=15
)

concluintes_cor_raca_bar = alt.Chart(frequencia_df_raca_conc).mark_bar(orient="horizontal").encode(
    x=alt.X("Frequência"),
    y=alt.Y("Raça", sort="-x"),
    tooltip=["Raça", "Frequência"],
    color=alt.Color("Raça", legend=None)
).properties(
    title=alt.TitleParams("Total de concluintes por cor e raça",
                          anchor="middle")
).configure_axisX(
    labelFontSize=15
).configure_axisY(
    labelFontSize=12
)

turnos_bar = alt.Chart(frequencia_df_turnos).mark_bar(orient="horizontal").encode(
    x=alt.X("Frequência"),
    y=alt.Y("Turno", sort="-x"),
    tooltip=["Frequência", "Turno"],
    color=alt.Color("Turno", legend=None)
).properties(
    title=alt.TitleParams("Total de vagas disponíveis por turno",
                          anchor="middle")
).configure_axisX(
    labelFontSize=15
).configure_axisY(
    labelFontSize=12
)

turnos_cursos_bar = alt.Chart(frequencia_df_turno_cursos).mark_bar(orient="vertical").encode(
    x=alt.X("Curso", sort="-y", axis=alt.Axis(labelAngle=45)),
    y=alt.Y("Frequência"),
    tooltip=["Curso", "Frequência"],
    color=alt.Color("Curso", legend=None)
).properties(
    title=alt.TitleParams("Total de vagas disponíveis por curso",
                          anchor="middle")
).configure_axisX(
    labelFontSize=15
).configure_axisY(
    labelFontSize=15
)

aba1, aba2, aba3, aba4 = st.tabs(["Docentes", "Redes", "Concluintes", "Vagas"])

with aba1:
    col_esquerda, col_direita = st.columns([1, 2], gap="large")
    with col_esquerda:
        st.altair_chart(sexo_pizza, use_container_width=True)
        st.markdown("---")
        st.altair_chart(barra_escolaridade, use_container_width=True)
        
        
    with col_direita:
        st.altair_chart(faixa_etaria_barra, use_container_width=True)

    st.altair_chart(cor_raca_barra, use_container_width=True)
    
with aba2:
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.altair_chart(barra_acesso_internet, use_container_width=True)
        st.altair_chart(barra_tprede, use_container_width=True)

    with col2:
        st.altair_chart(grafico_final_uf)
        
    with col3:
        st.altair_chart(barra_repositorio, use_container_width=True)

with aba3:
    colun1, colun2 = st.columns(2, gap="large")
    with colun1:
        st.altair_chart(concluintes_cor_raca_bar, use_container_width=True)
    st.altair_chart(concluintes_bar, use_container_width=True)

with aba4:
    coluna1, coluna2 = st.columns(2, gap="large")
    with coluna1:
        st.altair_chart(turnos_bar, use_container_width=True)
    st.altair_chart(turnos_cursos_bar, use_container_width=True)
    


#TO DO: heatmap do tipo de rede e acesso a internet
#TO DO: scatter plot com docentes, cor e raca e escolaridade