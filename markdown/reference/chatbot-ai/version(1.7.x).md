# ChatBot AI - 버전 명세서 v1.7.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.7.x 계열 버전에 대한 공식 명세서입니다. v1.6.x의 컨트롤러 패턴에서 **완전한 도커 기반 마이크로서비스 아키텍처**로 대전환되었으며, **nginx API Gateway**, **클린 아키텍처 패턴**, **성능 테스트 자동화**를 도입한 엔터프라이즈급 AI 챗봇 플랫폼입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **None** | 2025-05-16 | `0b5d65da73cae825fbf76e853fce56d86e103ae1` | Unstable |
| **v1.7.0** | 2025-05-30 | `a066bff70648487579f6c95219b42d23552e5501` | Stable |
| **v1.7.1** | 2025-05-30 | `a0e78809eef728324f9dde17ee7481052cd2fbae` | Stable |
| **v1.7.2** | 2025-06-10 | `6ed3a4af85834340523085fc4c4e1b1e125a5f4f` | Stable |
| **v1.7.3** | 2025-06-16 | `b96f909d752032d39510891a8c147ee340584f36` | Stable |
| **v1.7.4** | 2025-06-29 | `61e47793c0647baa5272cba6a3a82bee9a12ce74` | Latest |

## v1.7.3에서 v1.7.4로의 주요 변경사항

### AI 모델 통합 및 최적화
- **DarkIdol-Llama** → **Meta-Llama-3.1-8B-Claude** 모델로 통합
- **Character 서비스**: Q4_0 양자화 모델 사용 (GPU 0, 50 레이어)
- **Office 서비스**: Q4_1 양자화 모델 사용 (GPU 1, 모든 레이어)
- **모델 제작자**: QuantFactory로 일원화

### 성능 및 안정성 개선
- **Office 서비스**: 동시 처리 수 2 → 1로 조정 (안정성 우선)
- **GPU 할당**: 명확한 GPU 분리 (Character: GPU 0, Office: GPU 1)
- **컨텍스트 및 배치 크기**: 통일된 설정 (8191 토큰, 2048 배치)
- **백업 응답 생성**: 스트리밍 실패 시 폴백 메커니즘 추가

### 기술적 특징 강화
- **Flash Attention**: 메모리 효율성 향상
- **연속 배칭**: 멀티 사용자 처리 최적화
- **16bit KV 캐시**: 메모리 사용량 최적화
- **RoPE 스케일링**: 긴 문맥 지원 (linear scaling 2x)

### 볼륨 구조 변경
- **MLP-KTLim** → **QuantFactory** 폴더로 변경
- 모델 파일 경로 업데이트 및 통합 관리

## v1.6.x에서 v1.7.x로의 주요 변경사항

### 아키텍처 대혁신
- **모노리식 FastAPI** → **독립 마이크로서비스** (office/character 분리)
- **로컬 서버** → **Docker 컨테이너 오케스트레이션**
- **단일 진입점** → **nginx API Gateway** (포트 8001)
- **컨트롤러 패턴** → **클린 아키텍처** (DDD 기반)

### 인프라 완전 전환
- **Windows 네이티브** → **Docker Compose** 기반 배포
- **로컬 모델 관리** → **공유 볼륨** 시스템
- **개별 설정** → **통합 설정 관리**
- **수동 배포** → **컨테이너 오케스트레이션**

### 개발 환경 혁신
- **성능 테스트 자동화** (Locust 기반)
- **AI 모델 통합** (llama.cpp CUDA 12.1)
- **클린 코드 아키텍처** (Domain-Core-API 분리)
- **커스텀 404 페이지** 지원

### 신규 기능
- **nginx 리버스 프록시** (커스텀 404, 로드 밸런싱)
- **공유 Python 라이브러리** 볼륨
- **컨테이너 간 통신** 최적화
- **성능 모니터링** 대시보드 (visualization.html)

### 제거된 기능
- ❌ **모든 utils 폴더** 구조 (클린 아키텍처로 재편)
- ❌ **Windows 배치 파일** (도커 환경으로 전환)
- ❌ **로컬 서버 실행** (컨테이너 전용)
- ❌ **프로토타입 코드** 정리 (프로덕션 최적화)

## 시스템 요구사항

### 하드웨어 요구사항
- **GPU**: NVIDIA RTX 3060 (CUDA:0) + RTX 2080 (CUDA:1)
- **VRAM**: 최소 20GB RAM (3060 12GB + 2080 8GB)
- **저장공간**: 최소 100GB 여유 공간 (도커 이미지 포함)
- **네트워크**: 고속 인터넷 (모델 다운로드 + API 호출)

