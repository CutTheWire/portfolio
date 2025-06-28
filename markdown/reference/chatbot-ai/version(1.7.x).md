# ChatBot AI - 버전 명세서 v1.7.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.7.x 계열 버전에 대한 공식 명세서입니다. v1.6.x의 컨트롤러 패턴에서 **완전한 도커 기반 마이크로서비스 아키텍처**로 대전환되었으며, **nginx API Gateway**, **클린 아키텍처 패턴**, **성능 테스트 자동화**를 도입한 엔터프라이즈급 AI 챗봇 플랫폼입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.7.0** | 2025-05-30 | `a066bff70648487579f6c95219b42d23552e5501` | Stable |
| **v1.7.1** | 2025-05-30 | `a0e78809eef728324f9dde17ee7481052cd2fbae` | Stable |
| **v1.7.2** | 2025-06-10 | `6ed3a4af85834340523085fc4c4e1b1e125a5f4f` | Stable |
| **v1.7.3** | 2025-06-16 | `b96f909d752032d39510891a8c147ee340584f36` | Latest |

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
│   │   ├── MLP-KTLim/           # 한국어 Bllossom 모델
│   │   └── QuantFactory/        # DarkIdol 캐릭터 모델
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
│   │   │   │   └── app_state.py [NEW]
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
│   │   │   │   ├── character.py [MOVED]
│   │   │   │   └── office.py [MOVED]
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
├── docker-compose.yml [NEW]
├── rebuild.bat [NEW]
└── README.md [UPDATED]
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
Llama Office 모델 기반 검색 연동 JSON 응답

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

##### GET /office/performance
Office 서비스 성능 통계 조회

**응답 형식:**
```json
{
  "total_requests": 1250,
  "avg_response_time": 18.5,
  "success_rate": 98.4,
  "active_connections": 3
}
```

#### Character API (`/character/`)
캐릭터 대화 AI 서비스 (포트 8003)

##### POST /character/Llama
Llama Character 모델 기반 캐릭터 대화 JSON 응답

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

### 1. Docker Compose 오케스트레이션 - v1.7.x 신규

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

  # Office API 서비스
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
      - ./fastapi/ai_model:/app/fastapi/ai_model:ro
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
      - ./fastapi/ai_model:/app/fastapi/ai_model:ro
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

### 2. 클린 아키텍처 패턴 - v1.7.x 완전 재설계

#### API 계층 (api/)
외부 요청을 처리하는 프레젠테이션 계층입니다.

