
# 🤖 ChatBot-AI Project

> AI 기반 챗봇 API 프로젝트입니다.  
> FastAPI 기반의 Office/Character API 서버와 Llama 기반 AI 모델을 Docker로 통합 운영합니다.


## 🏗️ 전체 아키텍처

- **office**: 업무용 챗봇 API (FastAPI, 8002)
- **character**: 캐릭터 챗봇 API (FastAPI, 8003)
- **nginx**: API Gateway (8001, reverse proxy, 커스텀 404 지원)
- **python-libs-init**: 공통 Python 라이브러리 볼륨 초기화


## 📂 주요 폴더 구조

```
ChatBot-AI/
├── fastapi/
│   ├── .dockerignore
│   ├── requirements.txt                # Python 패키지 의존성
│   ├── requirements_llama.txt          # Llama 모델 전용 의존성
│   ├── ai_model/                       # AI 모델 파일 및 설명
│   │   └── README.md
│   ├── batch/                          # 배치 스크립트
│   │   ├── venv_install.bat
│   │   └── venv_setup.bat
│   ├── certificates/                   # 인증서 관련 문서
│   │   ├── DNS_README.md
│   │   └── PEM_README.md
│   ├── logs/                           # 로그 파일 (공유 볼륨)
│   ├── prompt/                         # 프롬프트 설정
│   │   ├── config-Llama.json
│   │   └── config-OpenAI.json
│   ├── src/
│   │   ├── server-office/              # Office API 서버 (정보 제공)
│   │   │   ├── Dockerfile
│   │   │   ├── server.py
│   │   │   └── ... (utils, handlers, routers 등)
│   │   └── server-character/           # Character API 서버 (캐릭터 대화)
│   │       ├── Dockerfile
│   │       ├── server.py
│   │       └── ... (utils, handlers, routers 등)
│   ├── .env                            # 환경 변수 파일
│   └── bot.yaml                        # 봇 설정
├── nginx/
│   ├── nginx.conf                      # nginx 리버스 프록시 설정
│   └── 404.html                        # 커스텀 404 페이지
├── docker-compose.yml                  # 전체 서비스 오케스트레이션
└── README.md                           # 프로젝트 설명서
```


## 📋 UML 클래스 다이어그램 
### 📑 utils(ai_models) 클래스 다이어그램 
![Class-Diagram-ChatBot(AI)-utils(ai_models)](/images/Class-Diagram-ChatBot(AI)-utils(ai_models).webp)

### 📑 utils(handlers) 클래스 다이어그램 
![Class-Diagram-ChatBot(AI)-utils(handlers)](/images/Class-Diagram-ChatBot(AI)-utils(handlers).webp)

### 📑 utils(schemas) 클래스 다이어그램
![Class-Diagram-ChatBot(AI)-utils(schemas)](/images/Class-Diagram-ChatBot(AI)-utils(schemas).webp)

## 📋 UML 패키지 다이어그램 
![Package-Diagram-ChatBot(AI)](/images/Package-Diagram-ChatBot(AI).webp)


## 🚀 빠른 시작 (Docker 기반)

### 1. **필수 요구사항**
- Docker, docker-compose
- NVIDIA GPU 및 드라이버 (CUDA 12.1 이상)
- (선택) 호스트 시간대가 Asia/Seoul로 설정되어 있으면 nginx 로그도 한국 시간으로 기록됨

### 2. **AI 모델 파일 준비**
- `fastapi/ai_model/MLP-KTLim/`, `fastapi/ai_model/QuantFactory/` 등  
  필요한 모델 파일을 Hugging Face 등에서 다운로드 후 해당 폴더에 위치시킵니다.
- `.dockerignore`에 의해 모델 파일은 이미지에 포함되지 않고,  
  반드시 **볼륨 마운트**로만 사용됩니다.

### 3. **환경 변수 파일 준비**
- `fastapi/src/.env` 파일에 필요한 환경 변수(OPENAI_API_KEY 등) 입력

### 4. **커스텀 404 페이지 준비**
- `nginx/404.html` 파일을 원하는 디자인으로 작성

### 5. **컨테이너 빌드 및 실행**
```bash

docker compose up --build
```


## 🌐 API Gateway (nginx) 구조

- **8001 포트**에서 모든 API를 통합 제공
- `/office/` → office 서버(8002)로 프록시
- `/character/` → character 서버(8003)로 프록시
- 존재하지 않는 경로는 `/404.html` 커스텀 페이지 반환


## 📝 주요 nginx 설정

```nginx

events {}

http {
    # HTTP/1.1 강제 설정
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    
    upstream office_backend {
        server office:8002;
        keepalive 32;
    }
    
    upstream character_backend {
        server character:8003;
        keepalive 32;
    }

    server {
        listen 8001;
        
        # HTTP 버전 강제 설정
        http2 off;  # HTTP/2 비활성화

        # office API
        location ^~ /office/ {
            proxy_pass http://office_backend/;
            proxy_http_version 1.1;
            # ... 
            # 세부 설정 생략
            
            # 타임아웃 설정을 420초(7분)
            proxy_read_timeout 420s;
            proxy_connect_timeout 420s;
            proxy_send_timeout 420s;

            # 버퍼 설정 추가
            proxy_buffering off;
            proxy_request_buffering off;
        }

        # character API
        location ^~ /character/ {
            proxy_pass http://character_backend/;
            # ... 
            # 세부 설정 생략
            
            # 타임아웃 설정을 420초(7분)
            proxy_read_timeout 420s;
            proxy_connect_timeout 420s;
            proxy_send_timeout 420s;
            
            # 버퍼 설정 추가
            proxy_buffering off;
            proxy_request_buffering off;
        }

        # 404 커스텀 페이지
        error_page 404 /404.html;
        location = /404.html {
            root /etc/nginx/html;
            default_type text/html;
            internal;
        }

        location / {
            return 404;
        }
    }
}
```


## 📦 도커 볼륨/마운트 구조

- **공통 라이브러리**: `python-libs` 볼륨 (컨테이너간 공유)
- **모델 파일**: 호스트의 `fastapi/ai_model/` → 컨테이너 내부 `/app/fastapi/ai_model/`
- **로그**: 호스트의 `fastapi/logs/` → 컨테이너 내부 `/app/logs/`
- **nginx 404.html**: 호스트의 `nginx/404.html` → 컨테이너 `/etc/nginx/html/404.html`
<br><br>