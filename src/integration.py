"""
🔥 CRUCES de información entre MongoDB y Redis
Este archivo vale 30% de tu nota
"""

import pandas as pd
from config import get_mongo_connection, get_redis_connection


def cruce_1_top_movies_netflix():
    """
    CRUCE #1: Top películas disponibles en Netflix

    COMBINA:
    - MongoDB: Ratings de películas
    - Redis: Disponibilidad en Netflix

    GENERA: Top 10 películas mejor valoradas EN Netflix
    """
    print("\n🔀 CRUCE #1: Top Películas en Netflix")
    print("=" * 50)

    # Conectar a ambas BD
    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()

    if mongo_col is None or redis_client is None:
        return None

    # Obtener películas de Netflix (REDIS)
    netflix_movies = redis_client.smembers('platform:netflix')
    print(f"📺 Redis: {len(netflix_movies)} películas en Netflix")

    if len(netflix_movies) == 0:
        print("⚠️  No hay películas en Netflix. Asegúrate de crear el dataset manual con plataformas.")
        return None

    # Para cada película, obtener rating de MongoDB
    movies_with_ratings = []

    for title in netflix_movies:
        movie = mongo_col.find_one({"name": title})

        if movie and 'rating' in movie:
            movies_with_ratings.append({
                'name': movie['name'],
                'year': movie.get('year', 'N/A'),
                'rating': movie['rating'],
                'genre': movie.get('genre', 'N/A')
            })

    # Ordenar por rating
    movies_sorted = sorted(movies_with_ratings, key=lambda x: x['rating'], reverse=True)
    top_10 = movies_sorted[:10]

    # Mostrar resultados
    print("\n🏆 RESULTADO - Top 10 en Netflix:")
    for i, movie in enumerate(top_10, 1):
        print(f"{i:2}. {movie['name']} ({movie['year']}) - ⭐ {movie['rating']:.1f}")

    print(f"\n✅ CRUCE COMPLETADO")

    return pd.DataFrame(top_10)


def cruce_2_rating_comparison():
    """
    CRUCE #2: Comparación Rating IMDb vs Personal

    COMBINA:
    - MongoDB: Rating de IMDb
    - Dataset Manual: Rating personal

    GENERA: Análisis de diferencias entre ratings
    """
    print("\n🔀 CRUCE #2: Rating IMDb vs Personal")
    print("=" * 50)

    mongo_client, mongo_db, mongo_col = get_mongo_connection()

    if mongo_col is None:
        return None

    # Obtener películas con ambos ratings
    movies = mongo_col.find({
        "rating": {"$exists": True},
        "personal_rating": {"$exists": True}
    })

    data = []
    for movie in movies:
        if movie.get('rating') and movie.get('personal_rating'):
            data.append({
                'name': movie['name'],
                'imdb_rating': movie['rating'],
                'personal_rating': movie['personal_rating'],
                'difference': movie['personal_rating'] - movie['rating']
            })

    df = pd.DataFrame(data)

    if len(df) > 0:
        print(f"\n📊 Analizadas {len(df)} películas")
        print(f"Promedio IMDb: {df['imdb_rating'].mean():.2f}")
        print(f"Promedio Personal: {df['personal_rating'].mean():.2f}")

        # Películas donde tu rating es mayor
        overrated = df[df['difference'] > 0].nlargest(5, 'difference')
        if len(overrated) > 0:
            print(f"\n⬆️ Películas que valoras MÁS que IMDb:")
            for _, row in overrated.iterrows():
                print(f"  • {row['name']}: +{row['difference']:.1f}")

        # Películas donde tu rating es menor
        underrated = df[df['difference'] < 0].nsmallest(5, 'difference')
        if len(underrated) > 0:
            print(f"\n⬇️ Películas que valoras MENOS que IMDb:")
            for _, row in underrated.iterrows():
                print(f"  • {row['name']}: {row['difference']:.1f}")
    else:
        print("⚠️  No se encontraron películas con ratings personales")

    print(f"\n✅ CRUCE COMPLETADO")

    return df


def cruce_3_genres_by_platform():
    """
    CRUCE #3: Géneros más populares por plataforma

    COMBINA:
    - MongoDB: Géneros de películas
    - Redis: Plataformas

    GENERA: Distribución de géneros en cada plataforma
    """
    print("\n🔀 CRUCE #3: Géneros por Plataforma")
    print("=" * 50)

    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()

    if mongo_col is None or redis_client is None:
        return None

    results = {}
    platforms = ['netflix', 'prime_video', 'hbo_max', 'disney+']

    for platform in platforms:
        # Obtener películas de la plataforma (REDIS)
        platform_movies = redis_client.smembers(f'platform:{platform}')

        if len(platform_movies) == 0:
            continue

        # Para cada película, obtener género (MONGODB)
        genre_count = {}

        for title in platform_movies:
            movie = mongo_col.find_one({"name": title})

            if movie and 'genre' in movie:
                genres = movie['genre'].split(',') if isinstance(movie['genre'], str) else [movie['genre']]

                for genre in genres:
                    genre = genre.strip()
                    genre_count[genre] = genre_count.get(genre, 0) + 1

        # Top 5 géneros
        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
        results[platform.capitalize()] = sorted_genres[:5]

    # Mostrar resultados
    print("\n📊 RESULTADO - Géneros por Plataforma:")
    for platform, genres in results.items():
        if genres:
            print(f"\n{platform}:")
            for genre, count in genres:
                print(f"  • {genre}: {count} películas")

    if not results:
        print("⚠️  No se encontraron plataformas con películas")

    print(f"\n✅ CRUCE COMPLETADO")

    return results


def execute_all_cruces():
    """Ejecuta todos los cruces"""
    print("🔥 EJECUCIÓN DE TODOS LOS CRUCES")
    print("=" * 70)

    results = {}

    try:
        results['cruce_1'] = cruce_1_top_movies_netflix()
    except Exception as e:
        print(f"❌ Error en Cruce 1: {e}")

    try:
        results['cruce_2'] = cruce_2_rating_comparison()
    except Exception as e:
        print(f"❌ Error en Cruce 2: {e}")

    try:
        results['cruce_3'] = cruce_3_genres_by_platform()
    except Exception as e:
        print(f"❌ Error en Cruce 3: {e}")

    print("\n" + "=" * 70)
    print("🎉 CRUCES COMPLETADOS")
    print("=" * 70)

    return results


if __name__ == "__main__":
    execute_all_cruces()
