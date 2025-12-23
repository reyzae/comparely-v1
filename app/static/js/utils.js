// ===================================
// Toast Notification System
// Simple notification untuk user feedback
// ===================================

/**
 * Function untuk show toast notification
 * @param {string} message - Pesan yang mau ditampilkan
 * @param {string} type - Tipe toast: 'success', 'error', 'warning', 'info'
 * @param {number} duration - Durasi tampil dalam ms (default 3000)
 */
function showToast(message, type = 'info', duration = 3000) {
    // Cek apakah toast container sudah ada
    let toastContainer = document.querySelector('.toast-container');

    // Kalau belum ada, buat dulu
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }

    // Buat toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    // Icon berdasarkan type
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };

    // HTML untuk toast
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <p class="toast-message">${message}</p>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;

    // Tambahkan ke container
    toastContainer.appendChild(toast);

    // Auto remove setelah duration
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, duration);
}

// ===================================
// Skeleton Loading Helper
// Untuk show loading state
// ===================================

/**
 * Function untuk create skeleton card
 * @returns {HTMLElement} Skeleton card element
 */
function createSkeletonCard() {
    const skeleton = document.createElement('div');
    skeleton.className = 'skeleton-card';
    skeleton.innerHTML = `
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-button"></div>
    `;
    return skeleton;
}

/**
 * Function untuk show skeleton loading di grid
 * @param {HTMLElement} container - Container element
 * @param {number} count - Jumlah skeleton cards
 */
function showSkeletonLoading(container, count = 6) {
    container.innerHTML = '';
    for (let i = 0; i < count; i++) {
        container.appendChild(createSkeletonCard());
    }
}

// ===================================
// Smooth Scroll Helper
// Untuk smooth scroll ke element
// ===================================

/**
 * Function untuk smooth scroll ke element
 * @param {string} selector - CSS selector untuk target element
 */
function smoothScrollTo(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// ===================================
// Button Loading State Helper
// Untuk toggle loading state pada button
// ===================================

/**
 * Function untuk set button loading state
 * @param {HTMLElement} button - Button element
 * @param {boolean} isLoading - True untuk show loading, false untuk hide
 */
function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.classList.add('loading');
        button.disabled = true;
        // Simpan text original
        button.dataset.originalText = button.textContent;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
        // Restore text original
        if (button.dataset.originalText) {
            button.textContent = button.dataset.originalText;
        }
    }
}

// ===================================
// Fade In Animation Helper
// Untuk animate elements saat muncul
// ===================================

/**
 * Function untuk add fade-in animation ke elements
 * @param {string} selector - CSS selector untuk target elements
 */
function addFadeInAnimation(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach((element, index) => {
        element.classList.add('fade-in');
        // Stagger animation
        if (index < 4) {
            element.classList.add(`fade-in-${index + 1}`);
        }
    });
}

// ===================================
// Local Storage Helper
// Untuk save/load user preferences
// ===================================

/**
 * Function untuk save data ke localStorage
 * @param {string} key - Key untuk data
 * @param {any} value - Value yang mau disimpan
 */
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Error saving to localStorage:', error);
        return false;
    }
}

/**
 * Function untuk load data dari localStorage
 * @param {string} key - Key untuk data
 * @returns {any} Data yang tersimpan atau null
 */
function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return null;
    }
}

// ===================================
// Debounce Helper
// Untuk limit function calls (useful untuk search)
// ===================================

/**
 * Debounce function untuk limit function calls
 * @param {Function} func - Function yang mau di-debounce
 * @param {number} wait - Wait time dalam ms
 * @returns {Function} Debounced function
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===================================
// Export functions untuk digunakan di file lain
// ===================================

// Kalau menggunakan modules, uncomment ini:
// export { showToast, createSkeletonCard, showSkeletonLoading, smoothScrollTo, setButtonLoading, addFadeInAnimation, saveToLocalStorage, loadFromLocalStorage, debounce };
