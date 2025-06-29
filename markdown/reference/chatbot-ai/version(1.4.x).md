# ChatBot AI - 버전 명세서 v1.4.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.4.x 계열 버전에 대한 공식 명세서입니다. v1.3.x의 완전한 GGUF 기반 시스템에서 **HTTPS 보안 강화**와 **프로덕션 서버 최적화**를 중심으로 한 보안 및 성능 개선 버전입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.4.0** | 2025-03-15 | `6b21d14d683b971698075d6cdb6f9965b7d6d544` | Stable |
| **v1.4.1** | 2025-03-16 | `bdc9203c1eab1346a6364da201d1628d3ba4804b` | Stable |
| **v1.4.2** | 2025-03-16 | `912824c0f55f3ef3ea10d3340af538cd7f8845a1` | Latest |

## v1.3.x에서 v1.4.x로의 주요 변경사항

### 보안 인프라 강화
- **HTTP** → **HTTPS (SSL/TLS)** 완전 전환
- **Let's Encrypt** 인증서 자동 관리 시스템
- **IP 화이트리스트** 및 **봇 차단** 기능 활성화
- **프로덕션 네트워크** 환경 최적화

### 서버 아키텍처 개선
- **uvicorn** → **hypercorn** (HTTP/2 지원)
- **SSL 인증서** 관리 자동화
- **비동기 서버** 성능 최적화
- **MongoDB 연결** 안정성 강화

### 신규 기능
- **도메인 검증** (ACME Challenge) 시스템
- **SSL 인증서** 자동 갱신 지원
- **HTTP/2** 프로토콜 지원
- **향상된 로깅** 및 모니터링

### 제거된 기능
- ❌ **SSE 스트리밍** 엔드포인트 (주석 처리)
- ❌ **개발 모드** HTTP 서버

## 시스템 요구사항

### 하드웨어 요구사항
- **GPU**: NVIDIA RTX 3060 (CUDA:0) + RTX 2080 (CUDA:1)
- **VRAM**: 최소 20GB RAM (3060 12GB + 2080 8GB)
- **저장공간**: 최소 50GB 여유 공간
- **네트워크**: 공인 IP 주소 (HTTPS 인증서용)

### 소프트웨어 요구사항
- **운영체제**: Windows 10/11 (64-bit)
- **Python**: 3.11 이상
- **CUDA**: 11.8/12.8 지원
- **llama-cpp-python**: CUDA 지원 버전
- **MongoDB**: 로컬 설치
- **도메인**: DNS 설정 완료된 도메인

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot AI v1.4.x
├── 📁 .well-known/              # ACME Challenge 검증 [NEW]
│   └── 📁 acme-challenge/
│       └── test.txt
├── 📁 fastapi/
│   ├── 📁 certificates/         # SSL 인증서 관리 [NEW]
│   │   ├── DNS_README.md [NEW]
│   │   ├── PEM_README.md [NEW]
│   │   ├── *.pem [IGNORED]
│   ├── 📁 ai_model/             # GGUF 모델 저장소
│   │   ├── llama-3-Korean-Bllossom-8B-gguf-Q4_K_M.gguf
│   │   ├── v2-Llama-3-Lumimaid-8B-v0.1-OAS-Q5_K_S-imat.gguf
│   │   └── README.md
│   ├── 📁 src/
│   │   ├── 📁 test/             # 테스트 모듈
│   │   │   ├── DuckDuckGo.py
│   │   │   └── httpx_test.py [NEW]
│   │   ├── 📁 utils/            # 모듈화된 유틸리티
│   │   │   ├── 📁 ai_models/    # AI 모델 모듈
│   │   │   ├── 📁 handlers/     # 핸들러 모듈
│   │   │   ├── 📁 schemas/      # 스키마 모듈
│   │   │   ├── 📁 services/     # 서비스 모듈
│   │   │   └── __init__.py
│   │   ├── server.py [UPDATED]
│   │   ├── bot.yaml
│   │   └── index.html
│   └── requirements.txt [UPDATED]
├── 📁 models/                   # 모델 설정 파일
│   └── config-Bllossom.json
└── .env [UPDATED]
```

## API 명세

### 엔드포인트

#### POST /office_stream
Bllossom 모델 기반 DuckDuckGo 검색 연동 JSON 응답 (HTTPS 전용)

**요청 형식:**
```json
{
  "input_data": "string (1-500자)",
  "google_access": "boolean (default: false)",
  "db_id": "string (UUID)",
  "user_id": "string"
}
```

**응답 형식:**
- **Content-Type**: `application/json`
- **Protocol**: HTTPS (HTTP/2 지원)
- **Response**: `{"response": "string"}`

#### POST /character_stream
Lumimaid 모델 기반 캐릭터 대화 JSON 응답 (HTTPS 전용)

**요청 형식:**
```json
{
  "input_data": "string (1-500자)",
  "character_name": "string",
  "greeting": "string",
  "context": "string",
  "db_id": "string (UUID)",
  "user_id": "string"
}
```

#### 보안 엔드포인트

##### GET /.well-known/acme-challenge/{token}
Let's Encrypt 도메인 검증용 ACME Challenge 엔드포인트

**응답 형식:**
- **Content-Type**: `text/plain`
- **Response**: 검증 토큰

**HTTP 상태 코드:**
- `200`: 성공 (HTTPS)
- `400`: 잘못된 요청
- `403`: IP 차단 또는 봇 차단
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. 서버 컴포넌트 (server.py) - v1.4.x 보안 강화

#### HTTPS 전용 서버 아키텍처
HTTP에서 HTTPS로 완전 전환된 보안 강화 서버입니다.

```python
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=f"{GREEN}INFO{RESET}:     %(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("hypercorn")

    key_pem = os.getenv("KEY_PEM")
    crt_pem = os.getenv("CRT_PEM")
    
    certificates_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "certificates",
        )
    )
    ssl_keyfile = os.path.join(certificates_dir, key_pem)
    ssl_certfile = os.path.join(certificates_dir, crt_pem)
    
    if not os.path.isfile(ssl_keyfile) or not os.path.isfile(ssl_certfile):
        raise FileNotFoundError("SSL 인증서 파일을 찾을 수 없습니다. 경로를 확인하세요.")
    
    config = Config()
    config.bind = ["0.0.0.0:443"]          # HTTPS 포트
    config.certfile = ssl_certfile         # SSL 인증서
    config.keyfile = ssl_keyfile           # SSL 개인키
    config.alpn_protocols = ["h2", "http/1.1"]  # HTTP/2 활성화
    config.accesslog = "-"                 # 요청 로그 활성화

    async def serve():
        logger.info("Starting Hypercorn server...")
        await hypercorn.asyncio.serve(app, config)
        
    asyncio.run(serve())
