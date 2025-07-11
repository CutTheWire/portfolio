# ChatBot - 버전 명세서 v1.1.x

## 개요
이 문서는 ChatBot 시스템의 v1.1.x 계열 버전에 대한 공식 명세서입니다. v1.0.x의 Flyway 기반 데이터베이스 마이그레이션 시스템에서 **프론트엔드 모바일 UI 최적화**와 **문서화 개선**, **오류 수정**을 중심으로 한 **사용자 경험 개선** 버전입니다.

## 버전 정보

| 버전 | 릴리즈 날짜 | 커밋 해시 | 상태 |
|------|-------------|-----------|------|
| **v1.1.0** | 2025-06-19 | `0dd8bd16` | Stable |
| **v1.1.1** | 2025-07-10 | `6a0aaa4a` | Latest |

## v1.0.x에서 v1.1.x로의 주요 변경사항

### 프론트엔드 사용자 경험 개선
- **데스크톱 중심** → **모바일 반응형 UI** 최적화
- **채팅 인터페이스** UX/UI 대폭 개선
- **토스트 알림** 시스템 간격 및 크기 조정

### 개발 환경 및 문서화 개선
- **GitHub Actions** 빌드 시스템 최적화
- **API 명세서** 자동화 개선
- **사용자 가이드** 문서 추가

### 버그 수정 및 안정성 강화
- **FastAPI 에러 로깅** 시스템 개선
- **채팅 전송** 오류 수정
- **모바일 환경** 호환성 강화

### 신규 기능
- **재전송 기능** 추가 (채팅 실패 시)
- **모바일 UI** 터치 최적화
- **이미지 업로드** PNG 누락 내용 보완

### 제거된 기능
- ❌ **구 버전 config** 파일 정리
- ❌ **불필요한 코드** 제거

## 시스템 요구사항

### 하드웨어 요구사항
- **CPU**: 멀티코어 프로세서 권장
- **메모리**: 최소 16GB RAM
- **저장공간**: 최소 30GB 여유 공간
- **네트워크**: 고속 인터넷 (API 연동)

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
📦 ChatBot v1.1.x
├── 📁 .github/                  # GitHub Actions
│   └── 📁 workflows/
│       └── build-and-push.yml [UPDATED v1.1.1]
├── 📁 fastapi/                  # FastAPI 서비스
│   └── 📁 src/
│       └── 📁 utils/
│           └── error_tools.py [UPDATED v1.1.1]
├── 📁 nginx/                    # React 프론트엔드
│   └── 📁 react-frontpage/      # React 애플리케이션
│       └── 📁 src/
│           ├── 📁 Component/
│           │   └── 📁 Chatting/
│           │       ├── Chatting.tsx [UPDATED v1.1.1]
│           │       └── 📁 Components/
│           │           ├── ChatFooter.tsx [UPDATED v1.1.1]
│           │           └── Toast.tsx [UPDATED v1.1.1]
│           └── tailwind.output.css [UPDATED v1.1.1]
├── 📁 springboot/               # Spring Boot 서비스
│   └── 📁 src/docs/             # API 문서
│       ├── CharacterController.md [UPDATED v1.1.1]
│       ├── RoomController.md [UPDATED v1.1.1]
│       └── UserController.md [UPDATED v1.1.1]
└── README.md [UPDATED]
```

## API 명세

### Spring Boot API (기존 API 유지)

#### 사용자 관리 API (`/api/users`)
기본적인 사용자 관리 기능을 제공합니다.

##### POST /api/users/register
사용자 회원가입 API

##### DELETE /api/users/{id}
사용자 삭제 API

#### 캐릭터 관리 API (`/api/characters`)
캐릭터 생성, 조회, 수정, 삭제 기능을 제공합니다.

##### POST /api/characters
캐릭터 생성 API

##### GET /api/characters
캐릭터 목록 조회 API

##### PUT /api/characters/{id}
캐릭터 수정 API

##### DELETE /api/characters/{id}
캐릭터 삭제 API

#### 채팅방 관리 API (`/api/rooms`)
채팅방 생성 및 관리 기능을 제공합니다.

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

### FastAPI API (기존 API 유지)

#### MongoDB 라우터 (`/mongo`)
MongoDB 연동 API를 제공합니다.

##### POST /mongo/office/create
Office 채팅방 문서 생성

##### PUT /mongo/office/save_log
Office 채팅 로그 저장

##### POST /mongo/chatbot/create
Chatbot 채팅방 문서 생성

##### PUT /mongo/chatbot/save_log
Chatbot 채팅 로그 저장

**HTTP 상태 코드:**
- `200`: 성공
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `422`: 유효성 검사 실패
- `500`: 서버 내부 오류

## 주요 컴포넌트

### 1. React 프론트엔드 - v1.1.x 모바일 최적화

#### Chatting.tsx - 채팅 컴포넌트 대폭 개선
사용자 경험을 향상시킨 채팅 인터페이스입니다.

**v1.1.1 주요 개선사항:**
- **모델 변경 처리**: useRef를 사용한 안전한 모델 참조
- **중복 전송 방지**: 로딩 상태 체크로 중복 요청 차단
- **채팅방 자동 생성**: roomId가 없을 경우 자동 생성
- **향상된 오류 처리**: 채팅방 생성 실패 시 적절한 피드백

```typescript
// v1.1.1 개선된 모델 참조 시스템
const [model, setModel] = useState<string>('Llama');
const modelRef = useRef(model);

