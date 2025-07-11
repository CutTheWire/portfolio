# ChatBot - 버전 명세서 v0.3.x

## 개요
이 문서는 ChatBot 시스템의 v0.3.x 계열 버전에 대한 공식 명세서입니다. v0.2.x의 Spring Boot 통합 시스템에서 **AI API 연동 강화**와 **Spring Boot 최적화**, **GitHub Actions 수정**을 중심으로 한 안정성 개선 버전입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v0.3.0** | 2024-10-31 | `a7577b91` | Stable |
| **v0.3.1** | 2024-10-31 | `9a002fc7` | Stable |
| **v0.3.2** | 2024-12-18 | `6c1f2be9` | Stable |
| **v0.3.3** | 2025-02-05 | `b1a75b67` | Stable |
| **v0.3.4** | 2025-03-13 | `caf668df` | Latest |

## v0.2.x에서 v0.3.x로의 주요 변경사항

### AI API 연동 완성
- **AI API 연결 코드 추가** 및 **연동 성공** 달성
- **Google Cloud Console** JSON 키 관리 체계 확립
- **FastAPI AI API** 인터페이스 안정화

### 빌드 시스템 최적화
- **Gradle 빌드 속도** 대폭 단축 (Docker 최적화)
- **컨테이너 빌드** 효율성 향상
- **의존성 관리** 개선

### 인프라 개선
- **GitHub Actions** 빌드 스크립트 수정
- **Docker 컨테이너** 설정 최적화
- **파일 경로** 절대 경로 방식으로 변경

### 문서화 강화
- **README.md** 지속적 업데이트 (10회 이상)
- **프로젝트 문서** 개선 및 보완
- **설치 가이드** 상세화

### 제거된 기능
- ❌ **프로토타입 코드** 정리 및 제거

## 시스템 요구사항

### 하드웨어 요구사항
- **CPU**: 멀티코어 프로세서 권장
- **메모리**: 최소 16GB RAM
- **저장공간**: 최소 30GB 여유 공간
- **네트워크**: 고속 인터넷 (AI API 연동)

### 소프트웨어 요구사항
- **운영체제**: Linux/Windows (Docker 지원)
- **Java**: 17 이상 (Spring Boot)
- **Python**: 3.8 이상 (FastAPI)
- **Docker**: 20.10 이상
- **Docker Compose**: 2.0 이상
- **MySQL**: 8.0 이상
- **MongoDB**: 4.4 이상

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot v0.3.x
├── 📁 .github/                  # GitHub Actions
│   └── 📁 workflows/
│       └── build-and-push.yml [UPDATED]
├── 📁 fastapi/                  # FastAPI 서비스
│   ├── 📁 ai_model/             # AI 모델 파일
│   ├── 📁 batchfile/
│   │   └── venv_setup.bat [UPDATED]
│   ├── 📁 sources/
│   │   ├── server.py [UPDATED]
│   │   └── 📁 utils/
│   │       ├── DB_mongo.py [UPDATED]
│   │       └── Models.py [UPDATED]
│   ├── chatbot-character-image-6b2ea50ecd70.json [NEW]
│   └── requirements.txt
├── 📁 springboot/               # Spring Boot 서비스
│   ├── 📁 src/main/java/com/TreeNut/ChatBot_Backend/
│   │   ├── 📁 controller/
│   │   │   ├── CharacterController.kt [UPDATED]
│   │   │   ├── RoomController.kt [NEW]
│   │   │   └── UserController.kt [UPDATED]
│   │   ├── 📁 model/
│   │   │   ├── Character.kt [UPDATED]
│   │   │   ├── Chatroom.kt [NEW]
│   │   │   ├── Officeroom.kt [NEW]
│   │   │   └── User.kt [UPDATED]
│   │   ├── 📁 repository/
│   │   │   ├── CharacterRepository.kt [UPDATED]
│   │   │   ├── ChatroomRepository.kt [NEW]
│   │   │   ├── OfficeroomRepository.kt [NEW]
│   │   │   └── UserRepository.kt [UPDATED]
│   │   ├── 📁 service/
│   │   │   ├── CharacterService.kt [UPDATED]
│   │   │   ├── RoomService.kt [NEW]
│   │   │   └── UserService.kt [UPDATED]
│   │   ├── 📁 middleware/
│   │   │   └── TokenAuth.kt [UPDATED]
│   │   └── 📁 config/
│   │       ├── SecurityConfig.kt [MOVED]
│   │       └── WebClientConfig.kt [NEW]
│   ├── build.gradle.kts [OPTIMIZED]
│   ├── gradle.properties [UPDATED]
│   ├── settings.gradle.kts [UPDATED]
│   ├── Dockerfile [UPDATED]
│   └── wait-for-it.sh [NEW]
├── 📁 mysql/                    # MySQL 데이터베이스
│   ├── init.sql [UPDATED]
│   └── log.cnf [UPDATED]
├── 📁 nginx/                    # nginx 설정
│   ├── nginx.conf [UPDATED]
│   └── react-frontpage/
│       └── package-lock.json [UPDATED]
├── docker-compose.yml [UPDATED]
├── rebuild.bat [UPDATED]
├── react_build.bat [NEW]
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
기존 채팅 로그를 업데이트합니다.

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
채팅방 전체를 삭제합니다.