### 소프트웨어 요구사항
- **운영체제**: Docker 지원 OS (Linux/Windows/macOS)
- **Docker**: 20.10 이상
- **Docker Compose**: 2.0 이상
- **NVIDIA Container Toolkit**: CUDA 12.1 지원
- **OpenAI API**: 유효한 API 키

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot AI v1.7.x
├── 📁 fastapi/                  # 메인 애플리케이션
│   ├── 📁 ai_model/             # AI 모델 파일 (볼륨 마운트)
│   │   └── 📁 QuantFactory/     # Meta-Llama-3.1-8B-Claude 모델 [v1.7.4]
│   │       ├── Meta-Llama-3.1-8B-Claude.Q4_0.gguf [NEW v1.7.4]
│   │       └── Meta-Llama-3.1-8B-Claude.Q4_1.gguf [NEW v1.7.4]
│   ├── 📁 logs/                 # 로그 파일 (공유 볼륨)
│   ├── 📁 prompt/               # 프롬프트 설정
│   │   ├── config-Llama.json [MOVED]
│   │   └── config-OpenAI.json [MOVED]
│   ├── 📁 src/                  # 소스 코드
│   │   ├── 📁 api/              # API 계층 [NEW]
│   │   │   ├── 📁 character/
│   │   │   │   └── llm_controller.py [NEW]
│   │   │   ├── 📁 office/
│   │   │   │   └── llm_controller.py [NEW]
│   │   │   └── __init__.py [NEW]
│   │   ├── 📁 core/             # 핵심 비즈니스 로직 [NEW]
│   │   │   ├── 📁 character/
│   │   │   │   └── app_state.py [NEW]
│   │   │   ├── 📁 office/
│   │   │   │   └── app_state.py [UPDATED v1.7.4]
│   │   │   └── __init__.py [NEW]
│   │   ├── 📁 domain/           # 도메인 모델 [NEW]
│   │   │   ├── 📁 character/
│   │   │   │   ├── config.py [NEW]
│   │   │   │   └── schema.py [MOVED]
│   │   │   ├── 📁 office/
│   │   │   │   ├── config.py [NEW]
│   │   │   │   └── schema.py [NEW]
│   │   │   ├── 📁 shared/
│   │   │   │   ├── base_config.py [NEW]
│   │   │   │   ├── error_tools.py [MOVED]
│   │   │   │   ├── mongodb_client.py [MOVED]
│   │   │   │   ├── queue_tools.py [NEW]
│   │   │   │   └── search_adapter.py [MOVED]
│   │   │   └── __init__.py [NEW]
│   │   ├── 📁 llm/              # LLM 모델 계층 [NEW]
│   │   │   ├── 📁 llama/
│   │   │   │   ├── character.py [UPDATED v1.7.4]
│   │   │   │   └── office.py [UPDATED v1.7.4]
│   │   │   ├── 📁 openai/
│   │   │   │   ├── character.py [MOVED]
│   │   │   │   └── office.py [MOVED]
│   │   │   └── __init__.py [NEW]
│   │   ├── 📁 server/           # 서버 진입점 [NEW]
│   │   │   ├── 📁 character/
│   │   │   │   ├── Dockerfile [NEW]
│   │   │   │   └── server.py [NEW]
│   │   │   └── 📁 office/
│   │   │       ├── Dockerfile [NEW]
│   │   │       └── server.py [NEW]
│   │   ├── 📁 test/             # 성능 테스트 [NEW]
│   │   │   ├── 📁 performance_results/
│   │   │   │   ├── character_2025-06-04_031424.csv [NEW]
│   │   │   │   ├── character_2025-06-04_180716.csv [NEW]
│   │   │   │   └── visualization.html [NEW]
│   │   │   ├── test.bat [NEW]
│   │   │   ├── test_character_load.py [NEW]
│   │   │   └── test_office_load.py [NEW]
│   │   ├── Dockerfile.base [NEW]
│   │   ├── Dockerfile.libs [NEW]
│   │   └── install_libs.sh [NEW]
│   ├── requirements.txt [UPDATED]
│   └── requirements_llama.txt [UPDATED]
├── 📁 nginx/                    # API Gateway [NEW]
│   ├── nginx.conf [NEW]
│   └── 404.html [NEW]
├── docker-compose.yml [UPDATED v1.7.4]
├── rebuild.bat [NEW]
└── README.md [UPDATED v1.7.4]
```

## API 명세

### nginx API Gateway 구조

#### 통합 진입점 (포트 8001)
모든 API 요청을 nginx가 받아 적절한 서비스로 라우팅합니다.

```nginx
server {
    listen 8001;
    server_name localhost;

    # Office API 라우팅
    location ^~ /office/ {
        proxy_pass http://office_backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Character API 라우팅
    location ^~ /character/ {
        proxy_pass http://character_backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 커스텀 404 페이지
    error_page 404 /404.html;
    location = /404.html {
        root /etc/nginx/html;
        internal;
    }

    # 기본 경로 처리
    location / {
        return 404;
    }
}
```

#### Office API (`/office/`)
업무용 AI 서비스 (포트 8002)

##### POST /office/Llama
Meta-Llama-3.1-8B-Claude (Q4_1) 모델 기반 검색 연동 JSON 응답

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
- **Response**: `"string"` (JSON 문자열 직접 반환)
- **GPU**: CUDA:1 (RTX 2080) 사용
- **모델**: Meta-Llama-3.1-8B-Claude.Q4_1.gguf

##### GET /office/performance
Office 서비스 성능 통계 조회

**응답 형식:**
```json
{
  "total_requests": 1250,
  "avg_response_time": 18.5,
  "success_rate": 98.4,
  "active_connections": 1,
  "max_concurrent": 1
}
```

#### Character API (`/character/`)
캐릭터 대화 AI 서비스 (포트 8003)

##### POST /character/Llama
Meta-Llama-3.1-8B-Claude (Q4_0) 모델 기반 캐릭터 대화 JSON 응답

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

**예시 요청:**
```json
{
  "input_data": "*I wave at Rachel with a smile.*",
  "character_name": "Rachel",
  "greeting": "*Rachel stands nervously at the lectern, adjusting her notes...*",
  "context": "Rachel is a devout Catholic girl of about 19 years old...",
  "db_id": "b440780c-cbaa-454f-a8d2-cf884786d89f",
  "user_id": "user_test_001"
}
```

**v1.7.4 개선사항:**
- **GPU**: CUDA:0 (RTX 3060) 사용
- **모델**: Meta-Llama-3.1-8B-Claude.Q4_0.gguf
- **GPU 레이어**: 50개 (이전: 모든 레이어)

##### GET /character/performance
Character 서비스 성능 통계 조회

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `404`: 커스텀 404 페이지 (nginx)
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류
- `503`: 서비스 일시 중단

## 주요 컴포넌트

### 1. Docker Compose 오케스트레이션 - v1.7.4 업데이트

#### 마이크로서비스 아키텍처
각 서비스가 독립적인 컨테이너로 실행되는 완전한 마이크로서비스 구조입니다.

```yaml
version: '3.8'

services:
  # 공통 라이브러리 초기화 서비스
  python-libs-init:
    build:
      context: ./fastapi
      dockerfile: src/Dockerfile.libs
    volumes:
      - python-libs:/opt/python-libs
    command: ["/app/install_libs.sh"]

  # Office API 서비스 (v1.7.4 업데이트)
  office:
    build:
      context: ./fastapi
      dockerfile: src/server/office/Dockerfile
    ports:
      - "8002:8002"
    environment:
      - APP_MODE=office
      - NVIDIA_VISIBLE_DEVICES=1  # RTX 2080
    volumes:
      - ./fastapi/ai_model/QuantFactory:/app/fastapi/ai_model/QuantFactory:rw  # v1.7.4 변경
      - ./fastapi/logs:/app/logs
      - python-libs:/opt/python-libs:ro
    depends_on:
      - python-libs-init
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ['1']
              capabilities: [gpu]

  # Character API 서비스
  character:
    build:
      context: ./fastapi
      dockerfile: src/server/character/Dockerfile
    ports:
      - "8003:8003"
    environment:
      - APP_MODE=character
      - NVIDIA_VISIBLE_DEVICES=0  # RTX 3060
    volumes:
      - ./fastapi/ai_model/QuantFactory:/app/fastapi/ai_model/QuantFactory:rw  # v1.7.4 변경
      - ./fastapi/logs:/app/logs
      - python-libs:/opt/python-libs:ro
    depends_on:
      - python-libs-init
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ['0']
              capabilities: [gpu]

  # nginx API Gateway
  nginx:
    image: nginx:alpine
    ports:
      - "8001:8001"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./nginx/404.html:/etc/nginx/html/404.html:ro
    depends_on:
      - office
      - character

volumes:
  python-libs:
    driver: local
```

### 2. AI 모델 통합 시스템 - v1.7.4 완전 재설계

#### 모델 정보 (v1.7.4)

| 항목 | **LlamaCharacterModel** | **LlamaOfficeModel** | 
|------|----------------------|-----------------------|
| **기반 모델** | Meta-Llama-3.1-8B-Claude | Meta-Llama-3.1-8B-Claude |
| **모델 파일** | `Meta-Llama-3.1-8B-Claude.Q4_0.gguf` | `Meta-Llama-3.1-8B-Claude.Q4_1.gguf` |
| **제작자** | QuantFactory | QuantFactory |
| **포맷** | GGUF 포맷 (Q4_0 양자화) | GGUF 포맷 (Q4_1 양자화) |
| **GPU 할당** | GPU 0번 (`main_gpu = 0`) | GPU 1번 (`main_gpu = 1`) |
| **GPU 레이어** | `n_gpu_layers = 50` | `n_gpu_layers = -1` (모든 레이어) |
| **용도** | 캐릭터 롤플레이 대화 | 업무용 AI 어시스턴트 |
| **로딩 방식** | `llama_cpp_cuda` | `llama_cpp_cuda` |
| **컨텍스트 길이** | 8191 토큰 | 8191 토큰 |
| **배치 크기** | 2048 | 2048 |
| **소스** | [QuantFactory/Meta-Llama-3.1-8B-Claude-GGUF](https://huggingface.co/QuantFactory/Meta-Llama-3.1-8B-Claude-GGUF) | [QuantFactory/Meta-Llama-3.1-8B-Claude-GGUF](https://huggingface.co/QuantFactory/Meta-Llama-3.1-8B-Claude-GGUF) |

#### 기술적 특징 (v1.7.4)

- **Flash Attention**: 메모리 효율성과 속도 향상을 위해 활성화
- **연속 배칭**: 멀티 사용자 처리를 위한 최적화
- **16bit KV 캐시**: 메모리 사용량 최적화
- **RoPE 스케일링**: 긴 문맥 지원을 위한 linear scaling (2x)
- **스트리밍 지원**: 실시간 텍스트 생성 및 응답
- **백업 응답 시스템**: 스트리밍 실패 시 자동 폴백

### 3. 클린 아키텍처 패턴 - v1.7.4 최적화

#### Core 계층 업데이트 (core/office/app_state.py)
비즈니스 로직과 상태 관리를 담당하는 핵심 계층의 안정성 개선입니다.

```python
# core/office/app_state.py (v1.7.4)
from typing import Optional
from domain import (
    mongodb_client,
    office_config,
    queue_tools,
    error_tools
)
from llm import office_llama

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

# 전역 상태 변수
llama_queue_handler: Optional[queue_tools.LlamaQueueHandler] = None
mongo_handler: Optional[mongodb_client.MongoDBHandler] = None

try:
    # 큐 핸들러 초기화 (안정성 우선 - 순차 처리)
    llama_queue_handler = queue_tools.LlamaQueueHandler(
        service_type=queue_tools.ServiceType.OFFICE,
        model_class=office_llama.LlamaOfficeModel,
        processing_request_class=office_config.ProcessingRequest,
        max_concurrent=1  # v1.7.4: 2 → 1로 변경 (안정성 우선)
    )
    
    # MongoDB 핸들러 초기화 (비동기)
    mongo_handler = mongodb_client.MongoDBHandler()  # 실제 초기화는 lifespan에서
    
    print(f"{GREEN}INFO{RESET}: Office 앱 상태 초기화 완료 (v1.7.4)")
    
except error_tools.InternalServerErrorException as e:
    mongo_handler = None
    print(f"{RED}ERROR{RESET}: MongoDB 초기화 오류 발생: {str(e)}")
except FileNotFoundError as e:
    llama_queue_handler = None
    print(f"{RED}ERROR{RESET}: 큐 핸들러 초기화 오류: {str(e)}")
except Exception as e:
    llama_queue_handler = None
    print(f"{RED}ERROR{RESET}: 예상치 못한 오류: {str(e)}")
```

### 4. LLM 모델 계층 - v1.7.4 통합 최적화

#### Character Llama 모델 (llm/llama/character.py) - v1.7.4
Meta-Llama-3.1-8B-Claude 모델을 사용한 캐릭터 대화 시스템의 최적화입니다.

```python
"""
Meta-Llama-3.1-8B-Claude GGUF 모델을 사용한 캐릭터 기반 대화 생성 모듈 (v1.7.4)
"""
from typing import Optional, Generator
from llama_cpp_cuda import Llama
import warnings
import sys
import json
import time
from queue import Queue
from threading import Thread
import os
from contextlib import contextmanager

from domain import character_config, base_config

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def build_llama3_prompt(character_info: character_config.CharacterPrompt) -> str:
    """
    캐릭터 정보를 기반으로 Llama3 GGUF 형식의 프롬프트 문자열을 생성합니다.

    Args:
        character_info (character_config.CharacterPrompt): 캐릭터 기본 정보 및 대화 맥락 포함 객체

    Returns:
        str: Llama3 GGUF 포맷용 프롬프트 문자열
    """
    system_prompt = (
        f"당신은 {character_info.name}이라는 캐릭터입니다.\n"
        f"당신의 설정: {character_info.context}\n"
        f"초기 인사말: {character_info.greeting}\n\n"
        f"지시 사항:\n"
        f"- 캐릭터의 성격과 말투를 일관성 있게 유지하세요\n"
        f"- 자연스럽고 몰입감 있는 대화를 만들어주세요\n"
        f"- 캐릭터 설정에 맞는 행동과 반응을 보여주세요\n"
    )

    # 시스템 프롬프트 시작
    prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{system_prompt}<|eot_id|>"
    )

    # 대화 기록 추가
    if character_info.chat_list:
        for chat in character_info.chat_list:
            user_input = chat.get("input_data", "")
            character_output = chat.get("output_data", "")

            if user_input:
                prompt += (
                    "<|start_header_id|>user<|end_header_id|>\n"
                    f"{user_input}<|eot_id|>"
                )
            if character_output:
                prompt += (
                    "<|start_header_id|>assistant<|end_header_id|>\n"
                    f"{character_output}<|eot_id|>"
                )

    # 최신 사용자 입력 추가
    prompt += (
        "<|start_header_id|>user<|end_header_id|>\n"
        f"{character_info.user_input}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n"
    )

    return prompt

class LlamaCharacterModel:
    """
    GGUF 포맷으로 경량화된 Meta-Llama-3.1-8B-Claude 모델을 사용한 캐릭터 대화 클래스 (v1.7.4)
    
    모델 정보: 
    - 모델명: Meta-Llama-3.1-8B-Claude
    - 유형: GGUF 포맷 (Q4_0 양자화)
    - 제작자: QuantFactory 
    - 소스: Hugging Face 모델 허브
    """
    def __init__(self) -> None:
        """
        LlamaCharacterModel 클래스 초기화 메소드 (v1.7.4)
        """
        self.model_id = "Meta-Llama-3.1-8B-Claude.Q4_0"  # v1.7.4 변경
        self.model_path = "/app/fastapi/ai_model/QuantFactory/Meta-Llama-3.1-8B-Claude.Q4_0.gguf"  # v1.7.4 변경
        self.file_path = '/app/prompt/config-Llama.json'
        self.loading_text = f"{BLUE}LOADING{RESET}:    {self.model_id} 로드 중..."
        self.character_info: Optional[character_config.CharacterPrompt] = None
        self.config: Optional[character_config.LlamaGenerationConfig] = None
        
        # 응답 큐 초기화
        self.response_queue = Queue()
        
        # 설정 파일 로드
        with open(self.file_path, 'r', encoding = 'utf-8') as file:
            self.data: base_config.BaseConfig = json.load(file)

        # 진행 상태 표시
        print(f"{BLUE}LOADING{RESET}:    {__class__.__name__} 모델 초기화 중...")
        self.model: Llama = self._load_model()
        print(f"{GREEN}SUCCESS{RESET}:   {__class__.__name__} 모델 로드 완료")

    def _load_model(self) -> Llama:
        """
        GGUF 포맷의 Meta-Llama-3.1-8B-Claude 모델을 GPU 0에 로드합니다. (v1.7.4)
        """
        print(f"{self.loading_text}")
        try:
            warnings.filterwarnings("ignore")
            
            @contextmanager
            def suppress_stdout():
                with open(os.devnull, "w") as devnull:
                    old_stdout = sys.stdout
                    sys.stdout = devnull
                    try:
                        yield
                    finally:
                        sys.stdout = old_stdout

            with suppress_stdout():
                model = Llama(
                    model_path = self.model_path,       # GGUF 모델 파일 경로
                    n_gpu_layers = 50,                  # v1.7.4: GPU 레이어 50개로 제한
                    main_gpu = 0,                       # 0번 GPU 사용
                    rope_scaling_type = 2,              # RoPE 스케일링 방식 (2 = linear) 
                    rope_freq_scale = 2.0,              # RoPE 주파수 스케일 → 긴 문맥 지원   
                    n_ctx = 8191,                       # 최대 context length
                    n_batch = 2048,                     # 배치 크기
                    verbose = False,                    # 디버깅 로그 비활성화  
                    offload_kqv = True,                 # K/Q/V 캐시를 CPU로 오프로드하여 VRAM 절약
                    use_mmap = False,                   # 메모리 매핑 비활성화 
                    use_mlock = True,                   # 메모리 잠금으로 메모리 페이지 스왑 방지
                    n_threads = 12,                     # CPU 스레드 수
                    tensor_split = [1.0],               # 단일 GPU에서 모든 텐서 로딩
                    split_mode = 1,                     # 텐서 분할 방식 (1 = 균등 분할)
                    flash_attn = True,                  # FlashAttention 사용 (속도 향상)
                    cont_batching = True,               # 연속 배칭 활성화
                    numa = False,                       # NUMA 비활성화
                    f16_kv = True,                      # 16bit KV 캐시 사용
                    logits_all = False,                 # 마지막 토큰만 logits 계산
                    embedding = False,                  # 임베딩 비활성화
                )
            return model
        except Exception as e:
            print(f"{RED}ERROR{RESET}: Character 모델 로드 실패: {e}")
            raise

    def _generate_fallback_response(self, prompt: str) -> str:
        """
        스트리밍 실패 시 백업 응답 생성 메서드 (v1.7.4 신규)
        
        Args:
            prompt (str): 생성할 프롬프트
            
        Returns:
            str: 생성된 응답
        """
        try:
            print(f"    백업 방식으로 응답 생성 중...")
            output = self.model.create_completion(
                prompt = prompt,
                max_tokens = 1024,
                temperature = 0.7,
                top_p = 0.9,
                repeat_penalty = 1.08,
                stop = ["<|eot_id|>"],
                stream = False  # 스트리밍 비활성화
            )
            
            if 'choices' in output and len(output['choices']) > 0:
                result = output['choices'][0].get('text', '').strip()
                print(f"    백업 방식 성공: {len(result)} 문자")
                return result
            else:
                return "응답을 생성할 수 없습니다. 다시 시도해 주세요."
                
        except Exception as e:
            print(f"    백업 방식도 실패: {e}")
            return "응답 생성에 실패했습니다. 잠시 후 다시 시도해 주세요."
```

#### Office Llama 모델 (llm/llama/office.py) - v1.7.4
Meta-Llama-3.1-8B-Claude 모델을 사용한 업무용 AI 어시스턴트의 완전한 재설계입니다.

```python
"""
Meta-Llama-3.1-8B-Claude.Q4_1.gguf 모델을 사용한 업무용 대화 생성 모듈 (v1.7.4)
"""
from typing import Optional, Generator, List, Dict
from llama_cpp_cuda import Llama
import os
import sys
import json
import warnings
import time
from queue import Queue
from threading import Thread
from contextlib import contextmanager
from datetime import datetime

from domain import office_config, base_config

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def build_llama3_prompt(character_info: office_config.OfficePrompt) -> str:
    """
    캐릭터 정보와 대화 기록을 기반으로 Llama3 GGUF 형식의 프롬프트 문자열을 생성합니다. (v1.7.4)

    Args:
        character_info (office_config.OfficePrompt): 캐릭터 기본 정보 및 대화 맥락 포함 객체

    Returns:
        str: Llama3 GGUF 포맷용 프롬프트 문자열
    """
    system_prompt = (
        f"당신은 AI 어시스턴트 {character_info.name}입니다.\n"
        f"당신의 역할: {character_info.context}\n\n"
        f"참고 정보 (사용자의 질문과 관련 있을 경우에만 활용하세요):\n"
        f"{character_info.reference_data}\n\n"
        f"지시 사항:\n"
        f"- 한국어로 답변하세요\n"
        f"- 친절하고 유익한 답변을 제공하세요\n"
        f"- 질문과 관련 없는 참고 정보는 언급하지 마세요\n"
        f"- 간결하면서도 핵심적인 정보를 포함하도록 하세요\n"
    )

    # 시스템 프롬프트 시작
    prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{system_prompt}<|eot_id|>"
    )

    # 대화 기록 추가
    if character_info.chat_list:
        for chat in character_info.chat_list:
            user_input = chat.get("input_data", "")
            assistant_output = chat.get("output_data", "")

            if user_input:
                prompt += (
                    "<|start_header_id|>user<|end_header_id|>\n"
                    f"{user_input}<|eot_id|>"
                )
            if assistant_output:
                prompt += (
                    "<|start_header_id|>assistant<|end_header_id|>\n"
                    f"{assistant_output}<|eot_id|>"
                )

    # 최신 사용자 입력 추가
    prompt += (
        "<|start_header_id|>user<|end_header_id|>\n"
        f"{character_info.user_input}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n"
    )

    return prompt

