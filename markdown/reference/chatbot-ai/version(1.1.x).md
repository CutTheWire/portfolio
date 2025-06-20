# 📌 버전 히스토리

| 버전      | 날짜                                   | 커밋 해시                                 |
|-----------|----------------------------------------|-------------------------------------------|
| **v1.1.0**| 2025-01-15 (수) 15:40:49 (KST)         | `d014744640fa72366c398541ec9f5b4c7361fd7f`|


# 🗂️ 주요 파일 구조
```
📦src
 ┣ 📂log
 ┣ 📂utils
 ┃ ┣ 📜AI_Bllossom_8B.py
 ┃ ┣ 📜AI_Llama_8B.py
 ┃ ┣ 📜BaseModels.py
 ┃ ┣ 📜Error_handlers.py
 ┃ ┗ 📜__init__.py
 ┣ 📜bot.yaml
 ┣ 📜index.html
 ┗ 📜server.py
```

# 📄 `__init__.py`
## 📌 패키지
|패키지 명칭|설명|
|:-----:|:-----|
|`utils`|AI 모델, 예외 처리, 언어 처리 등을 포함하는 유틸리티 패키지|

## 📌 모듈
|모듈 명칭|별칭|설명|
|:-----:|:-----:|:-----|
|`AI_Bllossom_8B`|`Bllossom_8B`|Bllossom 8B 모델을 사용하여 대화를 생성하는 BllossomChatModel 클래스를 정의|
|`AI_Llama_8B`|`Llama_8B`|Llama 8B 모델을 사용하여 대화를 생성하는 LlamaChatModel 클래스를 정의|
|`BaseModels`|`ChatModel`|FastAPI 애플리케이션에서 사용되는 Pydantic 모델을 정의|
|`Error_handlers`|`ChatError`|FastAPI 애플리케이션에서 발생하는 예외를 처리하는 모듈|
|`Language_handler`|`LanguageProcessor`|자연어 처리를 위한 LanguageProcessor 클래스를 정의|

# 📄 `server.py`
## 📌 Lifespan 컨텍스트 매니저
> FastAPI 애플리케이션의 시작과 종료 시점에 실행되는 코드를 정의하는 데 사용됩니다. 이 예제에서는 Llama 모델을 초기화하고 종료할 때 필요한 리소스를 관리합니다.

```python
from utils import Llama_8B, Bllossom_8B

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    FastAPI AI 모델 애플리케이션 초기화
    '''
    global llama_model_8b, bllossom_model_8b

    def get_cuda_device_info(device_id: int) -> str:
        device_name = torch.cuda.get_device_name(device_id)
        device_properties = torch.cuda.get_device_properties(device_id)
        total_memory = device_properties.total_memory / (1024 ** 3)
        return f"Device {device_id}: {device_name} (Total Memory: {total_memory:.2f} GB)"

    llama_model_8b = Llama_8B()
    bllossom_model_8b = Bllossom_8B()

    llama_device_info = get_cuda_device_info(0)
    bllossom_device_info = get_cuda_device_info(1)

    print(f"Llama 모델 로드 완료 ({llama_device_info})")
    print(f"Bllossom 모델 로드 완료 ({bllossom_device_info})")

    yield

    llama_model_8b = None
    bllossom_model_8b = None
    print("모델 해제 완료")
```

## 📌 API
|API 명칭|설명|
|:-----:|:-----|
|`/Llama_stream`|Llama 모델에 대한 요청을 처리하는 API 엔드포인트|
|`/Bllossom_stream`|Bllossom 모델에 대한 요청을 처리하는 API 엔드포인트|

