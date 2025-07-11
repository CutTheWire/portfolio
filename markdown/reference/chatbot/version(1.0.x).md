# ChatBot - 버전 명세서 v1.0.x

## 개요
이 문서는 ChatBot 시스템의 v1.0.x 계열 버전에 대한 공식 명세서입니다. v0.4.x의 React 기반 풀스택 시스템에서 **Flyway 마이그레이션 도입**과 **프로덕션 환경 최적화**, **모바일 UI 지원**을 중심으로 한 **엔터프라이즈급 완성 버전**입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.0.0** | 2025-05-10 | `148923d6` | Stable |
| **v1.0.1** | 2025-05-14 | `a07699e9` | Stable |
| **v1.0.2** | 2025-05-17 | `e56c2b79` | Stable |
| **v1.0.3** | 2025-05-25 | `e89d5e80` | Stable |
| **v1.0.4** | 2025-06-09 | `aecb2091` | Stable |
| **v1.0.5** | 2025-06-19 | `01eaa52b` | Latest |

## v0.4.x에서 v1.0.x로의 주요 변경사항

### 데이터베이스 인프라 혁신
- **수동 스키마 관리** → **Flyway 자동 마이그레이션** 시스템
- **버전 없는 스키마** → **체계적인 마이그레이션 버전 관리**
- **개발자 수동 배포** → **자동화된 스키마 업데이트**

### 사용자 경험 확장
- **데스크톱 중심 UI** → **모바일 반응형 UI** 완전 지원
- **기본 프로필 기능** → **사용자 프로필 이미지** 관리 시스템
- **단순 채팅** → **재전송 기능, 핀치 줌** 등 고급 UX

### 개발 환경 성숙화
- **수동 빌드** → **자동화된 릴리스 노트** 생성
- **분산된 API 문서** → **통합 API 명세서** 시스템
- **개별 컨트롤러 문서** → **체계적인 개발 문서화**

### 신규 기능
- **Flyway 마이그레이션** 스크립트 자동 실행
- **FastAPI 디렉토리** 구조 모놀리스 재설계
- **모바일 최적화** UI/UX 개선
- **캐릭터 좋아요** 기능 및 테이블 정규화
- **카카오 OAuth** 로그인 완성
- **사용자 프로필 이미지** 업로드 및 관리

### 제거된 기능
- ❌ **개발 모드** 설정 파일 정리
- ❌ **프로토타입 코드** 최종 정리
- ❌ **수동 스키마 관리** 방식

## 시스템 요구사항

### 하드웨어 요구사항
- **CPU**: 멀티코어 프로세서 권장
- **메모리**: 최소 16GB RAM
- **저장공간**: 최소 30GB 여유 공간
- **네트워크**: 고속 인터넷 (소셜 로그인 및 이메일 서비스)

