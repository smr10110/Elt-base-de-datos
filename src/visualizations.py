"""
Genera visualizaciones de los resultados de los cruces MongoDB + Redis
"""

import matplotlib.pyplot as plt
import pandas as pd
from integration import cruce_1_top_movies_netflix, cruce_2_trending_by_genre, cruce_3_classics_latam
from pathlib import Path

# Obtener la ruta raíz del proyecto (un nivel arriba de src)
PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_ROOT / 'docs' / 'images'


def plot_top_netflix():
    """Gráfico 1: Top 10 películas en Netflix con comparación IMDb vs Usuarios"""
    print("\n📊 Generando gráfico: Top Netflix IMDb vs Usuarios...")

    df = cruce_1_top_movies_netflix()

    if df is None or len(df) == 0:
        print("⚠️  No se pudo generar el gráfico de Netflix")
        return

    # Crear figura con subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Comparación de ratings
    x = range(len(df))
    width = 0.35

    ax1.barh([i - width/2 for i in x], df['imdb_rating'], width,
             label='IMDb', color='#F5C518', alpha=0.8)
    ax1.barh([i + width/2 for i in x], df['user_rating'], width,
             label='Usuarios', color='#E50914', alpha=0.8)

    ax1.set_yticks(x)
    ax1.set_yticklabels(df['name'], fontsize=9)
    ax1.set_xlabel('Rating', fontsize=11)
    ax1.set_title('Top 10 en Netflix: Comparación de Ratings', fontsize=12, fontweight='bold')
    ax1.set_xlim(0, 10)
    ax1.legend(loc='lower right')
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()

    # Subplot 2: Diferencia de ratings
    colors = ['#2ecc71' if diff >= 0 else '#e74c3c' for diff in df['difference']]
    ax2.barh(df['name'], df['difference'], color=colors, alpha=0.7)
    ax2.set_xlabel('Diferencia (Usuarios - IMDb)', fontsize=11)
    ax2.set_title('Diferencia entre Ratings', fontsize=12, fontweight='bold')
    ax2.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()

    plt.tight_layout()

    # Guardar
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = IMAGES_DIR / 'top_netflix.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Guardado: {output_path}")
    plt.close()


