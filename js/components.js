/**
 * Reusable Component Functions
 */

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const types = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-amber-500',
        info: 'bg-primary-500'
    };

    const notification = document.createElement('div');
    notification.className = `${types[type]} text-white px-6 py-3 rounded-lg shadow-lg fixed bottom-6 right-6 animate-slide-up z-50`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('opacity-0', 'transition-opacity');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Loading state for buttons
 */
function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner spinner-sm"></span> Loading...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || 'Submit';
    }
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Format date
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Debounce function
 */
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Modal component
 */
class Modal {
    constructor(id) {
        this.modal = document.getElementById(id);
        this.closeBtn = this.modal?.querySelector('[data-close-modal]');
        this.init();
    }

    init() {
        if (!this.modal) return;

        this.closeBtn?.addEventListener('click', () => this.close());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.close();
        });
    }

    open() {
        this.modal?.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    close() {
        this.modal?.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
}

/**
 * Tabs component
 */
class Tabs {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.tabs = this.container?.querySelectorAll('[data-tab]') || [];
        this.panels = this.container?.querySelectorAll('[data-panel]') || [];
        this.init();
    }

    init() {
        this.tabs.forEach((tab, index) => {
            tab.addEventListener('click', () => this.selectTab(index));
        });
    }

    selectTab(index) {
        this.tabs.forEach((tab, i) => {
            if (i === index) {
                tab.classList.add('border-primary-600', 'text-primary-600', 'dark:border-primary-400', 'dark:text-primary-400');
                tab.classList.remove('border-transparent', 'text-slate-600');
            } else {
                tab.classList.remove('border-primary-600', 'text-primary-600', 'dark:border-primary-400', 'dark:text-primary-400');
                tab.classList.add('border-transparent', 'text-slate-600');
            }
        });

        this.panels.forEach((panel, i) => {
            if (i === index) {
                panel.classList.remove('hidden');
            } else {
                panel.classList.add('hidden');
            }
        });
    }
}

export { showNotification, setButtonLoading, formatFileSize, formatDate, debounce, Modal, Tabs };