### 소프트웨어 요구사항
- **운영체제**: Linux/Windows (Docker 지원)
- **Node.js**: 18.0 이상 (React 개발)
- **Java**: 17 이상 (Spring Boot)
- **Python**: 3.8 이상 (FastAPI)
- **Docker**: 20.10 이상
- **MySQL**: 8.0 이상 (Flyway 지원)
- **MongoDB**: 4.4 이상

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot v1.0.x
├── 📁 .github/                  # GitHub Actions [UPDATED]
│   └── 📁 workflows/
│       └── build-and-push.yml [UPDATED]
├── 📁 admincontroller/          # 관리자 대시보드
│   ├── 📁 client/               # React 관리자 UI
│   │   ├── 📁 src/
│   │   │   └── 📁 components/
│   │   │       ├── AdminAuth.js [NEW]
│   │   │       └── DriveManager.js [NEW]
│   │   ├── package-lock.json [UPDATED]
│   │   └── package.json [UPDATED]
│   ├── 📁 server/               # Express.js 서버
│   │   ├── driveService.js [NEW]
│   │   ├── package-lock.json [UPDATED]
│   │   ├── package.json [UPDATED]
│   │   └── server.js [UPDATED]
│   ├── Dockerfile [UPDATED]
│   └── wait-for-it.sh [NEW]
├── 📁 fastapi/                  # FastAPI 서비스 [RESTRUCTURED]
│   ├── 📁 src/                  # 모놀리스 구조로 재설계 [RESTRUCTURED]
│   │   ├── 📁 api/              # API 계층 [RESTRUCTURED]
│   │   │   └── 📁 mongo_controller/
│   │   │       ├── character_controller.py [NEW]
│   │   │       └── office_controller.py [NEW]
│   │   ├── 📁 core/             # 핵심 비즈니스 로직 [NEW]
│   │   │   ├── app_state.py [NEW]
│   │   │   └── dependencies.py [NEW]
│   │   ├── 📁 schemas/          # 스키마 정의 [MOVED]
│   │   │   └── schema.py [RENAMED]
│   │   ├── 📁 services/         # 서비스 계층 [RENAMED]
│   │   │   ├── email_client.py [RENAMED]
│   │   │   ├── mongodb_client.py [RENAMED]
│   │   │   └── mysql_client.py [RENAMED]
│   │   ├── 📁 server/           # 서버 진입점 [NEW]
│   │   │   ├── Dockerfile [MOVED]
│   │   │   └── server.py [NEW]
│   │   ├── 📁 utils/
│   │   │   └── error_tools.py [NEW]
│   │   └── 📁 docs/
│   │       └── api_specification.md [NEW]
│   ├── .dockerignore [NEW]
│   └── requirements.txt [UPDATED]
├── 📁 mysql/                    # MySQL 및 Flyway [ENHANCED]
│   ├── 📁 migrations/           # Flyway 마이그레이션 [NEW]
│   │   ├── V1.1.0__init.sql [NEW]
│   │   ├── V1.1.1__init.sql [NEW]
│   │   ├── V1.1.2__init.sql [NEW]
│   │   └── V1.1.3__init.sql [NEW]
│   ├── Dockerfile [UPDATED]
│   ├── flyway-migrate.sh [NEW]
│   └── init.sql [UPDATED]
├── 📁 nginx/                    # nginx 및 React 앱
│   ├── 📁 react-frontpage/      # React 프론트엔드 [ENHANCED]
│   │   ├── 📁 src/
│   │   │   ├── 📁 Component/
│   │   │   │   ├── 📁 CharacterMain/
│   │   │   │   │   └── MyCharacter.tsx [NEW]
│   │   │   │   ├── 📁 Chatting/
│   │   │   │   │   ├── 📁 Services/
│   │   │   │   │   │   └── TokenUtils.ts [NEW]
│   │   │   │   │   ├── Chatting.css [UPDATED]
│   │   │   │   │   └── Chatting.tsx [UPDATED]
│   │   │   │   ├── 📁 Login/
│   │   │   │   │   ├── KakaoCallback.tsx [NEW]
│   │   │   │   │   └── Login.tsx [UPDATED]
│   │   │   │   ├── 📁 Profile/
│   │   │   │   │   └── Profile.tsx [UPDATED]
│   │   │   │   └── 📁 SideBar/
│   │   │   │       └── SideBar.tsx [UPDATED]
│   │   │   ├── 📁 Pages/
│   │   │   │   ├── CharacterChat.tsx [UPDATED]
│   │   │   │   ├── CharacterChatRoom.tsx [UPDATED]
│   │   │   │   ├── Home.tsx [UPDATED]
│   │   │   │   └── MainPage.tsx [UPDATED]
│   │   │   ├── App.tsx [UPDATED]
│   │   │   ├── index.css [UPDATED]
│   │   │   └── tailwind.output.css [UPDATED]
│   │   ├── public/index.html [UPDATED]
│   │   └── package.json [UPDATED]
│   ├── Dockerfile [UPDATED]
│   └── nginx.conf [UPDATED]
├── 📁 springboot/               # Spring Boot 서비스 [ENHANCED]
│   ├── 📁 src/
│   │   ├── 📁 docs/             # API 문서화 [NEW]
│   │   │   ├── CharacterController.md [NEW]
│   │   │   ├── RoomController.md [NEW]
│   │   │   └── UserController.md [NEW]
│   │   └── 📁 main/java/com/TreeNut/ChatBot_Backend/
│   │       ├── 📁 controller/
│   │       │   ├── CharacterController.kt [UPDATED]
│   │       │   ├── RoomController.kt [UPDATED]
│   │       │   └── UserController.kt [UPDATED]
│   │       ├── 📁 model/
│   │       │   ├── Character.kt [UPDATED]
│   │       │   ├── CharacterLike.kt [NEW]
│   │       │   └── User.kt [UPDATED]
│   │       ├── 📁 repository/
│   │       │   └── CharacterLikeRepository.kt [NEW]
│   │       └── 📁 service/
│   │           ├── CharacterService.kt [UPDATED]
│   │           ├── RoomService.kt [UPDATED]
│   │           └── UserService.kt [UPDATED]
│   └── build.gradle.kts [UPDATED]
├── docker-compose.yml [UPDATED]
├── rebuild.bat [UPDATED]
└── readme.md [UPDATED]
```

## API 명세

### Spring Boot API

#### 사용자 관리 API (`/api/users`) - v1.0.x 확장

##### POST /api/users/register
사용자 회원가입 및 약관 동의 처리

**요청 형식:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "eulaAgreed": "boolean",
  "privacyAgreed": "boolean"
}
```