```python
# api/character/llm_controller.py
from fastapi import Path, APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

import time
from core import character_app_state as AppState
from domain import (
    character_schema as ChatModel,
    error_tools as ChatError,
)
from llm import character_openai

# 처리 시간 임계값 설정
MAX_PROCESSING_TIME = 180  # 3분 (nginx 타임아웃보다 충분히 짧게)
RETRY_AFTER_MINUTES = 3    # 3분 후 재시도 권장

character_router = APIRouter()

@character_router.post("/Llama", summary="Llama 모델이 캐릭터 정보를 기반으로 답변 생성")
async def character_llama(request: ChatModel.character_Request, req: Request):
    """
    DarkIdol-Llama-3.1-8B GGUF 모델을 사용한 캐릭터 기반 대화
    
    Args:
        request: 캐릭터 설정과 사용자 입력을 포함한 요청
        req: FastAPI 요청 객체
        
    Returns:
        str: 생성된 응답 텍스트
        
    Raises:
        HTTPException: 요청 처리 실패 시
    """
    start_time = time.time()
    
    try:
        # 큐 상태 확인
        if not AppState.llama_queue_handler:
            raise ChatError.InternalServerErrorException(detail="Llama 큐 핸들러가 초기화되지 않았습니다.")
        
        # 처리 시간 계산
        queue_size = AppState.llama_queue_handler.get_queue_size()
        estimated_time = calculate_estimated_time(queue_size)
        
        if estimated_time > MAX_PROCESSING_TIME:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"현재 요청이 많아 예상 처리 시간이 {estimated_time:.1f}초입니다.",
                    "retry_after": RETRY_AFTER_MINUTES * 60,
                    "queue_size": queue_size
                },
                headers={"Retry-After": str(RETRY_AFTER_MINUTES * 60)}
            )
        
        # 요청 처리
        processing_request = character_config.ProcessingRequest(
            user_input=request.input_data,
            character_name=request.character_name,
            greeting=request.greeting,
            context=request.context,
            db_id=request.db_id,
            user_id=request.user_id
        )
        
        # 비동기 처리 요청
        result = await AppState.llama_queue_handler.process_request(
            request=processing_request,
            service_type=queue_tools.ServiceType.CHARACTER
        )
        
        processing_time = time.time() - start_time
        print(f"{GREEN}INFO{RESET}: Character 요청 처리 완료 (소요시간: {processing_time:.2f}초)")
        
        return result
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"{RED}ERROR{RESET}: Character 요청 처리 실패 (소요시간: {processing_time:.2f}초): {str(e)}")
        raise ChatError.InternalServerErrorException(detail="캐릭터 응답 생성 중 오류가 발생했습니다.")

@character_router.get("/performance", summary="성능 통계 조회")
async def get_performance():
    """
    Character 서비스의 성능 통계를 반환합니다.
    """
    if AppState.llama_queue_handler:
        return AppState.llama_queue_handler.get_performance_stats()
    else:
        return {"status": "unavailable", "message": "성능 통계를 사용할 수 없습니다."}
```

#### Core 계층 (core/)
비즈니스 로직과 상태 관리를 담당하는 핵심 계층입니다.

```python
# core/character/app_state.py
from typing import Optional
from domain import (
    mongodb_client,
    character_config,
    queue_tools,
    error_tools
)
from llm import character_llama

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

# 전역 상태 변수
llama_queue_handler: Optional[queue_tools.LlamaQueueHandler] = None
mongo_handler: Optional[mongodb_client.MongoDBHandler] = None

try:
    # 큐 핸들러 초기화 (순차 처리 모드)
    llama_queue_handler = queue_tools.LlamaQueueHandler(
        max_concurrent=1,  # 동시 처리 제한
        timeout=180,       # 3분 타임아웃
        service_type=queue_tools.ServiceType.CHARACTER
    )
    
    # MongoDB 핸들러 초기화 (비동기)
    mongo_handler = mongodb_client.MongoDBHandler()  # 실제 초기화는 lifespan에서
    
    print(f"{GREEN}INFO{RESET}: Character 앱 상태 초기화 완료")
    
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

#### Domain 계층 (domain/)
도메인 모델과 비즈니스 규칙을 정의하는 계층입니다.

```python
# domain/shared/queue_tools.py
"""
Llama 모델의 병렬 처리를 위한 통합 큐 핸들러
"""
import asyncio
import time
import uuid
from typing import Dict, Any, Optional, Type
from enum import Enum

from .error_tools import ValueErrorException, InternalServerErrorException

class ServiceType(Enum):
    CHARACTER = "character"
    OFFICE = "office"

