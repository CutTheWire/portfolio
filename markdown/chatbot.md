# 프로젝트 구성원

| 구성원 | 업무 | 사용 기술 |  
|--------|--------|------------|  
| 김준건 (jgkim14) | 백엔드 | Spring Boot, Node.js |  
| [서정훈 (CutTheWire)](https://github.com/CutTheWire) | 백엔드 | Spring Boot, FastAPI |  
| 이준호 (qwer9679) | 백엔드 | Spring Boot, FastAPI |  
| 모현준 (Flattt12) | 백엔드 | Spring Boot |  
| 권재현 (donismoney) | 백엔드 | Spring Boot |  
| 손유노 (GingGang) | 프론트엔드 | React, TypeScript |

# 시스템 아키텍처 다이어그램
![System-Architecture-Diagram-ChatBot](/images/System-Architecture-Diagram-ChatBot.webp)

### 도커 컨테이너 및 이미지 모두 삭제 후 자동 재빌드

#### 1. Linux, Mac OS
```bash

source ./rebuild.sh
```

#### 2. Windows OS
```bash

 & ./rebuild.bat
```

#### - FastAPI 작업영역
`./fastapi/sources`
#### - 프론트 작업영역
`./nginx/frontpage-react`
#### - 프론트 빌드파일 경로
`./frontpage-react/build`
