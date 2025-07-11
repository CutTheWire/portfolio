# ChatBot - 버전 명세서 v0.4.x

## 개요
이 문서는 ChatBot 시스템의 v0.4.x 계열 버전에 대한 공식 명세서입니다. v0.2.x의 Spring Boot 통합 시스템에서 **완전한 React 프론트엔드 통합**과 **사용자 경험 혁신**을 중심으로 한 **엔터프라이즈급 풀스택 웹 플랫폼**으로 진화했습니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v0.4.0** | 2025-03-15 | `a9cc0e55` | Stable |
| **v0.4.1** | 2025-05-05 | `8282e82d` | Stable |
| **v0.4.2** | 2025-05-07 | `62109a1e` | Stable |
| **v0.4.3** | 2025-05-10 | `86b53b3e` | Latest |

## v0.2.x에서 v0.4.x로의 주요 변경사항

### 프론트엔드 혁신
- **백엔드 중심** → **React + TypeScript 풀스택** 아키텍처
- **API 테스트 도구** → **완전한 웹 애플리케이션** 사용자 인터페이스
- **서버 사이드** → **클라이언트 사이드 렌더링 (CSR)** 전환

### 사용자 인증 시스템 혁신
- **단순 토큰 인증** → **소셜 로그인 통합** (Google, Kakao, 네이버)
- **기본 회원가입** → **약관 동의 및 이메일 인증** 시스템
- **관리자 수동 관리** → **AdminController 독립 관리 시스템**

### 데이터베이스 확장
- **기본 사용자 테이블** → **EULA 동의, 이메일 인증, 멤버십** 테이블 추가
- **MySQL 스키마** 대폭 확장 및 정규화
- **Spring Data JPA** 관계 매핑 최적화

### 신규 기능
- **React 기반 웹 인터페이스** (TypeScript, Tailwind CSS)
- **실시간 채팅 UI** (Markdown 지원, 메시지 디자인)
- **캐릭터 관리 시스템** (이미지 업로드, Swiper 컴포넌트)
- **관리자 전용 대시보드** (AdminController)
- **SMTP 이메일 인증** 시스템
- **멤버십 등급 관리** (Basic, VIP)

### 제거된 기능
- ❌ **단순 HTML 인터페이스** 완전 제거
- ❌ **MongoDB 라우터 세부화** (FastAPI 구조 간소화)
- ❌ **프로토타입 코드** 정리

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
- **MySQL**: 8.0 이상
- **MongoDB**: 4.4 이상

## 아키텍처

