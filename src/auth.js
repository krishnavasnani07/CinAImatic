// Toggle password visibility
const toggleButtons = document.querySelectorAll('[id^="togglePassword"]');
const confirmToggleButtons = document.querySelectorAll('[id^="toggleConfirmPassword"]');

toggleButtons.forEach(button => {
    button.addEventListener('click', () => {
        const passwordInput = document.getElementById('passwordInput');
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            button.textContent = '🙈';
        } else {
            passwordInput.type = 'password';
            button.textContent = '👁️';
        }
    });
});

confirmToggleButtons.forEach(button => {
    button.addEventListener('click', () => {
        const confirmPasswordInput = document.getElementById('confirmPasswordInput');
        if (confirmPasswordInput.type === 'password') {
            confirmPasswordInput.type = 'text';
            button.textContent = '🙈';
        } else {
            confirmPasswordInput.type = 'password';
            button.textContent = '👁️';
        }
    });
});

// Login Form Handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(loginForm);
        const email = formData.get('email');
        const password = formData.get('password');
        const remember = formData.get('remember') === 'on';

        // Validate
        if (!email || !password) {
            alert('Please fill in all fields');
            return;
        }

        try {
            // TODO: Replace with actual backend API call
            console.log('Login attempt:', { email, password, remember });
            
            // Show loading state
            const button = loginForm.querySelector('button[type="submit"]');
            const originalText = button.textContent;
            button.textContent = 'Signing In...';
            button.disabled = true;

            // Simulated API call
            setTimeout(() => {
                alert('Login successful! Redirecting...');
                // window.location.href = '/dashboard';
                button.textContent = originalText;
                button.disabled = false;
            }, 1500);

        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed. Please try again.');
        }
    });
}

// Signup Form Handler
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(signupForm);
        const fullname = formData.get('fullname');
        const email = formData.get('email');
        const password = formData.get('password');
        const confirmpassword = formData.get('confirmpassword');
        const terms = formData.get('terms') === 'on';

        // Validation
        if (!fullname || !email || !password || !confirmpassword) {
            alert('Please fill in all fields');
            return;
        }

        if (password.length < 8) {
            alert('Password must be at least 8 characters');
            return;
        }

        if (password !== confirmpassword) {
            alert('Passwords do not match');
            return;
        }

        if (!terms) {
            alert('Please agree to the Terms of Service');
            return;
        }

        // Validate password strength
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/;
        if (!passwordRegex.test(password)) {
            alert('Password must contain uppercase, lowercase, and numbers');
            return;
        }

        try {
            // TODO: Replace with actual backend API call
            console.log('Signup attempt:', { fullname, email, password });
            
            // Show loading state
            const button = signupForm.querySelector('button[type="submit"]');
            const originalText = button.textContent;
            button.textContent = 'Creating Account...';
            button.disabled = true;

            // Simulated API call
            setTimeout(() => {
                alert('Account created successfully! Redirecting to login...');
                // window.location.href = '/login.html';
                button.textContent = originalText;
                button.disabled = false;
            }, 1500);

        } catch (error) {
            console.error('Signup error:', error);
            alert('Signup failed. Please try again.');
        }
    });
}

// Password strength indicator
const passwordInput = document.getElementById('passwordInput');
if (passwordInput && signupForm) {
    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        let strength = 0;

        if (password.length >= 8) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/\d/.test(password)) strength++;
        if (/[^a-zA-Z\d]/.test(password)) strength++;

        // Could add visual feedback here
        console.log('Password strength:', strength);
    });
}

// Email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Real-time email validation
const emailInputs = document.querySelectorAll('input[type="email"]');
emailInputs.forEach(input => {
    input.addEventListener('blur', () => {
        if (input.value && !validateEmail(input.value)) {
            input.classList.add('border-red-500');
        } else {
            input.classList.remove('border-red-500');
        }
    });
});
