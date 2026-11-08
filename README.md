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

## 검색 및 AI 크롤러

- `/robots.txt`에서 일반 검색 엔진과 주요 AI 크롤러의 사이트 접근을 허용하고 사이트맵을 안내합니다.
- `/sitemap.xml`은 크롤링 가능한 페이지 목록을 제공합니다.
- `/llms.txt`는 포트폴리오와 FastAPI 기반 ChatBot-AI 프로젝트의 기술 요약 및 공개 소스 링크를 제공합니다.
- 크롤러 접근 허용은 방문을 보장하지 않습니다. 검색 노출이나 AI 답변 인용은 각 서비스의 수집 정책과 색인에 따라 달라집니다.

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

## UI 구성

- 밝은 Fluent 스타일: 중립 배경, 흰색 카드, 파란색 강조색, 작은 모서리 반경을 사용합니다.
- 홈은 프로필 → 대표 프로젝트 3개 → 경력 → 연락 순서로 구성됩니다. GitHub 저장소 자동 목록과 통계, 플로팅 버튼은 표시하지 않습니다.
- 공통 스타일은 `static/css/fluent.css`, 공통 탐색 메뉴와 푸터는 `static/components/site-header.html`, `site-footer.html`에서 관리합니다.
- 홈의 프로젝트 요약은 `static/index.html`에서 편집하고, 프로젝트 상세·레퍼런스 문서는 기존 `markdown/` 콘텐츠를 사용합니다.
- 문서 목차는 접기/펼치기로 제공하며, 시각화·문서 이미지 확대·이메일 전송 기능은 유지됩니다.
- 연락 양식은 기존 `/smtp/email` API를 사용합니다. 실제 이메일 발송 없이 테스트하려면 브라우저에서 해당 요청을 모의 응답으로 처리하세요.

## 📝 라이선스

MIT License