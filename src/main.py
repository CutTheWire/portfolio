import os
import uvicorn
import asyncio
import logging
import hypercorn.asyncio
from hypercorn.config import Config

from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import Scope, Receive, Send

from app import (
    error_tools,
    smtp_controller,
    portfolio_controller,
)

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# 베이스 디렉토리 설정 (portfolio 루트 디렉토리)
BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = Path(__file__).resolve().parent

class CachedStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs):
        self.cache_max_age = kwargs.pop('cache_max_age', 86400)  # 1일 기본값
        super().__init__(*args, **kwargs)
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # 원본 응답 처리
        response = await super().__call__(scope, receive, send)
        
        # 정적 파일에 대한 캐시 헤더 추가
        if scope["type"] == "http" and scope["method"] == "GET":
            path = scope["path"]
            if any(path.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.woff', '.woff2']):
                # Cache-Control 헤더 설정
                headers = dict(scope.get("headers", []))
                headers[b"cache-control"] = f"public, max-age={self.cache_max_age}".encode()
                scope["headers"] = [(k, v) for k, v in headers.items()]
        
        return response

app = FastAPI(
    title="서정훈 포트폴리오 - 백엔드 개발자",
    description="Python, FastAPI를 활용한 백엔드 개발자 서정훈의 포트폴리오입니다.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

# error_tools 등록
error_tools.ExceptionManager.register(app)

# .well-known 디렉토리 경로 설정 (BASE_DIR 기준)
well_known_path = BASE_DIR / ".well-known"
acme_challenge_path = well_known_path / "acme-challenge"

# 디렉토리가 없으면 생성
if not well_known_path.exists():
    well_known_path.mkdir(parents=True, exist_ok=True)
if not acme_challenge_path.exists():
    acme_challenge_path.mkdir(parents=True, exist_ok=True)

# .well-known 전체를 마운트 (BASE_DIR 기준)
app.mount(
    "/.well-known",
    StaticFiles(directory=str(well_known_path)),
    name="well-known",
)

# static 디렉토리 설정 (src/static 또는 BASE_DIR/static 확인)
static_dir_src = SRC_DIR / "static"
static_dir_base = BASE_DIR / "static"

if static_dir_src.exists():
    static_directory = str(static_dir_src)
elif static_dir_base.exists():
    static_directory = str(static_dir_base)
else:
    # 기본값으로 src/static 사용하고 생성
    static_directory = str(static_dir_src)
    static_dir_src.mkdir(exist_ok=True)

app.mount(
    path="/static",
    app=CachedStaticFiles(directory=static_directory, cache_max_age=2592000),  # 30일 캐시
    name="static"
)

# 이미지 디렉토리 설정 (src/images 또는 BASE_DIR/images 확인)
images_dir_src = SRC_DIR / "images"
images_dir_base = BASE_DIR / "images"

if images_dir_src.exists():
    images_directory = str(images_dir_src)
elif images_dir_base.exists():
    images_directory = str(images_dir_base)
else:
    # 기본값으로 src/images 사용하고 생성
    images_directory = str(images_dir_src)
    images_dir_src.mkdir(exist_ok=True)

app.mount(
    path="/images",
    app=CachedStaticFiles(directory=images_directory, cache_max_age=2592000),  # 30일 캐시
    name="images"
)

# 템플릿 디렉토리 설정
template_dir_src = SRC_DIR / "static"
template_dir_base = BASE_DIR / "static"

if template_dir_src.exists():
    template_directory = str(template_dir_src)
elif template_dir_base.exists():
    template_directory = str(template_dir_base)
else:
    template_directory = str(template_dir_src)

templates = Jinja2Templates(directory=template_directory)

# Google Search Console 인증 파일
@app.get("/googlec0f02607421c3396.html", response_class=Response)
async def google_verification():
    """
    Google Search Console 인증 파일
    """
    return Response(content="google-site-verification: googlec0f02607421c3396.html", media_type="text/html")

# SEO 관련 엔드포인트들
@app.get("/robots.txt", response_class=Response)
async def robots_txt():
    """
    검색 엔진 크롤러를 위한 robots.txt
    """
    content = """User-agent: *
    Allow: /
    Allow: /portfolio/
    Allow: /static/
    Allow: /images/

    # 백엔드 개발자 포트폴리오 사이트맵
    Sitemap: https://cutwire.myddns.me/sitemap.xml

    # 검색 엔진 최적화
    Crawl-delay: 1

    # 중요 페이지 우선순위
    User-agent: Googlebot
    Allow: /
    Allow: /portfolio/chatbot-ai
    Allow: /portfolio/chatbot
    Allow: /portfolio/

    User-agent: Bingbot
    Allow: /
    Allow: /portfolio/

    User-agent: NaverBot
    Allow: /
    Allow: /portfolio/
    """
    return Response(content=content, media_type="text/plain")

@app.get("/manifest.json", response_class=Response)
async def manifest_json():
    """
    PWA 매니페스트 파일
    """
    manifest = {
        "name": "서정훈 포트폴리오 - 백엔드 개발자",
        "short_name": "서정훈 Portfolio",
        "description": "Python, FastAPI를 활용한 백엔드 개발자 서정훈의 포트폴리오",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#000000",
        "icons": [
            {
                "src": "/static/icon/favicon.ico",
                "sizes": "32x32",
                "type": "image/x-icon"
            }
        ],
        "lang": "ko",
        "orientation": "portrait-primary"
    }
    
    import json
    return Response(content=json.dumps(manifest, ensure_ascii=False), media_type="application/json")

# 구조화된 데이터 (JSON-LD) 추가를 위한 헬퍼 함수
def get_structured_data():
    """
    검색 엔진을 위한 구조화된 데이터
    """
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "서정훈",
        "jobTitle": "FastAPI 백엔드 개발자",
        "description": "Python, FastAPI, Docker, MongoDB를 활용한 백엔드 개발자. AI 챗봇, 학생관리시스템 등 다양한 프로젝트 경험.",
        "url": "https://cutwire.myddns.me",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": "https://cutwire.myddns.me",
            "name": "FastAPI 포트폴리오 - 서정훈 백엔드 개발자"
        },
        "sameAs": [
            "https://github.com/CutTheWire",
            "https://github.com/TreeNut-KR",
            "https://treenut.ddns.net"
        ],
        "knowsAbout": [
            "FastAPI 프레임워크", "Python 백엔드 개발", "MongoDB", "Docker", "NginX", "Spring Boot", "MySQL", "백엔드 개발", "API 개발", "웹 개발", "서버 개발"
        ],
        "worksFor": {
            "@type": "Organization",
            "name": "TreeNut",
            "description": "FastAPI 백엔드 개발 전문 팀"
        },
        "alumniOf": {
            "@type": "CollegeOrUniversity",
            "name": "청운대학교",
            "department": "컴퓨터공학과"
        },
        "award": [
            "인천서부소방서장 표창장",
            "능력개발교육원 인공지능 비전인식 기반 협동로봇 제어 수료"
        ],
        "hasOccupation": {
            "@type": "Occupation",
            "name": "FastAPI Backend Developer",
            "skills": [
                "Python", "FastAPI", "Docker", "MongoDB", "API 설계", "AI 챗봇", "백엔드 아키텍처"
            ]
        }
    }