### 프로젝트 구조
```
📦 ChatBot v0.4.x
├── 📁 admincontroller/          # 관리자 대시보드 [NEW]
│   ├── 📁 client/               # React 관리자 UI
│   │   ├── package.json
│   │   ├── src/App.js
│   │   └── public/index.html
│   ├── 📁 server/               # Express.js 서버
│   │   ├── package.json
│   │   └── server.js
│   └── Dockerfile
├── 📁 fastapi/                  # FastAPI 서비스
│   ├── 📁 src/                  # 소스 코드 [RESTRUCTURED]
│   │   ├── 📁 utils/
│   │   │   ├── 📁 handlers/
│   │   │   │   ├── error_handler.py [REDESIGNED]
│   │   │   │   ├── mysql_handler.py [NEW]
│   │   │   │   └── smtp_handler.py [NEW]
│   │   │   ├── 📁 routers/
│   │   │   │   ├── 📁 mongo_controller/
│   │   │   │   │   ├── chatbot_controller.py [NEW]
│   │   │   │   │   └── office_controller.py [NEW]
│   │   │   │   ├── mysql_controller.py [NEW]
│   │   │   │   └── smtp_controller.py [NEW]
│   │   │   └── 📁 schemas/
│   │   │       └── chat_schema.py [UPDATED]
│   │   ├── server.py [UPDATED]
│   │   └── .env
│   └── requirements.txt [UPDATED]
├── 📁 nginx/                    # 웹 서버 및 React 앱
│   ├── 📁 react-frontpage/      # React 프론트엔드 [NEW]
│   │   ├── 📁 src/
│   │   │   ├── 📁 Component/    # React 컴포넌트
│   │   │   │   ├── 📁 Chatting/
│   │   │   │   │   ├── Chatting.tsx [NEW]
│   │   │   │   │   ├── 📁 Components/
│   │   │   │   │   │   ├── ChatContainer.tsx
│   │   │   │   │   │   ├── ChatFooter.tsx
│   │   │   │   │   │   ├── ChatHeader.tsx
│   │   │   │   │   │   ├── ChatMessage.tsx
│   │   │   │   │   │   └── ChatSidebar.tsx
│   │   │   │   │   ├── 📁 Services/
│   │   │   │   │   │   └── api.ts
│   │   │   │   │   └── 📁 Types/
│   │   │   │   │       └── index.ts
│   │   │   │   ├── 📁 CharacterMain/
│   │   │   │   │   ├── CharacterAdd.tsx [NEW]
│   │   │   │   │   ├── CharacterSwiper.tsx [NEW]
│   │   │   │   │   └── CharacterDetailModal.tsx [NEW]
│   │   │   │   ├── 📁 Login/
│   │   │   │   │   ├── Login.tsx [NEW]
│   │   │   │   │   └── 📁 logo/ (소셜 로그인 아이콘)
│   │   │   │   ├── 📁 Register/
│   │   │   │   │   ├── Register.tsx [NEW]
│   │   │   │   │   └── PrivacyConsentProps.tsx [NEW]
│   │   │   │   ├── 📁 Profile/
│   │   │   │   │   └── Profile.tsx [NEW]
│   │   │   │   └── 📁 SideBar/
│   │   │   │       └── SideBar.tsx [NEW]
│   │   │   ├── 📁 Pages/
│   │   │   │   ├── Home.tsx [NEW]
│   │   │   │   ├── MainPage.tsx [NEW]
│   │   │   │   ├── CharacterChat.tsx [NEW]
│   │   │   │   └── CharacterChatRoom.tsx [NEW]
│   │   │   ├── App.tsx [NEW]
│   │   │   ├── index.js [NEW]
│   │   │   └── types.ts [NEW]
│   │   ├── package.json [NEW]
│   │   ├── tsconfig.json [NEW]
│   │   ├── tailwind.config.js [NEW]
│   │   └── postcss.config.js [NEW]
│   ├── nginx.conf [UPDATED]
│   └── Dockerfile [UPDATED]
├── 📁 springboot/               # Spring Boot 서비스
│   ├── 📁 src/main/java/com/TreeNut/ChatBot_Backend/
│   │   ├── 📁 controller/
│   │   │   ├── CharacterController.kt [UPDATED]
│   │   │   ├── RoomController.kt [UPDATED]
│   │   │   └── UserController.kt [UPDATED]
│   │   ├── 📁 model/
│   │   │   ├── User.kt [UPDATED]
│   │   │   ├── Character.kt [UPDATED]
│   │   │   ├── UserEulaAgreement.kt [NEW]
│   │   │   └── middleware/TokenAuth.kt [NEW]
│   │   ├── 📁 repository/
│   │   │   ├── UserEulaAgreementRepository.kt [NEW]
│   │   │   └── UserRepository.kt [UPDATED]
│   │   ├── 📁 service/
│   │   │   ├── UserService.kt [UPDATED]
│   │   │   ├── CharacterService.kt [UPDATED]
│   │   │   └── RoomService.kt [UPDATED]
│   │   └── 📁 controller/config/
│   │       ├── SecurityConfig.kt [UPDATED]
│   │       ├── WebClientConfig.kt [UPDATED]
│   │       └── SwaggerConfig.kt [NEW]
│   ├── build.gradle.kts [UPDATED]
│   └── wait-for-it.sh [NEW]
├── 📁 mysql/
│   └── init.sql [EXPANDED]
├── docker-compose.yml [UPDATED]
├── rebuild.bat [UPDATED]
├── package.json [NEW]
└── README.md [UPDATED]
```

## API 명세

### Spring Boot API

#### 사용자 인증 및 관리 API

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

##### POST /api/users/login
일반 로그인 (이메일/비밀번호)

##### GET /api/users/profile
사용자 프로필 조회 (토큰 인증 필요)

##### PUT /api/users/profile
사용자 프로필 수정

##### GET /api/users/membership
사용자 멤버십 등급 조회

##### PUT /api/users/membership
사용자 멤버십 등급 수정

#### 소셜 로그인 API

