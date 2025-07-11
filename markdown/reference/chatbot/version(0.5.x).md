# ChatBot - 버전 명세서 v0.5.x

## 개요
이 문서는 ChatBot 시스템의 v0.5.x 계열 버전에 대한 공식 명세서입니다. v0.4.x의 React 풀스택 시스템에서 **API 설계 패턴 혁신**과 **의존성 주입(DI) 패턴**을 중심으로 한 **클린 아키텍처 최적화** 버전입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v0.5.0** | 2025-05-10 | `9a896ded` | Stable |
| **v0.5.1** | 2025-05-10 | `e98c1c75` | Latest |

## v0.4.x에서 v0.5.x로의 주요 변경사항

### 아키텍처 패턴 혁신
- **MVC 컨트롤러 패턴** → **의존성 주입(DI) 패턴** 도입
- **모노리식 서비스** → **모듈화된 API 호출 시스템**
- **단순 컨트롤러** → **REST API 설계 개선** 및 **API 호출 모듈화**

### FastAPI 구조 최적화
- **라우터 통합** → **MongoDB 컨트롤러 분리**
- **MySQL 컨트롤러 제거** (사용하지 않는 컴포넌트 정리)
- **채팅 스키마 정리** 및 **구조 개선**

### React 프론트엔드 개선
- **CharacterChatRoom 상태 초기화** 로직 개선
- **API 호출 모듈화** 및 **REST API 설계** 향상
- **조건부 사이드바** 표시 기능 추가

### 신규 기능
- **Google 접근 설정** 및 **알림 기능** 수정
- **약관 동의 회원가입** 구현 완료
- **메인페이지** 구성 및 **사용자 EULA 동의** 시스템 개선

