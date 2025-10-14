// Initialize tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Password visibility toggle
document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordInput = document.getElementById('password');
    const icon = this.querySelector('i');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});

document.getElementById('toggleConfirmPassword').addEventListener('click', function() {
    const confirmPasswordInput = document.getElementById('confirm_password');
    const icon = this.querySelector('i');
    
    if (confirmPasswordInput.type === 'password') {
        confirmPasswordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        confirmPasswordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});

// Name validation (letters and spaces only)
function validateName(inputId, errorId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);
    const namePattern = /^[A-Za-z\s]*$/;
    
    if (input.value && !namePattern.test(input.value)) {
        error.classList.add('show');
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        return false;
    } else if (input.value) {
        error.classList.remove('show');
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        return true;
    } else {
        error.classList.remove('show');
        input.classList.remove('is-invalid', 'is-valid');
        return false;
    }
}

document.getElementById('first_name').addEventListener('blur', function() {
    validateName('first_name', 'firstNameError');
});

document.getElementById('last_name').addEventListener('blur', function() {
    validateName('last_name', 'lastNameError');
});

// Student ID validation - Format: 00-0000-000
document.getElementById('student_id').addEventListener('blur', function() {
    const input = this;
    const error = document.getElementById('studentIdError');
    const idPattern = /^\d{2}-\d{4}-\d{3}$/; // Format: 00-0000-000
    
    if (input.value && !idPattern.test(input.value)) {
        error.textContent = '❌ Format must be: 00-0000-000 (e.g., 23-1234-567)';
        error.classList.add('show');
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    } else if (input.value) {
        error.classList.remove('show');
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        error.classList.remove('show');
        input.classList.remove('is-invalid', 'is-valid');
    }
});

// Real-time formatting for Student ID
document.getElementById('student_id').addEventListener('input', function(e) {
    const input = e.target;
    let value = input.value.replace(/\D/g, ''); // Remove non-digits
    
    // Format as 00-0000-000
    if (value.length > 2) {
        value = value.substring(0, 2) + '-' + value.substring(2);
    }
    if (value.length > 7) {
        value = value.substring(0, 7) + '-' + value.substring(7);
    }
    
    // Limit to 11 characters (00-0000-000)
    if (value.length > 11) {
        value = value.substring(0, 11);
    }
    
    input.value = value;
});

// Email validation for .edu domains
document.getElementById('email').addEventListener('blur', function() {
    const input = this;
    const error = document.getElementById('emailError');
    const studentEmailPattern = /\.edu$/i;
    
    if (input.value && !studentEmailPattern.test(input.value)) {
        error.classList.add('show');
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    } else if (input.value && studentEmailPattern.test(input.value)) {
        error.classList.remove('show');
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        error.classList.remove('show');
        input.classList.remove('is-invalid', 'is-valid');
    }
});

// Password validation
function validatePassword(password) {
    const hasMinLength = password.length >= 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
    
    return hasMinLength && hasUppercase && hasLowercase && hasNumber && hasSpecial;
}

document.getElementById('password').addEventListener('blur', function() {
    const input = this;
    const error = document.getElementById('passwordError');
    
    if (input.value && !validatePassword(input.value)) {
        error.classList.add('show');
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    } else if (input.value) {
        error.classList.remove('show');
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        error.classList.remove('show');
        input.classList.remove('is-invalid', 'is-valid');
    }
    
    checkPasswordMatch();
});

// Password confirmation validation
document.getElementById('confirm_password').addEventListener('blur', checkPasswordMatch);

function checkPasswordMatch() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const error = document.getElementById('confirmPasswordError');
    const input = document.getElementById('confirm_password');
    
    if (confirmPassword && password !== confirmPassword) {
        error.classList.add('show');
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    } else if (confirmPassword && password === confirmPassword) {
        error.classList.remove('show');
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        error.classList.remove('show');
        input.classList.remove('is-invalid', 'is-valid');
    }
}

// Real-time validation for confirm password when typing
document.getElementById('confirm_password').addEventListener('input', function() {
    const password = document.getElementById('password').value;
    if (password) {
        checkPasswordMatch();
    }
});

// Form submission validation
document.getElementById('signupForm').addEventListener('submit', function(e) {
    let isValid = true;
    
    // Validate all fields
    const firstNameValid = validateName('first_name', 'firstNameError');
    const lastNameValid = validateName('last_name', 'lastNameError');
    
  
        const studentId = document.getElementById('student_id');
        const studentIdPattern = /^\d{2}-\d{4}-\d{3}$/; // New pattern
        const studentIdValid = studentId.value && studentIdPattern.test(studentId.value);
        if (!studentIdValid && studentId.value) {
            document.getElementById('studentIdError').classList.add('show');
            studentId.classList.add('is-invalid');
            isValid = false;
        }
            
    const email = document.getElementById('email');
    const studentEmailPattern = /\.edu$/i;
    const emailValid = email.value && studentEmailPattern.test(email.value);
    if (!emailValid && email.value) {
        document.getElementById('emailError').classList.add('show');
        email.classList.add('is-invalid');
        isValid = false;
    }
    
    const passwordValid = validatePassword(document.getElementById('password').value);
    if (!passwordValid && document.getElementById('password').value) {
        document.getElementById('passwordError').classList.add('show');
        document.getElementById('password').classList.add('is-invalid');
        isValid = false;
    }
    
    const passwordsMatch = document.getElementById('password').value === document.getElementById('confirm_password').value;
    if (!passwordsMatch && document.getElementById('confirm_password').value) {
        document.getElementById('confirmPasswordError').classList.add('show');
        document.getElementById('confirm_password').classList.add('is-invalid');
        isValid = false;
    }
    
    // Check required fields are filled
    const requiredFields = ['first_name', 'last_name', 'student_id', 'email', 'password', 'confirm_password'];
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field.value) {
            field.classList.add('is-invalid');
            isValid = false;
        }
    });
    
    if (!isValid) {
        e.preventDefault();
        alert('Please fix the validation errors before submitting.');
    } else {
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating Account...';
        submitBtn.disabled = true;
    }
});

// Clear validation on focus
document.querySelectorAll('.form-control').forEach(input => {
    input.addEventListener('focus', function() {
        this.classList.remove('is-invalid');
        const errorId = this.id + 'Error';
        const errorElement = document.getElementById(errorId);
        if (errorElement) {
            errorElement.classList.remove('show');
        }
    });
});