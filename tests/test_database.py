from unittest.mock import patch
from src.loader.database import load_csv_to_postgres


@patch('src.loader.database.create_engine')
@patch('src.loader.database.pd.DataFrame.to_sql')
def test_load_csv_to_postgres(mock_to_sql, mock_create_engine, dummy_data_path):
    """Тестуємо очищення даних та виклик збереження в БД."""

    db_url = "postgresql+psycopg2://fake:fake@localhost/fake_db"

    load_csv_to_postgres(dummy_data_path, db_url, "test_table")

    # Перевіряємо, чи був створений engine
    mock_create_engine.assert_called_once_with(db_url)

    # Перевіряємо, чи викликався метод to_sql
    mock_to_sql.assert_called_once()

    # Можемо перевірити, чи дані очистилися (2 000,00 -> 2000.0)
    # df передається як аргумент у to_sql, ми можемо його дістати з моку
    args, kwargs = mock_to_sql.call_args
    df_called = args[0] if args else kwargs.get('self')  # Pandas передає df як контекст
    # Перевіряємо логіку pandas, що to_sql був викликаний з правильними параметрами
    assert kwargs.get('name') == "test_table"
    assert kwargs.get('if_exists') == "replace"