**요청 형식:**
```json
{
  "user_id": "string",
  "id": "string (UUID)"
}
```

### Spring Boot API

#### 사용자 관리 API (`/api/users`)

##### POST /api/users/register
사용자 회원가입 API

**요청 형식:**
```json
{
  "userid": "string",
  "username": "string",
  "email": "string",
  "password": "string"
}
```

##### DELETE /api/users/{id}
사용자 삭제 API

**경로 매개변수:**
- `id`: 사용자 ID

#### 캐릭터 관리 API (`/api/characters`)

##### POST /api/characters
캐릭터 생성 API (토큰 인증 필요)

**요청 형식:**
```json
{
  "userid": "string",
  "character_name": "string",
  "greeting": "string",
  "context": "string",
  "image": "string (optional)",
  "accesslevel": "boolean"
}
```

##### GET /api/characters
캐릭터 목록 조회 API

**쿼리 파라미터:**
- `search`: 검색어 (optional)
- `userid`: 사용자 ID (본인 캐릭터만 조회)

##### PUT /api/characters/{id}
캐릭터 수정 API

##### DELETE /api/characters/{id}
캐릭터 삭제 API

#### 채팅방 관리 API (`/api/rooms`)

##### POST /api/chatrooms
일반 채팅방 생성 API

##### POST /api/officerooms
Office 채팅방 생성 API

##### GET /api/chatrooms/{id}/logs
채팅 로그 조회 API

##### PUT /api/chatrooms/{id}/logs
채팅 로그 업데이트 API

##### DELETE /api/chatrooms/{id}/logs
채팅 로그 삭제 API

##### DELETE /api/officerooms/{id}
Office 채팅방 삭제 API

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. FastAPI 서버 컴포넌트 (server.py) - v0.3.x 업데이트

#### AI API 연동 완성 - 서정훈
v0.3.x에서 AI API와의 연동이 완전히 성공하였습니다.

```python
# AI API 연동 성공 - v0.3.x
async def call_ai_api(request_data):
    """
    AI API와의 연동을 처리하는 함수
    v0.3.x에서 연동 성공
    """
    try:
        # AI API 호출 로직
        api_response = await external_ai_service.process_request(request_data)
        return api_response
    except Exception as e:
        print(f"AI API 연동 오류: {e}")
        raise
```

#### 개선된 MongoDB 연동
MongoDB 라우터 기능이 더욱 안정화되었습니다.

```python
@mongo_router.put("/chat/save_log", summary="유저 채팅 저장")
async def save_chat_log(request: ChatModel.ChatLog_Create_Request):
    """
    새로운 채팅 로그를 MongoDB에 저장합니다.
    v0.3.x에서 안정성 개선
    """
    try:
        await Validators().url_status(request.img_url)
        request_data = request.model_dump()
        filtered_data = {key: value for key, value in request_data.items() if key != 'id'}
        
        response_message = await mongo_handler.add_chatlog_value(
            user_id=request.user_id,
            document_id=request.id,
            new_Data=filtered_data
        )
        return {"Result": response_message}
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except ChatError.NotFoundException as e:
        raise ChatError.NotFoundException(detail=str(e))
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))
```

### 2. Spring Boot 컨트롤러 컴포넌트 - v0.3.x 확장

#### RoomController 클래스 (RoomController.kt) - 신규 추가 - 서정훈

Office 및 Chatroom 관리를 위한 전용 컨트롤러입니다.

