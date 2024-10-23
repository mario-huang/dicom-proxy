FROM python:bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY config.json .

ENTRYPOINT ["python", "src/main.py"]