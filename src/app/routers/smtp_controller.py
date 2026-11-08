import logging

from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.utils import error_tools, email_client
from app.schemas import smtp_schema

logger = logging.getLogger(__name__)
smtp_handler = email_client.SMTPHandler()  # 모듈.클래스명() 형태로 사용
smtp_router = APIRouter()

# 이메일 전송 API 엔드포인트
@smtp_router.post("/email")
async def send_email_api(request: smtp_schema.Email_Request):
    """이메일 전송 API"""
    try:
        # 입력값 검증
        if not all([request.sender_name.strip(), request.sender_email.strip(), request.subject.strip(), request.message.strip()]):
            raise error_tools.BadRequestException("모든 필드를 입력해주세요.")
        
        # 이메일 형식 간단 검증
        if "@" not in request.sender_email or "." not in request.sender_email:
            raise error_tools.ValueErrorException("올바른 이메일 형식을 입력해주세요.")
        
        # 이메일 전송
        submit_inquiry = await smtp_handler.submit_inquiry_smtp(
            request.sender_name.strip(),
            request.sender_email.strip(),
            request.subject.strip(),
            request.message.strip()
        )
        
        if not submit_inquiry:
            raise error_tools.InternalServerErrorException("메일 전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")

        acknowledge_inquiry = await smtp_handler.acknowledge_inquiry_smtp(
            request.sender_name.strip(),
            request.sender_email.strip(),
            request.subject.strip(),
            request.message.strip()
        )
        if not acknowledge_inquiry:
            logger.warning("Inquiry email was delivered, but acknowledgement email delivery failed")

        return JSONResponse(
            content={
                "success": True,
                "message": "문의 이메일이 접수되었습니다. 빠른 시일 내에 답변드리겠습니다."
            }
        )
            
    except (
        error_tools.BadRequestException,
        error_tools.ValueErrorException,
        error_tools.InternalServerErrorException,
    ): 
        raise
    except Exception:
        logger.exception("Unexpected error while processing portfolio email")
        raise error_tools.InternalServerErrorException("서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")