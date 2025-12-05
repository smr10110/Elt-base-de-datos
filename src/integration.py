"""
🔥 CRUCES de información entre MongoDB y Redis
Este archivo vale 30% de tu nota - Optimizado para métricas profesionales
Actualizado para trabajar con redis_streaming_metrics.csv
"""

import pandas as pd
from config import get_mongo_connection, get_redis_connection


def cruce_1_top_movies_netflix():
    """CRUCE #1: Top 10 titulos por engagement usando views_30d."""
    print("\n[CRUCE #1] Top titulos (views_30d) IMDb vs Engagement")
    print("=" * 70)

    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()

    if mongo_col is None or redis_client is None:
        print("[ERROR] No se pudo conectar a las bases de datos")
        return None

    top_views = redis_client.zrevrange('views:30d', 0, 49, withscores=True)
    if not top_views:
        print("[WARN] No hay datos en Redis para views:30d")
        return None

    movies_data = []
    for title, views_30d in top_views:
        mongo_movie = mongo_col.find_one({"name": title})
        if not mongo_movie or 'rating' not in mongo_movie:
            continue

        redis_data = redis_client.hgetall(f"content:{title.replace(' ', '_')}")
        completion_30d = int(float(redis_data.get('completion_watches_30d', 0))) if redis_data else 0
        watchlist_30d = int(float(redis_data.get('watchlist_adds_30d', 0))) if redis_data else 0

        if views_30d > 0:
            completion_rate = (completion_30d / views_30d) * 100
            user_rating = (completion_rate / 100) * 10
        else:
            completion_rate = 0
            user_rating = 0

        movies_data.append({
            'name': mongo_movie['name'],
            'year': mongo_movie.get('year', 'N/A'),
            'imdb_rating': mongo_movie['rating'],
            'user_rating': user_rating,
            'views': int(views_30d),
            'completion_rate': completion_rate,
            'watchlist': watchlist_30d,
            'genre': mongo_movie.get('genre', 'N/A'),
            'difference': user_rating - mongo_movie['rating']
        })

    if not movies_data:
        print("[WARN] No se pudieron cruzar datos entre Mongo y Redis")
        return None

    movies_sorted = sorted(movies_data, key=lambda x: x['imdb_rating'], reverse=True)
    top_10 = movies_sorted[:10]

    print("\n[RESULT] Top 10 (ordenado por rating IMDb):")
    print("-" * 70)
    for i, movie in enumerate(top_10, 1):
        diff_symbol = "+" if movie['difference'] > 0 else ""
        print(f"{i:2}. {movie['name']}")
        print(f"    IMDb: {movie['imdb_rating']:.1f} | Engagement: {movie['user_rating']:.1f} | Diff: {diff_symbol}{movie['difference']:.1f}")
        print(f"    Vistas: {movie['views']:,} | Completion: {movie['completion_rate']:.1f}% | Watchlist: {movie['watchlist']:,}")

    df = pd.DataFrame(top_10)
    print("\nEstadisticas:")
    print(f"   Promedio IMDb: {df['imdb_rating'].mean():.2f}")
    print(f"   Promedio Engagement: {df['user_rating'].mean():.2f}")
    print(f"   Diferencia promedio: {df['difference'].mean():.2f}")
    print(f"   Completion rate promedio: {df['completion_rate'].mean():.1f}%")

    print("\nCRUCE #1 COMPLETADO")

    return df

