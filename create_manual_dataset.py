"""
Script helper para crear el dataset manual
Este script genera un ejemplo de dataset manual que puedes editar
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# Leer el dataset de Kaggle para obtener nombres de películas
kaggle_df = pd.read_csv('data/raw/IMDB_Top_250_Movies.csv')

# Seleccionar 75 películas aleatoriamente del top 100
top_movies = kaggle_df.head(100)['name'].tolist()
selected_movies = random.sample(top_movies, min(75, len(top_movies)))

# Usuarios
users = ['user_001', 'user_002', 'user_003', 'user_004']

# Plataformas de streaming
platforms = ['Netflix', 'Prime Video', 'HBO Max', 'Disney+']

# Generar datos
data = []

for i, movie in enumerate(selected_movies):
    # Asignar usuario de forma balanceada
    user = users[i % len(users)]

    # Datos aleatorios pero coherentes
    watched = random.choice([True, False])
    favorite = random.choice([True, False]) if watched else False

    # Rating personal (entre 6.0 y 10.0)
    personal_rating = round(random.uniform(6.0, 10.0), 1) if watched else None

    # Plataforma aleatoria
    platform = random.choice(platforms)

    # Fecha de visualización (últimos 12 meses)
    if watched:
        days_ago = random.randint(0, 365)
        watch_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    else:
        watch_date = None

    data.append({
        'user_id': user,
        'name': movie,
        'watched': watched,
        'favorite': favorite,
        'personal_rating': personal_rating,
        'platform': platform,
        'watch_date': watch_date
    })

# Crear DataFrame
manual_df = pd.DataFrame(data)

# Guardar
manual_df.to_csv('data/raw/dataset_manual_IMDB_Top250.csv', index=False)

print("✅ Dataset manual creado exitosamente!")
print(f"📊 Total de registros: {len(manual_df)}")
print(f"📁 Ubicación: data/raw/dataset_manual_IMDB_Top250.csv")
print("\nDistribución por usuario:")
print(manual_df['user_id'].value_counts())
print("\nDistribución por plataforma:")
print(manual_df['platform'].value_counts())
print("\nPrimeras filas:")
print(manual_df.head(10))

print("\n💡 Tip: Puedes editar este archivo CSV para personalizar los datos")
