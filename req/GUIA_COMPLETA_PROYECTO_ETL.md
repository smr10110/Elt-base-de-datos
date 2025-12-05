# 🎬 Proyecto ETL Cinema - MongoDB + Redis + Python

## 📋 Índice
1. [Contexto del Proyecto](#contexto)
2. [Requisitos y Criterios de Evaluación](#criterios)
3. [Arquitectura del Sistema](#arquitectura)
4. [Datasets](#datasets)
5. [Estructura del Proyecto](#estructura)
6. [Código Completo](#codigo)
7. [Instalación y Ejecución](#instalacion)
8. [Cruces de Información](#cruces)
9. [Checklist Final](#checklist)

---

## 📌 Contexto del Proyecto {#contexto}

**Nombre:** Coup de Grâce  
**Asignatura:** Database Workshop (ICC529)  
**Profesor:** Felipe Gastón Vasquez  
**Fecha límite:** 11 de Diciembre  
**Modalidad:** Proyecto en grupo de 2-3 personas  
**Presentación:** 10-15 minutos EN INGLÉS (obligatorio)

### Objetivo
Crear un mini sistema ETL artesanal usando dos motores de bases de datos NoSQL (MongoDB y Redis) para el dominio de Cine/Películas, integrando un dataset público de Kaggle con datos manuales, realizando cruces de información y presentando resultados con visualizaciones.

---

## 📊 Requisitos y Criterios de Evaluación {#criterios}

### Requisitos Obligatorios
- ✅ Dos motores NoSQL DIFERENTES (MongoDB + Redis)
- ✅ AL MENOS UNO debe usar dataset público (Kaggle)
- ✅ Lenguaje: Python
- ✅ Presentación: EN INGLÉS (10-15 min)
- ✅ Grupo: 2-3 personas (NO MÁS, NO MENOS)

### Distribución de Puntos (100% total)

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **Selección y Justificación de BD** | 10% | Justificar por qué MongoDB y por qué Redis |
| **Diseño y Carga de Datos** | 20% | Esquemas documentados + carga exitosa |
| **Extracción y CRUCE de Información** | 30% | ⭐ **MÁS IMPORTANTE** - Combinar MongoDB + Redis |
| **Análisis y Presentación de Resultados** | 30% | Visualizaciones + análisis detallado |
| **Presentación Oral** | 10% | En inglés, 10-15 min |

### Entregables
1. Código fuente (scripts Python documentados)
2. Informe final (justificación, metodología, análisis, conclusiones)
3. Presentación oral (inglés, con diapositivas)

---

## 🏗️ Arquitectura del Sistema {#arquitectura}

```
┌─────────────────────────────────────────────────────────────┐
│                     DATASETS                                 │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │  Kaggle (Público)    │    │  Manual (Tuyo)       │      │
│  │  IMDB Top 250        │    │  Preferencias        │      │
│  │  250 películas       │    │  75 registros        │      │
│  └──────────┬───────────┘    └──────────┬───────────┘      │
└─────────────┼──────────────────────────┼───────────────────┘
              │                           │
              ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │   PYTHON ETL    │         │   PYTHON ETL    │
    │                 │         │                 │
    │ Extract         │         │ Extract         │
    │ Transform       │         │ Transform       │
    │ Load            │         │ Load            │
    └────────┬────────┘         └────────┬────────┘
             │                           │
             ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │   🍃 MongoDB     │         │   ⚡ Redis       │
    │                 │         │                 │
    │ Info completa   │         │ Rankings        │
    │ 250 películas   │         │ Plataformas     │
    │ Permanente      │         │ Cache rápido    │
    └────────┬────────┘         └────────┬────────┘
             │                           │
             └──────────┬────────────────┘
                        ▼
              ┌──────────────────┐
              │   🔀 CRUCES      │
              │  (30% nota)      │
              │                  │
              │ MongoDB + Redis  │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │  📊 RESULTADOS   │
              │                  │
              │ Gráficos         │
              │ Análisis         │
              │ Insights         │
              └──────────────────┘
```

---

## 📦 Datasets {#datasets}

### Dataset 1: Kaggle (Público) - IMDB_Top_250_Movies.csv

**Origen:** Kaggle (dataset público de las mejores 250 películas de IMDb)  
**Destino:** MongoDB  
**Tamaño:** 250 películas

**Columnas:**
```
- rank: Posición en el Top 250
- name: Nombre de la película
- year: Año de estreno
- rating: Rating de IMDb (0-10)
- genre: Géneros (Drama, Action, Sci-Fi, etc.)
- certificate: Clasificación (R, PG-13, etc.)
- run_time: Duración
- tagline: Frase promocional
- budget: Presupuesto
- box_office: Taquilla
- casts: Actores
- directors: Directores
- writers: Escritores
```

**Ejemplo de fila:**
```csv
1,The Shawshank Redemption,1994,9.3,Drama,R,2h 22m,Fear can hold you prisoner...,25000000,28884504,Tim Robbins|Morgan Freeman,Frank Darabont,Stephen King
```

### Dataset 2: Manual - dataset_manual_IMDB_Top250.csv

**Origen:** Creado manualmente  
**Destino:** Redis (y cruces con MongoDB)  
**Tamaño:** 75 registros de 4 usuarios

**Columnas:**
```
- user_id: ID del usuario (user_001, user_002, etc.)
- name: Nombre de la película (coincide con Kaggle)
- watched: Si la viste (TRUE/FALSE)
- favorite: Si es favorita (TRUE/FALSE)
- personal_rating: Tu rating personal (0-10)
- platform: Plataforma de streaming (Netflix, Prime Video, HBO Max, Disney+)
- watch_date: Fecha que la viste (YYYY-MM-DD)
```

**Ejemplo de filas:**
```csv
user_id,name,watched,favorite,personal_rating,platform,watch_date
user_001,The Shawshank Redemption,TRUE,TRUE,10,Netflix,2024-03-15
user_001,The Godfather,TRUE,TRUE,9.5,Prime Video,2024-02-20
user_002,The Dark Knight,TRUE,TRUE,9.5,HBO Max,2024-03-22
```

### ¿Por qué dos datasets?

| Aspecto | Dataset Kaggle | Dataset Manual |
|---------|----------------|----------------|
| **Propósito** | Info oficial de IMDb | Info adicional (preferencias, plataformas) |
| **Tipo de datos** | Públicos, verificados | Personales, subjetivos |
| **Base de datos** | MongoDB (almacenamiento completo) | Redis (rankings rápidos) |
| **Uso en cruces** | Fuente de ratings IMDb | Fuente de disponibilidad |

---

## 📁 Estructura del Proyecto {#estructura}

```
proyecto_cinema_etl/
│
├── data/
│   ├── raw/
│   │   ├── IMDB_Top_250_Movies.csv          # Dataset Kaggle
│   │   └── dataset_manual_IMDB_Top250.csv   # Dataset manual
│   │
│   └── processed/
│       └── movies_final.csv                  # Generado por transform.py
│
├── src/
│   ├── config.py                  # Configuración de conexiones
│   ├── extract.py                 # Extracción de datos
│   ├── transform.py               # Transformación y limpieza
│   ├── load_mongo.py              # Carga a MongoDB (10%)
│   ├── load_redis.py              # Carga a Redis (10%)
│   ├── integration.py             # 🔥 CRUCES (30% - MÁS IMPORTANTE)
│   ├── queries.py                 # Consultas de prueba
│   └── visualizations.py          # Gráficos y análisis (30%)
│
├── docs/
│   ├── images/                    # Gráficos generados
│   ├── informe_final.docx         # Informe técnico
│   └── presentacion.pptx          # Presentación en inglés
│
├── requirements.txt               # Dependencias Python
├── README.md                      # Documentación
└── .gitignore
```

---

## 💻 Código Completo {#codigo}

### 1. requirements.txt

```txt
pymongo==4.6.0
redis==5.0.1
pandas==2.1.4
matplotlib==3.8.2
plotly==5.18.0
openpyxl==3.1.2
python-dotenv==1.0.0
```

### 2. src/config.py

```python
"""
Configuración centralizada para MongoDB y Redis
"""

from pymongo import MongoClient
import redis

# ===== CONFIGURACIÓN MONGODB =====
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "cinema_db"
MONGO_COLLECTION = "movies"

def get_mongo_connection():
    """Obtiene conexión a MongoDB"""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        client.server_info()  # Probar conexión
        print("✅ Conexión a MongoDB exitosa")
        
        return client, db, collection
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        return None, None, None


# ===== CONFIGURACIÓN REDIS =====
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

def get_redis_connection():
    """Obtiene conexión a Redis"""
    try:
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
        
        r.ping()  # Probar conexión
        print("✅ Conexión a Redis exitosa")
        
        return r
    except Exception as e:
        print(f"❌ Error conectando a Redis: {e}")
        return None


# ===== RUTAS DE ARCHIVOS =====
KAGGLE_CSV = "../data/raw/IMDB_Top_250_Movies.csv"
MANUAL_CSV = "../data/raw/dataset_manual_IMDB_Top250.csv"
PROCESSED_CSV = "../data/processed/movies_final.csv"


if __name__ == "__main__":
    print("🧪 Probando conexiones...")
    
    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()
    
    if mongo_client and redis_client:
        print("\n🎉 ¡Todas las conexiones funcionan!")
    else:
        print("\n⚠️ Revisa tu configuración")
```

### 3. src/extract.py

```python
"""
Fase EXTRACT del ETL
Extrae datos de datasets públicos y manuales
"""

import pandas as pd
from config import KAGGLE_CSV, MANUAL_CSV


def extract_kaggle_data():
    """Extrae datos del dataset público de Kaggle"""
    print("\n📥 EXTRACT - Dataset Público (Kaggle)")
    print("=" * 50)
    
    try:
        df = pd.read_csv(KAGGLE_CSV)
        
        print(f"✅ Extraídas {len(df)} películas de Kaggle")
        print(f"📊 Columnas: {list(df.columns)}")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ No se encontró: {KAGGLE_CSV}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def extract_manual_data():
    """Extrae datos del dataset manual"""
    print("\n📥 EXTRACT - Dataset Manual")
    print("=" * 50)
    
    try:
        df = pd.read_csv(MANUAL_CSV)
        
        print(f"✅ Extraídas {len(df)} preferencias")
        print(f"📊 Columnas: {list(df.columns)}")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ No se encontró: {MANUAL_CSV}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def extract_all():
    """Extrae todos los datasets"""
    kaggle = extract_kaggle_data()
    manual = extract_manual_data()
    
    return kaggle, manual


if __name__ == "__main__":
    print("🎬 FASE EXTRACT")
    kaggle_movies, user_preferences = extract_all()
    
    if kaggle_movies is not None and user_preferences is not None:
        print("\n🎉 Extracción completada!")
```

### 4. src/transform.py

```python
"""
Fase TRANSFORM del ETL
Limpia, normaliza y enriquece los datos
"""

import pandas as pd
from extract import extract_all
from config import PROCESSED_CSV


def clean_movies(df):
    """Limpia el dataset de películas"""
    print("\n🧹 TRANSFORM - Limpieza")
    print("=" * 50)
    
    original_count = len(df)
    
    # Eliminar filas sin título
    df = df.dropna(subset=['name'])
    
    # Eliminar duplicados
    df = df.drop_duplicates(subset=['name', 'year'])
    
    # Convertir año a numérico
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    
    # Normalizar ratings
    if 'rating' in df.columns:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['rating'] = df['rating'].fillna(0)
    
    print(f"🎉 Limpieza completada: {len(df)} películas limpias")
    
    return df


def merge_datasets(kaggle_df, manual_df):
    """Combina datasets de Kaggle y manual"""
    print("\n🔗 TRANSFORM - Combinación")
    print("=" * 50)
    
    merged = kaggle_df.merge(
        manual_df,
        on='name',
        how='left',
        suffixes=('', '_manual')
    )
    
    print(f"✅ Datasets combinados: {len(merged)} películas")
    
    return merged


def transform_all():
    """Pipeline completo de transformación"""
    print("⚙️ FASE TRANSFORM")
    print("=" * 50)
    
    # Extraer
    kaggle, manual = extract_all()
    
    if kaggle is None or manual is None:
        print("❌ No se pudieron extraer datos")
        return None
    
    # Limpiar
    kaggle_clean = clean_movies(kaggle)
    
    # Combinar
    final = merge_datasets(kaggle_clean, manual)
    
    # Guardar
    final.to_csv(PROCESSED_CSV, index=False)
    print(f"\n💾 Datos guardados en: {PROCESSED_CSV}")
    
    return final


if __name__ == "__main__":
    movies_final = transform_all()
    
    if movies_final is not None:
        print("\n🎉 Transformación completada!")
```

### 5. src/load_mongo.py

```python
"""
Carga datos a MongoDB
"""

import pandas as pd
from config import get_mongo_connection, PROCESSED_CSV


def load_to_mongodb(csv_path=PROCESSED_CSV):
    """Carga datos procesados a MongoDB"""
    print("\n📤 LOAD - Cargando a MongoDB")
    print("=" * 50)
    
    # Conectar
    client, db, collection = get_mongo_connection()
    if collection is None:
        return 0
    
    # Leer datos
    df = pd.read_csv(csv_path)
    print(f"✅ Leídas {len(df)} películas")
    
    # Limpiar colección anterior
    collection.delete_many({})
    
    # Convertir a lista de diccionarios
    movies_list = df.to_dict('records')
    
    # Convertir NaN a None
    for movie in movies_list:
        for key, value in movie.items():
            if pd.isna(value):
                movie[key] = None
    
    # Insertar
    result = collection.insert_many(movies_list)
    inserted_count = len(result.inserted_ids)
    
    print(f"✅ Insertados {inserted_count} documentos")
    
    return inserted_count


if __name__ == "__main__":
    print("🍃 CARGA A MONGODB")
    count = load_to_mongodb()
    
    if count > 0:
        print(f"\n🎉 Carga completada: {count} películas")
```

### 6. src/load_redis.py

```python
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
    
    # Leer datos
    df = pd.read_csv(csv_path)
    
    # 1. Cargar ratings individuales
    count = 0
    for _, movie in df.iterrows():
        if pd.notna(movie.get('rating')):
            key = f"movie:rating:{movie.get('name', '').replace(' ', '_')}"
            redis_client.set(key, str(movie['rating']))
            count += 1
    
    print(f"✅ Cargados {count} ratings")
    
    # 2. Cargar ranking
    top_movies = df.nlargest(100, 'rating')
    ranking_data = {}
    for _, movie in top_movies.iterrows():
        if pd.notna(movie.get('rating')):
            ranking_data[movie['name']] = float(movie['rating'])
    
    redis_client.zadd('ranking:top_movies', ranking_data)
    print(f"✅ Cargadas {len(ranking_data)} películas en ranking")
    
    # 3. Cargar plataformas
    if 'platform' in df.columns:
        for platform in ['Netflix', 'Prime Video', 'HBO Max', 'Disney+']:
            platform_movies = df[df['platform'].astype(str).str.contains(platform, na=False)]
            if len(platform_movies) > 0:
                titles = platform_movies['name'].tolist()
                key = f"platform:{platform.lower().replace(' ', '_')}"
                redis_client.sadd(key, *titles)
                print(f"  ✓ {platform}: {len(titles)} películas")
    
    print("\n✅ Carga a Redis completada")
    return True


if __name__ == "__main__":
    print("⚡ CARGA A REDIS")
    load_to_redis()
```

### 7. src/integration.py (🔥 MÁS IMPORTANTE - 30%)

```python
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
        print(f"{i:2}. {movie['name']} - ⭐ {movie['rating']:.1f}")
    
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
        print(f"\n⬆️ Películas que valoras MÁS que IMDb:")
        for _, row in overrated.iterrows():
            print(f"  • {row['name']}: +{row['difference']:.1f}")
    
    print(f"\n✅ CRUCE COMPLETADO")
    
    return df


def cruce_3_genres_by_platform():
    """
    CRUCE #3: Géneros más populares por plataforma
    
    COMBINA:
    - MongoDB: Géneros de películas
    - Dataset Manual/Redis: Plataformas
    
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
```

### 8. src/visualizations.py

```python
"""
Genera visualizaciones de los resultados
"""

import matplotlib.pyplot as plt
import pandas as pd
from integration import cruce_1_top_movies_netflix, cruce_2_rating_comparison
import os


def plot_top_netflix():
    """Gráfico 1: Top películas en Netflix"""
    print("\n📊 Generando gráfico: Top Netflix...")
    
    df = cruce_1_top_movies_netflix()
    
    if df is None or len(df) == 0:
        return
    
    plt.figure(figsize=(12, 6))
    plt.barh(df['name'], df['rating'], color='#E50914')
    plt.xlabel('Rating IMDb', fontsize=12)
    plt.ylabel('Película', fontsize=12)
    plt.title('Top 10 Películas en Netflix', fontsize=14, fontweight='bold')
    plt.xlim(0, 10)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    
    os.makedirs('../docs/images', exist_ok=True)
    plt.savefig('../docs/images/top_netflix.png', dpi=300, bbox_inches='tight')
    print("✅ Guardado: docs/images/top_netflix.png")
    plt.close()


def plot_rating_comparison():
    """Gráfico 2: Rating IMDb vs Personal"""
    print("\n📊 Generando gráfico: Rating Comparison...")
    
    df = cruce_2_rating_comparison()
    
    if df is None or len(df) == 0:
        return
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['imdb_rating'], df['personal_rating'], alpha=0.6, s=100)
    plt.plot([0, 10], [0, 10], 'r--', alpha=0.5, label='Línea de igualdad')
    plt.xlabel('Rating IMDb', fontsize=12)
    plt.ylabel('Rating Personal', fontsize=12)
    plt.title('Comparación: Rating IMDb vs Personal', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('../docs/images/rating_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Guardado: docs/images/rating_comparison.png")
    plt.close()


def generate_all_visualizations():
    """Genera todas las visualizaciones"""
    print("📊 GENERACIÓN DE VISUALIZACIONES")
    print("=" * 50)
    
    plot_top_netflix()
    plot_rating_comparison()
    
    print("\n🎉 Visualizaciones completadas")


if __name__ == "__main__":
    generate_all_visualizations()
```

---

## ⚙️ Instalación y Ejecución {#instalacion}

### Paso 1: Instalar Software

**MongoDB:**
```bash
# Descargar de mongodb.com/try/download/community
# Verificar instalación:
mongod --version
```

**Redis:**
```bash
# Windows: github.com/microsoftarchive/redis/releases
# Mac: brew install redis
# Linux: sudo apt-get install redis-server

# Verificar:
redis-cli --version
```

**Python + Librerías:**
```bash
# Instalar dependencias:
pip install -r requirements.txt
```

### Paso 2: Preparar Datos

1. Coloca `IMDB_Top_250_Movies.csv` en `data/raw/`
2. Coloca `dataset_manual_IMDB_Top250.csv` en `data/raw/`

### Paso 3: Iniciar Bases de Datos

```bash
# Terminal 1: MongoDB
mongod

# Terminal 2: Redis
redis-server
```

### Paso 4: Ejecutar Pipeline ETL

```bash
cd src/

# Probar conexiones
python config.py

# Extraer datos
python extract.py

# Transformar datos
python transform.py

# Cargar a MongoDB
python load_mongo.py

# Cargar a Redis
python load_redis.py

# 🔥 CRUCES (30% de tu nota)
python integration.py

# Generar visualizaciones
python visualizations.py
```

---

## 🔀 Cruces de Información (30% de la nota) {#cruces}

### ¿Qué es un CRUCE?

Un cruce válido DEBE:
1. Extraer datos de MongoDB
2. Extraer datos de Redis (o dataset manual)
3. COMBINAR ambos para generar nuevo insight
4. El resultado NO DEBE existir en ninguna BD por separado

### Ejemplo de CRUCE VÁLIDO ✅

**Cruce:** Top 10 películas en Netflix

1. **MongoDB dice:** The Shawshank Redemption tiene rating 9.3
2. **Redis/Manual dice:** The Shawshank Redemption está en Netflix
3. **CRUCE genera:** "Top 10 películas mejor valoradas EN Netflix"

❌ **Esto NO es un cruce:**
- Consultar top 10 de MongoDB
- Consultar top 10 de Redis
- Mostrar ambos por separado

### Cruces Implementados

1. **Top películas en Netflix** (combina rating + plataforma)
2. **Rating IMDb vs Personal** (compara dos fuentes de rating)
3. **Géneros por plataforma** (distribución de géneros en streaming)

---

## ✅ Checklist Final {#checklist}

### Antes de Entregar

- [ ] **Dataset Kaggle** descargado y en `data/raw/`
- [ ] **Dataset manual** creado y en `data/raw/`
- [ ] **MongoDB** instalado y funcionando
- [ ] **Redis** instalado y funcionando
- [ ] **Librerías** Python instaladas
- [ ] **extract.py** ejecutado sin errores
- [ ] **transform.py** ejecutado sin errores
- [ ] **load_mongo.py** ejecutado - datos en MongoDB
- [ ] **load_redis.py** ejecutado - datos en Redis
- [ ] **integration.py** ejecutado - 3 cruces funcionando
- [ ] **visualizations.py** ejecutado - gráficos generados
- [ ] **Justificación escrita** (10%) - MongoDB + Redis
- [ ] **Informe final** completado
- [ ] **Presentación en inglés** (10-15 min) preparada

### Distribución de Tiempo Sugerida

- **Día 1-2:** Setup + Justificación
- **Día 3-4:** Extract + Transform + Load
- **Día 5:** CRUCES (30% - prioridad máxima)
- **Día 6:** Visualizaciones y análisis
- **Día 7:** Informe + Presentación + Ensayo

---

## 🎯 Puntos Clave para Recordar

1. **El dataset manual ES PARA REDIS** - No necesitas otro dataset diferente
2. **Los cruces valen 30%** - Es lo más importante del proyecto
3. **Presentación EN INGLÉS** - Es obligatorio y vale 10%
4. **Ambos datasets son de películas** - Solo contienen información diferente
5. **MongoDB = info completa** | **Redis = info rápida/adicional**

---

## 📞 Información de Contacto del Profesor

**Profesor:** Felipe Gastón Vasquez  
**Disponibilidad:** Oficina (excepto martes 2:30-7:00pm)  
**Fecha límite:** 11 de Diciembre  

---

**¡Éxito en tu proyecto Coup de Grâce! 🚀**