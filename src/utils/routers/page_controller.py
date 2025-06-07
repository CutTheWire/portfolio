import os
import markdown as md

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from utils.handlers import error_handler as ErrorHandler

page_router = APIRouter()
templates = Jinja2Templates(directory="static")

@page_router.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    """메인 페이지"""
    try:
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
    except FileNotFoundError:
        raise ErrorHandler.NotFoundException("템플릿 파일이 존재하지 않습니다.")
    except UnicodeDecodeError:
        raise ErrorHandler.InternalServerErrorException("파일 인코딩 오류가 발생했습니다.")
    except Exception as e:
        raise ErrorHandler.InternalServerErrorException("페이지 로딩 중 오류가 발생했습니다.")

@page_router.get("/portfolio/{filename}", response_class=HTMLResponse)
async def read_markdown(request: Request, filename: str):
    """포트폴리오 마크다운 페이지"""
    try:
        # 확장자 체크 및 경로 보호
        if not filename.endswith(".md"):
            filename += ".md"
        
        safe_filename = os.path.basename(filename)
        
        # 파일명 검증
        if not safe_filename or safe_filename in [".", ".."]:
            raise ErrorHandler.BadRequestException("잘못된 파일명입니다.")
        
        md_path = os.path.join("markdown", safe_filename)
        
        if not os.path.exists(md_path):
            raise ErrorHandler.NotFoundException("마크다운 파일이 존재하지 않습니다.")
        
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
    except (ErrorHandler.NotFoundException, ErrorHandler.BadRequestException):
        raise
    except FileNotFoundError:
        raise ErrorHandler.NotFoundException("템플릿 파일이 존재하지 않습니다.")
    except UnicodeDecodeError:
        raise ErrorHandler.InternalServerErrorException("파일 인코딩 오류가 발생했습니다.")
    except Exception as e:
        raise ErrorHandler.InternalServerErrorException("페이지 로딩 중 오류가 발생했습니다.")

@page_router.get("/images/{img:path}")
async def get_image(img: str):
    """이미지 파일 제공"""
    try:
        # 경로 정규화 및 보안 검증
        safe_img = os.path.normpath(img).replace("\\", "/")
        
        if ".." in safe_img or safe_img.startswith("/") or safe_img.startswith("\\"):
            raise ErrorHandler.BadRequestException("잘못된 이미지 경로입니다.")
        
        # 빈 경로 체크
        if not safe_img.strip():
            raise ErrorHandler.BadRequestException("이미지 경로가 비어있습니다.")
        
        image_path = os.path.join("images", safe_img)
        
        if not os.path.exists(image_path):
            raise ErrorHandler.NotFoundException("이미지 파일이 존재하지 않습니다.")
        
        # 파일이 실제로 이미지 파일인지 확인 (확장자 기반)
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico'}
        file_ext = os.path.splitext(safe_img)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise ErrorHandler.BadRequestException("지원되지 않는 이미지 형식입니다.")
        
        return FileResponse(image_path)
        
    except (ErrorHandler.NotFoundException, ErrorHandler.BadRequestException):
        raise
    except PermissionError:
        raise ErrorHandler.InternalServerErrorException("파일 접근 권한이 없습니다.")
    except Exception as e:
        raise ErrorHandler.InternalServerErrorException("이미지 로딩 중 오류가 발생했습니다.")