### 제거된 기능
- ❌ **사용하지 않는 MySQL 컨트롤러** 완전 제거
- ❌ **멤버십 검증** 로직 제거 (API 경로 수정)
- ❌ **불필요한 import 문** 정리

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
📦 ChatBot v0.5.x
├── 📁 fastapi/                  # FastAPI 서비스
│   ├── 📁 src/                  # 소스 코드 [RESTRUCTURED]
│   │   ├── 📁 utils/
│   │   │   ├── 📁 handlers/
│   │   │   │   ├── error_handler.py [UPDATED]
│   │   │   │   ├── mysql_handler.py [REMOVED]
│   │   │   │   └── smtp_handler.py [UPDATED]
│   │   │   ├── 📁 routers/
│   │   │   │   ├── 📁 mongo_controller/
│   │   │   │   │   ├── chatbot_controller.py [SEPARATED]
│   │   │   │   │   └── office_controller.py [SEPARATED]
│   │   │   │   ├── mysql_controller.py [REMOVED]
│   │   │   │   └── smtp_controller.py [UPDATED]
│   │   │   └── 📁 schemas/
│   │   │       └── chat_schema.py [CLEANED]
│   │   ├── server.py [OPTIMIZED]
│   │   └── .env
│   └── requirements.txt [UPDATED]
├── 📁 nginx/                    # 웹 서버 및 React 앱
│   ├── 📁 react-frontpage/      # React 프론트엔드
│   │   ├── 📁 src/
│   │   │   ├── 📁 Component/
│   │   │   │   ├── 📁 Chatting/
│   │   │   │   │   ├── Chatting.tsx [UPDATED]
│   │   │   │   │   ├── 📁 Components/
│   │   │   │   │   │   ├── ChatContainer.tsx
│   │   │   │   │   │   ├── ChatFooter.tsx
│   │   │   │   │   │   ├── ChatHeader.tsx [UPDATED]
│   │   │   │   │   │   ├── ChatMessage.tsx
│   │   │   │   │   │   └── ChatSidebar.tsx
│   │   │   │   │   └── 📁 Services/
│   │   │   │   │       └── api.ts [NEW]
│   │   │   │   ├── 📁 CharacterMain/
│   │   │   │   │   ├── CharacterAdd.tsx [UPDATED]
│   │   │   │   │   └── CharacterSwiper.tsx [UPDATED]
│   │   │   │   ├── 📁 Login/
│   │   │   │   │   └── Login.tsx [UPDATED]
│   │   │   │   ├── 📁 Register/
│   │   │   │   │   ├── Register.tsx [UPDATED]
│   │   │   │   │   └── PrivacyConsentProps.tsx [UPDATED]
│   │   │   │   ├── 📁 Profile/
│   │   │   │   │   └── Profile.tsx [UPDATED]
│   │   │   │   └── 📁 SideBar/
│   │   │   │       └── SideBar.tsx [UPDATED]
│   │   │   ├── 📁 Pages/
│   │   │   │   ├── Home.tsx [UPDATED]
│   │   │   │   ├── MainPage.tsx [UPDATED]
│   │   │   │   ├── CharacterChat.tsx [UPDATED]
│   │   │   │   └── CharacterChatRoom.tsx [UPDATED]
│   │   │   ├── App.tsx [UPDATED]
│   │   │   └── types.ts [UPDATED]
│   │   └── tailwind.config.js [UPDATED]
│   └── nginx.conf [UPDATED]
├── 📁 springboot/               # Spring Boot 서비스
│   ├── 📁 src/main/java/com/TreeNut/ChatBot_Backend/
│   │   ├── 📁 controller/
│   │   │   ├── CharacterController.kt [UPDATED]
│   │   │   ├── RoomController.kt [UPDATED]
│   │   │   └── UserController.kt [UPDATED]
│   │   ├── 📁 model/
│   │   │   ├── User.kt [UPDATED]
│   │   │   ├── Character.kt [UPDATED]
│   │   │   └── UserEulaAgreement.kt [UPDATED]
│   │   ├── 📁 service/
│   │   │   ├── UserService.kt [UPDATED]
│   │   │   ├── CharacterService.kt [UPDATED]
│   │   │   └── RoomService.kt [UPDATED]
│   │   └── 📁 repository/
│   │       ├── UserEulaAgreementRepository.kt [UPDATED]
│   │       └── UserRepository.kt [UPDATED]
│   └── build.gradle.kts [UPDATED]
├── 📁 mysql/
│   └── init.sql [UPDATED]
├── docker-compose.yml [UPDATED]
└── README.md [UPDATED]
```

## API 명세

### Spring Boot API

#### 사용자 관리 API (`/api/users`)

##### POST /api/users/register
사용자 회원가입 및 약관 동의 처리 - v0.5.x 개선

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

**응답 형식:**
```json
{
  "id": "number",
  "username": "string",
  "email": "string",
  "created_at": "datetime"
}
```

##### GET /api/users/profile
사용자 프로필 조회 (토큰 인증 필요)

##### PUT /api/users/profile
사용자 프로필 수정

#### 캐릭터 관리 API (`/api/characters`)

##### GET /api/characters
캐릭터 목록 조회 (검색 지원) - v0.5.x 최적화

**쿼리 파라미터:**
- `search`: 검색어 (optional)
- `userId`: 사용자 ID (본인 캐릭터만 조회)

##### POST /api/characters
캐릭터 생성 (이미지 업로드 지원)

##### PUT /api/characters/{id}
캐릭터 수정

##### DELETE /api/characters/{id}
캐릭터 삭제

#### 채팅방 관리 API (`/api/rooms`)

##### POST /api/chatrooms
일반 채팅방 생성 - v0.5.x 멤버십 검증 제거

##### POST /api/officerooms
Office 채팅방 생성 - v0.5.x API 경로 수정

##### GET /api/chatrooms/{id}/logs
채팅 로그 조회

##### PUT /api/chatrooms/{id}/logs
채팅 로그 업데이트

##### DELETE /api/chatrooms/{id}/logs
채팅 로그 삭제

### FastAPI API - v0.5.x 구조 최적화

#### MongoDB 컨트롤러 분리

##### Chatbot 컨트롤러 (`/mongo/chatbot`)

###### POST /mongo/chatbot/create
Chatbot 채팅방 문서 생성

###### PUT /mongo/chatbot/save_log
Chatbot 채팅 로그 저장

###### PUT /mongo/chatbot/update_log
Chatbot 채팅 로그 업데이트

###### POST /mongo/chatbot/load_log
Chatbot 채팅 로그 조회

###### DELETE /mongo/chatbot/delete_log
Chatbot 채팅 로그 일부 삭제

###### DELETE /mongo/chatbot/delete_room
Chatbot 채팅방 삭제

##### Office 컨트롤러 (`/mongo/office`)

###### POST /mongo/office/create
Office 채팅방 문서 생성

###### PUT /mongo/office/save_log
Office 채팅 로그 저장

###### PUT /mongo/office/update_log
Office 채팅 로그 업데이트

###### POST /mongo/office/load_log
Office 채팅 로그 조회

###### DELETE /mongo/office/delete_log
Office 채팅 로그 일부 삭제

###### DELETE /mongo/office/delete_room
Office 채팅방 삭제

#### SMTP 컨트롤러 (`/smtp`)

##### POST /smtp/send-verification
이메일 인증 코드 발송

##### POST /smtp/verify-code
인증 코드 검증

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. FastAPI 구조 개선 - v0.5.x 최적화

#### MongoDB 컨트롤러 분리 - 서정훈

**chatbot_controller.py:**
```python
"""
Chatbot MongoDB 컨트롤러 - v0.5.x 분리
기존 통합 라우터에서 Chatbot 전용 컨트롤러로 분리
"""
from fastapi import APIRouter, HTTPException
from utils import ChatModel, ChatError, mongodb_client