def plot_trending_genres():
    """Gráfico 2: Géneros más trending según usuarios"""
    print("\n📊 Generando gráfico: Géneros Trending...")

    df = cruce_2_trending_by_genre()

    if df is None or len(df) == 0:
        print("⚠️  No se pudo generar el gráfico de géneros trending")
        return

    # Crear figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Cantidad de películas por género
    colors_palette = plt.cm.viridis(range(len(df)))
    ax1.barh(df['genre'], df['count'], color=colors_palette, alpha=0.8)
    ax1.set_xlabel('Número de Películas Trending', fontsize=11)
    ax1.set_ylabel('Género', fontsize=11)
    ax1.set_title('Géneros Más Trending (por cantidad)', fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()

    # Añadir valores en las barras
    for i, (genre, count) in enumerate(zip(df['genre'], df['count'])):
        ax1.text(count + 0.1, i, str(count), va='center', fontsize=9)

    # Subplot 2: Vistas promedio por género
    ax2.barh(df['genre'], df['avg_views'], color=colors_palette, alpha=0.8)
    ax2.set_xlabel('Vistas Promedio', fontsize=11)
    ax2.set_title('Géneros Trending (por popularidad)', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()

    # Formatear vistas con comas
    for i, (genre, views) in enumerate(zip(df['genre'], df['avg_views'])):
        ax2.text(views + 100, i, f'{views:,.0f}', va='center', fontsize=9)

    plt.tight_layout()

    # Guardar
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = IMAGES_DIR / 'trending_genres.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Guardado: {output_path}")
    plt.close()


def plot_classics_latam():
    """Gráfico 3: Clásicos más populares en LATAM"""
    print("\n📊 Generando gráfico: Clásicos en LATAM...")

    df = cruce_3_classics_latam()

    if df is None or len(df) == 0:
        print("⚠️  No se pudo generar el gráfico de clásicos LATAM")
        return

    # Crear figura con múltiples visualizaciones
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # Subplot 1: Top 10 clásicos por vistas
    ax1 = fig.add_subplot(gs[0, :])
    top_10 = df.nlargest(10, 'views')
    colors_views = plt.cm.RdYlGn(top_10['views'] / top_10['views'].max())

    ax1.barh(top_10['name'], top_10['views'], color=colors_views, alpha=0.8)
    ax1.set_xlabel('Vistas en últimos 30 días', fontsize=11)
    ax1.set_title('Top 10 Clásicos Más Vistos en LATAM', fontsize=13, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()

    # Añadir años
    for i, (name, views, year) in enumerate(zip(top_10['name'], top_10['views'], top_10['year'])):
        ax1.text(views + 100, i, f'{views:,} ({int(year)})', va='center', fontsize=8)

    # Subplot 2: Distribución por década
    ax2 = fig.add_subplot(gs[1, 0])
    df['decade'] = (df['year'] // 10) * 10
    decade_counts = df['decade'].value_counts().sort_index()

    ax2.bar(decade_counts.index.astype(str), decade_counts.values,
            color='#3498db', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Década', fontsize=11)
    ax2.set_ylabel('Número de Películas', fontsize=11)
    ax2.set_title('Clásicos por Década', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

    # Subplot 3: Distribución por plataforma
    ax3 = fig.add_subplot(gs[1, 1])
    platform_counts = df['platform'].value_counts()

    colors_platform = ['#E50914', '#00A8E1', '#8A2BE2', '#FF6B6B'][:len(platform_counts)]
    wedges, texts, autotexts = ax3.pie(platform_counts.values,
                                         labels=platform_counts.index,
                                         autopct='%1.1f%%',
                                         colors=colors_platform,
                                         startangle=90)

    ax3.set_title('Clásicos por Plataforma', fontsize=12, fontweight='bold')

    # Mejorar legibilidad
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    plt.tight_layout()

    # Guardar
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = IMAGES_DIR / 'classics_latam.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Guardado: {output_path}")
    plt.close()


def plot_summary_dashboard():
    """Gráfico 4: Dashboard resumen de todos los cruces"""
    print("\n📊 Generando dashboard resumen...")

    # Ejecutar cruces
    df_netflix = cruce_1_top_movies_netflix()
    df_genres = cruce_2_trending_by_genre()
    df_classics = cruce_3_classics_latam()

    if df_netflix is None or df_genres is None or df_classics is None:
        print("⚠️  No se pudo generar el dashboard (faltan datos)")
        return
    if len(df_netflix)==0 or len(df_genres)==0 or len(df_classics)==0:
        print("??  No se pudo generar el dashboard (datasets vac?os)")
        return

    # Crear dashboard
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Dashboard Resumen: Cruces MongoDB + Redis',
                 fontsize=16, fontweight='bold', y=0.98)

    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

    # 1. Rating promedio por fuente
    ax1 = fig.add_subplot(gs[0, 0])
    sources = ['IMDb', 'Usuarios']
    avg_ratings = [df_netflix['imdb_rating'].mean(), df_netflix['user_rating'].mean()]
    colors = ['#F5C518', '#E50914']

    ax1.bar(sources, avg_ratings, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Rating Promedio', fontsize=10)
    ax1.set_title('Ratings: IMDb vs Usuarios', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 10)
    ax1.grid(axis='y', alpha=0.3)

    for i, (source, rating) in enumerate(zip(sources, avg_ratings)):
        ax1.text(i, rating + 0.2, f'{rating:.2f}', ha='center', fontweight='bold')

    # 2. Top 5 géneros trending
    ax2 = fig.add_subplot(gs[0, 1])
    top_5_genres = df_genres.nlargest(5, 'count')
    ax2.barh(top_5_genres['genre'], top_5_genres['count'], color='#9b59b6', alpha=0.7)
    ax2.set_xlabel('Películas', fontsize=10)
    ax2.set_title('Top 5 Géneros Trending', fontsize=11, fontweight='bold')
    ax2.invert_yaxis()
    ax2.grid(axis='x', alpha=0.3)

    # 3. Vistas totales
    ax3 = fig.add_subplot(gs[0, 2])
    total_views_netflix = df_netflix['views'].sum()
    total_views_classics = df_classics['views'].sum()

    categories = ['Netflix\nTop 10', 'Clásicos\nLATAM']
    views = [total_views_netflix, total_views_classics]
    colors = ['#E50914', '#3498db']

    ax3.bar(categories, views, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_ylabel('Vistas Totales', fontsize=10)
    ax3.set_title('Vistas Totales por Categoría', fontsize=11, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)

    for i, (cat, view) in enumerate(zip(categories, views)):
        ax3.text(i, view + 1000, f'{view:,}', ha='center', fontweight='bold', fontsize=9)

    # 4. Distribución de diferencias IMDb vs Usuarios
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.hist(df_netflix['difference'], bins=10, color='#16a085', alpha=0.7, edgecolor='black')
    ax4.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Sin diferencia')
    ax4.set_xlabel('Diferencia (Usuarios - IMDb)', fontsize=10)
    ax4.set_ylabel('Frecuencia', fontsize=10)
    ax4.set_title('Distribución de Diferencias de Rating', fontsize=11, fontweight='bold')
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)

    # 5. Clásicos: Favoritos vs Vistas
    ax5 = fig.add_subplot(gs[1, 1])
    scatter = ax5.scatter(df_classics['views'], df_classics['favorites'],
                          c=df_classics['year'], cmap='viridis',
                          s=100, alpha=0.6, edgecolors='black')
    ax5.set_xlabel('Vistas', fontsize=10)
    ax5.set_ylabel('Favoritos', fontsize=10)
    ax5.set_title('Clásicos: Relación Vistas-Favoritos', fontsize=11, fontweight='bold')
    ax5.grid(True, alpha=0.3)

    # Colorbar para años
    cbar = plt.colorbar(scatter, ax=ax5)
    cbar.set_label('Año', fontsize=9)

    # 6. Métricas clave
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')

    metrics_text = f"""
    MÉTRICAS CLAVE
    {'='*30}

    Netflix Top 10:
    • Películas: {len(df_netflix)}
    • Rating IMDb promedio: {df_netflix['imdb_rating'].mean():.2f}
    • Rating usuarios promedio: {df_netflix['user_rating'].mean():.2f}
    • Vistas totales: {df_netflix['views'].sum():,}

    Géneros Trending:
    • Géneros únicos: {len(df_genres)}
    • Género más popular: {df_genres.iloc[0]['genre']}
    • Vistas totales: {df_genres['total_views'].sum():,}

    Clásicos LATAM:
    • Películas disponibles: {len(df_classics)}
    • Década promedio: {int(df_classics['year'].mean())}s
    • Vistas promedio: {df_classics['views'].mean():,.0f}
    • Favoritos promedio: {df_classics['favorites'].mean():,.0f}
    """

    ax6.text(0.1, 0.5, metrics_text, fontsize=9,
             verticalalignment='center', family='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

    # Guardar
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = IMAGES_DIR / 'dashboard_summary.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Guardado: {output_path}")
    plt.close()


def generate_all_visualizations():
    """Genera todas las visualizaciones de los cruces"""
    print("=" * 70)
    print("📊 GENERACIÓN DE VISUALIZACIONES")
    print("=" * 70)

    # Generar cada visualización
    plot_top_netflix()
    plot_trending_genres()
    plot_classics_latam()
    plot_summary_dashboard()

    print("\n" + "=" * 70)
    print("🎉 VISUALIZACIONES COMPLETADAS")
    print("=" * 70)
    print(f"📁 Archivos guardados en: {IMAGES_DIR}")
    print("\nArchivos generados:")
    print("  1. top_netflix.png - Comparación ratings IMDb vs Usuarios")
    print("  2. trending_genres.png - Géneros más trending")
    print("  3. classics_latam.png - Clásicos populares en LATAM")
    print("  4. dashboard_summary.png - Dashboard resumen completo")
    print("=" * 70)


if __name__ == "__main__":
    generate_all_visualizations()
