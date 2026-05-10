# CinAImatic Design System & Style Guide

## 🎨 Design System Overview

A complete design system for consistent, professional UI across CinAImatic.

---

## 🎯 Color Palette

### Primary Colors
```css
/* Red (Primary Brand Color) */
--red-50:   #fef2f2
--red-100:  #fee2e2
--red-500:  #ef4444  /* Accent text, hover states */
--red-600:  #dc2626  /* Primary buttons, main accent */
--red-700:  #b91c1c  /* Hover states, dark mode */

/* Usage */
.primary-btn { @apply bg-red-600 hover:bg-red-700; }
.primary-text { @apply text-red-500; }
.primary-border { @apply border-red-500; }
```

### Grayscale
```css
/* Blacks & Grays */
--bg-primary:   #0a0a0a  /* Main background */
--bg-secondary: #121212  /* Card backgrounds */
--bg-tertiary:  #1a1a1a  /* Elevated surfaces */

--text-primary:   #e4e2e1  /* Body text */
--text-secondary: #a8a8a8  /* Secondary text */
--text-tertiary:  #6b7280  /* Disabled text, placeholders */

/* Usage */
body { @apply bg-[#0a0a0a] text-[#e4e2e1]; }
.secondary-text { @apply text-gray-400; }
.tertiary-text { @apply text-gray-600; }
```

### Accent Colors
```css
/* Gradients */
--gradient-red-pink-purple: linear-gradient(to right, #ef4444, #ec4899, #a855f7)
--gradient-red-dark: linear-gradient(to right, #dc2626, #b91c1c)

/* Usage */
.gradient-text { @apply bg-gradient-to-r from-red-500 via-pink-500 to-purple-500 text-transparent bg-clip-text; }
.gradient-btn { @apply bg-gradient-to-r from-red-600 to-red-700; }
```

### Semantic Colors
```css
/* Status Colors */
--success: #22c55e    /* Green - Success, approved */
--warning: #f59e0b    /* Amber - Warning, pending */
--error:   #ef4444    /* Red - Error, invalid */
--info:    #3b82f6    /* Blue - Info, notification */

/* Usage */
.success { @apply text-green-500; }
.error { @apply text-red-500; }
.warning { @apply text-amber-500; }
.info { @apply text-blue-500; }
```

---

## 🔤 Typography System

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
```

### Font Sizes & Weights
```
Heading 1: 48px (3rem) | Font-weight: 700 (Bold)
Heading 2: 36px (2.25rem) | Font-weight: 700 (Bold)
Heading 3: 28px (1.75rem) | Font-weight: 700 (Bold)
Heading 4: 24px (1.5rem) | Font-weight: 700 (Bold)
Heading 5: 20px (1.25rem) | Font-weight: 700 (Bold)
Heading 6: 16px (1rem) | Font-weight: 700 (Bold)

Body Text: 16px (1rem) | Font-weight: 400 (Regular)
Body Small: 14px (0.875rem) | Font-weight: 400 (Regular)
Body Tiny: 12px (0.75rem) | Font-weight: 400 (Regular)

Button: 16px (1rem) | Font-weight: 700 (Bold)
Label: 14px (0.875rem) | Font-weight: 500 (Medium)
Hint: 12px (0.75rem) | Font-weight: 400 (Regular)
```

### Usage Examples
```html
<!-- Heading 1 -->
<h1 class="text-6xl font-bold">Discover Your Next Cinematic Masterpiece</h1>

<!-- Heading 2 -->
<h2 class="text-4xl font-bold">Why Choose CinAImatic?</h2>

<!-- Body Text -->
<p class="text-lg text-gray-300">Experience personalized movie recommendations</p>

<!-- Button Text -->
<button class="text-lg font-bold">Get Started Now</button>

<!-- Label -->
<label class="text-sm font-medium text-gray-300">Email Address</label>

<!-- Hint -->
<p class="text-xs text-gray-400">At least 8 characters with uppercase, lowercase, and numbers</p>
```

---

## 🎨 Component System

### Buttons

#### Primary Button
```html
<button class="px-8 py-4 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg font-bold text-lg hover:shadow-lg hover:shadow-red-500/50 transition-all transform hover:scale-105">
    Get Started Now
</button>
```
**Usage**: Main CTAs, primary actions
**States**: 
- Default: Red gradient
- Hover: Scale up, red shadow
- Active: Pressed state
- Disabled: Opacity 50%

#### Secondary Button
```html
<button class="px-8 py-4 border-2 border-white/30 text-white rounded-lg font-bold text-lg hover:bg-white/10 transition-all">
    Learn More
</button>
```
**Usage**: Secondary actions, alternatives
**States**:
- Default: Transparent with border
- Hover: Light background
- Active: Pressed state
- Disabled: Opacity 50%

#### Text Button
```html
<button class="px-6 py-2 text-white hover:text-red-500 transition-colors font-medium">
    Login
</button>
```
**Usage**: Navigation, links, less important actions
**States**:
- Default: White text
- Hover: Red text
- Active: Red text
- Disabled: Gray text

#### Button Sizes
```html
<!-- Large -->
<button class="px-8 py-4 text-lg font-bold">Large Button</button>

