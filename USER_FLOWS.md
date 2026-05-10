# CinAImatic - User Flow & Architecture

## 🗺️ User Flow Diagrams

### Landing Page Flow
```
User Visits / 
    ↓
Landing Page Loads
├─ Hero Section
├─ Features Section
├─ CTA Section
└─ Footer
    ↓
User Actions:
├─ Click "Login" → Opens Login Modal
├─ Click "Sign Up" → Opens Signup Modal
├─ Click "Get Started" → Opens Signup Modal
├─ Click "Learn More" → Scroll to Features
├─ Click "Create Account" → Opens Signup Modal
└─ Click Logo → Redirects to /
```

### Authentication Flow (Modal Based)
```
User on Landing Page
    ↓
Click "Login"/"Sign Up"
    ↓
Modal Opens
    ├─ If Login:
    │  ├─ Email Input
    │  ├─ Password Input
    │  ├─ Remember Me
    │  ├─ Login Button
    │  └─ "Sign up" Link → Switches to Signup Form
    │
    └─ If Signup:
       ├─ Full Name Input
       ├─ Email Input
       ├─ Password Input
       ├─ Confirm Password Input
       ├─ Terms Checkbox
       ├─ Sign Up Button
       └─ "Login" Link → Switches to Login Form
    ↓
User Submits Form
    ├─ Validation (Client-side)
    ├─ API Call (Server-side - TODO)
    ├─ Success → Redirect to Dashboard
    └─ Error → Show Error Message
```

### Standalone Auth Flow
```
User Visits /login
    ↓
Login Page Loads
├─ Logo + Branding
├─ Email Input
├─ Password Input
├─ Forgot Password Link
├─ Sign In Button
├─ Social Login Buttons
└─ "Sign up" Link → Redirects to /signup
    ↓
User Submits
    ├─ API Call to /api/login
    ├─ Success → Redirect to Dashboard
    └─ Error → Show Error Message

User Visits /signup
    ↓
Signup Page Loads
├─ Logo + Branding
├─ Full Name Input
├─ Email Input
├─ Password Input
├─ Confirm Password Input
├─ Terms Checkbox
├─ Sign Up Button
├─ Social Signup Buttons
└─ "Login" Link → Redirects to /login
    ↓
User Submits
    ├─ API Call to /api/signup
    ├─ Success → Redirect to Login Page
    └─ Error → Show Error Message
```

---

## 🏗️ Application Architecture

### Frontend Architecture
```
CinAImatic/
│
├── Public Pages
│   ├── landing.html (Landing Page)
│   ├── login.html (Dedicated Login)
│   └── signup.html (Dedicated Signup)
│
├── Assets & Styling
│   └── src/
│       ├── style.css (Tailwind CSS)
│       ├── landing.js (Landing Interactivity)
│       └── auth.js (Auth Form Handling)
│
├── Backend Server
│   └── server.js (Express Routes)
│
└── Documentation
    ├── QUICKSTART.md
    ├── FRONTEND_README.md
    ├── IMPLEMENTATION_SUMMARY.md
    └── USER_FLOWS.md (this file)
```

### Component Hierarchy
```
Landing Page
├── Navigation Bar
│   ├── Logo
│   └── Auth Buttons
│
├── Hero Section
│   ├── Background Animation
│   ├── Main Headline
│   ├── Subheadline
│   ├── CTA Buttons
│   └── Stats Grid
│
├── Features Section
│   ├── Section Title
│   └── Feature Cards (3)
│       ├── Icon
│       ├── Title
│       └── Description
│
├── CTA Section
│   ├── Card Container
│   ├── Headline
│   └── Call-to-Action
│
├── Modal (Auth)
│   ├── Login Form
│   │   ├── Email Input
│   │   ├── Password Input
│   │   ├── Remember Me
│   │   └── Submit Button
│   │
│   └── Signup Form
│       ├── Full Name Input
│       ├── Email Input
│       ├── Password Inputs (2)
│       ├── Terms Checkbox
│       └── Submit Button
│
└── Footer
    ├── Footer Columns
    └── Copyright
```

---

## 📊 State Management Flow

### Modal State
```
Modal Hidden (Default)
    ↓
User clicks Login/Signup button
    ↓
Modal Visible
├─ showLogin() → Display login form, hide signup form
└─ showSignup() → Display signup form, hide login form
    ↓
User clicks X or outside modal
    ↓
Modal Hidden
```

