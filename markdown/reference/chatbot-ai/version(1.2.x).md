# ChatBot AI - 버전 명세서 v1.2.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.2.x 계열 버전에 대한 공식 명세서입니다. v1.1.x의 듀얼 AI 모델 시스템에서 **GGUF 기반 최적화**와 **MongoDB 연동**, **파인튜닝 지원**을 추가한 차세대 AI 챗봇 서비스입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.2.0** | 2025-02-18 | `cba10b2cebceaf36d2836c9e9e0bb5fcaf37dffd` | Latest |

## v1.1.x에서 v1.2.x로의 주요 변경사항

### 모델 아키텍처 혁신
- **HuggingFace Transformers** → **GGUF (llama.cpp) 기반**
- **Korean Bllossom 8B** → **Lumimaid 8B** (캐릭터 특화 모델)
- **4-bit 양자화** → **Q5_K_S 양자화** (품질과 성능 균형)

### 인프라 변화
- **MySQL** → **MongoDB** 데이터베이스 전환
- **Docker FastAPI** → **로컬 네이티브** 환경 최적화

### 신규 기능
- **파인튜닝 프레임워크** (PEFT + LoRA)
- **캐릭터 카드 시스템** (PNG 메타데이터 지원)
- **데이터셋 관리** (ko_wikidata_QA)
- **성능 모니터링** 도구

### 제거된 기능
- ❌ **Transformers 기반 모델** 지원
- ❌ **Docker 컨테이너** 환경
- ❌ **검색 API 연동**

## 시스템 요구사항

### 하드웨어 요구사항
- **GPU**: NVIDIA RTX 2080 (Llama 모델용) + NVIDIA RTX 3060 (Lumimaid 8B 모델용)
- **VRAM**: 최소 20GB RAM (2080 8GB + 3060 12GB)
- **저장공간**: 최소 50GB 여유 공간

