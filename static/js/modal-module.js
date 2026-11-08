let lastFormData = null;
let retryCount = 0;
const MAX_RETRY = 3;
let isFormDirty = false;
let isSending = false;
let emailComponentPromise = null;
let emailOpenPromise = null;
let emailReturnFocus = null;
let emailPreviousOverflow = '';
let emailKeyboardInitialized = false;

async function openEmailModal() {
    if (emailOpenPromise) return emailOpenPromise;
    const existing = document.getElementById('mailOverlay');
    if (existing?.classList.contains('active')) return existing;
    emailReturnFocus = document.activeElement;
    emailOpenPromise = (async () => {
        const overlay = await loadEmailComponent() || createEmailFallback();
        resetEmailForm();
        emailPreviousOverflow = document.body.style.overflow;
        document.body.style.overflow = 'hidden';
        overlay.classList.remove('mail-container-hidden');
        overlay.hidden = false;
        overlay.classList.add('active');
        (overlay.querySelector('#senderName') || overlay.querySelector('.mail-modal')).focus();
        return overlay;
    })();
    try {
        return await emailOpenPromise;
    } finally {
        emailOpenPromise = null;
    }
}

function closeEmailModal() {
    const overlay = document.getElementById('mailOverlay');
    if (!overlay?.classList.contains('active') || isSending) return;
    if (isFormDirty && !confirm('작성 중인 내용을 삭제하고 닫으시겠습니까?')) return;
    overlay.classList.remove('active');
    overlay.classList.add('mail-container-hidden');
    overlay.hidden = true;
    document.body.style.overflow = emailPreviousOverflow;
    resetEmailForm();
    if (emailReturnFocus?.isConnected) emailReturnFocus.focus();
    emailReturnFocus = null;
}

function setEmailView(view) {
    ['Form', 'Success', 'Error'].forEach(name => {
        const container = document.getElementById(`mail${name}Container`);
        if (!container) return;
        const hidden = name !== view;
        container.hidden = hidden;
        container.classList.toggle('mail-container-hidden', hidden);
        container.style.removeProperty('display');
    });
}

function resetEmailForm() {
    const form = document.querySelector('#mailOverlay .mail-form');
    if (form) form.reset();
    setEmailView('Form');
    setEmailSending(false);
    clearFormErrors();
    hideNetworkError();
    retryCount = 0;
    lastFormData = null;
    isFormDirty = false;
    const status = document.getElementById('mailStatus');
    if (status) status.textContent = '';
}

// 폼 더티 상태 체크 함수
function markFormDirty() {
    isFormDirty = true;
}

// 폼 유효성 검사
function validateForm(data) {
    let isValid = true;
    clearFormErrors();

    // 이름 검사
    if (!data.sender_name || !data.sender_name.trim()) {
        showFieldError('senderName', 'nameError', '이름을 입력해주세요.');
        isValid = false;
    }

    // 이메일 검사
    if (!data.sender_email || !data.sender_email.trim()) {
        showFieldError('senderEmail', 'emailError', '이메일을 입력해주세요.');
        isValid = false;
    } else if (!validateEmail(data.sender_email.trim())) {
        showFieldError('senderEmail', 'emailError', '올바른 이메일 형식을 입력해주세요.');
        isValid = false;
    }

    // 제목 검사
    if (!data.subject || !data.subject.trim()) {
        showFieldError('subject', 'subjectError', '제목을 입력해주세요.');
        isValid = false;
    }

    // 메시지 검사
    if (!data.message || !data.message.trim()) {
        showFieldError('message', 'messageError', '메시지를 입력해주세요.');
        isValid = false;
    } else if (data.message.trim().length < 10) {
        showFieldError('message', 'messageError', '메시지는 10자 이상 입력해주세요.');
        isValid = false;
    }

    return isValid;
}

// 이메일 형식 검증
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// 필드 오류 표시
function showFieldError(fieldId, errorId, message) {
    const field = document.getElementById(fieldId);
    const error = document.getElementById(errorId);
    
    if (field && error) {
        field.classList.add('error');
        field.setAttribute('aria-invalid', 'true');
        error.textContent = message;
        error.classList.add('visible');
    }
}

