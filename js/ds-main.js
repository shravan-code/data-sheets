(function() {
    const html  = document.documentElement;
    const body  = document.body;

    /* ── Theme ──────────────────────────────────── */
    // Dark mode removed as per user request. Defaulting to light theme.
    html.classList.remove('dark');
    localStorage.setItem('ds-theme', 'light');
    
    // Sync Prism themes to light only
    const l = document.getElementById('prism-theme-light');
    const d = document.getElementById('prism-theme-dark');
    if(l && d) {
        l.disabled = false;
        d.disabled = true;
    }

    /* ── Sidebar state ───────────────────────────── */
    const sidebar  = document.getElementById('ds-sidebar');
    const overlay  = document.getElementById('sidebar-overlay');
    const togBtn   = document.getElementById('sidebar-toggle');

    // Default: expanded on desktop, closed on mobile
    const isDesktop = () => window.innerWidth >= 1024;
    const stored = localStorage.getItem('ds-sidebar');
    let sidebarOpen = (stored === null) ? isDesktop() : (stored === 'open');

    // MOBILE UX: Always start closed on mobile regardless of persisted state
    if (!isDesktop()) sidebarOpen = false;


    /* ── Active Link Highlighting ────────────────── */
    /* ── Active Link Highlighting ────────────────── */
    function highlightActive() {
        const currentPath = window.location.pathname;
        const links = document.querySelectorAll('.sb-link');
        let activeHeaders = new Set();

        links.forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;

            // Resolve relative href to absolute path for comparison
            const linkPath = new URL(href, window.location.href).pathname;
            
            // Normalize paths for comparison (handle .html extension)
            const normLink = linkPath.replace(/\.html$/, '');
            const normCurr = currentPath.replace(/\.html$/, '');
            
            const isExact = (normCurr === normLink);
            const isAncestor = !isExact && normCurr.startsWith(normLink + '/');
            
            if (isExact || isAncestor) {
                if (isExact) {
                    link.classList.add('active');
                    
                    // Position active link
                    const positionActiveLink = () => {
                        const sidebar = document.getElementById('ds-sidebar');
                        if (sidebar) {
                            sidebar.scrollTo({
                                top: link.offsetTop - 60, // Slightly more padding
                                behavior: 'smooth'
                            });
                        }
                    };
                    positionActiveLink();
                    setTimeout(positionActiveLink, 300);
                } else {
                    link.classList.add('ancestor-active');
                }

                // Expand all parent categories
                let parent = link.parentElement;
                while (parent && parent !== sidebar) {
                    if (parent.tagName.toLowerCase() === 'nav') {
                        const header = parent.previousElementSibling;
                        if (header && header.classList.contains('sb-cat')) {
                            activeHeaders.add(header);
                        }
                    }
                    parent = parent.parentElement;
                }
            } else {
                link.classList.remove('active');
                link.classList.remove('ancestor-active');
            }
        });

        // Expand sections
        if (activeHeaders.size > 0) {
            document.querySelectorAll('.sb-cat').forEach(cat => {
                if (activeHeaders.has(cat)) {
                    cat.classList.remove('collapsed');
                }
                // We DON'T collapse others here to prevent the "main section is closing" issue
                // when navigating within sub-sections or clicking around.
            });
        }
    }
    highlightActive();

    // Close sidebar on mobile ONLY when a sub-link is clicked (not on main sections/categories)
    document.querySelectorAll('.sb-link').forEach(link => {
        link.addEventListener('click', () => {
            if (!isDesktop()) {
                sidebarOpen = false;
                applyState(true);
            }
        });
    });

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

    /* ── Collapsible Sidebar Sections ─────────────── */
    function initCollapsibleSections() {
        const categories = document.querySelectorAll('.sb-cat');
        categories.forEach(cat => {
            // Add chevron icon if not present
            if (!cat.querySelector('.chevron')) {
                const chevron = document.createElement('i');
                chevron.setAttribute('data-lucide', 'chevron-down');
                chevron.classList.add('chevron', 'w-3', 'h-3', 'ml-auto', 'transition-transform', 'duration-300');
                cat.appendChild(chevron);
            }

            cat.addEventListener('click', () => {
                const isOpening = cat.classList.contains('collapsed');

                if (isOpening) {
                    // Collapse all others (Accordion behavior)
                    categories.forEach(other => {
                        if (other !== cat) {
                            other.classList.add('collapsed');
                        }
                    });
                }

                cat.classList.toggle('collapsed');
                
                // Refresh icons
                if (typeof lucide !== 'undefined') lucide.createIcons();
            });

        });
    }
    initCollapsibleSections();

    // On resize: ensure sidebar state is correct
    window.addEventListener('resize', () => {
        if (isDesktop()) {
            if (!sidebarOpen) {
                sidebarOpen = true;
                applyState(false);
            }
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
        const tocWrapper = document.querySelector('.toc-container');
        const content = document.querySelector('.prose');
        if (!tocContainer || !content) return;

        const headers = content.querySelectorAll('h2, h3');
        if (headers.length === 0) {
            if (tocWrapper) tocWrapper.style.display = 'none';
            return;
        }

        if (tocWrapper) {
            if (window.innerWidth >= 1280) tocWrapper.style.display = 'block';
            else tocWrapper.style.display = 'none';
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

    // Initial Icon Load
    if (typeof lucide !== 'undefined') lucide.createIcons();
})();
