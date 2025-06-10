from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.utils import error_tools, email_client
from app.schemas import smtp_schema

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
            raise error_tools.InternalServerErrorException("메일 전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
            
    except (
        error_tools.BadRequestException,
        error_tools.ValueErrorException,
        error_tools.InternalServerErrorException,
    ): 
        raise
    except Exception as e:
        raise error_tools.InternalServerErrorException("서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")