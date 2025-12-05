"""
Genera visualizaciones de los resultados
"""

import matplotlib.pyplot as plt
import pandas as pd
from integration import cruce_1_top_movies_netflix, cruce_2_rating_comparison, cruce_3_genres_by_platform
from pathlib import Path

# Obtener la ruta raíz del proyecto (un nivel arriba de src)
PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_ROOT / 'docs' / 'images'


def plot_top_netflix():
    """Gráfico 1: Top películas en Netflix"""
    print("\n📊 Generando gráfico: Top Netflix...")

    df = cruce_1_top_movies_netflix()

    if df is None or len(df) == 0:
        print("⚠️  No se pudo generar el gráfico de Netflix")
        return

    plt.figure(figsize=(12, 6))
    plt.barh(df['name'], df['rating'], color='#E50914')
    plt.xlabel('Rating IMDb', fontsize=12)
    plt.ylabel('Película', fontsize=12)
    plt.title('Top 10 Películas en Netflix', fontsize=14, fontweight='bold')
    plt.xlim(0, 10)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()

    # Crear directorio si no existe
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    output_path = IMAGES_DIR / 'top_netflix.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Guardado: {output_path}")
    plt.close()


def plot_rating_comparison():
    """Gráfico 2: Rating IMDb vs Personal"""
    print("\n📊 Generando gráfico: Rating Comparison...")

    df = cruce_2_rating_comparison()

    if df is None or len(df) == 0:
        print("⚠️  No se pudo generar el gráfico de comparación de ratings")
        return

    plt.figure(figsize=(10, 6))
    plt.scatter(df['imdb_rating'], df['personal_rating'], alpha=0.6, s=100, color='#1f77b4')
    plt.plot([0, 10], [0, 10], 'r--', alpha=0.5, label='Línea de igualdad')
    plt.xlabel('Rating IMDb', fontsize=12)
    plt.ylabel('Rating Personal', fontsize=12)
    plt.title('Comparación: Rating IMDb vs Personal', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.tight_layout()

    # Crear directorio si no existe
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    output_path = IMAGES_DIR / 'rating_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Guardado: {output_path}")
    plt.close()


def plot_genres_by_platform():
    """Gráfico 3: Géneros por plataforma"""
    print("\n📊 Generando gráfico: Géneros por Plataforma...")

    results = cruce_3_genres_by_platform()

    if not results:
        print("⚠️  No se pudo generar el gráfico de géneros por plataforma")
        return

    # Preparar datos para gráfico
    platforms = []
    genres = []
    counts = []

    for platform, genre_list in results.items():
        for genre, count in genre_list[:3]:  # Top 3 por plataforma
            platforms.append(platform)
            genres.append(genre)
            counts.append(count)

    if not platforms:
        print("⚠️  No hay datos para graficar")
        return

    df = pd.DataFrame({
        'Platform': platforms,
        'Genre': genres,
        'Count': counts
    })

    # Crear gráfico de barras agrupadas
    fig, ax = plt.subplots(figsize=(12, 6))

    unique_platforms = df['Platform'].unique()
    x = range(len(unique_platforms))
    width = 0.25

    colors = ['#E50914', '#00A8E1', '#8A2BE2', '#FF6B6B']

    for i, platform in enumerate(unique_platforms):
        platform_data = df[df['Platform'] == platform]
        positions = [x[i] + (j - 1) * width for j in range(len(platform_data))]
        ax.bar(positions, platform_data['Count'], width, label=platform, color=colors[i % len(colors)])

    ax.set_xlabel('Plataforma', fontsize=12)
    ax.set_ylabel('Número de Películas', fontsize=12)
    ax.set_title('Top 3 Géneros por Plataforma de Streaming', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(unique_platforms)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    # Crear directorio si no existe
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    output_path = IMAGES_DIR / 'genres_by_platform.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Guardado: {output_path}")
    plt.close()


def generate_all_visualizations():
    """Genera todas las visualizaciones"""
    print("📊 GENERACIÓN DE VISUALIZACIONES")
    print("=" * 50)

    plot_top_netflix()
    plot_rating_comparison()
    plot_genres_by_platform()

    print("\n🎉 Visualizaciones completadas")
    print(f"Archivos guardados en: {IMAGES_DIR}")


if __name__ == "__main__":
    generate_all_visualizations()
