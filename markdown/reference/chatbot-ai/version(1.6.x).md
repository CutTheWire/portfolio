# ChatBot AI - 버전 명세서 v1.6.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.6.x 계열 버전에 대한 공식 명세서입니다. v1.5.x의 라우터 기반 아키텍처에서 **컨트롤러 패턴 도입**과 **프로덕션 최적화**를 통해 **엔터프라이즈급 구조**로 완전히 전환되었으며, **GitHub Actions CI/CD**, **API 명세서 자동화**, **모듈 분리 최적화**를 도입한 프로덕션 준비 AI 챗봇 서비스입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.6.0** | 2025-05-10 | `abf6e1d4667e08418e661bcee41e6fc83cde9922` | Stable |
| **v1.6.1** | 2025-05-11 | `e93961d80627087bd9f284d52bac1f76d31c5613` | Latest |
| **None** | 2025-05-16 | `0b5d65da73cae825fbf76e853fce56d86e103ae1` | Unstable |

## v1.5.x에서 v1.6.x로의 주요 변경사항

### 아키텍처 완전 재편
- **라우터 기반** → **MVC 컨트롤러 패턴** 도입
- **모노리식 프로토타입** → **프로덕션/프로토타입 완전 분리**
- **단일 서버 파일** → **모듈화된 컨트롤러 시스템**

### AI 모델 통합 최적화
- **Bllossom/Lumimaid** → **통합 Office/Character 모델**
- **DarkIdol-Llama-3.1-8B** 도입 (캐릭터 특화)
- **공유 상태 관리** 시스템 (`app_state.py`)

### 개발 환경 혁신
- **GitHub Actions** CI/CD 파이프라인
- **자동 API 명세서** 생성 (`api_specification.md`)
- **프로토타입 정리** (14개 파일 삭제)
- **라우터 분리** (`office_controller.py`, `character_controller.py`)

### 신규 기능
- **ExceptionManager** 클래스 (예외 처리 통합)
- **로그 시스템** 개선 (날짜별 회전 로그)
- **코드 품질** 관리 (패키지 버전 통일)
- **웹사이트 연동** (Treenut 웹사이트 링크)

### 제거된 기능
- ❌ **모든 프로토타입** 파일 제거 (프로덕션 정리)
- ❌ **config-user.yaml** 설정 파일 제거
- ❌ **서버 파일 내 라우터** 로직 (컨트롤러 분리)

## 시스템 요구사항

### 하드웨어 요구사항
- **GPU**: NVIDIA RTX 3060 (CUDA:0) + RTX 2080 (CUDA:1)
- **VRAM**: 최소 20GB RAM (3060 12GB + 2080 8GB)
- **저장공간**: 최소 50GB 여유 공간
- **네트워크**: 고속 인터넷 (OpenAI API + GitHub Actions)