### Form State
```
Form Inputs (Empty)
    ↓
User Types
    ↓
Real-time Validation
├─ Email validation on blur
├─ Password strength on input
└─ Confirm password match on blur
    ↓
User Submits
    ↓
All Validation
├─ Email format check
├─ Password length check
├─ Password match check
├─ Terms acceptance check
└─ All required fields filled
    ↓
Valid → Send API Request
Invalid → Show Error Message
    ↓
API Response
├─ Success → Redirect/Show Success
└─ Error → Show Error Message
```

---

## 🔄 Event Flow Diagram

### Button Click Events
```
Navigation Buttons
├─ #loginBtn.click → openLoginModal() → showLoginForm()
├─ #signupBtn.click → openLoginModal() → showSignupForm()
├─ #getStartedBtn.click → openLoginModal() → showSignupForm()
├─ #learnMoreBtn.click → scrollToFeatures()
└─ #ctaSignupBtn.click → openLoginModal() → showSignupForm()

Form Switching
├─ #switchToSignup.click → showSignupForm()
└─ #switchToLogin.click → showLoginForm()

Modal Controls
├─ #closeLoginModal.click → closeModal()
├─ #closeSignupModal.click → closeModal()
└─ #loginModal.click (outside) → closeModal()

Form Submission
├─ #loginFormElement.submit → validateLogin() → submitLogin()
└─ #signupFormElement.submit → validateSignup() → submitSignup()
```

### Password Toggle Events
```
Password Input
    ↓
User clicks eye icon
    ↓
togglePassword()
├─ if type === "password" → type = "text" (show)
└─ if type === "text" → type = "password" (hide)
    ↓
Update icon (👁️ ↔ 🙈)
```

---

## 🔐 Authentication Flow (Detailed)

### Login Process
```
1. User fills email and password
   ├─ Client-side validation
   │  ├─ Email format check
   │  └─ Password not empty
   └─ Visual feedback
       └─ Enable submit button

2. User clicks "Sign In"
   ├─ Disable button (prevent duplicate)
   ├─ Show loading state
   └─ Send POST to /api/login

3. Server receives request
   ├─ Validate input
   ├─ Query database (TODO)
   ├─ Check password (TODO)
   ├─ Generate JWT token (TODO)
   └─ Return response

4. Client receives response
   ├─ Success:
   │  ├─ Store token (localStorage/sessionStorage)
   │  ├─ Show success message
   │  └─ Redirect to /dashboard
   └─ Error:
      ├─ Re-enable button
      ├─ Show error message
      └─ Highlight failed field
```

### Signup Process
```
1. User fills all fields
   ├─ Full name
   ├─ Email
   ├─ Password
   ├─ Confirm password
   └─ Terms checkbox

2. Client-side validation
   ├─ Name not empty
   ├─ Email format valid
   ├─ Password ≥ 8 chars
   ├─ Password has uppercase
   ├─ Password has lowercase
   ├─ Password has numbers
   ├─ Passwords match
   └─ Terms accepted

3. Validation passes
   ├─ Disable button
   ├─ Show loading state
   └─ Send POST to /api/signup

4. Server receives request
   ├─ Validate input again
   ├─ Check email not exists (TODO)
   ├─ Hash password (TODO)
   ├─ Create user in DB (TODO)
   ├─ Send verification email (TODO)
   └─ Return response

5. Client receives response
   ├─ Success:
   │  ├─ Show success message
   │  ├─ Redirect to /login
   │  └─ Pre-fill email in login
   └─ Error:
      ├─ Show specific error
      └─ Allow retry
```

---

## 🎨 Visual Flow - Landing Page Sections

### Section 1: Navigation (Fixed)
```
┌─────────────────────────────────────────────┐
│ 🎬 CinAImatic     [Login] [Sign Up]        │
└─────────────────────────────────────────────┘
```

### Section 2: Hero
```
┌─────────────────────────────────────────────┐
│                                             │
│   Discover Your Next                        │
│   Cinematic Masterpiece                     │
│                                             │
│   [Get Started Now]  [Learn More]           │
│                                             │
│   10K+          99%          50K+           │
│   Movies        Accuracy     Users          │
│                                             │
└─────────────────────────────────────────────┘
```

### Section 3: Features
```
┌─────────────────────────────────────────────┐
│         Why Choose CinAImatic?              │
│                                             │
│  ┌────────────┬────────────┬────────────┐   │
│  │ 🤖 AI      │ 🎯 Person  │ ⚡ Lightning│   │
│  │ Powered    │ alized     │ Fast       │   │
│  │ ...        │ ...        │ ...        │   │
│  └────────────┴────────────┴────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### Section 4: CTA
```
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐    │
│  │ Ready to Find Your Next Favorite?   │    │
│  │ [Create Your Account]               │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### Section 5: Footer
```
┌─────────────────────────────────────────────┐
│ CinAImatic   │ Product    │ Company  │ Legal│
│ AI-powered   │ Features   │ About    │ Priv│
│ ...          │ Pricing    │ Blog     │ Term│
│              │ API        │ Contact  │     │
├─────────────────────────────────────────────┤
│ © 2026 CinAImatic. All rights reserved.     │
└─────────────────────────────────────────────┘
```

