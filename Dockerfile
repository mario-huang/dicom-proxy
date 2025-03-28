FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY config.json .

ENTRYPOINT ["python", "src/main.py"]