def cruce_2_trending_by_genre():
    """
    CRUCE #2: Análisis de películas trending por género

    COMBINA:
    - Redis: Trending velocity (métricas calculadas)
    - MongoDB: Género de cada película
    - Redis: Visualizaciones de usuarios

    GENERA: ¿Qué géneros están creciendo más rápido?
    """
    print("\n🔀 CRUCE #2: Géneros Trending (velocidad de crecimiento)")
    print("=" * 70)

    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()

    if mongo_col is None or redis_client is None:
        print("❌ Error: No se pudo conectar a las bases de datos")
        return None

    # 1. Obtener películas con trending velocity > 1.0 (creciendo)
    trending_movies_data = redis_client.zrangebyscore(
        'analytics:trending_velocity',
        1.0,  # Mínimo: crecimiento sostenido
        '+inf',  # Sin límite superior
        withscores=True
    )

    print(f"🔥 Redis: {len(trending_movies_data)} películas con crecimiento (velocity > 1.0)")

    if len(trending_movies_data) == 0:
        print("⚠️  No hay películas trending en Redis")
        return None

    # 2. Para cada película trending, obtener género y vistas
    genre_data = {}

    for title, velocity in trending_movies_data:
        # Obtener género desde MongoDB
        mongo_movie = mongo_col.find_one({"name": title})

        if not mongo_movie or 'genre' not in mongo_movie:
            continue

        # Obtener vistas desde Redis
        movie_key = f"content:{title.replace(' ', '_')}"
        redis_data = redis_client.hgetall(movie_key)

        if not redis_data:
            continue

        views_30d = int(redis_data.get('views_30d', 0))
        views_7d = int(redis_data.get('views_7d', 0))

        # Procesar géneros (pueden ser múltiples separados por coma)
        genres = mongo_movie['genre'].split(',') if isinstance(mongo_movie['genre'], str) else [mongo_movie['genre']]

        for genre in genres:
            genre = genre.strip()
            if genre not in genre_data:
                genre_data[genre] = {
                    'count': 0,
                    'total_views': 0,
                    'total_velocity': 0,
                    'movies': []
                }

            genre_data[genre]['count'] += 1
            genre_data[genre]['total_views'] += views_30d
            genre_data[genre]['total_velocity'] += velocity
            genre_data[genre]['movies'].append({
                'title': title,
                'views_30d': views_30d,
                'views_7d': views_7d,
                'velocity': velocity,
                'rating': mongo_movie.get('rating', 0)
            })

    # 3. Ordenar géneros por velocidad promedio (no solo cantidad)
    sorted_genres = sorted(
        genre_data.items(),
        key=lambda x: x[1]['total_velocity'] / x[1]['count'] if x[1]['count'] > 0 else 0,
        reverse=True
    )

    # 4. Mostrar resultados
    print("\n📊 RESULTADO - Géneros con mayor trending velocity:")
    print("-" * 70)

    results_data = []
    for i, (genre, data) in enumerate(sorted_genres[:10], 1):
        avg_views = data['total_views'] / data['count'] if data['count'] > 0 else 0
        avg_velocity = data['total_velocity'] / data['count'] if data['count'] > 0 else 0

        print(f"{i:2}. {genre}")
        print(f"    Películas: {data['count']} | Velocity promedio: {avg_velocity:.2f}x")
        print(f"    Vistas totales: {data['total_views']:,} | Promedio: {avg_views:,.0f}")

        # Mostrar top 2 películas de ese género (por velocity)
        top_movies = sorted(data['movies'], key=lambda x: x['velocity'], reverse=True)[:2]
        for movie in top_movies:
            print(f"       • {movie['title']}: {movie['velocity']:.2f}x velocity ({movie['views_30d']:,} vistas)")

        results_data.append({
            'genre': genre,
            'count': data['count'],
            'total_views': data['total_views'],
            'avg_views': avg_views,
            'avg_velocity': avg_velocity
        })

    df = pd.DataFrame(results_data)

    print(f"\n✅ CRUCE #2 COMPLETADO")

    return df


