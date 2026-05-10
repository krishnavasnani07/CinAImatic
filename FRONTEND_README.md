# CinAImatic Frontend - Landing & Auth Pages

## Overview
This package contains a modern, responsive landing page and authentication system for the CinAImatic AI movie recommendation website.

## Features Implemented

### 1. **Landing Page** (`landing.html`)
- Hero section with gradient text and call-to-action buttons
- Feature highlights with glassmorphism cards
- Statistics showcase
- Responsive design for all devices
- Smooth scroll animations
- Footer with links

### 2. **Authentication Pages**
- **Login Page** (`login.html`) - Dedicated login interface
- **Signup Page** (`signup.html`) - User registration interface
- Modal-based auth on landing page

### 3. **Styling**
- Built with **Tailwind CSS** for utility-first styling
- Glassmorphism design pattern
- Dark theme optimized for movie content
- Smooth transitions and hover effects
- Responsive breakpoints (mobile, tablet, desktop)

### 4. **Interactivity**
- Modal system for login/signup
- Form validation
- Password visibility toggle
- Form submission handling
- Smooth page transitions
- Scroll-triggered animations

## File Structure

```
CinAImatic/
├── landing.html           # Main landing page with hero and features
├── login.html             # Dedicated login page
├── signup.html            # Dedicated signup page
├── server.js              # Express backend with API routes
└── src/
    ├── style.css          # Tailwind CSS styling
    ├── landing.js         # Landing page interactivity
    └── auth.js            # Authentication form handling
```

## Getting Started

### Installation
```bash
cd CinAImatic
npm install
```

### Development
```bash
npm run dev
```
This starts Vite development server

### Production Build
```bash
npm run build
```

### Run Server
```bash
npm start
```
Server runs on `http://localhost:3000`

## Component Breakdown

### Landing Page Elements

#### Navigation Bar
- Logo with branding
- Login/Sign Up buttons
- Fixed position with backdrop blur

#### Hero Section
- Animated gradient background
- Main headline with gradient text
- Subheadline
- Two CTA buttons (Get Started, Learn More)
- Stats section (Movies, Accuracy, Users)

#### Features Section
- 3-column grid of feature cards
- AI-Powered, Personalized, Lightning Fast
- Glassmorphism design
- Hover animations

#### CTA Section
- Call-to-action for account creation
- Highlighted card design

### Authentication System

#### Login Modal/Page
- Email input with validation
- Password input with show/hide toggle
- Remember me checkbox
- Forgot password link
- Social login (Google, GitHub)
- Link to signup page

#### Signup Modal/Page
- Full name input
- Email with validation
- Password with strength requirements
- Confirm password
- Terms & conditions checkbox
- Social signup options
- Link to login page

## Styling Guide

### Color Scheme
- **Primary**: Red (#dc2626, #991b1b)
- **Background**: Dark Gray (#0a0a0a, #121212)
- **Text**: Light Gray (#e4e2e1)
- **Accents**: Purple, Pink gradients

### CSS Classes
- `.glass-card` - Glassmorphism effect
- `.hero-gradient` - Background gradient
- `bg-[#0a0a0a]` - Main background
- `text-red-500` - Primary accent color

## API Integration Points

### Login Endpoint
```
POST /api/login
Body: { email, password, remember }
Response: { success, token, user }
```

### Signup Endpoint
```
POST /api/signup
Body: { fullname, email, password, confirmpassword }
Response: { success, user }
```

## JavaScript Features

### Landing Page (`landing.js`)
- Modal management (open/close)
- Form switching (login ↔ signup)
- Event listeners for all buttons
- Intersection Observer for animations
- Form submission handlers

### Authentication (`auth.js`)
- Password visibility toggle
- Form validation
- Email validation regex
- Password strength checking
- Loading states
- Error handling

## Responsive Design

### Breakpoints
- **Mobile**: < 640px (single column)
- **Tablet**: 640px - 1024px (2 columns)
- **Desktop**: > 1024px (3 columns)

### Mobile Optimizations
- Stack buttons vertically
- Reduce hero text size
- Adjust padding/margins
- Touch-friendly inputs

## Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Security Considerations

### Current Implementation
- Client-side form validation
- HTTPS ready
- CORS configured for API

### TODO for Production
- Implement JWT authentication
- Add password hashing (bcrypt)
- Set up database (MongoDB/PostgreSQL)
- Add rate limiting
- Implement CSRF protection
- Add email verification
- Set up OAuth integration
- Add refresh token mechanism

## Customization

### Change Colors
Edit `src/style.css` or use Tailwind classes:
```html
<!-- Change red-600 to your color -->
<div class="bg-red-600">...</div>
```

### Modify Content
- Update hero text in `landing.html`
- Change feature descriptions
- Update stats numbers
- Modify footer links

### Add/Remove Sections
- Copy component structure
- Adjust grid layouts
- Update CSS classes
- Test responsive design

## Troubleshooting

### Styles not loading
- Ensure Tailwind CSS is compiled
- Check `src/style.css` is imported
- Run `npm run build`

### Forms not working
- Check browser console for errors
- Verify form IDs match JavaScript
- Ensure input names are correct

### Modal not opening
- Verify `landing.js` is loaded
- Check browser console for JS errors
- Ensure modal element exists in HTML

## Next Steps

1. **Backend Integration**
   - Connect login/signup forms to your API
   - Implement authentication
   - Set up database models

2. **Additional Features**
   - Email verification
   - Password reset flow
   - Social OAuth integration
   - User profile page

3. **Optimization**
   - Image optimization
   - Code splitting
   - Lazy loading
   - Performance monitoring

4. **Testing**
   - Unit tests for form validation
   - E2E tests for user flows
   - Cross-browser testing
   - Mobile testing

## Support

For issues or questions, refer to:
- `server.js` - Backend route definitions
- `src/auth.js` - Form handling logic
- `src/style.css` - Styling system
- Tailwind CSS documentation: https://tailwindcss.com

---

**Made with ❤️ for CinAImatic**
