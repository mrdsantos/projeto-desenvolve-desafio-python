import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    top_danceable_songs,
    top_instrumental_songs,
    top_live_songs,
    top_happy_songs,
    top_spotify_streams,
    top_youtube_views,
    format_values,
)

# Configuração da página
st.set_page_config(
    page_title="Song Library",
    layout="wide",
    page_icon=":musical_score:",
    initial_sidebar_state="expanded",
)


# Função de cache para melhorar o desempenho
@st.cache_data
def load_data():
    return pd.read_csv("data/Spotify_Youtube.csv")


data = load_data()

# Configurando a barra lateral
st.sidebar.title("Song Library :musical_score:")
st.sidebar.write("Maicon Rodrigues dos Santos")
st.sidebar.write("PDBD026")
st.sidebar.subheader(
    "Song Library no GitHub [![Star](https://img.shields.io/github/stars/mrdsantos/projeto-desenvolve-desafio-python.svg?logo=github&style=social)](https://gitHub.com/mrdsantos/projeto-desenvolve-desafio-python)"
)

# Adicionando filtros
filter_option = st.sidebar.selectbox(
    "Escolha um filtro",
    [
        "Top 10 Músicas Mais Tocadas no YouTube",
        "Top 10 Músicas Mais Tocadas no Spotify",
        "Top 10 Músicas Mais Dançáveis",
        "Top 10 Músicas Mais Calmas",
        "Top 10 Músicas Mais Instrumentais",
        "Top 10 Músicas com Plateia",
    ],
)

# Dropdown para escolher o artista
artist_options = data["Artist"].unique()
selected_artist = st.sidebar.selectbox(
    "Escolha um Artista:", ["Todos"] + list(artist_options)
)

st.sidebar.write("Base de dados de 2023")

# Filtrando os dados com base na seleção
dados_filtrados = data.copy()

# Aplicando o filtro de artista
if selected_artist != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Artist"] == selected_artist]


# Função para criar gráfico de pizza
def create_pie_chart(df, names_col, values_col, title, labels):
    if names_col not in df.columns or values_col not in df.columns:
        st.error(f"Colunas esperadas '{names_col}' e '{values_col}' não encontradas.")
        return None
    return px.pie(df, names=names_col, values=values_col, title=title, labels=labels)


# Criando gráficos com base no filtro selecionado
if filter_option == "Top 10 Músicas Mais Tocadas no YouTube":
    top_youtube = top_youtube_views(dados_filtrados)
    fig = create_pie_chart(
        top_youtube,
        "Track",
        "Views",
        "Top 10 Músicas Mais Tocadas no YouTube",
        {"Views": "Visualizações", "Track": "Título"},
    )
elif filter_option == "Top 10 Músicas Mais Tocadas no Spotify":
    top_spotify = top_spotify_streams(dados_filtrados)
    fig = create_pie_chart(
        top_spotify,
        "Track",
        "Stream",
        "Top 10 Músicas Mais Tocadas no Spotify",
        {"Stream": "Streams", "Track": "Título"},
    )
elif filter_option == "Top 10 Músicas Mais Dançáveis":
    top_danceable = top_danceable_songs(dados_filtrados)
    fig = create_pie_chart(
        top_danceable,
        "Track",
        "Danceability",
        "Top 10 Músicas Mais Dançáveis",
        {"Danceability": "Dançabilidade", "Track": "Título"},
    )
elif filter_option == "Top 10 Músicas Mais Calmas":
    top_happy = top_happy_songs(dados_filtrados)
    fig = create_pie_chart(
        top_happy,
        "Track",
        "Valence",
        "Top 10 Músicas Mais Calmas",
        {"Valence": "Felicidade", "Track": "Título"},
    )
elif filter_option == "Top 10 Músicas Mais Instrumentais":
    top_instrumental = top_instrumental_songs(dados_filtrados)
    fig = create_pie_chart(
        top_instrumental,
        "Track",
        "Instrumentalness",
        "Top 10 Músicas Mais Instrumentais",
        {"Instrumentalness": "Instrumental", "Track": "Título"},
    )
elif filter_option == "Top 10 Músicas com Plateia":
    top_live = top_live_songs(dados_filtrados)
    fig = create_pie_chart(
        top_live,
        "Track",
        "Liveness",
        "Top 10 Músicas com Plateia",
        {"Liveness": "Plateia", "Track": "Título"},
    )

# Exibindo o gráfico
col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    st.subheader(":small_blue_diamond: Gráfico de Músicas")
    if fig is not None:
        st.plotly_chart(fig)