class LlamaOfficeModel:
    """
    GGUF 포맷으로 경량화된 Meta-Llama-3.1-8B-Claude 모델을 사용한 업무용 대화 클래스 (v1.7.4)
    
    모델 정보: 
    - 모델명: Meta-Llama-3.1-8B-Claude
    - 유형: GGUF 포맷 (Q4_1 양자화)
    - 제작자: QuantFactory
    - 소스: Hugging Face 모델 허브
    """
    def __init__(self) -> None:
        """
        LlamaOfficeModel 클래스 초기화 메소드 (v1.7.4)
        """
        self.model_id = 'Meta-Llama-3.1-8B-Claude.Q4_1'  # v1.7.4 변경
        self.model_path = "/app/fastapi/ai_model/QuantFactory/Meta-Llama-3.1-8B-Claude.Q4_1.gguf"  # v1.7.4 변경
        self.file_path = '/app/prompt/config-Llama.json'
        self.loading_text = f"{BLUE}LOADING{RESET}:    {self.model_id} 로드 중..."
        self.character_info: Optional[office_config.OfficePrompt] = None
        self.config: Optional[office_config.LlamaGenerationConfig] = None
        
        # 응답 큐 초기화
        self.response_queue = Queue()
        
        # 설정 파일 로드
        with open(self.file_path, 'r', encoding = 'utf-8') as file:
            self.data: base_config.BaseConfig = json.load(file)

        # 진행 상태 표시
        print(f"{BLUE}LOADING{RESET}:    {__class__.__name__} 모델 초기화 중...")
        self.model: Llama = self._load_model()
        print(f"{GREEN}SUCCESS{RESET}:   {__class__.__name__} 모델 로드 완료")

    def _load_model(self) -> Llama:
        """
        GGUF 포맷의 Meta-Llama-3.1-8B-Claude 모델을 GPU 1에 최대화 로드합니다. (v1.7.4)
        """
        print(f"{self.loading_text}")
        try:
            warnings.filterwarnings("ignore")
            
            @contextmanager
            def suppress_stdout():
                with open(os.devnull, "w") as devnull:
                    old_stdout = sys.stdout
                    sys.stdout = devnull
                    try:
                        yield
                    finally:
                        sys.stdout = old_stdout

            # GPU 사용량 극대화를 위한 설정
            with suppress_stdout():
                model = Llama(
                    model_path = self.model_path,       # GGUF 모델 파일 경로
                    n_gpu_layers = -1,                  # 모든 레이어를 GPU에 로드
                    main_gpu = 1,                       # 1번 GPU 사용 (office 서비스용)
                    rope_scaling_type = 2,              # RoPE 스케일링 방식 (2 = linear) 
                    rope_freq_scale = 2.0,              # RoPE 주파수 스케일 → 긴 문맥 지원   
                    n_ctx = 8191,                       # 최대 context length
                    n_batch = 2048,                     # 배치 크기 (VRAM 제한 고려한 중간 값)
                    verbose = False,                    # 디버깅 로그 비활성화  
                    offload_kqv = True,                 # K/Q/V 캐시를 CPU로 오프로드하여 VRAM 절약
                    use_mmap = False,                   # 메모리 매핑 비활성화 
                    use_mlock = True,                   # 메모리 잠금으로 메모리 페이지 스왑 방지
                    n_threads = 12,                     # CPU 스레드 수 (코어 12개 기준 적절한 값)
                    tensor_split = [1.0],               # 단일 GPU에서 모든 텐서 로딩
                    split_mode = 1,                     # 텐서 분할 방식 (1 = 균등 분할)
                    flash_attn = True,                  # FlashAttention 사용 (속도 향상)
                    cont_batching = True,               # 연속 배칭 활성화 (멀티 사용자 처리에 효율적)
                    numa = False,                       # NUMA 비활성화 (단일 GPU 시스템에서 불필요)
                    f16_kv = True,                      # 16bit KV 캐시 사용
                    logits_all = False,                 # 마지막 토큰만 logits 계산
                    embedding = False,                  # 임베딩 비활성화
                )
            return model
        except Exception as e:
            print(f"{RED}ERROR{RESET}: Office 모델 로드 실패: {e}")
            raise

    def _generate_fallback_response(self, prompt: str) -> str:
        """
        스트리밍 실패 시 백업 응답 생성 메서드 (v1.7.4 신규)
        
        Args:
            prompt (str): 생성할 프롬프트
            
        Returns:
            str: 생성된 응답
        """
        try:
            print(f"    백업 방식으로 응답 생성 중...")
            output = self.model.create_completion(
                prompt = prompt,
                max_tokens = 1024,
                temperature = 0.7,
                top_p = 0.9,
                repeat_penalty = 1.08,
                stop = ["<|eot_id|>"],
                stream = False  # 스트리밍 비활성화
            )
            
            if 'choices' in output and len(output['choices']) > 0:
                result = output['choices'][0].get('text', '').strip()
                print(f"    백업 방식 성공: {len(result)} 문자")
                return result
            else:
                return "응답을 생성할 수 없습니다. 다시 시도해 주세요."
                
        except Exception as e:
            print(f"    백업 방식도 실패: {e}")
            return "응답 생성에 실패했습니다. 잠시 후 다시 시도해 주세요."
