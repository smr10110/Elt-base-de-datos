"""
Script principal para ejecutar el pipeline ETL completo
EJECUTAR DESDE LA RAÍZ DEL PROYECTO
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import get_mongo_connection, get_redis_connection
from extract import extract_all
from transform import transform_all
from load_mongo import load_to_mongodb
from load_redis import load_to_redis
from integration import execute_all_cruces
from visualizations import generate_all_visualizations


def test_connections():
    """Prueba las conexiones a MongoDB y Redis"""
    print("\n🧪 PROBANDO CONEXIONES")
    print("=" * 70)


    mongo_client, mongo_db, mongo_col = get_mongo_connection()
    redis_client = get_redis_connection()

    if mongo_client is None or redis_client is None:
        print("\n❌ Error: Verifica que MongoDB y Redis estén ejecutándose")
        return False

    print("\n✅ Todas las conexiones exitosas")
    return True


def run_etl_pipeline():
    """Ejecuta el pipeline ETL completo"""
    print("\n" + "=" * 70)
    print("🎬 INICIANDO PIPELINE ETL - PROYECTO CINEMA")
    print("=" * 70)

    # Paso 1: Probar conexiones
    if not test_connections():
        sys.exit(1)

    # Paso 2: Extract
    print("\n📥 PASO 1: EXTRACT")
    print("-" * 70)
    kaggle, manual = extract_all()

    if kaggle is None:
        print("❌ Error: No se pudo extraer el dataset de Kaggle")
        sys.exit(1)

    if manual is None:
        print("⚠️  Advertencia: No se encontró el dataset manual")
        print("   Debes crear: data/raw/dataset_manual_IMDB_Top250.csv")
        print("   El pipeline continuará sin datos manuales...")

    # Paso 3: Transform
    print("\n⚙️  PASO 2: TRANSFORM")
    print("-" * 70)
    final_data = transform_all()

    if final_data is None:
        print("❌ Error en la transformación de datos")
        sys.exit(1)

    # Paso 4: Load - MongoDB
    print("\n🍃 PASO 3: LOAD - MongoDB")
    print("-" * 70)
    mongo_count = load_to_mongodb()

    if mongo_count == 0:
        print("❌ Error cargando datos a MongoDB")
        sys.exit(1)

    # Paso 5: Load - Redis
    print("\n⚡ PASO 4: LOAD - Redis")
    print("-" * 70)
    redis_success = load_to_redis()

    if not redis_success:
        print("❌ Error cargando datos a Redis")
        sys.exit(1)

    # Paso 6: Integration (Cruces)
    print("\n🔀 PASO 5: INTEGRATION - Cruces (30% de la nota)")
    print("-" * 70)
    cruces_results = execute_all_cruces()

    # Paso 7: Visualizations
    print("\n📊 PASO 6: VISUALIZATIONS - Gráficos y Análisis")
    print("-" * 70)
    generate_all_visualizations()

    # Resumen final
    print("\n" + "=" * 70)
    print("🎉 PIPELINE ETL COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print(f"✅ Películas en MongoDB: {mongo_count}")
    print(f"✅ Datos cargados en Redis")
    print(f"✅ Cruces ejecutados: {len(cruces_results)}")
    print(f"✅ Visualizaciones generadas en: docs/images/")
    print("\n📋 Próximos pasos:")
    print("   1. Revisa los gráficos en docs/images/")
    print("   2. Completa el informe final")
    print("   3. Prepara la presentación en inglés")
    print("=" * 70)


if __name__ == "__main__":
    try:
        run_etl_pipeline()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
