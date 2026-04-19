import pandas as pd
import logging
from pathlib import Path

# Налаштування логера
logger = logging.getLogger(__name__)


def analyze_quality(file_path: Path) -> None:
    """
    Проводить аналіз якості даних (EDA) та виводить звіт у консоль.

    Args:
        file_path (Path): Шлях до csv файлу з даними.
    """
    logger.info(f"Starting Data Quality Analysis for {file_path}...")

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return

    print("\n" + "=" * 40)
    print("DATA QUALITY REPORT")
    print("=" * 40)

    # 1. Загальна інформація
    print(f"\n[1] SHAPE: {df.shape[0]} rows, {df.shape[1]} columns")

    print("\n[2] DATA TYPES & INFO:")
    print(df.info())

    # 2. Перевірка на дублікати
    duplicates = df.duplicated().sum()
    print(f"\n[3] DUPLICATES: {duplicates} ({(duplicates / len(df)) * 100:.2f}%)")

    # 3. Аналіз пропущених значень
    print("\n[4] MISSING VALUES:")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print("No missing values found.")
    else:
        print(missing)
        print("\nMissing values percentage:")
        print((missing / len(df)) * 100)

    # 4. Унікальні значення (Cardinality)
    print("\n[5] UNIQUE VALUES (Cardinality):")
    for col in df.columns:
        print(f"{col}: {df[col].nunique()} unique values")

    # 5. Спроба конвертації числових колонок для статистики
    # (Ми знаємо, що amountValue та quantity часто зчитуються як об'єкти)
    print("\n[6] NUMERIC STATISTICS & OUTLIERS (Potential):")

    numeric_candidates = ['amountValue', 'quantity']

    for col in numeric_candidates:
        if col in df.columns:
            # Спробуємо тимчасово конвертувати в числа, ігноруючи помилки, щоб оцінити розподіл
            numeric_series = pd.to_numeric(df[col], errors='coerce')
            valid_count = numeric_series.count()

            print(f"\n--- Analysis for '{col}' ---")
            print(f"Valid numeric values: {valid_count} / {len(df)}")

            if valid_count > 0:
                print(numeric_series.describe())

                # Пошук аутлаєрів (IQR Method)
                Q1 = numeric_series.quantile(0.25)
                Q3 = numeric_series.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = numeric_series[(numeric_series < lower_bound) | (numeric_series > upper_bound)]
                print(f"Outliers count (IQR method): {len(outliers)}")
                if len(outliers) > 0:
                    print(f"Top 5 outliers: {outliers.nlargest(5).values}")

    print("\n" + "=" * 40)
    logger.info("Data Quality Analysis finished.")