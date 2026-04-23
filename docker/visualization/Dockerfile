FROM python:3.11-slim
WORKDIR /app
COPY docker/visualization/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
ENV PYTHONPATH=/app
CMD ["python", "-c", "from src.visualization.visualization import create_visuals; from src import config; create_visuals(config.RAW_DATA_FILE_PATH)"]