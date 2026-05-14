/* Data Cake Main Controller */

(function() {
    const html = document.documentElement;

    /* ── Theme Management ───────────────────────── */
    window.dsInitThemeToggle = function() {
        const themeBtn = document.getElementById('theme-toggle');
        if (!themeBtn) return;

        // Ensure current state matches localStorage
        const savedTheme = localStorage.getItem('theme') || 'dark';
        if (savedTheme === 'dark') html.classList.add('dark');
        else html.classList.remove('dark');

        themeBtn.onclick = () => {
            const isDark = html.classList.contains('dark');
            if (isDark) {
                html.classList.remove('dark');
                localStorage.setItem('theme', 'light');
            } else {
                html.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            }
        };
    };

    /* ── Mobile Sidebar ──────────────────────────── */
    window.dsInitMobileSidebar = function() {
        const sidebar = document.getElementById('mobile-sidebar');
        const overlay = document.getElementById('mobile-sidebar-overlay');
        const openBtn = document.getElementById('topbar-toggle');
        const closeBtn = document.getElementById('mobile-sidebar-close');

        if (!sidebar || !overlay || !openBtn) return;

        const open = () => {
            sidebar.style.transform = 'translateX(0)';
            overlay.style.opacity = '1';
            overlay.style.pointerEvents = 'auto';
        };

        const close = () => {
            sidebar.style.transform = 'translateX(-100%)';
            overlay.style.opacity = '0';
            overlay.style.pointerEvents = 'none';
        };

        openBtn.onclick = open;
        if (closeBtn) closeBtn.onclick = close;
        overlay.onclick = close;

        // Handle category clicks
        sidebar.querySelectorAll('.sb-cat').forEach(cat => {
            cat.onclick = () => {
                cat.classList.toggle('collapsed');
                const nav = cat.nextElementSibling;
                if (nav) nav.classList.toggle('hidden');
            };
        });

        // Close on link click
        sidebar.querySelectorAll('a').forEach(link => {
            link.onclick = close;
        });
    };

    /* ── Profile Pill ────────────────────────────── */
    window.dsInitProfilePill = function() {
        const profileBtn = document.getElementById('profile-btn');
        if (!profileBtn) return;

        profileBtn.classList.add('profile-pill');
        if (!profileBtn.querySelector('.profile-pill-text')) {
            const label = document.createElement('span');
            label.className = 'profile-pill-text';
            label.textContent = 'Shravan Kumar Tela 🙂'; // Short name for pill
            profileBtn.appendChild(label);
        }
    };

    /* ── Table of Contents ──────────────────────── */
    window.dsInitTOC = function() {
        const tocList = document.querySelector('.toc-list');
        const container = document.querySelector('.toc-container');
        if (!tocList || !container) return;

        const headings = Array.from(document.querySelectorAll('article.prose h2'));
        if (headings.length === 0) {
            container.style.display = 'none';
            return;
        }

        tocList.innerHTML = '';
        headings.forEach((h2, idx) => {
            if (!h2.id) {
                h2.id = 'section-' + idx;
            }
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#' + h2.id;
            a.className = 'toc-link';
            a.textContent = h2.textContent.replace('#', '').trim();
            
            a.onclick = (e) => {
                e.preventDefault();
                h2.scrollIntoView({ behavior: 'smooth', block: 'center' });
                history.pushState(null, null, '#' + h2.id);
            };

            li.appendChild(a);
            tocList.appendChild(li);
        });

        // Intersection Observer for active state
        const observerOptions = {
            rootMargin: '-100px 0px -70% 0px',
            threshold: 0
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    document.querySelectorAll('.toc-link').forEach(link => {
                        link.classList.toggle('active', link.getAttribute('href') === '#' + id);
                    });
                }
            });
        }, observerOptions);

        headings.forEach(h2 => observer.observe(h2));
    };

    /* ── Initializer ────────────────────────────── */
    function init() {
        window.dsInitThemeToggle();
        window.dsInitMobileSidebar();
        window.dsInitProfilePill();
        window.dsInitTOC();
        highlightActiveLinks();

        // Dropdown clicks
        document.addEventListener('click', (e) => {
            const group = e.target.closest('.tb-group');
            if (group) {
                const isOpen = group.classList.contains('open');
                document.querySelectorAll('.tb-group.open').forEach(g => g.classList.remove('open'));
                if (!isOpen) group.classList.add('open');
            } else {
                document.querySelectorAll('.tb-group.open').forEach(g => g.classList.remove('open'));
            }
        });

        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    /* ── Navigation Highlighting ─────────────────── */
    function highlightActiveLinks() {
        const path = window.location.pathname;
        document.querySelectorAll('.sb-link, .tb-link').forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;
            
            // Normalize paths for comparison
            const linkPath = new URL(href, window.location.href).pathname;
            if (path === linkPath || (path.replace(/\.html$/, '') === linkPath.replace(/\.html$/, ''))) {
                link.classList.add('active');
                // Open parent group if in dropdown
                const group = link.closest('.tb-group');
                if (group) group.classList.add('active-path');
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
