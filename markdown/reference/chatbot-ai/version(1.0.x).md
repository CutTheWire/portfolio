# ChatBot AI - 버전 명세서 v1.0.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.0.x 계열 버전에 대한 공식 명세서입니다. 본 시스템은 FastAPI 기반의 웹 서비스로, Meta의 Llama 3.1 8B 모델을 활용한 AI 챗봇 서비스를 제공합니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.0.0** | 2024-10-19 | `acfd23b2f0a67f6ae21105c5cd1f838d89a8d752` | Stable |
| **v1.0.1** | 2024-10-20 | `c4264a2f8f54dc3aef77b54aedc1853989074bc3` | Stable |
| **v1.0.2** | 2024-10-22 | `3ebe8e2a5edda44b2076937eb484a1f18b889927` | Latest |
| **None** | 2024-11-16 | `7d02373080f428092ee93138960784a0f91626d1` | Unstable |
| **None** | 2024-12-16 | `3071c6319a6e96e695d49f111bfbba5aea603f49` | Unstable |

## 시스템 요구사항

### 하드웨어 요구사항
- **GPU**: NVIDIA RTX 2080 (메인 모델용) + GTX 1050 (복잡도 분석용)
- **VRAM**: 최소 10GB (RTX 2080 8GB + GTX 1050 2GB)
- **저장공간**: 최소 50GB 여유 공간

### 소프트웨어 요구사항
- **운영체제**: Linux (Ubuntu 20.04 이상 권장)
- **Python**: 3.8 이상
- **CUDA**: 11.8 이상
- **PyTorch**: 2.0 이상

## 아키텍처
### 프로젝트 구조
```
📦 ChatBot AI v1.0.x
├── 📁 src/
│   ├── 📁 logs/               # 애플리케이션 로그 파일
│   ├── 📁 utils/              # 핵심 유틸리티 모듈
│   │   ├── AI_Llama_8B.py     # Llama 모델 인터페이스
│   │   ├── Error_handlers.py  # 예외 처리 핸들러
│   │   └── Models.py          # 데이터 모델 정의
│   └── server.py              # FastAPI 서버 진입점
└── .env                       # 환경 변수 설정
```

## API 명세

### 엔드포인트

#### POST /Llama
Llama 모델을 사용한 텍스트 생성 API

**요청 형식:**
```json
{
  "input_data": "string (1-500자)"
}
```

**응답 형식:**
```json
{
  "output_data": "string"
}
```

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트
### 1. 서버 컴포넌트 (server.py)

#### 애플리케이션 생명주기 관리
FastAPI 애플리케이션의 시작과 종료 시점을 관리하는 컨텍스트 매니저입니다.

**기능:**
- Llama 모델 초기화 및 리소스 할당
- 애플리케이션 종료 시 메모리 정리

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    global llama_model
    llama_model = LlamaChatModel()
    print("Llama 모델 로드 완료")
    yield
    llama_model = None
    print("Llama 모델 해제 완료")
```

#### API 엔드포인트 구현

```python
@app.post("/Llama", response_model=ChatModel.Llama_Response, summary="Llama 모델 답변 생성")
async def Llama_(request: ChatModel.Llama_Request):
    """
    Llama 모델에 질문을 입력하면 AI가 생성한 답변을 반환합니다.
    
    Args:
        request: 사용자 입력 텍스트를 포함한 요청 객체
        
    Returns:
        ChatModel.Llama_Response: AI가 생성한 응답 텍스트
        
    Raises:
        BadRequestException: 잘못된 요청 형식
        InternalServerErrorException: 서버 내부 오류
    """
    try:
        response_text = llama_model.generate_response(request.input_data)
        return {"output_data": response_text}
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))
```

### 2. AI 모델 컴포넌트 (AI_Llama_8B.py)

#### LlamaChatModel 클래스
GPU 기반의 Llama 3.1 8B 모델을 관리하는 핵심 클래스입니다.

**주요 특징:**
- 듀얼 GPU 활용 (RTX 2080 + GTX 1050)
- 4-bit 양자화를 통한 메모리 최적화
- 복잡도 기반 적응형 토큰 생성
- 스트리밍 응답 지원 (v1.0.2+)

#### 클래스 초기화

**구성 요소:**
- 모델 ID: `meta-llama/Llama-3.1-8B-Instruct`
- 복잡도 분석 모델: `facebook/bart-large-mnli`
- 양자화: 4-bit BitsAndBytesConfig
- 정밀도: FP16 혼합 정밀도

```python
def __init__(self):
    """
    LlamaChatModel 클래스를 초기화합니다.
    환경 변수 로드, GPU 설정, 모델 및 토크나이저 준비를 수행합니다.
    """
    # 환경 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    dotenv_path = os.path.join(parent_dir, '.env')
    load_dotenv(dotenv_path)
    
    # 모델 설정
    self.cache_dir = "./fastapi/ai_model/"
    self.model_id = "meta-llama/Llama-3.1-8B-Instruct"
    self.bart_model_id = "facebook/bart-large-mnli"
    
    # GPU 장치 설정
    self.device_2080 = torch.device("cuda:0")  # 메인 모델용
    self.device_1050 = torch.device("cuda:1")  # 복잡도 분석용
    
    # 컴포넌트 초기화
    self.tokenizer = self.load_tokenizer()
    self.model, self.optimizer = self.load_model_with_accelerator()
    self.complexity_analyzer = self.load_complexity_analyzer()
