FROM python:3.11-slim
WORKDIR /app
COPY docker/quality/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
ENV PYTHONPATH=/app
CMD ["python", "-c", "from src.quality.quality import analyze_quality; from src import config; analyze_quality(config.RAW_DATA_FILE_PATH)"]