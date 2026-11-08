import os
import smtplib
import logging

from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class SMTPHandler:
    """
    SMTP를 통한 이메일 전송 및 인증 관리를 위한 클래스.
    이메일 인증 코드를 생성하고 검증하는 기능을 제공합니다.
    """
    def __init__(self):
        """
        SMTP 핸들러 초기화. 환경 변수에서 SMTP 설정을 가져옵니다.
        """
        # 환경 변수 파일 경로 설정 수정
        env_file_path = Path(__file__).resolve().parents[2] / ".env"
        
        if not os.path.exists(env_file_path):
            raise FileNotFoundError(f".env 파일을 찾을 수 없습니다: {env_file_path}")
        
        load_dotenv(env_file_path)
        
        self.server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.port = int(os.getenv("SMTP_PORT", 587))
        self.user = os.getenv("SMTP_USER", "")
        self.password = os.getenv("SMTP_PASSWORD", "")
        self.recipient = "sjmbee04@gmail.com"
        
        # 환경 변수가 제대로 설정되었는지 확인
        if not self.user or not self.password:
            print("경고: SMTP_USER 또는 SMTP_PASSWORD가 설정되지 않았습니다.")

    async def submit_inquiry_smtp(self, sender_name: str, sender_email: str, subject: str, message: str):
        """
        SMTP를 통해 문의 이메일 전송
        
        Args:
            sender_name (str): 발신자 이름
            sender_email (str): 발신자 이메일 주소
            subject (str): 이메일 제목
            message (str): 이메일 본문 내용
        Returns:
            bool: 이메일 전송 성공 여부
        """
        try:
            # 이메일 메시지 구성
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = self.recipient
            msg['Subject'] = f"[포트폴리오 사이트 발신 메일] {subject}"
            
            # 이메일 본문 작성
            email_body = f"""
            포트폴리오 사이트를 통해 새로운 문의가 접수되었습니다.

            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            📧 발신자 정보
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            • 이름: {sender_name}
            • 이메일: {sender_email}
            • 제목: {subject}
            • 접수 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}

            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            💬 메시지 내용
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            {message}

            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            📌 답변 방법
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            위 발신자 이메일({sender_email})로 직접 답변하시면 됩니다.

            ※ 이 메일은 포트폴리오 사이트의 자동 발송 시스템에서 전송되었습니다.
            """
            
            msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
            
            # SMTP 서버 연결 및 전송
            with smtplib.SMTP(self.server, self.port, timeout=20) as server:
                server.starttls()  # TLS 암호화 시작
                server.login(self.user, self.password)
                server.send_message(msg)
            return True
            
        except Exception:
            logger.exception("Failed to send portfolio inquiry email")
            return False
        
    async def acknowledge_inquiry_smtp(self, sender_name: str, sender_email: str, subject: str, message: str) -> bool:
        """
        문의한 사용자에게 회신 이메일 전송 (SMTP 사용)

        Args:
            sender_name (str): 사용자 이름
            sender_email (str): 사용자 이메일 주소
            subject (str): 문의 제목
            message (str): 문의 내용

        Returns:
            bool: 이메일 전송 성공 여부
        """
        try:
            # 이메일 메시지 구성
            msg = MIMEMultipart("alternative")
            msg["From"] = self.user
            msg["To"] = sender_email
            msg["Subject"] = f"[문의 자동 발신] 서정훈 포트폴리오에 문의해주셔서 감사합니다."

            # HTML 본문 구성
            current_time = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")

            html_body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Segoe UI', sans-serif;
                        background-color: #f8f8f8;
                        padding: 20px;
                        color: #333;
                    }}
                    .container {{
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    }}
                    .title {{
                        font-size: 20px;
                        font-weight: bold;
                        color: #2c3e50;
                    }}
                    .section {{
                        margin-top: 20px;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #555;
                    }}
                    .footer {{
                        margin-top: 30px;
                        font-size: 12px;
                        color: #999;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="title">📩 문의가 정상적으로 접수되었습니다</div>
                    <p>{sender_name}님, 안녕하세요.<br>
                    서정훈의 포트폴리오 사이트에 문의해주셔서 감사합니다.</p>

                    <div class="section">
                        <div class="label">접수 내용</div>
                        <ul>
                            <li><strong>이름:</strong> {sender_name}</li>
                            <li><strong>이메일:</strong> {sender_email}</li>
                            <li><strong>제목:</strong> {subject}</li>
                            <li><strong>접수 시간:</strong> {current_time}</li>
                        </ul>
                    </div>

                    <div class="section">
                        <div class="label">💬 문의 내용</div>
                        <div style="white-space: pre-wrap; background-color:#f0f0f0; padding:10px; border-radius:6px;">
                            {message}
                        </div>
                    </div>

                    <div class="section">
                        <p>📌 빠른 시일 내에 확인 후 답변드리겠습니다.<br>
                        좋은 하루 되세요!</p>
                    </div>

                    <div class="footer">
                        ※ 본 메일은 서정훈 포트폴리오 자동 발신 시스템에서 전송되었습니다.
                    </div>
                </div>
            </body>
            </html>
            """

            # 본문 첨부
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            # SMTP 서버 연결 및 전송
            with smtplib.SMTP(self.server, self.port, timeout=20) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
            return True

        except Exception:
            logger.exception("Failed to send inquiry acknowledgement email")
            return False
