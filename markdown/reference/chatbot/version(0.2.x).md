# ChatBot - 버전 명세서 v0.2.x

## 개요
이 문서는 ChatBot 시스템의 v0.2.x 계열 버전에 대한 공식 명세서입니다. v0.1.x의 기본적인 채팅 로그 관리 시스템에서 **Spring Boot 백엔드 완전 통합**과 **캐릭터 관리 시스템**, **AI API 연동**을 도입한 엔터프라이즈급 채팅 플랫폼입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v0.2.0** | 2024-09-10 | `9fdcb3cf` | Stable |
| **v0.2.1** | 2024-09-29 | `c309af86` | Stable |
| **v0.2.2** | 2024-10-23 | `6e402a4c` | Stable |
| **v0.2.3** | 2024-10-26 | `93e63260` | Latest |

## v0.1.x에서 v0.2.x로의 주요 변경사항

### 백엔드 아키텍처 완전 전환
- **FastAPI 단독** → **FastAPI + Spring Boot 통합** 아키텍처
- **Spring Boot** 마이크로서비스 완전 안정화
- **Kotlin 기반** 백엔드 서비스 확장

### 데이터 모델 혁신
- **단순 채팅 로그** → **사용자/캐릭터/채팅방** 통합 관리 시스템
- **MySQL 스키마** 확장 (users, characters, chatrooms, officerooms)
- **JWT 토큰 인증** 미들웨어 도입

### 신규 기능
- **캐릭터 관리 시스템** (이미지 업로드, CRUD)
- **Office 채팅룸** 기능 추가
- **토큰 인증 미들웨어** 보안 강화
- **AI API 연동** (외부 AI 서비스 통합)
- **검색 기능** (캐릭터 및 데이터 검색)

### 개발 환경 개선
- **GitHub Actions** 자동화 강화
- **빌드 시스템** 최적화 (Gradle 캐시 활용)
- **코드 품질** 관리 (Kotlin 컨벤션)