def cruce_3_classics_latam():
    """
    CRUCE #3: Peliculas clasicas populares en LATAM

    COMBINA:
    - Redis: Rankings por region (region:latam:views ZSET)
    - MongoDB: Ano de estreno, genero, director
    - Redis: Metricas de engagement (watchlist, social)

    GENERA: Clasicos (pre-2000) que usuarios de LATAM estan viendo
    """
    print("\n[CRUCE #3] Clasicos en LATAM (engagement de usuarios)")
    print("=" * 70)

    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()

    if mongo_col is None or redis_client is None:
        print("[ERROR] No se pudo conectar a las bases de datos")
        return None

    latam_movies_data = redis_client.zrevrange('region:latam:views', 0, -1, withscores=True)
    print(f"[INFO] Redis: {len(latam_movies_data)} peliculas rankeadas en LATAM")

    if len(latam_movies_data) == 0:
        print("[WARN] No hay peliculas en LATAM en Redis")
        return None

    classics_data = []

    for title, latam_views in latam_movies_data:
        mongo_movie = mongo_col.find_one({"name": title})
        if not mongo_movie:
            continue

        year = mongo_movie.get('year', 0)
        if not year or year >= 2000:
            continue

        movie_key = f"content:{title.replace(' ', '_')}"
        redis_data = redis_client.hgetall(movie_key)
        if not redis_data:
            continue

        platform = redis_data.get('platform', 'N/A')
        views_30d = int(redis_data.get('views_30d', 0))
        watchlist_30d = int(redis_data.get('watchlist_adds_30d', 0))
        social_30d = int(redis_data.get('social_shares_30d', 0))
        completion_30d = int(redis_data.get('completion_watches_30d', 0))

        if views_30d > 0:
            completion_rate = (completion_30d / views_30d) * 100
            user_rating = (completion_rate / 100) * 10
        else:
            user_rating = 0

        classics_data.append({
            'name': mongo_movie['name'],
            'year': year,
            'genre': mongo_movie.get('genre', 'N/A'),
            'director': mongo_movie.get('directors', 'N/A'),
            'imdb_rating': mongo_movie.get('rating', 0),
            'platform': platform,
            'views': int(latam_views),
            'user_rating': user_rating,
            'favorites': watchlist_30d,
            'social_shares': social_30d,
            'completion_rate': (completion_30d / views_30d * 100) if views_30d > 0 else 0
        })

    if not classics_data:
        print("[WARN] No se encontraron clasicos pre-2000 en los datos actuales")
        empty_cols = [
            'name', 'year', 'genre', 'director', 'imdb_rating', 'platform',
            'views', 'user_rating', 'favorites', 'social_shares', 'completion_rate'
        ]
        return pd.DataFrame(columns=empty_cols)

    classics_sorted = sorted(classics_data, key=lambda x: x['views'], reverse=True)
    top_15 = classics_sorted[:15]

    print("\n[RESULT] Top 15 Clasicos (pre-2000) en LATAM:")
    print("-" * 70)
    for i, movie in enumerate(top_15, 1):
        print(f"{i:2}. {movie['name']} ({movie['year']})")
        print(f"    Plataforma: {movie['platform']} | Genero: {movie['genre']}")
        print(f"    Vistas LATAM: {movie['views']:,} | Watchlist: {movie['favorites']:,} | Shares: {movie['social_shares']:,}")
        print(f"    IMDb: {movie['imdb_rating']:.1f} | Engagement: {movie['user_rating']:.1f} | Completion: {movie['completion_rate']:.1f}%")

    df = pd.DataFrame(top_15)
    print("\nEstadisticas de clasicos en LATAM:")
    print(f"   Total clasicos disponibles: {len(classics_data)}")
    print(f"   Decada promedio: {int(df['year'].mean())}s")
    print(f"   Vistas promedio: {df['views'].mean():,.0f}")
    print(f"   Watchlist promedio: {df['favorites'].mean():,.0f}")
    print(f"   Social shares promedio: {df['social_shares'].mean():,.0f}")
    print(f"   Completion rate promedio: {df['completion_rate'].mean():.1f}%")

    platform_counts = df['platform'].value_counts()
    print("\nPlataformas con mas clasicos populares:")
    for platform, count in platform_counts.items():
        print(f"   {platform}: {count} peliculas")

    print("\nCRUCE #3 COMPLETADO")

    return df

