// 전역 변수
let lastFormData = null;
let retryCount = 0;
const MAX_RETRY = 3;
let isFormDirty = false; // 폼이 수정되었는지 확인하는 플래그

// 이메일 모달 관련 함수들
function openEmailModal() {
    document.getElementById('mailOverlay').classList.add('active');
    document.body.style.overflow = 'hidden';
    resetEmailForm();
}

function closeEmailModal() {
    // 폼이 수정된 상태에서 닫으려고 하면 확인 요청
    if (isFormDirty && !confirm('작성 중인 내용이 있습니다. 정말 닫으시겠습니까?')) {
        return;
    }
    
    document.getElementById('mailOverlay').classList.remove('active');
    document.body.style.overflow = '';
    resetEmailForm();
}

function resetEmailForm() {
    // 폼 초기화
    const form = document.querySelector('.mail-form');
    if (form) form.reset();
    
    // 컨테이너 표시 상태 초기화
    document.getElementById('mailFormContainer').style.display = 'block';
    document.getElementById('mailSuccessContainer').style.display = 'none';
    document.getElementById('mailErrorContainer').style.display = 'none';
    
    // 버튼 상태 초기화
    const submitBtn = document.getElementById('mailSubmitButton');
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
    }
    
    // 오류 상태 초기화
    clearFormErrors();
    hideNetworkError();
    
    // 재시도 카운트 초기화
    retryCount = 0;
    lastFormData = null;
    isFormDirty = false; // 더티 플래그 초기화
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
        if (field) field.classList.remove('error');
    });
    
    errors.forEach(errorId => {
        const error = document.getElementById(errorId);
        if (error) error.classList.remove('visible');
    });
}

// 네트워크 오류 표시/숨김
function showNetworkError() {
    const errorElement = document.getElementById('mailNetworkError');
    if (errorElement) errorElement.classList.add('visible');
}

function hideNetworkError() {
    const errorElement = document.getElementById('mailNetworkError');
    if (errorElement) errorElement.classList.remove('visible');
}

// 오류 메시지 업데이트
function updateErrorMessage(message) {
    const errorText = document.getElementById('mailErrorText');
    if (errorText) errorText.innerHTML = message;
}

// 이메일 전송 함수 (JSON으로 수정)
async function sendEmail(event) {
    event.preventDefault();
    
    const submitBtn = document.getElementById('mailSubmitButton');
    const form = event.target;
    
    // FormData 대신 JSON 객체로 생성
    const formData = {
        sender_name: form.sender_name.value,
        sender_email: form.sender_email.value,
        subject: form.subject.value,
        message: form.message.value
    };
    
    // 폼 유효성 검사
    if (!validateForm(formData)) {
        return;
    }

    // 마지막 폼 데이터 저장 (재시도용)
    lastFormData = formData;
    
    // 로딩 상태
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
    }
    hideNetworkError();
    
    try {
        const response = await fetch('/smtp/email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 성공 시
            showSuccessMessage();
            retryCount = 0;
            isFormDirty = false; // 전송 성공 시 더티 상태 해제
        } else {
            // 서버 오류 시
            const errorMessage = result.message || '서버에서 오류가 발생했습니다.';
            showErrorMessage(errorMessage);
        }
    } catch (error) {
        console.error('Email send error:', error);
        
        // 네트워크 오류 시
        if (error.name === 'TypeError' || error.message.includes('fetch')) {
            showNetworkError();
            showErrorMessage('네트워크 연결을 확인하고 다시 시도해주세요.');
        } else {
            showErrorMessage('예상치 못한 오류가 발생했습니다.<br>잠시 후 다시 시도해주세요.');
        }
    } finally {
        // 로딩 상태 해제
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
        }
    }
}

