from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

import os
import uvicorn
import markdown as md

app = FastAPI(
    title="서정훈 포트폴리오",
    docs_url=None,
    redoc_url=None,
)

app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static"
)

# 이미지 디렉토리 추가 (로컬 이미지용)
if not os.path.exists("images"):
    os.makedirs("images")

app.mount(
    path="/images",
    app=StaticFiles(directory="images"),
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
        "index.html",
        {
            "request": request,
            "title": safe_filename.replace(".md", ""),
            "content": html_content,
        }
    )

if __name__ == "__main__":
    # 로그 레벨을 warning으로 설정하여 404 로그 최소화
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True, log_level="warning")