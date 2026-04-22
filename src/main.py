from src import config
from src.loader import loader
from src.loader.database import load_csv_to_postgres
from src.quality import quality
from src.research import research
from src.visualization import visualization  # <--- Додаємо імпорт visualization


def main():
    """
    Головна функція виконання пайплайну.
    """
    print("--- Open Data AI Analytics Pipeline ---")

    # Етап 1: Завантаження даних
    print("\n>>> [Step 1] Data Loading...")
    try:
        if not config.RAW_DATA_FILE_PATH.exists():
            loader.download_data(config.DATASET_URL, config.RAW_DATA_FILE_PATH)
        else:
            print("Data file already exists. Skipping download.")
    except Exception as e:
        print(f"Critical error at Data Loading stage: {e}")
        return

    # Етап 1.5: Збереження в Базу Даних
    print("\n>>> [Step 1.5] Loading data to PostgreSQL...")
    try:
        load_csv_to_postgres(config.RAW_DATA_FILE_PATH, config.DATABASE_URL, "assets_table")
    except Exception as e:
        print(f"Error at Database stage: {e}")

    # Етап 2: Аналіз якості даних
    print("\n>>> [Step 2] Data Quality Analysis...")
    try:
        quality.analyze_quality(config.RAW_DATA_FILE_PATH)
    except Exception as e:
        print(f"Error at Data Quality Analysis stage: {e}")

    # Етап 3: Дослідження даних (Research)
    print("\n>>> [Step 3] Data Research...")
    try:
        research.analyze_research(config.RAW_DATA_FILE_PATH)
    except Exception as e:
        print(f"Error at Data Research stage: {e}")

    # Етап 4: Візуалізація (Visualization)
    print("\n>>> [Step 4] Visualization...")
    try:
        visualization.create_visuals(config.RAW_DATA_FILE_PATH)
    except Exception as e:
        print(f"Error at Visualization stage: {e}")

    print("\n--- Pipeline finished successfully ---")


if __name__ == "__main__":
    main()