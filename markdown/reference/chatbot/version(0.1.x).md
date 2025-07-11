# ChatBot - 버전 명세서 v1.0.x

## 개요
이 문서는 ChatBot 시스템의 v1.0.x 계열 버전에 대한 공식 명세서입니다. 본 시스템은 FastAPI 기반의 웹 서비스로, MongoDB와 MySQL을 연동한 채팅 로그 관리 시스템과 Spring Boot 백엔드를 포함한 다중 서비스 아키텍처를 제공합니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v0.1.0** | 2024-08-27 | `8f2c1131` | Stable |
| **v0.1.1** | 2024-09-02 | `047c94c9` | Stable |
| **v0.1.2** | 2024-09-03 | `48a7465b` | Latest |

## v0.1.0에서 v0.1.2로의 주요 변경사항

### 아키텍처 확장
- **FastAPI 단일 서비스** → **FastAPI + Spring Boot 다중 서비스** 아키텍처
- **MongoDB 전용** → **MongoDB + MySQL 하이브리드** 데이터베이스 시스템
- **Docker 컨테이너** 통합 환경 구축

### 신규 기능
- **Spring Boot 백엔드** 서비스 추가
- **채팅방 삭제** 기능 구현
- **채팅 로그 업데이트** API 추가
- **MySQL 연동** 지원

### 개발 환경 개선
- **GitHub Issue 템플릿** 추가
- **행동 강령 (CODE_OF_CONDUCT)** 수립
- **오픈소스 라이선스 (GPL-3.0)** 적용
- **리빌드 스크립트** 자동화

### 제거된 기능
- ❌ **MongoDB 초기화 스크립트** 간소화

## 시스템 요구사항

### 하드웨어 요구사항
- **CPU**: 멀티코어 프로세서 권장
- **메모리**: 최소 8GB RAM
- **저장공간**: 최소 20GB 여유 공간

### 소프트웨어 요구사항
- **운영체제**: Linux/Windows (Docker 지원)
- **Docker**: 20.10 이상
- **Docker Compose**: 2.0 이상
- **Python**: 3.8 이상
- **Java**: 17 이상 (Spring Boot)

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot v1.0.x
├── 📁 .github/                  # GitHub 설정
│   └── 📁 ISSUE_TEMPLATE/
│       └── feature_request.md [NEW]
├── 📁 .vscode/                  # VS Code 설정 [NEW]
│   └── settings.json [NEW]
├── 📁 fastapi/                  # FastAPI 서비스
│   └── 📁 sources/
│       ├── server.py [UPDATED]
│       └── 📁 utils/
│           ├── DB_mongo.py [UPDATED]
│           └── Models.py [UPDATED]
├── 📁 mongo/                    # MongoDB 컨테이너
│   ├── Dockerfile [UPDATED]
│   └── init.py [NEW]
├── 📁 mysql/                    # MySQL 컨테이너
│   ├── init.sql [UPDATED]
│   └── log.cnf [UPDATED]
├── 📁 springboot/               # Spring Boot 서비스 [NEW]
│   ├── 📁 src/
│   │   └── 📁 main/java/com/TreeNut/ChatBot_Backend/
│   │       ├── ChatBotBackendApplication.kt [NEW]
│   │       ├── 📁 config/
│   │       │   └── SecurityConfig.kt [NEW]
│   │       ├── 📁 controller/
│   │       │   └── UserController.kt [NEW]
│   │       ├── 📁 model/
│   │       │   └── User.kt [NEW]
│   │       ├── 📁 repository/
│   │       │   └── UserRepository.kt [NEW]
│   │       └── 📁 service/
│   │           └── UserService.kt [NEW]
│   ├── build.gradle.kts [NEW]
│   └── Dockerfile [NEW]
├── docker-compose.yml [UPDATED]
├── rebuild.sh [NEW]
├── CODE_OF_CONDUCT.md [NEW]
├── LICENSE [NEW]
└── readme.md [UPDATED]
```

## API 명세

### FastAPI 엔드포인트

#### MongoDB 라우터 (`/mongo`)

##### PUT /mongo/chat/save_log
새로운 채팅 로그를 저장합니다.

**요청 형식:**
```json
{
  "user_id": "string",
  "id": "string (UUID)",
  "img_url": "string (Google Drive URL)",
  "input_data": "string (1-500자)",
  "output_data": "string (1-500자)"
}
```

##### PUT /mongo/chat/update_log
기존 채팅 로그를 업데이트합니다. (v0.1.2 추가)

**요청 형식:**
```json
{
  "user_id": "string",
  "id": "string (UUID)",
  "img_url": "string (Google Drive URL)",
  "input_data": "string (1-500자)",
  "output_data": "string (1-500자)",
  "index": "integer (≥1)"
}
```

##### DELETE /mongo/chat/delete_log
특정 채팅 로그 항목을 삭제합니다.

**요청 형식:**
```json
{
  "user_id": "string",
  "id": "string (UUID)",
  "index": "integer (≥1)"
}
```

##### DELETE /mongo/chat/delete_room
채팅방 전체를 삭제합니다. (v0.1.2 추가)

**요청 형식:**
```json
{
  "user_id": "string",
  "id": "string (UUID)"
}
```

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `404`: 리소스 없음
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

### Spring Boot API

#### 사용자 관리 API
Spring Boot 서비스에서 제공하는 사용자 관리 기능입니다.

- **포트**: 8080
- **보안**: Spring Security 적용
- **데이터베이스**: MySQL 연동

## 주요 컴포넌트

### 1. FastAPI 서버 컴포넌트 (server.py) - v0.1.2 업데이트

#### MongoDB 채팅 로그 관리
채팅 로그의 생성, 조회, 수정, 삭제를 지원하는 완전한 CRUD 시스템입니다.

```python
@mongo_router.put("/chat/update_log", summary="유저 채팅 업데이트")
async def update_chat_log(request: ChatLog_Update_Request):
    '''
    기존 채팅 문서에 유저의 채팅 데이터를 수정합니다.
    '''
    try:
        await Validators().url_status(request.img_url)  # 이미지 URL 확인
        request_data = request.model_dump()
        filtered_data = {key: value for key, value in request_data.items() if key != 'id'}
        
        response_message = await mongo_handler.update_chatlog_value(
            user_id=request.user_id,
            document_id=request.id,
            new_Data=filtered_data
        )
        return {"Result": response_message}
    except ValidationError as e:
        raise BadRequestException(detail=str(e))
    except NotFoundException as e:
        raise NotFoundException(detail=str(e))
    except Exception as e:
        raise InternalServerErrorException(detail=str(e))
