import pandas as pd
import matplotlib
matplotlib.use('Agg')  # <--- ДОДАТИ ЦЕ: Вмикаємо "безголовий" режим
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from src import config

# Налаштування логера
logger = logging.getLogger(__name__)


def create_visuals(file_path: Path) -> None:
    """
    Генерує графіки (EDA visualization) та зберігає їх у папку reports/figures.

    Args:
        file_path (Path): Шлях до файлу з даними.
    """
    logger.info(f"Starting Data Visualization for {file_path}...")

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return

    # --- Підготовка даних (Preprocessing for Viz) ---
    # Конвертуємо числові змінні
    df['amountValue_num'] = pd.to_numeric(df['amountValue'], errors='coerce')
    df['quantity_num'] = pd.to_numeric(df['quantity'], errors='coerce')

    # Видаляємо пропуски в ціні для коректної побудови графіків
    df_clean = df.dropna(subset=['amountValue_num'])

    # Встановлюємо загальний стиль графіків
    sns.set_style("whitegrid")

    # Переконуємось, що папка для графіків існує
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 40)
    print("GENERATING VISUALIZATIONS...")
    print("=" * 40)

    # ---------------------------------------------------------
    # 1. Гістограма розподілу вартості (Histogram)
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6))
    # Використовуємо логарифмічну шкалу, оскільки ціни можуть сильно відрізнятися
    sns.histplot(df_clean['amountValue_num'], kde=True, bins=30, log_scale=True)
    plt.title('Розподіл вартості активів (Log Scale)')
    plt.xlabel('Вартість (UAH, log scale)')
    plt.ylabel('Кількість записів')

    save_path = config.FIGURES_DIR / 'amount_distribution.png'
    plt.savefig(save_path)
    plt.close()
    print(f"[Saved] Histogram -> {save_path}")

    # ---------------------------------------------------------
    # 2. Box Plot (Ящик з вусами) для пошуку викидів
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df_clean['amountValue_num'])
    plt.title('Box Plot вартості активів (пошук викидів)')
    plt.xlabel('Вартість (UAH)')
    # Обмежимо вісь X, щоб графік був читабельним (до 95-го перцентиля),
    # але викиди все одно будуть враховані статистично
    plt.xscale('log')

    save_path = config.FIGURES_DIR / 'amount_boxplot.png'
    plt.savefig(save_path)
    plt.close()
    print(f"[Saved] Box Plot -> {save_path}")

    # ---------------------------------------------------------
    # 3. Pie Chart (Кругова діаграма) - Топ проєктів
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 8))

    # Беремо топ-5 проєктів, решту позначаємо як "Інші"
    top_n = 5
    project_counts = df['projectTitle'].value_counts()

    if len(project_counts) > top_n:
        top_projects = project_counts[:top_n]
        other_count = project_counts[top_n:].sum()
        top_projects['Інші (Others)'] = other_count
    else:
        top_projects = project_counts

    plt.pie(top_projects, labels=top_projects.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'Топ-{top_n} проєктів за кількістю передач')

    save_path = config.FIGURES_DIR / 'projects_pie_chart.png'
    plt.savefig(save_path)
    plt.close()
    print(f"[Saved] Pie Chart -> {save_path}")

    # ---------------------------------------------------------
    # 4. Теплокарта кореляцій (Correlation Heatmap)
    # ---------------------------------------------------------
    plt.figure(figsize=(8, 6))

    # Вибираємо тільки числові колонки
    numeric_df = df_clean[['amountValue_num', 'quantity_num']]

    # Рахуємо матрицю кореляцій
    corr_matrix = numeric_df.corr()

    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Матриця кореляцій числових змінних')

    save_path = config.FIGURES_DIR / 'correlation_heatmap.png'
    plt.savefig(save_path)
    plt.close()
    print(f"[Saved] Heatmap -> {save_path}")

    print("\n" + "=" * 40)
    logger.info("Data Visualization finished.")