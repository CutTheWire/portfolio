> AI 기반 챗봇 API 프로젝트입니다.  
> FastAPI 기반의 Office/Character API 서버와 Llama 기반 AI 모델을 Docker로 통합 운영합니다.

[github-link](https://github.com/TreeNut-KR/ChatBot-AI)

# 프로젝트 구성원

| 구성원 | 업무 | 사용 기술 |  
|--------|--------|------------|  
| ✅ [서정훈 (CutTheWire)](https://github.com/CutTheWire) | 프로젝트 매니저, 백엔드 | FastAPI, Llama CPP CUDA |  

## 👨‍💻 담당 업무
- 전체 시스템 아키텍처 설계
- FastAPI 전체 API 서버 개발
- OpenAI, Venice API 연동
- FastAPI Llama 모델 연동
- 두개의 로컬 GPU(RTX 2080 8GB, RTX 3060 12GB)를 Docker에서 분리, 마이크로 서비스 형태(Office, Character)로 Llama 모델 할당 운용
- Nginx 8001 포트에서 모든 요청을 받아, /office/ 경로는 Office API 서버(8002)로, /character/ 경로는 Character API 서버(8003)로 처리
- MongoDB 채팅방 대화 내용 기반 답변 생성 기능
- 간트 차트, Hybrid ERD, 다이어그램 및 문서화 작업

## 📁 프로젝트 디렉토리 구조
> 파일을 클릭하면 해당 GitHub에 main 브런치 기준 파일로 이동합니다.

### 📦 루트 디렉토리 구조
<pre data-owner="TreeNut-KR" data-repo="ChatBot-AI" data-folder=""><code class="language-directory">
 ┣ 📜[.env](None)
 ┣ 📜.gitignore
 ┣ 📜CODE_OF_CONDUCT.md
 ┣ 📜docker-compose.yml
 ┣ 📜LICENSE
 ┣ 📜README.md
 ┗ 📜rebuild.bat
</code></pre>

### 📦 fastapi 디렉토리 구조
<pre data-owner="TreeNut-KR" data-repo="ChatBot-AI" data-folder="fastapi"><code class="language-directory">
 ┣ 📂ai_model
 ┃ ┣ 📂QuantFactory
 ┃ ┃ ┣ 📜[Meta-Llama-3.1-8B-Claude.Q4_0.gguf](https://huggingface.co/QuantFactory/Meta-Llama-3.1-8B-Claude-GGUF/blob/main/Meta-Llama-3.1-8B-Claude.Q4_0.gguf)
 ┃ ┃ ┗ 📜[Meta-Llama-3.1-8B-Claude.Q4_1.gguf](https://huggingface.co/QuantFactory/Meta-Llama-3.1-8B-Claude-GGUF/blob/main/Meta-Llama-3.1-8B-Claude.Q4_1.gguf)
 ┃ ┗ 📜README.md
 ┣ 📂batch
 ┃ ┣ 📜venv_install.bat
 ┃ ┗ 📜venv_setup.bat
 ┣ 📂certificates
 ┃ ┣ 📜DNS_README.md
 ┃ ┗ 📜PEM_README.md
 ┣ 📂logs
 ┣ 📂prompt
 ┃ ┣ 📜config-Llama.json
 ┃ ┣ 📜config-OpenAI.json
 ┃ ┗ 📜config-Venice.json
 ┣ 📂src
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📂character
 ┃ ┃ ┃ ┗ 📜llm_controller.py
 ┃ ┃ ┣ 📂office
 ┃ ┃ ┃ ┗ 📜llm_controller.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂core
 ┃ ┃ ┣ 📂character
 ┃ ┃ ┃ ┗ 📜app_state.py
 ┃ ┃ ┣ 📂office
 ┃ ┃ ┃ ┗ 📜app_state.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂docs
 ┃ ┃ ┗ 📜api_specification.md
 ┃ ┣ 📂domain
 ┃ ┃ ┣ 📂character
 ┃ ┃ ┃ ┣ 📜config.py
 ┃ ┃ ┃ ┗ 📜schema.py
 ┃ ┃ ┣ 📂office
 ┃ ┃ ┃ ┣ 📜config.py
 ┃ ┃ ┃ ┗ 📜schema.py
 ┃ ┃ ┣ 📂shared
 ┃ ┃ ┃ ┣ 📜base_config.py
 ┃ ┃ ┃ ┣ 📜error_tools.py
 ┃ ┃ ┃ ┣ 📜mongodb_client.py
 ┃ ┃ ┃ ┣ 📜queue_tools.py
 ┃ ┃ ┃ ┗ 📜search_adapter.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂llm
 ┃ ┃ ┣ 📂llama
 ┃ ┃ ┃ ┣ 📜character.py
 ┃ ┃ ┃ ┗ 📜office.py
 ┃ ┃ ┣ 📂openai
 ┃ ┃ ┃ ┣ 📜character.py
 ┃ ┃ ┃ ┗ 📜office.py
 ┃ ┃ ┣ 📂venice
 ┃ ┃ ┃ ┗ 📜character.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂server
 ┃ ┃ ┣ 📂character
 ┃ ┃ ┃ ┣ 📜Dockerfile
 ┃ ┃ ┃ ┗ 📜server.py
 ┃ ┃ ┗ 📂office
 ┃ ┃ ┃ ┣ 📜Dockerfile
 ┃ ┃ ┃ ┗ 📜server.py
 ┃ ┣ 📂test
 ┃ ┃ ┣ 📂performance_results
 ┃ ┃ ┃ ┗ 📜visualization.html
 ┃ ┃ ┣ 📜test.bat
 ┃ ┃ ┣ 📜test_character_load.py
 ┃ ┃ ┗ 📜test_office_load.py
 ┃ ┣ 📜[.env](None)
 ┃ ┣ 📜bot.yaml
 ┃ ┣ 📜Dockerfile.base
 ┃ ┣ 📜Dockerfile.libs
 ┃ ┗ 📜install_libs.sh
 ┣ 📜.dockerignore
 ┣ 📜requirements.txt
 ┗ 📜requirements_llama.txt
</code></pre>

### 📦 nginx 디렉토리 설명
<pre data-owner="TreeNut-KR" data-repo="ChatBot-AI" data-folder="nginx"><code class="language-directory">
 ┣ 📜404.html
 ┗ 📜nginx.conf
</code></pre>

## 🏗️ 전체 아키텍처

- **office**: 업무용 챗봇 API (FastAPI, 8002)
- **character**: 캐릭터 챗봇 API (FastAPI, 8003)
- **nginx**: API Gateway (8001, reverse proxy, 커스텀 404 지원)
- **python-libs-init**: 공통 Python 라이브러리 볼륨 초기화

## 📋 시스템 아키텍처 다이어그램
![System-Architecture-Diagram-ChatBot](/media/webp/System-Architecture-Diagram-ChatBot.webp)

## 📋 패키지 다이어그램 
![Package-Diagram-ChatBot(AI)](/media/webp/Package-Diagram-ChatBot(AI).webp)

## 🌐 API Gateway (nginx) 구조

- **8001 포트**에서 모든 API를 통합 제공
- `/office/` → office 서버(8002)로 프록시
- `/character/` → character 서버(8003)로 프록시
- 존재하지 않는 경로는 `/404.html` 커스텀 페이지 반환

## 📊 요청 성능
- **v1.7.4** 버전 기준
- **측정 일자**: 2025-07-12 (토) 15:08:57 GMT+0900 (한국 표준시)

<div class="project-link-content">
    <a href="/visualization/chatbot-ai" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">성능차트 상세보기</span>
    </a>
</div>

## 📅 개발 로드맵 및 버전 릴리즈 일정

### 간트 차트 (ChatBot AI 버전 릴리즈)
![Gantt-Chart-ChatBot(AI)](/media/webp/Gantt-Chart-ChatBot(AI).webp)

### 주요 마일스톤

| 버전 | 기간 | 주요 성과 | 아키텍처 변화 |
|------|------|-----------|---------------|
| **v1.0.x** | 2024.09-2024.10 | 단일 Llama 모델, 스트리밍 지원 | Transformers 기반 스트리밍 |
| **v1.1.x** | 2024.10-2025.01 | 듀얼 GPU 구성, Bllossom 모델 추가 | Llama + Bllossom 멀티모델 |
| **v1.2.x** | 2025.01-2025.02 | Lumimaid GGUF 전환 | 성능 최적화 (GGUF) |
| **v1.3.x** | 2025.02 | DuckDuckGo 검색 API 연동 | 외부 검색 통합 |
| **v1.4.x** | 2025.02-2025.03 | SSL/TLS 보안, 인증서 관리 | HTTPS 프로덕션 환경 |
| **v1.5.x** | 2025.03-2025.04 | 라우터 분리, OpenAI 모델 추가 | 하이브리드 API 아키텍처 |
| **v1.6.x** | 2025.04-2025.05 | MVC 구조, GitHub Actions | 체계적인 개발 파이프라인 |
| **v1.7.x** | 2025.05-2025.06 | Docker 컨테이너화, nginx 게이트웨이 | 마이크로서비스 완성 |

### 개발 통계

- **총 개발 기간**: 9개월 (2024.09 ~ 2025.06)
- **메이저 버전**: 8개 (v1.0.x ~ v1.7.x)
- **릴리즈 횟수**: 20회
- **주요 기술 전환**: 4회 (단일→듀얼→GGUF→마이크로서비스)

### 📄 v1.0.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.0.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- `First Commit Days` : 2024-10-19 (토) 23:02:45 GMT+0900 (한국 표준시)
- `Last Commit Days` : 2024-12-16 (월) 18:22:23 GMT+0900 (한국 표준시)

### 📄 v1.1.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.1.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- `First Commit Days` : 2025-01-15 (수) 15:40:49 GMT+0900 (한국 표준시)

### 📄 v1.2.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.2.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- `First Commit Days` : 2025-02-18 (화) 10:42:34 GMT+0900 (한국 표준시)

### 📄 v1.3.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.3.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- `First Commit Days` : 2025-02-18 (화) 11:26:36 GMT+0900 (한국 표준시)
- `Last Commit Days` : 2024-03-15 (토) 15:44:49 GMT+0900 (한국 표준시)

### 📄 v1.4.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.4.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- `First Commit Days` : 2024-03-15 (토) 15:47:20 GMT+0900 (한국 표준시)
- `Last Commit Days` : 2024-03-16 (일) 18:24:02 GMT+0900 (한국 표준시)

### 📄 v1.5.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.5.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- `First Commit Days` : 2024-03-21 (금) 15:41:35 GMT+0900 (한국 표준시)
- `Last Commit Days` : 2024-05-03 (토) 18:56:29 GMT+0900 (한국 표준시)

### 📄 v1.6.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.6.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- `First Commit Days` : 2024-05-10 (토) 04:43:23 GMT+0900 (한국 표준시)
- `Last Commit Days` : 2024-05-16 (금) 01:30:44 GMT+0900 (한국 표준시)

### 📄 v1.7.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.7.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- `First Commit Days` : 2024-05-30 (금) 19:19:05 GMT+0900 (한국 표준시)
- `Last Commit Days` : 2024-06-16 (월) 16:36:43 GMT+0900 (한국 표준시)