```

#### 주요 메서드

##### load_tokenizer()
Llama 모델용 토크나이저를 로드합니다.

```python
def load_tokenizer(self) -> transformers.PreTrainedTokenizerBase:
    """
    Llama 모델용 토크나이저를 로드하고 설정합니다.
    
    Returns:
        PreTrainedTokenizerBase: 설정된 토크나이저 객체
    """
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        self.model_id,
        token=self.hf_token
    )
    tokenizer.pad_token_id = tokenizer.eos_token_id
    return tokenizer
```

##### load_complexity_analyzer()
BART 모델을 사용한 텍스트 복잡도 분석기를 GTX 1050에 로드합니다.

```python
def load_complexity_analyzer(self) -> transformers.Pipeline:
    """
    텍스트 복잡도 분석을 위한 BART 모델을 GTX 1050에 로드합니다.
    
    Returns:
        Pipeline: 텍스트 분류 파이프라인
    """
    return pipeline(
        "text-classification",
        model=self.bart_model_id,
        device=self.device_1050.index,
    )
```

##### load_model_with_accelerator()
메인 Llama 모델을 RTX 2080에 로드하고 옵티마이저를 설정합니다.

```python
def load_model_with_accelerator(self) -> tuple:
    """
    Llama 모델을 4-bit 양자화로 로드하고 옵티마이저를 준비합니다.
    
    Returns:
        tuple: (모델, 옵티마이저) 튜플
    """
    model = transformers.AutoModelForCausalLM.from_pretrained(
        self.model_id,
        cache_dir=self.cache_dir,
        token=self.hf_token,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        quantization_config=BitsAndBytesConfig(load_in_4bit=True)
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
    model, optimizer = self.accelerator.prepare(model, optimizer)
    model.to(self.device_2080)
    return model, optimizer
```

#### 응답 생성 알고리즘

##### 복잡도 기반 적응형 토큰 할당
입력 텍스트의 복잡도를 분석하여 적절한 응답 길이를 결정합니다.

**복잡도 레벨:**
- **Low**: 100 토큰 (단순한 질문)
- **Medium**: 250 토큰 (일반적인 질문) 
- **High**: 500 토큰 (복잡한 질문)

```python
def analyze_complexity(self, input_text: str) -> str:
    """
    BART 모델을 사용하여 입력 텍스트의 복잡도를 분석합니다.
    
    Args:
        input_text: 분석할 입력 텍스트
        
    Returns:
        str: 복잡도 레벨 ('low', 'medium', 'high')
    """
    result = self.complexity_analyzer(input_text)
    label = result[0]['label']
    if "ENTAILMENT" in label:
        return "low"
    elif "CONTRADICTION" in label:
        return "high"
    return "medium"

def adjust_max_tokens(self, complexity: str) -> int:
    """
    복잡도에 따라 생성할 최대 토큰 수를 조정합니다.
    
    Args:
        complexity: 입력 텍스트의 복잡도
        
    Returns:
        int: 조정된 최대 토큰 수
    """
    complexity_map = {
        "low": 100,
        "medium": 250, 
        "high": 500
    }
    return complexity_map.get(complexity, 250)
```

#### 응답 생성 메서드

##### generate_response() - v1.0.0
동기식 응답 생성 메서드입니다.

**생성 파라미터:**
- Temperature: 0.64 (창의성과 일관성의 균형)
- Top-k: 51 (상위 51개 토큰 후보 고려)
- Top-p: 0.63 (누적 확률 63%까지 고려)
- Repetition Penalty: 1.21 (반복 억제)

```python
def generate_response(self, input_text: str) -> str:
    """
    입력 텍스트에 대해 Llama 모델을 사용하여 응답을 생성합니다.
    
    Args:
        input_text: 사용자 입력 텍스트
        
    Returns:
        str: 생성된 응답 텍스트
    """
    # 복잡도 분석 및 토큰 수 조정
    complexity = self.analyze_complexity(input_text)
    max_new_tokens = self.adjust_max_tokens(complexity)

    # 토크나이징
    input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
    attention_mask = (input_ids != self.tokenizer.pad_token_id).long()

    # 모델 추론
    with autocast(dtype=torch.float16):
        with torch.no_grad():
            output = self.model.generate(
                input_ids.to(self.device_2080),
                attention_mask=attention_mask.to(self.device_2080),
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.64,
                top_k=51,
                top_p=0.63,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.21,
            )
    
    # 디코딩 및 반환
    response = self.tokenizer.decode(output[0], skip_special_tokens=True)
    return response
```

##### generate_response_stream() - v1.0.2
스트리밍 응답 생성 메서드입니다. 실시간으로 텍스트를 생성하여 반환합니다.

```python
def generate_response_stream(self, input_text: str):
    """
    입력 텍스트에 대해 스트리밍 방식으로 응답을 생성합니다.
    
    Args:
        input_text: 사용자 입력 텍스트
        
    Yields:
        str: 생성되는 텍스트 조각들
    """
    # 복잡도 분석 및 토큰 수 조정
    complexity = self.analyze_complexity(input_text)
    max_new_tokens = self.adjust_max_tokens(complexity)

    # 토크나이징
    input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
    attention_mask = (input_ids != self.tokenizer.pad_token_id).long()

    # 스트리머 설정
    streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
    
    # 비동기 모델 실행을 위한 스레드 생성
    generation_kwargs = {
        "input_ids": input_ids.to(self.device_2080),
        "attention_mask": attention_mask.to(self.device_2080),
        "max_new_tokens": max_new_tokens,
        "do_sample": True,
        "temperature": 0.64,
        "top_k": 51,
        "top_p": 0.63,
        "eos_token_id": self.tokenizer.eos_token_id,
        "pad_token_id": self.tokenizer.eos_token_id,
        "repetition_penalty": 1.21,
        "streamer": streamer
    }

    thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
    thread.start()

    # 스트리밍 텍스트 반환
    for new_text in streamer:
        yield new_text
```

### 3. 예외 처리 컴포넌트 (Error_handlers.py)

#### 예외 클래스 계층구조
시스템에서 발생할 수 있는 모든 HTTP 예외를 체계적으로 관리합니다.

| 예외 클래스 | HTTP 코드 | 설명 | 사용 시점 |
|-------------|-----------|------|-----------|
| `NotFoundException` | 404 | 리소스 없음 | 요청한 리소스를 찾을 수 없음 |
| `BadRequestException` | 400 | 잘못된 요청 | 클라이언트 요청 형식 오류 |
| `UnauthorizedException` | 401 | 인증 필요 | 인증되지 않은 접근 |
| `ForbiddenException` | 403 | 접근 거부 | 권한 부족 |
| `ValueErrorException` | 422 | 유효성 검사 실패 | 입력값 형식/타입 오류 |
| `InternalServerErrorException` | 500 | 서버 내부 오류 | 예상치 못한 서버 오류 |
| `DatabaseErrorException` | 503 | 서비스 불가 | 데이터베이스 연결 실패 |
| `IPRestrictedException` | 403 | IP 차단 | 허용되지 않은 IP 접근 |
| `MethodNotAllowedException` | 405 | 메서드 불허 | 지원하지 않는 HTTP 메서드 |

#### 통합 예외 처리기

모든 HTTP 예외를 중앙에서 처리하고 로깅하는 통합 핸들러입니다.

**기능:**
- 예외 정보의 구조화된 로깅
- 요청 컨텍스트 정보 수집
- 표준화된 에러 응답 생성

```python
async def generic_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    FastAPI 애플리케이션에서 발생한 모든 HTTPException을 통합 처리합니다.
    
    Args:
        request: FastAPI 요청 객체
        exc: 발생한 HTTP 예외
        
    Returns:
        JSONResponse: 표준화된 에러 응답
    """
    # 요청 본문 추출
    body = await request.body()

    # 로그 데이터 구성
    log_data = {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers),
        "body": body.decode("utf-8") if body else "",
        "exception_class": exc.__class__.__name__,
        "detail": exc.detail
    }

    # 에러 로깅
    error_message = f"{exc.status_code} - {exc.detail}"
    logger.error(f"{error_message} | URL: {log_data['url']} | Method: {log_data['method']}")

    # 핸들러 확인 및 응답 생성
    handler = exception_handlers.get(type(exc), None)
    if handler:
        return handler(request, exc)
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred."},
        )
```

#### 예외 핸들러 등록기

```python
def add_exception_handlers(app: FastAPI):
    """
    FastAPI 애플리케이션에 모든 예외 핸들러를 등록합니다.
    
    Args:
        app: FastAPI 애플리케이션 인스턴스
    """
    for exc_type in exception_handlers:
        app.add_exception_handler(exc_type, generic_exception_handler)
```

### 4. 데이터 모델 컴포넌트 (Models.py)

#### Pydantic 모델 스키마
API 요청/응답을 위한 데이터 검증 및 직렬화를 담당합니다.

##### 요청 모델 (Llama_Request)
사용자 입력을 검증하고 구조화합니다.

**필드 제약사항:**
- 최소 길이: 1자
- 최대 길이: 500자
- 타입: 문자열 (필수)

```python
class Llama_Request(BaseModel):
    """
    Llama 모델 API 요청을 위한 데이터 모델
    
    Attributes:
        input_data: 사용자 입력 텍스트 (1-500자)
    """
    input_data: str = Field(
        examples=["Llama AI 모델의 출시일과 버전들을 각각 알려줘."],
        title="사용자 입력 문장",
        min_length=1, 
        max_length=500,
        description="사용자 입력 문장 길이 제약"
    )
```

##### 응답 모델 (Llama_Response)
AI 생성 텍스트를 구조화하여 반환합니다.

```python
class Llama_Response(BaseModel):
    """
    Llama 모델 API 응답을 위한 데이터 모델
    
    Attributes:
        output_data: AI가 생성한 응답 텍스트
    """
    output_data: str = Field(
        examples=["""
        물론이죠! Llama AI 모델의 출시일과 버전들은 다음과 같습니다:

        1. Llama 1: 2023년 출시
        2. Llama 2: 2024년 6월 1일 출시  
        3. Llama 3: 2024년 7월 23일 출시
        4. Llama 3.1: 2024년 7월 24일 출시

        이 모델들은 Meta (구 Facebook)에서 개발한 AI 모델입니다.
        각 버전마다 성능과 기능이 개선되었습니다. 더 궁금한 점이 있으신가요?
        """],
        title="Llama 답변"
    )
```

## 버전별 변경사항

### v1.0.0 (2024-10-19)
**초기 릴리즈**
- Llama 3.1 8B 모델 통합
- 듀얼 GPU 지원 (RTX 2080 + GTX 1050)
- 복잡도 기반 적응형 토큰 할당
- 기본 동기식 응답 생성
- 포괄적인 예외 처리 시스템
- RESTful API 구현

### v1.0.1 (2024-10-20)  
**안정성 개선**
- 메모리 누수 방지
- 에러 핸들링 강화
- 로깅 시스템 개선
- 성능 최적화

### v1.0.2 (2024-10-22)
**스트리밍 지원 추가**
- `generate_response_stream()` 메서드 구현
- 실시간 텍스트 스트리밍
- 비동기 처리 개선
- 사용자 경험 향상

## 성능 특성

### 메모리 사용량
- **기본 메모리**: ~12GB VRAM (RTX 2080)
- **보조 메모리**: ~2GB VRAM (GTX 1050)  
- **시스템 RAM**: ~8GB

### 처리량
- **동시 요청**: 1개 (단일 GPU 모델 특성)
- **시간당 요청**: ~300-500개 (복잡도에 따라 변동)

## 운영 가이드

### 환경 설정
1. `.env` 파일에 `HUGGING_FACE_TOKEN` 설정
2. CUDA 환경 구성 확인
3. 필요한 Python 패키지 설치

### 모니터링 포인트
- GPU 메모리 사용률
- 응답 시간 분포
- 에러 발생률
- 복잡도 분석 정확도

### 문제 해결
- **메모리 부족**: 배치 크기 조정 또는 모델 양자화 레벨 증가
- **응답 지연**: 복잡도 임계값 조정
- **품질 저하**: 생성 파라미터 튜닝

## 보안 고려사항

### 입력 검증
- 문자열 길이 제한 (1-500자)
- 악성 코드 패턴 필터링
- 입력 형식 검증

### 에러 정보 보호
- 상세 에러 정보 로그로만 기록
- 클라이언트에게는 일반화된 에러 메시지 반환
- 시스템 정보 노출 방지
