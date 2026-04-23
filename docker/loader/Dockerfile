# Використовуємо офіційний легкий образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл із залежностями та встановлюємо їх
COPY docker/loader/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь вихідний код проєкту
COPY src/ ./src/

# Вказуємо змінну середовища для правильних імпортів
ENV PYTHONPATH=/app

# Команда запуску (Модуль завантаження)
# Використовуємо -c, щоб запустити специфічний скрипт, а не весь main.py
CMD ["python", "-c", "from src.loader import loader; from src import config; from src.loader.database import load_csv_to_postgres; loader.download_data(config.DATASET_URL, config.RAW_DATA_FILE_PATH); load_csv_to_postgres(config.RAW_DATA_FILE_PATH, config.DATABASE_URL, 'assets_table')"]