useEffect(() => {
  modelRef.current = model;
}, [model]);

// 안전한 AI 응답 호출
const aiResponse = await getChatResponse(
  roomId, 
  message.text, 
  modelRef.current, // 최신 모델 값 보장
  googleAccess
);
```

**채팅방 관리 개선:**
- **자동 방 생성**: roomId가 없을 경우 자동으로 새 채팅방 생성
- **URL 동기화**: 페이지 URL에 roomId 자동 업데이트
- **오류 처리**: 채팅방 생성 실패 시 사용자에게 알림

```typescript
// v1.1.1 채팅방 자동 생성 로직
if (!roomId || !urlRoomId) {
  try {
    const responseData = await createNewChatRoom();
    roomId = responseData.mysql_officeroom.mongo_chatroomid;
    setCookie('mongo_chatroomid', roomId);
    
    const pageUrl = new URL(window.location.href);
    pageUrl.searchParams.set('roomId', roomId);
    window.history.replaceState({}, document.title, pageUrl.toString());
  } catch (error) {
    showToast('채팅방을 생성할 수 없습니다.', 'error');
    setIsLoading(false);
    return;
  }
}
```

#### ChatFooter.tsx - 입력 인터페이스 개선
모바일 환경에 최적화된 채팅 입력 시스템입니다.

**v1.1.1 주요 개선사항:**
- **멀티라인 입력**: input → textarea로 변경
- **자동 높이 조절**: 입력 내용에 따라 동적 크기 조정
- **키보드 단축키**: Enter(전송), Shift+Enter/Alt+Enter(줄바꿈)
- **모바일 최적화**: 터치 환경에서의 입력 편의성 향상

```typescript
// v1.1.1 멀티라인 textarea 구현
<textarea
  className="
    flex-1 px-3 py-1 rounded-lg bg-gray-900 text-white outline-none caret-white 
    border border-gray-700 focus:border-indigo-500 transition text-base
    sm:px-4 sm:py-1 resize-none sm:h-auto
  "
  style={{ 
    minWidth: 0, 
    minHeight: 36, 
    maxHeight: 120, 
    height: 'auto', 
    overflowY: 'auto' 
  }}
  rows={1}
  onInput={e => {
    const target = e.target as HTMLTextAreaElement;
    target.style.height = 'auto';
    target.style.height = `${target.scrollHeight}px`;
  }}
  onKeyDown={(e) => {
    if (e.key === 'Enter' && !e.altKey && !e.shiftKey) {
      e.preventDefault();
      if (!isLoading && userInput.trim()) {
        handleSubmit(e as any);
      }
    }
    // Alt+Enter 또는 Shift+Enter는 줄바꿈 허용
  }}
  // ... 기타 props
/>
```

#### Toast.tsx - 알림 시스템 개선
사용자 피드백을 위한 토스트 알림 시스템이 개선되었습니다.

**v1.1.1 주요 개선사항:**
- **간격 조정**: 토스트 간 간격을 64px → 80px로 증가
- **크기 표준화**: 최소 너비 320px, 최소 높이 56px 보장
- **가독성 향상**: 모바일 환경에서의 가독성 개선

```typescript
// v1.1.1 토스트 간격 및 크기 개선
const MOBILE_GAP = 80; // px, 토스트 간 간격 (64 → 80으로 증가)
const PC_GAP = 80; // px, 토스트 간 간격 (64 → 80으로 증가)

// 토스트 컴포넌트 스타일링
<div className="
  transition-opacity duration-500 max-w-xs min-w-[320px] min-h-[56px]
  // ... 기타 스타일
">
```

### 2. FastAPI 백엔드 - v1.1.x 로깅 개선

#### error_tools.py - 로깅 시스템 개선 - 서정훈
로그 파일 경로 및 디렉토리 구조가 개선되었습니다.

**v1.1.1 주요 개선사항:**
- **경로 수정**: BASE_DIR 계산을 3단계 상위로 변경
- **로그 디렉토리**: 프로젝트 루트의 logs 폴더로 통일

```python
# v1.1.1 경로 구조 개선
BASE_DIR = Path(__file__).resolve().parents[3]  # 2 → 3으로 변경
os.makedirs(LOG_DIR, exist_ok=True)

