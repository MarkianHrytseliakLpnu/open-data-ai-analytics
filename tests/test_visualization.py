from src.visualization.visualization import create_visuals
from unittest.mock import patch


@patch('src.visualization.visualization.config')
def test_create_visuals(mock_config, dummy_data_path, tmp_path):
    # Підміняємо шлях збереження графіків на тимчасову папку
    mock_config.FIGURES_DIR = tmp_path

    create_visuals(dummy_data_path)

    # Перевіряємо, чи згенерувалися всі 4 файли
    assert (tmp_path / 'amount_distribution.png').exists()
    assert (tmp_path / 'amount_boxplot.png').exists()
    assert (tmp_path / 'projects_pie_chart.png').exists()
    assert (tmp_path / 'correlation_heatmap.png').exists()