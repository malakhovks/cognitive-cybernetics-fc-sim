FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "src.cli", "run", "--config", "config/main.yaml", "--scenario", "all", "--trials", "50"]
