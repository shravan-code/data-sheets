(function() {
    const html  = document.documentElement;
    const body  = document.body;

    /* ── Theme ──────────────────────────────────── */
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = html.classList.toggle('dark');
            localStorage.setItem('ds-theme', isDark ? 'dark' : 'light');
            
            // Sync Prism themes
            const l = document.getElementById('prism-theme-light');
            const d = document.getElementById('prism-theme-dark');
            if(l && d) {
                l.disabled = isDark;
                d.disabled = !isDark;
            }
        });
    }

    /* ── Sidebar state ───────────────────────────── */
    const sidebar  = document.getElementById('ds-sidebar');
    const overlay  = document.getElementById('sidebar-overlay');
    const togBtn   = document.getElementById('sidebar-toggle');

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
        } else {
            sidebar.classList.add('sidebar-hidden');
            sidebar.classList.remove('sidebar-visible');
            body.classList.remove('sidebar-open');
            if (overlay) { overlay.style.opacity = '0'; overlay.style.pointerEvents = 'none'; }
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

    /* ── Table of Contents ───────────────────────── */
    function initTOC() {
        const tocContainer = document.querySelector('.toc-list');
        const content = document.querySelector('.prose');
        if (!tocContainer || !content) return;

        const headers = content.querySelectorAll('h2, h3');
        if (headers.length === 0) {
            const tocWrapper = document.querySelector('.toc-container');
            if (tocWrapper) tocWrapper.style.display = 'none';
            return;
        }

        headers.forEach((header, index) => {
            if (!header.id) {
                header.id = header.textContent.toLowerCase().trim()
                    .replace(/\s+/g, '-')
                    .replace(/[^\w-]/g, '') + '-' + index;
            }

            const link = document.createElement('a');
            link.href = '#' + header.id;
            link.textContent = header.textContent;
            link.className = 'toc-link';
            if (header.tagName.toLowerCase() === 'h3') link.classList.add('toc-h3');

            const li = document.createElement('li');
            li.appendChild(link);
            tocContainer.appendChild(li);

            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.getElementById(header.id);
                if (target) {
                    const navHeight = 100;
                    window.scrollTo({
                        top: target.getBoundingClientRect().top + window.pageYOffset - navHeight,
                        behavior: 'smooth'
                    });
                    history.pushState(null, null, '#' + header.id);
                }
            });
        });

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    document.querySelectorAll('.toc-link').forEach(l => {
                        l.classList.toggle('active', l.getAttribute('href') === '#' + entry.target.id);
                    });
                }
            });
        }, { rootMargin: '-100px 0px -70% 0px' });

        headers.forEach(h => observer.observe(h));
    }
    initTOC();

    /* ── Code Block Enhancements ─────────────── */
    function enhanceCodeBlocks() {
        const blocks = document.querySelectorAll('pre[class*="language-"]');
        blocks.forEach(block => {
            if (block.querySelector('.ds-code-header')) return; // Already enhanced

            // 1. Create Header
            const header = document.createElement('div');
            header.className = 'ds-code-header flex items-center justify-between px-4 py-2 bg-slate-50/50 dark:bg-slate-800/30 border-b border-slate-200/60 dark:border-slate-700/40 rounded-t-xl absolute top-0 left-0 right-0 z-10';
            
            // 2. Language Badge
            const langMatch = block.className.match(/language-([a-z0-9]+)/i);
            const lang = langMatch ? langMatch[1] : 'code';
            const badge = document.createElement('span');
            badge.className = 'text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500';
            badge.innerText = lang === 'bash' ? 'terminal' : lang;

            // 3. Copy Button
            const copyBtn = document.createElement('button');
            copyBtn.className = 'flex items-center gap-1.5 text-slate-400 hover:text-blue-500 dark:text-slate-500 dark:hover:text-blue-400 transition-colors';
            copyBtn.innerHTML = `
                <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                <span class="text-[10px] font-bold uppercase tracking-wider">Copy</span>
            `;

            copyBtn.addEventListener('click', async () => {
                const code = block.querySelector('code').innerText;
                await navigator.clipboard.writeText(code);
                
                const originalHTML = copyBtn.innerHTML;
                copyBtn.innerHTML = `
                    <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-500"></i>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-500">Copied</span>
                `;
                setTimeout(() => {
                    copyBtn.innerHTML = originalHTML;
                    lucide.createIcons();
                }, 2000);
            });

            header.appendChild(badge);
            header.appendChild(copyBtn);
            
            // 4. Adjust block styling to accommodate header
            block.style.paddingTop = '3rem';
            block.prepend(header);
        });
        
        // Refresh icons
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    // Run after a small delay to ensure Prism has finished
    window.addEventListener('load', () => {
        setTimeout(enhanceCodeBlocks, 500);
    });
})();
