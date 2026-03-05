import os
from pathlib import Path

# Визначаємо кореневу директорію проєкту (на 2 рівні вище від цього файлу)
PROJECT_ROOT = Path(__file__).parent.parent

# Шляхи до папок даних
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed" # На майбутнє
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

# Створюємо папки, якщо їх немає (безпечна перевірка)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# URL датасету (пряме посилання на CSV файл)
# Примітка: Я використав посилання на файл з ресурсу data.gov.ua.
# Якщо посилання зміниться, його треба оновити тут.
DATASET_URL = "https://data.gov.ua/dataset/2203c311-db7d-45ed-a933-64199c6934f2/resource/87a78723-8fe3-4d1b-bfa9-13a6ad010ac2/download/assets.csv"
DATASET_FILENAME = "assets.csv"

# Повний шлях до файлу, куди ми збережемо дані
RAW_DATA_FILE_PATH = RAW_DATA_DIR / DATASET_FILENAME