---

## 🔗 Route Mapping

### Frontend Routes
| Route | File | Purpose |
|-------|------|---------|
| `/` | `landing.html` | Main landing page |
| `/login` | `login.html` | Standalone login page |
| `/signup` | `signup.html` | Standalone signup page |
| `/components` | `components.html` | Component showcase (demo) |

### API Routes (Backend - TODO)
| Route | Method | Purpose | Body |
|-------|--------|---------|------|
| `/api/login` | POST | User login | `{email, password}` |
| `/api/signup` | POST | User registration | `{fullname, email, password}` |
| `/api/logout` | POST | User logout | `{}` |
| `/api/refresh` | POST | Refresh token | `{token}` |
| `/api/verify` | POST | Verify email | `{token}` |
| `/api/reset-password` | POST | Reset password | `{email}` |

---

## 💾 Data Flow

### Form Data → Server
```
User Input
  ↓
JavaScript Object
{
  email: "user@example.com",
  password: "SecurePass123"
}
  ↓
JSON Stringified
"{"email":"user@example.com","password":"SecurePass123"}"
  ↓
HTTP POST Request
  ↓
Server Receives
  ↓
Parse JSON
  ↓
Validate
  ↓
Database Operations
```

### Server Response → Client
```
Database
  ↓
Success/Error Object
{
  success: true,
  token: "eyJhbGc...",
  user: { id, email, name }
}
  ↓
JSON Response
  ↓
HTTP 200/400/401
  ↓
Client JavaScript
  ↓
Handle Response
  ↓
Update UI / Redirect
```

---

## 🔒 Security Checkpoints

### Client-Side
- ✅ Email format validation
- ✅ Password length check
- ✅ Password strength validation
- ✅ Match password confirmation
- ✅ Terms acceptance check
- ✅ Input sanitization (HTML encoded)

### Server-Side (TODO)
- 🔧 Input validation (again)
- 🔧 Email uniqueness check
- 🔧 Password hashing (bcrypt)
- 🔧 Rate limiting
- 🔧 HTTPS only
- 🔧 CSRF token validation
- 🔧 JWT signature verification
- 🔧 Database encryption

---

## 📈 Performance Flow

```
Page Load
  ↓
HTML Parse (landing.html - 50KB)
  ↓
CSS Load (style.css via Tailwind - 40KB)
  ↓
JavaScript Execute (landing.js - 8KB, auth.js - 6KB)
  ↓
DOM Ready
  ↓
CSS Animation Start
  ↓
User Interaction Ready ✓
  ↓
Lazy Load Images (if any)
  ↓
Fully Interactive ✓
```

### Optimization Tips
- Use CDN for CSS/JS
- Minify production builds
- Enable compression (gzip)
- Lazy load below-the-fold content
- Cache static assets
- Optimize images

---

## 🚀 Deployment Flow

```
Local Development
  ↓
npm start → http://localhost:3000
  ↓
Push to GitHub
  ↓
CI/CD Pipeline (GitHub Actions)
  ├─ Run tests
  ├─ Build
  └─ Deploy
  ↓
Production Server
  ↓
Users Access https://ciaimetic.com
```

---

## 📱 Responsive Flow

```
Desktop (>1024px)
├─ 3-column grid for features
├─ Large hero text
└─ Horizontal button layout

Tablet (640-1024px)
├─ 2-column grid for features
├─ Medium hero text
└─ Horizontal button layout

Mobile (<640px)
├─ 1-column grid (stacked)
├─ Smaller hero text
└─ Vertical button layout
```

---

## ✅ Checklist for Developers

### Before Going Live
- [ ] Test all form validations
- [ ] Test modal open/close
- [ ] Test form switching
- [ ] Test responsive design (all sizes)
- [ ] Test on different browsers
- [ ] Test on mobile devices
- [ ] Check console for errors
- [ ] Test form submission (with backend)
- [ ] Test error scenarios
- [ ] Performance testing
- [ ] Security audit
- [ ] Accessibility check

### Integration Checklist
- [ ] Connect login API
- [ ] Connect signup API
- [ ] Implement token storage
- [ ] Add protected routes
- [ ] Test authentication flow
- [ ] Implement logout
- [ ] Add session management
- [ ] Test all edge cases

---

This document provides a complete visual reference for understanding how CinAImatic's frontend works! 🎬✨