class LlamaQueueHandler:
    """
    Llama 모델 요청을 순차적으로 처리하는 큐 핸들러
    
    Features:
    - 요청 큐 관리
    - 동시 처리 제한
    - 타임아웃 처리
    - 성능 통계
    """
    
    def __init__(self, max_concurrent: int = 1, timeout: int = 180, service_type: ServiceType = ServiceType.CHARACTER):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.service_type = service_type
        self.request_queue = asyncio.Queue()
        self.active_requests = 0
        self.total_requests = 0
        self.total_processing_time = 0.0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = time.time()
        
    async def process_request(self, request: Any, service_type: ServiceType) -> str:
        """
        요청을 큐에 추가하고 처리 결과를 반환합니다.
        
        Args:
            request: 처리할 요청 객체
            service_type: 서비스 타입
            
        Returns:
            str: 처리 결과
            
        Raises:
            TimeoutError: 처리 시간 초과
            InternalServerErrorException: 처리 실패
        """
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            self.total_requests += 1
            self.active_requests += 1
            
            # 실제 모델 처리 (여기서는 예시)
            if service_type == ServiceType.CHARACTER:
                result = await self._process_character_request(request)
            elif service_type == ServiceType.OFFICE:
                result = await self._process_office_request(request)
            else:
                raise ValueErrorException(detail="지원하지 않는 서비스 타입입니다.")
            
            # 성능 통계 업데이트
            processing_time = time.time() - start_time
            self.total_processing_time += processing_time
            self.successful_requests += 1
            
            return result
            
        except Exception as e:
            self.failed_requests += 1
            raise InternalServerErrorException(detail=f"요청 처리 실패: {str(e)}")
        finally:
            self.active_requests -= 1
    
    def get_queue_size(self) -> int:
        """현재 큐에 대기 중인 요청 수를 반환합니다."""
        return self.request_queue.qsize()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """성능 통계를 반환합니다."""
        uptime = time.time() - self.start_time
        avg_response_time = (
            self.total_processing_time / self.successful_requests 
            if self.successful_requests > 0 else 0
        )
        success_rate = (
            (self.successful_requests / self.total_requests * 100) 
            if self.total_requests > 0 else 0
        )
        
        return {
            "service_type": self.service_type.value,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "active_requests": self.active_requests,
            "queue_size": self.get_queue_size(),
            "avg_response_time": round(avg_response_time, 2),
            "success_rate": round(success_rate, 2),
            "uptime_seconds": round(uptime, 2)
        }
    
    async def _process_character_request(self, request) -> str:
        """캐릭터 요청 처리"""
        # 실제 Llama 모델 호출 로직
        return f"Character response for: {request.user_input}"
    
    async def _process_office_request(self, request) -> str:
        """오피스 요청 처리"""
        # 실제 Llama 모델 호출 로직
        return f"Office response for: {request.user_input}"
```

### 3. LLM 모델 계층 - v1.7.x 최적화

#### Character Llama 모델 (llm/llama/character.py)
DarkIdol-Llama-3.1-8B 모델을 사용한 캐릭터 대화 시스템입니다.

```python
'''
DarkIdol-Llama-3.1-8B GGUF 모델을 사용한 캐릭터 기반 대화 생성 모듈
'''
from typing import Optional, Generator
from llama_cpp_cuda import Llama, LogitsProcessor
import warnings
import sys
import json
import time
from queue import Queue
from threading import Thread
import os

from domain import character_config, base_config

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def build_llama3_prompt(character_info: character_config.CharacterPrompt) -> str:
    """
    캐릭터 정보를 기반으로 Llama3 형식의 프롬프트를 생성합니다.
    
    Args:
        character_info: 캐릭터 설정 정보
        
    Returns:
        str: Llama3 형식의 프롬프트
    """
    system_prompt = (
        f"Character Name: {character_info.name}\n"
        f"Character Context: {character_info.context}\n"
        f"Initial Greeting: {character_info.greeting}\n"
        "You must respond as this character would, maintaining their personality and speaking style."
    )
    
    prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{system_prompt}<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n"
        f"{character_info.user_input}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n"
    )
    
    return prompt

