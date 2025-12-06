"""
Pipeline ETL completo: Flipkart → MongoDB | Redis Cart Simulation
Simula un Cyberday con múltiples productos y carritos en tiempo real.
"""

import sys
from datetime import datetime

# Importar módulos del pipeline
from src.extract import extract_all
from src.transform import transform_all, get_transformation_stats
from src.load import load_all
from src.integration import integration_all
from src.config import get_redis_connection


def print_header(title: str):
    """Imprime encabezado formateado."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_footer():
    """Imprime pie formateado."""
    print("=" * 70 + "\n")


def main():
    """Ejecuta el pipeline ETL completo."""
    
    print_header("🚀 PIPELINE ETL: CYBERDAY CON MONGODB Y REDIS")
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_footer()

    # ===== ETAPA 1: EXTRACT =====
    print_header("📥 ETAPA 1: EXTRACT (Extracción)")
    flipkart_df, redis_cart_df = extract_all()
    
    if flipkart_df is None or redis_cart_df is None:
        print("[ERROR] No se pudieron cargar los datos")
        sys.exit(1)

    print_footer()

    # ===== ETAPA 2-3: TRANSFORM + LOAD =====
    print_header("🔄 ETAPA 2: TRANSFORM (Transformación)")
    flipkart_transformed, cart_transformed = transform_all()
    stats = get_transformation_stats(flipkart_transformed, cart_transformed)
    print_footer()

    print_header("📤 ETAPA 3: LOAD (Carga a MongoDB y Redis)")
    load_success = load_all(flipkart_transformed, cart_transformed, simulate_realtime=False)
    
    if not load_success:
        print("[ADVERTENCIA] La carga no fue completamente exitosa")
        print("  ⚠️  Asegúrate de que MongoDB y Redis estén ejecutándose")

    print_footer()

    # ===== ETAPA 4: INTEGRATION =====
    print_header("🔀 ETAPA 4: INTEGRATION (Análisis Cruzado)")
    report = integration_all()
    print_footer()

    # ===== RESUMEN FINAL =====
    print_header("📊 RESUMEN DEL PIPELINE")
    print(f"✅ Productos Flipkart: {stats['products']['total']}")
    print(f"✅ Eventos de Carrito: {stats['carts']['total_events']}")
    print(f"✅ Carritos Únicos: {stats['carts']['unique_carts']}")
    print(f"✅ Clientes: {stats['carts']['unique_customers']}")
    print(f"💰 Ingresos Totales: ${stats['carts']['total_revenue']:.2f}")
    print(f"❌ Ingresos Perdidos: ${stats['carts']['lost_revenue']:.2f}")
    print(f"📅 Timestamp: {stats['timestamp']}")
    print_footer()

    print("✨ Pipeline completado exitosamente")


if __name__ == "__main__":
    main()