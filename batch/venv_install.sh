# UTF-8 인코딩 설정
export LANG=ko_KR.UTF-8

# 가상 환경 디렉토리 이름 설정
ENV_DIR=".venv"

# 가상 환경이 존재하는지 확인
if [ ! -d "$ENV_DIR" ]; then
    echo "가상 환경이 존재하지 않습니다. 먼저 venv_setup.sh를 실행해주세요."
    exit 1
fi

# 가상 환경 활성화
echo "가상 환경 활성화 중..."
source "$ENV_DIR/bin/activate"

# pip 최신 버전으로 업그레이드
echo "pip 업그레이드 중..."
python -m pip install --upgrade pip

# requirements.txt 파일 존재 확인
if [ ! -f "./src/requirements.txt" ]; then
    echo "requirements.txt 파일을 찾을 수 없습니다. ./src/requirements.txt 경로를 확인해주세요."
    deactivate
    exit 1
fi

# requirements.txt 파일에 있는 모든 패키지 설치
echo "패키지 설치 중..."
pip install -r ./src/requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "가상 환경이 성공적으로 설정되었습니다."
    echo "현재 가상 환경이 활성화되어 있습니다."
    echo ""
    echo "애플리케이션을 실행하려면:"
    echo "cd src && python main.py"
    echo ""
    echo "가상 환경을 비활성화하려면:"
    echo "deactivate"
else
    echo "패키지 설치에 실패했습니다."
    deactivate
    exit 1
fi