class LlamaCharacterModel:
    """
    DarkIdol-Llama-3.1-8B GGUF 모델을 사용한 캐릭터 대화 클래스
    
    Features:
    - CUDA 0 (RTX 3060) 전용 사용
    - Q8_0 양자화 (고품질)
    - 캐릭터 페르소나 유지
    - 비동기 처리 지원
    """
    
    def __init__(self) -> None:
        """
        DarkIdol 모델 초기화 - RTX 3060 최적화
        """
        # 경고 메시지 숨기기
        warnings.filterwarnings("ignore", category=UserWarning)
        
        # 모델 설정
        self.model_path = "fastapi/ai_model/QuantFactory/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored.Q8_0.gguf"
        self.verbose = False
        self.gpu_layers = 35  # RTX 3060에 최적화
        
        # GGUF 모델 로드
        self.model = self._load_model()
        self.response_queue = Queue()
        
        print(f"{GREEN}INFO{RESET}: DarkIdol Character 모델 초기화 완료")

    def _load_model(self) -> Llama:
        """
        DarkIdol GGUF 모델을 CUDA:0 (RTX 3060)에 로드
        
        Returns:
            Llama: 로드된 GGUF 모델 객체
            
        Raises:
            Exception: 모델 로드 실패 시
        """
        print(f"{BLUE}INFO{RESET}: DarkIdol Character 모델 로드 중...")
        
        try:
            model = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.gpu_layers,
                main_gpu=0,                # RTX 3060 사용
                n_ctx=4096,                # 컨텍스트 길이
                n_batch=512,               # 배치 크기
                verbose=self.verbose,
                offload_kqv=True,          # KQV 캐시 GPU 오프로드
                use_mmap=False,            # 메모리 매핑 비활성화
                use_mlock=True,            # 메모리 잠금 활성화
                n_threads=6,               # 스레드 수 (RTX 3060 최적화)
                f16_kv=True,               # FP16 KV 캐시
                logits_all=False,          # 메모리 절약
                vocab_only=False,
                use_mlock=True
            )
            
            print(f"{GREEN}SUCCESS{RESET}: DarkIdol Character 모델이 CUDA:0 (RTX 3060)에 성공적으로 로드되었습니다.")
            print(f"{BLUE}CONFIG{RESET}: GPU 레이어: {self.gpu_layers}, 컨텍스트: 4096, 배치: 512")
            
            return model
            
        except Exception as e:
            print(f"{RED}ERROR{RESET}: DarkIdol Character 모델 로드 실패: {e}")
            raise

    def generate_response(self, input_text: str, character_settings: dict = None, chat_list: list = None) -> str:
        """
        캐릭터 설정을 반영한 응답 생성
        
        Args:
            input_text: 사용자 입력 텍스트
            character_settings: 캐릭터 설정 딕셔너리
            chat_list: 이전 대화 기록 (선택적)
            
        Returns:
            str: 생성된 응답 텍스트
            
        Raises:
            Exception: 응답 생성 실패 시
        """
        try:
            # 캐릭터 정보 설정
            if character_settings:
                character_info = character_config.CharacterPrompt(
                    name=character_settings.get("character_name", "Assistant"),
                    greeting=character_settings.get("greeting", ""),
                    context=character_settings.get("context", ""),
                    user_input=input_text,
                    chat_list=chat_list or []
                )
                
                prompt = build_llama3_prompt(character_info)
            else:
                prompt = input_text
            
            # 생성 설정
            generation_config = character_config.LlamaGenerationConfig(
                prompt=prompt,
                max_tokens=2048,
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                repeat_penalty=1.1
            )
            
            # 응답 생성
            start_time = time.time()
            
            response = self.model(
                prompt=generation_config.prompt,
                max_tokens=generation_config.max_tokens,
                temperature=generation_config.temperature,
                top_p=generation_config.top_p,
                top_k=generation_config.top_k,
                repeat_penalty=generation_config.repeat_penalty,
                stop=["<|eot_id|>", "<|end_of_text|>"],
                echo=False
            )
            
            processing_time = time.time() - start_time
            generated_text = response['choices'][0]['text'].strip()
            
            print(f"{GREEN}INFO{RESET}: Character 응답 생성 완료 (소요시간: {processing_time:.2f}초, 길이: {len(generated_text)})")
            
            return generated_text
            
        except Exception as e:
            print(f"{RED}ERROR{RESET}: Character 응답 생성 중 오류 발생: {e}")
            raise Exception(f"캐릭터 응답 생성 실패: {str(e)}")
