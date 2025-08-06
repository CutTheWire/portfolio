/**
 * GitHub 리포지토리 정보를 서버 API에서 가져와서 표시하는 모듈 (전체 리포지토리 + 휠스크롤)
 * @author GitHub Copilot
 */
class RepositoriesModule {
    constructor() {
        this.container = document.getElementById('repositories-grid');
        this.baseUrl = '/github';
        this.maxRepos = 50; // 모든 리포지토리 가져오기
    }

    /**
     * 서버 API에서 모든 리포지토리 정보 가져오기
     */
    async fetchRepositories() {
        try {
            console.log('🔄 모든 리포지토리 정보 요청 시작...');
            
            const response = await fetch(`${this.baseUrl}/repositories?limit=${this.maxRepos}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
            
            console.log('📡 API 응답 상태:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ API 오류 응답:', errorText);
                throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
            }
            
            const result = await response.json();
            console.log('✅ API 응답 데이터:', result);
            
            if (result.success) {
                console.log('📦 전체 리포지토리 개수:', result.data.length);
                return result.data;
            } else {
                throw new Error(result.message || '리포지토리 정보를 가져올 수 없습니다.');
            }
            
        } catch (error) {
            console.error('❌ 리포지토리 정보를 가져오는데 실패했습니다:', error);
            return null;
        }
    }

    /**
     * 리포지토리 카드 HTML 생성
     */
    createRepositoryCard(repo) {
        return `
            <div class="repository-card">
                <div class="repository-header">
                    <a href="${repo.html_url}" target="_blank" rel="noopener" class="repository-name" title="${repo.name}">
                        <i class="fab fa-github"></i>
                        ${repo.name}
                    </a>
                    ${repo.private ? '<span class="repository-private">Private</span>' : ''}
                </div>
                
                <p class="repository-description" title="${repo.description}">
                    ${repo.description}
                </p>
                
                <div class="repository-stats">
                    ${repo.language ? `
                        <div class="repository-language">
                            <span class="language-color" style="background-color: ${repo.language_color}"></span>
                            ${repo.language}
                        </div>
                    ` : ''}
                    
                    <div class="repository-stat">
                        <i class="fas fa-star"></i>
                        ${repo.stargazers_count}
                    </div>
                    
                    <div class="repository-stat">
                        <i class="fas fa-code-branch"></i>
                        ${repo.forks_count}
                    </div>
                </div>
                
                <div class="repository-updated">
                    업데이트: ${repo.updated_relative}
                </div>
            </div>
        `;
    }

    /**
     * 오류 메시지 표시
     */
    showError(message = "리포지토리 정보를 불러올 수 없습니다") {
        this.container.innerHTML = `
            <div class="repositories-error">
                <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 1rem; color: var(--accent-secondary);"></i>
                <h3>${message}</h3>
                <p>네트워크 연결을 확인하거나 잠시 후 다시 시도해주세요.</p>
                <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: var(--accent-primary); color: white; border: none; border-radius: 4px; cursor: pointer;">
                    다시 시도
                </button>
                <a href="https://github.com/CutTheWire" target="_blank" rel="noopener" class="repository-name" style="margin-top: 1rem; display: inline-block;">
                    GitHub에서 직접 보기 →
                </a>
            </div>
        `;
    }

    /**
     * 횡스크롤 휠 이벤트 추가
     */
    addHorizontalScrollSupport() {
        this.container.addEventListener('wheel', (e) => {
            // Shift 키를 누르지 않은 상태에서 휠 이벤트가 발생하면 횡스크롤로 변경
            if (!e.shiftKey && Math.abs(e.deltaX) < Math.abs(e.deltaY)) {
                e.preventDefault();
                this.container.scrollLeft += e.deltaY;
            }
        }, { passive: false });

        // 터치 스크롤 지원 (모바일)
        let isDown = false;
        let startX;
        let scrollLeft;

        this.container.addEventListener('mousedown', (e) => {
            isDown = true;
            this.container.style.cursor = 'grabbing';
            startX = e.pageX - this.container.offsetLeft;
            scrollLeft = this.container.scrollLeft;
        });

        this.container.addEventListener('mouseleave', () => {
            isDown = false;
            this.container.style.cursor = 'grab';
        });

        this.container.addEventListener('mouseup', () => {
            isDown = false;
            this.container.style.cursor = 'grab';
        });

        this.container.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - this.container.offsetLeft;
            const walk = (x - startX) * 2;
            this.container.scrollLeft = scrollLeft - walk;
        });

        // 기본 커서 설정
        this.container.style.cursor = 'grab';
    }

    /**
     * 리포지토리 목록 렌더링
     */
    async renderRepositories() {
        try {
            console.log('🎨 모든 리포지토리 렌더링 시작...');
            
            const repos = await this.fetchRepositories();
            
            if (!repos) {
                console.error('❌ 리포지토리 데이터가 null입니다.');
                this.showError("서버에서 리포지토리 정보를 가져올 수 없습니다.");
                return;
            }

            if (repos.length === 0) {
                console.warn('⚠️ 리포지토리가 없습니다.');
                this.container.innerHTML = `
                    <div class="repositories-error">
                        <p>표시할 리포지토리가 없습니다.</p>
                    </div>
                `;
                return;
            }

            console.log('🔨 모든 리포지토리 카드 생성 중...');
            
            // 모든 리포지토리 카드 생성
            const cardsHTML = repos.map(repo => this.createRepositoryCard(repo)).join('');
            this.container.innerHTML = cardsHTML;

            console.log('✨ 모든 리포지토리 카드 생성 완료!');

            // 횡스크롤 지원 추가
            this.addHorizontalScrollSupport();

            // 애니메이션 효과 추가
            const cards = this.container.querySelectorAll('.repository-card');
            cards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateX(20px)';
                setTimeout(() => {
                    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateX(0)';
                }, index * 50); // 더 빠른 애니메이션
            });

        } catch (error) {
            console.error('❌ 리포지토리 렌더링 실패:', error);
            this.showError(`렌더링 오류: ${error.message}`);
        }
    }

    /**
     * 모듈 초기화
     */
    init() {
        console.log('🚀 RepositoriesModule 초기화 (전체 리포지토리 + 휠스크롤)...');
        
        if (!this.container) {
            console.error('❌ repositories-grid 컨테이너를 찾을 수 없습니다.');
            return;
        }

        console.log('✅ 컨테이너 발견:', this.container);
        this.renderRepositories();
    }
}

// 페이지 로드 시 자동 초기화
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM 로드 완료, RepositoriesModule 시작...');
    const repositoriesModule = new RepositoriesModule();
    repositoriesModule.init();
});