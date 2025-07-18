import os
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from app.utils import error_tools

media_router = APIRouter()

@media_router.get("/webp/{img:path}")
async def get_image(img: str):
    """이미지 파일 제공"""
    try:
        # 경로 정규화 및 보안 검증
        safe_img = os.path.normpath(img).replace("\\", "/")
        
        if ".." in safe_img or safe_img.startswith("/") or safe_img.startswith("\\"):
            raise error_tools.BadRequestException("잘못된 이미지 경로입니다.")
        
        # 빈 경로 체크
        if not safe_img.strip():
            raise error_tools.BadRequestException("이미지 경로가 비어있습니다.")
        
        image_path = os.path.join("images", safe_img)
        
        if not os.path.exists(image_path):
            raise error_tools.NotFoundException("이미지 파일이 존재하지 않습니다.")
        
        file_ext = os.path.splitext(safe_img)[1].lower()
        
        if file_ext not in '.webp':
            raise error_tools.BadRequestException("지원되지 않는 이미지 형식입니다.")
        
        return FileResponse(image_path)
        
    except (error_tools.NotFoundException, error_tools.BadRequestException):
        raise
    except PermissionError:
        raise error_tools.InternalServerErrorException("파일 접근 권한이 없습니다.")
    except Exception as e:
        raise error_tools.InternalServerErrorException("이미지 로딩 중 오류가 발생했습니다.")

@media_router.get("/webm/{video:path}")
async def get_video(video: str):
    """비디오 파일 제공"""
    try:
        # 경로 정규화 및 보안 검증
        safe_video = os.path.normpath(video).replace("\\", "/")
        
        if ".." in safe_video or safe_video.startswith("/") or safe_video.startswith("\\"):
            raise error_tools.BadRequestException("잘못된 비디오 경로입니다.")
        
        # 빈 경로 체크
        if not safe_video.strip():
            raise error_tools.BadRequestException("비디오 경로가 비어있습니다.")
        
        video_path = os.path.join("videos", safe_video)
        
        if not os.path.exists(video_path):
            raise error_tools.NotFoundException("비디오 파일이 존재하지 않습니다.")
        
        file_ext = os.path.splitext(safe_video)[1].lower()
        
        if file_ext not in '.webm':
            raise error_tools.BadRequestException("지원되지 않는 비디오 형식입니다.")
        
        return FileResponse(video_path)
        
    except (error_tools.NotFoundException, error_tools.BadRequestException):
        raise
    except PermissionError:
        raise error_tools.InternalServerErrorException("파일 접근 권한이 없습니다.")
    except Exception as e:
        raise error_tools.InternalServerErrorException("비디오 로딩 중 오류가 발생했습니다.")