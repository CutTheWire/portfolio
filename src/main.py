from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import Scope, Receive, Send

import os
import uvicorn
import markdown as md

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

# 404 예외 핸들러 - 개선된 버전
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # 브라우저/도구 자동 요청 경로들 필터링 (더 포괄적)
        ignored_paths = (
            "/.well-known",
            "/favicon.ico",
            "/robots.txt",
            "/sitemap.xml",
            "/apple-touch-icon",
            "/manifest.json",
            "/chrome-extension",
            "/devtools"
        )
        
        # 무시할 경로면 조용히 404 응답 (로그 없음)
        if any(request.url.path.startswith(p) for p in ignored_paths):
            return HTMLResponse(status_code=404, content="")
        
        # 나머지 404는 unauthorized.html로 처리
        return templates.TemplateResponse(
            "unauthorized.html",
            {"request": request},
            status_code=404
        )
    
    return templates.TemplateResponse(
        "unauthorized.html",
        {"request": request},
        status_code=exc.status_code
    )

@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import FileResponse
    favicon_path = os.path.join("static", "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    else:
        # 파일이 없으면 빈 응답 반환
        return HTMLResponse(status_code=204, content="")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # main.md 파일을 읽어와서 HTML로 변환
    md_path = os.path.join("markdown", "main.md")
    if not os.path.exists(md_path):
        html_content = "<h1>main.md 파일이 존재하지 않습니다.</h1>"
    else:
        with open(md_path, encoding="utf-8") as f:
            md_content = f.read()
        html_content = md.markdown(md_content, extensions=["fenced_code", "tables"])

    # 템플릿에 마크다운 변환 결과를 전달
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "메인",
            "content": html_content,
        }
    )

@app.get("/portfolio/{filename}", response_class=HTMLResponse)
async def read_markdown(request: Request, filename: str):
    # 확장자 체크 및 경로 보호
    if not filename.endswith(".md"):
        filename += ".md"
    safe_filename = os.path.basename(filename)
    md_path = os.path.join("markdown", safe_filename)
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="마크다운 파일이 존재하지 않습니다.")
    
    with open(md_path, encoding="utf-8") as f:
        md_content = f.read()
    html_content = md.markdown(md_content, extensions=["fenced_code", "tables"])
    
    return templates.TemplateResponse(
        "portfolio.html",
        {
            "request": request,
            "title": safe_filename.replace(".md", ""),
            "content": html_content,
        }
    )

@app.get("/images/{img:path}")
async def get_image(img: str):
    # 경로 보호: ../ 등 우회 방지
    safe_img = os.path.normpath(img).replace("\\", "/")
    if ".." in safe_img or safe_img.startswith("/"):
        raise HTTPException(status_code=400, detail="잘못된 이미지 경로입니다.")
    image_path = os.path.join("images", safe_img)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="이미지 파일이 존재하지 않습니다.")
    return FileResponse(image_path)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True)