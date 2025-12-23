/**
 * FORM VALIDATION MODULE
 * Module untuk validasi form yang mudah dipahami dan reusable
 * 
 * Fitur:
 * - Password visibility toggle
 * - Real-time email validation
 * - Username validation
 * - Password strength checker
 * - Loading state management
 * - Error message display
 */

// ========================================
// PASSWORD TOGGLE - Show/Hide Password
// ========================================
class PasswordToggle {
    constructor(passwordFieldId) {
        this.passwordField = document.getElementById(passwordFieldId);
        this.toggleButton = null;
        this.init();
    }

    init() {
        if (!this.passwordField) return;

        // Buat wrapper untuk password field
        const wrapper = document.createElement('div');
        wrapper.className = 'password-field-wrapper';

        // Pindahkan password field ke dalam wrapper
        this.passwordField.parentNode.insertBefore(wrapper, this.passwordField);
        wrapper.appendChild(this.passwordField);

        // Buat tombol toggle
        this.toggleButton = document.createElement('button');
        this.toggleButton.type = 'button';
        this.toggleButton.className = 'password-toggle-btn';
        this.toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
        this.toggleButton.setAttribute('aria-label', 'Toggle password visibility');

        // Tambahkan tombol ke wrapper
        wrapper.appendChild(this.toggleButton);

        // Event listener untuk toggle
        this.toggleButton.addEventListener('click', () => this.toggle());
    }

    toggle() {
        // Cek tipe input saat ini
        const isPassword = this.passwordField.type === 'password';

        // Toggle tipe input
        this.passwordField.type = isPassword ? 'text' : 'password';

        // Update icon
        const icon = this.toggleButton.querySelector('i');
        icon.className = isPassword ? 'fas fa-eye-slash' : 'fas fa-eye';
    }
}

// ========================================
// EMAIL VALIDATOR - Validasi Email Real-time
// ========================================
class EmailValidator {
    constructor(emailFieldId) {
        this.emailField = document.getElementById(emailFieldId);
        this.init();
    }

    init() {
        if (!this.emailField) return;

        // Event listener untuk validasi saat user mengetik
        this.emailField.addEventListener('input', () => this.validate());
        this.emailField.addEventListener('blur', () => this.validate());
    }

    validate() {
        const email = this.emailField.value.trim();

        // Regex untuk validasi email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (email === '') {
            this.removeValidationState();
            return true;
        }

        if (emailRegex.test(email)) {
            this.showValid();
            return true;
        } else {
            this.showInvalid('Format email tidak valid');
            return false;
        }
    }

    showValid() {
        this.emailField.classList.remove('input-invalid');
        this.emailField.classList.add('input-valid');
        this.removeError();
    }

    showInvalid(message) {
        this.emailField.classList.remove('input-valid');
        this.emailField.classList.add('input-invalid');
        this.showError(message);
    }

    removeValidationState() {
        this.emailField.classList.remove('input-valid', 'input-invalid');
        this.removeError();
    }

    showError(message) {
        this.removeError();

        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;

        this.emailField.parentNode.appendChild(errorDiv);
    }

    removeError() {
        const existingError = this.emailField.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }
}

// ========================================
// USERNAME VALIDATOR - Validasi Username
// ========================================
class UsernameValidator {
    constructor(usernameFieldId) {
        this.usernameField = document.getElementById(usernameFieldId);
        this.minLength = 3;
        this.init();
    }

    init() {
        if (!this.usernameField) return;

        this.usernameField.addEventListener('input', () => this.validate());
        this.usernameField.addEventListener('blur', () => this.validate());
    }

    validate() {
        const username = this.usernameField.value.trim();

        if (username === '') {
            this.removeValidationState();
            return true;
        }

        // Validasi panjang minimum
        if (username.length < this.minLength) {
            this.showInvalid(`Username minimal ${this.minLength} karakter`);
            return false;
        }

        // Validasi karakter (hanya huruf, angka, underscore, dash)
        const usernameRegex = /^[a-zA-Z0-9_-]+$/;
        if (!usernameRegex.test(username)) {
            this.showInvalid('Username hanya boleh huruf, angka, _ dan -');
            return false;
        }

        this.showValid();
        return true;
    }

    showValid() {
        this.usernameField.classList.remove('input-invalid');
        this.usernameField.classList.add('input-valid');
        this.removeError();
    }

    showInvalid(message) {
        this.usernameField.classList.remove('input-valid');
        this.usernameField.classList.add('input-invalid');
        this.showError(message);
    }

