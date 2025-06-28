# ChatBot AI - 버전 명세서 v1.5.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.5.x 계열 버전에 대한 공식 명세서입니다. v1.4.x의 HTTPS 보안 시스템에서 **OpenAI API 통합**과 **라우터 기반 아키텍처**로 대폭 확장되었으며, **프로토타입 분리**, **공유 설정 시스템**, **UML 다이어그램 도입**을 통한 엔터프라이즈급 AI 챗봇 서비스입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.5.0** | 2025-03-21 | `e924df6e591ae81cb6718a18eb1ded24c76bc659` | Stable |
| **v1.5.1** | 2025-04-16 | `682362de5a91d68fe1cd37db38a1184cf958476b` | Stable |
| **v1.5.2** | 2025-04-16 | `3e0b9525e44f097d91485b718e10ce6073917168` | Latest |
| **None** | 2025-05-03 | `11adcd7ee4022e5b3f5b595ff132e02a869c145b` | Unstable |

## v1.4.x에서 v1.5.x로의 주요 변경사항

### 아키텍처 대혁신
- **단일 엔드포인트** → **라우터 기반 RESTful API** (`/office`, `/character`)
- **GGUF 전용** → **GGUF + OpenAI API 하이브리드** 시스템
- **모노리식 구조** → **모듈화된 마이크로서비스** 아키텍처

### AI 모델 확장
- **2개 GGUF 모델** → **5개 AI 모델** 지원
- **OpenAI GPT 통합**: GPT-4o-mini, GPT-4.1, GPT-4.1-mini
- **공유 설정 시스템**: 통합된 프롬프트 및 생성 파라미터 관리

### 개발 환경 개선
- **테스트 폴더** → **프로토타입 디렉토리** 분리
- **배치 파일** 경로 정리 (`batchfile` → `batch`)
- **설정 파일** 경로 통합 (`models` → `prompt`)
- **UML 다이어그램** 도입 (클래스/패키지 다이어그램)

### 신규 기능
- **임베딩 기반 채팅 메모리** 프로토타입
- **SonarQube** 정적 코드 분석 지원
- **공유 설정 클래스** (TypedDict, dataclass 활용)
- **HTTP → HTTPS** 개발 환경 전환

### 제거된 기능
- ❌ **Transformers 기반 Llama 모델** 완전 제거
- ❌ **index.html** 웹 인터페이스 제거
- ❌ **SSE 스트리밍** 엔드포인트 비활성화
- ❌ **Hypercorn 서버** (uvicorn 복귀)

## 시스템 요구사항

### 하드웨어 요구사항
- **GPU**: NVIDIA RTX 3060 (CUDA:0) + RTX 2080 (CUDA:1)
- **VRAM**: 최소 20GB RAM (3060 12GB + 2080 8GB)
- **저장공간**: 최소 50GB 여유 공간
- **네트워크**: 공인 IP 주소 + OpenAI API 접속

