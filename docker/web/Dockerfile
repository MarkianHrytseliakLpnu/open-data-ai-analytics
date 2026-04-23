FROM python:3.11-slim
WORKDIR /app
COPY docker/web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
ENV PYTHONPATH=/app
EXPOSE 8501
CMD ["streamlit", "run", "src/web/app.py", "--server.address", "0.0.0.0"]