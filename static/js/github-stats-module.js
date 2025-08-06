/**
 * GitHub 통계 정보를 서버 API에서 가져와서 표시하는 모듈
 * @author GitHub Copilot
 */
class GitHubStatsModule {
    constructor() {
        this.contributionsContainer = document.getElementById('contributions-container');
        this.activityContainer = document.getElementById('activity-container');
        this.baseUrl = '/github';
        this.monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        this.dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    }

    /**
     * GitHub 기여도 정보 가져오기
     */
    async fetchContributions() {
        try {
            console.log('📊 GitHub 기여도 정보 요청...');
            
            const response = await fetch(`${this.baseUrl}/contributions?years=2023,2024,2025`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.success) {
                return result.data;
            } else {
                throw new Error(result.message || '기여도 정보를 가져올 수 없습니다.');
            }
            
        } catch (error) {
            console.error('❌ 기여도 정보 요청 실패:', error);
            return null;
        }
    }

    /**
     * GitHub 활동 개요 정보 가져오기
     */
    async fetchActivityOverview() {
        try {
            console.log('📈 GitHub 활동 개요 요청...');
            
            const response = await fetch(`${this.baseUrl}/activity`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.success) {
                return result.data;
            } else {
                throw new Error(result.message || '활동 개요를 가져올 수 없습니다.');
            }
            
        } catch (error) {
            console.error('❌ 활동 개요 요청 실패:', error);
            return null;
        }
    }

    /**
     * 주별로 데이터를 그룹화 (GitHub 스타일)
     */
    groupDataByWeeks(dailyData) {
        // 날짜별로 정렬
        const sortedData = dailyData.sort((a, b) => new Date(a.date) - new Date(b.date));
        
        const weeks = [];
        let currentWeek = [];
        
        sortedData.forEach((day, index) => {
            const date = new Date(day.date);
            const dayOfWeek = date.getDay(); // 0 = Sunday, 6 = Saturday
            
            // 첫 번째 날짜가 일요일이 아닌 경우, 앞부분을 빈 칸으로 채움
            if (index === 0 && dayOfWeek !== 0) {
                for (let i = 0; i < dayOfWeek; i++) {
                    currentWeek.push(null);
                }
            }
            
            currentWeek.push(day);
            
            // 토요일이거나 마지막 데이터인 경우 주 완성
            if (dayOfWeek === 6 || index === sortedData.length - 1) {
                // 마지막 주가 7개가 안 되는 경우 빈 칸으로 채움
                while (currentWeek.length < 7) {
                    currentWeek.push(null);
                }
                weeks.push(currentWeek);
                currentWeek = [];
            }
        });
        
        return weeks;
    }

    /**
     * 월 라벨 생성
     */
    generateMonthLabels(weeks) {
        const monthLabels = [];
        let currentMonth = -1;
        
        weeks.forEach((week, weekIndex) => {
            const firstDay = week.find(day => day !== null);
            if (firstDay) {
                const date = new Date(firstDay.date);
                const month = date.getMonth();
                
                if (month !== currentMonth && weekIndex % 4 === 0) {
                    monthLabels.push(this.monthNames[month]);
                    currentMonth = month;
                } else {
                    monthLabels.push('');
                }
            } else {
                monthLabels.push('');
            }
        });
        
        return monthLabels;
    }

    /**
     * 기여도 잔디 렌더링 (GitHub 스타일 + 스크롤 최적화)
     */
    renderContributions(contributionsData) {
        if (!contributionsData || !contributionsData.daily_data) {
            this.showContributionsError();
            return;
        }

        const dailyData = contributionsData.daily_data;
        
        // 잔디 블록 HTML 생성
        const contributionBlocks = dailyData.map(day => {
            return `
                <div class="contribution-day" 
                     data-level="${day.level}" 
                     data-date="${day.date}" 
                     data-count="${day.count}"
                     style="background-color: ${day.color || this.getDefaultColor(day.level)}"
                     title="${this.formatDate(day.date)}: ${day.count} contributions">
                </div>
            `;
        }).join('');

        this.contributionsContainer.innerHTML = `
            <div class="contributions-summary">
                <p class="contributions-total">
                    총 <strong>${contributionsData.total_contributions.toLocaleString()}</strong>개의 기여 
                    <span class="contributions-period">(개인 + TreeNut-KR 조직 통합)</span>
                </p>
                <p class="contributions-period-info">
                    ${contributionsData.start_date} ~ ${contributionsData.end_date}
                </p>
            </div>
            
            <div class="contributions-unified-grid">
                ${contributionBlocks}
            </div>
        `;

        // 스크롤 지원 추가
        this.setupUnifiedScrolling();

        console.log('✅ 통합 기여도 잔디밭 렌더링 완료');
    }

