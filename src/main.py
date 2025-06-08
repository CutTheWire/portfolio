import os
import datetime
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
from fastapi.responses import HTMLResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import Scope, Receive, Send

from utils import ErrorHandler, SmtpController, PageController

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

# ErrorHandler 등록
ErrorHandler.ExceptionManager.register(app)

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
    """Google Search Console 인증 파일"""
    return Response(content="google-site-verification: googlec0f02607421c3396.html", media_type="text/html")

# SEO 관련 엔드포인트들
@app.get("/robots.txt", response_class=Response)
async def robots_txt():
    """검색 엔진 크롤러를 위한 robots.txt"""
    content = """User-agent: *
Allow: /
Allow: /portfolio/
Allow: /static/
Allow: /images/

Sitemap: https://cutwire.myddns.me/sitemap.xml

# 검색 엔진 최적화
Crawl-delay: 1
"""
    return Response(content=content, media_type="text/plain")

@app.get("/sitemap.xml", response_class=Response)
async def sitemap_xml():
    """검색 엔진을 위한 사이트맵 (동적 생성)"""
    
    base_url = "https://cutwire.myddns.me"
    current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    # 마크다운 디렉토리 경로 확인
    markdown_dir_src = SRC_DIR / "markdown"
    markdown_dir_base = BASE_DIR / "markdown"
    
    if markdown_dir_src.exists():
        markdown_dir = markdown_dir_src
    elif markdown_dir_base.exists():
        markdown_dir = markdown_dir_base
    else:
        markdown_dir = markdown_dir_base  # 기본값
    
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
<!-- generated dynamically by FastAPI portfolio server -->

<url>
    <loc>{base_url}/</loc>
    <lastmod>{current_date}</lastmod>
    <priority>1.00</priority>
</url>"""
    
    # 마크다운 파일들을 동적으로 추가
    if markdown_dir.exists():
        for md_file in sorted(markdown_dir.glob("*.md")):
            if md_file.name == "main.md":
                continue  # main.md는 메인 페이지에서 사용되므로 제외
            
            filename_without_ext = md_file.stem
            
            # 파일 수정 시간 가져오기
            try:
                file_mtime = datetime.datetime.fromtimestamp(md_file.stat().st_mtime)
                lastmod = file_mtime.strftime("%Y-%m-%dT%H:%M:%S+00:00")
            except:
                lastmod = current_date
            
            sitemap_content += f"""
<url>
    <loc>{base_url}/portfolio/{filename_without_ext}</loc>
    <lastmod>{lastmod}</lastmod>
    <priority>0.80</priority>
</url>"""
    
    sitemap_content += """

