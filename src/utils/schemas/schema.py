import re
from pydantic import BaseModel, Field, field_validator

class Validators:
    @staticmethod
    def validate_email(v: str) -> str:
        """
        이메일 형식 검증 함수
        """
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(v):
            raise ValueError('지원하는 는 이메일 형식이 아닙니다. 다음과 같은 형식을 따르십쇼. ex) example@example.com')
        return v

class CommonFields:
    sender_name = Field(
        example="홍길동",
        title="발신자 이름",
        min_length=1,
        description="이메일을 보내는 사람의 이름"
    )
    sender_email = Field(
        example="example@email.com",
        title="발신자 이메일",
        description="이메일을 보내는 사람의 이메일 주소",
    )
    subject = Field(
        example="문의 사항",
        title="이메일 제목",
        min_length=1,
        description="이메일의 제목"
    )
    message = Field(
        example="안녕하세요, 문의 사항이 있습니다.",
        title="이메일 본문",
        min_length=1,
        description="이메일의 본문 내용"
    )

class Email_Request(BaseModel):
    """
    이메일 전송을 위한 스키마 정의
    """
    sender_name: str = CommonFields.sender_name
    sender_email: str = CommonFields.sender_email
    subject: str = CommonFields.subject
    message: str = CommonFields.message

    @field_validator('sender_email')
    def check_email(cls, v):
        return Validators.validate_email(v)