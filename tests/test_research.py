from src.research import analyze_research


def test_analyze_research(dummy_data_path, capsys):
    analyze_research(dummy_data_path)

    captured = capsys.readouterr()

    assert "DATA RESEARCH REPORT" in captured.out
    assert "CATEGORICAL DISTRIBUTION" in captured.out
    assert "KEY INSIGHTS" in captured.out