```

#### 채팅방 관리 시스템
v0.1.2에서 추가된 채팅방 삭제 기능입니다.

```python
@mongo_router.delete("/chat/delete_room", summary="유저 채팅 지우기")
async def delete_chat_room(request: ChatRoom_Delete_Request):
    '''
    유저의 채팅방을 삭제합니다.
    '''
    try:
        response_message = await mongo_handler.remove_chatroom_value(
            user_id=request.user_id,
            document_id=request.id
        )
        return {"Result": response_message}
    except ValidationError as e:
        raise BadRequestException(detail=str(e))
    except NotFoundException as e:
        raise NotFoundException(detail=str(e))
    except Exception as e:
        raise InternalServerErrorException(detail=str(e))
```

### 2. MongoDB 핸들러 컴포넌트 (DB_mongo.py) - v0.1.2 확장

#### 채팅 로그 업데이트 기능
기존 채팅 로그의 특정 인덱스 항목을 수정하는 기능입니다.

```python
async def update_chatlog_value(self, user_id:str, document_id:str, new_Data : Dict):
    """
    특정 문서의 'value' 필드를 수정합니다.

    :param user_id: 사용자 ID
    :param document_id: 문서의 ID
    :param new_Data: 업데이트할 데이터
    :return: 성공 메시지
    """
    try:
        collection = self.db[f'chatlog_{user_id}']
        document = await collection.find_one({"id": document_id})
        if document is None:
            raise NotFoundException(f"No document found with ID: {document_id}")

        update_data_filtered = {
            key: value for key, value in new_Data.items() if key not in ['user_id']
        }

        index = new_Data.get('index')
        update_data_with_index = {
            "index":index,
            **update_data_filtered
        }

        # 기존 인덱스 항목 삭제
        result = await collection.update_one(
            {"id": document_id},
            {"$pull": {"value": {"index": index}}}
        )

        # 새로운 데이터 추가
        result = await collection.update_one(
            {"id": document_id},
            {"$push": {"value": update_data_with_index}}
        )

        if result.modified_count > 0:
            return f"Successfully added data to document with ID: {document_id}, Values:{index}"
        else:
            raise NotFoundException(f"No document found with ID: {document_id} or no data added.")
    except PyMongoError as e:
        raise InternalServerErrorException(detail=f"Error adding chatlog value: {str(e)}")
    except Exception as e:
        raise InternalServerErrorException(detail=f"Unexpected error: {str(e)}")
