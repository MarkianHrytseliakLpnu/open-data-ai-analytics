# Changelog

Всі зміни в проєкті "Open Data AI Analytics" будуть задокументовані в цьому файлі.

Формат базується на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
і цей проєкт дотримується [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.0] - 2026-03-27

### Added (Додано)
- **Unit Testing Suite (`tests/`):** Додано інфраструктуру для модульного тестування за допомогою `pytest`. Створено фікстури (`conftest.py`) та тести для всіх модулів (`test_loader.py`, `test_quality.py`, `test_research.py`, `test_visualization.py`).
- **Dependencies Management:** Створено файл `requirements.txt` для фіксації версій бібліотек (`pandas`, `pytest`, `seaborn` тощо), що забезпечує стабільність CI/CD.
- **GitHub-hosted CI/CD (`.github/workflows/ci.yml`):** Налаштовано хмарний конвеєр з паралельним тестуванням модулів (Matrix strategy) та розумним фільтром змін (`dorny/paths-filter`).
- **Self-hosted CI/CD (`.github/workflows/ci-selfhosted.yml`):** Додано гібридний пайплайн для виконання тестів на локальному Windows-сервері з подальшим розгортанням з хмари.
- **Continuous Deployment (CD):** Автоматизовано генерацію статичної HTML-сторінки з результатами аналізу (графіками) та її деплой на GitHub Pages.
- **Documentation:** Додано файл `REPORT.md` у папку reports/lab_2 – додано звіт до Лабораторної роботи №2 (опис CI/CD пайплайнів, розв'язання проблем та порівняння продуктивності раннерів).

### Fixed (Виправлено)
- **Matrix Scope Context:** Виправлено помилку `Unrecognized named-value: 'matrix'` у GitHub Actions шляхом перенесення логіки перевірки у змінні середовища (`env`).
- **Windows Runner EBUSY Bug:** Вирішено проблему блокування тимчасових папок (`_temp`) антивірусом/Git на локальному раннері шляхом заміни `actions/checkout@v4` на надійні (bulletproof) системні команди Git (`git clone`, `git fetch`, `git clean -fd`).

---

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