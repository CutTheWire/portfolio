class TableOfContents {
    constructor() {
        this.toc = null;
        this.tocList = null;
        this.headings = [];
        this.scrollTimeout = null;
        this.isVisible = false;
        this.hideTimeout = null;
        
        this.init();
    }
    
    init() {
        // reference 페이지에서만 동작
        if (!document.querySelector('.reference-content')) {
            return;
        }
        
        this.createTOC();
        this.bindEvents();
        this.updateActiveHeading();
    }
    
    createTOC() {
        // h1, h2, h3까지만 헤딩 요소들 찾기
        this.headings = Array.from(document.querySelectorAll('.reference-content h1, .reference-content h2, .reference-content h3'));
        
        if (this.headings.length === 0) {
            return;
        }
        
        // 헤딩에 ID 추가 (없는 경우)
        this.headings.forEach((heading, index) => {
            if (!heading.id) {
                heading.id = this.generateId(heading.textContent, index);
            }
        });
        
        // TOC 컨테이너 생성
        this.toc = document.createElement('div');
        this.toc.className = 'toc-container';
        
        // TOC 내용 생성
        const tocTitle = document.createElement('div');
        tocTitle.className = 'toc-title';
        tocTitle.textContent = '목차';
        
        this.tocList = document.createElement('ul');
        this.tocList.className = 'toc-list';
        
        // 헤딩들을 TOC 아이템으로 변환
        this.headings.forEach(heading => {
            const listItem = document.createElement('li');
            listItem.className = 'toc-item';
            
            const link = document.createElement('a');
            link.className = 'toc-link';
            link.href = `#${heading.id}`;
            link.textContent = heading.textContent.trim();
            link.setAttribute('data-level', heading.tagName.charAt(1));
            
            // 클릭 이벤트
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.scrollToHeading(heading.id);
            });
            
            listItem.appendChild(link);
            this.tocList.appendChild(listItem);
        });
        
        this.toc.appendChild(tocTitle);
        this.toc.appendChild(this.tocList);
        document.body.appendChild(this.toc);
    }
    
    generateId(text, index) {
        // 텍스트에서 특수문자 제거하고 소문자로 변환
        let id = text
            .toLowerCase()
            .replace(/[^\w\s가-힣]/g, '')
            .replace(/\s+/g, '-')
            .substring(0, 50);
        
        // 중복 방지를 위해 인덱스 추가
        id = `heading-${index}-${id}`;
        
        return id;
    }
    
    bindEvents() {
        let lastScrollTop = 0;
        
        // 휠 이벤트
        window.addEventListener('wheel', () => {
            this.showTOC();
        });
        
        // 스크롤 이벤트 (활성 헤딩 업데이트용)
        window.addEventListener('scroll', () => {
            this.updateActiveHeading();
            
            // 스크롤 방향 감지
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (Math.abs(scrollTop - lastScrollTop) > 5) {
                this.showTOC();
            }
            
            lastScrollTop = scrollTop;
        });
        
        // 마우스가 TOC 위에 있을 때는 숨기지 않음
        this.toc.addEventListener('mouseenter', () => {
            this.clearHideTimeout();
        });
        
        this.toc.addEventListener('mouseleave', () => {
            this.hideTOC();
        });
    }
    
    showTOC() {
        if (!this.toc) return;
        
        this.clearHideTimeout();
        
        if (!this.isVisible) {
            this.toc.classList.add('visible');
            this.isVisible = true;
        }
        
        // 0.5초 후 자동으로 숨김
        this.hideTimeout = setTimeout(() => {
            this.hideTOC();
        }, 500);
    }
    
    hideTOC() {
        if (!this.toc) return;
        
        this.hideTimeout = setTimeout(() => {
            this.toc.classList.remove('visible');
            this.isVisible = false;
        }, 500);
    }
    
    clearHideTimeout() {
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
            this.hideTimeout = null;
        }
    }
    
    updateActiveHeading() {
        if (!this.headings.length) return;
        
        const scrollTop = window.pageYOffset;
        const windowHeight = window.innerHeight;
        
        let activeHeading = null;
        
        // 현재 화면에 보이는 헤딩 찾기
        for (let i = this.headings.length - 1; i >= 0; i--) {
            const heading = this.headings[i];
            const rect = heading.getBoundingClientRect();
            
            if (rect.top <= windowHeight / 3) {
                activeHeading = heading;
                break;
            }
        }
        
        // 활성 링크 업데이트
        const links = this.tocList.querySelectorAll('.toc-link');
        links.forEach(link => {
            link.classList.remove('active');
            if (activeHeading && link.getAttribute('href') === `#${activeHeading.id}`) {
                link.classList.add('active');
            }
        });
    }
    
    scrollToHeading(id) {
        const element = document.getElementById(id);
        if (element) {
            const offsetTop = element.getBoundingClientRect().top + window.pageYOffset - 80;
            
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }
}

// DOM이 로드되면 TOC 초기화
document.addEventListener('DOMContentLoaded', () => {
    new TableOfContents();
});