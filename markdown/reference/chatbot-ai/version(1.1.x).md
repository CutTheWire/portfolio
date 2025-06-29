# ChatBot AI - 버전 명세서 v1.1.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.1.x 계열 버전에 대한 공식 명세서입니다. v1.0.x 기반의 단일 Llama 모델 시스템에서 **듀얼 AI 모델 시스템**으로 확장되었으며, **캐릭터 기반 대화 기능**과 **검색 연동 응답**을 지원합니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **None** | 2024-11-16 | `7d02373080f428092ee93138960784a0f91626d1` | Unstable |
| **None** | 2024-12-16 | `3071c6319a6e96e695d49f111bfbba5aea603f49` | Unstable |
| **v1.1.0** | 2025-01-15 | `d014744640fa72366c398541ec9f5b4c7361fd7f` | Latest |

## v1.0.x에서 v1.1.x로의 주요 변경사항

### 아키텍처 확장
- **단일 모델** → **듀얼 모델 시스템**
- Llama 3.1 8B (CUDA:0) + **Korean Bllossom 8B (CUDA:1)** 추가
- **캐릭터 기반 대화** 시스템 도입

### 신규 기능
- **Google Search API** 통합 검색 기능
- **10가지 성격 파라미터** 기반 캐릭터 시스템
- **스트리밍 전용 API** 전환
- **Docker 환경** 최적화

### 제거된 기능
- ❌ **복잡도 분석** (BART 모델 제거)
- ❌ **동기식 응답** 생성
- ❌ **적응형 토큰 할당**

## 시스템 요구사항

### 하드웨어 요구사항
- **GPU**: NVIDIA RTX 2080 (Llama 모델용) + RTX 3060 (Bllossom 모델용)
- **VRAM**: 최소 20GB RAM (v1.0.x 대비 2배 증가; 2080 8GB + 3060 12GB)
- **저장공간**: 최소 50GB 여유 공간

### 소프트웨어 요구사항
- **운영체제**: Linux (Ubuntu 20.04 이상 권장)
- **Python**: 3.8 이상
- **CUDA**: 11.8 이상
- **PyTorch**: 2.0 이상
- **Docker**: 컨테이너 환경 지원 (권장)

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot AI v1.1.x
├── 📁 src/
│   ├── 📁 log/                   # 애플리케이션 로그 파일
│   ├── 📁 utils/                 # 핵심 유틸리티 모듈
│   │   ├── AI_Llama_8B.py        # Llama 3.1 8B 모델 인터페이스
│   │   ├── AI_Bllossom_8B.py     # Korean Bllossom 8B 모델 인터페이스 [NEW]
│   │   ├── BaseModels.py         # 확장된 데이터 모델 정의 [UPDATED]
│   │   ├── Error_handlers.py     # 예외 처리 핸들러
│   │   └── __init__.py           # 패키지 초기화 [NEW]
│   ├── server.py                 # FastAPI 서버 진입점 [UPDATED]
│   ├── bot.yaml                  # 봇 설정 파일 [NEW]
│   └── index.html                # 웹 인터페이스 [NEW]
└── .env                          # 환경 변수 설정
```

## API 명세

### 엔드포인트

#### POST /Llama_stream
검색 결과를 활용한 Llama 모델 스트리밍 응답 API

**요청 형식:**
```json
{
  "input_data": "string (1-500자)",
  "google_access": "boolean (default: false)"
}
```

**응답 형식:**
- **Content-Type**: `text/plain`
- **Transfer-Encoding**: `chunked` (스트리밍)

**예시 요청:**
```json
{
  "input_data": "Llama AI 모델의 출시일과 버전들을 각각 알려줘.",
  "google_access": true
}
```

#### POST /Bllossom_stream
캐릭터 설정 기반 Bllossom 모델 스트리밍 응답 API

**요청 형식:**
```json
{
  "input_data": "string (1-500자)",
  "character_name": "string",
  "description": "string",
  "greeting": "string", 
  "image": "string (Google Drive URL)",
  "character_setting": "string",
  "tone": "string",
  "energy_level": "integer (1-10)",
  "politeness": "integer (1-10)",
  "humor": "integer (1-10)",
  "assertiveness": "integer (1-10)",
  "access_level": "boolean (default: true)"
}
```

**예시 요청:**
```json
{
  "input_data": "안녕, 오늘 날씨 어때?",
  "character_name": "KindBot",
  "description": "친절한 도우미 봇",
  "greeting": "안녕하세요! 무엇을 도와드릴까요?",
  "image": "https://drive.google.com/thumbnail?id=12PqUS6bj4eAO_fLDaWQmoq94-771xfim",
  "character_setting": "친절하고 공손한 봇",
  "tone": "공손한",
  "energy_level": 8,
  "politeness": 10,
  "humor": 5,
  "assertiveness": 3,
  "access_level": true
}
```

**HTTP 상태 코드:**
- `200`: 성공 (스트리밍 응답)
- `400`: 잘못된 요청
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. 서버 컴포넌트 (server.py)

#### 듀얼 모델 생명주기 관리
v1.0.x의 단일 모델에서 **듀얼 AI 모델 시스템**으로 확장되었습니다.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI AI 모델 애플리케이션 초기화
    듀얼 GPU 환경에서 Llama와 Bllossom 모델을 동시 로드
    """
    global llama_model_8b, bllossom_model_8b

    def get_cuda_device_info(device_id: int) -> str:
        device_name = torch.cuda.get_device_name(device_id)
        device_properties = torch.cuda.get_device_properties(device_id)
        total_memory = device_properties.total_memory / (1024 ** 3)
        return f"Device {device_id}: {device_name} (Total Memory: {total_memory:.2f} GB)"

    # 듀얼 모델 초기화
    llama_model_8b = Llama_8B()      # CUDA:0 (RTX 2080)
    bllossom_model_8b = Bllossom_8B() # CUDA:1 (RTX 3060)

    llama_device_info = get_cuda_device_info(0)
    bllossom_device_info = get_cuda_device_info(1)

    print(f"Llama 모델 로드 완료 ({llama_device_info})")
    print(f"Bllossom 모델 로드 완료 ({bllossom_device_info})")

    yield

    llama_model_8b = None
    bllossom_model_8b = None
    print("모델 해제 완료")
```