```

#### 채팅방 삭제 기능
채팅방 전체를 삭제하는 기능입니다.

```python
async def remove_chatroom_value(self, user_id: str, document_id: str) -> str:
    """
    특정 대화방을 지웁니다.
    
    :param user_id: 사용자 ID
    :param document_id: 문서의 ID
    :return: 성공 메시지
    """
    try:
        collection = self.db[f'chatlog_{user_id}']
        document = await collection.find_one({"id": document_id})

        if document is None:
            raise NotFoundException(f"No document found with ID: {document_id}")

        remove_chatroom = await collection.delete_one({"id": document_id})

        if remove_chatroom.deleted_count == 0:
            raise NotFoundException(f"No data found to remove document: {document_id}")
        elif remove_chatroom.deleted_count > 0:
            return f"Successfully deleted document with ID: {document_id}"

    except PyMongoError as e:
        raise InternalServerErrorException(detail=f"Error deleting document: {str(e)}")
    except Exception as e:
        raise InternalServerErrorException(detail=f"Unexpected error: {str(e)}")
```

### 3. 데이터 모델 컴포넌트 (Models.py) - v0.1.2 모듈화

#### 통합된 필드 정의
중복 코드를 제거하고 재사용 가능한 필드 정의로 개선되었습니다.

```python
NATURAL_NUM = conint(ge=1)

user_id_set = Field(
    examples=["shaa97102"],
    title="유저 id",
    min_length=6, max_length=50,
    description="유저 id 길이 제약"
)

id_set = Field(
    examples=["123e4567-e89b-12d3-a456-426614174000"],
    title="채팅방 id",
    min_length=1, max_length=36,
    description="UUID 형식"
)

img_url_set = Field(
    examples=["https://drive.google.com/thumbnail?id=12PqUS6bj4eAO_fLDaWQmoq94-771xfim"],
    title="이미지 URL",
    min_length=1, max_length=2048,
    description="URL의 최대 길이는 일반적으로 2048자"
)

index_set = Field(
    examples=[1],
    title="채팅방 log index",
    description="int 형식"
)
```

#### 신규 요청 모델

##### ChatLog_Update_Request (신규)
채팅 로그 업데이트를 위한 요청 모델입니다.

```python
class ChatLog_Update_Request(BaseModel):
    user_id: str = user_id_set
    id: str = id_set
    img_url: str = img_url_set
    input_data: str = input_data_set
    output_data: str = output_data_set
    index: NATURAL_NUM = index_set # type: ignore

    @field_validator('img_url', mode='before')
    def check_img_url(cls, v):
        return Validators.validate_URL(v)
    
    def model_dump(self, **kwargs):
        return super().model_dump(**kwargs)
```

##### ChatRoom_Delete_Request (신규)
채팅방 삭제를 위한 요청 모델입니다.

```python
class ChatRoom_Delete_Request(BaseModel):
    user_id: str = user_id_set
    id: str = id_set
    
    @field_validator('id', mode='before')
    def check_id(cls, v):
        return Validators.validate_uuid(v)
```

### 4. Spring Boot 컴포넌트 - v0.1.1 신규 추가

#### 사용자 관리 시스템
Spring Boot 기반의 사용자 관리 백엔드 서비스입니다.

**주요 구성 요소:**
- **User 모델**: 사용자 데이터 정의
- **UserRepository**: JPA 기반 데이터 접근 계층
- **UserService**: 비즈니스 로직 처리
- **UserController**: REST API 엔드포인트
- **SecurityConfig**: Spring Security 설정

```kotlin
// UserController.kt 예시
@RestController
@RequestMapping("/api/users")
class UserController(private val userService: UserService) {
    
    @GetMapping
    fun getAllUsers(): List<User> {
        return userService.findAll()
    }
    
    @PostMapping
    fun createUser(@RequestBody user: User): User {
        return userService.save(user)
    }
}
```

### 5. Docker 컨테이너 오케스트레이션 - v0.1.1 확장

#### 다중 서비스 Docker Compose
FastAPI, Spring Boot, MongoDB, MySQL을 통합한 컨테이너 환경입니다.

```yaml
version: '3.8'

