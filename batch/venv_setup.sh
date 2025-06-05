# UTF-8 인코딩 설정
export LANG=ko_KR.UTF-8

# 가상 환경 디렉토리 이름 설정
ENV_DIR=".venv"

# Python3가 설치되어 있는지 확인
if ! command -v python3 &> /dev/null; then
    echo "Python3가 설치되어 있지 않습니다. 먼저 Python3를 설치해주세요."
    echo "Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-venv"
    exit 1
fi

echo "Python 가상 환경 생성 중..."

# Python 가상 환경 생성
python3 -m venv "$ENV_DIR"

if [ $? -eq 0 ]; then
    echo "가상 환경이 성공적으로 생성되었습니다."
    echo "가상 환경을 활성화하려면 다음 명령을 사용하세요:"
    echo "source $ENV_DIR/bin/activate"
    echo ""
    echo "가상 환경을 비활성화하려면:"
    echo "deactivate"
else
    echo "가상 환경 생성에 실패했습니다."
    exit 1
fi