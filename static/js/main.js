// Python Kurz - Hlavní JavaScript soubor

// Inicializace po načtení stránky
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Hlavní inicializační funkce
function initializeApp() {
    // Inicializace tooltipů
    initializeTooltips();
    
    // Inicializace animací
    initializeAnimations();
    
    // Inicializace interaktivních prvků
    initializeInteractiveElements();
    
    // Nastavení keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Inicializace progress tracking
    initializeProgressTracking();
}

// Inicializace tooltipů
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Inicializace animací
function initializeAnimations() {
    // Animace při scrollování
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Pozorování všech animovatelných prvků
    document.querySelectorAll('.course-card, .quick-action-card, .progress-card, .achievement-card').forEach(el => {
        observer.observe(el);
    });
}

// Inicializace interaktivních prvků
function initializeInteractiveElements() {
    // Hover efekty pro karty
    initializeCardHoverEffects();
    
    // Click efekty pro tlačítka
    initializeButtonEffects();
    
    // Progress bar animace
    initializeProgressBars();
    
    // Code editor funkce
    initializeCodeEditor();
}

// Hover efekty pro karty
function initializeCardHoverEffects() {
    const cards = document.querySelectorAll('.course-card, .quick-action-card, .progress-card, .achievement-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Click efekty pro tlačítka
function initializeButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Vytvoření ripple efektu
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Inicializace progress barů
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
}

// Inicializace code editoru
function initializeCodeEditor() {
    const codeEditor = document.getElementById('codeEditor');
    
    if (codeEditor) {
        // Syntax highlighting (základní)
        codeEditor.addEventListener('input', function() {
            highlightSyntax(this);
        });
        
        // Auto-resize
        codeEditor.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
        
        // Tab support
        codeEditor.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end = this.selectionEnd;
                
                this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });
    }
}

// Základní syntax highlighting
function highlightSyntax(textarea) {
    const code = textarea.value;
    const lines = code.split('\n');
    let highlighted = '';
    
    lines.forEach(line => {
        // Komentáře
        if (line.trim().startsWith('#')) {
            highlighted += '<span class="comment">' + line + '</span>\n';
        }
        // Klíčová slova
        else if (line.includes('print') || line.includes('if') || line.includes('for') || line.includes('while')) {
            highlighted += '<span class="keyword">' + line + '</span>\n';
        }
        // Řetězce
        else if (line.includes('"') || line.includes("'")) {
            highlighted += '<span class="string">' + line + '</span>\n';
        }
        else {
            highlighted += line + '\n';
        }
    });
    
    // V reálné aplikaci by se zde použil proper syntax highlighter
}

// Nastavení keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter pro spuštění kódu v playground
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const runButton = document.querySelector('.btn-success');
            if (runButton && runButton.textContent.includes('Spustit')) {
                runButton.click();
            }
        }
        
        // Escape pro zavření modálů
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

// Inicializace progress tracking
function initializeProgressTracking() {
    // Sledování času stráveného na stránce
    let startTime = Date.now();
    
    window.addEventListener('beforeunload', function() {
        const timeSpent = Date.now() - startTime;
        // V reálné aplikaci by se zde odeslal čas na server
        console.log('Čas strávený na stránce:', Math.round(timeSpent / 1000), 'sekund');
    });
    
    // Sledování scrollování
    let scrollDepth = 0;
    window.addEventListener('scroll', function() {
        const currentScroll = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
        if (currentScroll > scrollDepth) {
            scrollDepth = currentScroll;
        }
    });
}

// Utility funkce
const Utils = {
    // Debounce funkce
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle funkce
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Formátování času
    formatTime: function(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}h ${minutes}m ${secs}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${secs}s`;
        } else {
            return `${secs}s`;
        }
    },
    
    // Generování náhodného ID
    generateId: function() {
        return Math.random().toString(36).substr(2, 9);
    },
    
    // Kopírování do schránky
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Zkopírováno do schránky!', 'success');
            });
        } else {
            // Fallback pro starší prohlížeče
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showNotification('Zkopírováno do schránky!', 'success');
        }
    },
    
    // Zobrazení notifikace
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    },
    
    // Validace emailu
    isValidEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    // Animace počítadla
    animateCounter: function(element, start, end, duration) {
        const startTime = performance.now();
        const startValue = parseInt(start);
        const endValue = parseInt(end);
        
        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = Math.round(startValue + (endValue - startValue) * progress);
            element.textContent = currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        }
        
        requestAnimationFrame(updateCounter);
    }
};

// Event listeners pro globální funkce
document.addEventListener('click', function(e) {
    // Kopírování kódu
    if (e.target.classList.contains('copy-code')) {
        const codeBlock = e.target.closest('.code-block');
        if (codeBlock) {
            const code = codeBlock.querySelector('pre').textContent;
            Utils.copyToClipboard(code);
        }
    }
    
    // Zvýraznění aktivního odkazu v navigaci
    if (e.target.tagName === 'A') {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        e.target.classList.add('active');
    }
});

// Responzivní funkce
function handleResize() {
    const isMobile = window.innerWidth < 768;
    
    // Přizpůsobení pro mobilní zařízení
    if (isMobile) {
        document.body.classList.add('mobile');
    } else {
        document.body.classList.remove('mobile');
    }
    
    // Přizpůsobení code editoru
    const codeEditor = document.getElementById('codeEditor');
    if (codeEditor) {
        if (isMobile) {
            codeEditor.style.height = '200px';
        } else {
            codeEditor.style.height = '300px';
        }
    }
}

// Event listener pro změnu velikosti okna
window.addEventListener('resize', Utils.debounce(handleResize, 250));

// Inicializace při načtení
handleResize();

// Export pro použití v jiných souborech
// Autentifikace
function getAuthToken() {
    return localStorage.getItem('access_token');
}

function setAuthToken(token) {
    localStorage.setItem('access_token', token);
}

function removeAuthToken() {
    localStorage.removeItem('access_token');
}

function isLoggedIn() {
    return getAuthToken() !== null;
}

// AJAX helper s autentifikací
async function apiRequest(url, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        // Token je neplatný, odhlásit uživatele
        removeAuthToken();
        window.location.href = '/login';
        return;
    }
    
    return response;
}

// Logout funkce
function logout() {
    removeAuthToken();
    window.location.href = '/';
}

// Přidání logout funkce do window objektu
window.logout = logout;

window.PythonKurz = {
    Utils: Utils,
    initializeApp: initializeApp,
    getAuthToken: getAuthToken,
    setAuthToken: setAuthToken,
    removeAuthToken: removeAuthToken,
    isLoggedIn: isLoggedIn,
    apiRequest: apiRequest,
    logout: logout
};