### 소프트웨어 요구사항
- **운영체제**: Windows 10/11 (64-bit)
- **Python**: 3.11 이상
- **CUDA**: 12.1 이상
- **llama-cpp-python**: CUDA 지원 버전
- **MongoDB**: 7.0 이상

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot AI v1.2.x
├── 📁 fastapi/
│   ├── 📁 ai_model/              # GGUF 모델 저장소
│   │   ├── v2-Llama-3-Lumimaid-8B-v0.1-OAS-Q5_K_S-imat.gguf
│   │   ├── llama-3.1-8b-instruct.gguf
│   │   └── README.md
│   ├── 📁 src/
│   │   ├── 📁 utils/             # 핵심 유틸리티 모듈
│   │   │   ├── AI_Llama_8B.py    # Llama 3.1 8B 모델 (CUDA:0)
│   │   │   ├── AI_Lumimaid_8B.py # Lumimaid 8B 모델 (CUDA:1) [NEW]
│   │   │   ├── Database_mongo.py # MongoDB 핸들러 [NEW]
│   │   │   ├── BaseModels.py     # 데이터 모델 정의 [UPDATED]
│   │   │   ├── Error_handlers.py # 예외 처리 핸들러
│   │   │   └── __init__.py       # 패키지 초기화
│   │   ├── server.py             # FastAPI 서버 진입점 [UPDATED]
│   │   ├── bot.yaml              # 봇 설정 파일
│   │   └── index.html            # 웹 인터페이스
│   ├── requirements.txt          # 기본 패키지 [UPDATED]
│   └── requirements_llama.txt    # llama.cpp 관련 패키지 [NEW]
├── 📁 mongo/                     # MongoDB 컨테이너 설정 [NEW]
│   ├── Dockerfile                # MongoDB 도커파일
│   ├── mongod.conf               # MongoDB 설정
│   └── .env                      # MongoDB 환경변수
├── docker-compose.yml            # MongoDB 전용 컴포즈 [UPDATED]
├── rebuild.bat                   # 빌드 스크립트 [UPDATED]
└── .env                          # 환경 변수 설정
```

## API 명세

### 엔드포인트

#### POST /Llama_stream
Llama 3.1 8B 모델 기반 검색 연동 스트리밍 응답

**요청 형식:**
```json
{
  "input_data": "string (1-500자)",
  "google_access": "boolean (default: false)"
}
```

**응답 형식:**
- **Content-Type**: `text/plain`
- **Transfer-Encoding**: `chunked`

#### POST /Lumimaid_stream
GGUF 기반 Lumimaid 8B 모델 캐릭터 대화 API

**요청 형식:**
```json
{
  "input_data": "string (1-500자)",
  "character_name": "string",
  "greeting": "string",
  "context": "string",
  "image": "string (Google Drive URL)",
  "access_level": "boolean (default: true)"
}
```

**예시 요청:**
```json
{
  "input_data": "*I approach Rachel and talk to her.*",
  "character_name": "Rachel",
  "greeting": "*Rachel stands nervously at the lectern...*",
  "context": "Rachel is a devout Catholic girl of about 19 years old...",
  "image": "https://drive.google.com/thumbnail?id=12PqUS6bj4eAO_fLDaWQmoq94-771xfim",
  "access_level": true
}
```

#### MongoDB API 엔드포인트

##### GET /mongo/db
데이터베이스 목록 조회

**응답 형식:**
```json
{
  "Database": ["admin", "config", "local", "chatbot"]
}
```

##### GET /mongo/collections?db_name=chatbot
컬렉션 목록 조회

**응답 형식:**
```json
{
  "Collections": ["users", "conversations", "characters"]
}
```

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `404`: 리소스 없음
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. 서버 컴포넌트 (server.py) - v1.2.x 재설계

#### 하이브리드 모델 아키텍처
v1.1.x의 완전한 듀얼 시스템에서 **Transformers + GGUF 하이브리드**로 전환되었습니다.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI AI 모델 애플리케이션 초기화 - v1.2.x
    Transformers(CUDA:0) + GGUF(CUDA:1) 하이브리드 시스템
    """
    global llama_model_8b, Lumimaid_model_8b, mongo_handler

    def get_cuda_device_info(device_id: int) -> str:
        device_name = torch.cuda.get_device_name(device_id)
        device_properties = torch.cuda.get_device_properties(device_id)
        total_memory = device_properties.total_memory / (1024 ** 3)
        return f"Device {device_id}: {device_name} (Total Memory: {total_memory:.2f} GB)"

    # 하이브리드 모델 초기화
    llama_model_8b = Llama_8B()         # Transformers (CUDA:0)
    Lumimaid_model_8b = Lumimaid_8B()   # GGUF llama.cpp (CUDA:1)
    mongo_handler = MongoDBHandler()    # MongoDB 핸들러

    llama_device_info = get_cuda_device_info(0)
    lumimaid_device_info = get_cuda_device_info(1)

    print(f"Llama 모델 로드 완료 ({llama_device_info})")
    print(f"Lumimaid 모델 로드 완료 ({lumimaid_device_info})")
    print(f"MongoDB 연결 완료")

    yield

    llama_model_8b = None
    Lumimaid_model_8b = None
    print("모델 해제 완료")
```

#### MongoDB 라우터 추가
MongoDB 데이터베이스와의 상호작용을 위한 전용 라우터가 추가되었습니다.

```python
mongo_router = APIRouter()

@mongo_router.get("/db", summary="데이터베이스 목록 가져오기")
async def list_databases():
    """
    MongoDB 서버에 있는 모든 데이터베이스의 목록을 반환합니다.
    """
    try:
        databases = await mongo_handler.get_db()
        return {"Database": databases}
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))

@mongo_router.get("/collections", summary="데이터베이스 컬렉션 목록 가져오기")
async def list_collections(db_name: str = Query(..., description="데이터베이스 이름")):
    """
    현재 선택된 데이터베이스 내의 모든 컬렉션 이름을 반환합니다.
    """
    try:
        collections = await mongo_handler.get_collection(database_name=db_name)
        return {"Collections": collections}
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))

app.include_router(
    mongo_router,
    prefix="/mongo",
    tags=["MongoDB Router"],
    responses={500: {"description": "Internal Server Error"}}
)
```

#### 개선된 Lumimaid 스트리밍 API
GGUF 기반의 최적화된 캐릭터 대화 시스템입니다.