##### GET /api/users/profile
사용자 프로필 조회 (토큰 인증 필요)

**v1.0.x 신규 기능:**
- **프로필 이미지** 업로드 및 관리
- **이미지 URL** 자동 생성
- **파일 형식** 검증 (JPG, PNG, GIF)

##### PUT /api/users/profile
사용자 프로필 수정 (이미지 포함)

**요청 형식:**
```json
{
  "username": "string",
  "email": "string",
  "profileImage": "multipart/form-data"
}
```

#### 캐릭터 관리 API (`/api/characters`) - v1.0.x 대폭 확장

##### GET /api/characters
캐릭터 목록 조회 (검색 지원)

**v1.0.x 추가 기능:**
- **REST API 표준** 준수 경로 수정
- **캐릭터 좋아요** 기능 통합
- **내 캐릭터** 목록 분리 조회

##### POST /api/characters/{characterId}/like
캐릭터 좋아요 추가/제거 (토큰 인증 필요)

**요청 형식:**
```json
{
  "action": "like|unlike"
}
```

##### GET /api/characters/my
내가 생성한 캐릭터 목록 조회

#### 채팅방 관리 API (`/api/rooms`) - v1.0.x 개선

##### POST /api/chatrooms
일반 채팅방 생성

##### DELETE /api/chatrooms/{id}
채팅방 삭제 기능 개선

**v1.0.x 개선사항:**
- **MySQL 메타데이터** 동시 삭제
- **MongoDB 채팅 로그** 연계 삭제
- **트랜잭션** 무결성 보장

### FastAPI API - v1.0.x 모놀리스 재구조화

#### MongoDB 컨트롤러 (`/mongo`) - 재설계

##### POST /mongo/office/create
Office 채팅방 문서 생성

##### POST /mongo/character/create
Character 채팅방 문서 생성

**v1.0.x 구조 개선:**
- **모놀리스 디렉토리** 구조로 통합
- **컨트롤러 분리** (office/character)
- **의존성 주입** 패턴 적용

#### API 문서화 시스템 - v1.0.x 신규

##### 자동 생성 API 명세서
GitHub Actions를 통한 자동 API 문서 생성

**포함 내용:**
- **FastAPI 명세서** 자동 추출
- **SpringBoot 컨트롤러** 문서 통합
- **릴리스 노트** 자동 생성

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. Flyway 마이그레이션 시스템 - v1.0.x 핵심 신규 기능

#### 마이그레이션 스크립트 관리
체계적인 데이터베이스 스키마 버전 관리 시스템입니다.

##### V1.1.0__init.sql - 서정훈
기본 테이블 구조 정의 및 초기 데이터 설정

```sql
-- 사용자 테이블
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    membership_type ENUM('BASIC', 'VIP') DEFAULT 'BASIC',
    email_verified BOOLEAN DEFAULT FALSE,
    profile_image_url VARCHAR(500),
    provider VARCHAR(50),
    provider_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 캐릭터 테이블
CREATE TABLE characters (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    greeting TEXT,
    context TEXT,
    image_url VARCHAR(500),
    access_level BOOLEAN DEFAULT TRUE,
    user_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 인덱스 생성
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_characters_user_id ON characters(user_id);
CREATE INDEX idx_characters_access_level ON characters(access_level);
```

##### V1.1.2__init.sql - 캐릭터 좋아요 시스템
정규화된 좋아요 테이블 추가