def cruce_4_top_by_genre_region():
    """
    CRUCE #4: Películas más vistas por género en cada región

    COMBINA:
    - Redis: Rankings regionales (region:*:views ZSET)
    - MongoDB: Género de cada película
    - Redis: Métricas de engagement por película

    GENERA: Top 3 películas más vistas por género en cada región
    """
    print("\n🔀 CRUCE #4: Top Películas por Género y Región")
    print("=" * 70)

    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()

    if mongo_col is None or redis_client is None:
        print("❌ Error: No se pudo conectar a las bases de datos")
        return None

    # Regiones a analizar
    regions = ['latam', 'us', 'eu', 'asia']
    region_names = {
        'latam': 'Latinoamérica',
        'us': 'Estados Unidos',
        'eu': 'Europa',
        'asia': 'Asia'
    }

    all_results = {}

    for region in regions:
        print(f"\n📍 Analizando región: {region_names[region].upper()}")
        print("-" * 70)

        # 1. Obtener películas de la región desde REDIS ZSET
        region_movies_data = redis_client.zrevrange(f'region:{region}:views', 0, -1, withscores=True)
        print(f"   Películas con vistas: {len(region_movies_data)}")

        if len(region_movies_data) == 0:
            continue

        # 2. Para cada película, obtener género y métricas
        movies_by_genre = {}

        for title, region_views in region_movies_data:
            # Obtener género desde MongoDB
            mongo_movie = mongo_col.find_one({"name": title})

            if not mongo_movie or 'genre' not in mongo_movie:
                continue

            # Obtener métricas desde Redis
            movie_key = f"content:{title.replace(' ', '_')}"
            redis_data = redis_client.hgetall(movie_key)

            if not redis_data:
                continue

            views_30d = int(redis_data.get('views_30d', 0))
            completion_30d = int(redis_data.get('completion_watches_30d', 0))
            platform = redis_data.get('platform', 'N/A')

            # Calcular engagement
            if views_30d > 0:
                completion_rate = (completion_30d / views_30d) * 100
                user_rating = (completion_rate / 100) * 10
            else:
                user_rating = 0

            # Procesar géneros (pueden ser múltiples)
            genres = mongo_movie['genre'].split(',') if isinstance(mongo_movie['genre'], str) else [mongo_movie['genre']]

            for genre in genres:
                genre = genre.strip()

                if genre not in movies_by_genre:
                    movies_by_genre[genre] = []

                movies_by_genre[genre].append({
                    'title': title,
                    'views': int(region_views),  # Vistas en esta región específica
                    'rating': user_rating,
                    'completion_rate': (completion_30d / views_30d * 100) if views_30d > 0 else 0,
                    'platform': platform,
                    'year': mongo_movie.get('year', 'N/A')
                })

        # 3. Para cada género, ordenar por vistas y tomar top 3
        region_results = {}

        for genre, movies in movies_by_genre.items():
            # Ordenar por vistas en la región
            sorted_movies = sorted(movies, key=lambda x: x['views'], reverse=True)
            top_3 = sorted_movies[:3]
            region_results[genre] = top_3

        # 4. Mostrar resultados para esta región
        # Ordenar géneros por total de vistas
        genre_totals = {
            genre: sum(m['views'] for m in movies)
            for genre, movies in region_results.items()
        }
        sorted_genres = sorted(genre_totals.items(), key=lambda x: x[1], reverse=True)

        print(f"\n   📊 Top 5 Géneros más vistos en {region_names[region]}:")
        for i, (genre, total_views) in enumerate(sorted_genres[:5], 1):
            print(f"      {i}. {genre}: {total_views:,} vistas totales")
            top_movies = region_results[genre]
            for j, movie in enumerate(top_movies, 1):
                print(f"         {j}) {movie['title']}: {movie['views']:,} vistas | ⭐ {movie['rating']:.1f} | {movie['platform']}")

        all_results[region] = region_results

    # 5. Crear DataFrame consolidado
    print("\n" + "=" * 70)
    print("📊 TABLAS CONSOLIDADAS POR REGIÓN")
    print("=" * 70)

    consolidated_data = []

    for region, genres in all_results.items():
        for genre, movies in genres.items():
            for rank, movie in enumerate(movies, 1):
                consolidated_data.append({
                    'region': region_names[region],
                    'genre': genre,
                    'rank': rank,
                    'title': movie['title'],
                    'views': movie['views'],
                    'rating': movie['rating'],
                    'completion_rate': movie['completion_rate'],
                    'platform': movie['platform'],
                    'year': movie['year']
                })

    df = pd.DataFrame(consolidated_data)

    if len(df) > 0:
        # Mostrar tabla resumida por región
        for region in regions:
            region_name = region_names[region]
            region_data = df[df['region'] == region_name]

            if len(region_data) > 0:
                print(f"\n📍 {region_name.upper()}")
                print("-" * 70)

                # Top 3 géneros con más vistas totales
                top_genres = region_data.groupby('genre')['views'].sum().nlargest(3)

                for genre in top_genres.index:
                    genre_movies = region_data[region_data['genre'] == genre].nsmallest(3, 'rank')
                    print(f"\n   {genre}:")

                    for _, row in genre_movies.iterrows():
                        print(f"      {int(row['rank'])}. {row['title']} ({row['year']})")
                        print(f"         {row['views']:,} vistas | ⭐ {row['rating']:.1f} | Completion: {row['completion_rate']:.1f}% | {row['platform']}")

    print(f"\n✅ CRUCE #4 COMPLETADO")

    return df