##### POST /api/auth/google
Google OAuth 로그인

##### POST /api/auth/kakao  
Kakao OAuth 로그인

##### POST /api/auth/naver
네이버 OAuth 로그인

#### 캐릭터 관리 API

##### GET /api/characters
캐릭터 목록 조회 (검색 지원)

**쿼리 파라미터:**
- `search`: 검색어 (optional)
- `userId`: 사용자 ID (본인 캐릭터만 조회)

##### POST /api/characters
캐릭터 생성 (이미지 업로드 지원)

##### PUT /api/characters/{id}
캐릭터 수정

##### DELETE /api/characters/{id}
캐릭터 삭제

##### PUT /api/characters/{id}/access-level
캐릭터 공개 여부 변경 (관리자 전용)

### FastAPI API

#### 이메일 인증 API

##### POST /smtp/send-verification
이메일 인증 코드 발송

**요청 형식:**
```json
{
  "email": "string",
  "verification_type": "register|password_reset"
}
```

##### POST /smtp/verify-code
인증 코드 검증

**요청 형식:**
```json
{
  "email": "string",
  "code": "string"
}
```

#### MySQL 연동 API

##### GET /mysql/tables
MySQL 테이블 목록 조회

##### GET /mysql/users
사용자 정보 조회

#### MongoDB 채팅 API

##### POST /mongo/chatbot/create
Chatbot 채팅방 생성

##### PUT /mongo/chatbot/save_log
Chatbot 채팅 로그 저장

##### PUT /mongo/chatbot/update_log
Chatbot 채팅 로그 업데이트

##### POST /mongo/office/create
Office 채팅방 생성

##### PUT /mongo/office/save_log
Office 채팅 로그 저장

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. React 프론트엔드 - v0.4.x 완전 신규

#### App.tsx - 메인 애플리케이션 컴포넌트
React Router 기반의 SPA 구조를 구현합니다.

```typescript
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CookiesProvider } from 'react-cookie';

import Home from './Pages/Home';
import MainPage from './Pages/MainPage';
import CharacterChat from './Pages/CharacterChat';
import CharacterChatRoom from './Pages/CharacterChatRoom';
import Login from './Component/Login/Login';
import Register from './Component/Register/Register';
import Profile from './Component/Profile/Profile';

function App() {
  return (
    <CookiesProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/main" element={<MainPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/character" element={<CharacterChat />} />
            <Route path="/character/:characterId" element={<CharacterChatRoom />} />
          </Routes>
        </div>
      </Router>
    </CookiesProvider>
  );
}

export default App;
```

#### Chatting.tsx - 실시간 채팅 컴포넌트
완전한 채팅 인터페이스를 제공하는 핵심 컴포넌트입니다.

**주요 기능:**
- Markdown 렌더링 지원
- 실시간 메시지 스트리밍
- 채팅방 관리 (생성, 삭제)
- 스크롤 관리 및 UI 최적화

```typescript
import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import ChatContainer from './Components/ChatContainer';
import ChatFooter from './Components/ChatFooter';
import ChatHeader from './Components/ChatHeader';
import ChatSidebar from './Components/ChatSidebar';

interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

const Chatting: React.FC = () => {
  const { characterId } = useParams<{ characterId: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [roomId, setRoomId] = useState<string>('');
  
  // 채팅 전송 핸들러
  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    try {
      // API 호출 로직
      const response = await sendChatMessage(content, characterId);
      // ... 응답 처리
    } catch (error) {
      console.error('메시지 전송 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <ChatSidebar />
      <div className="flex-1 flex flex-col">
        <ChatHeader characterId={characterId} />
        <ChatContainer messages={messages} isLoading={isLoading} />
        <ChatFooter onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
};

export default Chatting;
```

#### Login.tsx - 소셜 로그인 컴포넌트
다중 소셜 로그인을 지원하는 로그인 컴포넌트입니다.

**지원 플랫폼:**
- Google OAuth 2.0
- Kakao Login
- 네이버 로그인

