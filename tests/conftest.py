import pytest
import pandas as pd


@pytest.fixture
def dummy_data_path(tmp_path):
    """
    Створює тимчасовий CSV файл з фейковими даними для тестів.
    Цей файл автоматично видаляється після завершення тесту.
    """
    df = pd.DataFrame({
        'uid': ['101', '102', '103', '104'],
        'name': ['Апарат 1', 'Апарат 2', 'Апарат 3', 'Апарат 4'],
        'description': ['Опис 1', 'Опис 2', 'Опис 3', 'Опис 4'],
        'quantity': ['1', '5', 'invalid', '2'],
        'unitName': ['шт.', 'шт.', 'шт.', 'шт.'],
        'amountValue': ['100.50', '200', 'invalid_string', '150'],
        'amountCurrency': ['UAH', 'UAH', 'UAH', 'USD'],
        'projectId': ['P1', 'P2', 'P1', 'P3'],
        'projectTitle': ['Проєкт А', 'Проєкт Б', 'Проєкт А', 'Проєкт В'],
        'recipientId': [1, 2, 1, 3],
        'recipientName': ['Отримувач X', 'Отримувач Y', 'Отримувач X', 'Отримувач Z'],
        'implementerName': ['Виконавець 1', 'Виконавець 2', 'Виконавець 1', 'Виконавець 3'],
        'actDate': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']
    })

    file_path = tmp_path / "test_assets.csv"
    df.to_csv(file_path, index=False)

    return file_path