</urlset>"""
    
    return Response(content=sitemap_content, media_type="application/xml")

@app.get("/manifest.json", response_class=Response)
async def manifest_json():
    """PWA 매니페스트 파일"""
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
                "src": "/static/favicon.ico",
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
    """검색 엔진을 위한 구조화된 데이터"""
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "서정훈",
        "jobTitle": "백엔드 개발자",
        "description": "Python, FastAPI, Docker, MongoDB를 활용한 백엔드 개발자. AI 챗봇, 학생관리시스템 등 다양한 프로젝트 경험.",
        "url": "https://cutwire.myddns.me",
        "sameAs": [
            "https://github.com/CutTheWire",
            "https://github.com/TreeNut-KR",
            "https://treenut.ddns.net"
        ],
        "knowsAbout": [
            "Python", "FastAPI", "MongoDB", "Docker", "NginX", "Spring Boot", "MySQL", "백엔드 개발", "API 개발", "웹 개발", "서버 개발"
        ],
        "worksFor": {
            "@type": "Organization",
            "name": "TreeNut"
        },
        "alumniOf": {
            "@type": "CollegeOrUniversity",
            "name": "청운대학교"
        },
        "award": [
            "인천서부소방서장 표창장",
            "능력개발교육원 인공지능 비전인식 기반 협동로봇 제어 수료"
        ],
        "hasOccupation": {
            "@type": "Occupation",
            "name": "Backend Developer",
            "skills": [
                "Python", "FastAPI", "Docker", "MongoDB", "API 설계", "AI 챗봇"
            ]
        }
    }

# 메타 태그 생성 헬퍼 함수
def generate_meta_tags(title="서정훈 포트폴리오", description="Python 백엔드 개발자 서정훈의 포트폴리오", url="https://cutwire.myddns.me"):
    """SEO 메타 태그 생성"""
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

# 404 예외 핸들러 - ACME Challenge 요청은 제외
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # 브라우저/도구 자동 요청 경로들 필터링
        ignored_paths = (
            "/favicon.ico",
            "/robots.txt", 
            "/sitemap.xml",
            "/apple-touch-icon",
            "/manifest.json",
            "/chrome-extension/",
            "/devtools/"
        )
        
        request_path = request.url.path
        
        # 무시할 경로면 조용히 404 응답 (로그 없음)
        if (any(request_path.startswith(p) for p in ignored_paths) or
            request_path in ["/favicon.ico", "/robots.txt", "/sitemap.xml", "/manifest.json"]):
            return HTMLResponse(status_code=404, content="")
        
        # 나머지 404는 ErrorHandler를 통해 로그 기록 후 unauthorized.html로 처리
        ErrorHandler.log_error(
            exc=exc,
            request=request,
            status_code=404,
            detail=f"Route not found: {request.url.path}"
        )
        
        # SEO 메타 태그와 함께 404 페이지 반환
        meta_tags = generate_meta_tags(
            title="페이지를 찾을 수 없습니다 - 서정훈 포트폴리오",
            description="요청하신 페이지를 찾을 수 없습니다. 서정훈의 백엔드 개발자 포트폴리오를 확인해보세요."
        )
        
        return templates.TemplateResponse(
            "unauthorized.html",
            {"request": request, "meta_tags": meta_tags},
            status_code=404
        )
    
    # 기타 HTTP 예외도 ErrorHandler를 통해 처리
    ErrorHandler.log_error(
        exc=exc,
        request=request,
        status_code=exc.status_code,
        detail=exc.detail if hasattr(exc, 'detail') else str(exc)
    )
    
    meta_tags = generate_meta_tags(
        title="오류가 발생했습니다 - 서정훈 포트폴리오",
        description="서비스 이용 중 오류가 발생했습니다. 서정훈의 백엔드 개발자 포트폴리오를 확인해보세요."
    )
    
    return templates.TemplateResponse(
        "unauthorized.html",
        {"request": request, "meta_tags": meta_tags},
        status_code=exc.status_code
    )

@app.get("/favicon.ico")
async def favicon():
    try:
        from fastapi.responses import FileResponse
        # favicon 파일 위치 확인 (static 디렉토리에서)
        favicon_path_src = SRC_DIR / "static" / "favicon.ico"
        favicon_path_base = BASE_DIR / "static" / "favicon.ico"
        
        if favicon_path_src.exists():
            return FileResponse(str(favicon_path_src))
        elif favicon_path_base.exists():
            return FileResponse(str(favicon_path_base))
        else:
            # 파일이 없으면 404 처리
            raise ErrorHandler.NotFoundException("Favicon not found")
    except ErrorHandler.NotFoundException:
        raise
    except Exception as e:
        raise ErrorHandler.InternalServerErrorException("Favicon loading error")

app.include_router(
    PageController.page_router,
    prefix = "",
    tags = ["Page Router"],
    responses = {500: {"description": "Internal Server Error"}}
)

app.include_router(
    SmtpController.smtp_router,
    prefix = "/smtp",
    tags = ["SMTP Router"],
    responses = {500: {"description": "Internal Server Error"}}
)

if __name__ == "__main__":
    load_dotenv()
    # uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
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
    ssl_certfile = certificates_dir / crt_pem
    
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