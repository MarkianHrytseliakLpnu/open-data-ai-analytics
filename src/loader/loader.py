import requests
import logging
from pathlib import Path

# Налаштування логування, щоб бачити, що відбувається
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_data(url: str, save_path: Path) -> None:
    """
    Завантажує файл за вказаним URL та зберігає його за вказаним шляхом.

    Args:
        url (str): Пряме посилання на файл.
        save_path (Path): Шлях, куди зберегти файл (включаючи ім'я файлу).
    """
    logger.info(f"Starting download from {url}...")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Викине помилку, якщо статус не 200 OK

        # Запис файлу частинами (chunk), щоб не забивати пам'ять, якщо файл великий
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"File successfully downloaded and saved to: {save_path}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download file. Error: {e}")
        raise e