# 메타 태그 생성 헬퍼 함수
def generate_meta_tags(title="서정훈 포트폴리오", description="Python 백엔드 개발자 서정훈의 포트폴리오", url="https://cutwire.myddns.me"):
    """
    SEO 메타 태그 생성
    """
    # 환경변수에서 Google 인증 코드 가져오기
    google_verification = os.getenv("GOOGLE_SITE_VERIFICATION", "")
    
    return {
        "title": title,
        "description": description,
        "keywords": "포트폴리오, portfolio, 백엔드 개발자, backend developer, Python, FastAPI, 웹 개발, API 개발, 서정훈",
        "author": "서정훈",
        "url": url,
        "google_verification": google_verification,  # 환경변수에서 가져온 Google 인증 메타 태그
        "og_title": title,
        "og_description": description,
        "og_url": url,
        "og_type": "website",
        "og_locale": "ko_KR",
        "twitter_card": "summary",
        "twitter_title": title,
        "twitter_description": description,
        "structured_data": get_structured_data()
    }

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    """
    커스텀 404 에러 핸들러
    """
    error_tools.log_error(
        exc=exc,
        request=request,
        status_code=exc.status_code,
        detail=exc.detail if hasattr(exc, 'detail') else str(exc)
    )

    meta_tags = generate_meta_tags(
        title="오류가 발생했습니다 - 서정훈 포트폴리오",
        description="서비스 이용 중 오류가 발생했습니다. 서정훈의 백엔드 포트폴리오를 확인해보세요."
    )

    return templates.TemplateResponse(
        "unauthorized.html",
        {"request": request, "meta_tags": meta_tags},
        status_code=exc.status_code
    )

@app.get("/favicon.ico")
async def favicon():
    """
    Favicon 엔드포인트
    """
    try:
        # static/icon 디렉토리에서 favicon 찾기
        favicon_paths = [
            SRC_DIR / "static" / "icon" / "favicon.ico",
            BASE_DIR / "static" / "icon" / "favicon.ico", 
            SRC_DIR / "static" / "favicon.ico",
            BASE_DIR / "static" / "favicon.ico"
        ]
        
        for favicon_path in favicon_paths:
            if favicon_path.exists():
                return FileResponse(
                    str(favicon_path),
                    media_type="image/x-icon",
                    headers={"Cache-Control": "public, max-age=86400"}
                )
        
        # 파일이 없으면 404 처리
        raise error_tools.NotFoundException("Favicon not found")
    except error_tools.NotFoundException:
        raise
    except Exception as e:
        raise error_tools.InternalServerErrorException("Favicon loading error")