// 모든 필드 오류 제거
function clearFormErrors() {
    const fields = ['senderName', 'senderEmail', 'subject', 'message'];
    const errors = ['nameError', 'emailError', 'subjectError', 'messageError'];
    
    fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.classList.remove('error');
            field.removeAttribute('aria-invalid');
        }
    });
    
    errors.forEach(errorId => {
        const error = document.getElementById(errorId);
        if (error) {
            error.classList.remove('visible');
            error.textContent = '';
        }
    });
}

// 네트워크 오류 표시/숨김
function showNetworkError() {
    const errorElement = document.getElementById('mailNetworkError');
    if (errorElement) {
        errorElement.hidden = false;
        errorElement.classList.add('visible');
    }
}

function hideNetworkError() {
    const errorElement = document.getElementById('mailNetworkError');
    if (errorElement) {
        errorElement.hidden = true;
        errorElement.classList.remove('visible');
    }
}

// 오류 메시지 업데이트
function updateErrorMessage(message) {
    const errorText = document.getElementById('mailErrorText');
    if (errorText) errorText.textContent = message;
}

async function sendEmail(event) {
    event.preventDefault();
    if (isSending) return;
    const form = event.target;
    const formData = {
        sender_name: form.elements.namedItem('sender_name').value.trim(),
        sender_email: form.elements.namedItem('sender_email').value.trim(),
        subject: form.elements.namedItem('subject').value.trim(),
        message: form.elements.namedItem('message').value.trim()
    };
    if (!validateForm(formData)) {
        form.querySelector('[aria-invalid="true"]')?.focus();
        return;
    }
    lastFormData = formData;
    retryCount = 0;
    isFormDirty = true;
    await submitEmailData(formData);
}

function setEmailSending(sending) {
    isSending = sending;
    const overlay = document.getElementById('mailOverlay');
    if (!overlay) return;
    overlay.querySelector('.mail-modal').setAttribute('aria-busy', String(sending));
    overlay.querySelectorAll('button, input, textarea').forEach(control => {
        control.disabled = sending;
    });
    overlay.querySelectorAll('.mail-form-submit, .mail-retry-button').forEach(button => {
        button.classList.toggle('loading', sending);
    });
    const retryButton = overlay.querySelector('.mail-retry-button');
    if (retryButton) retryButton.disabled = sending || retryCount >= MAX_RETRY;
    const status = document.getElementById('mailStatus');
    if (status) status.textContent = sending ? '전송 중입니다. 완료 후 닫을 수 있습니다.' : '';
}

