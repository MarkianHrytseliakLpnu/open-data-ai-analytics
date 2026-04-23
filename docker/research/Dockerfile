FROM python:3.11-slim
WORKDIR /app
COPY docker/research/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
ENV PYTHONPATH=/app
CMD ["python", "-c", "from src.research.research import analyze_research; from src import config; analyze_research(config.RAW_DATA_FILE_PATH)"]