```python
@app.post("/Lumimaid_stream", summary="스트리밍 방식으로 Lumimaid_8B 모델 답변 생성")
async def Lumimaid_stream(request: ChatModel.Lumimaid_Request):
    """
    Lumimaid_8B GGUF 모델에 질문을 입력하고 캐릭터 설정을 반영하여 
    답변을 스트리밍 방식으로 반환합니다.

    Args:
        request (ChatModel.Lumimaid_Request): 사용자 요청 데이터

    Returns:
        StreamingResponse: AI 모델의 스트리밍 답변
    """
    try:
        # 캐릭터 설정 구성
        character_settings = {
            "character_name": request.character_name,
            "greeting": request.greeting,
            "context": request.context,
            "access_level": request.access_level
        }
        
        # GGUF 모델 스트리밍 응답 생성
        response_stream = Lumimaid_model_8b.generate_response_stream(
            input_text=request.input_data,
            character_settings=character_settings
        )
        
        return StreamingResponse(
            response_stream,
            media_type="text/plain",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except TimeoutError:
        raise ChatError.InternalServerErrorException(
            detail="Lumimaid 모델 응답이 시간 초과되었습니다."
        )
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except Exception as e:
        print(f"처리되지 않은 예외: {e}")
        raise ChatError.InternalServerErrorException(detail=str(e))
```

### 2. AI 모델 컴포넌트

#### LlamaChatModel 클래스 (AI_Llama_8B.py) - v1.2.x 업데이트

**v1.1.x에서 변경된 사항:**
- ✅ **로컬 환경 최적화** (Docker 의존성 제거)
- ✅ **성능 튜닝** (생성 파라미터 최적화)

```python
def __init__(self):
    """
    LlamaChatModel 클래스 초기화 - v1.2.x
    로컬 환경에서 CUDA:0 전용으로 최적화
    """
    # 환경 설정 (로컬 경로)
    load_dotenv('.env')
    self.cache_dir = "./fastapi/ai_model"  # Docker → 로컬 경로
    self.model_id = "meta-llama/Llama-3.1-8B-Instruct"
    self.device = torch.device("cuda:0")   # RTX 2080

    # 4-bit 양자화 설정 (동일)
    self.model_kwargs = {
        "torch_dtype": torch.float16,
        "trust_remote_code": True,
        "device_map": {"": self.device},
        "quantization_config": BitsAndBytesConfig(
            load_in_4bit=True,
            double_quant=True,
            compute_dtype=torch.float16
        )
    }

    # 컴포넌트 초기화
    self.tokenizer = self.load_tokenizer()
    self.model = self.load_model()
    self.model.gradient_checkpointing_enable()
    self.conversation_history = []
```

#### LlamaModelHandler 클래스 (AI_Lumimaid_8B.py) - 신규 GGUF 모델

**주요 특징:**
- **모델**: `v2-Llama-3-Lumimaid-8B-v0.1-OAS-Q5_K_S-imat.gguf`
- **엔진**: llama-cpp-python (CUDA 지원)
- **GPU**: CUDA:1 (RTX 3060) 전용
- **양자화**: Q5_K_S (고품질 5-bit 양자화)
- **캐릭터 시스템**: PNG V2 카드 지원

**클래스 초기화:**
```python
def __init__(self, gpu_layers: int = 50) -> None:
    """
    GGUF 모델 초기화 - RTX 3060 최적화
    
    Args:
        gpu_layers (int): GPU에 로드할 레이어 수 (기본값 50)
    """
    self.model_path = "fastapi/ai_model/v2-Llama-3-Lumimaid-8B-v0.1-OAS-Q5_K_S-imat.gguf"
    self.verbose = False
    self.gpu_layers = gpu_layers
    self.model = self._load_model()
    self.response_queue = Queue()

def _load_model(self) -> Llama:
    """
    Llama 모델을 CUDA:1 디바이스(RTX 3060)에만 로드
    
    Returns:
        Llama: 로드된 GGUF 모델 객체
    """
    print("GGUF 모델 로드 중...")
    try:
        model = Llama(
            model_path=self.model_path,
            n_gpu_layers=self.gpu_layers,
            main_gpu=1,                # RTX 3060 사용
            n_ctx=2048,                # 컨텍스트 길이
            n_batch=512,               # 배치 크기
            verbose=self.verbose,
            offload_kqv=True,          # KQV 캐시를 GPU에 오프로드
            use_mmap=False,            # 메모리 매핑 비활성화
            use_mlock=True,            # 메모리 잠금 활성화
            n_threads=8                # 스레드 수 제한
        )
        print("✅ GGUF 모델이 CUDA:1 (RTX 3060)에 성공적으로 로드되었습니다.")
        print(f"🔧 GPU 설정: {self.gpu_layers}개 레이어, KQV 캐시 오프로드 활성화")
        return model
    except Exception as e:
        print(f"❌ GGUF 모델 로드 중 오류 발생: {e}")
        raise
```