```

## 성능 특성 (v1.7.4)

### 메모리 사용량 (최적화된 컨테이너)
- **Office Service**: ~12GB VRAM (RTX 2080, Q4_1) + ~2GB RAM
- **Character Service**: ~8GB VRAM (RTX 3060, Q4_0, 50 레이어) + ~2GB RAM  
- **nginx Gateway**: ~50MB RAM
- **Python Libs Volume**: ~1GB Disk
- **총 시스템**: ~15GB RAM, ~20GB VRAM

### 처리량 (최적화된 마이크로서비스)
- **동시 요청**: Office(1) + Character(1) = 독립 처리 (안정성 우선)
- **시간당 요청**: ~600-900개 (안정성 개선)
- **컨테이너 오버헤드**: ~10ms (nginx 프록시 포함)
- **GPU 격리**: 완전한 GPU 분리로 간섭 없음

### API 응답 시간 (v1.7.4 최적화)
- **Office/Llama**: 10-25초 (Meta-Llama Q4_1, CUDA:1, 모든 레이어)
- **Character/Llama**: 12-30초 (Meta-Llama Q4_0, CUDA:0, 50 레이어)
- **nginx Routing**: ~2ms (프록시 오버헤드)
- **Container Startup**: ~25초 (모델 로딩 최적화)

### 성능 테스트 결과 (v1.7.4 기준)
- **최대 동시 사용자**: 15명 (Character API)
- **평균 응답 시간**: 16.3초 (2초 개선)
- **성공률**: 96.1% (1.9% 개선)
- **큐 포화점**: 3개 요청 대기 시 (안정성 개선)

## 설치 및 설정 (v1.7.4)

### Docker 기반 배포 시스템

#### 필수 요구사항
1. **Docker & Docker Compose** 설치
2. **NVIDIA Container Toolkit** 설치 (GPU 지원)
3. **AI 모델 파일** 다운로드 (QuantFactory)

#### 빠른 시작 (v1.7.4)
```bash
# 1. 리포지토리 클론
git clone https://github.com/TreeNut-KR/ChatBot-AI.git
cd ChatBot-AI