<!-- Medium (default) -->
<button class="px-6 py-3 text-base font-bold">Medium Button</button>

<!-- Small -->
<button class="px-4 py-2 text-sm font-medium">Small Button</button>
```

### Form Inputs

#### Text Input
```html
<input 
    type="email" 
    placeholder="your@email.com"
    class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-red-500 focus:outline-none text-white placeholder-gray-500 transition-colors"
/>
```
**States**:
- Default: White/10 background, white/20 border
- Focus: White/10 background, red border
- Error: White/10 background, red border
- Disabled: Opacity 50%

#### Checkbox
```html
<input 
    type="checkbox" 
    class="w-4 h-4 rounded border-white/20 bg-white/10 cursor-pointer"
/>
```
**States**:
- Unchecked: Empty box
- Checked: Red background with checkmark
- Disabled: Opacity 50%

#### Select Input
```html
<select class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-red-500 focus:outline-none text-white transition-colors">
    <option>Choose option</option>
</select>
```

#### Textarea
```html
<textarea 
    placeholder="Enter message..."
    class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-red-500 focus:outline-none text-white placeholder-gray-500 transition-colors resize-none"
    rows="4"
></textarea>
```

### Cards

#### Glassmorphism Card
```html
<div class="glass-card p-8 rounded-xl hover:border-red-500/50 transition-all">
    <h3 class="text-2xl font-bold mb-3">Card Title</h3>
    <p class="text-gray-300">Card content goes here</p>
</div>
```
**CSS Definition**:
```css
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
```
**Usage**: Feature cards, containers, sections

#### Feature Card
```html
<div class="glass-card p-8 rounded-xl hover:border-red-500/50 transition-all">
    <div class="w-12 h-12 bg-red-600/20 rounded-lg flex items-center justify-center mb-4 text-2xl">🎬</div>
    <h3 class="text-2xl font-bold mb-3">Feature Name</h3>
    <p class="text-gray-300">Feature description and benefits</p>
</div>
```
**Usage**: Feature highlights

### Modals

#### Modal Container
```html
<div id="modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
    <div class="w-full max-w-md glass-card p-8 rounded-xl">
        <!-- Modal Content -->
    </div>
</div>
```
**Properties**:
- Backdrop: Black 80% opacity + blur
- Container: Centered, fixed positioning
- Content: Glass card with padding

#### Modal Form
```html
<form>
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-3xl font-bold">Modal Title</h2>
        <button type="button" class="text-gray-400 hover:text-white text-2xl">✕</button>
    </div>
    <!-- Form inputs -->
</form>
```

---

## 🎬 Spacing System

### Padding
```css
/* Consistent spacing */
1 unit = 4px (0.25rem)

px-1  = 4px    (0.25rem)  /* Extra small padding */
px-2  = 8px    (0.5rem)   /* Small */
px-3  = 12px   (0.75rem)  /* Base */
px-4  = 16px   (1rem)     /* Medium */
px-6  = 24px   (1.5rem)   /* Large */
px-8  = 32px   (2rem)     /* Extra large */
```

### Margin & Gap
```css
/* Same scale as padding */
gap-4 = 16px
mb-4  = margin-bottom: 16px
mt-6  = margin-top: 24px
```

### Common Spacing Patterns
```html
<!-- Sections -->
<section class="py-24 px-6">Content</section>

<!-- Containers -->
<div class="max-w-6xl mx-auto px-6">Content</div>

<!-- Cards -->
<div class="glass-card p-8 rounded-xl">Content</div>

<!-- Grid Gaps -->
<div class="grid grid-cols-3 gap-8">
    <div>Item</div>
    <div>Item</div>
    <div>Item</div>
</div>
```

---

## 🔄 Transitions & Animations

### Duration Scale
```css
duration-75    = 75ms   (Micro interactions)
duration-100   = 100ms  (Button hover)
duration-200   = 200ms  (Fade in/out)
duration-300   = 300ms  (Slide transitions)
duration-500   = 500ms  (Major transitions)
duration-700   = 700ms  (Slow animations)
```

### Common Transitions
```html
<!-- Color transition -->
<button class="text-white hover:text-red-500 transition-colors">Button</button>

<!-- Scale on hover -->
<button class="hover:scale-105 transition-all">Button</button>

<!-- Opacity fade -->
<div class="opacity-0 hover:opacity-100 transition-opacity">Content</div>

<!-- Combined transition -->
<button class="bg-red-600 hover:bg-red-700 hover:shadow-lg hover:scale-105 transition-all">Button</button>
```

### Animations
```css
/* Fade in animation */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Slide up animation */
@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* Usage */
.animate-fade-in { animation: fadeIn 0.3s ease-in; }
.animate-slide-up { animation: slideUp 0.5s ease-out; }
```

---

## 📐 Responsive Design

### Breakpoints
```css
/* Tailwind breakpoints */
sm  = 640px   (Tablets)
md  = 768px   (Small laptops)
lg  = 1024px  (Desktops)
xl  = 1280px  (Large desktops)
2xl = 1536px  (Extra large)

