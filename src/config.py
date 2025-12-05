"""
Configuración centralizada para MongoDB y Redis
"""

from pymongo import MongoClient
import redis
import os

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
# Las rutas son relativas al directorio donde ejecutas el script
KAGGLE_CSV = "data/raw/IMDB_Top_250_Movies.csv"
MANUAL_CSV = "data/raw/dataset_manual_IMDB_Top250.csv"
PROCESSED_CSV = "data/processed/movies_final.csv"


if __name__ == "__main__":
    print("🧪 Probando configuración...")
    print(f"\n📁 Dataset Kaggle: {KAGGLE_CSV}")
    print(f"📁 Dataset Manual: {MANUAL_CSV}")
    print(f"📁 Datos procesados: {PROCESSED_CSV}")

    print("\n🧪 Probando conexiones...")

    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()

    if mongo_client and redis_client:
        print("\n🎉 ¡Todas las conexiones funcionan!")
    else:
        print("\n⚠️ Revisa tu configuración")