#### 검색 연동 Llama API
Google Search API와 연동하여 실시간 정보를 포함한 응답을 생성합니다.

```python
@app.post("/Llama_stream", summary="AI 모델이 검색 결과를 활용하여 답변 생성")
async def Llama_stream(request: ChatModel.Llama_Request):
    """
    사용자 질문과 검색 결과를 결합하여 AI 답변을 생성합니다.
    
    Args:
        request: 사용자 질문과 검색 옵션 포함
        
    Returns:
        StreamingResponse: AI 모델의 스트리밍 답변
        
    Raises:
        TimeoutError: 모델 응답 시간 초과
        InternalServerErrorException: 서버 내부 오류
    """
    try:
        search_context = ""

        # Google Search API 연동
        if request.google_access:
            search_results = await fetch_search_results(request.input_data, num_results=5)

            if search_results:
                search_context = "\n".join([
                    f"제목: {item['title']}\n설명: {item['snippet']}\n링크: {item['link']}"
                    for item in search_results[:5]
                ])

        # 검색 결과를 포함한 프롬프트 생성
        prompt = (
            f"사용자 질문은 {request.input_data}\n\n"
            f"참고 정보는 {search_context}\n\n"
        )

        response_stream = llama_model_8b.generate_response_stream(input_text=prompt)
        return StreamingResponse(response_stream, media_type="text/plain")

    except TimeoutError:
        raise ChatError.InternalServerErrorException(detail="모델 응답이 시간 초과되었습니다.")
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))
```

#### 캐릭터 기반 Bllossom API
캐릭터 설정을 반영한 맞춤형 대화를 제공합니다.