# 2. AI 모델 파일 배치 (v1.7.4 업데이트)
# fastapi/ai_model/QuantFactory/ 폴더에 GGUF 모델 파일 복사
mkdir -p fastapi/ai_model/QuantFactory
# - Meta-Llama-3.1-8B-Claude.Q4_0.gguf (Character용)
# - Meta-Llama-3.1-8B-Claude.Q4_1.gguf (Office용)

# 3. 환경 변수 설정
cp fastapi/src/.env.example fastapi/src/.env
# .env 파일에서 OPENAI_API_KEY 등 설정

# 4. 컨테이너 빌드 및 실행
docker compose up --build

# 5. API 테스트 (v1.7.4)
curl -X POST "http://localhost:8001/office/Llama" \
  -H "Content-Type: application/json" \
  -d '{"input_data": "안녕하세요!", "user_id": "test_user"}'

curl -X POST "http://localhost:8001/character/Llama" \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": "안녕하세요!",
    "character_name": "AI Assistant",
    "greeting": "안녕하세요! 반갑습니다.",
    "context": "친근한 AI 어시스턴트",
    "db_id": "test-uuid",
    "user_id": "test_user"
  }'
```

#### 모델 다운로드 (v1.7.4)
```bash
# Hugging Face에서 모델 다운로드
wget https://huggingface.co/QuantFactory/Meta-Llama-3.1-8B-Claude-GGUF/resolve/main/Meta-Llama-3.1-8B-Claude.Q4_0.gguf -O fastapi/ai_model/QuantFactory/Meta-Llama-3.1-8B-Claude.Q4_0.gguf