```python
@app.post("/Llama_stream", summary="AI 모델이 검색 결과를 활용하여 답변 생성")
async def Llama_stream(request: ChatModel.Llama_Request):
    """
    사용자 질문과 위키백과, 나무위키, 뉴스 결과를 결합하여 AI 답변을 생성합니다.
    :param request: 사용자 질문과 옵션 포함
    :return: AI 모델의 답변
    """
    print(f"Request: {request}")
    try:
        search_context = ""

        if request.google_access:
            search_results = await fetch_search_results(request.input_data, num_results=5)

            if search_results:
                search_context = "\n".join([
                    f"제목: {item['title']}\n설명: {item['snippet']}\n링크: {item['link']}"
                    for item in search_results[:5]
                ])
            else:
                search_context = ""
        
        print(f"Search Context: {search_context}")

        prompt = (
            f"사용자 질문은 {request.input_data}\n\n"
            f"참고 정보는 {search_context}\n\n"
        )

        response_stream = llama_model_8b.generate_response_stream(input_text=prompt)
        return StreamingResponse(response_stream, media_type="text/plain")

    except TimeoutError:
        raise ChatError.InternalServerErrorException(detail="모델 응답이 시간 초과되었습니다.")
    except Exception as e:
        print(f"Unhandled Exception: {e}")
        raise ChatError.InternalServerErrorException(detail=str(e))

@app.post("/Bllossom_stream", summary="스트리밍 방식으로 Bllossom_8B 모델 답변 생성")
async def bllossom_stream(request: ChatModel.Bllossom_Request):
    '''
    Bllossom_8B 모델에 질문 입력 시 캐릭터 설정을 반영하여 답변을 스트리밍 방식으로 반환
    '''
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
    except TimeoutError:
        raise ChatError.InternalServerErrorException(detail="Bllossom 모델 응답이 시간 초과되었습니다.")
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unhandled Exception: {e}")
        raise ChatError.InternalServerErrorException(detail=str(e))
```

---

# 📄 `AI_Llama_8B.py`

## 📌 클래스

|클래스 명칭|설명|
|:-----:|:-----|
|`LlamaChatModel`|Llama 모델을 GPU에 할당하여 질의응답 하도록 처리하는 클래스|

## 📌 함수/메서드

- `__init__`
    > 클래스 초기화 메서드, Llama 모델의 파일 주소와 GPU 0에 모델을 할당하여 변수를 초기화, 토크나이저와 GPU의 파이프라인 로드, 모델의 옵티마이저를 준비하는 과정을 처리하는 메서드

    ```python
    def __init__(self):
        '''
        LlamaChatModel 클래스 초기화
        '''
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        dotenv_path = os.path.join(parent_dir, '.env')
        load_dotenv(dotenv_path)
        self.cache_dir = "/app/ai_model/"
        self.model_id = "meta-llama/Llama-3.1-8B-Instruct"
        self.device = torch.device("cuda:0")

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

        self.hf_token = os.getenv("HUGGING_FACE_TOKEN")
        self.accelerator = Accelerator(mixed_precision="fp16", device_placement=False)
        self.scaler = GradScaler()

        print("토크나이저 로드 중...")
        self.tokenizer = self.load_tokenizer()
        print("모델 로드 중...")
        self.model = self.load_model()
        print("모델과 토크나이저 로드 완료!")
        
        self.model.gradient_checkpointing_enable()
        self.conversation_history = []
    ```

- `load_tokenizer`
    > `transformers.AutoTokenizer`에 Llama 모델(`self.model_id`)을 할당한 변수(`tokenizer`)를 반환

    ```python
    def load_tokenizer(self) -> transformers.PreTrainedTokenizerBase:
        '''
        토크나이저를 로드합니다.
        :return: 로드된 토크나이저
        '''
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_id,
            token=self.hf_token
        )
        if tokenizer.eos_token_id is None:
            tokenizer.add_special_tokens({'eos_token': '<|endoftext|>'})
        tokenizer.pad_token_id = tokenizer.eos_token_id
        return tokenizer
    ```

- `load_model`
    > `transformers.AutoModelForCausalLM`에 Llama 모델(`self.model_id`)을 할당한 변수(`model`)를 반환

    ```python
    def load_model(self) -> transformers.PreTrainedModel:
        '''
        Llama 모델을 로드합니다.
        :return: 로드된 Llama 모델
        '''
        model = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_id,
            cache_dir=self.cache_dir,
            token=self.hf_token,
            **self.model_kwargs
        )
        return model

    ```