**Llama3 프롬프트 템플릿:**
```python
def build_llama3_prompt(character: CharacterPrompt, user_input: str) -> str:
    """
    캐릭터 정보를 포함한 Llama3 프롬프트 형식 생성

    Args:
        character (CharacterPrompt): 캐릭터 정보
        user_input (str): 사용자 입력

    Returns:
        str: Llama3 형식의 프롬프트 문자열
    """
    system_prompt = (
        f"Character Name: {character.name}\n"
        f"Character Context: {character.context}\n"
        f"Initial Greeting: {character.greeting}"
    )
    
    return (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{system_prompt}<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n"
        f"{user_input}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n"
    )
```

**스트리밍 응답 생성:**
```python
def generate_response_stream(self, input_text: str, character_settings: dict = None) -> Generator[str, None, None]:
    """
    API 호환을 위한 스트리밍 응답 생성 메서드

    Args:
        input_text (str): 사용자 입력 텍스트
        character_settings (dict): 캐릭터 설정 딕셔너리

    Yields:
        str: 생성된 텍스트 조각들
    """
    try:
        # 캐릭터 정보 설정
        if character_settings:
            character_info = CharacterPrompt(
                name=character_settings.get("character_name", "Assistant"),
                greeting=character_settings.get("greeting", ""),
                context=character_settings.get("context", "")
            )
            # Llama3 프롬프트 형식으로 변환
            prompt = build_llama3_prompt(character_info, input_text)
        else:
            prompt = input_text
        
        # 스트리밍 응답 생성
        for text_chunk in self.create_streaming_completion(
            prompt=prompt,
            max_tokens=2048,
            temperature=0.7,
            top_p=0.95,
            stop=["<|eot_id|>"]
        ):
            yield text_chunk

    except Exception as e:
        print(f"응답 생성 중 오류 발생: {e}")
        yield f"오류: {str(e)}"
```

### 3. 데이터베이스 컴포넌트 (Database_mongo.py) - 신규 추가

#### MongoDBHandler 클래스
MySQL을 대체하는 MongoDB 연동 핸들러입니다.

**주요 특징:**
- **비동기 처리**: motor.motor_asyncio 사용
- **연결 풀링**: 자동 연결 관리
- **에러 핸들링**: 통합 예외 처리

```python
class MongoDBHandler:
    def __init__(self) -> None:
        """
        MongoDBHandler 클래스 초기화.
        MongoDB에 연결하고 필요한 환경 변수를 로드합니다.
        """
        try:
            # 환경 변수 파일 경로 설정
            current_directory = os.path.dirname(os.path.abspath(__file__))
            env_file_path = os.path.join(current_directory, '../.env')
            load_dotenv(env_file_path)
            
            # 환경 변수에서 MongoDB 연결 URI 가져오기
            mongo_host = os.getenv("MONGO_HOST")
            mongo_port = os.getenv("MONGO_PORT", 27018)
            mongo_user = os.getenv("MONGO_ADMIN_USER")
            mongo_password = os.getenv("MONGO_ADMIN_PASSWORD")
            mongo_db = os.getenv("MONGO_DATABASE")
            mongo_auth = os.getenv("MONGO_AUTH")
            
            # MongoDB URI 생성
            self.mongo_uri = (
                f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
                f"{mongo_db}?authSource={mongo_auth}"
            )
            
            # MongoDB 클라이언트 초기화
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client[mongo_db]
        except PyMongoError as e:
            raise InternalServerErrorException(detail=f"MongoDB connection error: {str(e)}")
        except Exception as e:
            raise InternalServerErrorException(detail=f"Error initializing MongoDBHandler: {str(e)}")

    async def get_db(self) -> List[str]:
        """
        데이터베이스 이름 목록을 반환합니다.
        
        Returns:
            List[str]: 데이터베이스 이름 리스트
        Raises:
            InternalServerErrorException: 데이터베이스 이름을 가져오는 도중 문제가 발생할 경우
        """
        try:
            return await self.client.list_database_names()
        except PyMongoError as e:
            raise InternalServerErrorException(detail=f"Error retrieving database names: {str(e)}")
        except Exception as e:
            raise InternalServerErrorException(detail=f"Unexpected error: {str(e)}")

    async def get_collection(self, database_name: str) -> List[str]:
        """
        데이터베이스의 컬렉션 이름 목록을 반환합니다.
        
        Args:
            database_name (str): 데이터베이스 이름
        Returns:
            List[str]: 컬렉션 이름 리스트
        Raises:
            NotFoundException: 데이터베이스가 존재하지 않을 경우
            InternalServerErrorException: 컬렉션 이름을 가져오는 도중 문제가 발생할 경우
        """
        db_names = await self.get_db()
        if database_name not in db_names:
            raise NotFoundException(f"Database '{database_name}' not found.")
        try:
            return await self.client[database_name].list_collection_names()
        except PyMongoError as e:
            raise InternalServerErrorException(detail=f"Error retrieving collection names: {str(e)}")
        except Exception as e:
            raise InternalServerErrorException(detail=f"Unexpected error: {str(e)}")
```

