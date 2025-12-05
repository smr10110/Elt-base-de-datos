"""
Fase TRANSFORM del ETL.
Limpia y normaliza el dataset principal (Netflix Dataset.csv) y, si existe,
combina el dataset manual. El resultado se guarda en data/processed/movies_final.csv.
"""

import pandas as pd
from extract import extract_all
from config import PROCESSED_CSV


def standardize_movies_df(df):
    """
    Normaliza columnas para que el pipeline pueda trabajar con el dataset de Netflix.
    - Renombra Title -> name
    - Extrae year desde Release_Date
    - Crea columnas faltantes con valores razonables
    """
    df = df.copy()

    # Renombrar columnas comunes del dataset de Netflix
    rename_map = {
        "Title": "name",
        "Release_Date": "release_date",
        "Category": "category",
        "Director": "directors",
        "Cast": "casts",
        "Type": "genre",  # usamos Type como aproximacion de genero
        "Rating": "content_rating",
    }
    df = df.rename(columns=rename_map)

    # Asegurar columna name
    if "name" not in df.columns:
        raise ValueError("El dataset no contiene una columna 'name' o 'Title'")

    # Derivar year
    if "year" not in df.columns:
        if "release_date" in df.columns:
            df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
        else:
            df["year"] = None

    # Crear rating numerico (si no existe, o si viene como string tipo TV-MA se convierte a NaN -> 0)
    if "rating" not in df.columns:
        if "content_rating" in df.columns:
            df["rating"] = pd.to_numeric(df["content_rating"], errors="coerce")
        else:
            df["rating"] = None
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)

    # Si no hay genero, usar category o valor por defecto
    if "genre" not in df.columns:
        if "category" in df.columns:
            df["genre"] = df["category"]
        else:
            df["genre"] = "Unknown"

    # Limpiar filas sin nombre o anio
    df = df.dropna(subset=["name"])
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    # Eliminar duplicados por nombre/anio
    df = df.drop_duplicates(subset=["name", "year"])

    return df


def clean_movies(df):
    """Aplica normalizacion y reglas basicas de limpieza."""
    print("\n[TRANSFORM] Limpieza y normalizacion del dataset principal")
    print("=" * 50)

    original_count = len(df)
    df = standardize_movies_df(df)
    print(f"[OK] Filas limpias: {original_count} -> {len(df)}")

    return df


def merge_datasets(kaggle_df, manual_df):
    """
    Combina datasets principal y manual. Si no hay dataset manual, devuelve el principal.
    """
    print("\n[TRANSFORM] Combinando datasets (principal + manual)")
    print("=" * 50)

    if manual_df is None or len(manual_df) == 0:
        print("[WARN] No hay dataset manual, se continua solo con el principal")
        return kaggle_df

    manual_df = manual_df.copy()
    if "name" not in manual_df.columns and "Title" in manual_df.columns:
        manual_df = manual_df.rename(columns={"Title": "name"})

    if "name" not in manual_df.columns:
        print("[WARN] El dataset manual no tiene columna 'name'; se omite la combinacion")
        return kaggle_df

    merged = kaggle_df.merge(manual_df, on="name", how="left", suffixes=("", "_manual"))
    print(f"[OK] Datasets combinados: {len(merged)} filas")

    return merged


def transform_all():
    """Pipeline completo de transformacion."""
    print("[TRANSFORM] Fase TRANSFORM")
    print("=" * 50)

    kaggle, manual = extract_all()

    if kaggle is None:
        print("[ERROR] No se pudo leer el dataset principal")
        return None

    kaggle_clean = clean_movies(kaggle)
    final = merge_datasets(kaggle_clean, manual)

    final.to_csv(PROCESSED_CSV, index=False)
    print(f"\n[OK] Datos guardados en: {PROCESSED_CSV}")

    return final


if __name__ == "__main__":
    movies_final = transform_all()

    if movies_final is not None:
        print("\n[OK] Transformacion completada")
        print(f"Total de filas procesadas: {len(movies_final)}")
