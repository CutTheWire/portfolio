# 📌 버전 히스토리

| 버전      | 날짜                                   | 커밋 해시                                 |
|-----------|----------------------------------------|-------------------------------------------|
| **v1.0.0**| 2024-10-19 (토) 23:02:45 (KST)         | `acfd23b2f0a67f6ae21105c5cd1f838d89a8d752`|
| **v1.0.1**| 2024-10-20 (일) 00:34:16 (KST)         | `c4264a2f8f54dc3aef77b54aedc1853989074bc3`|
| **v1.0.2**| 2024-10-22 (화) 20:07:07 (KST)         | `3ebe8e2a5edda44b2076937eb484a1f18b889927`|

# 🗂️ 주요 파일 구조
```
📦src
 ┣ 📂logs
 ┣ 📂utils
 ┃ ┣ 📜AI_Llama_8B.py
 ┃ ┣ 📜Error_handlers.py 
 ┃ ┗ 📜Models.py
 ┗ 📜server.py
```
# 📄 server.py
## 📌 Lifespan 컨텍스트 매니저
> FastAPI 애플리케이션의 시작과 종료 시점에 실행되는 코드를 정의하는 데 사용됩니다. 이 예제에서는 Llama 모델을 초기화하고 종료할 때 필요한 리소스를 관리합니다.

```python
from utils.AI_Llama_8B import LlamaChatModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    global llama_model

    llama_model = LlamaChatModel()
    print("Llama 모델 로드 완료")
    yield

    llama_model = None
    print("Llama 모델 해제 완료")

app = FastAPI(lifespan=lifespan)
```

## 📌 API
|API 명칭|설명|
|:-----:|:-----|
|`/Llama`|Llama 모델에 대한 요청을 처리하는 API 엔드포인트|

```python
@app.post("/Llama", response_model=ChatModel.Llama_Response, summary="Llama 모델 답변 생성")
async def Llama_(request: ChatModel.Llama_Request):
    '''
    Llama 모델에 질문 입력 시 답변 반환.
    '''
    try:
        tables = llama_model.generate_response(request.input_data)
        return {"output_data": tables}
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))
```

---

# 📄 AI_Llama_8B.py

## 📌 클래스

|클래스 명칭|설명|
|:-----:|:-----|
|`LlamaChatModel`|Llama 모델을 GPU에 할당하여 질의응답 하도록 처리하는 클래스|

## 📌 함수/메서드

- `__init__`
> 클래스 초기화 메서드, Llama 모델의 파일 주소와 각 GPU의 변수를 초기화, 토크나이저와 GPU의 파이프라인 로드, 모델의 옵티마이저를 준비하는 과정을 처리하는 메서드

```python
def __init__(self):
    '''
    LlamaChatModel 클래스 초기화
    '''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    dotenv_path = os.path.join(parent_dir, '.env')
    load_dotenv(dotenv_path)
    self.cache_dir = "./fastapi/ai_model/"
    self.model_id = "meta-llama/Llama-3.1-8B-Instruct"
    self.bart_model_id = "facebook/bart-large-mnli"
    self.model_kwargs = {
        "torch_dtype": torch.float16,
        "trust_remote_code": True,
        "quantization_config": BitsAndBytesConfig(load_in_4bit=True)
    }

    self.hf_token = os.getenv("HUGGING_FACE_TOKEN")
    self.accelerator = Accelerator(mixed_precision="fp16")
    self.device_2080 = torch.device("cuda:0")
    self.device_1050 = torch.device("cuda:1")

    print("토크나이저 로드 중...")
    self.tokenizer = self.load_tokenizer()
    print("모델 로드 중...")
    self.model, self.optimizer = self.load_model_with_accelerator()
    print("복잡도 분석 모델 로드 중...")
    self.complexity_analyzer = self.load_complexity_analyzer()
    self.scaler = GradScaler()
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

- `load_complexity_analyzer`
> 복잡도 분석 모델을 GTX 1050에서 로드, `pipeline`에 `task="text-classification"`를 통한 GPU 1050에 복잡도 분석용으로 BART 할당

```python
def load_complexity_analyzer(self) -> transformers.Pipeline:
    '''
    복잡도 분석 모델을 GTX 1050에서 로드합니다.
    :return: 로드된 복잡도 분석 파이프라인
    '''
    return pipeline(
        "text-classification",
        model=self.bart_model_id,
        device=self.device_1050.index,
    )
