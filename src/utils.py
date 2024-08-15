import pandas as pd

def format_values(value, filter_option):
    """
    Formata os valores de acordo com o tipo de filtro aplicado e o valor recebido.

    Parameters:
    value (float or int): O valor a ser formatado.
    filter_option (str): O filtro selecionado para determinar a formatação.

    Returns:
    str: Valor formatado como uma string.
    """
    if pd.isna(value):
        return "Dado indisponível"
    
    if isinstance(value, (int, float)):
        if filter_option in ["Top 10 Músicas Mais Tocadas no YouTube", "Top 10 Músicas Mais Tocadas no Spotify"]:
            if value >= 1e3:
                return f"{value:,.0f}"  # Formatação com separadores de milhar e sem casas decimais
            else:
                return f"{value:.1f}"  # Formatação com uma casa decimal
        else:
            if value >= 1e3:
                return f"{value:,.0f}"  # Formatação com separadores de milhar e sem casas decimais
            elif value >= 1:
                return f"{value:.2f}"  # Formatação com duas casas decimais
            else:
                return f"{value:.2f}"  # Formatação com duas casas decimais
    return value

def top_youtube_views(data):
    """
    Retorna o top 10 músicas com mais visualizações no YouTube.

    Parameters:
    data (pd.DataFrame): DataFrame com as colunas 'Track' e 'Views'.

    Returns:
    pd.DataFrame: DataFrame com as 10 músicas mais visualizadas.
    """
    return data[['Track', 'Views']].nlargest(10, 'Views')

def top_spotify_streams(data):
    """
    Retorna o top 10 músicas com mais streams no Spotify.

    Parameters:
    data (pd.DataFrame): DataFrame com as colunas 'Track' e 'Stream'.

    Returns:
    pd.DataFrame: DataFrame com as 10 músicas com mais streams.
    """
    return data[['Track', 'Stream']].nlargest(10, 'Stream')

def top_danceable_songs(data):
    """
    Retorna o top 10 músicas mais dançáveis.

    Parameters:
    data (pd.DataFrame): DataFrame com as colunas 'Track' e 'Danceability'.

    Returns:
    pd.DataFrame: DataFrame com as 10 músicas mais dançáveis.
    """
    return data[['Track', 'Danceability']].nlargest(10, 'Danceability')

def top_instrumental_songs(data):
    """
    Retorna o top 10 músicas mais instrumentais.

    Parameters:
    data (pd.DataFrame): DataFrame com as colunas 'Track' e 'Instrumentalness'.

    Returns:
    pd.DataFrame: DataFrame com as 10 músicas mais instrumentais.
    """
    return data[['Track', 'Instrumentalness']].nlargest(10, 'Instrumentalness')

def top_live_songs(data):
    """
    Retorna o top 10 músicas com plateia.

    Parameters:
    data (pd.DataFrame): DataFrame com as colunas 'Track' e 'Liveness'.

    Returns:
    pd.DataFrame: DataFrame com as 10 músicas com mais plateia.
    """
    return data[['Track', 'Liveness']].nlargest(10, 'Liveness')

def top_happy_songs(data):
    """
    Retorna o top 10 músicas mais felizes.

    Parameters:
    data (pd.DataFrame): DataFrame com as colunas 'Track' e 'Valence'.

    Returns:
    pd.DataFrame: DataFrame com as 10 músicas mais felizes.
    """
    return data[['Track', 'Valence']].nlargest(10, 'Valence')