- `generate_response_stream`
    > `input_text: str`를 메게변수로 받아와서 토크나이저로 인코딩하여 llama 모델에 설정 값들과 함께 전송, 받아온 문장을 디코딩하여 스트리밍으로 반환한다.
    ```python
    def generate_response_stream(self, input_text: str):
        """
        Llama 모델에 입력 텍스트를 전달하고, 생성된 응답을 스트리밍 방식으로 반환합니다.
        :param input_text: 사용자 입력 텍스트
        :return: 생성된 응답을 스트리밍으로 반환
        """
        input_ids = self.tokenizer.encode(
            text=input_text,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        attention_mask = (input_ids != self.tokenizer.pad_token_id).long().to(self.device)
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)

        generation_kwargs = {
            "input_ids": input_ids.to(self.device),
            "attention_mask": attention_mask.to(self.device),
            "min_new_tokens": 1,
            "max_new_tokens": 512,
            "do_sample": True,          # 샘플링 활성화
            "top_p": 0.9,               # Top-p Sampling 활성화 (0.9로 설정)
            "top_k": 0,                 # Top-k 비활성화 (Top-p와 함께 사용하지 않음)
            "temperature": 0.7,         # 다양성을 위한 온도 조정
            "eos_token_id": self.tokenizer.eos_token_id,
            "pad_token_id": (
                self.tokenizer.pad_token_id
                if self.tokenizer.pad_token_id is not None
                else self.tokenizer.eos_token_id
            ),
            "repetition_penalty": 1.2,  # 반복 방지 패널티
            "num_return_sequences": 1,  # 한 번에 하나의 시퀀스 생성
            "streamer": streamer        # 스트리밍을 위한 스트리머 설정
        }

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for new_text in streamer:
            yield new_text
    ```
---

# 📄 `Bllossom_8B.py`
## 📌 클래스
|클래스 명칭|설명|
|:-----:|:-----|
|`BllossomChatModel`|Bllossom 모델을 GPU에 할당하여 질의응답 하도록 처리하는 클래스|


## 📌 함수/메서드

- `__init__`
    > 클래스 초기화 메서드, Llama-Bllossom 모델의 파일 주소와 GPU 1에 모델을 할당하여 변수를 초기화, 토크나이저와 GPU의 파이프라인 로드, 모델의 옵티마이저를 준비하는 과정을 처리하는 메서드

    ```python
    def __init__(self):
        '''
        BllossomChatModel 클래스 초기화
        '''
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        dotenv_path = os.path.join(parent_dir, '.env')
        load_dotenv(dotenv_path)
        self.cache_dir = "/app/ai_model/"
        self.model_id = "MLP-KTLim/llama-3-Korean-Bllossom-8B"
        self.device = torch.device("cuda:1")

        self.model_kwargs = {
            "torch_dtype": torch.float16,
            "trust_remote_code": True,
            "device_map": {"": self.device},
            "quantization_config": BitsAndBytesConfig(load_in_4bit=True)
        }

        self.hf_token = os.getenv("HUGGING_FACE_TOKEN")
        self.accelerator = Accelerator(mixed_precision="fp16", device_placement=False)
        self.scaler = GradScaler()

        print("토크나이저 로드 중...")
        self.tokenizer = self.load_tokenizer()
        print("모델 로드 중...")
        self.model = self.load_model()
        print("모델과 토크나이저 로드 완료!")

        self.model.gradient_checkpointing_enable()
        self.conversation_history = []
    ```

- `load_tokenizer`
    > `transformers.AutoTokenizer`에 Llama 모델(`self.model_id`)을 할당한 변수(`tokenizer`)를 반환

    ```python
    def load_tokenizer(self) -> transformers.PreTrainedTokenizerBase:
        '''
        토크나이저를 로드합니다.
        :return: 로드된 토크나이저
        '''
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_id,
            token=self.hf_token
        )
        tokenizer.pad_token_id = tokenizer.eos_token_id
        return tokenizer
    ```

- `load_model`
    > `transformers.AutoModelForCausalLM`에 Llama 모델(`self.model_id`)을 할당한 변수(`model`)를 반환

    ```python
    def load_model(self) -> transformers.PreTrainedModel:
        '''
        Llama 모델을 로드합니다.
        :return: 로드된 Llama 모델
        '''
        model = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_id,
            cache_dir=self.cache_dir,
            token=self.hf_token,
            **self.model_kwargs
        )
        return model

    ```

- `generate_response_stream`
    > `input_text: str`를 메게변수로 받아와서 `_build_prompt`를 통해 `prompt`을 생성, 토크나이저로 인코딩하여 llama 모델에 설정 값들과 함께 전송, 받아온 문장을 디코딩하여 스트리밍으로 반환한다.
    ```python
    def generate_response_stream(self, input_text: str, character_settings: dict):
        prompt = self._build_prompt(input_text, character_settings)
        input_ids = self.tokenizer.encode(
            text=input_text,
            text_pair=prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        attention_mask = (input_ids != self.tokenizer.pad_token_id).long().to(self.device)
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)

        generation_kwargs = {
            "input_ids": input_ids.to(self.device),
            "attention_mask": attention_mask.to(self.device),
            "min_new_tokens": 1,
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.9,
            "eos_token_id": self.tokenizer.eos_token_id,
            "pad_token_id": self.tokenizer.eos_token_id,
            "repetition_penalty": 1.2,
            "streamer": streamer
        }

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for new_text in streamer:
            yield new_text
    ```

