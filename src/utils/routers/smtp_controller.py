from fastapi import APIRouter
from starlette.responses import JSONResponse

from utils.handlers.smtp_handler import SMTPHandler as SmtpHandler
from utils.handlers import error_handler as ErrorHandler
from utils.schemas import schema as Schema

smtp_handler = SmtpHandler()
smtp_router = APIRouter()

# 이메일 전송 API 엔드포인트
@smtp_router.post("/email")
async def send_email_api(request: Schema.Email_Request):
    """이메일 전송 API"""
    try:
        # 입력값 검증
        if not all([request.sender_name.strip(), request.sender_email.strip(), request.subject.strip(), request.message.strip()]):
            raise ErrorHandler.BadRequestException("모든 필드를 입력해주세요.")
        
        # 이메일 형식 간단 검증
        if "@" not in request.sender_email or "." not in request.sender_email:
            raise ErrorHandler.ValueErrorException("올바른 이메일 형식을 입력해주세요.")
        
        # 이메일 전송
        submit_inquiry = await smtp_handler.submit_inquiry_smtp(
            request.sender_name.strip(),
            request.sender_email.strip(),
            request.subject.strip(),
            request.message.strip()
        )
        
        acknowledge_inquiry = await smtp_handler.acknowledge_inquiry_smtp(
            request.sender_name.strip(),
            request.sender_email.strip(),
            request.subject.strip(),
            request.message.strip()
        )
        
        if submit_inquiry and acknowledge_inquiry:
            return JSONResponse(
                content={
                    "success": True,
                    "message": "메일이 성공적으로 전송되었습니다! 빠른 시일 내에 답변드리겠습니다."
                }
            )
        else:
            raise ErrorHandler.InternalServerErrorException("메일 전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
            
    except (
        ErrorHandler.BadRequestException,
        ErrorHandler.ValueErrorException,
        ErrorHandler.InternalServerErrorException,
    ): 
        raise
    except Exception as e:
        raise ErrorHandler.InternalServerErrorException("서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")