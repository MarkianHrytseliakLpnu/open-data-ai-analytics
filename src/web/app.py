import streamlit as st
import pandas as pd
import json
from pathlib import Path
from PIL import Image

# Налаштування сторінки
st.set_page_config(page_title="Open Data Analytics", page_icon="📊", layout="wide")

# Шляхи до файлів (відштовхуємось від кореня проєкту)
DATA_PATH = Path("data/raw/assets.csv")
QUALITY_REPORT_PATH = Path("reports/quality/quality_report.json")
RESEARCH_REPORT_PATH = Path("reports/research/research_report.json")
FIGURES_DIR = Path("reports/figures")


def load_json(path):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def main():
    # Бічне меню (Система посилань/навігації)
    st.sidebar.title("Навігація")
    page = st.sidebar.radio(
        "Перейти до сторінки:",
        ["🏠 Головна", "📂 Завантажені Дані", "🛠 Звіт щодо якості даних", "🔬 Звіт про дослідження даних", "📈 Візуалізації"]
    )

    # ---------------------------------------------------------
    # 1. ГОЛОВНА СТОРІНКА
    # ---------------------------------------------------------
    if page == "🏠 Головна":
        st.title("📊 Аналітика Міжнародної Технічної Допомоги")
        st.write("Ласкаво просимо до веб-інтерфейсу нашого пайплайну!")
        st.write("Використовуйте бічне меню ліворуч для перегляду результатів роботи модулів:")
        st.markdown("""
        * **Завантажені Дані** - Перегляд та фільтрація сирих даних.
        * **Звіт щодо якості даних** - Результати перевірки на дублікати, пропуски та помилки.
        * **Звіт про дослідження даних** - Базові статистики та інсайти.
        * **Візуалізації** - Графіки розподілу, аутлаєрів та кореляції.
        """)

    # ---------------------------------------------------------
    # 2. ЗАВАНТАЖЕНІ ДАНІ
    # ---------------------------------------------------------
    elif page == "📂 Завантажені Дані":
        st.title("📂 Завантажені Дані (Dataset)")

        if DATA_PATH.exists():
            df = pd.read_csv(DATA_PATH)
            st.success(f"Дані успішно завантажено! Розмір: {df.shape[0]} рядків, {df.shape[1]} колонок.")

            # Додаємо можливість розділити по категоріям (фільтр)
            columns = df.columns.tolist()
            selected_cols = st.multiselect("Оберіть колонки для відображення:", columns, default=columns[:7])

            # Відображення самої таблиці
            st.dataframe(df[selected_cols], use_container_width=True)
        else:
            st.error("Файл даних не знайдено. Спочатку запустіть пайплайн (main.py).")

    # ---------------------------------------------------------
    # 3. ЗВІТ ПРО ЯКІСТЬ
    # ---------------------------------------------------------
    elif page == "🛠 Звіт щодо якості даних":
        st.title("🛠 Результати перевірки якості даних")
        report = load_json(QUALITY_REPORT_PATH)

        if report:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Дублікатів знайдено", report["duplicates"]["count"])
            with col2:
                st.metric("Відсоток дублікатів", f"{report['duplicates']['percentage']}%")

            st.subheader("Пропущені значення (Missing Values)")
            st.json(report["missing_values"])

            st.subheader("Перевірка типів та помилки форматування")
            st.json(report["data_types_and_correctness"]["types"])
            st.json(report["data_types_and_correctness"]["potential_issues"])
        else:
            st.error("Звіт про якість не знайдено.")

    # ---------------------------------------------------------
    # 4. ЗВІТ З ДОСЛІДЖЕННЯ
    # ---------------------------------------------------------
    elif page == "🔬 Звіт про дослідження даних":
        st.title("🔬 Результати дослідження (Інсайти)")
        report = load_json(RESEARCH_REPORT_PATH)

        if report:
            st.subheader("Базові статистики")
            st.json(report["basic_statistics"])

            st.subheader("Ключові інсайти (Топ-3 проєкти за вартістю)")
            for proj, amount in report["key_insights"]["top_3_projects_by_amount_UAH"].items():
                st.write(f"- **{proj}**: {amount:,} UAH")

            st.subheader("Розподіл проєктів (%)")
            for proj, amount in report["categorical_distribution"]["projectTitle"].items():
                st.write(f"- **{proj}**: {amount:,} %")

            st.subheader("Розподіл за установами-імплементаторами (%)")
            for proj, amount in report["categorical_distribution"]["implementerName"].items():
                st.write(f"- **{proj}**: {amount:,} %")

            st.subheader("Кореляція")
            st.write(report["correlations"])
        else:
            st.error("Звіт з дослідження не знайдено.")

    # ---------------------------------------------------------
    # 5. ВІЗУАЛІЗАЦІЇ
    # ---------------------------------------------------------
    elif page == "📈 Візуалізації":
        st.title("📈 Графіки та Візуалізації")

        if FIGURES_DIR.exists():
            # Отримуємо список всіх картинок
            images = [f.name for f in FIGURES_DIR.glob("*.png")]

            if images:
                # Окремі посилання (через селектор) на кожен графік
                selected_image = st.selectbox("Оберіть графік для перегляду:", images)

                img_path = FIGURES_DIR / selected_image
                img = Image.open(img_path)
                st.image(img, caption=selected_image, width=800)
            else:
                st.warning("Графіків ще немає в папці.")
        else:
            st.error("Папку з графіками не знайдено.")


if __name__ == "__main__":
    main()