### 제거된 기능
- ❌ **VS Code 설정 파일** 정리
- ❌ **Spring Boot 구 config** 파일 마이그레이션

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
- **MySQL**: 8.0 이상
- **MongoDB**: 4.4 이상

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot v0.2.x
├── 📁 .github/                  # GitHub Actions
│   └── 📁 workflows/
│       └── build-and-push.yml [UPDATED]
├── 📁 fastapi/                  # FastAPI 서비스
│   ├── 📁 batchfile/
│   │   └── venv_setup.bat [UPDATED]
│   ├── 📁 sources/
│   │   ├── server.py [REORGANIZED]
│   │   └── 📁 utils/
│   │       ├── DB_mongo.py [ENHANCED]
│   │       └── Models.py [EXPANDED]
│   └── requirements.txt [UPDATED]
├── 📁 nginx/                    # 웹 서버 설정
│   └── nginx.conf [UPDATED]
├── 📁 springboot/               # Spring Boot 서비스
│   ├── 📁 src/main/java/com/TreeNut/ChatBot_Backend/
│   │   ├── 📁 controller/       # REST API 컨트롤러
│   │   │   ├── CharacterController.kt [NEW]
│   │   │   ├── RoomController.kt [NEW]
│   │   │   └── UserController.kt [UPDATED]
│   │   ├── 📁 model/            # 데이터 모델
│   │   │   ├── Character.kt [NEW]
│   │   │   ├── Chatroom.kt [NEW]
│   │   │   ├── Officeroom.kt [NEW]
│   │   │   └── User.kt [UPDATED]
│   │   ├── 📁 repository/       # JPA 리포지토리
│   │   │   ├── CharacterRepository.kt [NEW]
│   │   │   ├── ChatroomRepository.kt [NEW]
│   │   │   ├── OfficeroomRepository.kt [NEW]
│   │   │   └── UserRepository.kt [UPDATED]
│   │   ├── 📁 service/          # 비즈니스 로직
│   │   │   ├── CharacterService.kt [NEW]
│   │   │   ├── RoomService.kt [NEW]
│   │   │   └── UserService.kt [UPDATED]
│   │   ├── 📁 middleware/       # 미들웨어
│   │   │   └── TokenAuth.kt [NEW]
│   │   ├── 📁 exceptions/       # 예외 처리
│   │   │   └── TokenAuthException.kt [NEW]
│   │   └── 📁 config/           # 설정
│   │       ├── SecurityConfig.kt [MOVED]
│   │       └── WebClientConfig.kt [NEW]
│   ├── build.gradle.kts [OPTIMIZED]
│   ├── gradle.properties [NEW]
│   └── wait-for-it.sh [NEW]
├── 📁 mysql/                    # MySQL 데이터베이스
│   └── init.sql [EXPANDED]
├── docker-compose.yml [UPDATED]
├── rebuild.bat [OPTIMIZED]
└── react_build.bat [NEW]
```

## API 명세

### Spring Boot API

#### 사용자 관리 API (`/api/users`)

##### POST /api/users/register
사용자 회원가입 API

**요청 형식:**
```json
{
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
  "name": "string",
  "greeting": "string",
  "context": "string",
  "imageUrl": "string (optional)"
}
```

##### GET /api/characters
캐릭터 목록 조회 API

**쿼리 파라미터:**
- `search`: 검색어 (optional)
- `userId`: 사용자 ID (본인 캐릭터만 조회)

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

### FastAPI API

#### MongoDB 라우터 (`/mongo`)

##### POST /mongo/office/create
Office 채팅방 문서 생성

##### PUT /mongo/office/save_log
Office 채팅 로그 저장

##### PUT /mongo/office/update_log
Office 채팅 로그 업데이트

##### POST /mongo/office/load_log
Office 채팅 로그 조회

##### DELETE /mongo/office/delete_log
Office 채팅 로그 일부 삭제

##### DELETE /mongo/office/delete_room
Office 채팅방 삭제

#### Chatbot 라우터 (`/mongo/chatbot`)

##### POST /mongo/chatbot/create
Chatbot 채팅방 문서 생성

##### PUT /mongo/chatbot/save_log
Chatbot 채팅 로그 저장

##### PUT /mongo/chatbot/update_log
Chatbot 채팅 로그 업데이트

##### POST /mongo/chatbot/load_log
Chatbot 채팅 로그 조회

##### DELETE /mongo/chatbot/delete_log
Chatbot 채팅 로그 일부 삭제

##### DELETE /mongo/chatbot/delete_room
Chatbot 채팅방 삭제

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. Spring Boot 컨트롤러 - v0.2.x 신규

#### CharacterController.kt (신규 추가) - 서정훈
캐릭터 관리를 위한 REST API 컨트롤러입니다.

**주요 기능:**
- 캐릭터 CRUD operations
- 이미지 업로드 지원
- 검색 기능
- 토큰 인증 미들웨어 적용

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
        // 토큰 검증
        tokenAuth.validateToken(token)
        
        return ResponseEntity.ok(characterService.createCharacter(character))
    }
    
    @GetMapping
    fun getAllCharacters(
        @RequestParam(required = false) search: String?,
        @RequestParam(required = false) userId: Long?
    ): ResponseEntity<List<Character>> {
        return ResponseEntity.ok(characterService.findCharacters(search, userId))
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

#### RoomController.kt (신규 추가) - 서정훈
채팅방 관리를 위한 REST API 컨트롤러입니다.

**주요 기능:**
- 채팅방 생성 및 삭제
- 채팅 로그 관리 (CRUD)
- Office 룸 전용 기능
- AI API 연동 준비

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

### 2. 데이터 모델 - v0.2.x 확장

#### Character.kt (신규) - 서정훈
캐릭터 정보를 관리하는 엔티티 클래스입니다.

```kotlin
@Entity
@Table(name = "characters")
data class Character(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,
    
    @Column(nullable = false, length = 100)
    val name: String,
    
    @Column(columnDefinition = "TEXT")
    val greeting: String,
    
    @Column(columnDefinition = "TEXT")
    val context: String,
    
    @Column(name = "image_url", length = 500)
    val imageUrl: String? = null,
    
    @Column(name = "access_level", nullable = false)
    val accessLevel: Boolean = true,
    
    @Column(name = "user_id")
    val userId: Long? = null,
    
    @Column(name = "created_at", updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "updated_at")
    val updatedAt: LocalDateTime = LocalDateTime.now()
)
```

#### Chatroom.kt (신규) - 서정훈
일반 채팅방 정보를 관리하는 엔티티 클래스입니다.

```kotlin
@Entity
@Table(name = "chatrooms")
data class Chatroom(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,
    
    @Column(name = "room_id", nullable = false, unique = true, length = 36)
    val roomId: String,
    
    @Column(name = "user_id", nullable = false)
    val userId: Long,
    
    @Column(name = "character_id")
    val characterId: Long? = null,
    
    @Column(name = "room_name", length = 200)
    val roomName: String? = null,
    
    @Column(name = "created_at", updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "updated_at")
    val updatedAt: LocalDateTime = LocalDateTime.now()
)
```

#### Officeroom.kt (신규) - 서정훈
Office 채팅방 정보를 관리하는 엔티티 클래스입니다.

```kotlin
@Entity
@Table(name = "officerooms")
data class Officeroom(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,
    
    @Column(name = "room_id", nullable = false, unique = true, length = 36)
    val roomId: String,
    
    @Column(name = "user_id", nullable = false)
    val userId: Long,
    
    @Column(name = "room_name", length = 200)
    val roomName: String? = null,
    
    @Column(name = "room_type", length = 50)
    val roomType: String = "office",
    
    @Column(name = "created_at", updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "updated_at")
    val updatedAt: LocalDateTime = LocalDateTime.now()
)
```

### 3. 미들웨어 시스템 - v0.2.x 신규

#### TokenAuth.kt (신규) - 서정훈
JWT 토큰 기반 인증 미들웨어입니다.

**주요 기능:**
- JWT 토큰 검증
- 사용자 인증 상태 확인
- 권한 기반 접근 제어
- 토큰 만료 처리

```kotlin
@Component
class TokenAuth {
    
