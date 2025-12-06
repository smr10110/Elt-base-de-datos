"""
Pipeline ETL: Cyberday con MongoDB y Redis
Módulo principal del ETL
"""

__version__ = "1.0.0"
__author__ = "ETL Pipeline"

from src.extract import extract_all
from src.transform import transform_all
from src.load import load_all
from src.integration import integration_all

__all__ = [
    "extract_all",
    "transform_all", 
    "load_all",
    "integration_all",
]
