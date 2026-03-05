from src import config
from src import loader


def main():
    """
    Головна функція виконання пайплайну.
    """
    print("--- Open Data AI Analytics Pipeline ---")

    # Етап 1: Завантаження даних
    print("[Step 1] Data Loading...")
    try:
        loader.download_data(config.DATASET_URL, config.RAW_DATA_FILE_PATH)
    except Exception as e:
        print(f"Critical error at Data Loading stage: {e}")
        return  # Зупиняємо виконання, якщо завантаження не вдалось

    # Тут будуть наступні етапи:
    # print("[Step 2] Data Quality Analysis...")
    # quality.check(...)

    print("--- Pipeline finished successfully ---")


if __name__ == "__main__":
    main()