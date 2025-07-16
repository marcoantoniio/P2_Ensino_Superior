<p align="center">
   <h1 align="center">Olá e bem-vindo! 👋</h1>
   <p align="center">
      Este é um <a href="https://p2-ensino-superior.streamlit.app/">dashboard</a> interativo desenvolvido no Streamlit para fazer análises das universidades e cursos da RIDE no ano de 2023.
   </p>
</p>

<br>

<p align="center">
   <h1 align="center">Descrição</h1>
   <p>
      Este dashboard foi feito para compor a nota da matéria Análise Exploratória de Dados e Visualização, do curso Ciência de Dados e Inteligência Artificial. O principal objetivo é entender mais a fundo como as universidades e os cursos da RIDE se comportaram no ano de 2023, analisando dados como: quantidade de pessoas do sexo masculino e feminino; faixa etária dos docentes; nível de escolaridade; quantidade de formados em cada curso; entre outros.
   </p>
</p>

<br>

<p align="center">
   <h1 align="center">Principais funcionalidades</h1>
   <ul>
     <li><b>Interface Interativa:</b> Apresenta uma interface intuitiva e responsiva, permitindo interação fluida com os gráficos e painéis em tempo real.</li>
     <li><b>Filtros Dinâmicos:</b> Filtros que permitem ajustar a visualização dos dados em tempo real conforme os critérios selecionados.</li>
     <li><b>Organização por Abas Temáticas:</b> Visualização facilitada com seções organizadas por categorias.</li>
   </ul>
</p>

<p align="center">
   <h1 align="center">Tecnologias Utilizadas</h1>
   <li><b>Python:</b></li>
   <ul>
      <li><b>Bibliotecas:</b> Streamlit, Pandas, Altair, Plotly, Geopandas, Shapely.</li>
   </ul>
   <li><b>Jupyter Notebook:</b> Análise e entendimento dos dados.</li>
   <li><b>PostgreSQL:</b> Armazenamento e gestão dos dados.</li>
</p>

<h1 align="center"> Como rodar o projeto na sua máquina </h1>

1. Clone o repositório
    ```
   $ git clone https://github.com/marcoantoniio/P2_Ensino_Superior.git
    ```

2. Crie um ambiente virtual dentro da pasta do repositório clonado
    ```
   $ python -m venv .venv
    ```
3. Entre no ambiente virtual
    ```
   $ source .venv/bin/activate
    ```
4. Instale o requirements

   ```
   $ pip install -r requirements.txt
   ```

5. Rode o aplicativo

   ```
   $ streamlit run streamlit_app.py
   ```
   O projeto foi desenvolvido para ser visualizado em monitores com resolução **1920x1080p (Full HD)**. Em resoluções diferentes, alguns elementos da interface podem não ser exibidos corretamente.