/* Mobile-first approach */
.responsive-class = mobile (default)
@sm:responsive-class = tablet
@md:responsive-class = small laptop
@lg:responsive-class = desktop
```

### Responsive Examples
```html
<!-- Grid that changes columns -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div>Item</div>
    <div>Item</div>
    <div>Item</div>
</div>

<!-- Text that scales -->
<h1 class="text-4xl md:text-5xl lg:text-6xl font-bold">Title</h1>

<!-- Hidden on mobile -->
<div class="hidden md:block">Desktop only content</div>

<!-- Stacked buttons -->
<div class="flex flex-col sm:flex-row gap-4">
    <button>Button 1</button>
    <button>Button 2</button>
</div>
```

---

## ♿ Accessibility Guidelines

### Semantic HTML
```html
<!-- Good -->
<button>Click me</button>
<input type="email" aria-label="Email address" />
<nav>Navigation</nav>
<main>Main content</main>
<footer>Footer</footer>

<!-- Avoid -->
<div class="button">Click me</div>
<div class="input"></div>
```

### Color Contrast
```
AAA Standard (Best): Contrast ratio ≥ 7:1
AA Standard (Good): Contrast ratio ≥ 4.5:1
Fail: Contrast ratio < 4.5:1

Example: #e4e2e1 (text) on #0a0a0a (background)
Ratio: 13.5:1 ✅ Exceeds AAA
```

### ARIA Labels
```html
<!-- Form inputs -->
<label for="email">Email</label>
<input id="email" type="email" />

<!-- Buttons -->
<button aria-label="Close modal">✕</button>

<!-- Icons as buttons -->
<button aria-label="Search">🔍</button>

<!-- Important regions -->
<nav aria-label="Main navigation"></nav>
<main aria-label="Main content"></main>
```

### Focus States
```html
<!-- Always include focus state -->
<input class="focus:outline-none focus:ring-2 focus:ring-red-500" />
<button class="focus:outline-none focus:ring-2 focus:ring-red-500" />
```

---

## 🖼️ Imagery & Icons

### Icon Style
```html
<!-- Emoji icons (current approach) -->
<span class="text-2xl">🎬</span>
<span class="text-3xl">🤖</span>
<span class="text-4xl">🎯</span>

<!-- Icon sizing -->
.icon-sm = 16px (1rem)
.icon-md = 24px (1.5rem)
.icon-lg = 32px (2rem)
.icon-xl = 48px (3rem)
```

### Image Guidelines
```html
<!-- Always include alt text -->
<img src="movie.jpg" alt="Movie poster for The Matrix" />

<!-- Responsive images -->
<img 
    srcset="movie-sm.jpg 640w, movie-md.jpg 1024w, movie-lg.jpg 1536w"
    src="movie.jpg"
    alt="Movie poster"
/>
```

---

## 🔍 Best Practices

### DO ✅
- ✅ Use semantic HTML
- ✅ Follow consistent spacing
- ✅ Use the color palette
- ✅ Test on mobile
- ✅ Include focus states
- ✅ Write alt text
- ✅ Use accessible colors
- ✅ Keep animations subtle
- ✅ Provide feedback on interactions
- ✅ Use consistent typography

### DON'T ❌
- ❌ Mix color palettes
- ❌ Use non-semantic HTML
- ❌ Create custom spacing
- ❌ Ignore focus states
- ❌ Use too many animations
- ❌ Forget mobile design
- ❌ Use inaccessible colors
- ❌ Break typography hierarchy
- ❌ Remove default focus indicators
- ❌ Use tiny text

---

## 📦 Component Quick Reference

| Component | File | CSS Class | State Variants |
|-----------|------|-----------|-----------------|
| Primary Button | landing.html | `.primary-btn` | default, hover, active, disabled |
| Secondary Button | landing.html | `.secondary-btn` | default, hover, active, disabled |
| Text Button | landing.html | `.text-btn` | default, hover, active, disabled |
| Card | landing.html | `.glass-card` | default, hover |
| Input | login.html | `.form-input` | default, focus, error, disabled |
| Modal | landing.html | `#loginModal` | hidden, visible |
| Badge | - | `.badge` | info, success, warning, error |

---

## 🎨 Customization Examples

### Change Primary Color (Red → Blue)
```bash
# Find and replace in HTML/CSS:
bg-red-600 → bg-blue-600
text-red-500 → text-blue-500
hover:text-red-500 → hover:text-blue-500
from-red-600 → from-blue-600
border-red-500 → border-blue-500
```

### Change Typography
```html
<!-- Make text larger -->
<h1 class="text-7xl">Larger Heading</h1>

<!-- Change font weight -->
<h1 class="text-6xl font-black">Bolder Text</h1>

<!-- Add custom font -->
/* In style.css */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
body { font-family: 'Poppins', sans-serif; }
```

---

This design system ensures consistency, maintainability, and professional appearance across CinAImatic! 🎬✨
