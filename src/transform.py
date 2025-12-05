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

    print(f"✅ Limpieza completada: {original_count} -> {len(df)} películas")

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
        print(f"Total de películas procesadas: {len(movies_final)}")
