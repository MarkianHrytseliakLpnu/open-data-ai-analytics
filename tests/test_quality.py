import json
from unittest.mock import patch
from src.quality.quality import analyze_quality


@patch('src.quality.quality.config')
def test_analyze_quality(mock_config, dummy_data_path, tmp_path):
    """Тестуємо створення JSON звіту про якість."""
    # Підміняємо шлях у конфігу на тимчасову папку
    mock_report_dir = tmp_path / "reports" / "quality"
    mock_config.QUALITY_REPORTS_DIR = mock_report_dir

    analyze_quality(dummy_data_path)

    report_file = mock_report_dir / "quality_report.json"
    assert report_file.exists()

    with open(report_file, 'r', encoding='utf-8') as f:
        report = json.load(f)

    # Перевіряємо, чи звіт містить необхідні ключі
    assert "dataset_shape" in report
    assert "missing_values" in report
    assert "data_types_and_correctness" in report