```python
@app.post("/Bllossom_stream", summary="스트리밍 방식으로 Bllossom_8B 모델 답변 생성")
async def bllossom_stream(request: ChatModel.Bllossom_Request):
    """
    Bllossom_8B 모델에 질문 입력 시 캐릭터 설정을 반영하여 답변을 스트리밍 방식으로 반환
    
    Args:
        request: 캐릭터 설정과 사용자 입력을 포함한 요청
        
    Returns:
        StreamingResponse: 캐릭터 기반 AI 응답
        
    Raises:
        ValidationError: 요청 데이터 검증 실패
        InternalServerErrorException: 서버 내부 오류
    """
    try:
        character_settings = {
            "character_name": request.character_name,
            "description": request.description,
            "greeting": request.greeting,
            "character_setting": request.character_setting,
            "tone": request.tone,
            "energy_level": request.energy_level,
            "politeness": request.politeness,
            "humor": request.humor,
            "assertiveness": request.assertiveness,
            "access_level": request.access_level
        }
        
        response_stream = bllossom_model_8b.generate_response_stream(
            input_text=request.input_data,
            character_settings=character_settings
        )
        return StreamingResponse(response_stream, media_type="text/plain")
        
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))
```

### 2. AI 모델 컴포넌트

#### LlamaChatModel 클래스 (AI_Llama_8B.py) - v1.1.x 업데이트

**v1.0.x에서 변경된 사항:**
- ❌ **복잡도 분석 제거** (BART 모델 불필요)
- ❌ **GTX 1050 의존성 제거**
- ✅ **Docker 환경 지원**
- ✅ **고정 토큰 수** (512 토큰)
- ✅ **스트리밍 전용** 최적화

**클래스 초기화:**
```python
def __init__(self):
    """
    LlamaChatModel 클래스 초기화 - v1.1.x
    Docker 환경에서 CUDA:0 (RTX 2080) 전용으로 최적화
    """
    # 환경 설정
    load_dotenv('.env')
    self.cache_dir = "/app/ai_model/"  # Docker 경로
    self.model_id = "meta-llama/Llama-3.1-8B-Instruct"
    self.device = torch.device("cuda:0")  # RTX 2080 전용

    # 4-bit 양자화 설정
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

    # Hugging Face 토큰 및 가속기 설정
    self.hf_token = os.getenv("HUGGING_FACE_TOKEN")
    self.accelerator = Accelerator(mixed_precision="fp16", device_placement=False)
    self.scaler = GradScaler()

    # 컴포넌트 초기화
    self.tokenizer = self.load_tokenizer()
    self.model = self.load_model()
    self.model.gradient_checkpointing_enable()
    self.conversation_history = []
```

**스트리밍 생성 메서드:**
```python
def generate_response_stream(self, input_text: str):
    """
    Llama 모델 스트리밍 응답 생성 - v1.1.x
    고정 512 토큰으로 최적화됨
    
    Args:
        input_text: 사용자 입력 텍스트
        
    Yields:
        str: 생성되는 텍스트 조각들
    """
    # 토크나이징
    input_ids = self.tokenizer.encode(
        text=input_text,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(self.device)
    
    attention_mask = (input_ids != self.tokenizer.pad_token_id).long().to(self.device)
    streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)

    # 생성 파라미터 (v1.1.x 최적화)
    generation_kwargs = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "min_new_tokens": 1,
        "max_new_tokens": 512,  # 고정값
        "do_sample": True,
        "top_p": 0.9,
        "temperature": 0.7,
        "repetition_penalty": 1.2,
        "streamer": streamer
    }

    thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
    thread.start()

    for new_text in streamer:
        yield new_text
```

#### BllossomChatModel 클래스 (AI_Bllossom_8B.py) - 신규 추가

한국어 특화 AI 모델로 **캐릭터 기반 대화**를 지원합니다.

**주요 특징:**
- **모델**: `MLP-KTLim/llama-3-Korean-Bllossom-8B`
- **GPU**: CUDA:1 (RTX 3060) 전용
- **캐릭터 시스템**: 10가지 성격 파라미터
- **대화 기록**: 최근 5개 대화 유지

**클래스 초기화:**
```python
def __init__(self):
    """
    BllossomChatModel 클래스 초기화
    한국어 특화 모델을 CUDA:1 (RTX 3060)에 로드
    """
    load_dotenv('.env')
    self.cache_dir = "/app/ai_model/"
    self.model_id = "MLP-KTLim/llama-3-Korean-Bllossom-8B"
    self.device = torch.device("cuda:1")  # RTX 3060 전용

    self.model_kwargs = {
        "torch_dtype": torch.float16,
        "trust_remote_code": True,
        "device_map": {"": self.device},
        "quantization_config": BitsAndBytesConfig(load_in_4bit=True)
    }

    # 컴포넌트 초기화
    self.tokenizer = self.load_tokenizer()
    self.model = self.load_model()
    self.conversation_history = []
```

