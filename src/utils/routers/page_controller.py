import os
import markdown as md
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from utils.handlers import error_handler as ErrorHandler

page_router = APIRouter()
templates = Jinja2Templates(directory="static")

env_file_path = Path(__file__).resolve().parents[2] / ".env"

if not os.path.exists(env_file_path):
    raise FileNotFoundError(f".env 파일을 찾을 수 없습니다: {env_file_path}")

load_dotenv(env_file_path)

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
        "google_verification": google_verification,
        "og_title": title,
        "og_description": description,
        "og_url": url,
        "og_type": "website",
        "og_locale": "ko_KR",
        "twitter_card": "summary",
        "twitter_title": title,
        "twitter_description": description,
        "structured_data": get_structured_data()  # 구조화된 데이터 추가
    }

def get_structured_data():
    """검색 엔진을 위한 구조화된 데이터"""
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "서정훈",
        "jobTitle": "백엔드 개발자",
        "description": "Python, FastAPI를 활용한 백엔드 개발자",
        "url": "https://cutwire.myddns.me",
        "sameAs": [
            "https://github.com/CutTheWire",
            "https://github.com/TreeNut-KR"
        ],
        "knowsAbout": [
            "Python",
            "FastAPI",
            "백엔드 개발",
            "API 개발",
            "웹 개발",
            "서버 개발",
            "Docker",
            "MongoDB"
        ],
        "worksFor": {
            "@type": "Organization",
            "name": "개인 프리랜서"
        }
    }

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

        meta_tags = generate_meta_tags(
            title="서정훈 - 백엔드 개발자 포트폴리오",
            description="Python, FastAPI를 활용한 백엔드 개발자 서정훈의 포트폴리오입니다. 웹 개발, API 개발 프로젝트를 확인해보세요.",
            url="https://cutwire.myddns.me/"
        )
        
        # 템플릿에 마크다운 변환 결과와 메타 태그를 전달
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "메인",
                "content": html_content,
                "meta_tags": meta_tags
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
            # 마크다운 파일이 존재하지 않으면 unauthorized.html 페이지로 리다이렉트
            meta_tags = generate_meta_tags(
                title="페이지를 찾을 수 없습니다 - 서정훈 포트폴리오",
                description="요청하신 포트폴리오 페이지를 찾을 수 없습니다."
            )
            return templates.TemplateResponse(
                "unauthorized.html",
                {"request": request, "meta_tags": meta_tags},
                status_code=404
            )
        
        with open(md_path, encoding="utf-8") as f:
            md_content = f.read()
        
        html_content = md.markdown(md_content, extensions=["fenced_code", "tables"])
        
        # 프로젝트별 SEO 메타 태그
        project_title = safe_filename.replace(".md", "").replace("_", " ").title()
        meta_tags = generate_meta_tags(
            title=f"{project_title} - 서정훈 포트폴리오",
            description=f"서정훈의 {project_title} 프로젝트입니다. 백엔드 개발, Python, FastAPI를 활용한 프로젝트를 확인해보세요.",
            url=f"https://cutwire.myddns.me/portfolio/{safe_filename.replace('.md', '')}"
        )
        
        return templates.TemplateResponse(
            "portfolio.html",
            {
                "request": request,
                "title": safe_filename.replace(".md", ""),
                "content": html_content,
                "meta_tags": meta_tags
            }
        )
    except ErrorHandler.BadRequestException:
        # 잘못된 파일명도 unauthorized.html로 처리
        meta_tags = generate_meta_tags(
            title="잘못된 요청 - 서정훈 포트폴리오",
            description="잘못된 요청입니다. 서정훈의 포트폴리오를 확인해보세요."
        )
        return templates.TemplateResponse(
            "unauthorized.html",
            {"request": request, "meta_tags": meta_tags},
            status_code=400
        )
    except FileNotFoundError:
        # 템플릿 파일이 없는 경우는 서버 에러로 처리
        raise ErrorHandler.NotFoundException("템플릿 파일이 존재하지 않습니다.")
    except UnicodeDecodeError:
        # 파일 인코딩 오류도 unauthorized.html로 처리
        meta_tags = generate_meta_tags(
            title="파일 오류 - 서정훈 포트폴리오",
            description="파일을 읽는 중 오류가 발생했습니다."
        )
        return templates.TemplateResponse(
            "unauthorized.html",
            {"request": request, "meta_tags": meta_tags},
            status_code=400
        )
    except Exception as e:
        # 기타 예외는 서버 에러로 처리
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