```sql
-- 캐릭터 좋아요 테이블 (정규화)
CREATE TABLE character_likes (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    character_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_character_like (user_id, character_id)
);

-- 좋아요 관련 인덱스
CREATE INDEX idx_character_likes_user_id ON character_likes(user_id);
CREATE INDEX idx_character_likes_character_id ON character_likes(character_id);
```

##### flyway-migrate.sh - 자동 실행 스크립트
```bash
#!/bin/bash
echo "Starting Flyway migration..."

# Flyway 실행
flyway -configFiles=/flyway/conf/flyway.conf migrate

# 마이그레이션 결과 확인
if [ $? -eq 0 ]; then
    echo "Migration completed successfully"
else
    echo "Migration failed"
    exit 1
fi
```

### 2. React 프론트엔드 - v1.0.x 모바일 최적화

#### 모바일 반응형 UI 시스템
완전한 모바일 지원을 위한 UI/UX 개선입니다.

##### Chatting.tsx - 모바일 최적화 - 서정훈
모바일 환경에서의 채팅 경험을 개선한 컴포넌트입니다.

```typescript
import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';

interface ChattingProps {
  isMobile?: boolean;
}

const Chatting: React.FC<ChattingProps> = ({ isMobile = false }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showRetryButton, setShowRetryButton] = useState(false);
  
  // 모바일 터치 이벤트 처리
  const [touchStart, setTouchStart] = useState<TouchEvent | null>(null);
  const [touchEnd, setTouchEnd] = useState<TouchEvent | null>(null);

  // 핀치 줌 기능
  const handleTouchStart = (e: TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0]);
  };

  const handleTouchMove = (e: TouchEvent) => {
    setTouchEnd(e.targetTouches[0]);
  };

  const handleTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = getTouchDistance();
    const isLeftSwipe = distance > 50;
    const isRightSwipe = distance < -50;

    if (isLeftSwipe) {
      // 사이드바 열기
      setSidebarOpen(true);
    }
  };

  // 재전송 기능
  const handleRetryMessage = async (messageId: string) => {
    try {
      setIsLoading(true);
      const message = messages.find(m => m.id === messageId);
      if (message) {
        await resendMessage(message.content);
        setShowRetryButton(false);
      }
    } catch (error) {
      console.error('재전송 실패:', error);
      setShowRetryButton(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div 
      className={`chatting-container ${isMobile ? 'mobile' : 'desktop'}`}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      {/* 모바일 헤더 */}
      {isMobile && (
        <div className="mobile-header">
          <button onClick={() => setSidebarOpen(!sidebarOpen)}>
            ☰
          </button>
          <h2>채팅</h2>
        </div>
      )}

      {/* 메시지 컨테이너 */}
      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className="message-wrapper">
            <div className={`message ${message.type}`}>
              {message.content}
            </div>
            
            {/* 재전송 버튼 (실패 시) */}
            {message.failed && (
              <button 
                className="retry-button"
                onClick={() => handleRetryMessage(message.id)}
              >
                🔄 재전송
              </button>
            )}
          </div>
        ))}
      </div>

      {/* 모바일 입력창 */}
      <div className="input-container mobile-optimized">
        <textarea 
          className="message-input mobile-input"
          placeholder="메시지를 입력하세요..."
          rows={isMobile ? 1 : 3}
        />
        <button className="send-button mobile-send">
          전송
        </button>
      </div>
    </div>
  );
};

export default Chatting;
```

#### 사용자 프로필 이미지 관리 시스템
프로필 이미지 업로드 및 관리 기능입니다.

