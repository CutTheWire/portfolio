@echo off
chcp 65001 >nul
setlocal

:: Run from the repository root regardless of the caller's current directory.
pushd "%~dp0.."
if errorlevel 1 (
    echo 프로젝트 디렉터리로 이동할 수 없습니다.
    exit /b 1
)

set "PROJECT_ROOT=%CD%"
set "ENV_DIR=%PROJECT_ROOT%\.venv"

if exist "%ENV_DIR%\Scripts\python.exe" goto VENV_READY

echo Python 가상 환경 생성 중...

where py >nul 2>&1
if not errorlevel 1 (
    py -3 -c "import sys" >nul 2>&1
    if not errorlevel 1 (
        py -3 -m venv "%ENV_DIR%"
        if errorlevel 1 goto VENV_FAILED
        goto VENV_READY
    )
)

where python >nul 2>&1
if errorlevel 1 (
    echo Python 3을 찾을 수 없습니다. Python을 설치하고 PATH에 추가해주세요.
    goto FAILED
)

python -m venv "%ENV_DIR%"
if errorlevel 1 goto VENV_FAILED

:VENV_READY
if not exist "%ENV_DIR%\Scripts\Activate.ps1" (
    echo 가상 환경 활성화 스크립트를 찾을 수 없습니다: "%ENV_DIR%\Scripts\Activate.ps1"
    goto FAILED
)

echo 가상 환경 활성화 중...
echo 새 PowerShell 창에서 가상 환경을 사용합니다. 창을 닫으면 원래 터미널로 돌아갑니다.
powershell -NoExit -ExecutionPolicy Bypass -Command "& { Set-Location -LiteralPath '%PROJECT_ROOT%'; . '%ENV_DIR%\Scripts\Activate.ps1' }"
set "RESULT=%ERRORLEVEL%"
popd
exit /b %RESULT%

:VENV_FAILED
echo 가상 환경 생성에 실패했습니다. Python 설치와 실행 권한을 확인해주세요.

:FAILED
popd
exit /b 1
