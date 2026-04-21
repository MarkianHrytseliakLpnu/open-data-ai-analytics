from unittest.mock import patch
from src.main import main


@patch('src.main.config')
@patch('src.main.visualization.config')
@patch('src.main.loader.download_data')
def test_main_pipeline(mock_download, mock_viz_config, mock_main_config, dummy_data_path, tmp_path):
    # Встановлюємо шляхи конфігурації на наші тестові папки
    mock_main_config.RAW_DATA_FILE_PATH = dummy_data_path
    mock_main_config.DATASET_URL = "https://fake.url"
    mock_viz_config.FIGURES_DIR = tmp_path

    # Запускаємо головний пайплайн
    main()

    # Оскільки dummy_data_path.exists() == True, завантаження має бути пропущено
    mock_download.assert_not_called()

    # Перевіряємо, чи пайплайн дійшов до кінця і згенерував графіки
    assert (tmp_path / 'amount_distribution.png').exists()