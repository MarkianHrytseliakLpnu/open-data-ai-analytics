# Звіт до лабораторної роботи №1

## 1. Огляд проєкту
Метою проєкту було створення автоматизованого конвеєра (pipeline) для обробки та аналізу відкритих даних про міжнародну технічну допомогу. Проєкт реалізовано мовою Python з використанням модульної архітектури.

## 2. Структура Workflow (Етапи роботи з даними)

Робота з даними розділена на 4 послідовні етапи, кожен з яких реалізований в окремому модулі пакету `src`:

### Етап 1: Завантаження даних (Data Load)
- **Модуль:** `src/loader.py`
- **Функціонал:** Скрипт перевіряє наявність локального файлу. Якщо файл відсутній, відбувається завантаження CSV-файлу з ресурсу data.gov.ua за допомогою бібліотеки `requests` (stream mode).
- **Результат:** Збережений файл `data/raw/assets.csv`.

### Етап 2: Аналіз якості (Data Quality Analysis)
- **Модуль:** `src/quality.py`
- **Функціонал:**
    - Перевірка розмірності датасету (shape).
    - Аналіз типів даних та пошук пропущених значень (missing values).
    - Виявлення повних дублікатів.
    - Пошук аномалій (outliers) у числових колонках за методом IQR (Interquartile Range).
- **Результат:** Звіт про якість даних у консолі.

### Етап 3: Дослідження даних (Data Research)
- **Модуль:** `src/research.py`
- **Функціонал:**
    - Аналіз розподілу категоріальних ознак (топ донорів, топ отримувачів).
    - Розрахунок кореляції між кількістю (`quantity`) та вартістю (`amountValue`).
    - Агрегація даних: підрахунок сумарних бюджетів по проєктах.
- **Результат:** Аналітичні інсайти у консолі.

### Етап 4: Візуалізація (Visualization)
- **Модуль:** `src/visualization.py`
- **Функціонал:** Генерація графіків за допомогою `matplotlib` та `seaborn`:
    1. **Histogram:** Розподіл вартості активів (Log scale).
    2. **Box Plot:** Візуалізація викидів вартості.
    3. **Pie Chart:** Частка топ-5 проєктів у загальній кількості допомоги.
    4. **Heatmap:** Матриця кореляцій числових змінних.
- **Результат:** PNG-файли, збережені у папці `reports/figures/`.

## 3. Методологія розробки (Git Flow)
Розробка велася з використанням системи контролю версій Git за стратегією Feature Branching:
1. Для кожного етапу створювалася окрема гілка (`feature/data_load`, `feature/data_research` тощо).
2. Після реалізації функціоналу гілка зливалася (merge) у `main`.
3. Використовувався файл `.gitignore` для виключення системних файлів (`.idea`, `__pycache__`) та "сирих" даних.

## 4. Історія змін (Git Graph)
Нижче наведено візуалізацію історії комітів проєкту:
```
PS C:\Users\Gil\PycharmProjects\open-data-ai-analytics> git log --oneline --graph --decorate --all
* 31eb3b8 (HEAD -> main, tag: v0.1.0) Changed: -CHANGELOG.md: added tag v0.1.0. -REPORT.md: added lab report
| * b65e992 (origin/feature/visualization, feature/visualization) Changed: -visualization.py: added method that makes graphs like corr heatmap, pie chart, boxplot and histogram -main.py: added visualization running script
|/
*   27ae025 (origin/main, origin/HEAD) Merge pull request #8 from MarkianHrytseliakLpnu/merge_conflict_2
|\
| *   0bf536f (origin/merge_conflict_2) Merge branch 'main' into merge_conflict_2
| |\
| |/
|/|
* |   77db80e Merge pull request #7 from MarkianHrytseliakLpnu/merge_conflict_1
|\ \
| * | 5e35910 (origin/merge_conflict_1, merge_conflict_1) Changed row to make merge conflict
|/ /
| * fe6d71a (merge_conflict_2) Changed row to make merge conflict
|/
*   7e1ba93 Merge pull request #6 from MarkianHrytseliakLpnu/feature/data_research
|\
| *   bfbf592 (origin/feature/data_research) Merge branch 'main' into feature/data_research
| |\
| |/
|/|
| | * bdfbfae (feature/data_research) Merge remote-tracking branch 'origin/main' into feature/data_research
| |/|
| |/
|/|
* |   aa782c9 Merge pull request #4 from MarkianHrytseliakLpnu/feature/data_quality_analisys
|\ \
| | * 199bc88 Changes: - research.py: added method that performs data research analysis - main.py: added research.py run script
| |/
|/|
| | * 31c1041 (feature/data_quality_analisys) Reverted changes
| | * 2b28cf5 (origin/feature/data_quality_analisys) Changes: - research.py: added method that performs data research analysis - main.py: added research.py run script  
| |/
| * 3c88db7 Changes: - quality.py: added method that performs data quality analysis - main.py: added quality.py run script
|/
*   6fd2767 Merge pull request #3 from MarkianHrytseliakLpnu/feature/data_load
|\
| * cd740fe (origin/feature/data_load, feature/data_load) Added: - config.py: renamed from .gitkeep, created configuration constants (file, url, etc.) - loader.py: method that uses requests lib to download dataset - main.py: runs script using config.py and loader.py
|/
*   ef49f53 Merge pull request #2 from MarkianHrytseliakLpnu/feature/data_load
|\
| *   b4e482b Merge pull request #1 from MarkianHrytseliakLpnu/main
| |\
| |/
|/|
* | ac9ab9e 1. Added: README.md .gitignore data/README.md notebooks/ src/ reports/figures/
|/
* 35db954 Delete .idea directory
* c69baa3 Changed README.md  - added topic  - url link to the dataset  - made 3 hypothesis/questions about data
* 01ad7c9 1. Added: README.md .gitignore data/README.md notebooks/ src/ reports/figures/
* a50e313 1. Added: README.md .gitignore data/README.md notebooks/ src/ reports/figures/
* 605c8aa Update README.md
* 80c72c0 1. Added: README.md .gitignore data/README.md notebooks/ src/ reports/figures/
* 50e73b4 Initial commit
(END)
* | ac9ab9e 1. Added: README.md .gitignore data/README.md notebooks/ src/ reports/figures/
|/
* 35db954 Delete .idea directory
* c69baa3 Changed README.md  - added topic  - url link to the dataset  - made 3 hypothesis/questions about data
* 01ad7c9 1. Added: README.md .gitignore data/README.md notebooks/ src/ reports/figures/
* a50e313 1. Added: README.md .gitignore data/README.md notebooks/ src/ reports/figures/
* 605c8aa Update README.md
* 80c72c0 1. Added: README.md .gitignore data/README.md notebooks/ src/ reports/figures/
* 50e73b4 Initial commit
```