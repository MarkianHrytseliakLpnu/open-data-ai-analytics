import pandas as pd
import logging
from src import config
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, BigInteger, String, Float, Text
from pathlib import Path

logger = logging.getLogger(__name__)


def load_csv_to_postgres(csv_path: Path, db_url: str, table_name: str) -> None:
    logger.info(f"Starting database load process for table '{table_name}'...")

    if not csv_path.exists():
        raise FileNotFoundError(f"Missing file: {csv_path}")

    try:
        engine = create_engine(db_url)

        logger.info("Reading CSV file with pandas...")
        df = pd.read_csv(csv_path)

        # ==========================================
        # ЕТАП ОЧИЩЕННЯ ДАНИХ (DATA CLEANING)
        # ==========================================
        logger.info("Cleaning data formats before DB insertion...")

        # Очищуємо колонку amountValue (Вартість)
        if 'amountValue' in df.columns:
            # 1. Перетворюємо все на текст, щоб безпечно шукати символи
            df['amountValue'] = df['amountValue'].astype(str)
            # 2. Видаляємо всі пробіли (регулярний вираз \s+ шукає будь-які пробіли)
            df['amountValue'] = df['amountValue'].str.replace(r'\s+', '', regex=True)
            # 3. Замінюємо кому на крапку
            df['amountValue'] = df['amountValue'].str.replace(',', '.', regex=False)
            # 4. Безпечно перетворюємо назад у дробове число (помилки стануть NaN)
            df['amountValue'] = pd.to_numeric(df['amountValue'], errors='coerce')

        # Якщо в колонці кількості (quantity) теж є якісь текстові артефакти, чистимо і її
        if 'quantity' in df.columns:
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        # ==========================================

        db_dtypes = {
            'uid': BigInteger(),
            'name': String(255),
            'description': Text(),
            'quantity': Integer(),
            'unitName': String(50),
            'amountValue': Float(),
            'amountCurrency': String(10),
            'projectId': String(50),
            'projectTitle': Text(),
            'recipientId': Integer(),
            'recipientName': String(255),
            'implementerid': Float(),
            'implementerAddressAdminUnitL1': Float(),
            'implementerName': String(255),
            'actId': String(255),
            'actDate': String(50)
        }

        logger.info(f"Creating table '{table_name}' and writing {len(df)} rows...")

        with engine.begin() as connection:
            df.to_sql(
                name=table_name,
                con=connection,
                if_exists='replace',
                index=False,
                dtype=db_dtypes,
                chunksize=10000
            )

        logger.info(f"Table '{table_name}' successfully created and populated!")

    except Exception as e:
        logger.error(f"Failed to load data to database. Error: {e}")
        raise e

if __name__ == "__main__":
    load_csv_to_postgres(config.RAW_DATA_FILE_PATH, config.DATABASE_URL, "assets_table")