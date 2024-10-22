FROM python:3.10-bookworm

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY download_pretrained_weights.py .
RUN python download_pretrained_weights.py
COPY main.py .

ENTRYPOINT ["fastapi", "run"]
EXPOSE 8000