# 로그 파일 생성 및 관리
class DailyRotatingFileHandler(logging.handlers.BaseRotatingHandler):
    def __init__(self, dir_path: str, date_format: str = "%Y%m%d", encoding=None):
        self.dir_path = dir_path
        self.date_format = date_format
        self.current_date = datetime.now().strftime(self.date_format)
        log_file = os.path.join(dir_path, f"error_{self.current_date}.log")
        super().__init__(log_file, 'a', encoding)
```

### 3. GitHub Actions 개선 - v1.1.x

#### build-and-push.yml - 빌드 시스템 최적화 - 서정훈
Docker 이미지 빌드 과정이 개선되었습니다.

**v1.1.1 주요 개선사항:**
- **FastAPI Dockerfile 경로**: 명시적 경로 지정으로 빌드 안정성 향상
- **Flyway 이미지 지원**: 데이터베이스 마이그레이션 컨테이너 추가

```yaml
# v1.1.1 FastAPI 빌드 개선
- name: Build and push FastAPI image
  uses: docker/build-push-action@v3
  with:
    context: .
    file: ./fastapi/src/server/Dockerfile  # 명시적 경로 지정
    push: true
    tags: |
      ghcr.io/treenut-kr/fastapi:latest
      ghcr.io/treenut-kr/fastapi:${{ github.ref_name }}

# v1.1.1 Flyway 지원 추가
- name: Create custom Flyway Dockerfile
  run: |
    cat > flyway.Dockerfile << 'EOF'
    FROM flyway/flyway:7.15.0
    
    # 마이그레이션 파일과 스크립트 복사 (실행 권한 포함)
    COPY ./mysql/migrations /flyway/sql
    COPY --chmod=755 ./mysql/flyway-migrate.sh /flyway/flyway-migrate.sh
    
    # 엔트리포인트 설정
    ENTRYPOINT ["/bin/bash", "/flyway/flyway-migrate.sh"]
    EOF
```

### 4. 문서화 시스템 - v1.1.x 개선

#### API 컨트롤러 문서 업데이트
모든 Spring Boot 컨트롤러의 문서가 개선되었습니다.

##### RoomController.md - 서정훈
불필요한 코드 블록을 제거하여 가독성을 향상시켰습니다.

##### UserController.md
사용자 컨트롤러 문서에 개요가 추가되었습니다.

##### CharacterController.md
PNG 이미지 업로드 관련 누락된 내용이 추가되었습니다.

```markdown
## 개요
이 문서는 사용자 관리를 위한 REST API 컨트롤러의 명세를 설명합니다.

### 주요 기능
- 사용자 등록 및 인증
- 프로필 관리
- 권한 관리

### API 엔드포인트
... (상세 내용)
```

## 설치 및 설정

### Docker 기반 통합 배포 시스템

#### 환경 구성
1. **Docker & Docker Compose** 설치
2. **React 빌드** 환경 구성
3. **환경 변수** 설정 (.env 파일)
4. **Flyway 마이그레이션** 설정

#### 빠른 시작
```bash
# 1. 리포지토리 클론
git clone https://github.com/TreeNut-KR/ChatBot.git
cd ChatBot

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일에서 데이터베이스 설정

# 3. React 앱 빌드
cd nginx/react-frontpage
npm install
npm run build
cd ../..

# 4. 컨테이너 빌드 및 실행
docker-compose up --build

# 5. 서비스 접근 확인
# 메인 웹사이트: http://localhost
# Spring Boot API: http://localhost:8080
# FastAPI: http://localhost:8000
```

#### 서비스 포트 설정
- **nginx (React 앱)**: 80
- **Spring Boot**: 8080
- **FastAPI**: 8000
- **MySQL**: 3308
- **MongoDB**: 27017

## 운영 가이드

### 환경 설정
1. **React 개발 환경** 구성 (Node.js 18+)
2. **모바일 테스트** 환경 설정
3. **데이터베이스** 초기화 및 스키마 설정
4. **Flyway 마이그레이션** 실행

### 모니터링 포인트
- **React 앱** 빌드 및 배포 상태
- **모바일 UI** 사용자 경험 지표
- **채팅 기능** 성공률 및 응답 시간
- **토스트 알림** 표시 정확성
- **오류 로그** 발생 빈도

### 문제 해결
- **React 빌드 실패**: Node.js 버전 및 의존성 확인
- **모바일 UI 문제**: 반응형 CSS 및 터치 이벤트 확인
- **채팅 전송 실패**: 네트워크 연결 및 API 엔드포인트 확인
- **로그 파일 문제**: 디렉토리 권한 및 경로 설정 확인

## 보안 고려사항

### 강화된 보안 기능
- **프론트엔드 보안**: XSS 방지 및 입력 검증
- **모바일 보안**: 터치 이벤트 보안 처리
- **로그 보안**: 민감 정보 로깅 방지
- **API 보안**: 요청 검증 및 에러 처리

### 사용자 경험 보안
- **입력 검증**: 클라이언트 사이드 검증 강화
- **세션 관리**: 모바일 환경에서의 세션 유지
- **데이터 보호**: 로컬 스토리지 보안 관리
- **네트워크