    removeValidationState() {
        this.usernameField.classList.remove('input-valid', 'input-invalid');
        this.removeError();
    }

    showError(message) {
        this.removeError();

        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;

        this.usernameField.parentNode.appendChild(errorDiv);
    }

    removeError() {
        const existingError = this.usernameField.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }
}

// ========================================
// PASSWORD STRENGTH - Cek Kekuatan Password
// ========================================
class PasswordStrength {
    constructor(passwordFieldId) {
        this.passwordField = document.getElementById(passwordFieldId);
        this.strengthIndicator = null;
        this.init();
    }

    init() {
        if (!this.passwordField) return;

        // Buat strength indicator
        this.createStrengthIndicator();

        // Event listener
        this.passwordField.addEventListener('input', () => this.checkStrength());
    }

    createStrengthIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'password-strength';
        indicator.innerHTML = `
            <div class="strength-bar">
                <div class="strength-bar-fill"></div>
            </div>
            <div class="strength-text"></div>
        `;

        // Insert after the password wrapper, not inside it
        // This prevents overlap with the toggle button
        const passwordWrapper = this.passwordField.closest('.password-field-wrapper');
        if (passwordWrapper) {
            // Insert after the wrapper
            passwordWrapper.parentNode.insertBefore(indicator, passwordWrapper.nextSibling);
        } else {
            // Fallback: insert after password field
            this.passwordField.parentNode.appendChild(indicator);
        }

        this.strengthIndicator = indicator;
    }

    checkStrength() {
        const password = this.passwordField.value;

        if (password === '') {
            this.strengthIndicator.style.display = 'none';
            return;
        }

        this.strengthIndicator.style.display = 'block';

        let strength = 0;
        let strengthText = '';
        let strengthClass = '';

        // Cek panjang
        if (password.length >= 8) strength++;
        if (password.length >= 12) strength++;

        // Cek huruf kecil
        if (/[a-z]/.test(password)) strength++;

        // Cek huruf besar
        if (/[A-Z]/.test(password)) strength++;

        // Cek angka
        if (/[0-9]/.test(password)) strength++;

        // Cek karakter spesial
        if (/[^a-zA-Z0-9]/.test(password)) strength++;

        // Tentukan level kekuatan
        if (strength <= 2) {
            strengthText = 'Lemah';
            strengthClass = 'weak';
        } else if (strength <= 4) {
            strengthText = 'Sedang';
            strengthClass = 'medium';
        } else {
            strengthText = 'Kuat';
            strengthClass = 'strong';
        }

        // Update UI
        const barFill = this.strengthIndicator.querySelector('.strength-bar-fill');
        const textElement = this.strengthIndicator.querySelector('.strength-text');

        barFill.style.width = `${(strength / 6) * 100}%`;
        barFill.className = `strength-bar-fill ${strengthClass}`;
        textElement.textContent = `Kekuatan: ${strengthText}`;
        textElement.className = `strength-text ${strengthClass}`;
    }
}

// ========================================
// FORM SUBMIT HANDLER - Loading State
// ========================================
class FormSubmitHandler {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.submitButton = null;
        this.originalButtonText = '';
        this.init();
    }

    init() {
        if (!this.form) return;

        this.submitButton = this.form.querySelector('button[type="submit"]');
        if (!this.submitButton) return;

        this.originalButtonText = this.submitButton.innerHTML;

        // Event listener untuk submit
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    handleSubmit(e) {
        // Cek validasi form
        if (!this.form.checkValidity()) {
            return; // Biarkan browser handle validasi default
        }

        // Tampilkan loading state
        this.showLoading();
    }

    showLoading() {
        this.submitButton.disabled = true;
        this.submitButton.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            Processing...
        `;
        this.submitButton.style.opacity = '0.7';
    }

    hideLoading() {
        this.submitButton.disabled = false;
        this.submitButton.innerHTML = this.originalButtonText;
        this.submitButton.style.opacity = '1';
    }
}

// ========================================
// INITIALIZE - Jalankan semua validator
// ========================================
function initializeFormValidation() {
    // Password toggle
    new PasswordToggle('password');

    // Email validator
    new EmailValidator('email');

    // Username validator
    new UsernameValidator('username');

    // Password strength (hanya untuk form create)
    const passwordField = document.getElementById('password');
    if (passwordField) {
        new PasswordStrength('password');
    }

    // Form submit handler
    new FormSubmitHandler('userForm');
}

// Jalankan saat DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeFormValidation);
} else {
    initializeFormValidation();
}