    @Value("\${jwt.secret}")
    private lateinit var jwtSecret: String
    
    @Value("\${jwt.expiration}")
    private var jwtExpiration: Long = 86400000 // 24시간
    
    fun validateToken(token: String): Boolean {
        return try {
            val cleanToken = token.removePrefix("Bearer ")
            val claims = Jwts.parser()
                .setSigningKey(jwtSecret)
                .parseClaimsJws(cleanToken)
                .body
            
            !claims.expiration.before(Date())
        } catch (e: Exception) {
            throw TokenAuthException("Invalid or expired token")
        }
    }
    
    fun getUserIdFromToken(token: String): Long {
        val cleanToken = token.removePrefix("Bearer ")
        val claims = Jwts.parser()
            .setSigningKey(jwtSecret)
            .parseClaimsJws(cleanToken)
            .body
        
        return claims.subject.toLong()
    }
    
    fun generateToken(userId: Long): String {
        val now = Date()
        val expiration = Date(now.time + jwtExpiration)
        
        return Jwts.builder()
            .setSubject(userId.toString())
            .setIssuedAt(now)
            .setExpiration(expiration)
            .signWith(SignatureAlgorithm.HS512, jwtSecret)
            .compact()
    }
}
```

### 4. FastAPI 라우터 재구성 - v0.2.x

#### 서버 구조 개선 (server.py) - 서정훈
FastAPI 서버가 Office와 Chatbot 라우터로 분리되었습니다.

```python
# FastAPI 라우터 시스템 개선
office_router = APIRouter()  # Office 관련 라우터 정의
chatbot_router = APIRouter() # Chatbot 관련 라우터 정의

@office_router.post("/create", summary="유저 채팅방 ID 생성")
async def create_chat(request: ChatModel.Id_Request):
    try:
        document_id = await mongo_handler.create_collection(
            user_id=request.user_id,
            router="office"
        )
        return {"Document ID": document_id}
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))

