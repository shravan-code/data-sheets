# 📊 Data Sheets - Technical Documentation Platform

A modern, elegant web platform for organizing, managing, and sharing technical data sheets and specifications. Built with **HTML, CSS, JavaScript, and Tailwind CSS**.

## 🎨 Design Aesthetic

**Modern Professional Minimalism** with:
- Sophisticated color palette (Indigo/Purple primary accents)
- Elegant serif fonts (Crimson Text) for headlines
- Clean sans-serif typography for body content
- Smooth animations and micro-interactions
- Dark mode by default (light mode included)
- Enterprise-ready, approachable tone

## 📁 Project Structure

```
data-sheets/
├── index.html                 # Homepage (main entry point)
├── tailwind.config.js         # Tailwind CSS configuration
│
├── css/
│   └── styles.css            # Custom themes, components & utilities
│
├── js/
│   ├── main.js               # Core app logic (theme, menu, animations)
│   └── components.js         # Reusable component utilities
│
├── pages/                    # Additional pages (to be created)
│   ├── dashboard.html
│   ├── upload.html
│   ├── browse.html
│   ├── login.html
│   └── signup.html
│
├── components/              # Reusable component templates
│   ├── header.html
│   ├── footer.html
│   ├── modal.html
│   └── notification.html
│
└── assets/
    ├── images/
    └── icons/
```

## 🚀 Quick Start

### Option 1: Direct in Browser (No Build Required)
```bash
# Just open index.html in a browser
# Works offline (uses CDN for Tailwind)
```

### Option 2: With Local Development Server
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server

# Using VS Code
# Install Live Server extension and click "Go Live"
```

Then open `http://localhost:8000` in your browser.

## 🎯 Features Implemented

### Homepage (`index.html`)
- ✅ Responsive navigation with mobile menu
- ✅ Dark/light theme toggle with persistence
- ✅ Hero section with gradients and animations
- ✅ Features showcase (6 cards with staggered animations)
- ✅ Benefits section with icons
- ✅ Pricing table (3 tiers)
- ✅ CTA (Call-to-Action) section
- ✅ Professional footer with links
- ✅ Smooth scroll navigation
- ✅ Intersection observer for scroll animations

## 🎨 Customization

### Color Scheme
Edit `tailwind.config.js` to modify the primary color palette:
```javascript
colors: {
  primary: { /* 50-950 shades */ },
  accent: { /* 50-950 shades */ },
  slate: { /* 50-950 shades */ }
}
```

### Fonts
Configured fonts in `tailwind.config.js`:
- **Display**: Crimson Text (serif) - Headlines
- **Body**: Segoe UI (sans-serif) - Body text
- **Mono**: JetBrains Mono - Code

To change, update the `fontFamily` in theme.extend.

### Theme Variables
CSS custom properties in `css/styles.css`:
```css
--color-primary
--color-accent
--color-text-primary
--color-bg-light
--color-border
```

## 🧩 Component Usage

### Buttons
```html
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-secondary">Secondary Button</button>
<button class="btn btn-outline">Outline Button</button>
<button class="btn btn-ghost">Ghost Button</button>
```

### Cards
```html
<div class="card">
  Content here
</div>
<div class="card card-elevated">
  Elevated card with more shadow
</div>
```

### Badges
```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-error">Error</span>
```

### Animations
```html
<!-- Fade in on scroll -->
<div class="animate-fade-in" data-animate>Content</div>

<!-- Slide up on load -->
<div class="animate-slide-up">Content</div>

<!-- Slide in from left -->
<div class="animate-slide-in-left" data-animate>Content</div>
```

## 🔧 JavaScript Features

### Theme Manager
- Automatic theme detection from system preferences
- LocalStorage persistence
- One-click toggle

### Mobile Menu Manager
- Responsive hamburger menu
- Auto-close on link click
- Outside click handling

### Smooth Scroll
- Click hash links for smooth scrolling
- Works with `#id` anchors

### Animation Observer
- Auto-animate elements with `data-animate` attribute
- Intersection Observer for performance

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px)
- Optimized for all screen sizes
- Touch-friendly buttons (min 44px height)

## 🔐 Security Considerations

- No external API calls on homepage
- CORS-safe CDN for Tailwind
- Safe HTML structure
- No inline scripts

## 📊 Performance

- CSS-only animations (GPU accelerated)
- Lazy-loaded images ready
- Optimized Tailwind purging
- < 50KB total CSS

## 🎯 Next Steps

Create additional pages:
1. **`pages/dashboard.html`** - User dashboard with recent sheets
2. **`pages/upload.html`** - File upload interface
3. **`pages/browse.html`** - Search and browse sheets
4. **`pages/login.html`** - Login form
5. **`pages/signup.html`** - Sign up form

Create reusable components:
1. **`components/header.html`** - Navigation header
2. **`components/footer.html`** - Footer template
3. **`components/modal.html`** - Modal dialogs
4. **`components/forms.html`** - Form components

## 🛠️ Troubleshooting

### Tailwind classes not working
- Ensure `tailwind.config.js` has correct paths
- Clear browser cache
- Use Full Build: `npx tailwindcss -i ./css/styles.css -o ./css/output.css`

### Dark mode not toggling
- Check browser LocalStorage isn't disabled
- Verify theme button ID is `theme-toggle`
- Check console for JavaScript errors

### Animations not playing
- Enable `data-animate` attribute on elements
- Check that Intersection Observer is supported (all modern browsers)
- Verify CSS animations aren't disabled in browser

## 📄 License

MIT License - Feel free to use and modify!

## 💡 Tips

1. **Color Gradients**: Use `text-gradient` class for gradient text
2. **Loading States**: Use `setButtonLoading()` function for button loading
3. **Notifications**: Use `showNotification()` for toast messages
4. **Date Formatting**: Use `formatDate()` and `formatFileSize()` utilities
5. **Spacing**: Use Tailwind spacing scale: `py-4`, `px-6`, etc.

---

**Built with ❤️ for engineers, by engineers**
