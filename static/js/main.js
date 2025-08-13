// Main JavaScript for ClipToEarn

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();
    
    // Initialize form validation
    initFormValidation();
    
    // Initialize auto-dismiss alerts
    initAlerts();
    
    // Initialize responsive tables
    initResponsiveTables();
    
    // Initialize loading states
    initLoadingStates();
    
    // Initialize datetime inputs
    initDatetimeInputs();
});

// Tooltip initialization
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'absolute bg-gray-800 text-white text-xs rounded px-2 py-1 z-50';
    tooltip.textContent = e.target.getAttribute('data-tooltip');
    tooltip.style.top = e.target.offsetTop - 30 + 'px';
    tooltip.style.left = e.target.offsetLeft + 'px';
    tooltip.id = 'tooltip';
    document.body.appendChild(tooltip);
}

function hideTooltip() {
    const tooltip = document.getElementById('tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showFieldError(input, 'Bu alan zorunludur');
            isValid = false;
        } else {
            hideFieldError(input);
        }
    });
    
    // URL validation
    const urlInputs = form.querySelectorAll('input[type="url"]');
    urlInputs.forEach(input => {
        if (input.value && !isValidUrl(input.value)) {
            showFieldError(input, 'Geçerli bir URL giriniz');
            isValid = false;
        }
    });
    
    // Email validation
    const emailInputs = form.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        if (input.value && !isValidEmail(input.value)) {
            showFieldError(input, 'Geçerli bir email adresi giriniz');
            isValid = false;
        }
    });
    
    return isValid;
}

function showFieldError(input, message) {
    hideFieldError(input);
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-red-400 text-sm mt-1';
    errorDiv.textContent = message;
    errorDiv.setAttribute('data-field-error', input.name);
    input.parentNode.appendChild(errorDiv);
    input.classList.add('border-red-500');
}

function hideFieldError(input) {
    const existingError = input.parentNode.querySelector(`[data-field-error="${input.name}"]`);
    if (existingError) {
        existingError.remove();
    }
    input.classList.remove('border-red-500');
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Alert auto-dismiss
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.className = 'float-right text-xl font-bold opacity-70 hover:opacity-100';
        closeBtn.addEventListener('click', () => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        });
        alert.appendChild(closeBtn);
    });
}

// Responsive tables
function initResponsiveTables() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        if (window.innerWidth < 768) {
            table.classList.add('text-sm');
        }
    });
    
    window.addEventListener('resize', () => {
        tables.forEach(table => {
            if (window.innerWidth < 768) {
                table.classList.add('text-sm');
            } else {
                table.classList.remove('text-sm');
            }
        });
    });
}

// Loading states
function initLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            form.addEventListener('submit', function() {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Gönderiliyor...';
            });
        }
    });
}

// Datetime inputs
function initDatetimeInputs() {
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    datetimeInputs.forEach(input => {
        // Set minimum date to now
        const now = new Date();
        const minDate = new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
        input.min = minDate;
        
        // Set default value if empty
        if (!input.value) {
            const defaultDate = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000 - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
            input.value = defaultDate;
        }
    });
}

// Utility functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 p-4 rounded-md z-50 ${getToastClass(type)}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

function getToastClass(type) {
    switch(type) {
        case 'success':
            return 'bg-green-800 text-green-100';
        case 'error':
            return 'bg-red-800 text-red-100';
        case 'warning':
            return 'bg-yellow-800 text-yellow-100';
        default:
            return 'bg-blue-800 text-blue-100';
    }
}

function formatNumber(number) {
    return new Intl.NumberFormat('tr-TR').format(number);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'USD' }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('tr-TR', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Progress calculation
function calculateProgress(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const now = new Date();
    
    const total = end - start;
    const elapsed = now - start;
    
    return Math.min(100, Math.max(0, (elapsed / total) * 100));
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Panoya kopyalandı!', 'success');
    }).catch(() => {
        showToast('Kopyalama başarısız!', 'error');
    });
}

// Confirm dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Auto-refresh for admin dashboard
if (window.location.pathname.includes('/admin/')) {
    setInterval(() => {
        const lastUpdate = document.getElementById('last-update');
        if (lastUpdate) {
            lastUpdate.textContent = new Date().toLocaleTimeString('tr-TR');
        }
    }, 60000);
}

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('hidden');
    }
}

// Search functionality
function initSearch() {
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const target = document.querySelector(input.getAttribute('data-search'));
            const searchTerm = input.value.toLowerCase();
            
            if (target) {
                const rows = target.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
        });
    });
}

// Initialize search if present
document.addEventListener('DOMContentLoaded', initSearch);