chatbot_router = APIRouter()

@chatbot_router.post("/create", summary="Chatbot 채팅방 ID 생성")
async def create_chatbot_room(request: ChatModel.Id_Request):
    """
    Chatbot 전용 채팅방 생성 API
    """
    try:
        document_id = await mongo_handler.create_collection(
            user_id=request.user_id,
            router="chatbot"
        )
        return {"Document ID": document_id}
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))

@chatbot_router.put("/save_log", summary="Chatbot 채팅 저장")
async def save_chatbot_log(request: ChatModel.ChatBot_Create_Request):
    """
    Chatbot 채팅 로그 저장 API
    """
    try:
        request_data = request.model_dump()
        filtered_data = {
            key: value for key, value in request_data.items() 
            if key != 'id'
        }
        
        response_message = await mongo_handler.add_chatbot_log(
            user_id=request.user_id,
            document_id=request.id,
            new_data=filtered_data
        )
        return {"Result": response_message}
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))

# ... (기타 메서드들)
```

**office_controller.py:**
```python
"""
Office MongoDB 컨트롤러 - v0.5.x 분리  
기존 통합 라우터에서 Office 전용 컨트롤러로 분리
"""
from fastapi import APIRouter, HTTPException
from utils import ChatModel, ChatError, mongodb_client

office_router = APIRouter()

@office_router.post("/create", summary="Office 채팅방 ID 생성")
async def create_office_room(request: ChatModel.Id_Request):
    """
    Office 전용 채팅방 생성 API
    """
    try:
        document_id = await mongo_handler.create_collection(
            user_id=request.user_id,
            router="office"
        )
        return {"Document ID": document_id}
    except Exception as e:
        raise ChatError.InternalServerErrorException(detail=str(e))

# ... (기타 메서드들)
```

#### 서버 구조 최적화 (server.py) - 서정훈

```python
"""
FastAPI 서버 - v0.5.x 구조 최적화
의존성 주입 패턴 및 모듈화 적용
"""
from fastapi import FastAPI
from utils.routers.mongo_controller import chatbot_controller, office_controller
from utils.routers import smtp_controller

app = FastAPI(
    title="ChatBot API v0.5.x",
    description="의존성 주입 패턴이 적용된 최적화된 ChatBot API",
    version="0.5.x"
)

# MongoDB 라우터 등록 (분리된 컨트롤러)
app.include_router(
    chatbot_controller.chatbot_router,
    prefix="/mongo/chatbot",
    tags=["MongoDB Chatbot Controller"]
)

app.include_router(
    office_controller.office_router,
    prefix="/mongo/office", 
    tags=["MongoDB Office Controller"]
)

# SMTP 라우터 등록
app.include_router(
    smtp_controller.smtp_router,
    prefix="/smtp",
    tags=["SMTP Controller"]
)

# 사용하지 않는 MySQL 컨트롤러 제거
# app.include_router(mysql_controller.mysql_router, ...) # REMOVED
```

#### 채팅 스키마 정리 (chat_schema.py) - 서정훈

```python
"""
채팅 스키마 - v0.5.x 정리 및 최적화
불필요한 필드 제거 및 구조 개선
"""
from pydantic import BaseModel, Field
from typing import Optional

# 공통 필드 정의 (v0.5.x 최적화)
user_id_field = Field(
    examples=["user123"],
    title="사용자 ID",
    min_length=1, max_length=50,
    description="사용자 식별자"
)