```typescript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [cookies, setCookie] = useCookies(['accessToken']);
  const navigate = useNavigate();

  // 일반 로그인
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setCookie('accessToken', data.token);
        navigate('/main');
      }
    } catch (error) {
      console.error('로그인 실패:', error);
    }
  };

  // Google 로그인
  const handleGoogleLogin = () => {
    window.location.href = '/api/auth/google';
  };

  // Kakao 로그인
  const handleKakaoLogin = () => {
    window.location.href = '/api/auth/kakao';
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <h2 className="text-3xl font-bold text-center">로그인</h2>
        
        {/* 일반 로그인 폼 */}
        <form onSubmit={handleLogin} className="mt-8 space-y-6">
          {/* ... 폼 필드들 */}
        </form>
        
        {/* 소셜 로그인 버튼들 */}
        <div className="space-y-3">
          <button onClick={handleGoogleLogin} className="w-full">
            <img src="/images/logo_google_kr.png" alt="Google 로그인" />
          </button>
          <button onClick={handleKakaoLogin} className="w-full">
            <img src="/images/logo_kakao_kr.png" alt="Kakao 로그인" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
```

#### CharacterSwiper.tsx - 캐릭터 카드 컴포넌트
Swiper.js를 사용한 캐릭터 카드 슬라이더입니다.

```typescript
import React, { useState, useEffect } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination } from 'swiper/modules';
import 'swiper/css';

interface Character {
  id: string;
  name: string;
  greeting: string;
  context: string;
  imageUrl?: string;
}

const CharacterSwiper: React.FC = () => {
  const [characters, setCharacters] = useState<Character[]>([]);

  useEffect(() => {
    fetchCharacters();
  }, []);

  const fetchCharacters = async () => {
    try {
      const response = await fetch('/api/characters');
      const data = await response.json();
      setCharacters(data);
    } catch (error) {
      console.error('캐릭터 로딩 실패:', error);
    }
  };

  return (
    <div className="character-swiper">
      <Swiper
        modules={[Navigation, Pagination]}
        navigation
        pagination={{ clickable: true }}
        spaceBetween={20}
        slidesPerView={3}
        breakpoints={{
          640: { slidesPerView: 1 },
          768: { slidesPerView: 2 },
          1024: { slidesPerView: 3 },
        }}
      >
        {characters.map((character) => (
          <SwiperSlide key={character.id}>
            <div className="character-card">
              <img 
                src={character.imageUrl || '/images/default-character.png'} 
                alt={character.name}
                className="character-image"
              />
              <h3 className="character-name">{character.name}</h3>
              <p className="character-context">{character.context}</p>
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
};

export default CharacterSwiper;
```

### 2. Spring Boot 백엔드 - v0.4.x 대폭 확장

#### UserController.kt - 사용자 관리 컨트롤러 - 서정훈
소셜 로그인과 멤버십 관리를 지원하는 확장된 사용자 컨트롤러입니다.

```kotlin
@RestController
@RequestMapping("/api/users")
class UserController(
    private val userService: UserService,
    private val tokenAuth: TokenAuth
) {
    
    @PostMapping("/register")
    fun register(@RequestBody request: UserRegisterRequest): ResponseEntity<UserResponse> {
        // EULA 동의 검증
        if (!request.eulaAgreed) {
            throw BadRequestException("이용약관에 동의해야 합니다.")
        }
        
        val user = userService.createUser(request)
        return ResponseEntity.ok(UserResponse.from(user))
    }
    
    @GetMapping("/profile")
    fun getProfile(@RequestHeader("Authorization") token: String): ResponseEntity<UserProfileResponse> {
        val userId = tokenAuth.getUserIdFromToken(token)
        val user = userService.findById(userId)
        return ResponseEntity.ok(UserProfileResponse.from(user))
    }
    
    @GetMapping("/membership")
    fun getMembership(@RequestHeader("Authorization") token: String): ResponseEntity<MembershipResponse> {
        val userId = tokenAuth.getUserIdFromToken(token)
        val membership = userService.getUserMembership(userId)
        return ResponseEntity.ok(MembershipResponse(membership))
    }
    
    @PutMapping("/membership")
    fun updateMembership(
        @RequestHeader("Authorization") token: String,
        @RequestBody request: MembershipUpdateRequest
    ): ResponseEntity<String> {
        val userId = tokenAuth.getUserIdFromToken(token)
        userService.updateMembership(userId, request.membershipType)
        return ResponseEntity.ok("멤버십이 업데이트되었습니다.")
    }
}
```

