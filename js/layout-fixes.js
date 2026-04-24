(function () {
    const ICON_MAP = {
        'terminal-square': 'square-terminal',
        'cloud-cog': 'cloud',
        'container': 'box',
        'git-branch-plus': 'waypoints'
    };

    const LEARN_CARD_META = {
        Python: ['code-2', 'blue'],
        SQL: ['database', 'blue'],
        Bash: ['terminal', 'blue'],
        PowerShell: ['square-terminal', 'blue'],
        'DE Fundamentals': ['layers', 'emerald'],
        'DSA for DE': ['waypoints', 'emerald'],
        Spark: ['zap', 'orange'],
        Flink: ['activity', 'orange'],
        Kafka: ['radio', 'orange'],
        dbt: ['blocks', 'orange'],
        Pandas: ['table-2', 'orange'],
        NumPy: ['hash', 'orange'],
        Airflow: ['wind', 'orange'],
        AWS: ['cloud', 'cyan'],
        GCP: ['cloud-sun', 'cyan'],
        Azure: ['cloud', 'cyan'],
        Snowflake: ['snowflake', 'cyan'],
        Databricks: ['box', 'cyan'],
        Docker: ['box', 'violet'],
        Kubernetes: ['network', 'violet'],
        Terraform: ['sliders-horizontal', 'violet'],
        GitHub: ['git-branch', 'violet'],
        'System Design': ['layout-dashboard', 'rose'],
        'Pipeline Design': ['workflow', 'rose'],
        'DE Architectures': ['cpu', 'rose']
    };

    function ensureStylesheet() {
        if (document.querySelector('link[href*="layout-fixes.css"]')) return;

        const current = document.currentScript;
        if (!current || !current.src) return;

        const href = current.src.replace(/\/js\/layout-fixes\.js(?:\?.*)?$/, '/css/layout-fixes.css');
        if (href === current.src) return;

        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        document.head.appendChild(link);
    }

    function ensureLucide() {
        if (typeof window.lucide !== 'undefined' || document.querySelector('script[src*="unpkg.com/lucide"]')) {
            return Promise.resolve();
        }

        return new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = 'https://unpkg.com/lucide@latest';
            script.onload = resolve;
            script.onerror = resolve;
            document.head.appendChild(script);
        });
    }

    function dedupeById(id) {
        const nodes = document.querySelectorAll(`#${id}`);
        nodes.forEach((node, index) => {
            if (index > 0) node.remove();
        });
    }

    function normalizePageTitle(raw) {
        const clean = (raw || document.title || 'Data Sheets').replace(/\s+/g, ' ').trim();
        const parts = clean.split(/\s+[\u2013\u2014-]\s+/).filter(Boolean);
        let title = parts[0] || 'Data Sheets';

        if (title === 'Data Sheets' && parts[1]) {
            title = parts[1];
        }

        title = title.replace(/^\d+\.\s*/, '').trim();
        return title === 'Data Sheets' ? 'Home' : title;
    }

    function replaceInvalidIcons() {
        document.querySelectorAll('[data-lucide]').forEach((node) => {
            const icon = node.getAttribute('data-lucide');
            if (ICON_MAP[icon]) {
                node.setAttribute('data-lucide', ICON_MAP[icon]);
            }
        });
    }

    function rebuildThemeToggle() {
        const button = document.getElementById('theme-toggle');
        if (!button) return;

        button.innerHTML = [
            '<i data-lucide="sun" class="theme-icon-light hidden dark:block"></i>',
            '<i data-lucide="moon" class="theme-icon-dark block dark:hidden"></i>'
        ].join('');
        
        button.setAttribute('aria-label', 'Toggle theme');
        button.setAttribute('aria-pressed', document.documentElement.classList.contains('dark') ? 'true' : 'false');
    }

    function handleThemeToggle() {
        let button = document.getElementById('theme-toggle');
        if (!button || button.dataset.dsHandleInit) return;

        // Replace button with clone to clear existing listeners from HTML script
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        button = newButton;
        button.dataset.dsHandleInit = 'true';
        
        button.addEventListener('click', () => {
            const html = document.documentElement;
            const isDark = html.classList.toggle('dark');
            localStorage.setItem('ds-theme', isDark ? 'dark' : 'light');
            
            button.setAttribute('aria-pressed', isDark ? 'true' : 'false');
            
            if (typeof lucide !== 'undefined') {
                requestAnimationFrame(() => lucide.createIcons());
            }
        });
    }

    function rebuildSidebarToggle() {
        const button = document.getElementById('sidebar-toggle');
        if (!button) return;

        button.innerHTML = '<i id="sb-toggle-glyph" data-lucide="menu"></i>';
    }

    function syncSidebarToggle() {
        const glyph = document.getElementById('sb-toggle-glyph');
        const sidebar = document.getElementById('ds-sidebar');
        const button = document.getElementById('sidebar-toggle');
        if (!glyph || !sidebar || !button) return;

        const open = sidebar.classList.contains('sidebar-visible');
        glyph.setAttribute('data-lucide', open ? 'x' : 'menu');
        button.setAttribute('aria-expanded', open ? 'true' : 'false');
        button.setAttribute('title', open ? 'Close sidebar' : 'Open sidebar');
    }

    function enhanceTopbar() {
        const navInner = document.querySelector('#ds-nav > div');
        const themeToggle = document.getElementById('theme-toggle');
        const toggleButton = document.getElementById('sidebar-toggle');
        if (!navInner || !themeToggle || !toggleButton || navInner.querySelector('.ds-topbar-center')) return;

        navInner.classList.add('ds-topbar-shell');

        const leftGroup = toggleButton.parentElement;
        if (leftGroup) {
            leftGroup.classList.add('ds-topbar-left');
        }

        const logoLink = navInner.querySelector('a[href]');
        if (!logoLink) return;

        const brandText = logoLink.querySelector('span');
        if (brandText) {
            brandText.classList.add('ds-topbar-brand-text');
        }

        logoLink.classList.add('ds-topbar-brand', 'no-underline');

        const pageTitle = document.createElement('span');
        pageTitle.className = 'ds-page-title';
        pageTitle.textContent = normalizePageTitle();
        logoLink.appendChild(pageTitle);

        const center = document.createElement('div');
        center.className = 'ds-topbar-center';
        center.appendChild(logoLink);

        if (leftGroup) {
            leftGroup.querySelectorAll('a[href]').forEach((anchor) => anchor.remove());
        }

        navInner.insertBefore(center, themeToggle);
    }

    function tagPage() {
        const path = window.location.pathname.replace(/\\/g, '/');
        if (path.endsWith('/learn.html') || path.endsWith('pages/learn.html')) {
            document.body.classList.add('ds-learn-home');
        }
        if (path.endsWith('/index.html') || path.endsWith('/') || path.endsWith('data-sheets') || path.endsWith('data-sheets/')) {
            document.body.classList.add('ds-is-home');
            localStorage.setItem('ds-sidebar', 'closed');
        }
    }

    function forceHomeSidebarClosed() {
        if (!document.body.classList.contains('ds-is-home')) return;
        const sidebar = document.getElementById('ds-sidebar');
        const body = document.body;
        if (sidebar) {
            sidebar.classList.add('sidebar-hidden');
            sidebar.classList.remove('sidebar-visible');
            body.classList.remove('sidebar-open');
            sessionStorage.setItem('ds-sidebar-scroll', '0');
            sidebar.scrollTop = 0;
        }
        const glyph = document.getElementById('sb-toggle-glyph');
        if (glyph) {
            glyph.setAttribute('data-lucide', 'menu');
        }
    }

    function restyleLearnHome() {
        if (!document.body.classList.contains('ds-learn-home')) return;

        const hero = document.querySelector('main[data-sb-padded="1"] > div.mb-12');
        if (hero && !hero.classList.contains('ds-learn-hero')) {
            hero.classList.add('ds-learn-hero');
        }

        document.querySelectorAll('body.ds-learn-home section').forEach((section) => {
            const heading = section.querySelector('h2');
            if (heading) {
                section.classList.add('ds-learn-section');
            }
        });

        document.querySelectorAll('body.ds-learn-home .topic-card').forEach((card) => {
            if (card.classList.contains('ds-topic-card')) return;

            const titleEl = card.querySelector('h3');
            const descEl = card.querySelector('p');
            const ctaEl = card.querySelector('span:last-child');
            if (!titleEl || !descEl || !ctaEl) return;

            const title = titleEl.textContent.trim();
            const meta = LEARN_CARD_META[title] || ['book-open', 'blue'];

            card.classList.add('ds-topic-card');
            card.classList.add(`ds-accent-${meta[1]}`);
            card.innerHTML = [
                '<div class="ds-topic-card-row">',
                `  <div class="ds-topic-card-icon"><i data-lucide="${meta[0]}"></i></div>`,
                '  <div class="ds-topic-card-copy"></div>',
                '</div>'
            ].join('');

            const copy = card.querySelector('.ds-topic-card-copy');
            titleEl.className = 'ds-topic-card-title';
            descEl.className = 'ds-topic-card-desc';
            copy.append(titleEl, descEl);
        });
    }

    function preserveSidebarScroll() {
        const sidebar = document.getElementById('ds-sidebar');
        if (!sidebar) return;

        document.querySelectorAll('.sb-link, .sb-section').forEach((link) => {
            link.addEventListener('click', () => {
                const scrollY = sidebar.scrollTop;
                sessionStorage.setItem('ds-sidebar-scroll', scrollY);
            });
        });

        const savedScroll = sessionStorage.getItem('ds-sidebar-scroll');
        if (savedScroll !== null) {
            setTimeout(() => {
                sidebar.scrollTop = parseInt(savedScroll, 10);
            }, 50);
        }
    }

    function addRevealAnimations() {
        const targets = [
            ...document.querySelectorAll('main > div, main > section, .topic-card, .prose h2, .prose h3, .prose p, .prose ul, .prose pre, .prose blockquote')
        ].filter((node, index, arr) => node && arr.indexOf(node) === index);

        targets.forEach((node, index) => {
            node.classList.add('ds-reveal');
            node.style.setProperty('--ds-delay', `${Math.min(index * 35, 280)}ms`);
        });

        if (!('IntersectionObserver' in window)) {
            targets.forEach((node) => node.classList.add('is-visible'));
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

        targets.forEach((node) => observer.observe(node));
    }

    function rerenderLucide() {
        if (typeof lucide === 'undefined') return;
        lucide.createIcons();
    }

    function autoCloseSidebarOnMobile() {
        const sidebar = document.getElementById('ds-sidebar');
        if (!sidebar) return;

        const links = sidebar.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 1024) {
                    sidebar.classList.add('sidebar-hidden');
                    sidebar.classList.remove('sidebar-visible');
                    document.body.classList.remove('sidebar-open');
                    
                    const overlay = document.getElementById('sidebar-overlay');
                    if (overlay) {
                        overlay.style.opacity = '0';
                        overlay.style.pointerEvents = 'none';
                    }
                    
                    localStorage.setItem('ds-sidebar', 'closed');
                    syncSidebarToggle();
                    rerenderLucide();
                }
            });
        });
    }

    async function init() {
        ensureStylesheet();
        await ensureLucide();
        dedupeById('ds-sidebar');
        dedupeById('sidebar-overlay');
        dedupeById('scroll-top');
        replaceInvalidIcons();
        rebuildThemeToggle();
        rebuildSidebarToggle();
        enhanceTopbar();
        tagPage();
        restyleLearnHome();
        forceHomeSidebarClosed();
        syncSidebarToggle();
        rerenderLucide();
        // addRevealAnimations();
        preserveSidebarScroll();
        autoCloseSidebarOnMobile();

        const sidebar = document.getElementById('ds-sidebar');
        if (sidebar) {
            const observer = new MutationObserver(() => {
                syncSidebarToggle();
                replaceInvalidIcons();
                rerenderLucide();
            });

            observer.observe(sidebar, { attributes: true, attributeFilter: ['class'] });
        }

        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            handleThemeToggle();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