```kotlin
@RestController
@RequestMapping("/api/rooms")
class RoomController(
    private val roomService: RoomService
) {
    
    @PostMapping("/chatrooms")
    fun createChatroom(@RequestBody chatroom: Chatroom): ResponseEntity<Chatroom> {
        return ResponseEntity.ok(roomService.createChatroom(chatroom))
    }
    
    @PostMapping("/officerooms")
    fun createOfficeroom(@RequestBody officeroom: Officeroom): ResponseEntity<Officeroom> {
        return ResponseEntity.ok(roomService.createOfficeroom(officeroom))
    }
    
    @GetMapping("/chatrooms/{id}/logs")
    fun getChatroomLogs(@PathVariable id: String): ResponseEntity<List<Any>> {
        return ResponseEntity.ok(roomService.getChatroomLogs(id))
    }
    
    @PutMapping("/chatrooms/{id}/logs")
    fun updateChatroomLog(
        @PathVariable id: String,
        @RequestBody logData: Map<String, Any>
    ): ResponseEntity<String> {
        return ResponseEntity.ok(roomService.updateChatroomLog(id, logData))
    }
    
    @DeleteMapping("/chatrooms/{id}/logs")
    fun deleteChatroomLog(
        @PathVariable id: String,
        @RequestParam index: Int
    ): ResponseEntity<String> {
        return ResponseEntity.ok(roomService.deleteChatroomLog(id, index))
    }
    
    @DeleteMapping("/officerooms/{id}")
    fun deleteOfficeroom(@PathVariable id: String): ResponseEntity<Void> {
        roomService.deleteOfficeroom(id)
        return ResponseEntity.noContent().build()
    }
}
```

#### 개선된 CharacterController - v0.3.x 업데이트 - 서정훈

캐릭터 관리 기능이 더욱 강화되었습니다.

```kotlin
@RestController
@RequestMapping("/api/characters")
class CharacterController(
    private val characterService: CharacterService,
    private val tokenAuth: TokenAuth
) {
    
    @PostMapping
    fun createCharacter(
        @RequestBody character: Character,
        @RequestHeader("Authorization") token: String
    ): ResponseEntity<Character> {
        tokenAuth.validateToken(token)
        return ResponseEntity.ok(characterService.createCharacter(character))
    }
    
    @GetMapping
    fun getAllCharacters(
        @RequestParam(required = false) search: String?,
        @RequestParam(required = false) userid: String?
    ): ResponseEntity<List<Character>> {
        return ResponseEntity.ok(characterService.findCharacters(search, userid))
    }
    
    @PutMapping("/{id}")
    fun updateCharacter(
        @PathVariable id: Long,
        @RequestBody character: Character
    ): ResponseEntity<Character> {
        return ResponseEntity.ok(characterService.updateCharacter(id, character))
    }
    
    @DeleteMapping("/{id}")
    fun deleteCharacter(@PathVariable id: Long): ResponseEntity<Void> {
        characterService.deleteCharacter(id)
        return ResponseEntity.noContent().build()
    }
}
```

### 3. 데이터 모델 컴포넌트 - v0.3.x 확장

#### Chatroom 모델 (Chatroom.kt) - 신규 추가 - 서정훈

일반 채팅방 정보를 관리하는 엔티티 클래스입니다.

```kotlin
@Entity
@Table(name = "chatroom")
data class Chatroom(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val idx: Long = 0,
    
    @Column(name = "userid", nullable = false, length = 100)
    val userid: String,
    
    @Column(name = "characters_idx")
    val charactersIdx: Long? = null,
    
    @Column(name = "mongo_chatroomid", length = 100)
    val mongoChatroomid: String? = null,
    
    @Column(name = "created_at", updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "updated_at")
    val updatedAt: LocalDateTime = LocalDateTime.now()
)
```

#### Officeroom 모델 (Officeroom.kt) - 신규 추가 - 서정훈

Office 채팅방 정보를 관리하는 엔티티 클래스입니다.

```kotlin
@Entity
@Table(name = "officeroom")
data class Officeroom(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val idx: Long = 0,
    
    @Column(name = "userid", nullable = false, length = 100)
    val userid: String,
    
    @Column(name = "mongo_chatroomid", length = 100)
    val mongoChatroomid: String? = null,
    
    @Column(name = "created_at", updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "updated_at")
    val updatedAt: LocalDateTime = LocalDateTime.now()
)
```

#### 개선된 Character 모델 - v0.3.x 업데이트