services:
  fastapi:
    # FastAPI 서비스 설정
    depends_on:
      - mongodb
      - springboot

  springboot:
    restart: always
    build:
      context: ./springboot
      dockerfile: Dockerfile
    command: ./gradlew build -x test --no-daemon
    ports:
      - "8080:8080"
    depends_on:
      - mysql

  mongodb:
    # MongoDB 서비스 설정
    ports:
      - "27017:27017"

  mysql:
    # MySQL 서비스 설정
    ports:
      - "3308:3306"
    environment:
      MYSQL_ROOT_HOST: ${MYSQL_ROOT_HOST}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
```

## 설치 및 설정

### Docker 기반 배포

#### 환경 구성
1. **Docker** 및 **Docker Compose** 설치
2. **환경 변수** 설정 (.env 파일)
3. **리빌드 스크립트** 실행

```bash
# 리빌드 스크립트 실행
chmod +x rebuild.sh
source ./rebuild.sh

# 또는 수동 실행
docker-compose down
docker-compose up --build
```

#### 서비스 접근
- **FastAPI**: http://localhost:80
- **Spring Boot**: http://localhost:8080
- **MongoDB**: localhost:27017
- **MySQL**: localhost:3308

### 개발 환경 설정

#### GitHub 이슈 템플릿 활용
프로젝트에 기여하기 위한 표준화된 이슈 템플릿이 제공됩니다.

**기능 요청 템플릿 포함 항목:**
- 기능 설명
- 필요한 이유
- 예상 동작
- 우선순위
- 추가 정보

## 버전별 변경사항

### v0.1.0 (2024-08-27) - 서정훈
**초기 릴리즈**
- MongoDB 기반 채팅 로그 시스템
- FastAPI 웹 서비스
- Docker 컨테이너 환경
- 기본 CRUD 기능
- MySQL 초기 설정

### v0.1.1 (2024-09-01) - 서정훈
**Spring Boot 통합**
- Spring Boot 백엔드 서비스 추가
- Docker Compose 다중 서비스 설정
- 채팅방 삭제 기능 구현
- MySQL 바인딩 설정 개선
- 리빌드 스크립트 자동화

### v0.1.2 (2024-09-03) - 서정훈
**채팅 로그 고도화**
- 채팅 로그 업데이트 API 추가
- 채팅방 전체 삭제 기능
- MongoDB 쿼리 최적화 (인덱스 정렬)
- 데이터 모델 모듈화 및 필드 통합
- 인코딩 문제 해결

## 운영 가이드

### 환경 설정
1. **Docker 환경** 구성
2. **환경 변수** 설정 (데이터베이스 연결 정보)
3. **네트워크 포트** 확인 (80, 8080, 27017, 3308)
4. **서비스 의존성** 순서 확인

### 모니터링 포인트
- **컨테이너 상태**: `docker-compose ps`
- **로그 확인**: `docker-compose logs [service_name]`
- **데이터베이스 연결**: MongoDB/MySQL 연결 상태
- **API 엔드포인트**: 각 서비스별 헬스체크

### 문제 해결
- **컨테이너 재시작**: `docker-compose restart [service_name]`
- **빌드 캐시 삭제**: `docker-compose build --no-cache`
- **볼륨 초기화**: `docker-compose down -v`
- **포트 충돌**: 사용 중인 포트 확인 및 변경

## 보안 고려사항

### 입력 검증
- **UUID 형식** 검증 (채팅방 ID)
- **URL 형식** 검증 (Google Drive 이미지)
- **문자열 길이** 제한 (1-500자)
- **자연수** 검증 (인덱스 값)

### 데이터 보호
- **사용자별 컬렉션** 분리 (`chatlog_{user_id}`)
- **인덱스 기반** 데이터 접근 제어
- **예외 처리** 를 통한 정보 노출 방지
- **환경 변수** 를 통한 민감 정보 관리

### API 보안
- **입력 데이터** 검증 및 필터링
- **HTTP 예외** 표준화된 응답
- **CORS** 설정 (FastAPI)
- **Spring Security** 적용 (Spring Boot)

## 라이선스 및 기여

### 오픈소스 라이선스
- **GPL-3.0 라이선스** 적용
- **자유 소프트웨어** 원칙 준수
- **소스 코드 공개** 의무

### 기여 가이드라인
- **행동 강령** (CODE_OF_CONDUCT.md) 준수
- **이슈 템플릿** 활용
- **기능 요청** 표준 양식 사용
- **커밋 메시지** 표준화 (예: `feat: 새로운 기능 추가`, `fix: 버그 수정`)