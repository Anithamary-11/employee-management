// CHANGE THIS URL to your Production Backend Server URL (e.g. Render/Railway/Heroku)
// Default is set to localhost for active development.
const API_BASE = 'https://employee-management-api-rsvn.onrender.com/api';

function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;
    
    const bgColor = type === 'success' ? 'bg-success' : 'bg-danger';
    const toastId = 'toast-' + Date.now();
    
    const toastHtml = `
        <div id="${toastId}" class="toast show align-items-center text-white ${bgColor} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="document.getElementById('${toastId}').remove()"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    setTimeout(() => {
        const t = document.getElementById(toastId);
        if(t) t.remove();
    }, 5000);
}

async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json'
            },
            ...options
        });
        const data = await response.json();
        if (!response.ok) {
            const errorMsg = data.detail || 'Something went wrong';
            showToast(errorMsg, 'error');
            throw new Error(errorMsg);
        }
        return data;
    } catch (err) {
        if (!options.silent) {
            // Toast may be handled by UI, or show generic
        }
        throw err;
    }
}

function setupLiveValidation(formId, rules) {
    const form = document.getElementById(formId);
    if (!form) return;

    function validateField(input, ruleSet) {
        let valid = true;
        let errorMessage = '';
        const val = input.value.trim();

        if (ruleSet.includes('required') && !val) {
            valid = false;
            errorMessage = 'This field is required';
        } else if (ruleSet.includes('email') && val) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!re.test(val)) {
                valid = false;
                errorMessage = 'Invalid email address';
            }
        } else if (ruleSet.includes('positive') && val) {
            if (parseFloat(val) <= 0) {
                valid = false;
                errorMessage = 'Must be > 0';
            }
        } else if (ruleSet.includes('nonNegative') && val) {
            if (parseFloat(val) < 0) {
                valid = false;
                errorMessage = 'Cannot be negative';
            }
        }

        if (valid) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
            const feedback = input.nextElementSibling;
            if(feedback && feedback.classList.contains('invalid-feedback')) {
                feedback.textContent = errorMessage;
            } else if (input.parentElement && input.parentElement.querySelector('.invalid-feedback')) {
                 input.parentElement.querySelector('.invalid-feedback').textContent = errorMessage;
            }
        }
        return valid;
    }

    Object.keys(rules).forEach(fieldName => {
        const input = form.elements[fieldName];
        if (input) {
            input.addEventListener('input', () => validateField(input, rules[fieldName]));
            input.addEventListener('change', () => validateField(input, rules[fieldName]));
        }
    });

    return function isFormValid() {
        let valid = true;
        Object.keys(rules).forEach(fieldName => {
            const input = form.elements[fieldName];
            if (input && !validateField(input, rules[fieldName])) {
                valid = false;
            }
        });
        return valid;
    }
}

function renderPagination(totalRecords, limit, currentPage, containerId, pageChangeCallbackFnName) {
    const totalPages = Math.ceil(totalRecords / limit);
    const container = document.getElementById(containerId);
    if (!container) return;
    
    let html = '';
    
    html += `<li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="${pageChangeCallbackFnName}(${currentPage - 1}); return false;">
                  <i class="ti ti-chevron-left"></i> prev
                </a>
             </li>`;
             
    for (let i = 1; i <= totalPages; i++) {
        if (totalPages > 7) {
            if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
                html += `<li class="page-item ${currentPage === i ? 'active' : ''}"><a class="page-link" href="#" onclick="${pageChangeCallbackFnName}(${i}); return false;">${i}</a></li>`;
            } else if (i === currentPage - 3 || i === currentPage + 3) {
                html += `<li class="page-item disabled"><a class="page-link" href="#">...</a></li>`;
            }
        } else {
            html += `<li class="page-item ${currentPage === i ? 'active' : ''}"><a class="page-link" href="#" onclick="${pageChangeCallbackFnName}(${i}); return false;">${i}</a></li>`;
        }
    }

    html += `<li class="page-item ${currentPage === totalPages || totalPages === 0 ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="${pageChangeCallbackFnName}(${currentPage + 1}); return false;">
                  next <i class="ti ti-chevron-right"></i>
                </a>
             </li>`;
             
    container.innerHTML = html;
}