// 성공 메시지 표시
function showSuccessMessage() {
    document.getElementById('mailFormContainer').style.display = 'none';
    document.getElementById('mailErrorContainer').style.display = 'none';
    document.getElementById('mailSuccessContainer').style.display = 'block';
    
    // 5초 후 자동으로 닫기 (성공 메시지를 충분히 읽을 수 있도록)
    setTimeout(() => {
        isFormDirty = false; // 성공 후에는 더티 상태 해제
        closeEmailModal();
    }, 5000);
}

// 오류 메시지 표시
function showErrorMessage(message) {
    updateErrorMessage(message);
    document.getElementById('mailFormContainer').style.display = 'none';
    document.getElementById('mailSuccessContainer').style.display = 'none';
    document.getElementById('mailErrorContainer').style.display = 'block';
    
    retryCount++;
}

// 재시도 함수 (JSON 데이터로 수정)
async function retryEmail() {
    if (!lastFormData) {
        closeEmailModal();
        return;
    }

    if (retryCount >= MAX_RETRY) {
        updateErrorMessage(
            '최대 재시도 횟수를 초과했습니다.<br>' +
            '나중에 다시 시도하시거나 직접 연락해주세요.<br>' +
            '<strong>직접 연락: sjmbee04@gmail.com</strong>'
        );
        return;
    }

    // 폼으로 돌아가기
    document.getElementById('mailFormContainer').style.display = 'block';
    document.getElementById('mailErrorContainer').style.display = 'none';
    hideNetworkError();
    
    // 로딩 상태
    const retryBtn = document.querySelector('.mail-retry-button');
    if (retryBtn) {
        retryBtn.disabled = true;
        retryBtn.classList.add('loading');
    }
    
    try {
        const response = await fetch('/smtp/email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(lastFormData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccessMessage();
            retryCount = 0;
            isFormDirty = false; // 재시도 성공 시 더티 상태 해제
        } else {
            const errorMessage = result.message || '서버에서 오류가 발생했습니다.';
            showErrorMessage(errorMessage);
        }
    } catch (error) {
        console.error('Retry email error:', error);
        showErrorMessage('재시도 중 오류가 발생했습니다.<br>잠시 후 다시 시도해주세요.');
    } finally {
        if (retryBtn) {
            retryBtn.disabled = false;
            retryBtn.classList.remove('loading');
        }
    }
}

// 이메일 모듈 초기화 함수
function initEmailModule() {
    // ESC 키로 모달 닫기 (더티 상태 확인)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && document.getElementById('mailOverlay')?.classList.contains('active')) {
            closeEmailModal();
        }
    });
    
    // 오버레이 배경 클릭시 닫기 방지 (더이상 닫히지 않음)
    const mailOverlay = document.getElementById('mailOverlay');
    if (mailOverlay) {
        mailOverlay.addEventListener('click', function(e) {
            // 배경 클릭으로는 닫히지 않도록 주석 처리
            // if (e.target === this) closeEmailModal();
        });
    }

    // 입력 필드 포커스 시 오류 상태 제거 및 더티 플래그 설정
    const fields = ['senderName', 'senderEmail', 'subject', 'message'];
    fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        
        if (field) {
            // 포커스 시 오류 상태 제거
            field.addEventListener('focus', function() {
                this.classList.remove('error');
                const errorId = fieldId === 'senderName' ? 'nameError' :
                                fieldId === 'senderEmail' ? 'emailError' :
                                fieldId === 'subject' ? 'subjectError' : 'messageError';
                const errorElement = document.getElementById(errorId);
                if (errorElement) errorElement.classList.remove('visible');
            });
            
            // 입력 시 더티 플래그 설정
            field.addEventListener('input', markFormDirty);
            field.addEventListener('change', markFormDirty);
        }
    });
}

// 이메일 HTML 로드 함수
async function loadEmailComponent() {
    try {
        const response = await fetch('/static/components/modal.html');
        const html = await response.text();
        
        // body 끝에 추가
        document.body.insertAdjacentHTML('beforeend', html);
        
        // 이메일 모듈 초기화
        initEmailModule();
        
        console.log('Email component loaded successfully');
    } catch (error) {
        console.error('Failed to load email component:', error);
    }
}