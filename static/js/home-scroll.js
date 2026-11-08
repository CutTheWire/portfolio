(() => {
    const header = document.querySelector('.site-header');
    const sections = [
        { element: document.querySelector('.home-main .hero'), id: null },
        { element: document.querySelector('.home-main #projects'), id: 'projects' },
        { element: document.querySelector('.home-main #career'), id: 'career' },
        { element: document.querySelector('.home-main #contact'), id: 'contact' }
    ];
    if (!header || sections.some(section => !section.element)) return;

    let isNavigating = false;
    let wheelGestureTriggered = false;
    let wheelDelta = 0;
    let wheelDirection = 0;
    let wheelGestureTimer;
    let navigationFallbackTimer;

    function finishNavigation() {
        isNavigating = false;
        window.clearTimeout(navigationFallbackTimer);
    }

    function getCurrentSectionIndex() {
        const hash = window.location.hash.slice(1);
        const hashIndex = sections.findIndex(section => section.id === hash);
        if (hashIndex >= 0) return hashIndex;

        const headerBottom = header.getBoundingClientRect().bottom;
        return sections.reduce((closestIndex, section, index) => {
            const closestDistance = Math.abs(
                sections[closestIndex].element.getBoundingClientRect().top - headerBottom
            );
            const distance = Math.abs(section.element.getBoundingClientRect().top - headerBottom);
            return distance < closestDistance ? index : closestIndex;
        }, 0);
    }

    function navigateToSection(index) {
        const section = sections[index];
        const url = section.id
            ? `${window.location.pathname}${window.location.search}#${section.id}`
            : `${window.location.pathname}${window.location.search}`;

        window.history.replaceState(window.history.state, '', url);
        isNavigating = true;
        section.element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        window.clearTimeout(navigationFallbackTimer);
        navigationFallbackTimer = window.setTimeout(() => {
            finishNavigation();
        }, 1000);
    }

    window.addEventListener('scrollend', finishNavigation);

    document.addEventListener('wheel', event => {
        const target = event.target instanceof Element ? event.target : null;
        if (event.ctrlKey || Math.abs(event.deltaY) < Math.abs(event.deltaX) ||
            window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
            target?.closest('.mail-modal, input, textarea, select, [contenteditable="true"]')) {
            return;
        }

        event.preventDefault();
        window.clearTimeout(wheelGestureTimer);
        wheelGestureTimer = window.setTimeout(() => {
            wheelGestureTriggered = false;
            wheelDelta = 0;
            wheelDirection = 0;
        }, 280);
        if (isNavigating || wheelGestureTriggered) return;

        const direction = Math.sign(event.deltaY);
        if (!direction) return;
        if (direction !== wheelDirection) wheelDelta = 0;
        wheelDirection = direction;
        wheelDelta += Math.abs(event.deltaY);
        if (wheelDelta < 40) return;
        wheelDelta = 0;
        wheelDirection = 0;
        wheelGestureTriggered = true;

        const currentIndex = getCurrentSectionIndex();
        const nextIndex = direction > 0
            ? Math.min(currentIndex + 1, sections.length - 1)
            : currentIndex === sections.length - 1
                ? 1
                : Math.max(currentIndex - 1, 0);
        if (nextIndex !== currentIndex) navigateToSection(nextIndex);
    }, { passive: false });
})();
