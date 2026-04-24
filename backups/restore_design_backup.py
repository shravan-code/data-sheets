import os
import sys

# ---------------------------------------------------------------------------
# DESIGN BACKUP (THE GOLDEN CONFIG)
# ---------------------------------------------------------------------------

CSS_BACKUP = """/* DS_SHARED_SIDEBAR_STYLES */
body {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, .font-display {
    font-family: 'Outfit', sans-serif;
}

.grid-bg {
    background-image: linear-gradient(rgba(0,0,0,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0,.05) 1px, transparent 1px);
    background-size: 40px 40px;
}

.dark .grid-bg {
    background-image: linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
}

/* ── Sidebar ────────────────────────────────── */
#ds-sidebar {
    scrollbar-width: thin;
    scrollbar-color: #e2e8f0 transparent;
    transition: transform 0.3s cubic-bezier(.4, 0, .2, 1), opacity 0.3s;
}

.dark #ds-sidebar {
    scrollbar-color: #1e293b transparent;
}

#ds-sidebar::-webkit-scrollbar {
    width: 3px;
}

#ds-sidebar::-webkit-scrollbar-track {
    background: transparent;
}

#ds-sidebar::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 999px;
}

.dark #ds-sidebar::-webkit-scrollbar-thumb {
    background: #1e293b;
}

#ds-sidebar.sidebar-hidden {
    transform: translateX(-100%);
}

#ds-sidebar.sidebar-visible {
    transform: translateX(0);
}

body.sidebar-open #ds-main-content {
    padding-left: 0 !important;
}

/* sidebar nav links */
.sb-link {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: .875rem;
    font-weight: 500;
    color: #64748b;
    text-decoration: none;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    min-height: 40px;
}

.sb-link > i,
.sb-section > span,
.sb-section > i {
    flex-shrink: 0;
}

.sb-link:hover {
    background: rgba(59, 130, 246, 0.05);
    color: #0f172a;
    transform: translateX(2px);
}

.dark .sb-link {
    color: #94a3b8;
}

.dark .sb-link:hover {
    background: rgba(59, 130, 246, 0.1);
    color: #f8fafc;
}

/* Active link indicator */
.sb-link.active {
    background: rgba(59, 130, 246, 0.1);
    color: #2563eb;
    font-weight: 600;
}

.dark .sb-link.active {
    background: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
}

.sb-link.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 20%;
    height: 60%;
    width: 3px;
    background: currentColor;
    border-radius: 0 4px 4px 0;
}

/* category labels */
.sb-cat {
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .05em;
    text-transform: uppercase;
    padding: 20px 12px 8px;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sb-cat::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(148, 163, 184, 0.15);
}

/* section headers */
.sb-section {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    border-radius: 10px;
    font-size: .8125rem;
    font-weight: 700;
    letter-spacing: .03em;
    text-decoration: none;
    margin-bottom: 4px;
    transition: background 0.15s, color 0.15s, transform 0.15s;
    min-height: 40px;
}

.sb-section:hover {
    opacity: .9;
    transform: translateX(2px);
}

/* toggle button */
#sidebar-toggle {
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: .8rem;
    border: 1px solid rgba(148,163,184,.28);
    background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(248,250,252,.96));
    color: #334155;
    box-shadow: 0 8px 20px rgba(15,23,42,.08), 0 1px 2px rgba(15,23,42,.05);
}

#sidebar-toggle:hover {
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    border-color: rgba(59,130,246,.35);
    color: #0f172a;
    transform: translateY(-1px);
}

.dark #sidebar-toggle {
    background: linear-gradient(180deg, rgba(30,41,59,.98), rgba(15,23,42,.94));
    color: #e2e8f0;
    border-color: rgba(71,85,105,.85);
    box-shadow: 0 10px 24px rgba(0,0,0,.28), 0 1px 2px rgba(0,0,0,.3);
}

.dark #sidebar-toggle:hover {
    background: linear-gradient(180deg, #334155, #1e293b);
    color: #f8fafc;
    border-color: rgba(96,165,250,.45);
    transform: translateY(-1px);
}

#sidebar-toggle svg {
    width: 1.1rem;
    height: 1.1rem;
    stroke-width: 2.2;
}

#ds-main-content {
    transition: padding 0.3s cubic-bezier(.4, 0, .2, 1), transform 0.3s cubic-bezier(.4, 0, .2, 1);
}

.portfolio-link {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(148,163,184,.14);
}

.portfolio-link .sb-link {
    background: rgba(59,130,246,.04);
    color: #475569;
}

.portfolio-link .sb-link:hover {
    background: rgba(59,130,246,.08);
    color: #1d4ed8;
}

.dark .portfolio-link {
    border-top-color: rgba(71,85,105,.5);
}

.dark .portfolio-link .sb-link {
    background: rgba(59,130,246,.08);
    color: #cbd5e1;
}

.dark .portfolio-link .sb-link:hover {
    background: rgba(59,130,246,.14);
    color: #93c5fd;
}

/* Scroll-to-top */
#scroll-top {
    opacity: 0;
    pointer-events: none;
    transition: opacity .25s, transform .25s;
}

#scroll-top.visible {
    opacity: 1;
    pointer-events: auto;
    transform: scale(1);
}

/* card hover */
.topic-card {
    transition: all 0.25s cubic-bezier(.4, 0, .2, 1);
}

.topic-card:hover {
    transform: translateY(-4px);
}

.dark .topic-card:hover {
    box-shadow: 0 20px 40px rgba(0,0,0,.5), 0 0 20px rgba(59,130,246,.12);
    border-color: rgba(96,165,250,.3);
}

.topic-card:hover {
    box-shadow: 0 20px 40px rgba(0,0,0,.08);
    border-color: rgba(96,165,250,.3);
}

/* prose */
.prose h2 {
    margin-top: 2.5rem;
    margin-bottom: 1.25rem;
    font-weight: 700;
    color: inherit;
    font-size: 2.25rem;
    letter-spacing: -.02em;
}

.prose h3 {
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-weight: 600;
    color: inherit;
    font-size: 1.6rem;
    letter-spacing: -.01em;
}

.prose p {
    margin-bottom: 1.25rem;
    line-height: 1.8;
    opacity: .9;
}

.prose ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 1.25rem;
}

.prose li {
    margin-bottom: .6rem;
}

.prose code {
    background: rgba(0,0,0,.05);
    padding: .2rem .4rem;
    border-radius: .25rem;
    font-size: .875em;
    font-weight: 500;
}

.dark .prose code {
    background: rgba(255,255,255,.1);
}

@media(min-width:1024px) {
    body.sidebar-open #ds-main-content {
        padding-left: 15rem !important;
    }
}
"""