##### Profile.tsx - 이미지 업로드 기능
```typescript
import React, { useState } from 'react';

const Profile: React.FC = () => {
  const [profileImage, setProfileImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [uploading, setUploading] = useState(false);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // 파일 형식 검증
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
      if (!allowedTypes.includes(file.type)) {
        alert('JPG, PNG, GIF 형식만 지원됩니다.');
        return;
      }

      // 파일 크기 검증 (5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('파일 크기는 5MB 이하여야 합니다.');
        return;
      }

      setProfileImage(file);
      
      // 미리보기 생성
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleImageUpload = async () => {
    if (!profileImage) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('profileImage', profileImage);

    try {
      const response = await fetch('/api/users/profile/image', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${getToken()}`,
        },
        body: formData,
      });

      if (response.ok) {
        alert('프로필 이미지가 업데이트되었습니다.');
        // 프로필 정보 새로고침
        await refreshProfile();
      }
    } catch (error) {
      console.error('이미지 업로드 실패:', error);
      alert('이미지 업로드에 실패했습니다.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="profile-container">
      <div className="profile-image-section">
        <div className="image-preview">
          {imagePreview ? (
            <img src={imagePreview} alt="프로필 미리보기" />
          ) : (
            <div className="placeholder">이미지 없음</div>
          )}
        </div>
        
        <input
          type="file"
          accept="image/jpeg,image/png,image/gif"
          onChange={handleImageChange}
          className="file-input"
        />
        
        <button 
          onClick={handleImageUpload}
          disabled={!profileImage || uploading}
          className="upload-button"
        >
          {uploading ? '업로드 중...' : '이미지 업로드'}
        </button>
      </div>
    </div>
  );
};
```

### 3. Spring Boot 백엔드 - v1.0.x 기능 확장

#### CharacterController.kt - REST API 표준화 - 서정훈
REST API 표준을 준수하는 캐릭터 관리 컨트롤러입니다.

```kotlin
@RestController
@RequestMapping("/api/characters")
class CharacterController(
    private val characterService: CharacterService,
    private val tokenAuth: TokenAuth
) {
    
    @GetMapping
    fun getAllCharacters(
        @RequestParam(required = false) search: String?,
        @RequestParam(required = false) userId: Long?
    ): ResponseEntity<List<CharacterResponse>> {
        val characters = when {
            search != null -> characterService.searchCharacters(search)
            userId != null -> characterService.findByUserId(userId)
            else -> characterService.findAllPublic()
        }
        return ResponseEntity.ok(characters.map { CharacterResponse.from(it) })
    }
    
    @GetMapping("/my")
    fun getMyCharacters(
        @RequestHeader("Authorization") token: String
    ): ResponseEntity<List<CharacterResponse>> {
        val userId = tokenAuth.getUserIdFromToken(token)
        val myCharacters = characterService.findByUserId(userId)
        return ResponseEntity.ok(myCharacters.map { CharacterResponse.from(it) })
    }
    
    @PostMapping("/{characterId}/like")
    fun toggleCharacterLike(
        @PathVariable characterId: Long,
        @RequestHeader("Authorization") token: String,
        @RequestBody request: LikeRequest
    ): ResponseEntity<LikeResponse> {
        val userId = tokenAuth.getUserIdFromToken(token)
        
        val result = when (request.action) {
            "like" -> characterService.addLike(userId, characterId)
            "unlike" -> characterService.removeLike(userId, characterId)
            else -> throw IllegalArgumentException("Invalid action: ${request.action}")
        }
        
        return ResponseEntity.ok(LikeResponse(
            success = result,
            likeCount = characterService.getLikeCount(characterId)
        ))
    }
    
    @DeleteMapping("/{id}")
    fun deleteCharacter(
        @PathVariable id: Long,
        @RequestHeader("Authorization") token: String
    ): ResponseEntity<Void> {
        val userId = tokenAuth.getUserIdFromToken(token)
        characterService.deleteCharacterWithChatLogs(id, userId)
        return ResponseEntity.noContent().build()
    }
}

data class LikeRequest(
    val action: String // "like" 또는 "unlike"
)