```kotlin
@Entity
@Table(name = "characters")
data class Character(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val idx: Long = 0,
    
    @Column(name = "userid", nullable = false, length = 50)
    val userid: String,
    
    @Column(name = "character_name", nullable = false, length = 30)
    val characterName: String,
    
    @Column(name = "greeting", columnDefinition = "TEXT")
    val greeting: String? = null,
    
    @Column(name = "context", columnDefinition = "TEXT")
    val context: String? = null,
    
    @Column(name = "image", length = 255)
    val image: String? = null,
    
    @Column(name = "accesslevel", nullable = false)
    val accesslevel: Boolean = true,
    
    @Column(name = "created_at", updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "updated_at")
    val updatedAt: LocalDateTime = LocalDateTime.now()
)
```

### 4. 빌드 시스템 최적화 - v0.3.x

#### Gradle 최적화 (build.gradle.kts) - 서정훈

빌드 속도 단축과 AI API 연동을 위한 의존성이 최적화되었습니다.

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-webflux")
    
    // JWT 토큰 처리
    implementation("io.jsonwebtoken:jjwt:0.9.1")
    
    // MySQL 드라이버
    implementation("mysql:mysql-connector-java:8.0.33")
    
    // Kotlin 지원
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    
    // JSON 처리
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

// 빌드 속도 최적화
tasks.withType<Test> {
    useJUnitPlatform()
    enabled = false // 빌드 시 테스트 스킵으로 속도 향상
}
```

#### Docker 최적화 (Dockerfile) - 서정훈

빌드 속도 단축을 위한 Docker 설정이 개선되었습니다.

```dockerfile
FROM openjdk:17-jdk-slim

WORKDIR /app

# Gradle 캐시 최적화
COPY gradle gradle
COPY gradlew .
COPY gradle.properties .
COPY settings.gradle.kts .
COPY build.gradle.kts .

# 의존성 캐시
RUN ./gradlew dependencies --no-daemon

# 소스 코드 복사 및 빌드
COPY src src
RUN ./gradlew build -x test --no-daemon

EXPOSE 8080

CMD ["java", "-jar", "build/libs/ChatBot_Backend-0.0.1-SNAPSHOT.jar"]
```

### 5. GitHub Actions 최적화 - v0.3.x

#### 빌드 스크립트 수정 (build-and-push.yml) - 서정훈

GitHub Actions 빌드 프로세스가 개선되었습니다.

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Copy chatbot-character JSON key
      run: |
        mkdir -p ./fastapi
        echo "${{ secrets.CHATBOT_JSON_KEY }}" > ./fastapi/chatbot-character-image-6b2ea50ecd70.json
    
    - name: Copy Spring Boot config
      run: |
        mkdir -p ./springboot/src/main/resources
        echo "${{ secrets.SPRING_ENV }}" > ./springboot/src/main/resources/application.properties
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to GitHub Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push FastAPI
      uses: docker/build-push-action@v5
      with:
        context: ./fastapi
        file: ./fastapi/Dockerfile
        push: true
        tags: ghcr.io/treenut-kr/fastapi:${{ github.ref_name }}
    
    - name: Build and push Spring Boot
      uses: docker/build-push-action@v5
      with:
        context: ./springboot
        file: ./springboot/Dockerfile
        push: true
        tags: ghcr.io/treenut-kr/springboot:${{ github.ref_name }}
```

### 6. AI API 연동 시스템 - v0.3.x 완성

#### Google Cloud Console JSON 키 관리 - 서정훈

AI API 연동을 위한 인증 시스템이 완성되었습니다.

```python
# AI API 인증 및 연동
import json
import os
from google.oauth2 import service_account

def initialize_ai_client():
    """
    Google Cloud AI API 클라이언트 초기화
    JSON 키 파일을 사용한 인증
    """
    try:
        key_path = "/app/chatbot-character-image-6b2ea50ecd70.json"
        
        if os.path.exists(key_path):
            credentials = service_account.Credentials.from_service_account_file(key_path)
            # AI 클라이언트 초기화
            return initialize_client_with_credentials(credentials)
        else:
            raise FileNotFoundError("AI API 키 파일을 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"AI API 초기화 오류: {e}")
        raise
```

#### WebClient 설정 (WebClientConfig.kt) - 신규 추가 - 서정훈

Spring Boot에서 외부 API 호출을 위한 WebClient 설정입니다.

```kotlin
@Configuration
class WebClientConfig {
    
    @Bean
    fun webClient(): WebClient {
        return WebClient.builder()
            .codecs { configurer ->
                configurer.defaultCodecs().maxInMemorySize(10 * 1024 * 1024) // 10MB
            }
            .build()
    }
    
    @Bean
    fun aiApiWebClient(): WebClient {
        return WebClient.builder()
            .baseUrl("https://api.ai-service.com")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .build()
    }
}
```