# Criando a tabela de músicas
tabela_musicas = dados_filtrados.copy()

# Adicionando as colunas de URL
tabela_musicas["YouTube"] = tabela_musicas["Url_youtube"].apply(
    lambda url: f'<a href="{url}" target="_blank">Link</a>'
)
tabela_musicas["Spotify"] = tabela_musicas["Url_spotify"].apply(
    lambda url: f'<a href="{url}" target="_blank">Link</a>'
)

# Mapeamento de títulos de coluna para exibição
col_titles = {
    "Danceability": "Dançabilidade",
    "Instrumentalness": "Instrumental",
    "Liveness": "Plateia",
    "Valence": "Felicidade",
    "Stream": "Streams",
    "Views": "Visualizações",
    "Energy": "Energia",
}

# Ajustando o título da coluna baseada no filtro
coluna_filtro = {
    "Top 10 Músicas Mais Tocadas no YouTube": "Views",
    "Top 10 Músicas Mais Tocadas no Spotify": "Stream",
    "Top 10 Músicas Mais Dançáveis": "Danceability",
    "Top 10 Músicas Mais Calmas": "Energy",
    "Top 10 Músicas Mais Instrumentais": "Instrumentalness",
    "Top 10 Músicas com Plateia": "Liveness",
}[filter_option]

titulo_coluna = col_titles[coluna_filtro]

# Ordenando e limitando o DataFrame
tabela_musicas = tabela_musicas.sort_values(by=coluna_filtro, ascending=False).head(10)

# Selecionando as colunas apropriadas
tabela_musicas = tabela_musicas[
    [
        "Artist",
        "Track",
        coluna_filtro,
        "YouTube",
        "Spotify",
    ]
]
tabela_musicas.columns = [
    "Artista",
    "Título",
    titulo_coluna,
    "YouTube",
    "Spotify",
]

# Aplicando a formatação na coluna filtrada
tabela_musicas[titulo_coluna] = tabela_musicas[titulo_coluna].apply(
    lambda x: format_values(x, filter_option)
)


# Ajuste para alinhar os títulos das colunas à esquerda e remover o índice
def style_table(df):
    return df.style.set_properties(**{"text-align": "left"}).hide(axis="index")


# Exibindo a Tabela de Resultados
st.subheader(":small_blue_diamond: Tabela de Músicas")

# Exibindo a tabela com estilos
st.markdown(
    style_table(tabela_musicas).to_html(escape=False, index=False),
    unsafe_allow_html=True,
)

with col2:
    # Adicionar coluna 'Total' para cálculo da soma de visualizações e streams
    data["Total"] = data["Views"] + data["Stream"]

    # Calcular o top 5 artistas mais tocados
    top_artists = (
        data.groupby("Artist")["Total"]
        .sum()
        .nlargest(5)
        .reset_index()
        .rename(columns={"Artist": "Artista", "Total": "Total de Exibições"})
    )
    top_artists.index += 1  # Ajusta o índice para começar em 1
    top_artists.index.name = "Rank"  # Define o nome da coluna de índice

    # Exibindo o card com os artistas mais tocados
    st.subheader(":small_blue_diamond: Top 5 Artistas Mais Tocados")
    st.write(top_artists)

    # Calcular o top 5 músicas mais tocadas
    top_songs = (
        data.sort_values(by="Total", ascending=False)
        .drop_duplicates(subset=["Track"])
        .head(5)
        .reset_index(drop=True)
        .rename(
            columns={
                "Track": "Música",
                "Artist": "Artista",
                "Total": "Total de Exibições",
            }
        )
    )
    top_songs.index += 1  # Ajusta o índice para começar em 1
    top_songs.index.name = "Rank"  # Define o nome da coluna de índice

    # Formatar a coluna 'Música' para ter no máximo 15 caracteres e adicionar "..." se necessário
    top_songs["Música"] = top_songs["Música"].apply(
        lambda x: x[:15] + "..." if len(x) > 15 else x
    )

    # Formatar a coluna 'Total de Exibições' para ser mais legível
    top_songs["Total de Exibições"] = top_songs["Total de Exibições"].apply(
        lambda x: f"{x:,.0f}"
    )

    # Selecionar e reordenar as colunas para exibição
    top_songs = top_songs[["Artista", "Música", "Total de Exibições"]]

    # Exibindo a tabela
    st.subheader(":small_blue_diamond: Top 5 Músicas Mais Tocadas")
    st.write(top_songs)
