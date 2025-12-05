"""
Carga rankings y datos rápidos a Redis
"""

import pandas as pd
from config import get_redis_connection, PROCESSED_CSV


def load_to_redis(csv_path=PROCESSED_CSV):
    """Carga datos a Redis"""
    print("\n⚡ LOAD - Cargando a Redis")
    print("=" * 50)

    # Conectar
    redis_client = get_redis_connection()
    if redis_client is None:
        return False

    # Limpiar Redis
    redis_client.flushdb()
    print("🗑️  Redis limpiado")

    # Leer datos
    df = pd.read_csv(csv_path)

    # 1. Cargar ratings individuales
    count = 0
    for _, movie in df.iterrows():
        if pd.notna(movie.get('rating')):
            key = f"movie:rating:{movie.get('name', '').replace(' ', '_')}"
            redis_client.set(key, str(movie['rating']))
            count += 1

    print(f"✅ Cargados {count} ratings individuales")

    # 2. Cargar ranking (sorted set)
    top_movies = df.nlargest(100, 'rating')
    ranking_data = {}
    for _, movie in top_movies.iterrows():
        if pd.notna(movie.get('rating')):
            ranking_data[movie['name']] = float(movie['rating'])

    if ranking_data:
        redis_client.zadd('ranking:top_movies', ranking_data)
        print(f"✅ Cargadas {len(ranking_data)} películas en ranking")

    # 3. Cargar plataformas (sets)
    if 'platform' in df.columns:
        platforms_count = {}
        for platform in ['Netflix', 'Prime Video', 'HBO Max', 'Disney+']:
            platform_movies = df[df['platform'].astype(str).str.contains(platform, na=False)]
            if len(platform_movies) > 0:
                titles = platform_movies['name'].tolist()
                key = f"platform:{platform.lower().replace(' ', '_')}"
                redis_client.sadd(key, *titles)
                platforms_count[platform] = len(titles)
                print(f"  ✓ {platform}: {len(titles)} películas")

        if not platforms_count:
            print("  ⚠️  No se encontraron plataformas en el dataset")

    print("\n✅ Carga a Redis completada")
    return True


if __name__ == "__main__":
    print("⚡ CARGA A REDIS")
    success = load_to_redis()

    if success:
        print("\n🎉 Redis configurado exitosamente")