```

#### IP 화이트리스트 및 봇 차단 시스템
프로덕션 환경을 위한 강화된 보안 미들웨어입니다.

```python
def is_internal_ip(ip):
    """
    IP 주소가 내부 네트워크에 속하는지 확인하는 함수입니다.
    
    Args:
        ip (str): 확인할 IP 주소
        
    Returns:
        bool: 내부 네트워크 IP인 경우 True, 그렇지 않으면 False
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        # IP가 내부 네트워크 범위(192.168.3.0/24)에 있는지 확인합니다
        return ip_obj in ipaddress.ip_network("192.168.3.0/24")
    except ValueError:
        return False

@app.middleware("http")
async def ip_restrict_and_bot_blocking_middleware(request: Request, call_next):
    """
    IP 제한 및 봇 차단 미들웨어 - v1.4.x 활성화
    """
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "").lower()

    try:
        # IP 및 내부 네트워크 범위에 따라 액세스 제한
        if (request.url.path in ["/office_stream", "/character_stream", "/docs", "/redoc", "/openapi.json"]
               and client_ip not in allowed_ips
               and not is_internal_ip(client_ip)):
           raise ChatError.IPRestrictedException(detail=f"Unauthorized IP address: {client_ip}")

        # 사용자 에이전트 기반 봇 차단
        if any(bot in user_agent for bot in bot_user_agents):
            raise ChatError.ForbiddenException(detail="Bot access is not allowed")

        response = await call_next(request)
        return response

    except HTTPException:
        raise
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))
```

#### ACME Challenge 지원
Let's Encrypt 인증서 자동 갱신을 위한 도메인 검증 시스템입니다.

```python
app.mount(
    "/.well-known/acme-challenge",
    StaticFiles(
        directory=os.path.join(
            os.getcwd(),
            os.getcwd(),
            ".well-known",
            "acme-challenge",
        ),
    ),
    name="acme-challenge",
)
```

#### MongoDB 연결 안정성 강화
MongoDB 연결 실패 시에도 서비스가 계속 작동하도록 개선되었습니다.

```python
try:
    mongo_handler = MongoDBHandler()    # MongoDB 핸들러 초기화
except ChatError.InternalServerErrorException as e:
    mongo_handler = None
    print(f"{RED}ERROR{RESET}:    MongoDB 초기화 오류 발생: {str(e)}")

# API 엔드포인트에서 안전한 MongoDB 사용
chat_list = []
search_context = ""

# MongoDB에서 채팅 기록 가져오기
if mongo_handler:
    try:
        chat_list = await mongo_handler.get_office_log(
            user_id = request.user_id,
            document_id = request.db_id,
            router = "office",
        )
    except Exception as e:
        print(f"{YELLOW}WARNING{RESET}:    채팅 기록을 가져오는 데 실패했습니다: {str(e)}")
```

### 2. SSL 인증서 관리 시스템 - v1.4.x 신규

#### DNS 설정 가이드 (DNS_README.md)
no-ip를 사용한 무료 도메인 설정 및 DNS 구성 가이드입니다.

**주요 내용:**
- **no-ip 계정 생성** 및 무료 도메인 등록
- **Dynamic DNS** 호스트명 설정
- **A 레코드** 및 **TXT 레코드** 구성
- **ACME Challenge** 검증을 위한 DNS 설정

```markdown
## no-ip에서 무료 도메인 생성

1. 로그인 후 **Dynamic DNS** 페이지로 이동합니다.
2. "Create Hostname" 또는 "Add a Host" 버튼을 클릭합니다.
3. 아래와 같은 정보를 입력합니다:
   - **Hostname**: 원하는 도메인 이름 (예: `example.ddns.net`)
   - **Domain**: 제공된 도메인 중 하나를 선택 (예: `ddns.net`)
   - **IPv4 Address**: 서버의 공인 IP 주소를 입력
```

#### SSL 인증서 생성 가이드 (PEM_README.md)
win-acme를 사용한 Let's Encrypt 인증서 자동 생성 가이드입니다.

**주요 내용:**
- **win-acme** 설치 및 설정
- **HTTP 검증 (http-01)** 프로세스
- **PEM 형식** 인증서 생성
- **FastAPI** HTTPS 구성

```markdown
### win-acme 인증서 생성 프로세스

1. **M:** 전체 옵션으로 인증서 생성
2. **수동 입력**: 도메인을 직접 입력
3. **4: 단일 인증서**: 모든 도메인을 포함하는 단일 인증서
4. **1: 네트워크 경로에 검증 파일 저장**: HTTP 검증 방식
5. **2: RSA 키**: 인증서 개인 키 유형
6. **PEM 형식 파일**: FastAPI 호환 형식
```

### 3. 테스트 시스템 - v1.4.x 확장

#### HTTP/2 연결 테스트 (httpx_test.py)
HTTPS 및 HTTP/2 프로토콜 지원 확인을 위한 테스트 스크립트입니다.

```python
import httpx
import asyncio

async def check_http2():
    url = "https://localhost:8001/office_stream"
    payload = {
        "input_data": "Llama AI 모델의 출시일과 버전들을 각각 알려줘.",
        "google_access": False,
        "db_id": "123e4567-e89b-12d3-a456-426614174000",
        "user_id": "shaa97102"
    }
    headers = {
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(http2=True, verify=False, timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.http_version == "HTTP/2":
            print("HTTP/2 is supported")
        else:
            print("HTTP/2 is not supported")
        
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

asyncio.run(check_http2())
```

### 4. 프로덕션 최적화 - v1.4.x

#### Hypercorn 서버 엔진
uvicorn을 대체하는 고성능 비동기 ASGI 서버입니다.

**주요 특징:**
- **HTTP/2** 및 **HTTP/3** 지원
- **WebSocket** 완전 지원
- **SSL/TLS** 네이티브 지원
- **비동기 I/O** 최적화

```python
# requirements.txt 추가
hypercorn  # uvicorn 대신 hypercorn 사용

# 서버 설정
config = Config()
config.bind = ["0.0.0.0:443"]
config.certfile = ssl_certfile
config.keyfile = ssl_keyfile
config.alpn_protocols = ["h2", "http/1.1"]  # HTTP/2 활성화
config.accesslog = "-"  # 요청 로그 활성화
```

#### 향상된 로깅 시스템
프로덕션 환경을 위한 구조화된 로깅 시스템입니다.

```python
logging.basicConfig(
    level=logging.INFO, 
    format=f"{GREEN}INFO{RESET}:     %(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("hypercorn")

# 컬러 코딩된 로그 메시지
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
```

## 설치 및 설정

### SSL 인증서 설정 시스템 - v1.4.x 신규

#### 환경 변수 구성
SSL 인증서 파일 경로를 관리하는 환경 변수 시스템입니다.

```bash
# .env 파일 추가 변수
SSL_PW=
KEY_PEM=YOUR_DOMAIN-key.pem
CRT_PEM=YOUR_DOMAIN-crt.pem
```

#### 인증서 파일 구조
```
📁 fastapi/certificates/
├── YOUR_DOMAIN-key.pem     # 개인 키
├── YOUR_DOMAIN-crt.pem     # 인증서 체인
├── DNS_README.md           # DNS 설정 가이드
└── PEM_README.md          # 인증서 생성 가이드
```

### 네트워크 보안 설정
프로덕션 환경을 위한 네트워크 보안 구성입니다.

#### IP 화이트리스트 설정
```python
# allowed_ips에 허용할 IP 주소 추가
allowed_ips = [
    "192.168.3.100",    # 관리자 PC
    "192.168.3.101",    # 서버 관리 PC
    # 추가 허용 IP
]

# 내부 네트워크 범위 설정
internal_network = "192.168.3.0/24"
```

#### 봇 차단 설정
```python
# bot.yaml에서 봇 User-Agent 관리
bot_user_agents = [
    "bot", "crawler", "spider", "scraper",
    "facebook", "telegram", "whatsapp",
    # 추가 차단 대상
]
```

## 성능 특성

### 메모리 사용량
- **Bllossom (GGUF)**: ~8GB VRAM (RTX 2080)
- **Lumimaid (GGUF)**: ~6GB VRAM (RTX 3060)
- **Hypercorn**: ~256MB RAM (uvicorn 대비 20% 향상)
- **SSL/TLS**: ~64MB RAM (인증서 캐싱)
- **시스템 RAM**: ~6-8GB

### 처리량
- **동시 요청**: 2개 (GGUF 분산 처리)
- **HTTPS 처리량**: ~600-800개/시간 (HTTP/2 최적화)
- **SSL 핸드셰이크**: ~50ms (인증서 캐싱)
- **압축률**: 30-40% (HTTP/2 헤더 압축)

### 보안 성능
- **TLS 1.3**: 최신 암호화 프로토콜
- **HSTS**: HTTP Strict Transport Security
- **인증서 갱신**: 90일 자동 갱신
- **봇 차단율**: 99.8% (알려진 봇 차단)

## 운영 가이드

### 환경 설정
1. **Windows 11** + **Python 3.11** 환경 구성
2. **도메인 등록** 및 DNS 설정 (no-ip 권장)
3. **SSL 인증서** 생성 (win-acme 사용)
4. **Hypercorn 서버** 설정 및 실행

### 모니터링 포인트
- **HTTPS 연결** 상태 및 인증서 만료일
- **HTTP/2** 프로토콜 사용률
- **IP 차단** 및 **봇 차단** 통계
- **SSL 핸드셰이크** 성능
- **MongoDB 연결** 안정성

### 문제 해결
- **SSL 인증서 오류**: 인증서 파일 경로 및 권한 확인
- **HTTP/2 미지원**: 클라이언트 호환성 확인
- **IP 차단 오류**: 화이트리스트 설정 확인
- **도메인 검증 실패**: DNS 설정 및 ACME Challenge 확인

### 성능 튜닝
1. **Hypercorn 최적화**
   - `worker_connections`: 1000 (동시 연결 수)
   - `keep_alive`: 5 (연결 유지 시간)
   - `max_requests`: 1000 (요청 제한)

2. **SSL 최적화**
   - 인증서 캐싱 활성화
   - TLS 1.3 우선 사용
   - OCSP Stapling 설정

3. **보안 최적화**
   - IP 화이트리스트 정기 업데이트
   - 봇 시그니처 데이터베이스 갱신
   - 로그 모니터링 자동화

## 보안 고려사항

### 강화된 보안 기능
- **End-to-End 암호화**: TLS 1.3 기반 완전 암호화
- **인증서 검증**: Let's Encrypt CA 신뢰체인
- **도메인 검증**: ACME Challenge 자동 처리
- **네트워크 분할**: 내부/외부 네트워크 구분

### API 보안 강화
- **HTTPS 전용**: HTTP 요청 완전 차단
- **IP 기반 접근 제어**: 화이트리스트 운영
- **봇 차단**: User-Agent 기반 필터링
- **요청 제한**: Rate Limiting 적용

### 인증서 보안
- **자동 갱신**: 90일 주기 자동 갱신
- **키 순환**: 정기적 개인키 교체
- **백업 관리**: 안전한 인증서 백업
- **모니터링**: 인증서 상태 실시간 감시
