# Portfolio - 서정훈 백엔드 개발자 포트폴리오

Python, FastAPI, Docker, NginX를 활용한 백엔드 개발자 포트폴리오 웹사이트입니다.

## 🚀 빠른 시작 (Docker)

### 사전 준비사항
- Docker & Docker Compose 설치
- SSL 인증서 파일 (`src/certificates/` 디렉토리에 위치)
  - `cutwire.myddns.me-fullchain.pem` (인증서 체인 포함)
  - `cutwire.myddns.me-key.pem` (개인키)

### 배포 방법

```bash
# 1. 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 값 입력

# 2. 배포 스크립트 실행 권한 부여
chmod +x deploy.sh

# 3. 이미지 빌드 및 컨테이너 시작
./deploy.sh build
./deploy.sh up

# 4. 상태 확인
./deploy.sh status
```

### 접속 주소
- **HTTPS**: https://cutwire.myddns.me (메인)
- **HTTP**: http://cutwire.myddns.me (자동으로 HTTPS로 리다이렉트)

### 유용한 명령어
```bash
./deploy.sh logs      # 실시간 로그 확인
./deploy.sh restart   # 컨테이너 재시작
./deploy.sh down      # 컨테이너 중지
./deploy.sh status    # 상태 확인
./deploy.sh ssl-renew # SSL 인증서 갱신 안내
```

## 🏗️ 아키텍처

```
┌─────────────────┐     ┌─────────────────┐
│   Client        │────▶│   Nginx (80/443)│
│   (Browser)     │     │   Reverse Proxy │
└─────────────────┘     └────────┬────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
            ┌───────────────┐         ┌───────────────┐
            │ Static Files  │         │ FastAPI App   │
            │ (CSS, JS,     │         │ (Port 8000)   │
            │  Images)      │         │               │
            └───────────────┘         └───────────────┘
```

### 구성 요소
- **Nginx**: SSL 종료, HTTP→HTTPS 리다이렉트, 정적 파일 서빙, 리버스 프록시
- **FastAPI (Hypercorn)**: 백엔드 API 서버, 동적 라우팅 처리
- **Docker Compose**: 멀티 컨테이너 오케스트레이션

## 🔒 SSL/HTTPS 설정

### 인증서 갱신 (Let's Encrypt)
인증서는 호스트에서 `win-acme` (Windows) 또는 `certbot` (Linux)로 갱신하세요.

```bash
# 인증서 갱신 후
./deploy.sh restart
```

### 인증서 파일 구조
```
src/certificates/
├── cutwire.myddns.me-fullchain.pem  # 전체 체인 (서버 인증서 + 중간 인증서)
├── cutwire.myddns.me-key.pem        # 개인키
├── cutwire.myddns.me-chain.pem      # 중간 인증서만
├── cutwire.myddns.me-crt.pem        # 서버 인증서만
└── isrgrootx1.pem                   # 루트 인증서
```

## 📁 프로젝트 구조

```
portfolio/
├── Dockerfile              # FastAPI 앱 Docker 이미지
├── docker-compose.yml      # 멀티 컨테이너 구성
├── deploy.sh               # 배포 자동화 스크립트
├── .env.example            # 환경 변수 템플릿
├── .dockerignore           # Docker 빌드 제외 파일
├── nginx/
│   └── nginx.conf          # Nginx 설정 (SSL, 프록시, 정적 파일)
├── src/
│   ├── main.py             # FastAPI 앱 진입점
│   ├── requirements.txt    # Python 의존성
│   ├── certificates/       # SSL 인증서 (gitignore 권장)
│   └── app/                # 애플리케이션 코드
├── static/                 # 정적 파일 (CSS, JS, HTML)
├── images/                 # 이미지 파일
├── markdown/               # 마크다운 콘텐츠
└── logs/                   # 로그 디렉토리
```

## 🛠️ 개발 환경

### 로컬 개발 (HTTPS 없이)
```bash
cd src
pip install -r requirements.txt
USE_SSL=false python main.py
# http://localhost:8000 접속
```

### 환경 변수
| 변수 | 기본값 | 설명 |
|------|--------|------|
| `USE_SSL` | `true` | SSL 사용 여부 |
| `PORT` | `8000` | 서버 포트 |
| `HOST` | `0.0.0.0` | 바인딩 호스트 |
| `KEY_PEM` | - | SSL 개인키 파일명 |
| `CRT_PEM` | - | SSL 인증서 파일명 |
| `GOOGLE_SITE_VERIFICATION` | - | Google Search Console 인증 코드 |

## 📝 라이선스

MIT License