    /**
     * 통합 잔디밭 스크롤 설정
     */
    setupUnifiedScrolling() {
        const contributionsGrid = this.contributionsContainer.querySelector('.contributions-unified-grid');
        
        if (contributionsGrid) {
            // 마우스 휠을 좌우 스크롤로 변환
            contributionsGrid.addEventListener('wheel', (e) => {
                if (Math.abs(e.deltaX) < Math.abs(e.deltaY)) {
                    e.preventDefault();
                    contributionsGrid.scrollLeft += e.deltaY;
                }
            }, { passive: false });
            
            // 드래그 스크롤 지원
            this.addTouchScrollSupport(contributionsGrid);
        }
    }

    /**
     * 터치 스크롤 지원 추가
     */
    addTouchScrollSupport(element) {
        let isDown = false;
        let startX;
        let scrollLeft;

        element.addEventListener('mousedown', (e) => {
            isDown = true;
            element.style.cursor = 'grabbing';
            startX = e.pageX - element.offsetLeft;
            scrollLeft = element.scrollLeft;
            e.preventDefault();
        });

        element.addEventListener('mouseleave', () => {
            isDown = false;
            element.style.cursor = 'grab';
        });

        element.addEventListener('mouseup', () => {
            isDown = false;
            element.style.cursor = 'grab';
        });

        element.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - element.offsetLeft;
            const walk = (x - startX) * 2;
            element.scrollLeft = scrollLeft - walk;
        });

        // 기본 커서 설정
        element.style.cursor = 'grab';
        element.style.userSelect = 'none'; // 텍스트 선택 방지
    }

    /**
     * 활동 개요 렌더링 (통합 정보)
     */
    renderActivityOverview(activityData) {
        if (!activityData) {
            this.showActivityError();
            return;
        }

        // 언어별 색상 매핑
        const languageColors = {
            'Python': '#3572A5',
            'JavaScript': '#f1e05a',
            'TypeScript': '#2b7489',
            'HTML': '#e34c26',
            'CSS': '#563d7c',
            'Java': '#b07219',
            'C++': '#f34b7d',
            'Shell': '#89e051',
            'Dockerfile': '#384d54',
            'Vue': '#4FC08D',
            'C': '#555555'
        };

        // 언어 통계 계산
        const totalRepos = Object.values(activityData.languages).reduce((a, b) => a + b, 0);
        const languageBars = Object.entries(activityData.languages)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 6)
            .map(([lang, count]) => {
                const percentage = ((count / totalRepos) * 100).toFixed(1);
                const color = languageColors[lang] || '#586069';
                
                return `
                    <div class="language-bar">
                        <span class="language-name">${lang}</span>
                        <div class="language-progress">
                            <div class="language-progress-bar" style="width: ${percentage}%; background-color: ${color};"></div>
                        </div>
                        <span class="language-percentage">${percentage}%</span>
                    </div>
                `;
            }).join('');

        this.activityContainer.innerHTML = `
            <div class="activity-stats">
                <div class="activity-stat-item">
                    <span class="activity-stat-label">
                        <i class="fas fa-folder"></i> 총 리포지토리
                    </span>
                    <span class="activity-stat-value">${activityData.total_repositories}</span>
                </div>
                
                <div class="activity-stat-item">
                    <span class="activity-stat-label">
                        <i class="fas fa-star"></i> 총 스타 (개인+조직)
                    </span>
                    <span class="activity-stat-value">${activityData.total_stars}</span>
                </div>
                
                <div class="activity-stat-item">
                    <span class="activity-stat-label">
                        <i class="fas fa-code-branch"></i> 총 포크 (개인+조직)
                    </span>
                    <span class="activity-stat-value">${activityData.total_forks}</span>
                </div>
                
                <div class="activity-stat-item">
                    <span class="activity-stat-label">
                        <i class="fas fa-users"></i> 팔로워
                    </span>
                    <span class="activity-stat-value">${activityData.followers}</span>
                </div>
                
                <div class="activity-stat-item">
                    <span class="activity-stat-label">
                        <i class="fas fa-calendar"></i> 올해 신규 프로젝트
                    </span>
                    <span class="activity-stat-value">${activityData.this_year_repos}</span>
                </div>
                
                <div class="activity-stat-item">
                    <span class="activity-stat-label">
                        <i class="fas fa-building"></i> 조직 기여
                    </span>
                    <span class="activity-stat-value">${activityData.organization_contribution || 'TreeNut-KR'}</span>
                </div>
            </div>
            
            <div class="activity-languages">
                <h4 style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.8rem;">
                    <i class="fas fa-code"></i> 주요 언어 (개인+조직 통합)
                </h4>
                ${languageBars}
            </div>
        `;

        console.log('✅ 통합 활동 개요 렌더링 완료');
    }

    /**
     * 날짜 포맷팅
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        const options = { 
            weekday: 'short', 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        };
        return date.toLocaleDateString('ko-KR', options);
    }

    /**
     * 기본 색상 반환 (백업용) - 어두운색 → 밝은색
     */
    getDefaultColor(level) {
        const colors = {
            0: '#000000',  // 가장 어두운색 (Less)
            1: '#004c1a',  // 어두운 초록
            2: '#39d353',  // 중간 초록
            3: '#7fff00',  // 밝은 초록
            4: '#00ff44'   // 가장 밝은 초록 (More)
        };
        return colors[level] || colors[0];
    }

    /**
     * 기여도 오류 표시
     */
    showContributionsError() {
        this.contributionsContainer.innerHTML = `
            <div class="contributions-error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>기여도 정보를 불러올 수 없습니다.</p>
                <small>GitHub API 제한 또는 네트워크 오류가 발생했을 수 있습니다.</small>
            </div>
        `;
    }

    /**
     * 활동 개요 오류 표시
     */
    showActivityError() {
        this.activityContainer.innerHTML = `
            <div class="activity-error">
                <p style="color: var(--text-muted); text-align: center;">활동 정보를 불러올 수 없습니다.</p>
            </div>
        `;
    }

    /**
     * 모든 GitHub 통계 로드
     */
    async loadGitHubStats() {
        try {
            console.log('🚀 GitHub 통계 로드 시작...');
            
            // 병렬로 데이터 요청
            const [contributionsData, activityData] = await Promise.all([
                this.fetchContributions(),
                this.fetchActivityOverview()
            ]);

            // 기여도 렌더링
            if (contributionsData) {
                this.renderContributions(contributionsData);
            } else {
                this.showContributionsError();
            }

            // 활동 개요 렌더링
            if (activityData) {
                this.renderActivityOverview(activityData);
            } else {
                this.showActivityError();
            }

            console.log('✅ GitHub 통계 로드 완료');

        } catch (error) {
            console.error('❌ GitHub 통계 로드 실패:', error);
            this.showContributionsError();
            this.showActivityError();
        }
    }

    /**
     * 모듈 초기화
     */
    init() {
        console.log('🚀 GitHubStatsModule 초기화...');
        
        if (!this.contributionsContainer || !this.activityContainer) {
            console.error('❌ GitHub 통계 컨테이너를 찾을 수 없습니다.');
            return;
        }

        this.loadGitHubStats();
    }
}

// 페이지 로드 시 자동 초기화
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM 로드 완료, GitHubStatsModule 시작...');
    const githubStatsModule = new GitHubStatsModule();
    githubStatsModule.init();
});