async function submitEmailData(formData) {
    setEmailSending(true);
    hideNetworkError();
    document.querySelector('#mailOverlay .mail-modal').focus();
    try {
        const response = await fetch('/smtp/email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (response.ok && result?.success) {
            showSuccessMessage();
        } else {
            showErrorMessage(typeof result?.message === 'string'
                ? result.message : '서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
        }
    } catch (error) {
        if (error instanceof TypeError) {
            showNetworkError();
            showErrorMessage('네트워크 연결을 확인하고 다시 시도해주세요.');
        } else {
            showErrorMessage('응답을 확인하지 못했습니다. 잠시 후 다시 시도해주세요.');
        }
    } finally {
        setEmailSending(false);
    }
}

function showSuccessMessage() {
    isFormDirty = false;
    retryCount = 0;
    lastFormData = null;
    setEmailView('Success');
    document.querySelector('#mailOverlay .mail-success-title').focus();
}

function showErrorMessage(message) {
    retryCount++;
    updateErrorMessage(retryCount >= MAX_RETRY
        ? `${message} 전송 시도 횟수를 초과했습니다. sjmbee04@gmail.com으로 직접 연락해주세요.`
        : message);
    setEmailView('Error');
    document.querySelector('#mailOverlay .mail-error-title').focus();
}

async function retryEmail() {
    if (isSending || !lastFormData || retryCount >= MAX_RETRY) return;
    await submitEmailData(lastFormData);
}

function editEmail() {
    if (isSending) return;
    setEmailView('Form');
    hideNetworkError();
    document.getElementById('senderName')?.focus();
}

function emailFocusableElements(overlay) {
    return Array.from(overlay.querySelectorAll('a[href], button, input, textarea, [tabindex]'))
        .filter(element => !element.disabled && element.tabIndex >= 0 &&
            !element.closest('[hidden], .mail-container-hidden') && element.getClientRects().length);
}

function initEmailModule() {
    const overlay = document.getElementById('mailOverlay');
    if (!overlay) return;
    if (!overlay.dataset.initialized) {
        overlay.dataset.initialized = 'true';
        overlay.querySelectorAll('input, textarea').forEach(field => {
            field.addEventListener('input', markFormDirty);
            field.addEventListener('change', markFormDirty);
        });
    }
    if (emailKeyboardInitialized) return;
    emailKeyboardInitialized = true;
    document.addEventListener('keydown', event => {
        const activeOverlay = document.getElementById('mailOverlay');
        if (!activeOverlay?.classList.contains('active')) return;
        if (event.key === 'Escape') {
            event.preventDefault();
            closeEmailModal();
        } else if (event.key === 'Tab') {
            const elements = emailFocusableElements(activeOverlay);
            const first = elements[0];
            const last = elements[elements.length - 1];
            if (!first) {
                event.preventDefault();
                activeOverlay.querySelector('.mail-modal').focus();
            } else if (!elements.includes(document.activeElement) ||
                (event.shiftKey && document.activeElement === first) ||
                (!event.shiftKey && document.activeElement === last)) {
                event.preventDefault();
                (event.shiftKey ? last : first).focus();
            }
        }
    });
    document.addEventListener('focusin', event => {
        const activeOverlay = document.getElementById('mailOverlay');
        if (activeOverlay?.classList.contains('active') && !activeOverlay.contains(event.target)) {
            activeOverlay.querySelector('.mail-modal').focus();
        }
    });
}

function createEmailFallback() {
    const existing = document.getElementById('mailOverlay');
    if (existing) return existing;
    const overlay = document.createElement('div');
    overlay.id = 'mailOverlay';
    overlay.className = 'mail-overlay';
    overlay.hidden = true;
    overlay.dataset.fallback = 'true';
    overlay.innerHTML = `
        <div class="mail-modal" role="dialog" aria-modal="true" aria-labelledby="mailModalTitle" tabindex="-1">
            <div class="mail-modal-header">
                <h2 class="mail-modal-title" id="mailModalTitle">이메일 문의</h2>
                <button type="button" class="mail-modal-close" aria-label="문의 창 닫기">×</button>
            </div>
            <p>문의 양식을 불러오지 못했습니다. 이메일로 직접 연락해주세요.</p>
            <p class="mail-direct-contact"><a href="mailto:sjmbee04@gmail.com">sjmbee04@gmail.com</a></p>
        </div>`;
    overlay.querySelector('button').addEventListener('click', closeEmailModal);
    document.body.appendChild(overlay);
    initEmailModule();
    return overlay;
}

async function loadEmailComponent() {
    const existing = document.getElementById('mailOverlay');
    if (existing && (!existing.dataset.fallback || existing.classList.contains('active'))) {
        initEmailModule();
        return existing;
    }
    if (emailComponentPromise) return emailComponentPromise;
    emailComponentPromise = (async () => {
        try {
            const response = await fetch('/static/components/modal.html', { cache: 'no-cache' });
            if (!response.ok) throw new Error('Contact component unavailable');
            const template = document.createElement('template');
            template.innerHTML = await response.text();
            const overlay = template.content.querySelector('#mailOverlay');
            if (!overlay?.querySelector('.mail-form') || !overlay.querySelector('[role="dialog"]')) {
                throw new Error('Invalid contact component');
            }
            const current = document.getElementById('mailOverlay');
            if (current && !current.dataset.fallback) return current;
            if (current?.classList.contains('active')) return current;
            if (current) current.remove();
            overlay.hidden = true;
            document.body.appendChild(overlay);
            initEmailModule();
            return overlay;
        } catch (error) {
            console.error('Failed to load email component:', error);
            return null;
        }
    })();
    try {
        return await emailComponentPromise;
    } finally {
        emailComponentPromise = null;
    }
}