### 4. 데이터 모델 컴포넌트 (BaseModels.py) - v1.2.x 간소화

#### Lumimaid_Request (신규)
v1.1.x의 복잡한 Bllossom_Request를 간소화한 캐릭터 요청 모델입니다.

**제거된 필드:**
- ❌ `description` (greeting에 통합)
- ❌ `character_setting` (context로 통합)
- ❌ `tone` (context에 포함)
- ❌ `energy_level`, `politeness`, `humor`, `assertiveness` (수치 파라미터 제거)

**유지된 필드:**
- ✅ `input_data` (사용자 입력)
- ✅ `character_name` (캐릭터 이름)
- ✅ `greeting` (인사말/첫 메시지)
- ✅ `context` (캐릭터 설정 텍스트)
- ✅ `image` (캐릭터 이미지 URL)
- ✅ `access_level` (접근 권한)

```python
class Lumimaid_Request(BaseModel):
    """
    Lumimaid 모델 API 요청 - v1.2.x 간소화
    캐릭터 기반 대화를 위한 최적화된 요청 모델
    """
    input_data: str = character_input_data_set
    character_name: str = character_name_set
    greeting: str = greeting_set
    context: str = context_set
    image: str = image_set
    access_level: bool = access_level_set
    
    @field_validator('image', mode='before')
    def check_img_url(cls, v):
        """Google Drive URL 형식 검증"""
        return Validators.validate_URL(v)

    def model_dump(self, **kwargs):
        """
        모델을 딕셔너리로 변환할 때 사용하는 메서드
        """
        return super().model_dump(**kwargs)
    
class Lumimaid_Response(BaseModel):
    output_data: str = output_data_set
```

#### 향상된 URL 검증
Google Drive 이미지 URL에 대한 고급 검증 시스템입니다.

```python
class Validators:
    @staticmethod
    def validate_URL(v: str) -> str:
        """
        Google Drive URL 형식 검증 함수
        
        Args:
            v (str): 검증할 URL 문자열
            
        Returns:
            str: 검증된 URL
            
        Raises:
            ValueError: 유효하지 않은 URL 형식
        """
        url_pattern = re.compile(
            r'''
            ^                     # 문자열의 시작
            https?://             # http:// 또는 https://
            (drive\.google\.com)  # Google Drive 도메인
            /thumbnail            # 경로의 일부
            \?id=([a-zA-Z0-9_-]+) # 쿼리 파라미터 id
            $                     # 문자열의 끝
            ''', re.VERBOSE
        )
        if not url_pattern.match(v):
            raise ValueError('유효한 URL 형식이 아닙니다.')
        return v

    @staticmethod
    async def check_img_url(img_url: str):
        """
        URL의 연결 테스트 함수
        
        Args:
            img_url (str): 테스트할 이미지 URL
            
        Raises:
            ValueError: 이미지 접근 불가 또는 연결 오류
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(img_url, follow_redirects=True)
            if response.status_code != 200:
                raise ValueError('이미지에 접근할 수 없습니다.')
        except httpx.RequestError:
            raise ValueError('이미지 URL에 접근하는 중 오류가 발생했습니다.')
```

## 설치 및 설정

### 패키지 설치 시스템 (venv_install.bat) - v1.2.x 대폭 개선

Windows 환경에서 복잡한 CUDA 의존성을 자동으로 처리하는 향상된 설치 스크립트입니다.

