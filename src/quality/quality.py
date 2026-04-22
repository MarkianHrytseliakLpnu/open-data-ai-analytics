import pandas as pd
import logging
import json
from pathlib import Path
from src import config


# Налаштування логера
logger = logging.getLogger(__name__)


def analyze_quality(file_path: Path) -> None:
    """
    Проводить аналіз якості даних (EDA) та формує JSON-звіт.

    Args:
        file_path (Path): Шлях до csv файлу з даними.
    """
    logger.info(f"Starting Data Quality Analysis for {file_path}...")

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return

    # Ініціалізація структури звіту
    report = {
        "dataset_shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "missing_values": {},
        "duplicates": {},
        "data_types_and_correctness": {}
    }

    # 1. Визначення кількості пропусків
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    report["missing_values"]["count"] = missing.to_dict()
    report["missing_values"]["percentage"] = ((missing / len(df)) * 100).round(2).to_dict()

    # 2. Перевірка на дублікати
    duplicates = int(df.duplicated().sum())
    report["duplicates"]["count"] = duplicates
    report["duplicates"]["percentage"] = round((duplicates / len(df)) * 100, 2)

    # 3. Перевірка типів та коректності значень
    type_info = {}
    correctness_issues = {}

    for col in df.columns:
        col_type = str(df[col].dtype)
        type_info[col] = col_type

        # Перевірка коректності: якщо колонка має бути числовою, але містить текст/пробіли
        if col_type == 'object' and col in ['amountValue', 'quantity']:
            # Шукаємо значення, які містять літери, коми або пробіли
            non_numeric = df[col].astype(str).str.contains(r'[^\d.]', na=False)
            issues_count = int(non_numeric.sum())
            if issues_count > 0:
                correctness_issues[
                    col] = f"Found {issues_count} values with invalid format (e.g. spaces, commas, letters)"

    report["data_types_and_correctness"]["types"] = type_info
    report["data_types_and_correctness"]["potential_issues"] = correctness_issues

    # 4. Формування звіту (Збереження у JSON)
    report_dir = config.QUALITY_REPORTS_DIR
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "quality_report.json"

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    logger.info(f"Data Quality Analysis finished. Report saved to {report_path}")

    # Виводимо прев'ю у консоль
    print("\n--- DATA QUALITY REPORT ---")
    print(json.dumps(report, indent=4, ensure_ascii=False))