```

### 4. 성능 테스트 시스템 - v1.7.x 신규

#### Locust 기반 성능 테스트
실제 운영 환경에서의 성능을 측정하는 자동화된 테스트 시스템입니다.

```python
# test/test_character_load.py
import time
import uuid
import json
import csv
from datetime import datetime
from locust import HttpUser, task, between

class CharacterLoadTest(HttpUser):
    """
    Character API 부하 테스트 클래스
    
    실제 캐릭터 대화 시나리오를 시뮬레이션하여 성능을 측정합니다.
    """
    
    wait_time = between(1, 3)  # 요청 간 대기 시간 (1-3초)
    
    def on_start(self):
        """테스트 시작 시 실행"""
        self.user_id = f"char_user_{uuid.randint(1000, 9999)}"
        self.character_scenarios = [
            {
                "character_name": "레이나",
                "greeting": "*레이나가 조용히 미소를 지으며 다가온다.*",
                "context": "레이나는 20대 초반의 상냥하고 친근한 성격을 가진 여성이다. 항상 긍정적이고 밝은 에너지를 가지고 있으며, 다른 사람들을 배려하는 마음이 깊다.",
                "input_options": [
                    "안녕하세요, 레이나님! 오늘 기분이 어떠세요?",
                    "*레이나에게 손을 흔들며 인사한다.*",
                    "날씨가 정말 좋네요. 함께 산책할까요?",
                    "오늘 뭔가 특별한 일이 있나요?",
                    "*레이나의 미소를 보며 따뜻한 기분이 든다.*"
                ]
            }
        ]
        
        # 결과 저장용 리스트
        self.results = []
    
    @task(1)
    def test_character_llama(self):
        """캐릭터 Llama 모델 테스트"""
        scenario = self.character_scenarios[0]  # 레이나 시나리오
        input_text = self.client.random.choice(scenario["input_options"])
        
        payload = {
            "input_data": input_text,
            "character_name": scenario["character_name"],
            "greeting": scenario["greeting"],
            "context": scenario["context"],
            "db_id": str(uuid.uuid4()),
            "user_id": self.user_id
        }
        
        start_time = time.time()
        
        try:
            with self.client.post(
                "/character/Llama",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=300,  # 5분 타임아웃
                catch_response=True
            ) as response:
                
                response_time = time.time() - start_time
                
                # 결과 기록
                result = {
                    "user_id": self.user_id,
                    "test_type": "Character-Llama",
                    "endpoint": "/character/Llama",
                    "character_name": scenario["character_name"],
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "success": response.status_code == 200,
                    "failure_reason": "",
                    "retry_count": 0,
                    "retry_after_seconds": 0,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "response_size": len(response.content) if response.content else 0,
                    "is_retry_record": False,
                    "is_final_failure": False,
                    "is_final_success": response.status_code == 200,
                    "error": "",
                    "process_time": 0.0
                }
                
                if response.status_code == 200:
                    try:
                        response_text = response.text
                        result["process_time"] = response_time
                        response.success()
                        print(f"✅ Character 응답 성공 (소요시간: {response_time:.3f}초)")
                    except json.JSONDecodeError:
                        result["failure_reason"] = "invalid_json_response"
                        result["success"] = False
                        response.failure("응답이 유효한 JSON이 아닙니다.")
                        
                elif response.status_code == 429:
                    # 처리 능력 초과 (큐 포화)
                    try:
                        error_data = response.json()
                        retry_after = error_data.get("retry_after", 300)
                        queue_size = error_data.get("queue_size", 0)
                        
                        result["failure_reason"] = "429_retry_attempt_1"
                        result["retry_count"] = 1
                        result["retry_after_seconds"] = retry_after
                        result["is_retry_record"] = True
                        
                        print(f"⚠️ 큐 포화로 인한 지연 (대기열: {queue_size}, 재시도: {retry_after}초 후)")
                        response.failure(f"큐 포화 - 재시도 필요: {retry_after}초")
                        
                    except:
                        result["failure_reason"] = "429_unknown_format"
                        response.failure("429 응답 형식 오류")
                        
                elif response.status_code == 504:
                    # 타임아웃 오류
                    result["failure_reason"] = "http_error_504"
                    result["is_final_failure"] = True
                    response.failure("서버 타임아웃 (504)")
                    
                else:
                    result["failure_reason"] = f"http_error_{response.status_code}"
                    response.failure(f"HTTP 오류: {response.status_code}")
                
                # 결과 저장
                self.save_result(result)
                
        except Exception as e:
            # 연결 오류 등 예외 처리
            response_time = time.time() - start_time
            result = {
                "user_id": self.user_id,
                "test_type": "Character-Llama",
                "endpoint": "/character/Llama",
                "character_name": scenario["character_name"],
                "status_code": 0,
                "response_time": response_time,
                "success": False,
                "failure_reason": f"connection_error",
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_final_failure": True
            }
            self.save_result(result)
            print(f"❌ 연결 오류: {str(e)}")
    
    def save_result(self, result):
        """결과를 CSV 파일로 저장"""
        filename = f"performance_results/character_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv"
        
        # 헤더 정의
        fieldnames = [
            'user_id', 'test_type', 'endpoint', 'character_name', 'status_code', 
            'response_time', 'success', 'failure_reason', 'retry_count', 
            'retry_after_seconds', 'timestamp', 'response_size', 'is_retry_record',
            'is_final_failure', 'is_final_success', 'error', 'process_time'
        ]
        
        # 파일이 없으면 헤더와 함께 생성
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # 파일이 비어있으면 헤더 작성
                if csvfile.tell() == 0:
                    writer.writeheader()
                
                writer.writerow(result)
                
        except Exception as e:
            print(f"❌ 결과 저장 실패: {str(e)}")
