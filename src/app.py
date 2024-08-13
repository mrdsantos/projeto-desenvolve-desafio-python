import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html
from utils import (
    top_danceable_songs,
    top_instrumental_songs,
    top_live_songs,
    top_happy_songs,
    top_longest_songs,
    top_shortest_songs,
    top_spotify_streams,
    top_youtube_views,
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
    return pd.read_csv("/workspaces/projeto-desenvolve-desafio-python/data/Spotify_Youtube.csv")


data = load_data()

# Configurando a barra lateral
st.sidebar.title("Song Library :musical_score:")
st.sidebar.header("Informações do Aluno")
st.sidebar.write("Maicon Rodrigues dos Santos")
st.sidebar.write(
    "[![Star](https://img.shields.io/github/stars/mrdsantos/projeto-desenvolve-desafio-python.svg?logo=github&style=social)](https://gitHub.com/mrdsantos/projeto-desenvolve-desafio-python)"
)
st.sidebar.write("PDBD026")

# Adicionando filtros
artist = st.sidebar.selectbox(
    "Escolha um artista", ["Todos os artistas"] + list(data["Artist"].unique())
)
filter_option = st.sidebar.selectbox(
    "Escolha um filtro",
    [
        "Top 10 Músicas Dançáveis",
        "Top 10 Músicas Instrumentais",
        "Top 10 Músicas com Plateia",
        "Top 10 Músicas Felizes",
        "Top 10 Músicas Mais Longas",
        "Top 10 Músicas Mais Curtas",
        "Top 10 Músicas Mais Tocadas no Spotify",
        "Top 10 Músicas Mais Tocadas no YouTube",
        "Músicas Calmas",
    ],
)

# Filtrando os dados com base na seleção
if artist != "Todos os artistas":
    dados_filtrados = data[data["Artist"] == artist]
else:
    dados_filtrados = data

# Aplicando o filtro selecionado
if filter_option == "Top 10 Músicas Dançáveis":
    fig = top_danceable_songs(dados_filtrados)
elif filter_option == "Top 10 Músicas Instrumentais":
    fig = top_instrumental_songs(dados_filtrados)
elif filter_option == "Top 10 Músicas com Plateia":
    fig = top_live_songs(dados_filtrados)
elif filter_option == "Top 10 Músicas Felizes":
    fig = top_happy_songs(dados_filtrados)
elif filter_option == "Top 10 Músicas Mais Longas":
    fig = top_longest_songs(dados_filtrados)
elif filter_option == "Top 10 Músicas Mais Curtas":
    fig = top_shortest_songs(dados_filtrados)
elif filter_option == "Top 10 Músicas Mais Tocadas no Spotify":
    fig = top_spotify_streams(dados_filtrados)
elif filter_option == "Top 10 Músicas Mais Tocadas no YouTube":
    fig = top_youtube_views(dados_filtrados)
elif filter_option == "Músicas Calmas":
    calm_songs = dados_filtrados[
        dados_filtrados["Energy"] < 0.3
    ]  # Ajuste o valor conforme necessário
    fig = px.bar(
        calm_songs.sort_values(by="Energy", ascending=True).head(10),
        x="Track",
        y="Energy",
        title="Top 10 Músicas Calmas",
    )

# Exibindo o gráfico
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader(":small_blue_diamond: Gráfico de Músicas")
    st.plotly_chart(fig)

    # Criando a tabela de músicas
    tabela_musicas = dados_filtrados.copy()
    tabela_musicas["Duração"] = tabela_musicas["Duration_ms"].apply(
        lambda ms: f"{ms // 60000:02}:{(ms % 60000) // 1000:02}"
    )
    tabela_musicas["Visualizações no YouTube"] = tabela_musicas["Views"].apply(
        lambda v: f"{v:,} visualizações"
    )
    tabela_musicas["Streams no Spotify"] = tabela_musicas["Stream"].apply(
        lambda s: f"{s:,} streams"
    )
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
        "Duration_ms": "Duração",
        "Stream": "Streams",
        "Views": "Visualizações",
        "Energy": "Energia",
    }

    # Ajustando o título da coluna baseada no filtro
    coluna_filtro = {
        "Top 10 Músicas Dançáveis": "Danceability",
        "Top 10 Músicas Instrumentais": "Instrumentalness",
        "Top 10 Músicas com Plateia": "Liveness",
        "Top 10 Músicas Felizes": "Valence",
        "Top 10 Músicas Mais Longas": "Duration_ms",
        "Top 10 Músicas Mais Curtas": "Duration_ms",
        "Top 10 Músicas Mais Tocadas no Spotify": "Stream",
        "Top 10 Músicas Mais Tocadas no YouTube": "Views",
        "Músicas Calmas": "Energy",
    }[filter_option]

    titulo_coluna = col_titles[coluna_filtro]

    # Ordenando e renomeando as colunas
    tabela_musicas = tabela_musicas.sort_values(by=coluna_filtro, ascending=False).head(
        10
    )
    tabela_musicas = tabela_musicas[
        [
            "Artist",
            "Track",
            coluna_filtro,
            "YouTube",
            "Spotify",
            "Visualizações no YouTube",
            "Streams no Spotify",
        ]
    ]
    tabela_musicas.columns = [
        "Artista",
        "Título",
        titulo_coluna,
        "YouTube",
        "Spotify",
        "Visualizações",
        "Streams",
    ]

    # Exibindo a tabela de músicas
    st.subheader(":small_blue_diamond: Tabela de Músicas:")
    st.markdown(
        tabela_musicas.to_html(escape=False, index=False), unsafe_allow_html=True
    )

# Definindo o CSS para as colunas


with col2:
    # Calcular a soma das visualizações no YouTube e streams no Spotify por artista
    data["Total"] = data["Views"] + data["Stream"]

    # Top 5 artistas mais tocados
    top_artists = data.groupby("Artist")["Total"].sum().nlargest(5).reset_index()
    top_artists.index += 1  # Ajusta o índice para começar em 1
    top_artists.index.name = "Rank"  # Define o nome da coluna de índice
    top_artists = top_artists.rename(
        columns={"Artist": "Artista", "Total": "Total de Visualizações e Streams"}
    )

    # Exibindo o card com os artistas mais tocados
    st.subheader(":small_blue_diamond: Top 5 Artistas Mais Tocados")
    st.write(top_artists)

    # Top 5 músicas mais tocadas com base no total de visualizações e streams
    top_songs_list = []
    added_songs = set()

    # Ordenar o DataFrame por total de visualizações e streams em ordem decrescente
    sorted_data = data.sort_values(by="Total", ascending=False)

    for index, row in sorted_data.iterrows():
        # Verificar se a música já foi adicionada
        if row["Track"] not in added_songs:
            # Adicionar a música à lista e ao conjunto
            top_songs_list.append(row)
            added_songs.add(row["Track"])

        # Parar quando tiver 5 músicas
        if len(top_songs_list) == 5:
            break

    # Converter a lista de músicas top 5 em um DataFrame
    top_songs = pd.DataFrame(top_songs_list, columns=["Track", "Artist", "Total"])
    top_songs.index += 1  # Ajusta o índice para começar em 1
    top_songs.index.name = "Rank"  # Define o nome da coluna de índice
    top_songs = top_songs.rename(
        columns={"Track": "Música", "Artist": "Artista", "Total": "Total"}
    )

    # Exibindo o card com as músicas mais tocadas
    st.subheader(":small_blue_diamond: Top 5 Músicas Mais Tocadas")
    st.write(top_songs)