#### CharacterController.kt - 캐릭터 관리 컨트롤러 업데이트
이미지 업로드와 검색 기능이 추가된 캐릭터 컨트롤러입니다.

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
    
    @PostMapping
    fun createCharacter(
        @RequestBody request: CharacterCreateRequest,
        @RequestHeader("Authorization") token: String
    ): ResponseEntity<CharacterResponse> {
        tokenAuth.validateToken(token)
        val userId = tokenAuth.getUserIdFromToken(token)
        
        val character = characterService.createCharacter(request, userId)
        return ResponseEntity.ok(CharacterResponse.from(character))
    }
    
    @PutMapping("/{id}/access-level")
    fun updateAccessLevel(
        @PathVariable id: Long,
        @RequestBody request: AccessLevelUpdateRequest,
        @RequestHeader("Authorization") token: String
    ): ResponseEntity<String> {
        // 관리자 권한 검증
        tokenAuth.validateAdminToken(token)
        
        characterService.updateAccessLevel(id, request.accessLevel)
        return ResponseEntity.ok("캐릭터 공개 여부가 변경되었습니다.")
    }
}
```

#### SwaggerConfig.kt - API 문서화 설정 - 서정훈
Swagger를 사용한 API 문서 자동화 설정입니다.

```kotlin
@Configuration
@EnableOpenApi
class SwaggerConfig {
    
    @Bean
    fun openAPI(): OpenAPI {
        return OpenAPI()
            .info(apiInfo())
            .addSecurityItem(securityRequirement())
            .components(components())
    }
    
    private fun apiInfo(): Info {
        return Info()
            .title("ChatBot API Documentation")
            .description("ChatBot v0.4.x API 명세서")
            .version("v0.4.3")
            .contact(Contact().name("TreeNut").email("sjmbee04@gmail.com"))
    }
    
    private fun securityRequirement(): SecurityRequirement {
        return SecurityRequirement().addList("Bearer Authentication")
    }
    
    private fun components(): Components {
        return Components()
            .addSecuritySchemes("Bearer Authentication", 
                SecurityScheme()
                    .type(SecurityScheme.Type.HTTP)
                    .scheme("bearer")
                    .bearerFormat("JWT")
            )
    }
}
```

### 3. 데이터베이스 모델 - v0.4.x 확장

#### User.kt - 사용자 모델 확장
멤버십과 소셜 로그인을 지원하는 확장된 사용자 모델입니다.

```kotlin
@Entity
@Table(name = "users")
data class User(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,
    
    @Column(nullable = false, unique = true, length = 100)
    val username: String,
    
    @Column(nullable = false, unique = true, length = 100)
    val email: String,
    
    @Column(nullable = false)
    val password: String,
    
    @Enumerated(EnumType.STRING)
    @Column(name = "membership_type", nullable = false)
    val membershipType: MembershipType = MembershipType.BASIC,
    
    @Column(name = "email_verified", nullable = false)
    val emailVerified: Boolean = false,
    
    @Column(name = "provider")
    val provider: String? = null, // google, kakao, naver
    
    @Column(name = "provider_id")
    val providerId: String? = null,
    
    @Column(name = "created_at", updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "updated_at")
    val updatedAt: LocalDateTime = LocalDateTime.now()
)

enum class MembershipType {
    BASIC, VIP
}
```

#### UserEulaAgreement.kt - EULA 동의 모델 - 신규 추가
사용자의 약관 동의 내역을 관리하는 모델입니다.

```kotlin
@Entity
@Table(name = "user_eula_agreements")
data class UserEulaAgreement(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,
    
    @Column(name = "user_id", nullable = false)
    val userId: Long,
    
    @Column(name = "eula_agreed", nullable = false)
    val eulaAgreed: Boolean,
    
    @Column(name = "privacy_agreed", nullable = false)
    val privacyAgreed: Boolean,
    
    @Column(name = "marketing_agreed", nullable = false)
    val marketingAgreed: Boolean = false,
    
    @Column(name = "agreed_at", nullable = false)
    val agreedAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "ip_address")
    val ipAddress: String? = null
)
```

### 4. FastAPI 서비스 - v0.4.x 구조 개선

#### SMTP Handler - 이메일 인증 시스템 - 서정훈
SMTP를 사용한 이메일 인증 코드 발송 시스템입니다.

```python
"""
SMTP 이메일 전송 핸들러
이메일 인증 코드 발송 및 검증을 담당
"""
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
import redis
import os