wget https://huggingface.co/QuantFactory/Meta-Llama-3.1-8B-Claude-GGUF/resolve/main/Meta-Llama-3.1-8B-Claude.Q4_1.gguf -O fastapi/ai_model/QuantFactory/Meta-Llama-3.1-8B-Claude.Q4_1.gguf
```

## 운영 가이드 (v1.7.4)

### 환경 설정
1. **Docker 환경** 구성 및 GPU 지원 확인
2. **AI 모델 파일** 다운로드 및 QuantFactory 폴더 배치
3. **환경 변수** 설정 (OpenAI API 키 등)
4. **컨테이너 오케스트레이션** 실행

### 모니터링 포인트 (v1.7.4)
- **컨테이너 상태**: `docker compose ps`
- **GPU 사용률**: `nvidia-smi` (Character: GPU 0, Office: GPU 1)
- **nginx 로그**: `docker compose logs nginx`
- **API 성능**: `/performance` 엔드포인트
- **모델 성능**: 응답 시간 및 품질 모니터링

### 문제 해결 (v1.7.4)
- **모델 로딩 실패**: QuantFactory 폴더 및 모델 파일 경로 확인
- **GPU 메모리 부족**: Character 서비스의 GPU 레이어 수 조정 (50 → 더 낮게)
- **응답 품질 저하**: 백업 응답 시스템 동작 여부 확인
- **안정성 문제**: Office 서비스 max_concurrent 설정 확인 (1로 고정)

### 성능 튜닝 (v1.7.4)
1. **모델 최적화**
   - Character: GPU 레이어 수 조정 (30-50)
   - Office: 배치 크기 최적화 (1024-2048)
   - 양자화 레벨 변경 (Q4_0 ↔ Q4_1)

2. **서비스 최적화**
   - 동시 처리 수 조정 (안정성 vs 처리량)
   - 큐 타임아웃 설정 최적화
   - 백업 시스템 파라미터 튜닝

3. **인프라 최적화**
   - nginx 프록시 설정 최적화
   - 볼륨 마운트 성능 개선
   - 컨테이너 리소스 한계 조정
