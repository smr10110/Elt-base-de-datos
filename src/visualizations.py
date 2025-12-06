"""
Visualizaciones para análisis del Cyberday: MongoDB + Redis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from src.config import get_mongo_connection, get_redis_connection


def plot_product_brands_distribution():
    """Gráfico de distribución de productos por marca."""
    try:
        _, _, collection = get_mongo_connection()
        if collection is None:
            return

        # Agregación
        pipeline = [
            {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 15},
        ]

        results = list(collection.aggregate(pipeline))
        
        if not results:
            print("[VIZ] No hay datos de productos")
            return

        brands = [r["_id"] for r in results]
        counts = [r["count"] for r in results]

        plt.figure(figsize=(12, 6))
        plt.barh(brands, counts, color="steelblue")
        plt.xlabel("Cantidad de Productos")
        plt.title("Top 15 Marcas por Cantidad de Productos")
        plt.tight_layout()
        plt.savefig("data/processed/brands_distribution.png", dpi=100, bbox_inches="tight")
        print("[VIZ] Gráfico guardado: brands_distribution.png")
        plt.close()

    except Exception as e:
        print(f"[VIZ] Error en gráfico de marcas: {e}")


def plot_price_distribution():
    """Gráfico de distribución de precios."""
    try:
        _, _, collection = get_mongo_connection()
        if collection is None:
            return

        # Obtener precios
        prices = [doc["discounted_price"] for doc in collection.find({}, {"discounted_price": 1})]
        
        if not prices:
            print("[VIZ] No hay datos de precios")
            return

        plt.figure(figsize=(12, 6))
        plt.hist(prices, bins=50, color="coral", edgecolor="black", alpha=0.7)
        plt.xlabel("Precio Descuentado (Rupias)")
        plt.ylabel("Cantidad de Productos")
        plt.title("Distribución de Precios - Flipkart")
        plt.tight_layout()
        plt.savefig("data/processed/price_distribution.png", dpi=100, bbox_inches="tight")
        print("[VIZ] Gráfico guardado: price_distribution.png")
        plt.close()

    except Exception as e:
        print(f"[VIZ] Error en distribución de precios: {e}")


def plot_cart_events_timeline():
    """Gráfico de eventos de carrito en tiempo."""
    try:
        redis_client = get_redis_connection()
        if redis_client is None:
            return

        # Obtener eventos
        cart_keys = redis_client.keys("cart:CART-*")
        events_by_type = {"add": 0, "checkout": 0, "abandon": 0, "stock_out": 0}

        for key in cart_keys:
            cart_data = redis_client.hgetall(key)
            try:
                events = json.loads(cart_data.get("events", "[]"))
                for event in events:
                    event_type = event.get("event_type", "unknown")
                    if event_type in events_by_type:
                        events_by_type[event_type] += 1
            except:
                pass

        if sum(events_by_type.values()) == 0:
            print("[VIZ] No hay eventos de carrito")
            return

        plt.figure(figsize=(10, 6))
        colors = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12"]
        plt.bar(events_by_type.keys(), events_by_type.values(), color=colors)
        plt.xlabel("Tipo de Evento")
        plt.ylabel("Cantidad de Eventos")
        plt.title("Eventos de Carrito - Cyberday")
        plt.tight_layout()
        plt.savefig("data/processed/cart_events.png", dpi=100, bbox_inches="tight")
        print("[VIZ] Gráfico guardado: cart_events.png")
        plt.close()

        redis_client.close()

    except Exception as e:
        print(f"[VIZ] Error en gráfico de eventos: {e}")


def plot_revenue_metrics():
    """Gráfico de métricas de ingresos."""
    try:
        redis_client = get_redis_connection()
        if redis_client is None:
            return

        cart_keys = redis_client.keys("cart:CART-*")
        total_revenue = 0
        lost_revenue = 0
        revenue_by_cart = []

        for key in cart_keys:
            cart_data = redis_client.hgetall(key)
            revenue = float(cart_data.get("total_revenue", 0))
            lost = float(cart_data.get("lost_revenue", 0))
            
            total_revenue += revenue
            lost_revenue += lost
            
            if revenue > 0:
                revenue_by_cart.append(revenue)

        if not revenue_by_cart:
            print("[VIZ] No hay datos de ingresos")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Gráfico 1: Ingresos vs Perdidos
        ax1.bar(["Ingresos", "Perdidos"], [total_revenue, lost_revenue], color=["#27ae60", "#e74c3c"])
        ax1.set_ylabel("Rupias")
        ax1.set_title("Ingresos Totales vs Perdidos")
        for i, v in enumerate([total_revenue, lost_revenue]):
            ax1.text(i, v + 100, f"${v:.0f}", ha="center", va="bottom", fontweight="bold")

        # Gráfico 2: Distribución de ingresos por carrito
        ax2.hist(revenue_by_cart, bins=10, color="steelblue", edgecolor="black", alpha=0.7)
        ax2.set_xlabel("Ingresos por Carrito")
        ax2.set_ylabel("Cantidad de Carritos")
        ax2.set_title("Distribución de Ingresos")

        plt.tight_layout()
        plt.savefig("data/processed/revenue_metrics.png", dpi=100, bbox_inches="tight")
        print("[VIZ] Gráfico guardado: revenue_metrics.png")
        plt.close()

        redis_client.close()

    except Exception as e:
        print(f"[VIZ] Error en gráfico de ingresos: {e}")


def generate_all_visualizations():
    """Genera todas las visualizaciones."""
    print("\n[VIZ] Generando visualizaciones del Cyberday...\n")
    
    plot_product_brands_distribution()
    plot_price_distribution()
    plot_cart_events_timeline()
    plot_revenue_metrics()
    
    print("\n[VIZ] ✅ Todas las visualizaciones completadas\n")


if __name__ == "__main__":
    generate_all_visualizations()