@app.get("/sitemap.xml", response_class=Response)
async def sitemap_xml():
    """
    동적 사이트맵 생성, ./sitemap.xml은 필요 시에 사용 예정.
    """
    try:
        # 기본 URL들
        urls = [
            {
                "loc": "https://cutwire.myddns.me/",
                "lastmod": "2025-06-08",
                "changefreq": "weekly",
                "priority": "1.0"
            }
        ]
        
        # 주요 포트폴리오 페이지들 (우선순위 높음)
        main_portfolios = [
            "chatbot-ai",
            "chatbot", 
            "treenut-chatbot",
            "jmeduserver",
            "docker-optimization"
        ]
        
        for portfolio in main_portfolios:
            urls.append({
                "loc": f"https://cutwire.myddns.me/portfolio/{portfolio}",
                "lastmod": "2025-06-08",
                "changefreq": "monthly",
                "priority": "0.9"
            })
        
        # 마크다운 파일들을 동적으로 추가
        markdown_dir = SRC_DIR / "markdown"
        if markdown_dir.exists():
            for md_file in markdown_dir.glob("*.md"):
                filename = md_file.stem  # 확장자 제거
                if filename not in main_portfolios and filename != "main":
                    urls.append({
                        "loc": f"https://cutwire.myddns.me/portfolio/{filename}",
                        "lastmod": "2025-06-08",
                        "changefreq": "monthly",
                        "priority": "0.7"
                    })
        
        # XML 생성 (공백 없이 시작)
        xml_lines = []
        xml_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        
        for url in urls:
            xml_lines.append('  <url>')
            xml_lines.append(f'    <loc>{url["loc"]}</loc>')
            xml_lines.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
            xml_lines.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
            xml_lines.append(f'    <priority>{url["priority"]}</priority>')
            xml_lines.append('  </url>')
        
        xml_lines.append('</urlset>')
        
        xml_content = '\n'.join(xml_lines)
        
        return Response(
            content=xml_content,
            media_type="application/xml",
            headers={
                "Cache-Control": "public, max-age=3600",
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except Exception as e:
        # 정적 파일로 폴백
        sitemap_path = SRC_DIR / "sitemap.xml"
        if sitemap_path.exists():
            return FileResponse(str(sitemap_path), media_type="application/xml")
        else:
            raise error_tools.NotFoundException("sitemap.xml not found")

app.include_router(
    portfolio_controller.page_router,
    prefix = "",
    tags = ["Page Router"],
    responses = {500: {"description": "Internal Server Error"}}
)

app.include_router(
    smtp_controller.smtp_router,
    prefix = "/smtp",
    tags = ["SMTP Router"],
    responses = {500: {"description": "Internal Server Error"}}
)

if __name__ == "__main__":
    load_dotenv()
    # uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True) # 개발 모드에서 실행
    logging.basicConfig(level=logging.INFO, format=f"{GREEN}INFO{RESET}:     %(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("hypercorn")

    key_pem = os.getenv("KEY_PEM")
    crt_pem = os.getenv("CRT_PEM")
    
    # pathlib를 사용하여 certificates 디렉토리 경로 설정 (src/certificates 확인)
    certificates_dir_src = SRC_DIR / "certificates"
    certificates_dir_base = BASE_DIR / "certificates"
    
    if certificates_dir_src.exists():
        certificates_dir = certificates_dir_src
    elif certificates_dir_base.exists():
        certificates_dir = certificates_dir_base
    else:
        certificates_dir = certificates_dir_src  # 기본값
    
    ssl_keyfile = certificates_dir / key_pem
    ssl_certfile = certificates_dir / crt_pem  # 반드시 체인 포함 PEM 지정

    if not ssl_keyfile.is_file() or not ssl_certfile.is_file():
        raise FileNotFoundError("SSL 인증서 파일을 찾을 수 없습니다. 경로를 확인하세요.")
    
    config = Config()
    config.bind = ["0.0.0.0:443"]
    config.certfile = str(ssl_certfile)
    config.keyfile = str(ssl_keyfile)
    config.alpn_protocols = ["h2", "http/1.1"]  # HTTP/2 활성화
    config.accesslog = "-"  # 요청 로그 활성화

    async def serve():
        logger.info("Starting Hypercorn server...")
        await hypercorn.asyncio.serve(app, config)
        
    asyncio.run(serve())