id_field = Field(
    examples=["123e4567-e89b-12d3-a456-426614174000"],
    title="채팅방 ID", 
    min_length=1, max_length=36,
    description="UUID 형식의 채팅방 식별자"
)

# 정리된 요청 모델
class ChatBot_Create_Request(BaseModel):
    """
    Chatbot 채팅 생성 요청 - v0.5.x 정리
    """
    user_id: str = user_id_field
    id: str = id_field
    img_url: str = Field(..., description="캐릭터 이미지 URL")
    input_data: str = Field(..., min_length=1, max_length=500)
    output_data: str = Field(..., min_length=1)

class Office_Create_Request(BaseModel):
    """
    Office 채팅 생성 요청 - v0.5.x 정리
    """
    user_id: str = user_id_field
    id: str = id_field
    input_data: str = Field(..., min_length=1, max_length=500)
    output_data: str = Field(..., min_length=1)

# 공통 응답 모델
class Standard_Response(BaseModel):
    """
    표준 응답 모델 - v0.5.x 신규
    """
    status: str = Field(default="success")
    message: str
    data: Optional[dict] = None
```

### 2. React 프론트엔드 개선 - v0.5.x

#### API 호출 모듈화 (api.ts) - 서정훈

```typescript
/**
 * API 호출 모듈 - v0.5.x 신규
 * REST API 설계 개선 및 모듈화
 */
import axios from 'axios';

// API 기본 설정
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8080',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 토큰 인터셉터
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API 함수들
export const chatAPI = {
  // 채팅방 관리
  createChatroom: async (data: any) => {
    const response = await api.post('/api/rooms/chatrooms', data);
    return response.data;
  },

  createOfficeroom: async (data: any) => {
    const response = await api.post('/api/rooms/officerooms', data);
    return response.data;
  },

  getChatroomLogs: async (id: string) => {
    const response = await api.get(`/api/rooms/chatrooms/${id}/logs`);
    return response.data;
  },

  updateChatroomLog: async (id: string, logData: any) => {
    const response = await api.put(`/api/rooms/chatrooms/${id}/logs`, logData);
    return response.data;
  },

  deleteChatroomLog: async (id: string, index: number) => {
    const response = await api.delete(`/api/rooms/chatrooms/${id}/logs`, {
      params: { index }
    });
    return response.data;
  },
};

export const characterAPI = {
  // 캐릭터 관리
  getCharacters: async (search?: string, userId?: number) => {
    const params: any = {};
    if (search) params.search = search;
    if (userId) params.userId = userId;
    
    const response = await api.get('/api/characters', { params });
    return response.data;
  },

  createCharacter: async (data: any) => {
    const response = await api.post('/api/characters', data);
    return response.data;
  },

  updateCharacter: async (id: number, data: any) => {
    const response = await api.put(`/api/characters/${id}`, data);
    return response.data;
  },

  deleteCharacter: async (id: number) => {
    const response = await api.delete(`/api/characters/${id}`);
    return response.data;
  },
};

export const userAPI = {
  // 사용자 관리
  register: async (data: any) => {
    const response = await api.post('/api/users/register', data);
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/api/users/profile');
    return response.data;
  },

  updateProfile: async (data: any) => {
    const response = await api.put('/api/users/profile', data);
    return response.data;
  },
};

export default api;
```

#### CharacterChatRoom 상태 초기화 개선 - 서정훈

```typescript
/**
 * CharacterChatRoom 컴포넌트 - v0.5.x 개선
 * 상태 초기화 로직 개선 및 API 호출 모듈화 적용
 */
import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { chatAPI, characterAPI } from '../Component/Chatting/Services/api';

interface CharacterChatRoomProps {
  // ... props 정의
}