class SMTPHandler:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        
        # Redis 연결 (인증 코드 캐시용)
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            decode_responses=True
        )

    def generate_verification_code(self, length: int = 6) -> str:
        """랜덤 인증 코드 생성"""
        return ''.join(random.choices(string.digits, k=length))

    async def send_verification_email(self, email: str, verification_type: str) -> bool:
        """인증 이메일 발송"""
        try:
            code = self.generate_verification_code()
            
            # 인증 코드 Redis에 저장 (5분 만료)
            cache_key = f"verification:{email}:{verification_type}"
            self.redis_client.setex(cache_key, 300, code)
            
            # 이메일 내용 구성
            subject = self._get_email_subject(verification_type)
            body = self._get_email_body(code, verification_type)
            
            # 이메일 발송
            return self._send_email(email, subject, body)
            
        except Exception as e:
            print(f"이메일 발송 실패: {e}")
            return False

    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """실제 이메일 발송"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"SMTP 전송 실패: {e}")
            return False

    async def verify_code(self, email: str, code: str, verification_type: str) -> bool:
        """인증 코드 검증"""
        try:
            cache_key = f"verification:{email}:{verification_type}"
            stored_code = self.redis_client.get(cache_key)
            
            if stored_code and stored_code == code:
                # 인증 성공 시 코드 삭제
                self.redis_client.delete(cache_key)
                return True
            
            return False
            
        except Exception as e:
            print(f"인증 코드 검증 실패: {e}")
            return False
```

#### MySQL Handler - 데이터베이스 연동 - 서정훈
MySQL 데이터베이스와의 연동을 담당하는 핸들러입니다.

```python
"""
MySQL 데이터베이스 연동 핸들러
Spring Boot와 데이터 동기화 및 조회 기능 제공
"""
import aiomysql
import os
from typing import List, Dict, Optional

class MySQLHandler:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", "3306"))
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")
        
    async def get_connection(self):
        """MySQL 연결 생성"""
        return await aiomysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            charset='utf8mb4'
        )

    async def get_user_info(self, user_id: int) -> Optional[Dict]:
        """사용자 정보 조회"""
        try:
            conn = await self.get_connection()
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            query = """
            SELECT id, username, email, membership_type, email_verified, 
                   created_at, updated_at
            FROM users 
            WHERE id = %s
            """
            
            await cursor.execute(query, (user_id,))
            result = await cursor.fetchone()
            
            await cursor.close()
            conn.close()
            
            return result
            
        except Exception as e:
            print(f"사용자 정보 조회 실패: {e}")
            return None

    async def get_user_characters(self, user_id: int) -> List[Dict]:
        """사용자 캐릭터 목록 조회"""
        try:
            conn = await self.get_connection()
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            query = """
            SELECT id, name, greeting, context, image_url, access_level,
                   created_at, updated_at
            FROM characters 
            WHERE user_id = %s AND access_level = true
            ORDER BY created_at DESC
            """
            
            await cursor.execute(query, (user_id,))
            results = await cursor.fetchall()
            
            await cursor.close()
            conn.close()
            
            return list(results)
            
        except Exception as e:
            print(f"캐릭터 목록 조회 실패: {e}")
            return []
```

### 5. AdminController - 관리자 시스템 - v0.4.x 신규

#### Express.js 서버 (server.js)
관리자 전용 대시보드를 위한 독립적인 Express.js 서버입니다.

```javascript
const express = require('express');
const cors = require('cors');
const mysql = require('mysql2/promise');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// 미들웨어 설정
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../client/build')));

// MySQL 연결 설정
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME || 'chatbot',
  port: process.env.DB_PORT || 3308
};

// 사용자 통계 API
app.get('/api/admin/users/stats', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    
    const [totalUsers] = await connection.execute(
      'SELECT COUNT(*) as total FROM users'
    );
    
    const [activeUsers] = await connection.execute(
      'SELECT COUNT(*) as active FROM users WHERE updated_at > DATE_SUB(NOW(), INTERVAL 7 DAY)'
    );
    
    const [membershipStats] = await connection.execute(
      'SELECT membership_type, COUNT(*) as count FROM users GROUP BY membership_type'
    );
    
    await connection.end();
    
    res.json({
      totalUsers: totalUsers[0].total,
      activeUsers: activeUsers[0].active,
      membershipStats
    });
    
  } catch (error) {
    console.error('사용자 통계 조회 실패:', error);
    res.status(500).json({ error: '서버 오류' });
  }
});

// 캐릭터 관리 API
app.get('/api/admin/characters', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    
    const [characters] = await connection.execute(`
      SELECT c.*, u.username 
      FROM characters c 
      LEFT JOIN users u ON c.user_id = u.id 
      ORDER BY c.created_at DESC
    `);
    
    await connection.end();
    res.json(characters);
    
  } catch (error) {
    console.error('캐릭터 목록 조회 실패:', error);
    res.status(500).json({ error: '서버 오류' });
  }
});

// React 앱 서빙
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`관리자 서버가 포트 ${PORT}에서 실행 중입니다.`);
});
```

## 설치 및 설정

### Docker 기반 통합 배포 시스템

#### 환경 구성
1. **Docker & Docker Compose** 설치
2. **React 빌드** 환경 구성
3. **환경 변수** 설정 (.env 파일)
4. **소셜 로그인** API 키 설정
5. **SMTP 서비스** 설정

#### 빠른 시작
```bash
# 1. 리포지토리 클론
git clone https://github.com/TreeNut-KR/ChatBot.git
cd ChatBot

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일에서 데이터베이스, API 키, SMTP 설정

# 3. React 앱 빌드
cd nginx/react-frontpage
npm install
npm run build
cd ../..

# 4. 컨테이너 빌드 및 실행
docker-compose up --build

# 5. 서비스 접근 확인
# 메인 웹사이트: http://localhost
# 관리자 대시보드: http://localhost:3001
# Spring Boot API: http://localhost:8080
# FastAPI: http://localhost:8000
```

#### 서비스 포트 설정
- **nginx (React 앱)**: 80
- **Spring Boot**: 8080
- **FastAPI**: 8000
- **AdminController**: 3001
- **MySQL**: 3308
- **MongoDB**: 27017

## 운영 가이드

### 환경 설정
1. **React 개발 환경** 구성 (Node.js 18+)
2. **소셜 로그인** API 키 발급 및 설정
3. **SMTP 서비스** 설정 (Gmail, AWS SES 등)
4. **데이터베이스** 초기화 및 스키마 설정
5. **관리자 계정** 생성 및 권한 설정

### 모니터링 포인트
- **React 앱** 빌드 및 배포 상태
- **소셜 로그인** API 연동 상태
- **이메일 인증** 발송 성공률
- **사용자 가입/로그인** 통계
- **캐릭터 생성/수정** 활동
- **채팅 서비스** 이용률

### 문제 해결
- **React 빌드 실패**: Node.js 버전 및 의존성 확인
- **소셜 로그인 오류**: API 키 및 리다이렉트 URL 확인
- **이메일 발송 실패**: SMTP 설정 및 계정 상태 확인
- **토큰 인증 오류**: JWT 시크릿 키 및 만료 설정 확인
- **파일 업로드 실패**: 저장 경로 및 권한 확인

## 보안 고려사항

### 강화된 보안 기능
- **소셜 로그인 보안**: OAuth 2.0 표준 준수
- **이메일 인증**: 2단계 인증 체계
- **EULA 동의**: 법적 컴플라이언스 확보
- **관리자 권한 분리**: 독립적인 관리 시스템
- **토큰 기반 인증**: JWT를 통한 상태 없는 인증

### 프론트엔드 보안
- **XSS 방지**: React의 기본 보안 기능 활용
- **CSRF 보호**: SameSite 쿠키 정책
- **API 호출 보안**: 토큰 기반 인증
- **민감 정보 보호**: 환경 변수 분리
- **라우팅 보안**: 권한 기반 페이지 접근 제어

### 데이터 보호
- **개인정보 암호화**: 비밀번호 해싱 (BCrypt)
- **이메일 인증 코드**: 시간 제한 및 일회성
- **멤버십 정보**: 사용자별 접근 권한 관리
- **채팅 데이터**: 사용자별 격리 및 암호화
- **관리자 데이터**: 별도 인증