```

- `load_model_with_accelerator`
> Llama 모델에 대한 옵티마이저를 생성하기 위해 `transformers.AutoModelForCausalLM`를 사용하여 Llama 모델의 인스턴스를 생성, 모델 인서턴스를 활용하여 GPU 2080을 할당 및 옵티마이저를 생성 후 모델과 옵티마이저를 반환

```python
def load_model_with_accelerator(self) -> tuple:
    '''
    모델을 Accelerator를 사용하여 로드하고 옵티마이저를 준비합니다.
    :return: 모델과 옵티마이저
    '''
    model = transformers.AutoModelForCausalLM.from_pretrained(
        self.model_id,
        cache_dir=self.cache_dir,
        token=self.hf_token,
        **self.model_kwargs
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
    model, optimizer = self.accelerator.prepare(model, optimizer)
    model.to(self.device_2080)
    return model, optimizer
```

- `analyze_complexity`
> `input_text: str`를 메게변수로 받아와서 `load_complexity_analyzer`를 통해 할당한 인스턴스 `self.complexity_analyzer`에 전달, 문장의 복잡도를 전달 받아 `low`,`medium`,`high`를 반환

```python
def analyze_complexity(self, input_text: str) -> str:
    '''
    입력 텍스트의 복잡성을 GTX 1050에서 분석합니다.
    :param input_text: 입력 텍스트
    :return: 복잡도 결과 (low, medium, high)
    '''
    result = self.complexity_analyzer(input_text)
    label = result[0]['label']
    if "ENTAILMENT" in label:
        return "low"
    elif "CONTRADICTION" in label:
        return "high"
    return "medium"
```

- `adjust_max_tokens`
> `complexity: str`를 메게변수로 반아와서 각 복잡도에 따른 토큰 값을 `low = 100`, `medium = 250`, `high = 500`으로 반환
```python
def adjust_max_tokens(self, complexity: str) -> int:
    '''
    복잡도에 따라 생성할 최대 토큰 수를 조정합니다.
    :param complexity: 입력 텍스트의 복잡도
    :return: 조정된 최대 토큰 수
    '''
    if complexity == "low":
        return 100 
    elif complexity == "high":
        return 500
    return 250
```

- `generate_response`  (v1.0.0)
> `input_text: str`를 메게변수로 받아와서 `analyze_complexity`, `adjust_max_tokens`를 거쳐 최대치 토큰 값을 할당 받은 뒤, 토크나이저로 인코딩하여 llama 모델에 설정 값들과 함께 전송, 받아온 문장을 디코딩하여 반환한다.

```python
def generate_response(self, input_text: str) -> str:
    '''
    주어진 입력 텍스트에 대한 응답을 생성합니다.
    :param input_text: 입력 텍스트
    :return: 생성된 응답 텍스트
    '''
    complexity = self.analyze_complexity(input_text)
    max_new_tokens = self.adjust_max_tokens(complexity)

    full_input = f"{input_text}"
    input_ids = self.tokenizer.encode(full_input, return_tensors="pt").to(torch.device("cpu"))
    attention_mask = (input_ids != self.tokenizer.pad_token_id).long()

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
    response = self.tokenizer.decode(output[0], skip_special_tokens=True)
    return response
```

- `generate_response_stream`  (v1.0.2)
> `input_text: str`를 메게변수로 받아와서 `analyze_complexity`, `adjust_max_tokens`를 거쳐 최대치 토큰 값을 할당 받은 뒤, 토크나이저로 인코딩하여 llama 모델에 설정 값들과 함께 전송, 받아온 문장을 디코딩하여 스트리밍으로 반환한다.

```python
def generate_response_stream(self, input_text: str):
    '''
    입력 텍스트에 대한 응답을 스트리밍 방식으로 생성합니다.
    :param input_text: 입력 텍스트
    :yield: 생성된 텍스트의 스트림
    '''
    complexity = self.analyze_complexity(input_text)
    max_new_tokens = self.adjust_max_tokens(complexity)

    full_input = f"{input_text}"
    input_ids = self.tokenizer.encode(full_input, return_tensors="pt").to(torch.device("cpu"))
    attention_mask = (input_ids != self.tokenizer.pad_token_id).long()

    streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
    
    # 모델을 실행할 스레드를 생성합니다.
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

    # 스트리머에서 텍스트가 생성될 때마다 이를 yield 합니다.
    for new_text in streamer:
        yield new_text
```

---

# 📄 Error_handlers.py
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

# 📄 Models.py

## 📌 클래스

|클래스 명칭|설명|
|:-----:|:-----|
|`Llama_Request`|Llama의 요청을 처리하는 Pydantic 모델. 입력 텍스트를 포함|
|`Llama_Response`|Llama의 응답을 처리하는 Pydantic 모델. 생성된 응답 텍스트를 포함|

## 📌 함수/필드
- `Field`
> Pydantic 모델의 필드를 정의하는 데 사용되는 함수로, 입력 데이터와 출력 데이터를 위한 필드를 설정합니다.

```python
input_data_set = Field(
    examples=["Llama AI 모델의 출시일과 버전들을 각각 알려줘."],
    title="사용자 입력 문장",
    min_length=1, max_length=500,
    description="사용자 입력 문장 길이 제약"
)

output_data_set = Field(
    examples=['''\
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
```
- 요청 형식
```JSON
{
    "input_text": "Llama AI 모델의 출시일과 버전들을 각각 알려줘."
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