**캐릭터 프롬프트 생성:**
```python
def _build_prompt(self, user_input: str, character_settings: dict):
    """
    캐릭터 설정 기반 프롬프트 생성
    
    Args:
        user_input: 사용자 입력 텍스트
        character_settings: 캐릭터 설정 딕셔너리
        
    Returns:
        str: 구성된 프롬프트
    """
    # 최근 5개 대화 기록 유지
    recent_history = self.conversation_history[-5:]
    history = "\n".join([f"{entry['role']}: {entry['content']}" for entry in recent_history])
    
    prompt = (
        "캐릭터 설정:\n"
        f"이름: {character_settings['character_name']}\n"
        f"설명: {character_settings['description']}\n"
        f"인사말: {character_settings['greeting']}\n"
        f"성격: {character_settings['character_setting']}\n"
        f"말투: {character_settings['tone']}\n"
        f"에너지 레벨: {character_settings['energy_level']}\n"
        f"공손함: {character_settings['politeness']}\n"
        f"유머 감각: {character_settings['humor']}\n"
        f"단호함: {character_settings['assertiveness']}\n"
        f"액세스 수준: {'허용됨' if character_settings['access_level'] else '제한됨'}\n\n"
        
        "지침:\n"
        "- 답변은 항상 한국어로 제공됩니다.\n"
        "- 캐릭터 설정은 응답에 포함되지 않아야 합니다.\n"
        "- 자연스러운 대화형식으로 답변하십시오.\n"
        "- 필요 이상의 반복을 피하십시오.\n"
        f"대화 기록: {history}\n"
    )
    
    self.conversation_history.append({"role": "user", "content": user_input})
    return prompt
```

### 3. 데이터 모델 컴포넌트 (BaseModels.py) - v1.1.x 확장

#### 신규 모델 스키마

##### Llama_Request (확장)
검색 기능이 추가된 요청 모델입니다.

```python
class Llama_Request(BaseModel):
    """
    Llama 모델 API 요청 - v1.1.x 확장
    """
    input_data: str = Field(
        examples=["Llama AI 모델의 출시일과 버전들을 각각 알려줘."],
        title="사용자 입력 문장",
        description="사용자 입력 문장 길이 제약",
        min_length=1, max_length=500
    )
    google_access: bool = Field(
        examples=[False, True],
        default=False,
        title="검색 기반 액세스",
        description="검색 기반 액세스 수준을 나타냅니다. True: 검색 기반 활성화. False: 검색 기반 제한됨."
    )
```

##### Bllossom_Request (신규)
캐릭터 설정을 포함한 복합 요청 모델입니다.

**성격 파라미터 (1-10 범위):**
- **energy_level**: 에너지 수준 (1: 매우 느긋함, 10: 매우 활기참)
- **politeness**: 공손함 (1: 직설적임, 10: 매우 공손함)
- **humor**: 유머 감각 (1: 유머 없음, 10: 매우 유머러스함)
- **assertiveness**: 단호함 (1: 매우 유연함, 10: 매우 단호함)

