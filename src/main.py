from src import config
from src import loader
from src import research  
from src import quality


def main():
    """
    Головна функція виконання пайплайну.
    """
    print("--- Open Data AI Analytics Pipeline ---")

    # Етап 1: Завантаження даних
    print("\n>>> [Step 1] Data Loading...")
    try:
        # Перевіряємо, чи файл вже існує, щоб не качати щоразу (опціонально)
        if not config.RAW_DATA_FILE_PATH.exists():
            loader.download_data(config.DATASET_URL, config.RAW_DATA_FILE_PATH)
        else:
            print("Data file already exists. Skipping download.")
    except Exception as e:
        print(f"Critical error at Data Loading stage: {e}")
        return
      
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

    # Тут будуть наступні етапи:
    # print("\n>>> [Step 4] Visualization...")
    # visualization.create_visuals(...)

    print("\n--- Pipeline finished successfully ---")

if __name__ == "__main__":
    main()