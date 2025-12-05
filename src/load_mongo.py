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
    print("🗑️  Colección limpiada")

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

    print(f"✅ Insertados {inserted_count} documentos en MongoDB")

    return inserted_count


if __name__ == "__main__":
    print("🍃 CARGA A MONGODB")
    count = load_to_mongodb()

    if count > 0:
        print(f"\n🎉 Carga completada: {count} películas en MongoDB")
