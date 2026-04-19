from src.quality.quality import analyze_quality


def test_analyze_quality(dummy_data_path, capsys):
    # Викликаємо функцію з нашим фейковим файлом
    analyze_quality(dummy_data_path)

    # Захоплюємо вивід у консоль
    captured = capsys.readouterr()

    # Перевіряємо наявність ключових маркерів у звіті
    assert "DATA QUALITY REPORT" in captured.out
    assert "SHAPE: 4 rows" in captured.out
    assert "MISSING VALUES" in captured.out