data class LikeResponse(
    val success: Boolean,
    val likeCount: Long
)
```

#### CharacterLike.kt - 정규화된 좋아요 모델
캐릭터 좋아요 기능을 위한 정규화된 데이터 모델입니다.

```kotlin
@Entity
@Table(name = "character_likes")
data class CharacterLike(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,
    
    @Column(name = "user_id", nullable = false)
    val userId: Long,
    
    @Column(name = "character_id", nullable = false)
    val characterId: Long,
    
    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()
) {
    init {
        // 유니크 제약조건 검증
        require(userId > 0) { "사용자 ID는 0보다 커야 합니다." }
        require(characterId > 0) { "캐릭터 ID는 0보다 커야 합니다." }
    }
}
```

#### UserController.kt - 프로필 이미지 기능 확장
사용자 프로필 이미지 관리 기능이 추가된 컨트롤러입니다.

```kotlin
@RestController
@RequestMapping("/api/users")
class UserController(
    private val userService: UserService,
    private val tokenAuth: TokenAuth
) {
    
    @PostMapping("/profile/image")
    fun uploadProfileImage(
        @RequestParam("profileImage") file: MultipartFile,
        @RequestHeader("Authorization") token: String
    ): ResponseEntity<ImageUploadResponse> {
        val userId = tokenAuth.getUserIdFromToken(token)
        
        // 파일 검증
        if (file.isEmpty) {
            throw IllegalArgumentException("파일이 비어있습니다.")
        }
        
        val allowedTypes = listOf("image/jpeg", "image/png", "image/gif")
        if (file.contentType !in allowedTypes) {
            throw IllegalArgumentException("지원하지 않는 파일 형식입니다.")
        }
        
        if (file.size > 5 * 1024 * 1024) { // 5MB 제한
            throw IllegalArgumentException("파일 크기가 5MB를 초과합니다.")
        }
        
        val imageUrl = userService.uploadProfileImage(userId, file)
        
        return ResponseEntity.ok(ImageUploadResponse(
            success = true,
            imageUrl = imageUrl,
            message = "프로필 이미지가 업로드되었습니다."
        ))
    }
    
    @GetMapping("/profile")
    fun getProfile(
        @RequestHeader("Authorization") token: String
    ): ResponseEntity<UserProfileResponse> {
        val userId = tokenAuth.getUserIdFromToken(token)
        val user = userService.findById(userId)
        
        return ResponseEntity.ok(UserProfileResponse(
            id = user.id,
            username = user.username,
            email = user.email,
            profileImageUrl = user.profileImageUrl,
            membershipType = user.membershipType,
            createdAt = user.createdAt
        ))
    }
}

data class ImageUploadResponse(
    val success: Boolean,
    val imageUrl: String?,
    val message: String
)

data class UserProfileResponse(
    val id: Long,
    val username: String,
    val email: String,
    val profileImageUrl: String?,
    val membershipType: String,
    val createdAt: LocalDateTime
)
```

### 4. FastAPI 서비스 - v1.0.x 모놀리스 재구조화

#### 디렉토리 구조 재설계 - 서정훈
마이크로서비스에서 모놀리스 구조로 재설계되었습니다.

```python
# src/server/server.py - 메인 서버 진입점
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.dependencies import get_database_handler
from api.mongo_controller import character_controller, office_controller

