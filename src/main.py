import os
import uvicorn

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import Scope, Receive, Send

from utils import ErrorHandler, SmtpController, PageController

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
    title="서정훈 포트폴리오",
    docs_url=None,
    redoc_url=None,
)

# ErrorHandler 등록
ErrorHandler.ExceptionManager.register(app)

# 기존 StaticFiles를 CachedStaticFiles로 교체
app.mount(
    path="/static",
    app=CachedStaticFiles(directory="static", cache_max_age=2592000),  # 30일 캐시
    name="static"
)

# 이미지 디렉토리 추가 (로컬 이미지용)
if not os.path.exists("images"):
    os.makedirs("images")

app.mount(
    path="/images",
    app=CachedStaticFiles(directory="images", cache_max_age=2592000),  # 30일 캐시
    name="images"
)

templates = Jinja2Templates(directory="static")

# 404 예외 핸들러 - ErrorHandler를 사용하도록 개선
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # 브라우저/도구 자동 요청 경로들 필터링 (더 포괄적)
        ignored_paths = (
            "/.well-known/",
            "/favicon.ico",
            "/robots.txt", 
            "/sitemap.xml",
            "/apple-touch-icon",
            "/manifest.json",
            "/chrome-extension/",
            "/devtools/",
            "/.well-known/appspecific/"
        )
        
        # 정확한 경로 매칭을 위해 startswith와 exact match 모두 확인
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
        
        return templates.TemplateResponse(
            "unauthorized.html",
            {"request": request},
            status_code=404
        )
    
    # 기타 HTTP 예외도 ErrorHandler를 통해 처리
    ErrorHandler.log_error(
        exc=exc,
        request=request,
        status_code=exc.status_code,
        detail=exc.detail if hasattr(exc, 'detail') else str(exc)
    )
    
    return templates.TemplateResponse(
        "unauthorized.html",
        {"request": request},
        status_code=exc.status_code
    )

@app.get("/favicon.ico")
async def favicon():
    try:
        from fastapi.responses import FileResponse
        favicon_path = os.path.join("static", "favicon.ico")
        if os.path.exists(favicon_path):
            return FileResponse(favicon_path)
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
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True)