- `_build_prompt`
  - > Bllossom 모델의 캐릭터 설정을 반영하여 프롬프트를 생성하는 메서드로, 입력 텍스트와 캐릭터 설정을 기반으로 프롬프트를 구성합니다.

    ```python
    def _build_prompt(self, user_input: str, character_settings: dict):
        """
        대화 기록 기반으로 프롬프트 생성
        """
        recent_history = self.conversation_history[-5:]  # 최근 5개의 대화만 유지
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
            "부정 라벨:\n"
            "답변은 항상 한국어로 제공됩니다."
            "답변에서 max_new_tokens의 값을 다 채워서 답변 할 필요 없음."
            "'캐릭터 설정' 또는 설정 세부 정보는 응답에 포함되지 않아야 합니다."
            "자연스러운 대화형식으로 답변하십시오."
            "필요 이상의 반복을 피하십시오."
            "질문에 대해 적절히 응답하며, 대답이 없을 경우 '죄송합니다, 이 질문에 답변할 수 없습니다.'로 응답하십시오."
            f"대화 기록: {history}\n"
        )
        self.conversation_history.append({"role": "user", "content": user_input})
        return prompt
---

# 📄 `Error_handlers.py`
## 📌 클래스

|클래스 명칭|설명|
|:-----:|:-----|
|`NotFoundException`|HTTP 404 에러를 처리하는 예외 클래스. 요청한 리소스를 찾을 수 없을 때 발생|
|`BadRequestException`|HTTP 400 에러를 처리하는 예외 클래스. 클라이언트의 잘못된 요청으로 인해 발생|
|`UnauthorizedException`|HTTP 401 에러를 처리하는 예외 클래스. 인증되지 않은 사용자의 접근 시도 시 발생|
|`ForbiddenException`|HTTP 403 에러를 처리하는 예외 클래스. 권한이 없는 리소스에 대한 접근 시도 시 발생|
|`ValueErrorException`|HTTP 422 에러를 처리하는 예외 클래스. 입력값의 형식이나 타입이 올바르지 않을 때 발생|
|`InternalServerErrorException`|HTTP 500 에러를 처리하는 예외 클래스. 서버 내부에서 예상치 못한 오류가 발생했을 때 사용|
|`DatabaseErrorException`|HTTP 503 에러를 처리하는 예외 클래스. 데이터베이스 연결 실패나 쿼리 오류 등 DB 관련 문제 발생 시 사용|
|`IPRestrictedException`|HTTP 403 에러를 처리하는 예외 클래스. 허용되지 않은 IP 주소에서의 접근 시도 시 발생|
|`MethodNotAllowedException`|HTTP 405 에러를 처리하는 예외 클래스. 지원하지 않는 HTTP 메서드로 요청했을 때 발생|

## 📌 함수/메서드

- `generic_exception_handler`
    > FastAPI 애플리케이션에서 발생한 HTTPException을 처리하며, 요청 정보와 예외에 대한 세부 사항을 로그에 기록합니다.

    ```python
    async def generic_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """
        FastAPI 애플리케이션에서 발생한 HTTPException을 처리하며,
        요청 정보와 예외에 대한 세부 사항을 로그에 기록합니다.
        """
        handler = exception_handlers.get(type(exc), None)
        
        body = await request.body()

        log_data = {
            "url": str(request.url),
            "method": request.method,
            "headers": dict(request.headers),
            "body": body.decode("utf-8") if body else "",
            "exception_class": exc.__class__.__name__,
            "detail": exc.detail
        }

        error_message = f"{exc.status_code} - {exc.detail}"
        logger.error(f"{error_message} | URL: {log_data['url']} | Method: {log_data['method']}")

        if handler:
            return handler(request, exc)
        else:
            return JSONResponse(
                status_code=500,
                content={"detail": "An unexpected error occurred."},
            )
    ```

- `add_exception_handlers`
    > FastAPI 애플리케이션에 예외 핸들러를 추가하는 함수. 정의된 예외 타입과 관련된 핸들러를 FastAPI 애플리케이션에 등록합니다.

    ```python
    def add_exception_handlers(app: FastAPI):
        """
        FastAPI 애플리케이션에 예외 핸들러를 추가하는 함수.
        정의된 예외 타입과 관련된 핸들러를 FastAPI 애플리케이션에 등록합니다.
        """
        for exc_type in exception_handlers:
            app.add_exception_handler(exc_type, generic_exception_handler)
    ```

---

# 📄 `BaseModels.py`

## 📌 클래스
|클래스 명칭|설명|
|:-----:|:-----|
|`Validators`|URL 형식 검증 및 이미지 URL 연결 테스트를 위한 유틸리티 클래스|
|`Llama_Request`|Llama의 요청을 처리하는 Pydantic 모델. 입력 텍스트를 포함|
|`Llama_Response`|Llama의 응답을 처리하는 Pydantic 모델. 생성된 응답 텍스트를 포함|
|`Bllossom_Request`|Bllossom의 요청을 처리하는 Pydantic 모델. 입력 텍스트와 캐릭터 설정을 포함|
|`Bllossom_Response`|Bllossom의 응답을 처리하는 Pydantic 모델. 생성된 응답 텍스트를 포함|

## 📌 함수/필드
- `Validators`
    > URL 형식 검증 및 이미지 URL 연결 테스트를 위한 유틸리티 클래스
    ```python
    class Validators:
        @staticmethod
        def validate_URL(v: str) -> str:
            """
            URL 형식 검증 함수
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
            '''
            URL의 연결 테스트 함수
            '''
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.head(img_url, follow_redirects=True)
                if response.status_code != 200:
                    raise ValueError('이미지에 접근할 수 없습니다.')
            except httpx.RequestError:
                raise ValueError('이미지 URL에 접근하는 중 오류가 발생했습니다.')
    ```

- `Field`
    > Pydantic 모델 필드를 정의하는 데 사용되는 함수로, 각 필드의 예시, 제목, 설명, 길이 제약 등을 설정합니다.
    ```python
    input_data_set = Field(
        examples=["Llama AI 모델의 출시일과 버전들을 각각 알려줘."],
        title="사용자 입력 문장",
        description="사용자 입력 문장 길이 제약",
        min_length=1, max_length=500
    )

    google_access_set = Field(
        examples=[False, True],
        default=False,
        title="검색 기반 액세스",
        description="검색 기반 액세스 수준을 나타냅니다. True: 검색 기반 활성화. False: 검색 기반 제한됨."
    )

    NATURAL_NUM: int = conint(ge=1, le=10)  # 1~10 범위의 자연수

    character_name_set = Field(
        examples=["KindBot"],
        title="케릭터 이름",
        description="캐릭터의 이름입니다. 봇의 정체성을 나타내며, 사용자가 이 이름으로 봇을 부릅니다.",
        min_length=1
    )
    description_set = Field(
        examples=["친절한 도우미 봇"],
        title="케릭터 설명",
        description="캐릭터의 짧은 설명입니다. 이 봇의 성격이나 역할을 간략히 표현하며, 사용자에게 첫인상을 제공합니다.",
        min_length=1
    )
    greeting_set = Field(
        examples=["안녕하세요! 무엇을 도와드릴까요?"],
        title="케릭터 인사말",
        description="사용자가 봇과 상호작용을 시작할 때 표시되는 인사말입니다. 봇의 성격과 의도를 반영합니다.",
        min_length=1
    )
    image_set = Field(
        examples=["https://drive.google.com/thumbnail?id=12PqUS6bj4eAO_fLDaWQmoq94-771xfim"],
        title="케릭터 이미지 URL",
        description="URL의 최대 길이는 일반적으로 2048자",
        min_length=1, max_length=2048
    )
    character_setting_set = Field(
        examples=["친절하고 공손한 봇"],
        title="케릭터 설정 값",
        description="캐릭터의 성격이나 태도를 나타냅니다. 이는 봇이 대화에서 어떻게 행동하고 응답할지를 정의합니다.",
        min_length=1
    )
    tone_set = Field(
        examples=["공손한"],
        title="케릭터 말투",
        description="대화의 어조를 나타냅니다. 봇이 대화에서 사용하는 언어 스타일이나 태도입니다.",
        min_length=1
    )
    energy_level_set = Field(
        examples=[8],
        title="케릭터 에너지 ",
        description="봇의 에너지 수준을 나타내는 숫자입니다. 높은 값일수록 활기차고 적극적인 대화를 할 수 있음을 의미합니다. 1(매우 느긋함) ~ 10(매우 활기참)."
    )
    politeness_set = Field(
        examples=[10],
        title="케릭터 공손함",
        description="봇의 공손함을 나타내는 숫자입니다. 높은 값일수록 공손하고 존중하는 언어를 사용할 가능성이 높습니다. 1(직설적임) ~ 10(매우 공손함)"
    )
    humor_set = Field(
        examples=[5],
        title="케릭터 유머 감각",
        description="봇의 유머 감각의 정도를 나타냅니다. 숫자가 높을수록 대화에서 유머러스한 요소를 추가하려고 시도합니다. 1(유머 없음) ~ 10(매우 유머러스함)."
    )
    assertiveness_set = Field(
        examples=[3],
        title="케릭터 단호함",
        description="봇의 단호함을 나타냅니다. 숫자가 높을수록 주장을 강하게 하거나 명확히 표현하는 경향이 있습니다. 1(매우 유연함) ~ 10(매우 단호함)."
    )
    access_level_set = Field(
        examples=[True, False],
        default=True,
        title="케릭터 액세스",
        description="봇의 액세스 수준을 나타냅니다. True: 특정 기능이나 영역에 대한 접근 권한이 허용됨. False: 제한됨."
    )

    output_data_set = Field(
        examples=['''
        물론이죠! Llama AI 모델의 출시일과 버전들은 다음과 같습니다:

        1. Llama 1: 2023년 출시1

        2. Llama 2: 2024년 6월 1일 출시2

        3. Llama 3: 2024년 7월 23일 출시3

        4. Llama 3.1: 2024년 7월 24일 출시4

        이 모델들은 Meta (구 Facebook)에서 개발한 AI 모델입니다.
        각 버전마다 성능과 기능이 개선되었습니다. 더 궁금한 점이 있으신가요?
        '''],
        title="Llama 답변"
    )
    ```

## 📌 Body 모델
- `Llama_Request`
    > Llama 모델에 대한 요청을 처리하는 Pydantic 모델로, 입력 텍스트를 포함합니다.

    ```python
    class Llama_Request(BaseModel):
        input_data: str = input_data_set
        google_access: bool = google_access_set
    
    ```
    - 요청 형식
        ```JSON
        {
            "input_data": "Llama AI 모델의 출시일과 버전들을 각각 알려줘.",
            "google_access": false
        }
        ```
- `Llama_Response`
    > Llama 모델의 응답을 처리하는 Pydantic 모델로, 생성된 응답 텍스트를 포함합니다.

    ```python
    class Llama_Response(BaseModel):
        output_data: str = output_data_set
    ```
    - 응답 형식
        ```JSON
        {
            "output_text": "물론이죠! Llama AI 모델의 출시일과 버전들은 다음과 같습니다:\n\n1. Llama 1: 2023년 출시\n\n2. Llama 2: 2024년 6월 1일 출시\n\n3. Llama 3: 2024년 7월 23일 출시\n\n4. Llama 3.1: 2024년 7월 24일 출시\n\n이 모델들은 Meta (구 Facebook)에서 개발한 AI 모델입니다.\n각 버전마다 성능과 기능이 개선되었습니다. 더 궁금한 점이 있으신가요?"
        }
        ```

- `Bllossom_Request`
    > Bllossom 모델에 대한 요청을 처리하는 Pydantic 모델로, 입력 텍스트와 캐릭터 설정을 포함합니다.
    ```python
    class Bllossom_Request(BaseModel):
        input_data: str = input_data_set
        character_name: str = character_name_set
        description: str = description_set
        greeting: str = greeting_set
        image: str = image_set
        character_setting: str = character_setting_set
        tone: str = tone_set
        energy_level: NATURAL_NUM = energy_level_set    # type: ignore
        politeness: NATURAL_NUM = politeness_set        # type: ignore
        humor: NATURAL_NUM = humor_set                  # type: ignore
        assertiveness: NATURAL_NUM = assertiveness_set  # type: ignore
        access_level: bool = access_level_set
        
        @field_validator('image', mode='before')
        def check_img_url(cls, v):
            return Validators.validate_URL(v)
        
        def model_dump(self, **kwargs):
            """
            Pydantic BaseModel의 dict() 메서드를 대체하는 model_dump() 메서드입니다.
            필터링된 데이터만 반환하도록 수정할 수 있습니다.
            """
            return super().model_dump(**kwargs)
    
    ```
    - 요청 형식
        ```JSON
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

- `Bllossom_Response`
    ```python
    class Bllossom_Response(BaseModel):
        output_data: str = output_data_set
    ```
    - 응답 형식
        ```JSON
        {
            "output_text": "안녕하세요! 오늘 날씨는 맑고 기온이 25도입니다. 무엇을 도와드릴까요?"
        }
        ```