### 소프트웨어 요구사항
- **운영체제**: Windows 10/11 (64-bit)
- **Python**: 3.11 이상
- **CUDA**: 11.8/12.8 지원
- **llama-cpp-python**: CUDA 지원 버전
- **MongoDB**: 로컬 설치
- **OpenAI API**: 유효한 API 키

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot AI v1.5.x
├── 📁 fastapi/
│   ├── 📁 ai_model/              # GGUF 모델 저장소
│   │   ├── llama-3-Korean-Bllossom-8B-Q4_K_M.gguf
│   │   ├── v2-Llama-3-Lumimaid-8B-v0.1-OAS-Q5_K_S-imat.gguf
│   │   └── README.md [UPDATED]
│   ├── 📁 batch/                 # 환경 설정 배치 파일 [RENAMED]
│   │   ├── venv_install.bat [MOVED]
│   │   └── venv_setup.bat [MOVED]
│   ├── 📁 certificates/         # SSL 인증서 관리
│   │   ├── DNS_README.md
│   │   ├── PEM_README.md [UPDATED]
│   │   └── *.pem [IGNORED]
│   ├── 📁 src/
│   │   ├── 📁 prototypes/        # 실험/프로토타입 코드 [NEW]
│   │   │   ├── 📁 train/         # 파인튜닝 관련 [MOVED]
│   │   │   │   ├── train.py [MOVED]
│   │   │   │   └── train_README.md [MOVED]
│   │   │   ├── embedding_chat_memory.py [NEW]
│   │   │   ├── shared.py [NEW]
│   │   │   ├── DuckDuckGo.py [MOVED]
│   │   │   ├── GGUF_CPU.py [MOVED]
│   │   │   ├── GGUF_GPU.py [MOVED]
│   │   │   ├── Llama_cpp_test.py [MOVED]
│   │   │   ├── V2_prompt.py [MOVED]
│   │   │   ├── bot.py [MOVED]
│   │   │   ├── cuda_gpu.py [MOVED]
│   │   │   ├── httpx_test.py [MOVED]
│   │   │   └── load_dataset.py [MOVED]
│   │   ├── 📁 utils/             # 모듈화된 유틸리티
│   │   │   ├── 📁 ai_models/     # AI 모델 모듈
│   │   │   │   ├── 📁 shared/    # 공유 설정 [NEW]
│   │   │   │   │   └── shared_configs.py [NEW]
│   │   │   │   ├── bllossom_model.py [UPDATED]
│   │   │   │   ├── lumimaid_model.py [UPDATED]
│   │   │   │   ├── openai_character_model.py [NEW]
│   │   │   │   └── openai_office_model.py [NEW]
│   │   │   ├── 📁 handlers/      # 핸들러 모듈
│   │   │   │   ├── error_handler.py [UPDATED]
│   │   │   │   ├── language_handler.py [UPDATED]
│   │   │   │   └── mongodb_handler.py [UPDATED]
│   │   │   ├── 📁 schemas/       # 스키마 모듈
│   │   │   │   └── chat_schema.py [UPDATED]
│   │   │   ├── 📁 services/      # 서비스 모듈
│   │   │   │   └── search_service.py [UPDATED]
│   │   │   └── __init__.py [UPDATED]
│   │   ├── server.py [COMPLETELY REDESIGNED]
│   │   ├── bot.yaml
│   │   └── .env
│   └── requirements.txt [UPDATED]
├── 📁 prompt/                    # 프롬프트 및 설정 파일 [RENAMED]
│   ├── config-Llama.json [NEW]
│   ├── config-OpenAI.json [RENAMED]
│   └── config-user.yaml [MOVED]
└── .gitignore [UPDATED]
```

## API 명세

### 라우터 기반 API 아키텍처

#### Office Router (`/office`)
업무 및 일반적인 질의응답을 처리하는 라우터입니다.

##### POST /office/Llama
Bllossom GGUF 모델 기반 검색 연동 JSON 응답

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

**요청 형식:**
```json
{
  "input_data": "Llama AI 모델의 출시일과 버전들을 각각 알려줘.",
  "google_access": true,
  "db_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user123"
}
```

#### Character Router (`/character`)
캐릭터 기반 대화를 처리하는 라우터입니다.

##### POST /character/Llama
Lumimaid GGUF 모델 기반 캐릭터 대화 JSON 응답

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

### 1. 서버 컴포넌트 (server.py) - v1.5.x 완전 재설계

#### 라우터 기반 아키텍처
v1.4.x의 단일 엔드포인트에서 **RESTful 라우터 시스템**으로 대폭 전환되었습니다.

```python
# OpenAI 모델 매핑 시스템
OPENAI_MODEL_MAP = {
    "gpt4o_mini": "gpt-4o-mini",
    "gpt4.1": "gpt-4.1",
    "gpt4.1_mini": "gpt-4.1-mini",
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI AI 모델 애플리케이션 초기화 - v1.5.x
    GGUF + OpenAI API 하이브리드 시스템
    """
    global Bllossom_model, Lumimaid_model, GREEN, RESET

    try:
        # GGUF 모델 로드
        Bllossom_model = Bllossom()                 # cuda:1 (RTX 2080)
        Lumimaid_model = Lumimaid()                 # cuda:0 (RTX 3060)
    except ChatError.InternalServerErrorException as e:
        component = "MongoDBHandler"
        print(f"{RED}ERROR{RESET}: {component} 초기화 중 {e.__class__.__name__} 오류 발생: {str(e)}")
        exit(1)

    # 디버깅용 출력
    print(f"{GREEN}INFO{RESET}: Bllossom 모델 로드 완료 ({Bllossom_device_info})")
    print(f"{GREEN}INFO{RESET}: Lumimaid 모델 로드 완료 ({Lumimaid_device_info})")
    print(f"{GREEN}INFO{RESET}: OpenAiOffice 모델 로드 완료 (API 호출)")
    print(f"{GREEN}INFO{RESET}: OpenAiCharacter 모델 로드 완료 (API 호출)")

    yield

    Bllossom_model = None
    Lumimaid_model = None
    print(f"{GREEN}INFO{RESET}: 모델 해제 완료")
```

#### Office 라우터 구현
업무용 AI 응답을 처리하는 전용 라우터입니다.

```python
office_router = APIRouter()

@office_router.post("/Llama", summary="Llama 모델이 검색 결과를 활용하여 답변 생성")
async def office_llama(request: ChatModel.office_Request):
    """
    Bllossom GGUF 모델 기반 검색 연동 응답
    """
    chat_list = []
    search_context = ""
    
    # MongoDB에서 채팅 기록 가져오기
    if mongo_handler or request.db_id:
        try:
            chat_list = await mongo_handler.get_office_log(
                user_id=request.user_id,
                document_id=request.db_id,
                router="office",
            )
        except Exception as e:
            print(f"{YELLOW}WARNING{RESET}: 채팅 기록을 가져오는 데 실패했습니다: {str(e)}")

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
            print(f"{YELLOW}WARNING{RESET}: 검색의 한도 초과로 DuckDuckGo 검색 결과를 가져올 수 없습니다.")

    try:        
        full_response = Bllossom_model.generate_response(
            input_text=request.input_data,
            search_text=search_context,
            chat_list=chat_list,
        )
        return full_response
    except TimeoutError:
        raise ChatError.InternalServerErrorException(detail="Bllossom 모델 응답이 시간 초과되었습니다.")
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")

@office_router.post("/{gpt_set}", summary="gpt 모델이 검색 결과를 활용하여 답변 생성")
async def office_gpt(
        request: ChatModel.office_Request,
        gpt_set: str = Path(
            ...,
            title="GPT 모델명",
            description="사용할 OpenAI GPT 모델의 별칭 (예: gpt4o_mini, gpt4.1, gpt4.1_mini)",
            examples=list(OPENAI_MODEL_MAP.keys()),
        )
    ):
    """
    OpenAI GPT 모델 기반 검색 연동 응답
    """
    if gpt_set not in OPENAI_MODEL_MAP:
        raise HTTPException(status_code=400, detail="Invalid model name.")

    model_id = OPENAI_MODEL_MAP[gpt_set]
    # ... (검색 로직 동일)

    OpenAiOffice_model = OpenAiOffice(model_id=model_id)
    try:
        full_response = OpenAiOffice_model.generate_response(
            input_text=request.input_data,
            search_text=search_context,
            chat_list=chat_list,
        )
        return full_response
    except TimeoutError:
        raise ChatError.InternalServerErrorException(detail="OpenAI 모델 응답이 시간 초과되었습니다.")
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")

app.include_router(
    office_router,
    prefix="/office",
    tags=["office Router"],
    responses={500: {"description": "Internal Server Error"}}
)
```

#### Character 라우터 구현
캐릭터 기반 대화를 처리하는 전용 라우터입니다.

```python
character_router = APIRouter()

@character_router.post("/Llama", summary="Llama 모델이 케릭터 정보를 기반으로 답변 생성")
async def character_llama(request: ChatModel.character_Request):
    """
    Lumimaid GGUF 모델 기반 캐릭터 대화
    """
    chat_list = []
    
    # MongoDB에서 채팅 기록 가져오기
    if mongo_handler or request.db_id:
        try:
            chat_list = await mongo_handler.get_character_log(
                user_id=request.user_id,
                document_id=request.db_id,
                router="character",
            )
        except Exception as e:
            print(f"{YELLOW}WARNING{RESET}: 채팅 기록을 가져오는 데 실패했습니다: {str(e)}")
            
    try:
        character_settings = {
            "character_name": request.character_name,
            "greeting": request.greeting,
            "context": request.context,
            "chat_list": chat_list,
        }
        full_response = Lumimaid_model.generate_response(
            input_text=request.input_data,
            character_settings=character_settings,
        )
        return full_response
    except TimeoutError:
        raise ChatError.InternalServerErrorException(detail="Lumimaid 모델 응답이 시간 초과되었습니다.")
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")

@character_router.post("/{gpt_set}", summary="gpt 모델이 케릭터 정보를 기반으로 답변 생성")
async def character_gpt(
        request: ChatModel.character_Request,
        gpt_set: str = Path(
            ...,
            title="GPT 모델명",
            description="사용할 OpenAI GPT 모델의 별칭 (예: gpt4o_mini, gpt4.1, gpt4.1_mini)",
            examples=list(OPENAI_MODEL_MAP.keys()),
        )
    ):
    """
    OpenAI GPT 모델 기반 캐릭터 대화
    """
    if gpt_set not in OPENAI_MODEL_MAP:
        raise HTTPException(status_code=400, detail="Invalid model name.")

    model_id = OPENAI_MODEL_MAP[gpt_set]
    # ... (채팅 기록 로직 동일)

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
    except TimeoutError:
        raise ChatError.InternalServerErrorException(detail="Lumimaid 모델 응답이 시간 초과되었습니다.")
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")

app.include_router(
    character_router,
    prefix="/character",
    tags=["character Router"],
    responses={500: {"description": "Internal Server Error"}}
)
```

#### 개발 환경 복귀
HTTPS에서 HTTP 개발 환경으로 복귀했습니다.

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 2. AI 모델 컴포넌트 - v1.5.x 공유 설정 시스템

#### 공유 설정 클래스 (shared/shared_configs.py) - 신규 추가

TypedDict와 dataclass를 활용한 통합 설정 관리 시스템입니다.

```python
from typing import TypedDict, Optional, List, Dict
from dataclasses import dataclass

class BaseConfig(TypedDict):
    """
    기본 모델 설정을 위한 TypedDict
    """
    character_name: str
    character_setting: str
    greeting: str

@dataclass
class OfficePrompt:
    """
    Office 라우터용 프롬프트 데이터 클래스
    """
    name: str
    context: str
    reference_data: str
    user_input: str
    chat_list: List[Dict]

@dataclass
class CharacterPrompt:
    """
    Character 라우터용 프롬프트 데이터 클래스
    """
    name: str
    greeting: str
    context: str
    user_input: str
    chat_list: List[Dict]

@dataclass
class LlamaGenerationConfig:
    """
    Llama 모델 생성 파라미터 설정
    """
    prompt: str
    max_tokens: int = 2048
    temperature: float = 0.5
    top_p: float = 0.80
    stop: Optional[List[str]] = None
```

#### BllossomChatModel 클래스 (bllossom_model.py) - v1.5.x 리팩토링

공유 설정 시스템을 활용한 모듈화된 구조로 개선되었습니다.

```python
from .shared.shared_configs import OfficePrompt, LlamaGenerationConfig, BaseConfig

class BllossomChatModel:
    def __init__(self) -> None:
        self.model_id = "llama-3-Korean-Bllossom-8B-Q4_K_M"
        self.model_path = "fastapi/ai_model/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf"
        self.file_path = './prompt/config-Llama.json'
        self.loading_text = f"{BLUE}LOADING{RESET}: {self.model_id} 로드 중..."
        self.gpu_layers: int = 70
        self.character_info: Optional[OfficePrompt] = None
        self.config: Optional[LlamaGenerationConfig] = None

        print("\n" + f"{BLUE}LOADING{RESET}: " + "="*len(self.loading_text))
        print(f"{BLUE}LOADING{RESET}: {__class__.__name__} 모델 초기화 시작...")

        # JSON 파일 읽기
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.data: BaseConfig = json.load(file)

        # 진행 상태 표시
        print(f"{BLUE}LOADING{RESET}: {__class__.__name__} 모델 초기화 중...")
        self.model: Llama = self._load_model()
        print(f"{BLUE}LOADING{RESET}: 모델 로드 완료!")
        print(f"{BLUE}LOADING{RESET}: " + "="*len(self.loading_text) + "\n")
        
        self.response_queue: Queue = Queue()

    def generate_response(self, input_text: str, search_text: str, chat_list: List[Dict]) -> str:
        """
        JSON 응답 생성 메서드 (스트리밍에서 변경)
        """
        try:
            current_time = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
            time_info = f"현재 시간은 {current_time}입니다.\n\n"
            reference_text = time_info + (search_text if search_text else "")

            normalized_chat_list = []
            for chat in chat_list:
                normalized_chat_list.append({
                    "input_data": self._normalize_escape_chars(chat.get("input_data", "")),
                    "output_data": self._normalize_escape_chars(chat.get("output_data", ""))
                })

            self.character_info: OfficePrompt = OfficePrompt(
                name=self.data.get("character_name"),
                context=self.data.get("character_setting"),
                reference_data=reference_text,
                user_input=input_text,
                chat_list=normalized_chat_list,
            )

            messages = build_llama3_messages(character_info=self.character_info)

            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            self.config = LlamaGenerationConfig(
                prompt=prompt,
                max_tokens=2048,
                temperature=0.5,
                top_p=0.80,
                stop=["<|eot_id|>"]
            )

            chunks = []
            for text_chunk in self.create_streaming_completion(config=self.config):
                chunks.append(text_chunk)
            return "".join(chunks)

        except Exception as e:
            return f"오류: {str(e)}"
```

#### LumimaidChatModel 클래스 (lumimaid_model.py) - v1.5.x 업데이트

공유 설정 시스템을 통합한 캐릭터 대화 모델입니다.

```python
from .shared.shared_configs import CharacterPrompt, LlamaGenerationConfig, BaseConfig

class LumimaidChatModel:
    def __init__(self) -> None:
        self.model_id = "Llama-3-Lumimaid-8B-v0.1-OAS"
        self.model_path = "fastapi/ai_model/v2-Llama-3-Lumimaid-8B-v0.1-OAS-Q5_K_S-imat.gguf"
        self.file_path = './prompt/config-Llama.json'
        self.loading_text = f"{BLUE}LOADING{RESET}: {self.model_id} 로드 중..."
        self.gpu_layers: int = 70
        self.character_info: Optional[CharacterPrompt] = None
        self.config: Optional[LlamaGenerationConfig] = None

        # JSON 파일 읽기
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.data: BaseConfig = json.load(file)

        # 모델 초기화
        self.model: Llama = self._load_model()
        self.response_queue: Queue = Queue()

    def generate_response(self, input_text: str, character_settings: dict = None) -> str:
        """
        캐릭터 기반 JSON 응답 생성 메서드
        """
        try:
            if character_settings:
                self.character_info = CharacterPrompt(
                    name=character_settings.get("character_name", "Assistant"),
                    greeting=character_settings.get("greeting", ""),
                    context=character_settings.get("context", ""),
                    user_input=input_text,
                    chat_list=character_settings.get("chat_list", [])
                )
                prompt = build_llama3_prompt(character_info=self.character_info)
            else:
                prompt = input_text

            self.config = LlamaGenerationConfig(
                prompt=prompt,
                max_tokens=2048,
                temperature=0.8,
                top_p=0.95,
                stop=["<|eot_id|>"]
            )

            chunks = []
            for text_chunk in self.create_streaming_completion(config=self.config):
                chunks.append(text_chunk)
            return "".join(chunks)

        except Exception as e:
            return f"오류: {str(e)}"
```

#### OpenAI 모델 클래스 - v1.5.x 신규 추가

##### OpenAIChatModel 클래스 (openai_office_model.py)
Office 라우터용 OpenAI API 통합 모델입니다.

```python
import openai
from typing import List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime

class OpenAIChatModel:
    """
    OpenAI API를 사용하는 Office용 채팅 모델
    """
    def __init__(self, model_id: str = "gpt-4o-mini"):
        load_dotenv()
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model_id = model_id

    def generate_response(self, input_text: str, search_text: str = "", chat_list: List[Dict] = None) -> str:
        """
        OpenAI API를 사용하여 응답 생성
        
        Args:
            input_text (str): 사용자 입력
            search_text (str): 검색 결과 컨텍스트
            chat_list (List[Dict]): 대화 기록
            
        Returns:
            str: 생성된 응답
        """
        try:
            # 현재 시간 정보 추가
            current_time = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
            time_info = f"현재 시간은 {current_time}입니다.\n\n"
            
            # 시스템 프롬프트 구성
            system_content = (
                "당신은 도움이 되는 AI 어시스턴트입니다. "
                "정확하고 유용한 정보를 제공해주세요.\n\n"
                f"{time_info}"
            )
            
            if search_text:
                system_content += f"참고 정보:\n{search_text}\n\n"
            
            # 메시지 구성
            messages = [{"role": "system", "content": system_content}]
            
            # 대화 기록 추가
            if chat_list:
                for chat in chat_list[-5:]:  # 최근 5개만
                    if chat.get("input_data"):
                        messages.append({"role": "user", "content": chat["input_data"]})
                    if chat.get("output_data"):
                        messages.append({"role": "assistant", "content": chat["output_data"]})
            
            # 현재 질문 추가
            messages.append({"role": "user", "content": input_text})
            
            # OpenAI API 호출
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=0.9
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"OpenAI API 오류: {str(e)}"
```

##### OpenAICharacterModel 클래스 (openai_character_model.py)
Character 라우터용 OpenAI API 통합 모델입니다.

```python
class OpenAICharacterModel:
    """
    OpenAI API를 사용하는 캐릭터 대화 모델
    """
    def __init__(self, model_id: str = "gpt-4o-mini"):
        load_dotenv()
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model_id = model_id

    def generate_response(self, input_text: str, character_settings: dict = None) -> str:
        """
        캐릭터 기반 OpenAI API 응답 생성
        
        Args:
            input_text (str): 사용자 입력
            character_settings (dict): 캐릭터 설정
            
        Returns:
            str: 생성된 응답
        """
        try:
            if character_settings:
                # 캐릭터 시스템 프롬프트 구성
                system_content = (
                    f"당신은 {character_settings.get('character_name', 'Assistant')}라는 캐릭터입니다.\n"
                    f"인사말: {character_settings.get('greeting', '')}\n"
                    f"캐릭터 설명: {character_settings.get('context', '')}\n\n"
                    "위의 캐릭터 설정에 맞게 일관된 성격과 말투로 대화해주세요. "
                    "감정 표현과 행동 묘사를 포함하여 생동감 있는 대화를 만들어주세요."
                )
            else:
                system_content = "당신은 도움이 되는 AI 어시스턴트입니다."
            
            # 메시지 구성
            messages = [{"role": "system", "content": system_content}]
            
            # 대화 기록 추가
            if character_settings and character_settings.get("chat_list"):
                for chat in character_settings["chat_list"][-5:]:  # 최근 5개만
                    if chat.get("input_data"):
                        messages.append({"role": "user", "content": chat["input_data"]})
                    if chat.get("output_data"):
                        messages.append({"role": "assistant", "content": chat["output_data"]})
            
            # 현재 질문 추가
            messages.append({"role": "user", "content": input_text})
            
            # OpenAI API 호출
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                max_tokens=2048,
                temperature=0.8,
                top_p=0.95
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"OpenAI API 오류: {str(e)}"
```

### 3. 프로토타입 시스템 - v1.5.x 신규 분리

#### 임베딩 기반 채팅 메모리 (embedding_chat_memory.py)
벡터 임베딩을 활용한 대화 기록 검색 프로토타입입니다.

```python
"""
임베딩 기반 채팅 메모리 프로토타입
벡터 임베딩을 사용하여 유사한 대화 기록을 검색하고 관련성 높은 응답을 생성합니다.
"""
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import json
import os

class EmbeddingChatMemory:
    """
    임베딩 기반 채팅 메모리 관리 클래스
    """
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        임베딩 모델 초기화
        
        Args:
            model_name (str): 사용할 sentence-transformers 모델명
        """
        self.embedding_model = SentenceTransformer(model_name)
        self.chat_embeddings: List[np.ndarray] = []
        self.chat_texts: List[str] = []
        self.chat_metadata: List[Dict] = []

    def add_chat(self, user_input: str, bot_response: str, metadata: Dict = None):
        """
        대화를 메모리에 추가하고 임베딩 생성
        
        Args:
            user_input (str): 사용자 입력
            bot_response (str): 봇 응답
            metadata (Dict): 추가 메타데이터
        """
        chat_text = f"User: {user_input}\nBot: {bot_response}"
        embedding = self.embedding_model.encode(chat_text)
        
        self.chat_embeddings.append(embedding)
        self.chat_texts.append(chat_text)
        self.chat_metadata.append(metadata or {})

    def search_similar_chats(self, query: str, top_k: int = 5) -> List[Tuple[str, float, Dict]]:
        """
        쿼리와 유사한 대화 기록 검색
        
        Args:
            query (str): 검색 쿼리
            top_k (int): 반환할 상위 k개 결과
            
        Returns:
            List[Tuple[str, float, Dict]]: (대화텍스트, 유사도점수, 메타데이터) 리스트
        """
        if not self.chat_embeddings:
            return []
        
        query_embedding = self.embedding_model.encode(query)
        similarities = []
        
        for i, chat_embedding in enumerate(self.chat_embeddings):
            similarity = np.dot(query_embedding, chat_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(chat_embedding)
            )
            similarities.append((self.chat_texts[i], similarity, self.chat_metadata[i]))
        
        # 유사도 기준 정렬
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def get_context_for_response(self, query: str, threshold: float = 0.3) -> str:
        """
        응답 생성을 위한 컨텍스트 제공
        
        Args:
            query (str): 사용자 쿼리
            threshold (float): 유사도 임계값
            
        Returns:
            str: 관련 대화 기록을 포함한 컨텍스트
        """
        similar_chats = self.search_similar_chats(query, top_k=3)
        relevant_chats = [chat for chat in similar_chats if chat[1] >= threshold]
        
        if not relevant_chats:
            return ""
        
        context = "관련 대화 기록:\n"
        for chat_text, similarity, metadata in relevant_chats:
            context += f"(유사도: {similarity:.2f}) {chat_text}\n\n"
        
        return context

    def save_memory(self, filepath: str):
        """메모리를 파일로 저장"""
        memory_data = {
            "chat_texts": self.chat_texts,
            "chat_embeddings": [emb.tolist() for emb in self.chat_embeddings],
            "chat_metadata": self.chat_metadata
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=2)

    def load_memory(self, filepath: str):
        """파일에서 메모리 로드"""
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            self.chat_texts = memory_data["chat_texts"]
            self.chat_embeddings = [np.array(emb) for emb in memory_data["chat_embeddings"]]
            self.chat_metadata = memory_data["chat_metadata"]
```

#### 공유 프로토타입 설정 (shared.py)
프로토타입 간 공유되는 설정 및 유틸리티입니다.

```python
"""
프로토타입 공유 설정 및 유틸리티
"""
import os
from typing import Dict, Any

# 공통 설정
PROTOTYPE_CONFIG = {
    "model_paths": {
        "bllossom": "fastapi/ai_model/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf",
        "lumimaid": "fastapi/ai_model/v2-Llama-3-Lumimaid-8B-v0.1-OAS-Q5_K_S-imat.gguf"
    },
    "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "memory_save_path": "./prototypes/memory/",
    "log_level": "INFO",
    "cuda_devices": {
        "bllossom": 1,  # RTX 2080
        "lumimaid": 0   # RTX 3060
    }
}

def get_prototype_config() -> Dict[str, Any]:
    """프로토타입 설정 반환"""
    return PROTOTYPE_CONFIG.copy()

def ensure_memory_directory():
    """메모리 저장 디렉토리 생성"""
    memory_path = PROTOTYPE_CONFIG["memory_save_path"]
    os.makedirs(memory_path, exist_ok=True)
    return memory_path

class PrototypeLogger:
    """프로토타입용 간단한 로거"""
    def __init__(self, name: str):
        self.name = name
    
    def info(self, message: str):
        print(f"[{self.name}] INFO: {message}")
    
    def warning(self, message: str):
        print(f"[{self.name}] WARNING: {message}")
    
    def error(self, message: str):
        print(f"[{self.name}] ERROR: {message}")
```

### 4. 데이터 모델 컴포넌트 (chat_schema.py) - v1.5.x 라우터 기반 재설계

#### 라우터별 요청/응답 모델
기존의 단일 모델에서 라우터별 전용 모델로 분리되었습니다.

```python
class office_Request(BaseModel):
    """
    Office 라우터 API 요청 - v1.5.x 신규
    업무용 AI 응답을 위한 요청 모델
    """
    input_data: str = office_input_data_set
    google_access: bool = google_access_set
    db_id: str | None = db_id_set
    user_id: str | None = user_id_set

class character_Request(BaseModel):
    """
    Character 라우터 API 요청 - v1.5.x 신규
    캐릭터 기반 대화를 위한 요청 모델
    """
    input_data: str = character_input_data_set
    character_name: str = character_name_set
    greeting: str = greeting_set
    context: str = context_set
    db_id: str | None = db_id_set
    user_id: str | None = user_id_set

# v1.4.x 호환성을 위한 별칭 유지
Bllossom_Request = office_Request
Lumimaid_Request = character_Request
```

## UML 다이어그램 시스템

### 클래스 다이어그램
v1.5.x에서 도입된 UML 클래스 다이어그램으로 시스템 구조를 시각화합니다.

#### AI Models 클래스 다이어그램
```
┌─────────────────────────────────────────────────────────────┐
│                     AI Models Package                       │
├─────────────────────────────────────────────────────────────┤
│ BaseConfig (TypedDict)                                      │
│ + character_name: str                                       │
│ + character_setting: str                                    │
│ + greeting: str                                             │
├─────────────────────────────────────────────────────────────┤
│ BllossomChatModel                                           │
│ + model_path: str                                           │
│ + character_info: OfficePrompt                              │
│ + config: LlamaGenerationConfig                             │
│ + generate_response(): str                                  │
├─────────────────────────────────────────────────────────────┤
│ LumimaidChatModel                                           │
│ + model_path: str                                           │
│ + character_info: CharacterPrompt                           │
│ + config: LlamaGenerationConfig                             │
│ + generate_response(): str                                  │
├─────────────────────────────────────────────────────────────┤
│ OpenAIChatModel                                             │
│ + client: openai.OpenAI                                     │
│ + model_id: str                                             │
│ + generate_response(): str                                  │
├─────────────────────────────────────────────────────────────┤
│ OpenAICharacterModel                                        │
│ + client: openai.OpenAI                                     │
│ + model_id: str                                             │
│ + generate_response(): str                                  │
└─────────────────────────────────────────────────────────────┘
```

#### Handlers 클래스 다이어그램
```
┌─────────────────────────────────────────────────────────────┐
│                    Handlers Package                         │
├─────────────────────────────────────────────────────────────┤
│ MongoDBHandler                                              │
│ + client: AsyncIOMotorClient                                │
│ + db: AsyncIOMotorDatabase                                  │
│ + get_office_log(): List[Dict]                              │
│ + get_character_log(): List[Dict]                           │
├─────────────────────────────────────────────────────────────┤
│ LanguageProcessor                                           │
│ + translate(): str                                          │
│ + detect_language(): str                                    │
├─────────────────────────────────────────────────────────────┤
│ ChatError                                                   │
│ + add_exception_handlers(): None                            │
│ + generic_exception_handler(): JSONResponse                 │
└─────────────────────────────────────────────────────────────┘
```

#### Schemas 클래스 다이어그램
```
┌─────────────────────────────────────────────────────────────┐
│                     Schemas Package                         │
├─────────────────────────────────────────────────────────────┤
│ office_Request (BaseModel)                                  │
│ + input_data: str                                           │
│ + google_access: bool                                       │
│ + db_id: str | None                                         │
│ + user_id: str | None                                       │
├─────────────────────────────────────────────────────────────┤
│ character_Request (BaseModel)                               │
│ + input_data: str                                           │
│ + character_name: str                                       │
│ + greeting: str                                             │
│ + context: str                                              │
│ + db_id: str | None                                         │
│ + user_id: str | None                                       │
└─────────────────────────────────────────────────────────────┘
```

### 패키지 다이어그램
```
┌─────────────────────────────────────────────────────────────┐
│                      ChatBot AI v1.5.x                      │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐ │
│ │   FastAPI       │  │   Prototypes    │  │    Prompt     │ │
│ │   Server        │  │   Research      │  │    Config     │ │
│ │                 │  │                 │  │               │ │ 
│ │ • server.py     │  │ • embedding_    │  │ • config-     │ │
│ │ • routers       │  │   chat_memory   │  │   Llama.json  │ │
│ │ • middlewares   │  │ • shared.py     │  │ • config-     │ │
│ │                 │  │ • train/        │  │   OpenAI.json │ │
│ └─────────────────┘  └─────────────────┘  └───────────────┘ │
│          │                     │                   │        │
│          ▼                     ▼                   ▼        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                     Utils Package                       │ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │ │
│ │ │ AI Models   │ │  Handlers   │ │     Services        │ │ │
│ │ │             │ │             │ │                     │ │ │
│ │ │ • GGUF      │ │ • MongoDB   │ │ • DuckDuckGo        │ │ │
│ │ │ • OpenAI    │ │ • Error     │ │   Search            │ │ │
│ │ │ • Shared    │ │ • Language  │ │                     │ │ │
│ │ └─────────────┘ └─────────────┘ └─────────────────────┘ │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │                   Schemas                           │ │ │
│ │ │ • office_Request  • character_Request               │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 설치 및 설정

### 환경 설정 시스템 - v1.5.x 통합

#### 개선된 환경 구성
OpenAI API 키와 함께 CUDA 환경을 지원하는 통합 설치 가이드입니다.

**환경 변수 설정:**
```bash
# .env 파일 추가 변수
OPENAI_API_KEY=your_openai_api_key_here
LOCAL_HOST=192.168.3.0/24

# 기존 변수 유지
SESSION_KEY=default-secret
MONGO_HOST=localhost
MONGO_PORT=27017
# ... (기타 MongoDB 설정)
```

**필수 패키지:**
```bash
# 기본 패키지 (v1.5.x 업데이트)
pip install torch==2.3.1+cu118 torchvision==0.18.1+cu118 torchaudio==2.3.1+cu118

# OpenAI API
pip install openai

# GGUF 지원
pip install llama-cpp-python[cuda]

# 검색 및 번역
pip install duckduckgo-search langchain-community deep-translator

# 임베딩 및 벡터 검색
pip install sentence-transformers

# 자연어 처리
pip install spacy
```

#### 배치 파일 경로 정리
배치 파일이 `batchfile` → `batch`로 이동되었습니다.

```bash
# 가상환경 생성
./fastapi/batch/venv_setup.bat

# 패키지 설치
./fastapi/batch/venv_install.bat

# 서버 실행
./.venv/Scripts/python.exe ./fastapi/src/server.py
```

### 프로토타입 개발 환경
연구 및 실험을 위한 프로토타입 실행 환경입니다.

```bash
# 임베딩 채팅 메모리 테스트
cd fastapi/src/prototypes
python embedding_chat_memory.py

# GGUF 모델 테스트
python GGUF_GPU.py

# 파인튜닝 실행
cd train
python train.py
```

## 성능 특성

### 메모리 사용량
- **Bllossom (GGUF)**: ~8GB VRAM (RTX 2080)
- **Lumimaid (GGUF)**: ~6GB VRAM (RTX 3060)
- **OpenAI API**: ~0MB VRAM (외부 API)
- **임베딩 모델**: ~500MB RAM
- **MongoDB**: ~512MB RAM
- **시스템 RAM**: ~8-10GB

### 처리량
- **동시 요청**: 5개 (GGUF 2개 + OpenAI 3개)
- **시간당 요청**: ~800-1200개
- **OpenAI API**: 실시간 응답 (~2-5초)
- **GGUF 성능**: v1.4.x 대비 일관된 성능
- **라우터 오버헤드**: 최소 (~5ms)

### API 응답 시간
- **Office/Llama**: 10-30초 (GGUF 로컬)
- **Office/GPT**: 2-5초 (OpenAI API)
- **Character/Llama**: 15-40초 (GGUF 로컬)
- **Character/GPT**: 3-7초 (OpenAI API)

## 운영 가이드

### 환경 설정
1. **Windows 11** + **Python 3.11** 환경 구성
2. **OpenAI API 키** 발급 및 설정
3. **CUDA 11.8/12.8** 드라이버 설치
4. **로컬 MongoDB** 설치 및 구성
5. **GGUF 모델** 다운로드 및 배치

### 모니터링 포인트
- **라우터별 API** 사용량 및 성능
- **OpenAI API** 호출 횟수 및 비용
- **GGUF 모델** 메모리 사용률
- **MongoDB** 대화 기록 저장 성능
- **임베딩 메모리** 성능 (프로토타입)

### 문제 해결
- **OpenAI API 오류**: API 키 유효성 및 크레딧 확인
- **라우터 라우팅 실패**: 엔드포인트 경로 및 모델명 확인
- **GGUF 로딩 실패**: GPU 메모리 할당 확인
- **프로토타입 오류**: 의존성 패키지 설치 확인

### 성능 튜닝
1. **라우터 최적화**
   - 모델별 요청 분산
   - 캐싱 전략 구현
   - 비동기 처리 향상

2. **OpenAI API 최적화**
   - 배치 요청 구현
   - 토큰 사용량 최적화
   - 응답 캐싱 구현

3. **프로토타입 활용**
   - 임베딩 메모리로 응답 품질 향상
   - 파인튜닝으로 특화 모델 개발
   - A/B 테스트로 성능 비교

## 보안 고려사항

### 확장된 보안 기능
- **OpenAI API 키**: 환경 변수를 통한 안전한 관리
- **라우터 기반 접근 제어**: 엔드포인트별 권한 관리
- **프로토타입 분리**: 실험 코드와 프로덕션 코드 격리

### API 보안 강화
- **모델별 접근 제어**: GGUF/OpenAI 모델 분리 관리
- **비용 모니터링**: OpenAI API 사용량 추적
- **라우터 보안**: 경로별 인증 및 검증
- **프로토타입 보안**: 실험 데이터 보호