const CharacterChatRoom: React.FC<CharacterChatRoomProps> = () => {
  const { characterId } = useParams<{ characterId: string }>();
  const navigate = useNavigate();
  
  // 상태 초기화 개선 - v0.5.x
  const [state, setState] = useState({
    messages: [],
    isLoading: false,
    roomId: '',
    character: null,
    error: null,
  });

  // 초기화 로직 개선
  const initializeRoom = useCallback(async () => {
    if (!characterId) {
      navigate('/character');
      return;
    }

    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      // 캐릭터 정보 로드 (모듈화된 API 사용)
      const character = await characterAPI.getCharacters(undefined, characterId);
      
      if (!character) {
        throw new Error('캐릭터를 찾을 수 없습니다.');
      }

      // 채팅방 생성 또는 기존 채팅방 로드
      const roomData = await chatAPI.createChatroom({
        characterId: parseInt(characterId),
        userId: getUserId(), // 사용자 ID 가져오기
      });

      setState(prev => ({
        ...prev,
        character,
        roomId: roomData.roomId,
        isLoading: false,
      }));

      // 기존 채팅 로그 로드
      await loadChatHistory(roomData.roomId);

    } catch (error) {
      console.error('방 초기화 실패:', error);
      setState(prev => ({
        ...prev,
        error: error.message,
        isLoading: false,
      }));
    }
  }, [characterId, navigate]);

  // 채팅 히스토리 로드
  const loadChatHistory = async (roomId: string) => {
    try {
      const logs = await chatAPI.getChatroomLogs(roomId);
      setState(prev => ({
        ...prev,
        messages: logs || [],
      }));
    } catch (error) {
      console.error('채팅 히스토리 로드 실패:', error);
    }
  };

  // 메시지 전송 핸들러
  const handleSendMessage = async (content: string) => {
    if (!content.trim() || !state.roomId) return;

    try {
      setState(prev => ({ ...prev, isLoading: true }));

      const newMessage = {
        content,
        timestamp: new Date().toISOString(),
        type: 'user',
      };

      // 로컬 상태 업데이트
      setState(prev => ({
        ...prev,
        messages: [...prev.messages, newMessage],
      }));

      // 서버에 메시지 저장
      await chatAPI.updateChatroomLog(state.roomId, {
        input_data: content,
        timestamp: newMessage.timestamp,
      });

      // AI 응답 요청 (구현 필요)
      // const aiResponse = await getAIResponse(content, state.character);
      
    } catch (error) {
      console.error('메시지 전송 실패:', error);
    } finally {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  };

  useEffect(() => {
    initializeRoom();
  }, [initializeRoom]);

  // 에러 처리
  if (state.error) {
    return (
      <div className="error-container">
        <h2>오류가 발생했습니다</h2>
        <p>{state.error}</p>
        <button onClick={() => navigate('/character')}>
          캐릭터 목록으로 돌아가기
        </button>
      </div>
    );
  }

  // 로딩 처리
  if (state.isLoading && !state.character) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="character-chat-room">
      {/* 채팅 UI 렌더링 */}
    </div>
  );
};

export default CharacterChatRoom;
```

#### 조건부 사이드바 시스템 - 서정훈

```typescript
/**
 * App.tsx - v0.5.x 라우팅 개선
 * 조건부 사이드바 표시 기능 추가
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import SideBar from './Component/SideBar/SideBar';

// 사이드바를 숨길 경로들
const SIDEBAR_HIDDEN_PATHS = [
  '/login',
  '/register',
  '/',
];

const AppContent: React.FC = () => {
  const location = useLocation();
  
  // 현재 경로에서 사이드바를 표시할지 결정
  const shouldShowSidebar = !SIDEBAR_HIDDEN_PATHS.includes(location.pathname);

  return (
    <div className="app-container">
      {shouldShowSidebar && <SideBar />}
      <div className={`main-content ${shouldShowSidebar ? 'with-sidebar' : 'full-width'}`}>
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
    </div>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;
```

### 3. Spring Boot 백엔드 개선 - v0.5.x

#### RoomController 멤버십 검증 제거 - 서정훈

```kotlin
/**
 * RoomController - v0.5.x 최적화
 * 멤버십 검증 제거 및 API 경로 수정
 */