```batch
@echo off
chcp 65001
SETLOCAL

:: pip 최신 버전으로 업그레이드
python.exe -m pip install --upgrade pip

:: numpy 먼저 설치 (버전 제한)
pip install "numpy>=1.22.4,<2.0.0"

:: CUDA 관련 패키지 설치
pip install torch==2.3.1+cu118 torchvision==0.18.1+cu118 torchaudio==2.3.1+cu118 -f https://download.pytorch.org/whl/torch_stable.html

:: CUDA llama-cpp 설치
set CMAKE_ARGS="-DLLAMA_CUBLAS=on"
set FORCE_CMAKE=1
pip install --no-cache-dir "https://github.com/oobabooga/llama-cpp-python-cuBLAS-wheels/releases/download/textgen-webui/llama_cpp_python_cuda-0.3.6+cu121-cp311-cp311-win_amd64.whl"

:: ExLlamaV2 설치 (최신 버전)
pip install exllamav2==0.2.8

:: Flash Attention 설치 (pre-built wheel 사용)
pip install --no-cache-dir --find-links https://github.com/Dao-AILab/flash-attention/releases/download/v2.3.3/ flash-attn==2.3.3

:: CUDA 빌드 도구 설치
pip install ninja

:: spaCy 설치 및 모델 다운로드
pip install spacy
python -m spacy download en_core_web_sm
python -m spacy download ko_core_news_sm

:: 나머지 requirements.txt 패키지 설치
pip install -r .\fastapi\requirements.txt
pip install -r .\fastapi\requirements_llama.txt

echo 가상 환경이 성공적으로 설정되었습니다.
ENDLOCAL
```

### MongoDB 컨테이너 설정

#### Docker Compose (docker-compose.yml) - MongoDB 전용
FastAPI 컨테이너를 제거하고 MongoDB만 컨테이너로 실행합니다.

```yaml
version: '3.8'

services:
  mongodb:
    restart: unless-stopped
    build:
      context: ./mongo
    ports:
      - "27018:27018"
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ADMIN_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ADMIN_PASSWORD}
      MONGO_DATABASE: ${MONGO_DATABASE}
    volumes:
      - ./mongo/data:/data/db
      - ./mongo/log:/var/log/mongodb
      - ./mongo/.env:/docker-entrypoint-initdb.d/.env
```

#### MongoDB 설정 (mongo/mongod.conf)
```yaml
# MongoDB 구성 파일
storage:
  dbPath: /data/db
  journal:
    enabled: true

systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true

net:
  port: 27018
  bindIp: 0.0.0.0

security:
  authorization: enabled
```

## 성능 특성

### 메모리 사용량
- **Llama (Transformers)**: ~8GB VRAM (RTX 2080)
- **Lumimaid (GGUF)**: ~6GB VRAM (RTX 3060)
- **MongoDB**: ~1GB RAM
- **시스템 RAM**: ~8-12GB

### 처리량
- **동시 요청**: 2개 (하이브리드 시스템)
- **시간당 요청**: ~300-500개
- **GGUF 성능**: Transformers 대비 20-30% 향상

## 운영 가이드

### 환경 설정
1. **Windows 11** + **Python 3.11** 환경 구성
2. **CUDA 12.1** 드라이버 설치
3. **MongoDB 컨테이너** 실행
4. **가상환경** 설정 및 패키지 설치

### 모니터링 포인트
- **하이브리드 GPU** 메모리 사용률 (CUDA:0, CUDA:1)
- **GGUF 모델** 로딩 및 추론 성능
- **MongoDB** 연결 상태 및 쿼리 성능
- **스트리밍 응답** 지연시간 및 처리량

### 문제 해결
- **GGUF 로딩 실패**: GPU 메모리 부족 시 레이어 수 조정
- **MongoDB 연결 오류**: 컨테이너 상태 및 포트 확인
- **스트리밍 끊김**: 네트워크 설정 및 큐 크기 조정
- **캐릭터 카드 오류**: PNG 메타데이터 형식 확인

### 성능 튜닝
1. **GGUF 파라미터** 조정
   - `n_gpu_layers`: 50 (기본값) → 35-60 (VRAM에 따라)
   - `n_ctx`: 2048 → 4096 (긴 대화 지원)
   - `n_batch`: 512 → 256-1024 (메모리 vs 속도)

2. **MongoDB 최적화**
   - 인덱스 생성 (자주 쿼리하는 필드)
   - 연결 풀 크기 조정
   - 캐시 설정 최적화

3. **캐릭터 시스템 최적화**
   - 프롬프트 템플릿 간소화
   - 컨텍스트 길이 제한
   - 반복 토큰 방지 설정

## 보안 고려사항

### 확장된 보안 기능
- **MongoDB 인증**: 사용자 기반 접근 제어
- **GGUF 모델 검증**: 파일 무결성 확인
- **로컬 환경 보안**: Docker 의존성 제거

### API 보안 강화
- **MongoDB 라우터** 접근 제한
- **스트리밍 연결** 속도 제한
- **캐릭터 데이터** 크기 제한
- **파일 업로드** 검증 강화
