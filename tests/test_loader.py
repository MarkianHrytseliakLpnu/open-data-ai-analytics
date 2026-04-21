from unittest.mock import patch, MagicMock
from src.loader.loader import download_data


@patch('src.loader.loader.requests.get')
def test_download_data(mock_get, tmp_path):
    # Імітуємо успішну відповідь від сервера
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content.return_value = [b"col1,col2\n", b"val1,val2\n"]
    mock_get.return_value = mock_response

    # Тимчасовий шлях для збереження
    save_path = tmp_path / "downloaded.csv"

    # Викликаємо функцію
    download_data("https://fake-url.com/data.csv", save_path)

    # Перевіряємо результати
    assert save_path.exists()
    assert save_path.read_bytes() == b"col1,col2\nval1,val2\n"