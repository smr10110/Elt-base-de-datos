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
