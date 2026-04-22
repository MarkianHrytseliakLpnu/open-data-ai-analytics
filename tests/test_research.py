import json
from unittest.mock import patch
from src.research.research import analyze_research


@patch('src.research.research.config')
def test_analyze_research(mock_config, dummy_data_path, tmp_path):
    """Тестуємо розрахунок статистик та створення JSON звіту."""
    # Підміняємо шлях у конфігу на тимчасову папку
    mock_report_dir = tmp_path / "reports" / "research"
    mock_config.RESEARCH_REPORTS_DIR = mock_report_dir

    analyze_research(dummy_data_path)

    report_file = mock_report_dir / "research_report.json"
    assert report_file.exists()

    with open(report_file, 'r', encoding='utf-8') as f:
        report = json.load(f)

    # Перевіряємо, чи сформувались секції зі статистикою
    assert "basic_statistics" in report
    assert "amountValue" in report["basic_statistics"]
    assert "categorical_distribution" in report