```python
class Bllossom_Request(BaseModel):
    """
    Bllossom 모델 API 요청 - v1.1.x 신규
    캐릭터 기반 대화를 위한 확장된 요청 모델
    """
    input_data: str = Field(min_length=1, max_length=500)
    character_name: str = Field(
        examples=["KindBot"],
        title="캐릭터 이름",
        min_length=1
    )
    description: str = Field(
        examples=["친절한 도우미 봇"],
        title="캐릭터 설명",
        min_length=1
    )
    greeting: str = Field(
        examples=["안녕하세요! 무엇을 도와드릴까요?"],
        title="캐릭터 인사말",
        min_length=1
    )
    image: str = Field(
        examples=["https://drive.google.com/thumbnail?id=12PqUS6bj4eAO_fLDaWQmoq94-771xfim"],
        title="캐릭터 이미지 URL",
        min_length=1, max_length=2048
    )
    character_setting: str = Field(
        examples=["친절하고 공손한 봇"],
        title="캐릭터 설정 값",
        min_length=1
    )
    tone: str = Field(
        examples=["공손한"],
        title="캐릭터 말투",
        min_length=1
    )
    
    # 성격 파라미터 (1-10 범위)
    energy_level: conint(ge=1, le=10) = Field(
        examples=[8],
        title="캐릭터 에너지",
        description="1(매우 느긋함) ~ 10(매우 활기참)"
    )
    politeness: conint(ge=1, le=10) = Field(
        examples=[10],
        title="캐릭터 공손함", 
        description="1(직설적임) ~ 10(매우 공손함)"
    )
    humor: conint(ge=1, le=10) = Field(
        examples=[5],
        title="캐릭터 유머 감각",
        description="1(유머 없음) ~ 10(매우 유머러스함)"
    )
    assertiveness: conint(ge=1, le=10) = Field(
        examples=[3],
        title="캐릭터 단호함",
        description="1(매우 유연함) ~ 10(매우 단호함)"
    )
    access_level: bool = Field(
        examples=[True, False],
        default=True,
        title="캐릭터 액세스",
        description="True: 특정 기능이나 영역에 대한 접근 권한이 허용됨. False: 제한됨."
    )

    @field_validator('image', mode='before')
    def check_img_url(cls, v):
        """Google Drive URL 형식 검증"""
        return Validators.validate_URL(v)
```

#### URL 검증 유틸리티 (신규)
Google Drive 이미지 URL 검증을 위한 유틸리티 클래스입니다.

```python
class Validators:
    @staticmethod
    def validate_URL(v: str) -> str:
        """
        Google Drive URL 형식 검증 함수
        
        Args:
            v: 검증할 URL 문자열
            
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
            img_url: 테스트할 이미지 URL
            
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

### 4. 예외 처리 컴포넌트 (Error_handlers.py)

v1.0.x와 동일한 예외 처리 시스템을 유지합니다.

#### 예외 클래스 계층구조

| 예외 클래스 | HTTP 코드 | 설명 | 사용 시점 |
|-------------|-----------|------|-----------|
| `NotFoundException` | 404 | 리소스 없음 | 요청한 리소스를 찾을 수 없음 |
| `BadRequestException` | 400 | 잘못된 요청 | 클라이언트 요청 형식 오류 |
| `UnauthorizedException` | 401 | 인증 필요 | 인증되지 않은 접근 |
| `ForbiddenException` | 403 | 접근 거부 | 권한 부족 |
| `ValueErrorException` | 422 | 유효성 검사 실패 | 입력값 형식/타입 오류 |
| `InternalServerErrorException` | 500 | 서버 내부 오류 | 예상치 못한 서버 오류 |

## 성능 특성

### 메모리 사용량
- **Llama 모델**: ~14GB VRAM (RTX 2080) - v1.0.x 대비 17% 증가
- **Bllossom 모델**: ~6GB VRAM (RTX 3060) - 신규
- **시스템 RAM**: ~12GB - v1.0.x 대비 50% 증가

### 처리량
- **동시 요청**: 2개 (듀얼 GPU 활용)
- **시간당 요청**: ~200-400개 (모델별 분산 처리)

## 운영 가이드

### 환경 설정
1. **Docker 환경** 구성 권장
2. `.env` 파일에 `HUGGING_FACE_TOKEN` 설정
3. **Google Search API** 키 설정 (검색 기능 사용 시)
4. 필요한 Python 패키지 설치

### 모니터링 포인트
- **듀얼 GPU** 메모리 사용률 모니터링
- **스트리밍 응답** 지연시간 추적
- **캐릭터 설정** 파라미터 효과성 분석
- **검색 API** 호출 빈도 및 성공률

### 문제 해결
- **메모리 부족**: 모델별 배치 크기 개별 조정
- **스트리밍 지연**: 네트워크 설정 및 토큰 생성 속도 최적화
- **캐릭터 일관성**: 대화 기록 길이 및 프롬프트 템플릿 조정

## 보안 고려사항

### 확장된 입력 검증
- **캐릭터 파라미터** 범위 검증 (1-10)
- **Google Drive URL** 형식 검증 및 접근성 확인
- **검색 쿼리** 필터링 및 제한

### API 보안
- **모델별 접근 제어** (Llama/Bllossom 분리)
- **스트리밍 연결** 타임아웃 설정
- **캐릭터 데이터** 민감정보 보호