def execute_all_cruces():
    """Ejecuta todos los cruces y muestra resumen"""
    print("🔥 EJECUCIÓN DE TODOS LOS CRUCES (30% de la nota)")
    print("=" * 70)

    results = {}

    # Cruce 1
    try:
        print("\n" + "="*70)
        results['cruce_1'] = cruce_1_top_movies_netflix()
    except Exception as e:
        print(f"❌ Error en Cruce 1: {e}")
        import traceback
        traceback.print_exc()
        results['cruce_1'] = None

    # Cruce 2
    try:
        print("\n" + "="*70)
        results['cruce_2'] = cruce_2_trending_by_genre()
    except Exception as e:
        print(f"❌ Error en Cruce 2: {e}")
        import traceback
        traceback.print_exc()
        results['cruce_2'] = None

    # Cruce 3
    try:
        print("\n" + "="*70)
        results['cruce_3'] = cruce_3_classics_latam()
    except Exception as e:
        print(f"❌ Error en Cruce 3: {e}")
        import traceback
        traceback.print_exc()
        results['cruce_3'] = None

    # Cruce 4 (BONUS)
    try:
        print("\n" + "="*70)
        results['cruce_4'] = cruce_4_top_by_genre_region()
    except Exception as e:
        print(f"❌ Error en Cruce 4: {e}")
        import traceback
        traceback.print_exc()
        results['cruce_4'] = None

    # Resumen final
    print("\n" + "=" * 70)
    print("🎉 RESUMEN DE CRUCES")
    print("=" * 70)

    successful = sum(1 for v in results.values() if v is not None)
    total_cruces = len(results)
    print(f"✅ Cruces exitosos: {successful}/{total_cruces}")

    if results['cruce_1'] is not None:
        print(f"   Cruce #1: {len(results['cruce_1'])} películas analizadas")
    if results['cruce_2'] is not None:
        print(f"   Cruce #2: {len(results['cruce_2'])} géneros identificados")
    if results['cruce_3'] is not None:
        print(f"   Cruce #3: {len(results['cruce_3'])} clásicos populares")
    if results.get('cruce_4') is not None:
        print(f"   Cruce #4 (BONUS): {len(results['cruce_4'])} entradas región-género")

    print("=" * 70)

    return results


if __name__ == "__main__":
    execute_all_cruces()
