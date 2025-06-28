# ChatBot AI - 버전 명세서 v1.3.x

## 개요
이 문서는 ChatBot AI 시스템의 v1.3.x 계열 버전에 대한 공식 명세서입니다. v1.2.x의 GGUF 기반 하이브리드 시스템에서 **완전한 GGUF 기반 아키텍처**로 전환되었으며, **DuckDuckGo 검색 연동**, **모듈화된 구조**, **JSON 응답 시스템**을 도입한 차세대 AI 챗봇 서비스입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.3.0** | 2025-02-18 | `a1a8067b5175df55789daab8dcf250c95e6d2932` | Stable |
| **v1.3.1** | 2025-02-18 | `be178f1d87d1508284a425cb3094402804c593b0` | Latest |
| **None** | 2025-03-15 | `6d78b2bfcb9d13aad2766baa30acd684da81f973` | Unstable |

## v1.2.x에서 v1.3.x로의 주요 변경사항

### 아키텍처 혁신
- **Transformers + GGUF 하이브리드** → **완전한 GGUF 기반** 시스템
- **Llama Transformers 모델 제거** → **Bllossom GGUF 모델 추가**
- **Lumimaid 8B** → **3개 GGUF 모델 지원** (Llama, Lumimaid, Bllossom)

### 인프라 변화
- **MongoDB 컨테이너** → **로컬 MongoDB 연동**
- **Docker 의존성 완전 제거**
- **모듈화된 패키지 구조** 도입

### 신규 기능
- **DuckDuckGo 검색 API** 통합 (Google 검색 대체)
- **JSON 응답 시스템** (SSE 스트리밍과 병행)
- **대화 기록 관리** (MongoDB 기반)
- **깊은 번역기** (deep-translator) 지원
- **향상된 에러 처리** 및 로깅 시스템

### 제거된 기능
- ❌ **Transformers 기반 Llama 모델**
- ❌ **Google Search API** 연동
- ❌ **Docker 컨테이너** 환경
- ❌ **MongoDB 라우터** 독립 엔드포인트

## 시스템 요구사항

### 하드웨어 요구사항
- **GPU**: NVIDIA RTX 3060 (CUDA:0) + RTX 2080 (CUDA:1)
- **VRAM**: 최소 20GB RAM (3060 12GB + 2080 8GB)
- **저장공간**: 최소 50GB 여유 공간

### 소프트웨어 요구사항
- **운영체체**: Windows 10/11 (64-bit)
- **Python**: 3.11 이상
- **CUDA**: 11.8/12.8 지원
- **llama-cpp-python**: CUDA 지원 버전
- **MongoDB**: 로컬 설치

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot AI v1.3.x
├── 📁 fastapi/
│   ├── 📁 ai_model/              # GGUF 모델 저장소
│   │   ├── llama-3-Korean-Bllossom-8B-gguf-Q4_K_M.gguf [NEW]
│   │   ├── v2-Llama-3-Lumimaid-8B-v0.1-OAS-Q5_K_S-imat.gguf
│   │   └── README.md [UPDATED]
│   ├── 📁 src/
│   │   ├── 📁 utils/             # 모듈화된 유틸리티
│   │   │   ├── 📁 ai_models/     # AI 모델 모듈 [NEW]
│   │   │   │   ├── bllossom_model.py [NEW]
│   │   │   │   ├── lumimaid_model.py [RENAMED]
│   │   │   │   └── llama_model.py [RENAMED]
│   │   │   ├── 📁 handlers/      # 핸들러 모듈 [NEW]
│   │   │   │   ├── error_handler.py [NEW]
│   │   │   │   ├── language_handler.py [NEW]
│   │   │   │   └── mongodb_handler.py [NEW]
│   │   │   ├── 📁 schemas/       # 스키마 모듈 [NEW]
│   │   │   │   └── chat_schema.py [NEW]
│   │   │   ├── 📁 services/      # 서비스 모듈 [NEW]
│   │   │   │   └── search_service.py [NEW]
│   │   │   └── __init__.py [UPDATED]
│   │   ├── server.py [UPDATED]
│   │   ├── bot.yaml
│   │   └── index.html [UPDATED]
│   ├── requirements_llama.txt    # llama.cpp 관련 패키지
│   └── requirements.txt [UPDATED]
├── 📁 models/                    # 모델 설정 파일 [NEW]
│   └── config-Bllossom.json [NEW]
└── .env
```

## API 명세

### 엔드포인트

#### POST /office_stream
Bllossom 모델 기반 DuckDuckGo 검색 연동 JSON 응답

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
- **Response**: `{"response": "string"}`

#### POST /character_stream
Lumimaid 모델 기반 캐릭터 대화 JSON 응답

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
  "input_data": "*I approach Rachel and talk to her.*",
  "character_name": "Rachel",
  "greeting": "*Rachel stands nervously at the lectern...*",
  "context": "Rachel is a devout Catholic girl...",
  "db_id": "b440780c-cbaa-454f-a8d2-cf884786d89f",
  "user_id": "djjdjs74"
}
```

