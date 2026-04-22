import pandas as pd
import logging
import json
from pathlib import Path
import warnings
from src import config

# Ігноруємо попередження для чистоти виводу в консоль
warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)


def analyze_research(file_path: Path) -> None:
    """
    Виконує глибинний аналіз даних (статистики, розподіл) та формує JSON-звіт.
    """
    logger.info(f"Starting Data Research for {file_path}...")

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return

    # Структура майбутнього звіту
    report = {
        "basic_statistics": {},
        "categorical_distribution": {},
        "correlations": {},
        "key_insights": {}
    }

    # Попередня обробка: очищення даних для коректних обчислень
    if 'amountValue' in df.columns:
        df['amountValue_num'] = pd.to_numeric(
            df['amountValue'].astype(str).str.replace(r'\s+', '', regex=True).str.replace(',', '.'), errors='coerce')
    if 'quantity' in df.columns:
        df['quantity_num'] = pd.to_numeric(df['quantity'], errors='coerce')

    df_clean = df.dropna(subset=['amountValue_num'])

    # 1. Обчислення базових статистик та пошук викидів
    for col in ['amountValue_num', 'quantity_num']:
        if col in df.columns:
            stats = df[col].describe().to_dict()
            # Додаємо медіану
            stats['median'] = df[col].median()

            # Очищуємо від NaN та округлюємо
            clean_stats = {k: round(v, 2) if isinstance(v, float) else v for k, v in stats.items() if pd.notnull(v)}

            # Аутлаєри (За методом IQR)
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers_count = int(((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum())

            clean_stats["outliers_count"] = outliers_count
            report["basic_statistics"][col.replace('_num', '')] = clean_stats

    # 2. Категоріальний розподіл (Топ 5 відсотків)
    for col in ['projectTitle', 'implementerName', 'recipientName', 'amountCurrency']:
        if col in df.columns:
            counts = df[col].value_counts(normalize=True).head(5) * 100
            report["categorical_distribution"][col] = counts.round(2).to_dict()

    # 3. Кореляційний аналіз
    if 'quantity_num' in df_clean.columns and 'amountValue_num' in df_clean.columns:
        corr = df_clean[['amountValue_num', 'quantity_num']].corr().iloc[0, 1]
        if pd.notnull(corr):
            report["correlations"]["amount_vs_quantity"] = round(corr, 4)

    # 4. Базові агрегації (Інсайти)
    if 'projectTitle' in df_clean.columns:
        top_projects = df_clean.groupby('projectTitle')['amountValue_num'].sum().sort_values(ascending=False).head(3)
        report["key_insights"]["top_3_projects_by_amount_UAH"] = top_projects.round(2).to_dict()

    # Формування та збереження JSON-звіту
    report_dir = config.RESEARCH_REPORTS_DIR
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "research_report.json"

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    logger.info(f"Data Research finished. Report saved to {report_path}")

    # Виводимо прев'ю у консоль
    print("\n--- DATA RESEARCH REPORT ---")
    print(json.dumps(report, indent=4, ensure_ascii=False))