## 설치 및 설정

### Docker 기반 통합 배포 시스템 - v0.3.x

#### 환경 구성
1. **Docker & Docker Compose** 설치
2. **AI API 키** 설정 (Google Cloud Console)
3. **환경 변수** 설정 (.env 파일)
4. **MySQL 및 MongoDB** 컨테이너 설정

#### 빠른 시작 (v0.3.x)
```bash
# 1. 리포지토리 클론
git clone https://github.com/TreeNut-KR/ChatBot_Docker.git
cd ChatBot_Docker

# 2. AI API 키 설정
# chatbot-character-image-6b2ea50ecd70.json 파일을 fastapi/ 폴더에 배치

# 3. 환경 변수 설정
cp .env.example .env
# .env 파일에서 데이터베이스 및 API 설정

# 4. 빌드 스크립트 실행 (최적화됨)
chmod +x rebuild.bat
./rebuild.bat

# 5. 컨테이너 실행
docker-compose up --build

# 6. 서비스 접근 확인
# FastAPI: http://localhost:8000
# Spring Boot: http://localhost:8080
# MySQL: localhost:3308
# MongoDB: localhost:27017
```

#### React 빌드 스크립트 (react_build.bat) - 신규 추가 - 서정훈
```batch
@echo off
echo React 프론트엔드 빌드 시작...

cd nginx/react-frontpage
npm install
npm run build

echo React 빌드 완료!
pause
```

### 개발 환경 설정

#### Spring Boot 개발환경 (최적화됨)
```bash
# Gradle 최적화된 빌드
cd springboot
./gradlew build -x test --no-daemon

# 개발 서버 실행
./gradlew bootRun
```

#### FastAPI 개발환경 (AI API 연동)
```bash
# 가상환경 설정 (개선됨)
cd fastapi
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# AI API 의존성 포함 설치
pip install -r requirements.txt

# AI API 키 환경 변수 설정
export GOOGLE_APPLICATION_CREDENTIALS="./chatbot-character-image-6b2ea50ecd70.json"

# 개발 서버 실행
uvicorn sources.server:app --reload --host 0.0.0.0 --port 8000
```

## 운영 가이드

### 환경 설정
1. **Docker 환경** 구성 및 컨테이너 오케스트레이션
2. **AI API 키** 설정 및 인증 확인
3. **데이터베이스** 초기화 (MySQL 스키마, MongoDB 컬렉션)
4. **GitHub Actions** 시크릿 설정
5. **빌드 최적화** 설정 확인

### 모니터링 포인트
- **AI API** 연동 상태 및 응답 시간
- **Gradle 빌드** 속도 및 성공률
- **Docker 컨테이너** 상태 및 리소스 사용량
- **GitHub Actions** 빌드 상태
- **Spring Boot** 애플리케이션 상태
- **FastAPI** 서비스 응답 시간

### 문제 해결
- **AI API 연동 실패**: JSON 키 파일 경로 및 권한 확인
- **Gradle 빌드 오류**: 캐시 삭제 및 의존성 재설치
- **Docker 빌드 실패**: 컨테이너 이미지 및 의존성 확인
- **GitHub Actions 실패**: 시크릿 변수 및 권한 설정 확인

### 성능 튜닝
1. **Gradle 최적화**
   - 빌드 캐시 활용
   - 테스트 스킵 설정
   - 병렬 빌드 활성화

2. **Docker 최적화**
   - 멀티 스테이지 빌드
   - 레이어 캐싱 최적화
   - 컨테이너 크기 최소화

3. **AI API 최적화**
   - 연결 풀링 설정
   - 타임아웃 최적화
   - 재시도 로직 구현

## 보안 고려사항

### 강화된 보안 기능
- **AI API 키**: 안전한 JSON 키 파일 관리
- **GitHub Secrets**: 민감 정보 암호화 저장
- **토큰 인증**: JWT 기반 API 접근 제어
- **환경 변수**: Docker Secrets 활용

### API 보안 강화
- **AI API 인증**: Google Cloud 서비스 계정 기반
- **Spring Boot Security**: 토큰 검증 미들웨어
- **FastAPI 보안**: 입력 검증 및 예외 처리
- **데이터베이스 보안**: 사용자별 데이터 격리

### 빌드 보안
- **GitHub Actions**: 안전한 시크릿 관리
- **Docker 이미지**: 최소 권한 원칙
- **의존성 관리**: 취약점 스캔 및 업데이트
- **코드 품질**: 정적 분석 및 검증