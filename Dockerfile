FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 및 필수 정적 파일만 복사 (markdown, csv, videos 등은 docker-compose 볼륨으로 마운트)
COPY src/ ./src/
COPY static/ ./static/
COPY images/ ./images/

# SSL 인증서용 디렉터리 생성 및 복사
RUN mkdir -p /app/certificates
COPY src/certificates/ ./certificates/

EXPOSE 8000

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]