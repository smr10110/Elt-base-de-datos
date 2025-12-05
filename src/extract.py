"""
Extraction helpers for the Flipkart sample dataset.
Reads the CSV defined in config and can print a preview of the first rows.
"""

from pathlib import Path
from typing import Tuple

import pandas as pd

from config import KAGGLE_CSV

DEFAULT_SAMPLE_SIZE = 50


def load_flipkart_data(csv_path: str = KAGGLE_CSV) -> pd.DataFrame:
    """
    Load the Flipkart sample CSV into a DataFrame.

    Parameters
    ----------
    csv_path: str
        Path to the Flipkart CSV file.

    Returns
    -------
    pd.DataFrame
        Raw dataset.
    """
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"Could not find CSV at {path.resolve()}")

    df = pd.read_csv(path)
    print(f"[EXTRACT] Loaded {len(df)} rows from {path}")
    print(f"[EXTRACT] Columns: {list(df.columns)}")
    return df

def preview_data(df: pd.DataFrame, sample_size: int = DEFAULT_SAMPLE_SIZE) -> pd.DataFrame:
    """
    Return and display the first N rows of a DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to preview.
    sample_size: int
        Number of rows to display (defaults to 50).

    Returns
    -------
    pd.DataFrame
        The sampled rows.
    """
    if sample_size <= 0:
        raise ValueError("sample_size must be a positive integer")

    sample = df.head(sample_size)
    print(f"[PREVIEW] Showing the first {len(sample)} rows")
    print(sample)
    return sample


def extract_flipkart(sample_size: int = DEFAULT_SAMPLE_SIZE) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the Flipkart dataset and return it along with a small preview.

    Parameters
    ----------
    sample_size: int
        Number of rows to include in the preview (defaults to 50).

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        Raw dataset and preview sample.
    """
    df = load_flipkart_data()
    sample = preview_data(df, sample_size)
    return df, sample


def extract_all() -> Tuple[pd.DataFrame, None]:
    """
    Backwards-compatible helper expected by the rest of the pipeline.
    Returns the full dataset and None for manual data (not used here).
    """
    df = load_flipkart_data()
    return df, None


if __name__ == "__main__":
    print("[EXTRACT] Starting Flipkart extraction")
    raw_df, preview_df = extract_flipkart()
    print(f"[EXTRACT] Extraction complete. Rows loaded: {len(raw_df)} | Preview rows: {len(preview_df)}")
