# ⚡ Instrucciones Rápidas - Proyecto ETL Cinema

## 🎯 Pasos para Ejecutar el Proyecto

### 1️⃣ Preparación (Solo una vez)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear dataset manual
python create_manual_dataset.py
```

### 2️⃣ Iniciar Bases de Datos

**Terminal 1 - MongoDB:**
```bash
mongod
```

**Terminal 2 - Redis:**
```bash
redis-server
```

### 3️⃣ Ejecutar Pipeline ETL

**Terminal 3 (desde la raíz del proyecto):**
```bash
python run_pipeline.py
```

O si prefieres ejecutar paso a paso:
```bash
cd src
python extract.py
python transform.py
python load_mongo.py
python load_redis.py
python integration.py
python visualizations.py
```

## ✅ Checklist Antes de Ejecutar

- [ ] MongoDB instalado y ejecutándose
- [ ] Redis instalado y ejecutándose
- [ ] Dependencias Python instaladas (`pip install -r requirements.txt`)
- [ ] Dataset Kaggle en: `data/raw/IMDB_Top_250_Movies.csv` ✅
- [ ] Dataset manual creado: `data/raw/dataset_manual_IMDB_Top250.csv`

## 📊 ¿Qué hace el pipeline?

1. **Extract:** Lee los 2 CSV (Kaggle + Manual)
2. **Transform:** Limpia y combina los datos
3. **Load MongoDB:** Carga 250 películas
4. **Load Redis:** Carga rankings y plataformas
5. **Integration:** 🔥 **CRUCES (30% de la nota)**
   - Top películas en Netflix
   - Rating IMDb vs Personal
   - Géneros por plataforma
6. **Visualizations:** Genera 3 gráficos en `docs/images/`

## 📁 Archivos Generados

Después de ejecutar, encontrarás:

```
data/processed/movies_final.csv          # Datos procesados
docs/images/top_netflix.png              # Gráfico 1
docs/images/rating_comparison.png        # Gráfico 2
docs/images/genres_by_platform.png       # Gráfico 3
```

## 🔧 Solución de Problemas

### Error: "No se pudo conectar a MongoDB"
```bash
# Verifica que esté ejecutándose
mongod --version

# Inicia MongoDB
mongod
```

### Error: "No se pudo conectar a Redis"
```bash
# Verifica que esté ejecutándose
redis-cli ping

# Debería responder: PONG
# Si no, inicia Redis
redis-server
```

### Error: "No se encontró el dataset manual"
```bash
# Genera el dataset manual
python create_manual_dataset.py
```

## 📝 Próximos Pasos

Después de ejecutar el pipeline:

1. ✅ Revisa los gráficos en `docs/images/`
2. ✅ Analiza los resultados de los cruces
3. ✅ Completa el informe final con:
   - Justificación de MongoDB y Redis (10%)
   - Metodología ETL
   - Análisis de cruces (30%)
   - Visualizaciones (30%)
   - Conclusiones
4. ✅ Prepara presentación en **INGLÉS** (10-15 min)

## 🎯 Distribución de Puntos

| Criterio | Peso | Archivo Relacionado |
|----------|------|---------------------|
| Justificación de BD | 10% | Informe (por escribir) |
| Diseño y Carga | 20% | `load_mongo.py`, `load_redis.py` |
| **CRUCES** | **30%** | `integration.py` ⭐ |
| Análisis y Visualizaciones | 30% | `visualizations.py` |
| Presentación (inglés) | 10% | Presentación (por crear) |

## 📅 Fecha Límite

**11 de Diciembre**

---

**¿Necesitas ayuda?** Revisa el [README.md](README.md) completo o la [GUIA_COMPLETA_PROYECTO_ETL.md](req/GUIA_COMPLETA_PROYECTO_ETL.md)