#### SSE 스트리밍 엔드포인트

##### POST /office_sse
Bllossom 모델 SSE 스트리밍 응답

##### POST /character_sse
Lumimaid 모델 SSE 스트리밍 응답

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. 서버 컴포넌트 (server.py) - v1.3.x 완전 재설계

#### 완전한 GGUF 기반 아키텍처
v1.2.x의 하이브리드 시스템에서 **순수 GGUF 기반**으로 전환되었습니다.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI AI 모델 애플리케이션 초기화 - v1.3.x
    완전한 GGUF 기반 시스템 (Bllossom + Lumimaid)
    """
    global Bllossom_model, Lumimaid_model, GREEN, RESET

    def get_cuda_device_info(device_id: int) -> str:
        device_name = torch.cuda.get_device_name(device_id)
        device_properties = torch.cuda.get_device_properties(device_id)
        total_memory = device_properties.total_memory / (1024 ** 3)
        return f"Device {device_id}: {device_name} (Total Memory: {total_memory:.2f} GB)"

    try:
        # 완전한 GGUF 모델 시스템
        Bllossom_model = Bllossom()  # cuda:1 (RTX 2080)
        Lumimaid_model = Lumimaid()  # cuda:0 (RTX 3060)
    except ChatError.InternalServerErrorException as e:
        print(f"{RED}ERROR{RESET}: 모델 초기화 중 오류 발생: {str(e)}")
        exit(1)
        
    # 디버깅용 출력
    Bllossom_device_info = get_cuda_device_info(1)
    Lumimaid_device_info = get_cuda_device_info(0)
    print(f"{GREEN}INFO{RESET}: Bllossom 모델 로드 완료 ({Bllossom_device_info})")
    print(f"{GREEN}INFO{RESET}: Lumimaid 모델 로드 완료 ({Lumimaid_device_info})")

    yield

    Bllossom_model = None
    Lumimaid_model = None
    print(f"{GREEN}INFO{RESET}: 모델 해제 완료")
```

#### JSON 응답 시스템
스트리밍 대신 JSON 응답을 기본으로 하는 새로운 API 구조입니다.

```python
@app.post("/office_stream", summary="AI 모델이 검색 결과를 활용하여 Bllossom 모델 답변 생성")
async def office_stream(request: ChatModel.Bllossom_Request):
    """
    Bllossom_8B 모델에 질문을 DuckDuckGo 검색 결과와 결합하여 JSON 응답으로 반환합니다.
    """
    try:
        chat_list = await mongo_handler.get_office_log(
            user_id=request.user_id,
            document_id=request.db_id,
            router="office",
        )
        search_context = ""
        
        # DuckDuckGo 검색 연동
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
                print(f"{RED}ERROR{RESET}: DuckDuckGo 검색 실패")
                search_context = ""
                
        # JSON 응답 생성
        full_response = ""
        for chunk in Bllossom_model.generate_response_stream(
            input_text=request.input_data,
            search_text=search_context,
            chat_list=chat_list,
        ):
            full_response += chunk
            
        return full_response
    
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail="내부 서버 오류가 발생했습니다.")
```

### 2. AI 모델 컴포넌트 - v1.3.x 모듈화

#### BllossomChatModel 클래스 (bllossom_model.py) - 신규 추가

**주요 특징:**
- **모델**: `llama-3-Korean-Bllossom-8B-gguf-Q4_K_M.gguf`
- **엔진**: llama-cpp-cuda (CUDA 지원)
- **GPU**: CUDA:1 (RTX 2080) 전용
- **양자화**: Q4_K_M (고효율 4-bit 양자화)
- **검색 연동**: DuckDuckGo 검색 결과 처리

```python
class BllossomChatModel:
    """
    GGUF 포맷으로 경량화된 Llama-3-Bllossom-8B 모델을 로드하고, 
    주어진 입력 프롬프트에 대한 응답을 생성하는 클래스입니다.
    """
    def __init__(self) -> None:
        """
        GGUF 모델 초기화 - RTX 2080 최적화
        """
        self.model_path = "fastapi/ai_model/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M.gguf"
        self.verbose = False
        self.gpu_layers = 50
        self.model = self._load_model()
        self.response_queue = Queue()

    def _load_model(self) -> Llama:
        """
        Llama 모델을 CUDA:1 디바이스(RTX 2080)에 로드
        """
        print("GGUF Bllossom 모델 로드 중...")
        try:
            model = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.gpu_layers,
                main_gpu=1,                # RTX 2080 사용
                n_ctx=4096,                # 컨텍스트 길이 증가
                n_batch=512,
                verbose=self.verbose,
                offload_kqv=True,
                use_mmap=False,
                use_mlock=True,
                n_threads=8
            )
            print("✅ GGUF Bllossom 모델이 CUDA:1 (RTX 2080)에 성공적으로 로드되었습니다.")
            return model
        except Exception as e:
            print(f"❌ GGUF Bllossom 모델 로드 중 오류 발생: {e}")
            raise
```

#### LumimaidChatModel 클래스 (lumimaid_model.py) - v1.3.x 업데이트

**v1.2.x에서 변경된 사항:**
- ✅ **GPU 할당 변경** (CUDA:1 → CUDA:0)
- ✅ **대화 기록 관리** 통합
- ✅ **모듈화된 구조** 적용

```python
def generate_response_stream(self, input_text: str, character_settings: dict = None, chat_list: List[Dict] = None) -> Generator[str, None, None]:
    """
    캐릭터 설정과 대화 기록을 반영한 스트리밍 응답 생성 - v1.3.x
    
    Args:
        input_text (str): 사용자 입력 텍스트
        character_settings (dict): 캐릭터 설정 딕셔너리
        chat_list (List[Dict]): 이전 대화 기록
        
    Yields:
        str: 생성된 텍스트 조각들
    """
    try:
        # 캐릭터 정보 및 대화 기록 설정
        if character_settings:
            character_info = CharacterPrompt(
                name=character_settings.get("character_name", "Assistant"),
                context=character_settings.get("context", ""),
                search_text=""
            )
            # Llama3 messages 형식으로 변환 (대화 기록 포함)
            messages = build_llama3_messages(character_info, input_text, chat_list)
        else:
            messages = [{"role": "user", "content": input_text}]
        
        # 스트리밍 응답 생성
        for text_chunk in self.create_streaming_completion(
            messages=messages,
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

### 3. 검색 서비스 컴포넌트 (search_service.py) - 신규 추가

#### DuckDuckGo 검색 연동
Google Search API를 대체하는 DuckDuckGo 검색 시스템입니다.

**주요 특징:**
- **라이브러리**: langchain-community
- **검색 엔진**: DuckDuckGo API
- **필터링**: 도메인별 결과 분류
- **제한 없음**: API 키 불필요

```python
async def fetch_duck_search_results(query: str) -> list:
    """
    DuckDuckGo를 사용하여 웹 검색을 수행하고 결과를 반환합니다.
    
    Args:
        query (str): 검색어
        
    Returns:
        list: 검색 결과 리스트 (제목, 내용, 링크 포함)
        
    Raises:
        Exception: 검색 실패 시 예외 발생
    """
    try:
        # 검색 래퍼 설정
        wrapper = DuckDuckGoSearchAPIWrapper(
            region="kr-kr",
            safesearch="moderate",
            max_results=50,
            time="y",  # 1년 이내 결과
            backend="auto"
        )
        
        # 검색 도구 설정
        search = DuckDuckGoSearchResults(
            api_wrapper=wrapper,
            num_results=20,
            output_format="json",
            backend="text"
        )
        
        # 검색 수행
        result = search.invoke(query)
        search_results = json.loads(result)
        
        # 결과 포맷팅
        formatted_results = []
        for item in search_results:
            formatted_results.append({
                "title": item.get('title', 'N/A'),
                "snippet": item.get('snippet', 'N/A'),
                "link": item.get('link', 'N/A')
            })
            
        return formatted_results
        
    except Exception as e:
        print(f"{RED}ERROR{RESET}: DuckDuckGo 검색 중 오류 발생: {e}")
        return []
```

### 4. 데이터베이스 컴포넌트 (mongodb_handler.py) - v1.3.x 확장

#### 대화 기록 관리 시스템
MongoDB 기반의 대화 기록 저장 및 검색 시스템입니다.

```python
async def get_office_log(self, user_id: str, document_id: str, router: str) -> List[Dict]:
    """
    Office 라우터의 대화 기록을 가져옵니다.
    
    Args:
        user_id (str): 사용자 ID
        document_id (str): 문서 ID
        router (str): 라우터 타입
        
    Returns:
        List[Dict]: 대화 기록 리스트
    """
    try:
        collection = self.db["chat_logs"]
        
        # 최근 10개 대화 기록 조회
        cursor = collection.find({
            "user_id": user_id,
            "document_id": document_id,
            "router": router
        }).sort("timestamp", -1).limit(10)
        
        chat_logs = await cursor.to_list(length=10)
        
        # 시간순 정렬 (오래된 것부터)
        chat_logs.reverse()
        
        return chat_logs
        
    except Exception as e:
        print(f"{self.RED}ERROR{self.RESET}: 대화 기록 조회 중 오류 발생: {e}")
        return []

async def get_character_log(self, user_id: str, document_id: str, router: str) -> List[Dict]:
    """
    Character 라우터의 대화 기록을 가져옵니다.
    """
    # office_log와 동일한 로직
    return await self.get_office_log(user_id, document_id, router)
```

### 5. 데이터 모델 컴포넌트 (chat_schema.py) - v1.3.x 간소화

#### 통합된 요청/응답 모델
v1.2.x의 복잡한 모델 구조를 간소화하고 통합했습니다.

**신규 필드:**
- ✅ `db_id` (데이터베이스 문서 ID)
- ✅ `user_id` (사용자 식별자)

**제거된 필드:**
- ❌ `image` (캐릭터 이미지 URL 제거)
- ❌ `access_level` (접근 권한 단순화)

```python
class Bllossom_Request(BaseModel):
    """
    Bllossom 모델 API 요청 - v1.3.x 업데이트
    DuckDuckGo 검색과 대화 기록을 지원하는 요청 모델
    """
    input_data: str = Bllossom_input_data_set
    google_access: bool = google_access_set
    db_id: str | None = db_id_set
    user_id: str | None = user_id_set

class Lumimaid_Request(BaseModel):
    """
    Lumimaid 모델 API 요청 - v1.3.x 업데이트
    캐릭터 기반 대화와 대화 기록을 지원하는 요청 모델
    """
    input_data: str = Lumimaid_input_data_set
    character_name: str = character_name_set
    greeting: str = greeting_set
    context: str = context_set
    db_id: str | None = db_id_set
    user_id: str | None = user_id_set
```

## 설치 및 설정

### 환경 설정 시스템 - v1.3.x 개선

#### 통합된 환경 구성
Windows 환경에서 CUDA 11.8과 12.8을 동시 지원하는 개선된 설치 가이드입니다.

**CUDA 환경 설정:**
- **CUDA 11.8**: PyTorch 및 기본 모델용
- **CUDA 12.8**: llama-cpp-python 최적화용

**필수 패키지:**
```bash
# 기본 패키지
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# GGUF 지원
pip install llama-cpp-python[cuda]

# 검색 및 번역
pip install duckduckgo-search langchain-community deep-translator

# 자연어 처리
pip install spacy sentence-transformers
```

### 로컬 MongoDB 설정
Docker 의존성을 제거하고 로컬 MongoDB 설치를 권장합니다.

```yaml
# MongoDB 설정 예시
database:
  host: localhost
  port: 27017
  name: chatbot_db
  collections:
    - chat_logs
    - user_profiles
    - character_configs
```

## 성능 특성

### 메모리 사용량
- **Bllossom (GGUF)**: ~8GB VRAM (RTX 2080)
- **Lumimaid (GGUF)**: ~6GB VRAM (RTX 3060)
- **MongoDB**: ~512MB RAM
- **시스템 RAM**: ~6-8GB

### 처리량
- **동시 요청**: 2개 (완전한 GGUF 분산 처리)
- **시간당 요청**: ~400-600개
- **GGUF 성능**: v1.2.x 대비 15-25% 향상
- **JSON 응답**: 스트리밍 대비 30% 빠른 응답

## 운영 가이드

### 환경 설정
1. **Windows 11** + **Python 3.11** 환경 구성
2. **CUDA 11.8/12.8** 드라이버 설치
3. **로컬 MongoDB** 설치 및 구성
4. **GGUF 모델** 다운로드 및 배치

### 문제 해결
- **GGUF 로딩 실패**: GPU 메모리 할당 확인
- **DuckDuckGo 검색 실패**: 네트워크 연결 및 속도 제한 확인
- **MongoDB 연결 오류**: 로컬 MongoDB 서비스 상태 확인
- **대화 기록 손실**: 컬렉션 인덱스 및 권한 확인

### 성능 튜닝
1. **GGUF 파라미터** 최적화
   - `n_gpu_layers`: 50 (Bllossom) / 35 (Lumimaid)
   - `n_ctx`: 4096 (긴 대화 지원)
   - `n_batch`: 512 → 1024 (처리량 향상)

2. **MongoDB 최적화**
   - 대화 기록 TTL 인덱스 설정
   - 사용자별 샤딩 구성
   - 캐시 크기 조정

3. **검색 시스템 최적화**
   - DuckDuckGo 결과 캐싱
   - 검색어 전처리 및 필터링
   - 결과 수 제한 (10-20개)

## 보안 고려사항

### 확장된 보안 기능
- **로컬 MongoDB**: 인증 및 권한 관리
- **GGUF 모델 검증**: 파일 무결성 확인
- **DuckDuckGo 제한**: 검색 쿼리 필터링

### API 보안 강화
- **사용자 인증**: user_id 기반 접근 제어
- **대화 기록 보호**: 사용자별 격리
- **검색 제한**: 악성 쿼리 방지
- **JSON 응답**: XSS 및 인젝션 방지

## 버전 호환성

### v1.2.x와의 차이점

| 기능 | v1.2.x | v1.3.x |
|------|--------|--------|
| **모델 아키텍처** | Transformers + GGUF | 완전한 GGUF |
| **검색 엔진** | Google Search API | DuckDuckGo |
| **응답 형식** | 스트리밍 전용 | JSON + SSE |
| **대화 기록** | ❌ 없음 | ✅ MongoDB 기반 |
| **모듈 구조** | 단일 파일 | 모듈화된 패키지 |
| **번역 시스템** | googletrans | deep-translator |
| **환경** | 로컬 + Docker | 완전한 로컬 |

## 라이선스
이 소프트웨어는 다음 라이선스를 준수합니다:
- **Meta Llama 3.1**: Meta의 Llama 모델 라이선스
- **Lumimaid 8B**: Lewdiculous 모델 라이선스
- **Korean Bllossom 8B**: MLP-KTLim 모델 라이선스
- **llama.cpp**: MIT 라이선스
- **DuckDuckGo**: 공개 검색 API