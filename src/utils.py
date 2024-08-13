import pandas as pd
import plotly.express as px

def top_danceable_songs(data):
    df = data.sort_values(by='Danceability', ascending=False).head(10)
    return px.bar(df, x='Track', y='Danceability', title='Top 10 Músicas Dançáveis')

def top_instrumental_songs(data):
    df = data[data['Instrumentalness'] > 0.5].sort_values(by='Instrumentalness', ascending=False).head(10)
    return px.bar(df, x='Track', y='Instrumentalness', title='Top 10 Músicas Instrumentais')

def top_live_songs(data):
    df = data[data['Liveness'] > 0.8].sort_values(by='Liveness', ascending=False).head(10)
    return px.bar(df, x='Track', y='Liveness', title='Top 10 Músicas com Plateia')

def top_happy_songs(data):
    df = data.sort_values(by='Valence', ascending=False).head(10)
    return px.bar(df, x='Track', y='Valence', title='Top 10 Músicas Felizes')

def top_longest_songs(data):
    df = data.sort_values(by='Duration_ms', ascending=False).head(10)
    df['Duration_min'] = df['Duration_ms'] / 60000
    return px.bar(df, x='Track', y='Duration_min', title='Top 10 Músicas Mais Longas')

def top_shortest_songs(data):
    df = data.sort_values(by='Duration_ms', ascending=True).head(10)
    df['Duration_min'] = df['Duration_ms'] / 60000
    return px.bar(df, x='Track', y='Duration_min', title='Top 10 Músicas Mais Curtas')

def top_spotify_streams(data):
    df = data.sort_values(by='Stream', ascending=False).head(10)
    return px.bar(df, x='Track', y='Stream', title='Top 10 Músicas Mais Tocadas no Spotify')

def top_youtube_views(data):
    df = data.sort_values(by='Views', ascending=False).head(10)
    return px.bar(df, x='Track', y='Views', title='Top 10 Músicas Mais Tocadas no YouTube')