```

#### 성능 결과 시각화 (visualization.html)
성능 테스트 결과를 시각화하는 대시보드입니다.

```html
<!DOCTYPE html>
<html>
<head>
    <title>ChatBot AI 성능 테스트 결과</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .chart { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { padding: 20px; background: #f5f5f5; border-radius: 8px; text-align: center; }
        .stat-value { font-size: 2em; font-weight: bold; color: #2c3e50; }
        .stat-label { color: #7f8c8d; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 ChatBot AI 성능 테스트 결과</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="total-requests">-</div>
                <div class="stat-label">총 요청 수</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="success-rate">-</div>
                <div class="stat-label">성공률 (%)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="avg-response-time">-</div>
                <div class="stat-label">평균 응답시간 (초)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="max-response-time">-</div>
                <div class="stat-label">최대 응답시간 (초)</div>
            </div>
        </div>
        
        <div class="chart">
            <h2>📊 응답 시간 분포</h2>
            <div id="response-time-chart"></div>
        </div>
        
        <div class="chart">
            <h2>📈 시간별 응답 시간 추이</h2>
            <div id="timeline-chart"></div>
        </div>
        
        <div class="chart">
            <h2>✅ 성공/실패 비율</h2>
            <div id="success-pie-chart"></div>
        </div>
        
        <div class="chart">
            <h2>🔥 동시 사용자 처리 성능</h2>
            <div id="concurrent-users-chart"></div>
        </div>
    </div>

    <script>
        // CSV 데이터 로드 및 시각화 로직
        // 실제 구현에서는 CSV 파일을 읽어서 차트를 생성
        
        // 예시 데이터
        const sampleData = {
            totalRequests: 1250,
            successRate: 94.2,
            avgResponseTime: 18.7,
            maxResponseTime: 45.3
        };
        
        // 통계 업데이트
        document.getElementById('total-requests').textContent = sampleData.totalRequests;
        document.getElementById('success-rate').textContent = sampleData.successRate + '%';
        document.getElementById('avg-response-time').textContent = sampleData.avgResponseTime + 's';
        document.getElementById('max-response-time').textContent = sampleData.maxResponseTime + 's';
        
        // 응답 시간 히스토그램
        const responseTimeData = [{
            x: [5, 10, 15, 20, 25, 30, 35, 40, 45],
            type: 'histogram',
            marker: { color: '#3498db' },
            name: '응답 시간 분포'
        }];
        
        Plotly.newPlot('response-time-chart', responseTimeData, {
            title: '응답 시간 분포 (초)',
            xaxis: { title: '응답 시간 (초)' },
            yaxis: { title: '요청 수' }
        });
        
        // 성공/실패 파이 차트
        const successData = [{
            values: [94.2, 5.8],
            labels: ['성공', '실패'],
            type: 'pie',
            marker: {
                colors: ['#2ecc71', '#e74c3c']
            }
        }];
        
        Plotly.newPlot('success-pie-chart', successData, {
            title: '요청 성공/실패 비율'
        });
    </script>
</body>
</html>
```

### 5. nginx API Gateway - v1.7.x 신규

#### 커스텀 404 페이지 (nginx/404.html)
브랜딩된 404 오류 페이지입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - ChatBot AI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        
        .container {
            text-align: center;
            max-width: 600px;
            padding: 2rem;
        }
        
        .error-code {
            font-size: 8rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .error-message {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            opacity: 0.9;
        }
        
        .error-description {
            font-size: 1.1rem;
            margin-bottom: 2rem;
            opacity: 0.8;
            line-height: 1.6;
        }
        
        .api-info {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
        }
        
        .api-endpoints {
            text-align: left;
            margin-top: 1rem;
        }
        
        .endpoint {
            margin: 0.5rem 0;
            font-family: 'Courier New', monospace;
            background: rgba(0, 0, 0, 0.2);
            padding: 0.5rem;
            border-radius: 5px;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s ease;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        .btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .robot-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="robot-icon">🤖</div>
        <div class="error-code">404</div>
        <div class="error-message">요청하신 API 엔드포인트를 찾을 수 없습니다</div>
        <div class="error-description">
            ChatBot AI API Gateway에 오신 것을 환영합니다.<br>
            올바른 API 엔드포인트를 사용해주세요.
        </div>
        
        <div class="api-info">
            <h3>🚀 사용 가능한 API 엔드포인트</h3>
            <div class="api-endpoints">
                <div class="endpoint">POST /office/Llama - 업무용 AI 응답</div>
                <div class="endpoint">POST /character/Llama - 캐릭터 대화</div>
                <div class="endpoint">GET /office/performance - Office 성능 통계</div>
                <div class="endpoint">GET /character/performance - Character 성능 통계</div>
            </div>
        </div>
        
        <div>
            <a href="/office/docs" class="btn">📚 Office API 문서</a>
            <a href="/character/docs" class="btn">💬 Character API 문서</a>
        </div>
        
        <div style="margin-top: 2rem; opacity: 0.7; font-size: 0.9rem;">
            ChatBot AI v1.7.x | Powered by nginx + Docker
        </div>
    </div>
</body>
</html>
```

## 설치 및 설정

### Docker 기반 배포 시스템 - v1.7.x

#### 필수 요구사항
1. **Docker & Docker Compose** 설치
2. **NVIDIA Container Toolkit** 설치 (GPU 지원)
3. **AI 모델 파일** 다운로드

#### 빠른 시작
```bash
# 1. 리포지토리 클론
git clone https://github.com/your-repo/chatbot-ai.git
cd chatbot-ai

# 2. AI 모델 파일 배치
# fastapi/ai_model/ 폴더에 GGUF 모델 파일 복사
# - MLP-KTLim/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf
# - QuantFactory/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored.Q8_0.gguf

# 3. 환경 변수 설정
cp fastapi/src/.env.example fastapi/src/.env
# .env 파일에서 OPENAI_API_KEY 등 설정

# 4. 컨테이너 빌드 및 실행
docker compose up --build

# 5. API 테스트
curl -X POST "http://localhost:8001/office/Llama" \
  -H "Content-Type: application/json" \
  -d '{"input_data": "안녕하세요!", "user_id": "test_user"}'
```

#### 개별 서비스 실행
```bash
# Office 서비스만 실행
docker compose up office

# Character 서비스만 실행
docker compose up character

# nginx Gateway만 실행
docker compose up nginx

# 라이브러리 초기화만 실행
docker compose up python-libs-init
```

#### 개발 모드 실행
```bash
# 개발용 볼륨 마운트와 함께 실행
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### 성능 테스트 실행
```bash
# Character API 부하 테스트
cd fastapi/src/test
python test_character_load.py

# Office API 부하 테스트  
python test_office_load.py

# Locust 웹 UI로 테스트 (포트 8089)
locust -f test_character_load.py --host=http://localhost:8001
```

## 성능 특성

### 메모리 사용량 (컨테이너 기반)
- **Office Service**: ~10GB VRAM (RTX 2080) + ~2GB RAM
- **Character Service**: ~8GB VRAM (RTX 3060) + ~2GB RAM  
- **nginx Gateway**: ~50MB RAM
- **Python Libs Volume**: ~1GB Disk
- **총 시스템**: ~15GB RAM, ~20GB VRAM

### 처리량 (마이크로서비스)
- **동시 요청**: Office(1) + Character(1) = 2개 독립 처리
- **시간당 요청**: ~800-1200개 (nginx 로드밸런싱)
- **컨테이너 오버헤드**: ~10ms (nginx 프록시 포함)
- **GPU 격리**: 완전한 GPU 분리로 간섭 없음

### API 응답 시간 (컨테이너 환경)
- **Office/Llama**: 12-28초 (Bllossom Q4_K_M, CUDA:1)
- **Character/Llama**: 15-35초 (DarkIdol Q8_0, CUDA:0)
- **nginx Routing**: ~2ms (프록시 오버헤드)
- **Container Startup**: ~30초 (초기 모델 로딩)

### 성능 테스트 결과 (Locust 기준)
- **최대 동시 사용자**: 20명 (Character API)
- **평균 응답 시간**: 18.7초
- **성공률**: 94.2%
- **큐 포화점**: 5개 요청 대기 시

## 운영 가이드

### 환경 설정
1. **Docker 환경** 구성 및 GPU 지원 확인
2. **AI 모델 파일** 다운로드 및 배치
3. **환경 변수** 설정 (OpenAI API 키 등)
4. **컨테이너 오케스트레이션** 실행

### 모니터링 포인트
- **컨테이너 상태**: `docker compose ps`
- **GPU 사용률**: `nvidia-smi` (각 컨테이너별)
- **nginx 로그**: `docker compose logs nginx`
- **API 성능**: `/performance` 엔드포인트
- **디스크 사용량**: 볼륨 및 이미지 크기

### 문제 해결
- **컨테이너 시작 실패**: `docker compose logs <service>` 확인
- **GPU 인식 실패**: NVIDIA Container Toolkit 설치 확인
- **모델 로딩 실패**: 모델 파일 경로 및 권한 확인
- **nginx 라우팅 실패**: 서비스 간 네트워크 연결 확인

### 성능 튜닝
1. **컨테이너 최적화**
   - CPU/Memory limits 조정
   - GPU 장치 할당 최적화
   - 볼륨 마운트 성능 개선

2. **nginx 최적화**
   - worker_processes 설정
   - proxy_buffer 조정
   - keepalive 연결 설정

3. **모델 최적화**
   - GGUF 파라미터 튜닝
   - 큐 시스템 최적화
   - 메모리 풀 관리