"""
Ejemplos de consultas para MongoDB y Redis
Uso: python -m examples.queries
"""

def mongodb_examples():
    """Ejemplos de consultas en MongoDB."""
    print("\n" + "="*60)
    print(" 📊 EJEMPLOS DE CONSULTAS MONGODB")
    print("="*60)
    
    from src.config import get_mongo_connection
    
    _, _, collection = get_mongo_connection()
    if not collection:
        print("❌ No se pudo conectar a MongoDB")
        return
    
    # 1. Productos por marca
    print("\n1️⃣  Productos por marca:")
    pipeline = [
        {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    for doc in collection.aggregate(pipeline):
        print(f"   {doc['_id']}: {doc['count']} productos")
    
    # 2. Descuento promedio
    print("\n2️⃣  Descuentos promedio por marca:")
    pipeline = [
        {"$group": {
            "_id": "$brand",
            "discount_pct": {"$avg": {"$subtract": ["$retail_price", "$discounted_price"]}}
        }},
        {"$sort": {"discount_pct": -1}},
        {"$limit": 5},
    ]
    for doc in collection.aggregate(pipeline):
        print(f"   {doc['_id']}: ${doc['discount_pct']:.2f}")
    
    # 3. Precio promedio
    print("\n3️⃣  Precio promedio por marca:")
    pipeline = [
        {"$group": {
            "_id": "$brand",
            "avg_price": {"$avg": "$discounted_price"}
        }},
        {"$sort": {"avg_price": -1}},
        {"$limit": 5},
    ]
    for doc in collection.aggregate(pipeline):
        print(f"   {doc['_id']}: ${doc['avg_price']:.2f}")
    
    # 4. Categorías principales
    print("\n4️⃣  Categorías principales:")
    pipeline = [
        {"$group": {"_id": "$main_category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    for doc in collection.aggregate(pipeline):
        print(f"   {doc['_id']}: {doc['count']} productos")
    
    # 5. Productos por rango de precio
    print("\n5️⃣  Productos por rango de precio:")
    ranges = [
        (0, 500, "< $500"),
        (500, 1000, "$500-$1000"),
        (1000, 5000, "$1000-$5000"),
        (5000, float('inf'), "> $5000"),
    ]
    
    for min_p, max_p, label in ranges:
        count = collection.count_documents({
            "discounted_price": {"$gte": min_p, "$lt": max_p}
        })
        print(f"   {label}: {count} productos")


def redis_examples():
    """Ejemplos de consultas en Redis."""
    print("\n" + "="*60)
    print(" 🔴 EJEMPLOS DE CONSULTAS REDIS")
    print("="*60)
    
    from src.config import get_redis_connection
    import json
    
    r = get_redis_connection()
    if not r:
        print("❌ No se pudo conectar a Redis")
        return
    
    # 1. Carritos totales
    print("\n1️⃣  Carritos totales:")
    cart_keys = r.keys("cart:CART-*")
    print(f"   Total: {len(cart_keys)} carritos")
    
    # 2. Detalles de carritos
    print("\n2️⃣  Detalles de carritos:")
    for key in cart_keys[:3]:  # Primeros 3
        data = r.hgetall(key)
        cart_id = key.replace("cart:", "")
        customer_id = data.get("customer_id", "Unknown")
        revenue = data.get("total_revenue", 0)
        print(f"   {cart_id} ({customer_id}): ${revenue}")
    
    # 3. Ingresos totales
    print("\n3️⃣  Ingresos totales por carrito:")
    total_revenue = 0
    for key in cart_keys:
        data = r.hgetall(key)
        revenue = float(data.get("total_revenue", 0))
        total_revenue += revenue
    print(f"   Total: ${total_revenue:.2f}")
    
    # 4. Ingresos perdidos
    print("\n4️⃣  Ingresos perdidos:")
    total_lost = 0
    for key in cart_keys:
        data = r.hgetall(key)
        lost = float(data.get("lost_revenue", 0))
        total_lost += lost
    print(f"   Total: ${total_lost:.2f}")
    
    # 5. Análisis de eventos
    print("\n5️⃣  Análisis de eventos:")
    event_counts = {}
    for key in cart_keys:
        data = r.hgetall(key)
        try:
            events = json.loads(data.get("events", "[]"))
            for event in events:
                event_type = event.get("event_type", "unknown")
                event_counts[event_type] = event_counts.get(event_type, 0) + 1
        except:
            pass
    
    for event_type, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {event_type}: {count} eventos")
    
    # 6. Clientes únicos
    print("\n6️⃣  Clientes únicos:")
    customers = set()
    for key in cart_keys:
        data = r.hgetall(key)
        customer = data.get("customer_id")
        if customer:
            customers.add(customer)
    print(f"   Total: {len(customers)} clientes")
    for cust in sorted(customers):
        print(f"     - {cust}")
    
    # 7. Cálculo de tasas
    print("\n7️⃣  Tasas de conversión:")
    total_carts = len(cart_keys)
    checkouts = 0
    abandons = 0
    
    for key in cart_keys:
        data = r.hgetall(key)
        try:
            events = json.loads(data.get("events", "[]"))
            for event in events:
                if event.get("event_type") == "checkout":
                    checkouts += 1
                elif event.get("event_type") == "abandon":
                    abandons += 1
        except:
            pass
    
    checkout_rate = (checkouts / total_carts * 100) if total_carts > 0 else 0
    abandon_rate = (abandons / total_carts * 100) if total_carts > 0 else 0
    
    print(f"   Completados: {checkouts} ({checkout_rate:.1f}%)")
    print(f"   Abandonados: {abandons} ({abandon_rate:.1f}%)")
    
    r.close()


def cross_database_analysis():
    """Análisis cruzado MongoDB + Redis."""
    print("\n" + "="*60)
    print(" 🔀 ANÁLISIS CRUZADO MONGODB + REDIS")
    print("="*60)
    
    from src.config import get_mongo_connection, get_redis_connection
    import json
    
    _, _, mongo_col = get_mongo_connection()
    redis = get_redis_connection()
    
    if not mongo_col or not redis:
        print("❌ Error de conexión")
        return
    
    # 1. Productos más comprados
    print("\n1️⃣  Top productos comprados:")
    product_counts = {}
    cart_keys = redis.keys("cart:CART-*")
    
    for key in cart_keys:
        data = redis.hgetall(key)
        try:
            events = json.loads(data.get("events", "[]"))
            for event in events:
                if event.get("event_type") == "checkout":
                    prod = event.get("product_id")
                    product_counts[prod] = product_counts.get(prod, 0) + 1
        except:
            pass
    
    for prod, count in sorted(product_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {prod}: {count} ventas")
    
    # 2. Ingresos por categoría
    print("\n2️⃣  Estadísticas por categoría:")
    pipeline = [
        {"$group": {
            "_id": "$main_category",
            "count": {"$sum": 1},
            "avg_price": {"$avg": "$discounted_price"}
        }},
        {"$sort": {"count": -1}},
    ]
    
    for doc in mongo_col.aggregate(pipeline):
        category = doc["_id"]
        count = doc["count"]
        avg_price = doc["avg_price"]
        print(f"   {category}: {count} productos, ${avg_price:.2f} promedio")
    
    redis.close()


def main():
    """Ejecuta todos los ejemplos."""
    try:
        mongodb_examples()
    except Exception as e:
        print(f"⚠️  Error en MongoDB: {e}")
    
    try:
        redis_examples()
    except Exception as e:
        print(f"⚠️  Error en Redis: {e}")
    
    try:
        cross_database_analysis()
    except Exception as e:
        print(f"⚠️  Error en análisis cruzado: {e}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