@RestController
@RequestMapping("/api/rooms")
class RoomController(
    private val roomService: RoomService
) {
    
    @PostMapping("/chatrooms")
    fun createChatroom(@RequestBody chatroom: Chatroom): ResponseEntity<Chatroom> {
        // v0.5.x: 멤버십 검증 로직 제거
        // 이전 버전의 membershipService.validateUser() 제거
        
        return ResponseEntity.ok(roomService.createChatroom(chatroom))
    }
    
    @PostMapping("/officerooms")
    fun createOfficeroom(@RequestBody officeroom: Officeroom): ResponseEntity<Officeroom> {
        // v0.5.x: 멤버십 검증 로직 제거
        // API 경로 정리 및 단순화
        
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

#### CharacterController 개선 - 서정훈

```kotlin
/**
 * CharacterController - v0.5.x 개선
 * API 설계 최적화 및 응답 구조 개선
 */
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
        // v0.5.x: 응답 구조 최적화
        val characters = when {
            search != null -> characterService.searchCharacters(search)
            userId != null -> characterService.findByUserId(userId)
            else -> characterService.findAllPublic()
        }
        
        return ResponseEntity.ok(
            characters.map { CharacterResponse.from(it) }
        )
    }
    
    @PostMapping
    fun createCharacter(
        @RequestBody request: CharacterCreateRequest,
        @RequestHeader("Authorization") token: String
    ): ResponseEntity<ApiResponse<CharacterResponse>> {
        // v0.5.x: 표준화된 응답 구조
        tokenAuth.validateToken(token)
        val userId = tokenAuth.getUserIdFromToken(token)
        
        val character = characterService.createCharacter(request, userId)
        
        return ResponseEntity.ok(
            ApiResponse.success(
                data = CharacterResponse.from(character),
                message = "캐릭터가 성공적으로 생성되었습니다."
            )
        )
    }
    
    // ... 기타 메서드들
}

// v0.5.x: 표준화된 API 응답 모델
data class ApiResponse<T>(
    val status: String,
    val message: String,
    val data: T? = null,
    val errors: List<String>? = null
) {
    companion object {
        fun <T> success(data: T? = null, message: String = "성공"): ApiResponse<T> {
            return ApiResponse(
                status = "success",
                message = message,
                data = data
            )
        }
        
        fun <T> error(message: String, errors: List<String>? = null): ApiResponse<T> {
            return ApiResponse(
                status = "error", 
                message = message,
                errors = errors
            )
        }
    }
}
```

## 설치 및 설정

### Docker 기반 배포 시스템 - v0.5.x 최적화

#### 빠른 시작
```bash
# 1. 리포지토리 클론
git clone https://github.com/TreeNut-KR/ChatBot.git
cd ChatBot

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일에서 데이터베이스, API 키, SMTP 설정

# 3. React 앱 빌드 (v0.5.x 최적화)
cd nginx/react-frontpage
npm install
npm run build
cd ../..

# 4. 컨테이너 빌드 및 실행
docker-compose up --build

# 5. API 테스트 (v0.5.x 최적화된 엔드포인트)
# 분리된 MongoDB 컨트롤러 테스트
curl -X POST "http://localhost:8000/mongo/chatbot/create" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

curl -X POST "http://localhost:8000/mongo/office/create" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'
```

#### 서비스 포트 설정
- **nginx (React 앱)**: 80
- **Spring Boot**: 8080 
- **FastAPI**: 8000
- **MySQL**: 3308
- **MongoDB**: 27017

## 운영 가이드

### 환경 설정
1. **의존성 주입 패턴** 이해 및 적용
2. **분리된 MongoDB 컨트롤러** 설정 확인
3. **API 모듈화** 시스템 활용
4. **조건부 사이드바** 설정

### 모니터링 포인트
- **분리된 컨트롤러** 별 API 사용량
- **모듈화된 API 호출** 성능
- **상태 초기화** 로직 안정성
- **조건부 UI 렌더링** 성능

### 문제 해결
- **의존성 주입 오류**: 모듈 임포트 경로 및 순환 참조 확인
- **API 모듈화 실패**: axios 설정 및 토큰 인터셉터 확인
- **상태 초기화 실패**: useCallback 의존성 배열 확인
- **사이드바 렌더링 오류**: 경로 조건 및 CSS 클래스 확인

## 보안 고려사항

### 강화된 보안 기능
- **의존성 주입**: 모듈 간 안전한 의존성 관리
- **API 모듈화**: 중앙집중식 인증 및 에러 처리
- **토큰 인터셉터**: 자동 토큰 갱신 및 만료 처리
- **컨트롤러 분리**: 서비스별 독립적 보안 정책

### API 보안 강화
- **표준화된 응답**: 일관된 API 응답 구조
- **중앙집중식 에러 처리**: axios 인터셉터 기반
- **토큰 자동 관리**: localStorage와 HTTP 헤더 동기화
- **경로별 접근 제어**: 조건부 라우팅 및