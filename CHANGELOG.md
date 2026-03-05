# Changelog

Всі зміни в проєкті "Open Data AI Analytics" будуть задокументовані в цьому файлі.

Формат базується на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
і цей проєкт дотримується [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.1.0] - 2026-03-05

### Added (Додано)
- **Data Pipeline Core:** Реалізовано базову архітектуру пайплайну в `src/main.py`.
- **Data Loader (`src/loader.py`):** Модуль для автоматичного завантаження dataset з data.gov.ua.
- **Quality Analysis (`src/quality.py`):** Скрипт для перевірки типів даних, дублікатів та пропущених значень.
- **Data Research (`src/research.py`):** Модуль для статистичного аналізу, кореляцій та агрегації даних.
- **Visualization (`src/visualization.py`):** Генерація графіків (Histogram, Boxplot, Pie Chart, Heatmap) з використанням `seaborn`.
- **Configuration:** Файл `src/config.py` для керування шляхами та константами.
- **Structure:** Налаштовано `.gitignore` для Python та JetBrains IDE.

### Changed (Змінено)
- Оновлено `README.md` з описом структури проєкту.