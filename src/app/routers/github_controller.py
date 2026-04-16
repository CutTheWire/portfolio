from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
from datetime import datetime

from app.utils.github_tools import github_api
from app.utils import error_tools

github_router = APIRouter()

@github_router.get("/test")
async def test_github_api(request: Request):
    """
    GitHub API 연결 테스트
    """
    try:
        return JSONResponse(
            content={
                "success": True,
                "message": "GitHub API 엔드포인트가 정상적으로 작동합니다.",
                "timestamp": datetime.now().isoformat(),
                "token_configured": bool(github_api.token),
                "username": github_api.username
            }
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"테스트 실패: {str(e)}"
            },
            status_code=500
        )

@github_router.get("/repositories")
async def get_repositories(request: Request, limit: int = 50):
    """
    GitHub 리포지토리 목록 조회 (전체 리포지토리)
    """
    try:
        print(f"📡 GitHub API 요청: limit={limit}")
        
        if limit < 1 or limit > 100:
            raise error_tools.BadRequestException("리포지토리 개수는 1-100 사이여야 합니다.")
        
        repositories = await github_api.get_repositories_cached(max_repos=limit)
        
        print(f"📦 GitHub API 응답: {len(repositories) if repositories else 0}개 리포지토리")
        
        if repositories is None:
            raise error_tools.ExternalServiceException("GitHub API 요청에 실패했습니다.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": repositories,
                "total": len(repositories),
                "message": "리포지토리 목록을 성공적으로 조회했습니다."
            },
            headers={
                "Cache-Control": "public, max-age=300",  # 5분 캐시
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except error_tools.BadRequestException as e:
        print(f"❌ BadRequest: {str(e)}")
        raise
    except error_tools.ExternalServiceException as e:
        print(f"❌ ExternalService: {str(e)}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        error_tools.log_error(
            exc=e,
            request=request,
            status_code=500,
            detail="GitHub 리포지토리 조회 중 오류 발생"
        )
        raise error_tools.InternalServerErrorException("서버 내부 오류가 발생했습니다.")

@github_router.get("/user", response_model=Dict)
async def get_user_info(request: Request):
    """
    GitHub 사용자 정보 조회
    """
    try:
        user_info = await github_api.get_user_info_cached()
        
        if user_info is None:
            raise error_tools.ExternalServiceException("GitHub 사용자 정보를 가져올 수 없습니다.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": user_info,
                "message": "사용자 정보를 성공적으로 조회했습니다."
            },
            headers={
                "Cache-Control": "public, max-age=600",  # 10분 캐시
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except error_tools.ExternalServiceException:
        raise
    except Exception as e:
        error_tools.log_error(
            exc=e,
            request=request,
            status_code=500,
            detail="GitHub 사용자 정보 조회 중 오류 발생"
        )
        raise error_tools.InternalServerErrorException("서버 내부 오류가 발생했습니다.")

@github_router.get("/repository/{repo_name}", response_model=Dict)
async def get_repository_details(request: Request, repo_name: str):
    """
    특정 리포지토리 상세 정보 조회
    """
    try:
        # 리포지토리명 검증
        if not repo_name or len(repo_name) > 100:
            raise error_tools.BadRequestException("유효하지 않은 리포지토리명입니다.")
        
        repository = await github_api.get_repository_details_cached(repo_name)
        
        if repository is None:
            raise error_tools.NotFoundException("리포지토리를 찾을 수 없습니다.")
        
        # 언어 통계도 함께 조회
        languages = await github_api.get_repository_languages_cached(repo_name)
        repository["languages"] = languages
        
        return JSONResponse(
            content={
                "success": True,
                "data": repository,
                "message": f"{repo_name} 리포지토리 정보를 성공적으로 조회했습니다."
            },
            headers={
                "Cache-Control": "public, max-age=300",  # 5분 캐시
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except error_tools.BadRequestException:
        raise
    except error_tools.NotFoundException:
        raise
    except Exception as e:
        error_tools.log_error(
            exc=e,
            request=request,
            status_code=500,
            detail=f"{repo_name} 리포지토리 조회 중 오류 발생"
        )
        raise error_tools.InternalServerErrorException("서버 내부 오류가 발생했습니다.")

@github_router.get("/stats", response_model=Dict)
async def get_github_stats(request: Request):
    """
    GitHub 통계 정보 조회 (리포지토리 + 사용자 정보 결합)
    """
    try:
        # 병렬로 사용자 정보와 리포지토리 정보 조회
        import asyncio
        
        user_task = github_api.get_user_info_cached()
        repos_task = github_api.get_repositories_cached(max_repos=10)
        
        user_info, repositories = await asyncio.gather(user_task, repos_task)
        
        if user_info is None or repositories is None:
            raise error_tools.ExternalServiceException("GitHub 통계 정보를 가져올 수 없습니다.")
        
        # 통계 계산
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repositories)
        total_forks = sum(repo.get("forks_count", 0) for repo in repositories)
        languages = {}
        
        for repo in repositories:
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        stats = {
            "user": user_info,
            "repositories": {
                "total": user_info.get("public_repos", 0),
                "recent": repositories[:6],  # 최신 6개만
                "total_stars": total_stars,
                "total_forks": total_forks,
                "languages": languages
            }
        }
        
        return JSONResponse(
            content={
                "success": True,
                "data": stats,
                "message": "GitHub 통계 정보를 성공적으로 조회했습니다."
            },
            headers={
                "Cache-Control": "public, max-age=600",  # 10분 캐시
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except error_tools.ExternalServiceException:
        raise
    except Exception as e:
        error_tools.log_error(
            exc=e,
            request=request,
            status_code=500,
            detail="GitHub 통계 조회 중 오류 발생"
        )
        raise error_tools.InternalServerErrorException("서버 내부 오류가 발생했습니다.")

@github_router.get("/contributions")
async def get_user_contributions(request: Request, years: str = "2023,2024,2025"):
    """
    GitHub 사용자 기여도 정보 조회
    """
    try:
        print(f"📊 GitHub Contributions API 요청: years={years}")
        
        # 년도 파싱
        year_list = [int(year.strip()) for year in years.split(",") if year.strip().isdigit()]
        
        if not year_list or len(year_list) > 5:
            raise error_tools.BadRequestException("년도는 1-5개까지만 지정할 수 있습니다.")
        
        contributions = await github_api.get_user_contributions_cached(years=year_list)
        
        if contributions is None:
            raise error_tools.ExternalServiceException("GitHub 기여도 정보를 가져올 수 없습니다.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": contributions,
                "message": "기여도 정보를 성공적으로 조회했습니다."
            },
            headers={
                "Cache-Control": "public, max-age=3600",  # 1시간 캐시
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except error_tools.BadRequestException:
        raise
    except error_tools.ExternalServiceException:
        raise
    except Exception as e:
        print(f"❌ Contributions error: {str(e)}")
        error_tools.log_error(
            exc=e,
            request=request,
            status_code=500,
            detail="GitHub 기여도 조회 중 오류 발생"
        )
        raise error_tools.InternalServerErrorException("서버 내부 오류가 발생했습니다.")

@github_router.get("/activity")
async def get_user_activity_overview(request: Request):
    """
    GitHub 사용자 활동 개요 조회
    """
    try:
        print(f"📈 GitHub Activity Overview API 요청")
        
        activity = await github_api.get_activity_overview_cached()
        
        if activity is None:
            raise error_tools.ExternalServiceException("GitHub 활동 개요를 가져올 수 없습니다.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": activity,
                "message": "활동 개요를 성공적으로 조회했습니다."
            },
            headers={
                "Cache-Control": "public, max-age=1800",  # 30분 캐시
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except error_tools.ExternalServiceException:
        raise
    except Exception as e:
        print(f"❌ Activity Overview error: {str(e)}")
        error_tools.log_error(
            exc=e,
            request=request,
            status_code=500,
            detail="GitHub 활동 개요 조회 중 오류 발생"
        )
        raise error_tools.InternalServerErrorException("서버 내부 오류가 발생했습니다.")