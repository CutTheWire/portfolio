[github-link](https://github.com/TreeNut-KR/ChatBot)

# 프로젝트 구성원

| 구성원 | 업무 | 사용 기술 |  
|--------|--------|------------|  
| 김준건 (jgkim14) | 백엔드 | Spring Boot, Node.js |  
| [서정훈 (CutTheWire)](https://github.com/CutTheWire) | 백엔드 | Spring Boot, FastAPI |  
| 이준호 (qwer9679) | 백엔드 | Spring Boot, FastAPI |  
| 모현준 (Flattt12) | 백엔드 | Spring Boot |  
| 권재현 (donismoney) | 백엔드 | Spring Boot |  
| 손유노 (GingGang) | 프론트엔드 | React, TypeScript |

## 🏗️ 전체 아키텍처

- **nginx**: API Gateway 및 웹 서버 (443 포트, HTTPS 지원)
    - React 프론트엔드 정적 파일 서빙
    - FastAPI/Spring Boot 백엔드 프록시 역할
- **fastapi**: Python 백엔드 API 서버 (8000 포트)
    - FastAPI 프레임워크 기반
    - MySQL/MongoDB 연동
- **springboot**: Java 백엔드 API 서버 (8080 포트)
    - Spring Boot 프레임워크 기반
    - MySQL 연동
- **admincontroller**: Node.js 관리자 컨트롤러 (5785 포트)
    - Google Cloud 서비스 연동
    - 시스템 관리 기능
- **mysql**: 관계형 데이터베이스 (3308 포트)
    - UTF8MB4 문자셋 지원
    - Flyway를 통한 스키마 마이그레이션
- **mongodb**: NoSQL 데이터베이스 (27017 포트)
    - 문서 기반 데이터 저장
    - Google Cloud 인증 지원
- **flyway**: 데이터베이스 마이그레이션 도구
    - MySQL 스키마 버전 관리

## 📋 시스템 아키텍처 다이어그램
![System-Architecture-Diagram-ChatBot](/images/System-Architecture-Diagram-ChatBot.webp)

## 🌐 API Gateway (nginx) 구조

- **443 포트**에서 HTTPS로 모든 요청을 통합 처리
- **SSL/TLS 보안**: TLSv1.2, TLSv1.3 지원으로 암호화 통신
- **정적 파일 서빙**: React 빌드 결과물과 정적 리소스 제공
    - `/static/` → 정적 파일 (7일 캐시)
    - CSS, JS, 이미지 파일 등 (30일 캐시)
- **API 라우팅**:
    - `/` → React SPA (index.html 폴백)
    - `/sub/` → FastAPI 서버(8000)로 프록시
    - `/server` → Spring Boot 서버(8080)로 프록시
- **OAuth 인증 처리**:
    - `/auth/` → 인증 관련 요청 처리
    - Google, Facebook 등 외부 인증 제공자와 연동
    - JWT 토큰 발급 및 검증
- **CORS 설정**:
    - 모든 도메인에서의 요청 허용
    - 인증 정보 포함 요청에 대한 처리
- **에러 핸들링**:
    - 404 에러 페이지 설정
    - 서버 에러 시 일반화된 에러 메시지 반환

## 🗓️ 버전별 명세
