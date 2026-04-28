(function() {
    const html  = document.documentElement;
    const body  = document.body;

    // Keep topbar logo behavior universal across pages,
    // even if individual page markup slightly differs.
    function ensureUniversalTopbarBrand() {
        const nav = document.getElementById('ds-nav');
        if (!nav) return;

        const logoLink = nav.querySelector('a[href]');
        if (!logoLink) return;

        const titleRow = logoLink.querySelector('span[style*="Outfit"], span[class*="tracking-tighter"]');
        if (!titleRow) return;

        let dataSpan = titleRow.querySelector('span.font-light');
        let cakeSpan = Array.from(titleRow.querySelectorAll('span'))
            .find((span) => /cake/i.test((span.textContent || '').trim()));

        // If page markup drifted, reconstruct the expected two-part logo text.
        if (!cakeSpan) {
            titleRow.textContent = '';

            dataSpan = document.createElement('span');
            dataSpan.className = 'font-light text-slate-500';
            dataSpan.textContent = 'Data';

            cakeSpan = document.createElement('span');
            cakeSpan.className = 'font-black bg-gradient-to-br from-indigo-600 via-blue-600 to-emerald-500 bg-clip-text text-transparent ml-1.5 inline-block -rotate-3 origin-bottom-left';
            cakeSpan.textContent = 'Cake';

            titleRow.appendChild(dataSpan);
            titleRow.appendChild(cakeSpan);
        }

        cakeSpan.classList.add('ds-logo-cake');
        cakeSpan.setAttribute('data-text', (cakeSpan.textContent || 'Cake').trim() || 'Cake');
    }

    ensureUniversalTopbarBrand();

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

    /* ── Profile Button Expand Label ─────────────── */
    function initProfileHoverLabel() {
        const profileBtn = document.getElementById('profile-btn');
        if (!profileBtn || profileBtn.dataset.profileLabelInit === '1') return;

        profileBtn.dataset.profileLabelInit = '1';
        profileBtn.classList.add('profile-pill');
        profileBtn.setAttribute('aria-label', 'Shravan Kumar Tela profile');

        if (!profileBtn.querySelector('.profile-pill-text')) {
            const label = document.createElement('span');
            label.className = 'profile-pill-text';
            label.textContent = 'Shravan Kumar Tela';
            profileBtn.appendChild(label);
        }
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

    /* ── Split Combined Concept Code Blocks ─────── */
    function splitCombinedCodeExamples() {
        const isConceptHeader = (line, lang) => {
            const trimmed = line.trim();
            if (!trimmed) return false;

            const isComment =
                (lang === 'sql' && trimmed.startsWith('--')) ||
                (lang !== 'sql' && trimmed.startsWith('#'));
            if (!isComment) return false;

            const text = lang === 'sql'
                ? trimmed.replace(/^--\s?/, '')
                : trimmed.replace(/^#\s?/, '');
            if (!text || /^output[:\s]/i.test(text)) return false;

            // Treat only "heading-like" comments as split boundaries.
            return /:|example|approach|concept|pattern|method|technique|case|vs|complexity|operation|workflow/i.test(text);
        };

        const parseSections = (code, lang) => {
            const lines = code.replace(/\r\n/g, '\n').split('\n');
            const markers = [];

            for (let i = 0; i < lines.length; i++) {
                if (isConceptHeader(lines[i], lang)) {
                    const prev = i > 0 ? lines[i - 1].trim() : '';
                    if (i === 0 || prev === '') {
                        markers.push(i);
                    }
                }
            }

            if (markers.length < 2) return null;

            const sections = [];
            for (let m = 0; m < markers.length; m++) {
                const start = markers[m];
                const end = m + 1 < markers.length ? markers[m + 1] : lines.length;
                const chunkLines = lines.slice(start, end);
                const titleLine = chunkLines[0].trim();
                const title = lang === 'sql'
                    ? titleLine.replace(/^--\s?/, '').trim()
                    : titleLine.replace(/^#\s?/, '').trim();
                const body = chunkLines.join('\n').trimEnd();
                if (body) {
                    sections.push({ title, body });
                }
            }

            return sections.length >= 2 ? sections : null;
        };

        document.querySelectorAll('pre > code[class*="language-"]').forEach((codeEl) => {
            const pre = codeEl.parentElement;
            if (!pre || pre.dataset.splitDone === '1') return;

            const languageMatch = codeEl.className.match(/language-([a-z0-9]+)/i);
            const lang = languageMatch ? languageMatch[1].toLowerCase() : '';
            if (!['python', 'sql', 'bash', 'powershell'].includes(lang)) return;

            const sections = parseSections(codeEl.textContent || '', lang);
            if (!sections) return;

            const wrapper = document.createElement('div');
            wrapper.className = 'concept-block-group not-prose my-8';

            sections.forEach((section) => {
                const block = document.createElement('section');
                block.className = 'concept-block-item mb-6';

                const title = document.createElement('h4');
                title.className = 'concept-block-title';
                title.textContent = section.title;

                const newPre = document.createElement('pre');
                const newCode = document.createElement('code');
                newCode.className = codeEl.className;
                newCode.textContent = section.body;
                newPre.appendChild(newCode);

                block.appendChild(title);
                block.appendChild(newPre);
                wrapper.appendChild(block);
            });

            pre.replaceWith(wrapper);
            pre.dataset.splitDone = '1';
        });
    }

    /* ── Preserve Main Page Scroll On Browser Back ─ */
    function preserveScrollOnBackNavigation() {
        const keyPrefix = 'ds-scroll-pos:';
        const restoreNextPrefix = 'ds-restore-next:';
        const selectedLinkPrefix = 'ds-selected-link:';
        const currentPath = window.location.pathname;
        const currentKey = keyPrefix + currentPath;

        // Save current page scroll when navigating away via links.
        document.querySelectorAll('a[href]').forEach((link) => {
            link.addEventListener('click', () => {
                const href = link.getAttribute('href');
                if (!href || href.startsWith('#') || link.target === '_blank') return;

                try {
                    const target = new URL(link.href, window.location.href);
                    if (target.origin !== window.location.origin) return;
                    if (target.pathname === currentPath && !target.hash) return;

                    sessionStorage.setItem(currentKey, String(window.scrollY || window.pageYOffset || 0));
                    sessionStorage.setItem(selectedLinkPrefix + currentPath, link.href);

                    // If this is a "Back to ..." link, request restore on destination too.
                    const text = (link.textContent || '').trim().toLowerCase();
                    if (text.startsWith('back to')) {
                        sessionStorage.setItem(restoreNextPrefix + target.pathname, '1');
                    }
                } catch (e) {
                    // Ignore invalid URLs.
                }
            });
        });

        const restoreScroll = () => {
            const saved = sessionStorage.getItem(currentKey);
            if (!saved) return;

            const navigation = performance.getEntriesByType('navigation')[0];
            const isBackForward = navigation && navigation.type === 'back_forward';
            const isMarkedRestore = sessionStorage.getItem(restoreNextPrefix + currentPath) === '1';
            if (!isBackForward && !isMarkedRestore) return;

            const top = parseInt(saved, 10);
            if (Number.isNaN(top)) return;

            if (isMarkedRestore) {
                sessionStorage.removeItem(restoreNextPrefix + currentPath);
            }

            requestAnimationFrame(() => {
                window.scrollTo(0, top);
            });
        };

        const restoreSelectedLink = () => {
            const savedHref = sessionStorage.getItem(selectedLinkPrefix + currentPath);
            if (!savedHref) return;

            let matched = null;
            document.querySelectorAll('a[href]').forEach((a) => {
                const href = a.href;
                if (href === savedHref && !matched) {
                    matched = a;
                }
            });
            if (!matched) return;

            document.querySelectorAll('.ds-last-selected-link').forEach((el) => {
                el.classList.remove('ds-last-selected-link');
            });
            matched.classList.add('ds-last-selected-link');
        };

        window.addEventListener('pageshow', restoreScroll);
        restoreScroll();
        restoreSelectedLink();
    }

    /* ── Bottom Breadcrumbs For Subpages ─────────── */
    function addBottomBreadcrumb() {
        const path = window.location.pathname.replace(/\\/g, '/');
        if (!path.includes('/pages/')) return;

        // Exclude index-level pages that have no valid parent to link to
        const noBreadcrumbPages = ['/pages/learn/de-architectures.html'];
        if (noBreadcrumbPages.some(p => path.endsWith(p))) return;

        const parts = path.split('/').filter(Boolean);
        const pagesIdx = parts.indexOf('pages');
        if (pagesIdx < 0 || pagesIdx + 2 >= parts.length) return; // not deep enough to be a subpage

        const main = document.querySelector('main');
        const navContainer = document.querySelector('.nav-container');
        if (!main || main.querySelector('.ds-bottom-breadcrumb')) return;

        const labelize = (segment) => segment
            .replace(/\.html$/, '')
            .replace(/---/g, ' / ')
            .replace(/--/g, ' - ')
            .replace(/-/g, ' ')
            .replace(/\b\w/g, (c) => c.toUpperCase());

        const breadcrumb = document.createElement('nav');
        breadcrumb.className = 'ds-bottom-breadcrumb not-prose';
        breadcrumb.setAttribute('aria-label', 'Breadcrumb');

        const ordered = document.createElement('ol');
        ordered.className = 'ds-breadcrumb-list';

        const trail = parts.slice(pagesIdx + 1); // after "pages"
        trail.forEach((segment, index) => {
            const li = document.createElement('li');
            const isLast = index === trail.length - 1;

            if (!isLast) {
                const hrefPath = '/' + parts.slice(0, pagesIdx + 2 + index).join('/') + '.html';
                const anchor = document.createElement('a');
                anchor.href = hrefPath.replace('/learn/learn.html', '/learn.html');
                anchor.textContent = labelize(segment);
                li.appendChild(anchor);
            } else {
                const span = document.createElement('span');
                span.textContent = labelize(segment).replace(/^\d+\.\s*/, '');
                span.setAttribute('aria-current', 'page');
                li.appendChild(span);
            }

            ordered.appendChild(li);
        });

        breadcrumb.appendChild(ordered);
        if (navContainer) main.insertBefore(breadcrumb, navContainer);
        else main.appendChild(breadcrumb);
    }

    splitCombinedCodeExamples();
    preserveScrollOnBackNavigation();
    addBottomBreadcrumb();
    initProfileHoverLabel();

    // Initial Icon Load
    if (typeof lucide !== 'undefined') lucide.createIcons();
})();