### 소프트웨어 요구사항
- **운영체제**: Windows 10/11 (64-bit)
- **Python**: 3.11 이상
- **CUDA**: 11.8/12.8 지원
- **llama-cpp-python**: CUDA 지원 버전
- **MongoDB**: 로컬 설치
- **OpenAI API**: 유효한 API 키
- **GitHub**: Actions 활성화

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot AI v1.6.x
├── 📁 .github/                  # GitHub Actions [NEW]
│   └── 📁 workflows/
│       └── update-api-docs.yml [NEW]
├── 📁 fastapi/
│   ├── 📁 ai_model/             # GGUF 모델 저장소
│   │   ├── DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored.Q8_0.gguf [NEW]
│   │   ├── llama-3-Korean-Bllossom-8B-Q4_K_M.gguf
│   │   └── README.md [UPDATED]
│   ├── 📁 batch/                # 환경 설정 배치 파일
│   │   ├── venv_install.bat
│   │   └── venv_setup.bat [UPDATED]
│   ├── 📁 src/
│   │   ├── 📁 docs/             # API 명세서 [NEW]
│   │   │   └── api_specification.md [NEW]
│   │   ├── 📁 utils/            # 모듈화된 유틸리티
│   │   │   ├── 📁 ai_models/    # AI 모델 모듈
│   │   │   │   ├── llama_character_model.py [RENAMED]
│   │   │   │   ├── llama_office_model.py [RENAMED]
│   │   │   │   ├── openai_character_model.py [UPDATED]
│   │   │   │   └── openai_office_model.py [UPDATED]
│   │   │   ├── 📁 handlers/     # 핸들러 모듈
│   │   │   │   └── error_handler.py [COMPLETELY REDESIGNED]
│   │   │   ├── 📁 routers/      # 컨트롤러 패턴 [NEW]
│   │   │   │   ├── office_controller.py [NEW]
│   │   │   │   └── character_controller.py [NEW]
│   │   │   ├── 📁 schemas/      # 스키마 모듈
│   │   │   │   └── chat_schema.py [UPDATED]
│   │   │   ├── app_state.py [NEW]
│   │   │   └── __init__.py [UPDATED]
│   │   ├── server.py [COMPLETELY REDESIGNED]
│   │   ├── bot.yaml
│   │   └── .env
│   └── requirements.txt [UPDATED]
├── 📁 prompt/                   # 프롬프트 및 설정 파일
│   ├── config-Llama.json [UPDATED]
│   └── config-OpenAI.json [UPDATED]
├── CODE_OF_CONDUCT.md [UPDATED]
└── README.md [UPDATED]
```

## API 명세

### 컨트롤러 기반 API 아키텍처

#### Office Controller (`/office`)
업무 및 일반적인 질의응답을 처리하는 컨트롤러입니다.

##### POST /office/Llama
LlamaOffice GGUF 모델 기반 검색 연동 JSON 응답

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

##### POST /office/{gpt_set}
OpenAI GPT 모델 기반 검색 연동 JSON 응답

**경로 매개변수:**
- `gpt_set`: OpenAI 모델 별칭
  - `gpt4o_mini` → `gpt-4o-mini`
  - `gpt4.1` → `gpt-4.1`
  - `gpt4.1_mini` → `gpt-4.1-mini`

#### Character Controller (`/character`)
캐릭터 기반 대화를 처리하는 컨트롤러입니다.

##### POST /character/Llama
LlamaCharacter GGUF 모델 기반 캐릭터 대화 JSON 응답

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

##### POST /character/{gpt_set}
OpenAI GPT 모델 기반 캐릭터 대화 JSON 응답

**예시 요청:**
```json
{
  "input_data": "*I approach Rachel and talk to her.*",
  "character_name": "Rachel",
  "greeting": "*Rachel stands nervously at the lectern...*",
  "context": "Rachel is a devout Catholic girl of about 19 years old...",
  "db_id": "b440780c-cbaa-454f-a8d2-cf884786d89f",
  "user_id": "djjdjs74"
}
```

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청 (잘못된 모델명)
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. 서버 컴포넌트 (server.py) - v1.6.x 완전 재설계

#### 컨트롤러 패턴 도입
v1.5.x의 라우터 통합에서 **MVC 컨트롤러 패턴**으로 완전 전환되었습니다.

```python
import utils.app_state as AppState
from utils import (
    LlamaOffice,
    LlamaCharacter,
    OfficeController,
    ChearacterController,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI AI 모델 애플리케이션 초기화 - v1.6.x
    컨트롤러 패턴 기반 모듈화된 시스템
    """
    def get_cuda_device_info(device_id: int) -> str:
        """
        주어진 CUDA 장치 ID에 대한 정보를 반환합니다.
        """
        device_name = torch.cuda.get_device_name(device_id)
        device_properties = torch.cuda.get_device_properties(device_id)
        total_memory = device_properties.total_memory / (1024 ** 3)
        return f"Device {device_id}: {device_name} (Total Memory: {total_memory:.2f} GB)"
    
    try:
        # 공유 상태 관리 시스템
        AppState.LlamaOffice_model = LlamaOffice()          # cuda:1 (RTX 2080)
        AppState.LlamaCharacter_model = LlamaCharacter()    # cuda:0 (RTX 3060)
    except ChatError.InternalServerErrorException as e:
        print(f"{RED}ERROR{RESET}: 모델 초기화 중 오류 발생: {str(e)}")
        exit(1)
        
    # 디버깅용 출력
    LlamaOffice_device_info = get_cuda_device_info(1)      # LlamaOffice 모델은 cuda:1
    LlamaCharacter_device_info = get_cuda_device_info(0)   # LlamaCharacter 모델은 cuda:0
    print(f"{GREEN}INFO{RESET}: LlamaOffice 모델 로드 완료 ({LlamaOffice_device_info})")
    print(f"{GREEN}INFO{RESET}: LlamaCharacter 모델 로드 완료 ({LlamaCharacter_device_info})")

    yield

    # 모델 메모리 해제
    AppState.LlamaOffice_model = None
    AppState.LlamaCharacter_model = None
    print(f"{GREEN}INFO{RESET}: 모델 해제 완료")

app = FastAPI(lifespan=lifespan)

# 컨트롤러 등록
app.include_router(
    OfficeController.office_router,
    prefix="/office",
    tags=["Office API"],
    responses={500: {"description": "Internal Server Error"}}
)

app.include_router(
    ChearacterController.character_router,
    prefix="/character",
    tags=["Character API"],
    responses={500: {"description": "Internal Server Error"}}
)
```

#### 개선된 API 정보 시스템
버전 관리와 로고가 개선된 OpenAPI 명세서입니다.

```python
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="ChatBot AI API",
        version="v1.6.*",
        summary="AI 모델 관리 API",
        description=(
            "이 API는 AI 기반 챗봇 서비스를 제공합니다.\n\n"
            "주요 기능:\n"
            "- LlamaOffice: 업무용 AI 응답 생성\n"
            "- LlamaCharacter: 캐릭터 기반 대화 생성\n"
            "- OpenAI GPT: 고품질 AI 응답 생성\n"
            "- DuckDuckGo 검색: 실시간 정보 검색 연동"
        ),
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://drive.google.com/thumbnail?id=12PqUS6bj4eAO_fLDaWQmoq94-771xfim"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### 2. 공유 상태 관리 컴포넌트 (app_state.py) - v1.6.x 신규

#### 전역 상태 관리 시스템
모델 인스턴스를 전역적으로 관리하는 상태 관리 시스템입니다.

```python
"""
애플리케이션 전역 상태 관리 모듈

이 모듈은 FastAPI 애플리케이션의 전역 상태를 관리합니다.
주로 AI 모델 인스턴스들을 저장하고 접근할 수 있도록 합니다.

전역 변수:
    LlamaOffice_model: Office용 Llama 모델 인스턴스
    LlamaCharacter_model: Character용 Llama 모델 인스턴스

사용 예시:
    from utils import app_state as AppState
    
    # 모델 할당
    AppState.LlamaOffice_model = LlamaOffice()
    
    # 모델 사용
    response = AppState.LlamaOffice_model.generate_response(input_text)
    
    # 모델 해제
    AppState.LlamaOffice_model = None
"""

# AI 모델 인스턴스들을 저장할 전역 변수
LlamaOffice_model = None
LlamaCharacter_model = None

def get_office_model():
    """Office 모델 인스턴스를 반환합니다."""
    return LlamaOffice_model

def get_character_model():
    """Character 모델 인스턴스를 반환합니다."""
    return LlamaCharacter_model

def set_office_model(model):
    """Office 모델 인스턴스를 설정합니다."""
    global LlamaOffice_model
    LlamaOffice_model = model

def set_character_model(model):
    """Character 모델 인스턴스를 설정합니다."""
    global LlamaCharacter_model
    LlamaCharacter_model = model

def clear_all_models():
    """모든 모델 인스턴스를 해제합니다."""
    global LlamaOffice_model, LlamaCharacter_model
    LlamaOffice_model = None
    LlamaCharacter_model = None
```

### 3. 컨트롤러 컴포넌트 - v1.6.x 신규

#### OfficeController 클래스 (office_controller.py) - 신규 추가

Office 라우터 로직을 완전히 분리한 컨트롤러입니다.

```python
"""
Office 라우터 컨트롤러

업무 및 일반적인 질의응답을 처리하는 라우터 컨트롤러입니다.
DuckDuckGo 검색 연동과 MongoDB 채팅 기록 관리를 지원합니다.

지원 모델:
- LlamaOffice: Bllossom-8B GGUF 모델
- OpenAI GPT: GPT-4o-mini, GPT-4.1, GPT-4.1-mini

주요 기능:
- 검색 기반 응답 생성
- 채팅 기록 관리
- JSON 응답 형식
"""

from fastapi import APIRouter, Path, HTTPException
from pydantic import ValidationError
import utils.app_state as AppState
from utils import ChatModel, ChatError, ChatSearch, MongoDBHandler, OpenAiOffice

# OpenAI 모델 매핑
OPENAI_MODEL_MAP = {
    "gpt4o_mini": "gpt-4o-mini",
    "gpt4.1": "gpt-4.1",
    "gpt4.1_mini": "gpt-4.1-mini",
}

office_router = APIRouter()

# MongoDB 핸들러 초기화
try:
    mongo_handler = MongoDBHandler()
except Exception as e:
    mongo_handler = None
    print(f"MongoDB 초기화 오류: {str(e)}")

@office_router.post("/Llama", summary="Llama 모델이 검색 결과를 활용하여 답변 생성")
async def office_llama(request: ChatModel.office_Request):
    """
    LlamaOffice GGUF 모델 기반 검색 연동 응답
    """
    chat_list = []
    search_context = ""
    
    # MongoDB에서 채팅 기록 가져오기
    if mongo_handler and request.db_id:
        try:
            chat_list = await mongo_handler.get_office_log(
                user_id=request.user_id,
                document_id=request.db_id,
                router="office",
            )
        except Exception as e:
            print(f"WARNING: 채팅 기록을 가져오는 데 실패했습니다: {str(e)}")

    # DuckDuckGo 검색 결과 가져오기
    if request.google_access:
        try:
            duck_results = await ChatSearch.fetch_duck_search_results(query=request.input_data)
            
            if duck_results:
                formatted_results = []
                for idx, item in enumerate(duck_results[:10], 1):
                    formatted_result = (
                        f"[검색결과 {idx}]\n"
                        f"제목: {item.get('title', '제목 없음')}\n"
                        f"내용: {item.get('snippet', '내용 없음')}\n"
                        f"출처: {item.get('link', '링크 없음')}\n"
                    )
                    formatted_results.append(formatted_result)
                
                search_context = (
                    "다음은 검색에서 가져온 관련 정보입니다:\n\n" +
                    "\n".join(formatted_results)
                )
        except Exception:
            print("WARNING: DuckDuckGo 검색 실패")
            search_context = ""

    try:        
        full_response = AppState.LlamaOffice_model.generate_response(
            input_text=request.input_data,
            search_text=search_context,
            chat_list=chat_list,
        )
        return full_response

    except Exception as e:
        print(f"처리되지 않은 예외: {e}")
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")

@office_router.post("/{gpt_set}", summary="GPT 모델이 검색 결과를 활용하여 답변 생성")
async def office_gpt(
        request: ChatModel.office_Request,
        gpt_set: str = Path(
            ...,
            title="GPT 모델명",
            description="사용할 OpenAI GPT 모델의 별칭",
            examples=list(OPENAI_MODEL_MAP.keys()),
        )
    ):
    """
    OpenAI GPT 모델 기반 검색 연동 응답
    """
    if gpt_set not in OPENAI_MODEL_MAP:
        raise HTTPException(status_code=400, detail="Invalid model name.")

    model_id = OPENAI_MODEL_MAP[gpt_set]
    chat_list = []
    search_context = ""

    # MongoDB에서 채팅 기록 가져오기
    if mongo_handler and request.db_id:
        try:
            chat_list = await mongo_handler.get_office_log(
                user_id=request.user_id,
                document_id=request.db_id,
                router="office",
            )
        except Exception as e:
            print(f"WARNING: 채팅 기록을 가져오는 데 실패했습니다: {str(e)}")

    # DuckDuckGo 검색 결과 가져오기 (office_llama와 동일 로직)
    if request.google_access:
        # ... (검색 로직 동일)

    OpenAiOffice_model = OpenAiOffice(model_id=model_id)
    try:
        full_response = OpenAiOffice_model.generate_response(
            input_text=request.input_data,
            search_text=search_context,
            chat_list=chat_list,
        )
        return full_response

    except Exception as e:
        print(f"처리되지 않은 예외: {e}")
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")
```

#### CharacterController 클래스 (character_controller.py) - 신규 추가

Character 라우터 로직을 완전히 분리한 컨트롤러입니다.

```python
"""
Character 라우터 컨트롤러

캐릭터 기반 대화를 처리하는 라우터 컨트롤러입니다.
MongoDB 채팅 기록 관리와 캐릭터 설정 관리를 지원합니다.

지원 모델:
- LlamaCharacter: DarkIdol-Llama-3.1-8B GGUF 모델
- OpenAI GPT: GPT-4o-mini, GPT-4.1, GPT-4.1-mini

주요 기능:
- 캐릭터 기반 대화 생성
- 채팅 기록 관리
- JSON 응답 형식
"""

from fastapi import APIRouter, Path, HTTPException
from pydantic import ValidationError
import utils.app_state as AppState
from utils import ChatModel, ChatError, MongoDBHandler, OpenAiCharacter

# OpenAI 모델 매핑
OPENAI_MODEL_MAP = {
    "gpt4o_mini": "gpt-4o-mini",
    "gpt4.1": "gpt-4.1",
    "gpt4.1_mini": "gpt-4.1-mini",
}

character_router = APIRouter()

# MongoDB 핸들러 초기화
try:
    mongo_handler = MongoDBHandler()
except Exception as e:
    mongo_handler = None
    print(f"MongoDB 초기화 오류: {str(e)}")

@character_router.post("/Llama", summary="Llama 모델이 캐릭터 정보를 기반으로 답변 생성")
async def character_llama(request: ChatModel.character_Request):
    """
    LlamaCharacter GGUF 모델 기반 캐릭터 대화
    """
    chat_list = []
    
    # MongoDB에서 채팅 기록 가져오기
    if mongo_handler and request.db_id:
        try:
            chat_list = await mongo_handler.get_character_log(
                user_id=request.user_id,
                document_id=request.db_id,
                router="character",
            )
        except Exception as e:
            print(f"WARNING: 채팅 기록을 가져오는 데 실패했습니다: {str(e)}")
            
    try:
        character_settings = {
            "character_name": request.character_name,
            "greeting": request.greeting,
            "context": request.context,
            "chat_list": chat_list,
        }
        full_response = AppState.LlamaCharacter_model.generate_response(
            input_text=request.input_data,
            character_settings=character_settings,
        )
        return full_response

    except Exception as e:
        print(f"처리되지 않은 예외: {e}")
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")

@character_router.post("/{gpt_set}", summary="GPT 모델이 캐릭터 정보를 기반으로 답변 생성")
async def character_gpt(
        request: ChatModel.character_Request,
        gpt_set: str = Path(
            ...,
            title="GPT 모델명",
            description="사용할 OpenAI GPT 모델의 별칭",
            examples=list(OPENAI_MODEL_MAP.keys()),
        )
    ):
    """
    OpenAI GPT 모델 기반 캐릭터 대화
    """
    if gpt_set not in OPENAI_MODEL_MAP:
        raise HTTPException(status_code=400, detail="Invalid model name.")

    model_id = OPENAI_MODEL_MAP[gpt_set]
    chat_list = []
    
    # MongoDB에서 채팅 기록 가져오기
    if mongo_handler and request.db_id:
        try:
            chat_list = await mongo_handler.get_character_log(
                user_id=request.user_id,
                document_id=request.db_id,
                router="character",
            )
        except Exception as e:
            print(f"WARNING: 채팅 기록을 가져오는 데 실패했습니다: {str(e)}")

    OpenAiCharacter_model = OpenAiCharacter(model_id=model_id)
    try:
        character_settings = {
            "character_name": request.character_name,
            "greeting": request.greeting,
            "context": request.context,
            "chat_list": chat_list,
        }
        full_response = OpenAiCharacter_model.generate_response(
            input_text=request.input_data,
            character_settings=character_settings,
        )
        return full_response

    except Exception as e:
        print(f"처리되지 않은 예외: {e}")
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")
```

### 4. 예외 처리 컴포넌트 (error_handler.py) - v1.6.x 완전 재설계

#### ExceptionManager 클래스 도입
통합된 예외 처리 관리 시스템입니다.

```python
"""
FastAPI 애플리케이션에서 발생하는 예외를 처리하는 모듈입니다.
v1.6.x에서 ExceptionManager 클래스 패턴으로 완전 재설계되었습니다.
"""

import uuid
import os
import logging
import traceback
from datetime import datetime
from typing import Callable, Dict, Optional, Type, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

# ==========================
# 1. 로그 디렉토리 및 설정
# ==========================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

class DailyRotatingFileHandler(logging.handlers.BaseRotatingHandler):
    """
    날짜별 로그 파일을 생성하는 커스텀 핸들러입니다.
    """
    def __init__(self, dir_path: str, date_format: str = "%Y%m%d", encoding=None):
        self.dir_path = dir_path
        self.date_format = date_format
        self.current_date = datetime.now().strftime(self.date_format)
        log_file = os.path.join(dir_path, f"error_{self.current_date}.log")
        super().__init__(log_file, 'a', encoding)

    def shouldRollover(self, record):
        return datetime.now().strftime(self.date_format) != self.current_date

    def doRollover(self):
        self.stream.close()
        self.current_date = datetime.now().strftime(self.date_format)
        log_file = os.path.join(self.dir_path, f"error_{self.current_date}.log")
        self.baseFilename = log_file
        self.stream = self._open()

# ==========================
# 2. Logger 구성
# ==========================
logger = logging.getLogger("fastapi_error_handlers")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s:\n%(message)s\n',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler = DailyRotatingFileHandler(LOG_DIR, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# ==========================
# 3. 예외 클래스 정의
# ==========================
class BaseCustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundException(BaseCustomException):
    def __init__(self, detail="Resource not found"):
        super().__init__(404, detail)

class BadRequestException(BaseCustomException):
    def __init__(self, detail="Bad request"):
        super().__init__(400, detail)

class UnauthorizedException(BaseCustomException):
    def __init__(self, detail="Unauthorized"):
        super().__init__(401, detail)

class ForbiddenException(BaseCustomException):
    def __init__(self, detail="Forbidden"):
        super().__init__(403, detail)

class ValueErrorException(BaseCustomException):
    def __init__(self, detail="Invalid value"):
        super().__init__(422, detail)

class InternalServerErrorException(BaseCustomException):
    def __init__(self, detail="Internal Server Error"):
        trace_id = uuid.uuid4()
        super().__init__(500, detail)

class DatabaseErrorException(BaseCustomException):
    def __init__(self, detail="Database Error"):
        super().__init__(503, detail)

class IPRestrictedException(BaseCustomException):
    def __init__(self, detail="Unauthorized IP address"):
        super().__init__(403, detail)

class MethodNotAllowedException(BaseCustomException):
    def __init__(self, detail="Method Not Allowed"):
        super().__init__(405, detail)

class RouteNotFoundException(BaseCustomException):
    def __init__(self, detail="Route not found"):
        super().__init__(404, detail)

# ==========================
# 4. 핸들러 함수
# ==========================
def log_error(
    *,
    exc: Exception,
    request: Request,
    status_code: int,
    detail: str,
    extra: dict = None
):
    """
    에러 정보를 로그로 기록하는 함수.
    """
    body = ""
    try:
        body = request._body.decode('utf-8') if hasattr(request, "_body") and request._body else ""
    except Exception:
        pass

    client_ip = request.client.host if request.client else "Unknown"
    query_params = dict(request.query_params)

    # 포맷터에 맡기고, 메시지는 본문만 작성
    log_msg = (
        f"{'='*80}\n"
        f"Error Type: {type(exc).__name__}\n"
        f"Status: {status_code}\n"
        f"Detail: {detail}\n"
        f"URL: {request.url}\n"
        f"Method: {request.method}\n"
        f"Client IP: {client_ip}\n"
        f"Body: {body}\n"
        f"Query: {query_params}\n"
    )

    # traceback이 extra에 있으면 별도로 추가
    if extra and "traceback" in extra:
        log_msg += f"Traceback:\n{extra['traceback']}\n"
    if extra:
        log_msg += f"Extra: {extra}\n"
    log_msg += f"{'='*80}"
    
    logger.error(log_msg)

class ExceptionHandlerFactory:
    """
    예외 핸들러 팩토리 클래스
    """
    handlers: Dict[Type[HTTPException], Callable[[Request, HTTPException], JSONResponse]] = {
        NotFoundException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": "Not found"}),
        BadRequestException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": "Bad request"}),
        UnauthorizedException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": "Unauthorized"}),
        ForbiddenException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": "Forbidden"}),
        ValueErrorException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": "Invalid input"}),
        InternalServerErrorException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": "Server error"}),
        DatabaseErrorException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": "Database error"}),
        IPRestrictedException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": exc.detail}),
        MethodNotAllowedException: lambda req, exc: JSONResponse(status_code=exc.status_code, content={"detail": "Not allowed"})
    }

    @staticmethod
    async def generic_handler(request: Request, exc: HTTPException) -> JSONResponse:
        handler = ExceptionHandlerFactory.handlers.get(type(exc))
        log_error(
            exc=exc,
            request=request,
            status_code=exc.status_code,
            detail=exc.detail
        )
        return handler(request, exc) if handler else JSONResponse(
            status_code=500,
            content={"detail": "Unexpected error", "type": type(exc).__name__}
        )

    @staticmethod
    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        error_details = [
            {"location": err["loc"], "message": err["msg"], "type": err["type"]}
            for err in exc.errors()
        ]
        log_error(
            exc=exc,
            request=request,
            status_code=422,
            detail="입력 데이터 검증 실패",
            extra={"validation_errors": error_details}
        )
        return JSONResponse(status_code=422, content={"detail": error_details, "message": "입력 데이터 검증 실패"})

    @staticmethod
    async def database_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        log_error(
            exc=exc,
            request=request,
            status_code=503,
            detail="데이터베이스 오류",
            extra={"traceback": traceback.format_exc()}
        )
        return JSONResponse(status_code=503, content={"detail": "데이터베이스 오류", "message": "관리자에게 문의하세요."})

# ==========================
# 5. ExceptionManager 클래스
# ==========================
class ExceptionManager:
    """
    예외 처리 관리자 클래스 - v1.6.x 신규
    """
    @staticmethod
    def register(app: FastAPI):
        """
        FastAPI 애플리케이션에 모든 예외 핸들러를 등록합니다.
        
        Args:
            app: FastAPI 애플리케이션 인스턴스
        """
        # 커스텀 예외 핸들러 등록
        for exc_type in ExceptionHandlerFactory.handlers:
            app.add_exception_handler(exc_type, ExceptionHandlerFactory.generic_handler)
        
        # 검증 오류 핸들러 등록
        app.add_exception_handler(RequestValidationError, ExceptionHandlerFactory.validation_handler)
        
        # 데이터베이스 오류 핸들러 등록
        app.add_exception_handler(SQLAlchemyError, ExceptionHandlerFactory.database_handler)
        
        # 에러 로깅 미들웨어 추가
        app.add_middleware(ErrorLoggingMiddleware)

# ==========================
# 6. 미들웨어
# ==========================
class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Any:
        try:
            return await call_next(request)
        except Exception as exc:
            log_error(
                exc=exc,
                request=request,
                status_code=500,
                detail="Unhandled exception",
                extra={"traceback": traceback.format_exc()}
            )
            raise exc

# 하위 호환성을 위한 별칭
add_exception_handlers = ExceptionManager.register
generic_exception_handler = ExceptionHandlerFactory.generic_handler
```

### 5. AI 모델 컴포넌트 - v1.6.x 모델명 변경

#### LlamaOfficeModel 클래스 (llama_office_model.py) - 이름 변경

`bllossom_model.py`에서 `llama_office_model.py`로 이름이 변경되었습니다.

```python
class LlamaOfficeModel:
    """
    GGUF 포맷으로 경량화된 Llama-3-Korean-Bllossom-8B 모델을 로드하고, 
    주어진 입력 프롬프트에 대한 응답을 생성하는 클래스입니다.
    
    v1.6.x에서 BllossomChatModel에서 LlamaOfficeModel로 이름 변경
    """
    def __init__(self) -> None:
        """
        GGUF 모델 초기화 - RTX 2080 최적화
        """
        self.model_id = "llama-3-Korean-Bllossom-8B-Q4_K_M"
        self.model_path = "fastapi/ai_model/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf"
        self.file_path = './prompt/config-Llama.json'
        self.gpu_layers: int = 70
        
        # 모델 초기화
        self.model: Llama = self._load_model()
        self.response_queue: Queue = Queue()

    def generate_response(self, input_text: str, search_text: str, chat_list: List[Dict]) -> str:
        """
        JSON 응답 생성 메서드 - v1.6.x 최적화
        """
        try:
            current_time = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
            # 응답 생성 로직
            chunks = []
            for chunk in self.create_streaming_completion(
                prompt=prompt,
                max_tokens=2048,
                temperature=0.5,
                top_p=0.80,
                stop=["<|eot_id|>"]
            ):
                chunks.append(chunk)
            
            return "".join(chunks)

        except Exception as e:
            return f"오류: {str(e)}"
```

#### LlamaCharacterModel 클래스 (llama_character_model.py) - 이름 변경

`lumimaid_model.py`에서 `llama_character_model.py`로 이름이 변경되었습니다.

```python
class LlamaCharacterModel:
    """
    GGUF 포맷으로 경량화된 DarkIdol-Llama-3.1-8B 모델을 로드하고, 
    캐릭터 기반 대화 응답을 생성하는 클래스입니다.
    
    v1.6.x에서 LumimaidChatModel에서 LlamaCharacterModel로 이름 변경
    DarkIdol-Llama-3.1-8B 모델로 업그레이드
    """
    def __init__(self) -> None:
        """
        GGUF 모델 초기화 - RTX 3060 최적화
        """
        self.model_id = "DarkIdol-Llama-3.1-8B"
        self.model_path = "fastapi/ai_model/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored.Q8_0.gguf"
        self.file_path = './prompt/config-Llama.json'
        self.gpu_layers: int = 70
        
        # 모델 초기화
        self.model: Llama = self._load_model()
        self.response_queue: Queue = Queue()

    def generate_response(self, input_text: str, character_settings: dict = None) -> str:
        """
        캐릭터 기반 JSON 응답 생성 메서드 - v1.6.x 최적화
        """
        try:
            if character_settings:
                character_info = CharacterPrompt(
                    name=character_settings.get("character_name", "Assistant"),
                    greeting=character_settings.get("greeting", ""),
                    context=character_settings.get("context", ""),
                    user_input=input_text,
                    chat_list=character_settings.get("chat_list", [])
                )
                # Llama3 messages 형식으로 변환
                messages = build_llama3_messages(character_info, input_text, chat_list)
            else:
                messages = [{"role": "user", "content": input_text}]
            
            chunks = []
            for chunk in self.create_streaming_completion(
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=0.95,
                stop=["<|eot_id|>"]
            ):
                chunks.append(chunk)
            
            return "".join(chunks)

        except Exception as e:
            return f"오류: {str(e)}"
```

### 6. 자동화 시스템 - v1.6.x 신규

#### GitHub Actions CI/CD (update-api-docs.yml)

API 명세서 자동 업데이트를 위한 GitHub Actions 워크플로우입니다.

```yaml
name: Update API Documentation

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'fastapi/src/**/*.py'
      - 'fastapi/requirements.txt'
  pull_request:
    branches: [ main ]
    paths:
      - 'fastapi/src/**/*.py'

jobs:
  update-docs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install fastapi uvicorn pydantic
        
    - name: Extract API endpoints
      run: |
        python -c "
        import sys
        import os
        sys.path.append('fastapi/src')
        
        # API 엔드포인트 추출 스크립트
        from fastapi import FastAPI
        from utils.routers import office_controller, character_controller
        
        app = FastAPI()
        app.include_router(office_controller.office_router, prefix='/office')
        app.include_router(character_controller.character_router, prefix='/character')
        
        # OpenAPI 스키마 생성
        openapi_schema = app.openapi()
        
        # Markdown 형식으로 변환
        markdown_content = '''# ChatBot AI - API 명세서
        
## 개요
이 문서는 ChatBot AI API의 자동 생성된 명세서입니다.

## 엔드포인트

'''
        
        for path, methods in openapi_schema['paths'].items():
            markdown_content += f'### {path}\n\n'
            for method, details in methods.items():
                markdown_content += f'#### {method.upper()}\n'
                markdown_content += f'{details.get(\"summary\", \"No summary\")}\n\n'
                
        # 파일 저장
        with open('fastapi/src/docs/api_specification.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        "
        
    - name: Commit and push if changed
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add fastapi/src/docs/api_specification.md
        git diff --staged --quiet || git commit -m "docs: Update API specification [automated]"
        git push
```

#### API 명세서 자동 생성 (api_specification.md)

FastAPI OpenAPI 스키마에서 자동 생성되는 API 문서입니다.

```markdown
# ChatBot AI - API 명세서

## 개요
이 문서는 ChatBot AI API의 자동 생성된 명세서입니다.
GitHub Actions를 통해 코드 변경 시 자동으로 업데이트됩니다.

## 업데이트 정보
- **최종 업데이트**: 2025-06-28 20:34:20
- **API 버전**: v1.6.*
- **FastAPI 버전**: 0.112.0

## 엔드포인트

### Office API (`/office`)

#### POST /office/Llama
**요약**: Llama 모델이 검색 결과를 활용하여 답변 생성

**설명**: LlamaOffice GGUF 모델 기반 검색 연동 응답

**요청 스키마**:
```json
{
  "input_data": "string",
  "google_access": "boolean",
  "db_id": "string",
  "user_id": "string"
}
```

**응답**: JSON 문자열

#### POST /office/{gpt_set}
**요약**: GPT 모델이 검색 결과를 활용하여 답변 생성

**설명**: OpenAI GPT 모델 기반 검색 연동 응답

**경로 매개변수**:
- `gpt_set`: 사용할 GPT 모델 (gpt4o_mini, gpt4.1, gpt4.1_mini)

### Character API (`/character`)

#### POST /character/Llama
**요약**: Llama 모델이 캐릭터 정보를 기반으로 답변 생성

**설명**: LlamaCharacter GGUF 모델 기반 캐릭터 대화

**요청 스키마**:
```json
{
  "input_data": "string",
  "character_name": "string",
  "greeting": "string",
  "context": "string",
  "db_id": "string",
  "user_id": "string"
}
```

#### POST /character/{gpt_set}
**요약**: GPT 모델이 캐릭터 정보를 기반으로 답변 생성

**설명**: OpenAI GPT 모델 기반 캐릭터 대화

## 오류 코드

| 코드 | 설명 | 해결 방법 |
|------|------|-----------|
| 400 | 잘못된 요청 | 요청 형식 확인 |
| 403 | 접근 거부 | IP 화이트리스트 확인 |
| 422 | 유효성 검사 실패 | 입력 데이터 형식 확인 |
| 500 | 서버 내부 오류 | 서버 로그 확인 |

## 사용 예시

### Office API 호출
```bash
curl -X POST "https://your-domain/office/Llama" \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": "ChatBot AI에 대해 설명해주세요",
    "google_access": true,
    "db_id": "12345678-1234-1234-1234-123456789012",
    "user_id": "user123"
  }'
```

### Character API 호출
```bash
curl -X POST "https://your-domain/character/Llama" \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": "안녕하세요!",
    "character_name": "친절한 도우미",
    "greeting": "안녕하세요! 무엇을 도와드릴까요?",
    "context": "친절하고 도움이 되는 AI 어시스턴트",
    "db_id": "12345678-1234-1234-1234-123456789012",
    "user_id": "user123"
  }'
```

---
*이 문서는 GitHub Actions를 통해 자동으로 생성되었습니다.*
```

## 설치 및 설정

### 환경 설정 시스템 - v1.6.x 통합

#### 개선된 가상환경 설정
Windows PowerShell 호환성이 개선된 배치 파일입니다.

```batch
@echo off
chcp 65001
SETLOCAL

:: Python 설치 경로 설정 (공백 없이)
SET PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe

:: 가상 환경 디렉토리 이름 설정 (공백 없이)
SET ENV_DIR=.venv

"%PYTHON_PATH%" -m venv %ENV_DIR%

IF NOT EXIST "%ENV_DIR%\Scripts\activate.ps1" (
    echo 가상 환경 생성에 실패했습니다.
    EXIT /B 1
)

echo 가상 환경 활성화 중...
powershell -NoExit -ExecutionPolicy Bypass -Command "& { .\%ENV_DIR%\Scripts\Activate.ps1 }"

ENDLOCAL
```

#### 통일된 패키지 버전 관리
코드 품질 향상을 위한 패키지 버전 통일화입니다.

```bash
# requirements.txt - v1.6.x 업데이트
torch==2.3.1+cu118
torchvision==0.18.1+cu118
torchaudio==2.3.1+cu118
-f https://download.pytorch.org/whl/torch_stable.html

# OpenAI API
openai

# FastAPI 관련
fastapi==0.112.0
uvicorn==0.30.5

# 유틸리티 패키지 (버전 통일)
python-dotenv==1.0.1
requests==2.32.3
httpx==0.27.0
itsdangerous==2.2.0

# AI 관련
bitsandbytes
accelerate>=0.26.0

# 기타 의존성 패키지 (== 버전 고정)
annotated-types==0.7.0
anyio==4.4.0
click>=8.1.7
colorama==0.4.6
dnspython==2.6.1
h11==0.14.0
idna==3.7
pydantic==2.8.2
pydantic_core==2.20.1
setuptools==65.5.0
sniffio==1.3.1
starlette==0.37.2
typing_extensions==4.12.2

# GGUF 및 검색
ua-parser
motor
llama-cpp-python[cuda]
gguf
duckduckgo-search
langchain-community

# 자연어 처리
spacy
deep-translator>=1.11.4
Pillow
```

### GitHub 통합 설정
CI/CD 파이프라인과 자동 문서화를 위한 설정입니다.

```bash
# GitHub Actions 환경 변수 설정
OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
MONGODB_URI: ${{ secrets.MONGODB_URI }}

# 로컬 개발 환경 설정
git config core.autocrlf true
git config push.default current
```

## 성능 특성

### 메모리 사용량
- **LlamaOffice (GGUF)**: ~8GB VRAM (RTX 2080)
- **LlamaCharacter (GGUF)**: ~6GB VRAM (RTX 3060)
- **OpenAI API**: ~0MB VRAM (외부 API)
- **AppState 관리**: ~64MB RAM
- **로그 시스템**: ~32MB RAM (일별 로테이션)
- **시스템 RAM**: ~8-10GB

### 처리량
- **동시 요청**: 4개 (컨트롤러 분산 처리)
- **시간당 요청**: ~1000-1500개
- **컨트롤러 오버헤드**: 최소 (~2ms)
- **GitHub Actions**: 푸시당 ~30초 (문서 업데이트)

### API 응답 시간
- **Office/Llama**: 8-25초 (Bllossom Q4_K_M)
- **Office/GPT**: 2-5초 (OpenAI API)
- **Character/Llama**: 10-30초 (DarkIdol Q8_0)
- **Character/GPT**: 3-7초 (OpenAI API)

## 운영 가이드

### 환경 설정
1. **GitHub 리포지토리** 설정 (Actions 활성화)
2. **Windows 11** + **Python 3.11** 환경 구성
3. **OpenAI API 키** 발급 및 설정
4. **CUDA 11.8/12.8** 드라이버 설치
5. **로컬 MongoDB** 설치 및 구성
6. **GGUF 모델** 다운로드 및 배치

### 모니터링 포인트
- **컨트롤러별 API** 사용량 및 성능
- **AppState 메모리** 사용률 모니터링
- **로그 시스템** 디스크 사용량
- **GitHub Actions** 빌드 성공률
- **API 명세서** 자동 업데이트 상태

### 문제 해결
- **컨트롤러 라우팅 실패**: 모듈 임포트 경로 확인
- **AppState 메모리 누수**: 모델 해제 로직 확인
- **GitHub Actions 실패**: 권한 및 시크릿 설정 확인
- **API 문서 동기화 실패**: OpenAPI 스키마 검증

### 성능 튜닝
1. **컨트롤러 최적화**
   - 비동기 처리 향상
   - 메모리 풀링 구현
   - 요청 큐 관리

2. **AppState 최적화**
   - 모델 인스턴스 캐싱
   - 메모리 사용량 모니터링
   - GC 튜닝 적용

3. **CI/CD 최적화**
   - 캐싱 전략 구현
   - 병렬 빌드 설정
   - 조건부 실행 최적화

## 보안 고려사항

### 확장된 보안 기능
- **컨트롤러 분리**: 라우터별 독립 보안 정책
- **AppState 보호**: 모델 인스턴스 무단 접근 방지
- **GitHub Secrets**: API 키 및 민감 정보 보호
- **로그 보안**: 개인정보 로깅 방지

### API 보안 강화
- **컨트롤러 접근 제어**: 경로별 인증 및 검증
- **예외 처리 통합**: 보안 취약점 최소화
- **자동 문서화**: 민감 정보 노출 방지