JS_BACKUP = """(function() {
    const html  = document.documentElement;
    const body  = document.body;

    /* ── Theme ──────────────────────────────────── */
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = html.classList.toggle('dark');
            localStorage.setItem('ds-theme', isDark ? 'dark' : 'light');
        });
    }

    /* ── Sidebar state ───────────────────────────── */
    const sidebar  = document.getElementById('ds-sidebar');
    const overlay  = document.getElementById('sidebar-overlay');
    const togBtn   = document.getElementById('sidebar-toggle');
    const iconOpen  = document.getElementById('sb-icon-open');
    const iconClose = document.getElementById('sb-icon-close');

    // Restore persisted state (default: open on desktop, closed on mobile)
    const isDesktop = () => window.innerWidth >= 1024;
    const stored = localStorage.getItem('ds-sidebar');
    let sidebarOpen = stored !== null ? stored === 'open' : isDesktop();

    /* ── Active Link Highlighting ────────────────── */
    function highlightActive() {
        const path = window.location.pathname;
        const page = path.split('/').pop() || 'index.html';
        const links = document.querySelectorAll('.sb-link');
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.includes(page)) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
    highlightActive();

    function applyState(animate) {
        if (!sidebar) return;
        if (sidebarOpen) {
            sidebar.classList.remove('sidebar-hidden');
            sidebar.classList.add('sidebar-visible');
            body.classList.add('sidebar-open');
            if (overlay) { overlay.style.opacity = '0'; overlay.style.pointerEvents = 'none'; }
            if (!isDesktop() && overlay) { overlay.style.opacity = '1'; overlay.style.pointerEvents = 'auto'; }
            if (iconOpen)  { iconOpen.style.opacity  = '0'; iconOpen.style.transform  = 'scale(.7)'; }
            if (iconClose) { iconClose.style.opacity = '1'; iconClose.style.transform = 'scale(1)'; }
        } else {
            sidebar.classList.add('sidebar-hidden');
            sidebar.classList.remove('sidebar-visible');
            body.classList.remove('sidebar-open');
            if (overlay) { overlay.style.opacity = '0'; overlay.style.pointerEvents = 'none'; }
            if (iconOpen)  { iconOpen.style.opacity  = '1'; iconOpen.style.transform  = 'scale(1)'; }
            if (iconClose) { iconClose.style.opacity = '0'; iconClose.style.transform = 'scale(.7)'; }
        }
    }

    applyState(false);

    if (togBtn) {
        togBtn.addEventListener('click', () => {
            sidebarOpen = !sidebarOpen;
            localStorage.setItem('ds-sidebar', sidebarOpen ? 'open' : 'closed');
            applyState(true);
        });
    }
    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebarOpen = false;
            localStorage.setItem('ds-sidebar', 'closed');
            applyState(true);
        });
    }

    // On resize: if going to desktop re-open by default if never set
    window.addEventListener('resize', () => {
        if (isDesktop() && localStorage.getItem('ds-sidebar') === null) {
            sidebarOpen = true;
            applyState(false);
        }
    });

    /* ── Scroll-to-top ───────────────────────────── */
    const scrollBtn = document.getElementById('scroll-top');
    if (scrollBtn) {
        window.addEventListener('scroll', () => {
            scrollBtn.classList.toggle('visible', window.scrollY > 300);
        });
        scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    /* ── Lucide icons ────────────────────────────── */
    if (typeof lucide !== 'undefined') lucide.createIcons();
})();
"""

# ---------------------------------------------------------------------------
# RESTORE LOGIC
# ---------------------------------------------------------------------------

def restore():
    print("--- Design System Restore ---")
    
    # 1. Root check
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    print(f"Working in: {os.getcwd()}")

    # 2. Restore CSS
    print("Restoring css/ds-main.css...")
    os.makedirs("css", exist_ok=True)
    with open("css/ds-main.css", "w", encoding="utf-8") as f:
        f.write(CSS_BACKUP.strip())

    # 3. Restore JS
    print("Restoring js/ds-main.js...")
    os.makedirs("js", exist_ok=True)
    with open("js/ds-main.js", "w", encoding="utf-8") as f:
        f.write(JS_BACKUP.strip())

    # 4. Trigger full rebuild/patch
    print("Triggering rebuild_all.py to synchronize HTML layouts...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "scripts/rebuild_all.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Successfully synchronized all HTML files.")
        else:
            print(f"Error during rebuild: {result.stderr}")
    except Exception as e:
        print(f"Failed to trigger rebuild: {e}")

    print("\nRestore Complete. The design system is now back to its 'Golden' state.")

if __name__ == "__main__":
    restore()
