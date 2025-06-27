
> AI 기반 챗봇 API 프로젝트입니다.  
> FastAPI 기반의 Office/Character API 서버와 Llama 기반 AI 모델을 Docker로 통합 운영합니다.

[github-link](https://github.com/TreeNut-KR/ChatBot-AI)

## 🏗️ 전체 아키텍처

- **office**: 업무용 챗봇 API (FastAPI, 8002)
- **character**: 캐릭터 챗봇 API (FastAPI, 8003)
- **nginx**: API Gateway (8001, reverse proxy, 커스텀 404 지원)
- **python-libs-init**: 공통 Python 라이브러리 볼륨 초기화

## 🌐 API Gateway (nginx) 구조

- **8001 포트**에서 모든 API를 통합 제공
- `/office/` → office 서버(8002)로 프록시
- `/character/` → character 서버(8003)로 프록시
- 존재하지 않는 경로는 `/404.html` 커스텀 페이지 반환

## 🗓️ 버전별 명세
### 📄 v1.0.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.0.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- Last Commit Hash : `3071c6319a6e96e695d49f111bfbba5aea603f49`
- Last Commit Days : 2024-12-16 (화) 15:48:19 (KST)


### 📄 v1.1.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.1.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- Last Commit Hash : `d014744640fa72366c398541ec9f5b4c7361fd7f`
- Last Commit Days : 2025-01-15 (수) 15:40:49 (KST)

### 📄 v1.2.x
<div class="project-link-content">
    <a href="/portfolio/reference/chatbot-ai/version(1.2.x).md" class="project-link-card dark">
        <i class="fas fa-external-link-alt project-link-icon"></i>
        <span class="project-link-text">명세 상세보기</span>
    </a>
</div>

- Last Commit Hash : `cba10b2cebceaf36d2836c9e9e0bb5fcaf37dffd`
- Last Commit Days : 2025-02-18 (수) 10:42:34 (KST)


## 📋 시스템 아키텍처 다이어그램
![System-Architecture-Diagram-ChatBot](/images/System-Architecture-Diagram-ChatBot.webp)

## 📋 패키지 다이어그램 
![Package-Diagram-ChatBot(AI)](/images/Package-Diagram-ChatBot(AI).webp)
