// 모바일에서 확대 방지 및 레이아웃 최적화
(function() {
    'use strict';
    
    // 모바일 디바이스 감지
    function isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                window.innerWidth <= 768;
    }
    
    // 뷰포트 설정 강화
    function enforceViewport() {
        const viewport = document.querySelector('meta[name="viewport"]');
        if (viewport && isMobile()) {
            viewport.setAttribute('content', 
                'width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover'
            );
        }
    }
    
    // 수평 스크롤 방지
    function preventHorizontalScroll() {
        if (isMobile()) {
            document.documentElement.style.overflowX = 'hidden';
            document.body.style.overflowX = 'hidden';
            document.body.style.maxWidth = '100vw';
            document.body.style.width = '100%';
        }
    }
    
    // 확대 상태 감지 및 수정
    function resetZoomOnLoad() {
        if (isMobile() && window.visualViewport) {
            // Visual Viewport API를 사용하여 확대 상태 감지
            const viewport = window.visualViewport;
            
            function handleViewportChange() {
                const scale = window.outerWidth / window.innerWidth;
                
                // 확대된 상태라면 스크롤을 맨 왼쪽으로
                if (scale > 1.1 || viewport.scale > 1.1) {
                    window.scrollTo(0, window.scrollY);
                    document.documentElement.scrollLeft = 0;
                    document.body.scrollLeft = 0;
                }
            }
            
            viewport.addEventListener('resize', handleViewportChange);
            viewport.addEventListener('scroll', handleViewportChange);
            
            // 페이지 로드 시 한 번 실행
            setTimeout(handleViewportChange, 100);
        }
    }
    
    // 터치 제스처 최적화 (핀치 줌 제한)
    function optimizeTouchGestures() {
        if (isMobile()) {
            let isZooming = false;
            
            document.addEventListener('touchstart', function(e) {
                if (e.touches.length > 1) {
                    isZooming = true;
                }
            }, { passive: true });
            
            document.addEventListener('touchend', function(e) {
                if (isZooming) {
                    isZooming = false;
                    // 줌 후 스크롤 위치 조정
                    setTimeout(() => {
                        if (document.documentElement.scrollLeft > 0 || document.body.scrollLeft > 0) {
                            window.scrollTo(0, window.scrollY);
                        }
                    }, 100);
                }
            }, { passive: true });
        }
    }
    
    // 페이지 초기화
    function initMobileFix() {
        enforceViewport();
        preventHorizontalScroll();
        resetZoomOnLoad();
        optimizeTouchGestures();
        
        // 방향 변경 시 레이아웃 재조정
        window.addEventListener('orientationchange', function() {
            setTimeout(() => {
                enforceViewport();
                preventHorizontalScroll();
                window.scrollTo(0, window.scrollY);
            }, 500);
        });
        
        // 리사이즈 시 레이아웃 재조정
        window.addEventListener('resize', function() {
            if (isMobile()) {
                preventHorizontalScroll();
                setTimeout(() => {
                    if (document.documentElement.scrollLeft > 0 || document.body.scrollLeft > 0) {
                        window.scrollTo(0, window.scrollY);
                    }
                }, 100);
            }
        });
    }
    
    // DOM 로드 후 실행
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileFix);
    } else {
        initMobileFix();
    }
    
    // 페이지 표시 시에도 실행 (뒤로가기 등)
    window.addEventListener('pageshow', function(e) {
        if (e.persisted) {
            setTimeout(initMobileFix, 100);
        }
    });
})();