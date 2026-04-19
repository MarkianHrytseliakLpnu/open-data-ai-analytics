import pandas as pd
import logging
from pathlib import Path
import warnings

# Ігноруємо попередження для чистоти виводу в консоль
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


def analyze_research(file_path: Path) -> None:
    """
    Виконує глибинний аналіз даних: кореляції, розподіл категорій, групування.
    """
    logger.info(f"Starting Data Research for {file_path}...")

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return

    # --- Pre-processing for Research (Конвертація типів) ---
    # Для кореляції нам потрібні числа. Конвертуємо, ігноруючи помилки ('coerce')
    df['amountValue_num'] = pd.to_numeric(df['amountValue'], errors='coerce')
    df['quantity_num'] = pd.to_numeric(df['quantity'], errors='coerce')

    # Видаляємо рядки, де не вдалось конвертувати ціну (для чистоти статистики)
    df_clean = df.dropna(subset=['amountValue_num'])

    print("\n" + "=" * 40)
    print("DATA RESEARCH REPORT")
    print("=" * 40)

    # 1. Аналіз категоріальних ознак (Збалансованість класів)
    print("\n[1] CATEGORICAL DISTRIBUTION (Top 5):")

    categorical_cols = ['projectTitle', 'implementerName', 'recipientName', 'amountCurrency']

    for col in categorical_cols:
        if col in df.columns:
            print(f"\n--- Distribution for '{col}' ---")
            counts = df[col].value_counts(normalize=True).head(5) * 100
            for name, pct in counts.items():
                # Обрізаємо довгі назви для красивого виводу
                short_name = (name[:50] + '..') if isinstance(name, str) and len(name) > 50 else name
                print(f"{short_name:<55} : {pct:.2f}%")

    # 2. Кореляційний аналіз
    print("\n[2] NUMERIC CORRELATION:")
    if 'quantity_num' in df_clean.columns and 'amountValue_num' in df_clean.columns:
        # Кореляція Пірсона
        corr = df_clean[['amountValue_num', 'quantity_num']].corr().iloc[0, 1]
        print(f"Correlation between Amount and Quantity: {corr:.4f}")

        if abs(corr) < 0.3:
            print(">> Interpretation: Very weak or no linear relationship.")
        elif abs(corr) < 0.7:
            print(">> Interpretation: Moderate relationship.")
        else:
            print(">> Interpretation: Strong relationship.")
    else:
        print("Not enough numeric data for correlation.")

    # 3. Групування та агрегація (Інсайти)
    print("\n[3] KEY INSIGHTS (Aggregation):")

    # Топ-3 проєкти за загальною вартістю активів
    if 'projectTitle' in df_clean.columns:
        print("\n--- Top 3 Projects by Total Budget (amountValue) ---")
        top_projects = df_clean.groupby('projectTitle')['amountValue_num'].sum().sort_values(ascending=False).head(3)
        for proj, total in top_projects.items():
            print(f"{proj[:60]:<60} : {total:,.2f} UAH (approx)")

    # Середня вартість одиниці техніки по виконавцях
    if 'implementerName' in df_clean.columns:
        print("\n--- Average Asset Value by Implementer (Top 3) ---")
        avg_cost = df_clean.groupby('implementerName')['amountValue_num'].mean().sort_values(ascending=False).head(3)
        for impl, mean_val in avg_cost.items():
            print(f"{impl[:60]:<60} : {mean_val:,.2f}")

    print("\n" + "=" * 40)
    logger.info("Data Research finished.")