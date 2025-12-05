"""
Carga métricas de streaming de Netflix a Redis
Diseño profesional como director ejecutivo de Netflix

Estructuras Redis:
1. SETS por categoría (Movie vs TV Show)
2. SORTED SETS para rankings temporales (views:7d, views:30d, watchlist, etc.)
3. SORTED SETS por región (region:*:views)
4. HASHES para metadata completa
5. SORTED SETS para engagement y analytics
"""

import pandas as pd
from pathlib import Path
from config import get_redis_connection

# Ruta al dataset de Netflix
PROJECT_ROOT = Path(__file__).parent.parent
NETFLIX_CSV = PROJECT_ROOT / 'data' / 'raw' / 'netflix_streaming_metrics.csv'


def load_to_redis(csv_path=NETFLIX_CSV):
    """Carga métricas de Netflix a Redis"""
    print("\n[NETFLIX ANALYTICS] Cargando metricas de streaming a Redis")
    print("=" * 70)

    # Conectar
    redis_client = get_redis_connection()
    if redis_client is None:
        return False

    # Limpiar Redis
    redis_client.flushdb()
    print("[CLEAN] Redis limpiado")

    # Verificar archivo
    if not csv_path.exists():
        print(f"[ERROR] No se encontro el archivo: {csv_path}")
        return False

    # Leer datos
    print(f"[LOAD] Leyendo: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"[OK] Cargados {len(df)} titulos de Netflix")

    # ====================
    # 1. SETS POR CATEGORIA
    # ====================
    print("\n[STEP 1/6] Cargando SETS por categoria...")
    category_count = {}

    for _, content in df.iterrows():
        category = content.get('category', '')
        title = content.get('title', '')

        if pd.notna(category) and pd.notna(title):
            category_key = category.lower().replace(' ', '_')
            redis_client.sadd(f'category:{category_key}', title)
            category_count[category] = category_count.get(category, 0) + 1

    for cat, count in category_count.items():
        print(f"  -> {cat}: {count} titulos")

    # ====================
    # 2. SORTED SETS TEMPORALES
    # ====================
    print("\n[STEP 2/6] Cargando SORTED SETS temporales...")

    # Views 7d
    views_7d_data = {}
    for _, content in df.iterrows():
        title = content.get('title', '')
        views = content.get('views_7d', 0)
        if pd.notna(title) and pd.notna(views):
            views_7d_data[title] = float(views)

    if views_7d_data:
        redis_client.zadd('views:7d', views_7d_data)
        print(f"  -> Ranking views 7d: {len(views_7d_data)} titulos")

    # Views 30d
    views_30d_data = {}
    for _, content in df.iterrows():
        title = content.get('title', '')
        views = content.get('views_30d', 0)
        if pd.notna(title) and pd.notna(views):
            views_30d_data[title] = float(views)

    if views_30d_data:
        redis_client.zadd('views:30d', views_30d_data)
        print(f"  -> Ranking views 30d: {len(views_30d_data)} titulos")

    # Watchlist 7d
    watchlist_7d_data = {}
    for _, content in df.iterrows():
        title = content.get('title', '')
        adds = content.get('watchlist_adds_7d', 0)
        if pd.notna(title) and pd.notna(adds):
            watchlist_7d_data[title] = float(adds)

    if watchlist_7d_data:
        redis_client.zadd('watchlist:7d', watchlist_7d_data)
        print(f"  -> Ranking watchlist 7d: {len(watchlist_7d_data)} titulos")

    # Watchlist 30d
    watchlist_30d_data = {}
    for _, content in df.iterrows():
        title = content.get('title', '')
        adds = content.get('watchlist_adds_30d', 0)
        if pd.notna(title) and pd.notna(adds):
            watchlist_30d_data[title] = float(adds)

    if watchlist_30d_data:
        redis_client.zadd('watchlist:30d', watchlist_30d_data)
        print(f"  -> Ranking watchlist 30d: {len(watchlist_30d_data)} titulos")

    # Search 30d
    search_30d_data = {}
    for _, content in df.iterrows():
        title = content.get('title', '')
        searches = content.get('search_hits_30d', 0)
        if pd.notna(title) and pd.notna(searches):
            search_30d_data[title] = float(searches)

    if search_30d_data:
        redis_client.zadd('search:30d', search_30d_data)
        print(f"  -> Ranking busquedas 30d: {len(search_30d_data)} titulos")

    # ====================
    # 3. SORTED SETS ENGAGEMENT
    # ====================
    print("\n[STEP 3/6] Cargando SORTED SETS engagement...")

    # Social shares
    social_data = {}
    for _, content in df.iterrows():
        title = content.get('title', '')
        shares = content.get('social_shares_30d', 0)
        if pd.notna(title) and pd.notna(shares):
            social_data[title] = float(shares)

    if social_data:
        redis_client.zadd('engagement:social', social_data)
        print(f"  -> Ranking social shares: {len(social_data)} titulos")

    # Completion rate
    completion_data = {}
    for _, content in df.iterrows():
        title = content.get('title', '')
        completions = content.get('completion_watches_30d', 0)
        views = content.get('views_30d', 1)

        if pd.notna(title) and pd.notna(completions) and views > 0:
            completion_rate = (float(completions) / float(views)) * 100
            completion_data[title] = completion_rate

    if completion_data:
        redis_client.zadd('engagement:completion_rate', completion_data)
        print(f"  -> Ranking completion rate: {len(completion_data)} titulos")

    # ====================
    # 4. SORTED SETS REGIONALES
    # ====================
    print("\n[STEP 4/6] Cargando SORTED SETS regionales...")

    regions = ['latam', 'us', 'eu', 'asia']
    regions_count = {region: 0 for region in regions}

    for region in regions:
        region_views = {}
        col_name = f'region_{region}_views'

        for _, content in df.iterrows():
            title = content.get('title', '')
            views = content.get(col_name, 0)

            if pd.notna(title) and pd.notna(views) and views > 0:
                region_views[title] = float(views)
                regions_count[region] += 1

        if region_views:
            redis_client.zadd(f'region:{region}:views', region_views)

    for region, count in regions_count.items():
        print(f"  -> {region.upper()}: {count} titulos")

    # ====================
    # 5. HASHES METADATA
    # ====================
    print("\n[STEP 5/6] Cargando HASHES metadata...")
    hash_count = 0

    for _, content in df.iterrows():
        title = content.get('title', '')
        if pd.notna(title):
            # Key normalizada
            content_key = f"content:{title.replace(' ', '_')}"

            # Hash con todas las metricas
            content_hash = {
                'category': str(content.get('category', '')),
                'rating': str(content.get('rating', '')),
                'views_7d': str(content.get('views_7d', 0)),
                'views_30d': str(content.get('views_30d', 0)),
                'watchlist_adds_7d': str(content.get('watchlist_adds_7d', 0)),
                'watchlist_adds_30d': str(content.get('watchlist_adds_30d', 0)),
                'search_hits_7d': str(content.get('search_hits_7d', 0)),
                'search_hits_30d': str(content.get('search_hits_30d', 0)),
                'social_shares_7d': str(content.get('social_shares_7d', 0)),
                'social_shares_30d': str(content.get('social_shares_30d', 0)),
                'completion_watches_7d': str(content.get('completion_watches_7d', 0)),
                'completion_watches_30d': str(content.get('completion_watches_30d', 0)),
                'platform_rank': str(content.get('platform_rank', 0)),
                'region_latam_views': str(content.get('region_latam_views', 0)),
                'region_us_views': str(content.get('region_us_views', 0)),
                'region_eu_views': str(content.get('region_eu_views', 0)),
                'region_asia_views': str(content.get('region_asia_views', 0)),
                'last_metric_update': str(content.get('last_metric_update', ''))
            }

            redis_client.hset(content_key, mapping=content_hash)
            hash_count += 1

    print(f"  -> Hashes creados: {hash_count} titulos")

    # ====================
    # 6. ANALYTICS DERIVADOS
    # ====================
    print("\n[STEP 6/6] Calculando analytics derivados...")

    # Trending velocity
    trending_velocity = {}
    for _, content in df.iterrows():
        title = content.get('title', '')
        views_7d = content.get('views_7d', 0)
        views_30d = content.get('views_30d', 1)

        if pd.notna(title) and views_30d > 0:
            weekly_rate = float(views_7d) / 7
            monthly_rate = float(views_30d) / 30

            if monthly_rate > 0:
                velocity = weekly_rate / monthly_rate
                trending_velocity[title] = velocity

    if trending_velocity:
        redis_client.zadd('analytics:trending_velocity', trending_velocity)
        print(f"  -> Trending velocity: {len(trending_velocity)} titulos")

    # ====================
    # RESUMEN FINAL
    # ====================
    print("\n" + "=" * 70)
    print("[SUCCESS] Carga a Redis completada")
    print("=" * 70)
    print(f"[STATS] Categorias: {len(category_count)}")
    print(f"[STATS] Rankings temporales: 5 (views, watchlist, search)")
    print(f"[STATS] Engagement metrics: 2 (social, completion)")
    print(f"[STATS] Regiones: {len(regions)}")
    print(f"[STATS] Hashes: {hash_count} titulos")
    print(f"[STATS] Analytics: 1 (trending velocity)")
    total_keys = hash_count + len(category_count) + len(regions) + 9
    print(f"[STATS] Total keys: ~{total_keys}")
    print("=" * 70)

    return True


def test_redis_data():
    """Prueba datos cargados"""
    print("\n[TEST] Verificando datos en Redis")
    print("=" * 70)

    redis_client = get_redis_connection()
    if redis_client is None:
        return

    # Test 1: Contenido por categoria
    print("\n[TEST 1] Contenido por categoria")
    movies = redis_client.smembers('category:movie')
    tvshows = redis_client.smembers('category:tv_show')
    print(f"  Movies: {len(movies)}")
    print(f"  TV Shows: {len(tvshows)}")
    if len(movies) > 0:
        print(f"  Ejemplo Movie: {list(movies)[:2]}")
    if len(tvshows) > 0:
        print(f"  Ejemplo TV Show: {list(tvshows)[:2]}")

    # Test 2: Top 5 mas vistos (30d)
    print("\n[TEST 2] Top 5 mas vistos (30d)")
    top_views = redis_client.zrevrange('views:30d', 0, 4, withscores=True)
    for i, (title, views) in enumerate(top_views, 1):
        print(f"  {i}. {title}: {int(views):,} vistas")

    # Test 3: Top 5 trending velocity
    print("\n[TEST 3] Top 5 trending velocity")
    trending = redis_client.zrevrange('analytics:trending_velocity', 0, 4, withscores=True)
    for i, (title, velocity) in enumerate(trending, 1):
        print(f"  {i}. {title}: {velocity:.2f}x")

    # Test 4: Metadata de un titulo
    print("\n[TEST 4] Metadata de ejemplo")
    all_keys = redis_client.keys('content:*')
    if all_keys:
        sample_key = all_keys[0]
        data = redis_client.hgetall(sample_key)
        title = sample_key.decode('utf-8').replace('content:', '').replace('_', ' ')
        print(f"  Titulo: {title}")
        print(f"  Categoria: {data.get('category', 'N/A')}")
        print(f"  Views 30d: {data.get('views_30d', 'N/A')}")
        print(f"  Completion rate: {int(float(data.get('completion_watches_30d', 0)) / max(float(data.get('views_30d', 1)), 1) * 100)}%")

    # Test 5: Top 3 en LATAM
    print("\n[TEST 5] Top 3 en LATAM")
    latam_top = redis_client.zrevrange('region:latam:views', 0, 2, withscores=True)
    for i, (title, views) in enumerate(latam_top, 1):
        print(f"  {i}. {title}: {int(views):,} vistas")

    # Test 6: Total keys
    print("\n[TEST 6] Estructura Redis")
    all_keys = redis_client.keys('*')
    print(f"  Total keys: {len(all_keys)}")

    key_types = {}
    for key in all_keys:
        key_prefix = key.decode('utf-8').split(':')[0]
        key_types[key_prefix] = key_types.get(key_prefix, 0) + 1

    print("  Distribucion:")
    for prefix, count in sorted(key_types.items()):
        print(f"    {prefix}: {count} keys")

    print("\n" + "=" * 70)
    print("[OK] Pruebas completadas")
    print("=" * 70)


if __name__ == "__main__":
    print("[NETFLIX ANALYTICS] Sistema de metricas de streaming")
    print("=" * 70)

    success = load_to_redis()

    if success:
        print("\n" + "=" * 70)
        test_redis_data()
        print("\n[SUCCESS] Redis configurado con metricas de Netflix")
    else:
        print("\n[ERROR] Error en la carga de datos")