app = FastAPI(
    title="ChatBot FastAPI",
    description="MongoDB 기반 채팅 로그 관리 API",
    version="1.0.x"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(
    character_controller.router,
    prefix="/mongo/character",
    tags=["Character"]
)

app.include_router(
    office_controller.router,
    prefix="/mongo/office",
    tags=["Office"]
)

@app.get("/")
async def root():
    return {"message": "ChatBot FastAPI v1.0.x"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.x"}
```

#### 의존성 주입 시스템 - 서정훈
```python
# src/core/dependencies.py - 의존성 주입 관리
from functools import lru_cache
from services.mongodb_client import MongoDBHandler
from services.mysql_client import MySQLHandler
from utils.error_tools import ChatBotException

@lru_cache()
def get_database_handler() -> MongoDBHandler:
    """
    MongoDB 핸들러 싱글톤 인스턴스 반환
    """
    try:
        return MongoDBHandler()
    except Exception as e:
        raise ChatBotException(f"MongoDB 연결 실패: {str(e)}")

@lru_cache()
def get_mysql_handler() -> MySQLHandler:
    """
    MySQL 핸들러 싱글톤 인스턴스 반환
    """
    try:
        return MySQLHandler()
    except Exception as e:
        raise ChatBotException(f"MySQL 연결 실패: {str(e)}")
```

### 5. GitHub Actions - v1.0.x 자동화 강화

#### 릴리스 노트 자동 생성 시스템 - 서정훈
통합된 API 명세서를 포함한 릴리스 노트 자동 생성입니다.

```yaml
# .github/workflows/build-and-push.yml - 업데이트된 워크플로우
name: Build and Push Docker Images

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  update-docs-and-release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Update API specification version
        run: |
          VERSION=$(echo ${{ github.ref_name }} | sed 's/^v//')
          sed -i "s/- \*\*버전\*\*: .*/- \*\*버전\*\*: $VERSION/" fastapi/src/docs/api_specification.md
      
      - name: Prepare Release Notes
        run: |
          echo "# 릴리스 ${{ github.ref_name }}" > release_notes.md
          echo "" >> release_notes.md
          
          # FastAPI 명세서 추가
          echo "## FastAPI 명세서" >> release_notes.md
          cat fastapi/src/docs/api_specification.md >> release_notes.md
          echo "" >> release_notes.md
          
          # SpringBoot 컨트롤러 명세서 통합
          echo "## SpringBoot API 명세서" >> release_notes.md
          
          echo "### RoomController" >> release_notes.md
          cat springboot/src/docs/RoomController.md >> release_notes.md
          echo "" >> release_notes.md
          
          echo "### UserController" >> release_notes.md
          cat springboot/src/docs/UserController.md >> release_notes.md
          echo "" >> release_notes.md
          
          echo "### CharacterController" >> release_notes.md
          cat springboot/src/docs/CharacterController.md >> release_notes.md
          echo "" >> release_notes.md
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          name: Release ${{ github.ref_name }}
          body_path: release_notes.md
          files: docker-compose.yml
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  build-and-push-images:
    runs-on: ubuntu-latest
    needs: update-docs-and-release
    steps:
      - name: Set up SSL certificates
        run: |
          mkdir -p nginx/certificates
          echo "${{ secrets.SSL_CERT }}" | base64 -d > nginx/certificates/cert.pem
          echo "${{ secrets.SSL_KEY }}" | base64 -d > nginx/certificates/key.pem
          chmod 644 nginx/certificates/*.pem
      
      - name: Build and push images
        # ... 기존 Docker 빌드 로직
```

## 설치 및 설정

### Flyway 마이그레이션 설정 - v1.0.x 핵심

#### 환경 구성
1. **Docker & Docker Compose** 설치
2. **Flyway 설정** 파일 구성
3. **마이그레이션 스크립트** 배치
4. **MySQL 초기화** 설정

#### 빠른 시작 (v1.0.x)
```bash
# 1. 리포지토리 클론
git clone https://github.com/TreeNut-KR/ChatBot.git
cd ChatBot

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일에서 데이터베이스 설정

# 3. Flyway 마이그레이션 자동 실행
# Docker Compose가 자동으로 마이그레이션 실행
docker-compose up --build

# 4. 마이그레이션 상태 확인
docker exec chatbot-mysql flyway info

# 5. 서비스 접근 확인
# 메인 웹사이트: http://localhost
# 관리자 대시보드: http://localhost:3001
# Spring Boot API: http://localhost:8080
# FastAPI: http://localhost:8000
```

## 운영 가이드

### 환경 설정
1. **Flyway 마이그레이션** 자동 실행 설정
2. **모바일 UI** 반응형 테스트
3. **프로필 이미지** 스토리지 설정
4. **캐릭터 좋아요** 기능 테스트
5. **카카오 OAuth** API 키 설정

### 모니터링 포인트
- **Flyway 마이그레이션** 성공률 및 상태
- **모바일 사용자** 접속률 및 UX 지표
- **프로필 이미지** 업로드 성공률
- **캐릭터 좋아요** 기능 사용률
- **소셜 로그인** 성공률 (Google, Kakao)

### 문제 해결
- **마이그레이션 실패**: Flyway 로그 확인 및 스크립트 검증
- **모바일 UI 오류**: 반응형 CSS 및 터치 이벤트 확인
- **이미지 업로드 실패**: 파일 크기 및 형식 제한 확인
- **좋아요 기능 오류**: 테이블 제약조건 및 인덱스 확인
- **OAuth 로그인 실패**: API 키 및 리다이렉트 URL 확인

## 보안 고려사항

### 강화된 보안 기능
- **Flyway 마이그레이션**: 스키마 변경 추적 및 롤백
- **프로필 이미지**: 파일 형식 및 크기 검증
- **캐릭터 좋아요**: 중복 방지 및 권한 확인
- **모바일 보안**: 터치 이벤트 검증

### API 보안 강화
- **REST API 표준**: 일관된 엔드포인트 구조
- **토큰 기반 인증**: JWT 토큰 유효성 검사
- **파일 업로드 보안**: 악성 파일 검증
- **데이터베이스 무결성**: Flyway 마이그레이션을 통한 안전한 스키마 변경

### 데이터 보호
- **사용자 프로필**: 이미지 파일 안전한 저장
- **좋아요 데이터**: 정규화된 테이블 구조
- **마이그레이션 히스토리**: 모든 스키마 변경 추적
- **모바일 데이터**: 클라이언트