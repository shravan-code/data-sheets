(function() {
    const html  = document.documentElement;
    const body  = document.body;

    // Keep topbar logo behavior universal across pages,
    // even if individual page markup slightly differs.
    function normalizeSidebarLinks() {
        const sidebar = document.getElementById('ds-sidebar');
        if (!sidebar || sidebar.dataset.normalized) return;
        sidebar.dataset.normalized = 'true';

        const path = window.location.pathname.replace(/\\/g, '/');
        const parts = path.split('/').filter(Boolean);
        
        // Find "pages" in the path to determine depth from project root
        const pagesIdx = parts.indexOf('pages');
        let depth = 0;
        if (pagesIdx >= 0) {
            // If path is /pages/python.html -> parts=['pages','python.html'], pagesIdx=0, length=2, depth=1
            // If path is /pages/airflow/fundamentals.html -> parts=['pages','airflow','fundamentals.html'], pagesIdx=0, length=3, depth=2
            depth = parts.length - 1 - pagesIdx;
        } else if (parts.length > 0 && !path.endsWith('/') && !path.endsWith('index.html')) {
            // Probably in a subdirectory but not under "pages"
            depth = parts.length - 1;
        }

        let prefix = '';
        if (depth === 0) {
            // We are at root (index.html), links should point into pages/
            prefix = './pages/';
        } else if (depth === 1) {
            // We are in a main page (e.g., pages/python.html), links are sibling
            prefix = './';
        } else {
            // We are in a sub-page (e.g., pages/airflow/fundamentals.html), go up
            prefix = '../'.repeat(depth - 1);
        }

        sidebar.querySelectorAll('a').forEach(link => {
            const href = link.getAttribute('href');
            if (!href || href.startsWith('http') || href.startsWith('#') || href.startsWith('mailto:')) return;
            
            // The sidebar HTML contains links authored as if they were in pages/ folder, 
            // e.g. "./python.html" or "../python.html".
            // Clean it to get the base path relative to "pages/" directory.
            // Wait! The HTML files have `href="../python.html"` in subpages and `href="./python.html"` in main pages.
            // If we remove ALL leading `../` and `./`, we get `python.html` or `roadmaps/data-engineering.html`.
            let cleanHref = href.replace(/^(\.\.\/|\.\/)+/, '').replace(/^pages\//, '');
            
            // Special case: if it links to index.html at root
            if (cleanHref === 'index.html') {
                if (depth === 0) {
                    link.setAttribute('href', './index.html');
                } else {
                    link.setAttribute('href', '../'.repeat(depth) + 'index.html');
                }
                return;
            }

            // Re-apply correct relative prefix
            link.setAttribute('href', prefix + cleanHref);
        });
    }

    function removeSubpageSidebarTitles() {
        // Remove #guide-topics wrapper (used by Airflow, Databricks, etc.)
        const guideTopics = document.getElementById('guide-topics');
        if (guideTopics) guideTopics.remove();

        // Also remove hardcoded guide nav sections not inside #guide-topics
        // These are identified by the grey slate styling used for guide navs
        // (vs blue/emerald/orange/rose/violet for main categories)
        const sidebar = document.getElementById('ds-sidebar');
        if (!sidebar) return;

        const cats = sidebar.querySelectorAll('.sb-cat');
        cats.forEach(cat => {
            const nav = cat.nextElementSibling;
            if (!nav || nav.tagName.toLowerCase() !== 'nav') return;

            const links = nav.querySelectorAll('a.sb-link');
            if (links.length < 3) return;

            // Guide-specific navs use slate/grey colors — main categories use blue/emerald/orange/rose/violet
            const isGuideCat = 
                cat.classList.contains('bg-slate-50') ||
                cat.classList.contains('bg-slate-100') ||
                cat.classList.contains('bg-gray-50') ||
                cat.classList.contains('bg-gray-100');

            if (isGuideCat) {
                cat.remove();
                nav.remove();
            }
        });
    }


    function removeBottomBreadcrumbs() {
        const selectors = [
            '.nav-container', 
            '.bottom-nav', 
            'nav.mt-16.pt-8',
            '.pagination-nav'
        ];
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => el.remove());
        });
    }

    // Fix raw JSON objects displayed as text in example/info cards
    function fixRawJsonInCards() {
        // Only run on DE architecture pages
        const main = document.querySelector('main');
        if (!main) return;

        // Find all small text spans that contain raw JSON
        main.querySelectorAll('span.text-sm, span.text-xs, p.text-sm, p.text-xs, div.text-sm, div.text-xs').forEach(el => {
            const text = el.textContent.trim();
            if (!text.startsWith('{') && !text.startsWith('[')) return;
            if (!text.includes(':') || !text.includes('"')) return;

            // Don't process if it's already inside a code block or pre
            if (el.closest('pre') || el.closest('code')) return;

            try {
                // Try to extract the JSON-like start (it may be truncated with "...")
                let jsonStr = text.replace(/…$/, '').trim();
                
                // Try to complete truncated JSON
                if (!jsonStr.endsWith('}') && !jsonStr.endsWith(']')) {
                    // Remove trailing commas
                    jsonStr = jsonStr.replace(/,\s*$/, '');
                    
                    // Count open brackets
                    const openBraces = (jsonStr.match(/\{/g) || []).length;
                    const closeBraces = (jsonStr.match(/\}/g) || []).length;
                    const openBrackets = (jsonStr.match(/\[/g) || []).length;
                    const closeBrackets = (jsonStr.match(/\]/g) || []).length;
                    
                    // Add missing quotes if the last character is a string that wasn't closed
                    if ((jsonStr.match(/"/g) || []).length % 2 !== 0) {
                        jsonStr += '"';
                    }
                    
                    for (let i = 0; i < openBrackets - closeBrackets; i++) jsonStr += ']';
                    for (let i = 0; i < openBraces - closeBraces; i++) jsonStr += '}';
                }
                const parsed = JSON.parse(jsonStr);
                
                // Build a nice key-value list
                const container = document.createElement('div');
                container.className = 'space-y-1.5 mt-2';
                Object.entries(parsed).forEach(([k, v]) => {
                    const row = document.createElement('div');
                    row.className = 'flex items-start gap-2 bg-white dark:bg-slate-800/50 p-2 rounded border border-slate-100 dark:border-slate-700/50';
                    const key = document.createElement('span');
                    key.className = 'text-[10px] font-black uppercase tracking-widest text-slate-400 flex-shrink-0 pt-0.5 w-20';
                    key.textContent = k;
                    const val = document.createElement('span');
                    val.className = 'text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-mono';
                    val.textContent = Array.isArray(v) ? v.join(', ') : String(v);
                    if (text.endsWith('…') && typeof v === 'string' && val.textContent === String(v) && k === Object.keys(parsed).pop()) {
                         val.textContent += '…';
                    }
                    row.appendChild(key);
                    row.appendChild(val);
                    container.appendChild(row);
                });
                
                // If we succeeded and it has keys, replace the element
                if (Object.keys(parsed).length > 0) {
                    el.replaceWith(container);
                }
            } catch (e) {
                // Not valid JSON — leave as-is but style it as a code block
                const pre = document.createElement('pre');
                pre.className = 'mt-2 p-3 bg-slate-900 text-slate-100 rounded-lg text-xs font-mono whitespace-pre-wrap break-all border border-slate-700 shadow-sm leading-relaxed';
                pre.textContent = text;
                el.replaceWith(pre);
            }
        });
    }

    // Fix raw code snippets (SQL, Cron, Python) in cards
    function fixCodeSnippetsInCards() {
        const main = document.querySelector('main');
        if (!main) return;

        const codePatterns = [
            /SELECT\s+.*?\s+FROM/i,
            /0\s+\d+\s+\*\s+\*\s+\*/, // Cron
            /INSERT\s+INTO/i,
            /UPDATE\s+.*?\s+SET/i,
            /import\s+[\w\.]+/,
            /def\s+\w+\(.*\):/,
            /spark\.(read|write|sql|conf|table)/i,
            /df\.(show|select|filter|groupBy|withColumn|write|read)/i,
            /dbutils\.(fs|secrets|notebook|widgets)/i,
            /logger\.(info|error|warn|debug)/i,
            /CREATE\s+(TABLE|VIEW|DATABASE)/i
        ];

        main.querySelectorAll('span.text-sm, span.text-xs, p.text-sm, p.text-xs, div.text-sm, div.text-xs').forEach(el => {
            if (el.closest('pre') || el.closest('code') || el.querySelector('pre') || el.querySelector('code')) return;
            
            const text = el.textContent.trim();
            if (codePatterns.some(p => p.test(text))) {
                const pre = document.createElement('pre');
                pre.className = 'mt-2 p-3 bg-slate-900 text-slate-100 rounded-xl text-xs font-mono whitespace-pre-wrap break-all border border-slate-700/50 shadow-inner leading-relaxed';
                pre.textContent = text;
                el.replaceWith(pre);
            }
        });
    }

    // Fix typography and code block styling on DE Architecture pages
    function fixDeArchitectureStyling() {
        const main = document.querySelector('main');
        if (!main) return;
        
        // Only apply if we're on a DE architectures page
        if (!window.location.pathname.includes('/de-architectures/')) return;

        const style = document.createElement('style');
        style.textContent = `
            /* Fix overly tight tracking on large headers with Outfit font */
            h1.tracking-tighter, h2.tracking-tighter, h3.tracking-tighter, 
            .tracking-tighter, h1.tracking-tight, h2.tracking-tight, h3.tracking-tight,
            .tracking-tight {
                letter-spacing: normal !important;
            }
            
            /* Enhance code block design */
            pre[class*="language-"] {
                border-radius: 0.75rem !important;
                background: #0f172a !important; /* slate-900 */
                border: 1px solid #1e293b !important; /* slate-800 */
                margin: 1.5rem 0 !important;
                padding: 1.25rem !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
            }
            code[class*="language-"], pre[class*="language-"] {
                color: #e2e8f0 !important; /* slate-200 */
                text-shadow: none !important;
                font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace !important;
                font-size: 0.875rem !important;
                line-height: 1.6 !important;
            }
            
            /* Add subtle border and background to inline code */
            :not(pre) > code[class*="language-"], p code, li code {
                background: #f1f5f9 !important; /* slate-100 */
                color: #0f172a !important; /* slate-900 */
                padding: 0.2em 0.4em !important;
                border-radius: 0.25rem !important;
                border: 1px solid #e2e8f0 !important; /* slate-200 */
                font-size: 0.85em !important;
                white-space: normal !important;
            }
            
            /* Card alignment fixes */
            .grid > div {
                display: flex;
                flex-direction: column;
            }
            .grid > div > div:last-child {
                margin-top: auto;
            }
        `;
        document.head.appendChild(style);
    }

    normalizeSidebarLinks();
    removeSubpageSidebarTitles();
    removeBottomBreadcrumbs();
    fixRawJsonInCards();
    fixDeArchitectureStyling();

    // Also run on DOMContentLoaded to catch any deferred content
    document.addEventListener('DOMContentLoaded', () => {
        removeSubpageSidebarTitles();
        normalizeSidebarLinks();
        fixRawJsonInCards();
        fixDeArchitectureStyling();
    });





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
                    const targetPosition = target.getBoundingClientRect().top + window.scrollY;
                    const offset = window.innerHeight / 2;
                    window.scrollTo({
                        top: targetPosition - offset,
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

    fixRawJsonInCards();
    fixCodeSnippetsInCards();
    normalizeSidebarLinks();
    splitCombinedCodeExamples();
    preserveScrollOnBackNavigation();
    initProfileHoverLabel();

    // Initial Icon Load
    if (typeof lucide !== 'undefined') lucide.createIcons();
})();
