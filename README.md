# 🎬 Proyecto ETL Cinema - MongoDB + Redis + Python

## Información del Proyecto

**Nombre:** Coup de Grâce
**Asignatura:** Database Workshop (ICC529)
**Profesor:** Felipe Gastón Vasquez
**Fecha límite:** 11 de Diciembre
**Presentación:** 10-15 minutos EN INGLÉS (obligatorio)

## Estructura del Proyecto

```
proyecto_cinema_etl/
│
├── data/
│   ├── raw/
│   │   ├── IMDB_Top_250_Movies.csv          # Dataset Kaggle ✅
│   │   └── dataset_manual_IMDB_Top250.csv   # Dataset manual (POR CREAR)
│   │
│   └── processed/
│       └── movies_final.csv                  # Generado automáticamente
│
├── src/
│   ├── config.py                  # Configuración de conexiones
│   ├── extract.py                 # Extracción de datos
│   ├── transform.py               # Transformación y limpieza
│   ├── load_mongo.py              # Carga a MongoDB
│   ├── load_redis.py              # Carga a Redis
│   ├── integration.py             # 🔥 CRUCES (30% - MÁS IMPORTANTE)
│   ├── visualizations.py          # Gráficos y análisis
│   └── main.py                    # Script principal
│
├── docs/
│   └── images/                    # Gráficos generados automáticamente
│
├── req/                           # Documentación del proyecto
├── requirements.txt               # Dependencias Python
└── README.md                      # Este archivo
```

## Instalación

### 1. Instalar MongoDB

**Windows:**
1. Descargar de: https://www.mongodb.com/try/download/community
2. Instalar y ejecutar como servicio
3. Verificar: `mongod --version`

**Mac:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

### 2. Instalar Redis

**Windows:**
1. Descargar de: https://github.com/microsoftarchive/redis/releases
2. Instalar y ejecutar `redis-server.exe`

**Mac:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

### 3. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

## Dataset Manual (IMPORTANTE)

Antes de ejecutar el pipeline, debes crear el dataset manual:

**Archivo:** `data/raw/dataset_manual_IMDB_Top250.csv`

**Formato:**
```csv
user_id,name,watched,favorite,personal_rating,platform,watch_date
user_001,The Shawshank Redemption,TRUE,TRUE,10,Netflix,2024-03-15
user_001,The Godfather,TRUE,TRUE,9.5,Prime Video,2024-02-20
user_002,The Dark Knight,TRUE,TRUE,9.5,HBO Max,2024-03-22
```

**Requisitos:**
- 75 registros de 4 usuarios diferentes (user_001, user_002, user_003, user_004)
- Columnas: user_id, name, watched, favorite, personal_rating, platform, watch_date
- Plataformas: Netflix, Prime Video, HBO Max, Disney+
- Los nombres deben coincidir exactamente con el dataset de Kaggle

## Ejecución

### Opción 1: Ejecutar Pipeline Completo

```bash
cd src
python main.py
```

Esto ejecutará automáticamente:
1. ✅ Prueba de conexiones
2. 📥 Extract (extracción de datos)
3. ⚙️  Transform (limpieza y normalización)
4. 🍃 Load MongoDB
5. ⚡ Load Redis
6. 🔀 Integration (cruces de información)
7. 📊 Visualizations (gráficos)

### Opción 2: Ejecutar Paso a Paso

```bash
cd src

# Probar conexiones
python config.py

# Extraer datos
python extract.py

# Transformar datos
python transform.py

# Cargar a MongoDB
python load_mongo.py

# Cargar a Redis
python load_redis.py

# Ejecutar cruces (30% de la nota)
python integration.py

# Generar visualizaciones
python visualizations.py
```

## Cruces de Información (30% de la nota)

Los 3 cruces implementados combinan datos de MongoDB y Redis:

1. **Top películas en Netflix**
   - MongoDB: Ratings de películas
   - Redis: Disponibilidad en Netflix
   - Resultado: Top 10 mejor valoradas EN Netflix

2. **Rating IMDb vs Personal**
   - MongoDB: Rating oficial de IMDb
   - Dataset Manual: Rating personal
   - Resultado: Análisis de diferencias

3. **Géneros por plataforma**
   - MongoDB: Géneros de películas
   - Redis: Plataformas de streaming
   - Resultado: Distribución de géneros

## Evaluación del Proyecto

| Criterio | Peso |
|----------|------|
| Selección y Justificación de BD | 10% |
| Diseño y Carga de Datos | 20% |
| **Extracción y CRUCE de Información** | **30%** |
| Análisis y Presentación de Resultados | 30% |
| Presentación Oral (inglés) | 10% |

## Justificación de Bases de Datos

### MongoDB
- **Ventajas:** Esquema flexible, ideal para datos no estructurados
- **Uso:** Almacenar información completa de 250 películas
- **Por qué:** Consultas complejas, agregaciones, análisis detallado

### Redis
- **Ventajas:** Velocidad extrema, estructuras de datos especializadas
- **Uso:** Rankings (sorted sets), plataformas (sets), cache de ratings
- **Por qué:** Acceso rápido a rankings y disponibilidad en streaming

## Próximos Pasos

- [ ] Crear dataset manual (75 registros)
- [ ] Ejecutar pipeline completo
- [ ] Revisar visualizaciones generadas
- [ ] Completar informe final
- [ ] Preparar presentación en inglés (10-15 min)

## Solución de Problemas

### Error: "No se pudo conectar a MongoDB"
- Verifica que MongoDB esté ejecutándose: `mongod --version`
- Windows: Inicia el servicio MongoDB
- Mac/Linux: `brew services start mongodb-community`

### Error: "No se pudo conectar a Redis"
- Verifica que Redis esté ejecutándose: `redis-cli ping`
- Debería responder: `PONG`
- Inicia Redis: `redis-server`

### Error: "No se encontró el dataset manual"
- Crea el archivo: `data/raw/dataset_manual_IMDB_Top250.csv`
- Sigue el formato especificado arriba

## Contacto

**Profesor:** Felipe Gastón Vasquez
**Fecha límite:** 11 de Diciembre