@office_router.put("/save_log", summary="유저 채팅 저장")
async def save_chat_log(request: ChatModel.Office_Create_Request):
    try:
        request_data = request.model_dump()
        filtered_data = {key: value for key, value in request_data.items() if key != 'id'}
        
        response_message = await mongo_handler.add_office_log(
            user_id=request.user_id,
            document_id=request.id,
            new_data=filtered_data
        )
        return {"Result": response_message}
    except ValidationError as e:
        raise ChatError.BadRequestException(detail=str(e))
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))

# mongo_router에 세분화된 라우터 추가
mongo_router.include_router(office_router, prefix="/office", tags=["MongoDB Router / Office Router"])
mongo_router.include_router(chatbot_router, prefix="/chatbot", tags=["MongoDB Router / Chatbot Router"])
```

#### MongoDB 핸들러 확장 (DB_mongo.py) - 서정훈
라우터별 데이터 관리 기능이 추가되었습니다.

```python
async def create_collection(self, user_id: str, router: str) -> str:
    """
    사용자 ID와 라우터 타입에 기반한 채팅 로그 컬렉션을 생성합니다.
    
    Args:
        user_id (str): 사용자 ID
        router (str): 라우터 타입 ("office" 또는 "chatbot")
    
    Returns:
        str: 생성된 문서 ID
    """
    try:
        collection_name = f'{router}_log_{user_id}'
        collection = self.db[collection_name]
        document = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.utcnow(),
            "value": []
        }
        await collection.insert_one(document)
        return document["id"]
    except Exception as e:
        raise InternalServerErrorException(detail=f"Error creating {router} collection: {str(e)}")

async def get_log(self, user_id: str, document_id: str, router: str) -> List[Dict]:
    """
    특정 라우터의 채팅 로그를 조회합니다.
    
    Args:
        user_id (str): 사용자 ID
        document_id (str): 문서 ID
        router (str): 라우터 타입
    
    Returns:
        List[Dict]: 정렬된 채팅 로그 리스트
    """
    try:
        collection = self.db[f'{router}_log_{user_id}']
        document = await collection.find_one({"id": document_id})
        
        if document is None:
            raise NotFoundException(f"No document found with ID: {document_id}")
        
        value_list = document.get("value", [])
        sorted_value_list = sorted(value_list, key=lambda x: x.get("index"))
        
        return sorted_value_list
    except Exception as e:
        raise InternalServerErrorException(detail=f"Error retrieving {router} log: {str(e)}")
```

### 5. 데이터 모델 확장 (Models.py) - v0.2.x

#### 통합 필드 정의 시스템
코드 재사용성을 높이기 위한 공통 필드 정의 시스템입니다.

```python
# 공통 필드 정의
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

index_set = Field(
    examples=[1],
    title="채팅방 log index",
    description="int 형식"
)

# 라우터별 전용 모델
class Office_Create_Request(BaseModel):
    user_id: str = user_id_set
    id: str = id_set
    input_data: str = input_data_set
    output_data: str = output_data_set

class Office_Update_Request(BaseModel):
    user_id: str = user_id_set
    id: str = id_set
    input_data: str = input_data_set
    output_data: str = output_data_set
    index: NATURAL_NUM = index_set

class ChatBot_Create_Request(BaseModel):
    user_id: str = user_id_set
    id: str = id_set
    img_url: str = img_url_set
    input_data: str = input_data_set
    output_data: str = output_data_set

class ChatBot_Update_Request(BaseModel):
    user_id: str = user_id_set
    id: str = id_set
    img_url: str = img_url_set
    input_data: str = input_data_set
    output_data: str = output_data_set
    index: NATURAL_NUM = index_set
