
(() => {
    const header = document.querySelector('.site-header');

    const sections = [
        document.querySelector('.home-main .hero'),
        document.querySelector('.home-main #projects'),
        document.querySelector('.home-main #repository'),
        document.querySelector('.home-main #career'),
        document.querySelector('.home-main #contact')
    ];

    if (!header || sections.some(section => !section)) return;

    const sectionIds = [
        null,
        'projects',
        'repository',
        'career',
        'contact'
    ];

    const CONFIG = {
        threshold: 55,
        gestureResetDelay: 180,
        navigationCooldown: 650,
        animationFallback: 1400,
        maxQueuedNavigation: 1
    };

    let currentIndex = 0;
    let isNavigating = false;
    let wheelDelta = 0;
    let wheelDirection = 0;
    let gestureTimer = null;
    let navigationTimer = null;
    let queuedDirection = 0;

    const prefersReducedMotion = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
    );

    function getCurrentSectionIndex() {
        const headerBottom = header.getBoundingClientRect().bottom;

        let closestIndex = 0;
        let closestDistance = Infinity;

        sections.forEach((section, index) => {
            const distance = Math.abs(
                section.getBoundingClientRect().top - headerBottom
            );

            if (distance < closestDistance) {
                closestDistance = distance;
                closestIndex = index;
            }
        });

        return closestIndex;
    }

    function finishNavigation() {
        if (!isNavigating) return;

        window.clearTimeout(navigationTimer);

        isNavigating = false;
        currentIndex = getCurrentSectionIndex();

        if (queuedDirection !== 0) {
            const direction = queuedDirection;
            queuedDirection = 0;

            requestAnimationFrame(() => {
                navigate(direction);
            });
        }
    }

    function navigateToSection(index) {
        index = Math.max(0, Math.min(index, sections.length - 1));

        if (index === currentIndex) return;

        currentIndex = index;
        isNavigating = true;

        const id = sectionIds[index];
        const url = id
            ? `${location.pathname}${location.search}#${id}`
            : `${location.pathname}${location.search}`;

        history.replaceState(history.state, '', url);

        sections[index].scrollIntoView({
            behavior: prefersReducedMotion.matches ? 'instant' : 'smooth',
            block: 'start'
        });

        window.clearTimeout(navigationTimer);

        navigationTimer = window.setTimeout(() => {
            finishNavigation();
        }, CONFIG.animationFallback);
    }

    function navigate(direction) {
        if (isNavigating) {
            queuedDirection = direction;
            return;
        }

        const nextIndex = Math.max(
            0,
            Math.min(currentIndex + direction, sections.length - 1)
        );

        navigateToSection(nextIndex);
    }

    function resetGesture() {
        wheelDelta = 0;
        wheelDirection = 0;
    }

    document.addEventListener('wheel', event => {
        const target = event.target instanceof Element
            ? event.target
            : null;

        if (
            event.ctrlKey ||
            Math.abs(event.deltaY) < Math.abs(event.deltaX) ||
            prefersReducedMotion.matches ||
            target?.closest(
                '.mail-modal, input, textarea, select, [contenteditable="true"]'
            )
        ) {
            return;
        }

        event.preventDefault();

        if (isNavigating) {
            return;
        }

        const direction = Math.sign(event.deltaY);

        if (!direction) return;

        if (direction !== wheelDirection) {
            resetGesture();
            wheelDirection = direction;
        }

        wheelDelta += Math.abs(event.deltaY);

        window.clearTimeout(gestureTimer);

        gestureTimer = window.setTimeout(
            resetGesture,
            CONFIG.gestureResetDelay
        );

        if (wheelDelta < CONFIG.threshold) return;

        resetGesture();
        navigate(direction);

    }, { passive: false });

    window.addEventListener('scrollend', finishNavigation);

    currentIndex = getCurrentSectionIndex();

})();
