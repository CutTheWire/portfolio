#!/bin/bash
# Docker 배포 스크립트
# 사용법: ./deploy.sh [build|up|down|logs|restart|status]

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_env() {
    if [ ! -f .env ]; then
        log_warn ".env 파일이 없습니다. .env.example을 복사하여 생성하세요."
        if [ -f .env.example ]; then
            cp .env.example .env
            log_info ".env 파일이 생성되었습니다. 필요한 값을 입력하세요."
        fi
        return 1
    fi
    return 0
}

check_certificates() {
    if [ ! -f "src/certificates/cutwire.myddns.me-fullchain.pem" ] || [ ! -f "src/certificates/cutwire.myddns.me-key.pem" ]; then
        log_error "SSL 인증서 파일이 없습니다."
        log_info "필요한 파일:"
        log_info "  - src/certificates/cutwire.myddns.me-fullchain.pem"
        log_info "  - src/certificates/cutwire.myddns.me-key.pem"
        return 1
    fi
    return 0
}

cmd_build() {
    log_info "Docker 이미지 빌드 중..."
    docker compose build --no-cache
    log_info "빌드 완료"
}

cmd_up() {
    check_env || exit 1
    check_certificates || exit 1
    
    log_info "컨테이너 시작 중..."
    docker compose up -d
    log_info "컨테이너가 시작되었습니다."
    log_info "HTTPS: https://cutwire.myddns.me"
    log_info "HTTP (리다이렉트): http://cutwire.myddns.me"
}

cmd_down() {
    log_info "컨테이너 중지 중..."
    docker compose down
    log_info "컨테이너가 중지되었습니다."
}

cmd_restart() {
    check_env || exit 1
    check_certificates || exit 1
    
    log_info "컨테이너 재시작 중..."
    docker compose restart
    log_info "컨테이너가 재시작되었습니다."
}

cmd_logs() {
    docker compose logs -f --tail=100
}

cmd_status() {
    docker compose ps
    echo ""
    log_info "헬스체크 상태:"
    # 포트폴리오 앱은 HTTP 8000 포트에서 실행
    docker compose exec portfolio curl -f http://localhost:8000/robots.txt 2>/dev/null && log_info "포트폴리오 앱: 정상" || log_error "포트폴리오 앱: 비정상"
    # Nginx는 HTTPS 443 포트에서 실행 (인증서 검증 무시)
    docker compose exec nginx wget -q --spider --no-check-certificate https://localhost/robots.txt 2>/dev/null && log_info "Nginx: 정상" || log_error "Nginx: 비정상"
}

cmd_ssl_renew() {
    log_info "SSL 인증서 갱신은 win-acme 또는 certbot을 사용하여 호스트에서 수행하세요."
    log_info "갱신 후에는 컨테이너를 재시작하세요: ./deploy.sh restart"
}

case "${1:-help}" in
    build)
        cmd_build
        ;;
    up)
        cmd_up
        ;;
    down)
        cmd_down
        ;;
    restart)
        cmd_restart
        ;;
    logs)
        cmd_logs
        ;;
    status)
        cmd_status
        ;;
    ssl-renew)
        cmd_ssl_renew
        ;;
    *)
        echo "사용법: $0 {build|up|down|restart|logs|status|ssl-renew}"
        echo ""
        echo "명령어:"
        echo "  build      - Docker 이미지 빌드"
        echo "  up         - 컨테이너 시작 (HTTPS 활성화)"
        echo "  down       - 컨테이너 중지"
        echo "  restart    - 컨테이너 재시작"
        echo "  logs       - 로그 실시간 확인"
        echo "  status     - 컨테이너 상태 확인"
        echo "  ssl-renew  - SSL 인증서 갱신 안내"
        exit 1
        ;;
esac