```

### 6. 빌드 시스템 최적화 - v0.2.x

#### Gradle 최적화 (build.gradle.kts) - 서정훈
Spring Boot 빌드 성능과 AI API 연동을 위한 의존성이 추가되었습니다.

**주요 개선사항:**
- 빌드 캐시 최적화
- 테스트 스킵 옵션
- AI API 연동 라이브러리
- WebClient 설정

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-webflux") // WebClient용
    
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

tasks.withType<Test> {
    useJUnitPlatform()
    enabled = false // 빌드 시 테스트 스킵
}
```

## 설치 및 설정

### Docker 기반 통합 배포 시스템

#### 환경 구성
1. **Docker & Docker Compose** 설치
2. **MySQL 및 MongoDB** 컨테이너 설정
3. **환경 변수** 설정 (.env 파일)
4. **AI API 키** 설정 (외부 AI 서비스용)

#### 빠른 시작
```bash
# 1. 리포지토리 클론
git clone https://github.com/TreeNut-KR/ChatBot_Docker.git
cd ChatBot_Docker

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일에서 데이터베이스 및 API 설정

# 3. 컨테이너 빌드 및 실행
docker-compose up --build

# 4. 서비스 접근 확인
# FastAPI: http://localhost:8000
# Spring Boot: http://localhost:8080
# MySQL: localhost:3308
# MongoDB: localhost:27017
```

#### 서비스 포트 설정
- **FastAPI**: 8000 (MongoDB API)
- **Spring Boot**: 8080 (MySQL API)
- **MySQL**: 3308 (외부 접근)
- **MongoDB**: 27017 (FastAPI 전용)
- **nginx**: 80 (프록시 서버)

### 개발 환경 설정

#### Spring Boot 개발환경
```bash
# Gradle 빌드
cd springboot
./gradlew build -x test

# 개발 서버 실행
./gradlew bootRun
```

#### FastAPI 개발환경
```bash
# 가상환경 설정
cd fastapi
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt

# 개발 서버 실행
uvicorn sources.server:app --reload --host 0.0.0.0 --port 8000
```

## 운영 가이드

### 환경 설정
1. **Docker 환경** 구성 및 컨테이너 오케스트레이션
2. **데이터베이스** 초기화 (MySQL 스키마, MongoDB 컬렉션)
3. **인증 시스템** 설정 (JWT 시크릿 키)
4. **AI API** 연동 설정 (외부 서비스 키)

### 모니터링 포인트
- **컨테이너 상태**: `docker-compose ps`
- **서비스 로그**: `docker-compose logs [service_name]`
- **데이터베이스 연결**: MySQL/MongoDB 연결 상태
- **API 엔드포인트**: Spring Boot/FastAPI 헬스체크
- **인증 미들웨어**: JWT 토큰 검증 성공률

### 문제 해결
- **컨테이너 재시작**: `docker-compose restart [service_name]`
- **빌드 캐시 삭제**: `docker-compose build --no-cache`
- **데이터베이스 초기화**: 볼륨 삭제 후 재생성
- **토큰 인증 오류**: JWT 시크릿 키 및 만료 시간 확인
- **AI API 연동 실패**: API 키 유효성 및 네트워크 연결 확인

## 보안 고려사항

### 강화된 보안 기능
- **JWT 토큰 인증**: 모든 민감한 API 엔드포인트 보호
- **미들웨어 검증**: Spring Boot 요청 전처리
- **데이터베이스 분리**: MySQL(메타데이터) + MongoDB(채팅로그)
- **환경 변수 보호**: Docker Secrets 활용

### API 보안 강화
- **토큰 기반 인증**: 사용자별 세션 관리
- **CORS 설정**: 허용된 도메인만 접근
- **입력 검증**: Kotlin/Python 데이터 모델 검증
- **SQL 인젝션 방지**: JPA 쿼리 메서드 사용
- **NoSQL 인젝션 방지**: MongoDB 파라미터 바인딩

### 데이터 보호
- **사용자별 격리**: 채팅 데이터 사용자별 분리
- **캐릭터 소유권**: 사용자별 캐릭터 접근 제어
- **채팅방 권한**: 방 생성자 기반 권한 관리
- **토큰 만료**: 자동 세션 만료 및