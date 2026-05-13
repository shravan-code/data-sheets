(function() {
    const html  = document.documentElement;
    const body  = document.body;

    // Detect path depth to fix links
    const path = window.location.pathname.replace(/\\/g, '/');
    const parts = path.split('/').filter(Boolean);
    const pagesIdx = parts.indexOf('pages');
    let depth = 0;
    if (pagesIdx >= 0) {
        depth = parts.length - 1 - pagesIdx;
    } else if (parts.length > 0 && !path.endsWith('/') && !path.endsWith('index.html')) {
        depth = parts.length - 1;
    }
    
    // We treat 'pages' index as depth 1 relative to root, root as depth 0.
    // If we are at root, depth is 0. If we are in pages/python.html, depth is 1. If we are in pages/learn/python.html, depth is 2.
    // Let's refine depth calculation:
    let prefix = '';
    let isRoot = false;
    if (path.endsWith('index.html') || path === '/' || path.endsWith('data-sheets/')) {
        prefix = './pages/';
        isRoot = true;
    } else if (path.includes('/pages/')) {
        // e.g. /pages/learn/python.html -> depth after pages is 2.
        const pathAfterPages = path.substring(path.indexOf('/pages/') + 7);
        const depthAfterPages = pathAfterPages.split('/').length - 1;
        if (depthAfterPages === 0) {
            prefix = './';
        } else if (depthAfterPages === 1) {
            prefix = '../';
        } else if (depthAfterPages === 2) {
            prefix = '../../';
        } else if (depthAfterPages === 3) {
            prefix = '../../../';
        }
    } else {
        // Fallback
        prefix = './';
    }

    const navData = [
        {
            catText: "Programming",
            links: [
                { href: "python.html", iconName: "code-2", text: "Python" },
                { href: "sql.html", iconName: "database", text: "SQL" },
                { href: "bash.html", iconName: "terminal", text: "Bash" },
                { href: "powershell.html", iconName: "terminal-square", text: "PowerShell" },
                { href: "dsa-de.html", iconName: "git-branch-plus", text: "DSA" }
            ]
        },
        {
            catText: "Concepts & Design",
            links: [
                { href: "de-fundamentals.html", iconName: "layers", text: "DE Fundamentals" },
                { href: "system-design.html", iconName: "layout-dashboard", text: "System Design" },
                { href: "pipeline-design.html", iconName: "workflow", text: "Pipeline Design" },
                { href: "de-architectures.html", iconName: "cpu", text: "DE Architectures" }
            ]
        },
        {
            catText: "Tools",
            links: [
                { href: "spark.html", iconName: "zap", text: "Spark" },
                { href: "flink.html", iconName: "activity", text: "Flink" },
                { href: "kafka.html", iconName: "radio", text: "Kafka" },
                { href: "dbt.html", iconName: "blocks", text: "dbt" },
                { href: "pandas.html", iconName: "table-2", text: "Pandas" },
                { href: "numpy.html", iconName: "hash", text: "NumPy" },
                { href: "airflow.html", iconName: "wind", text: "Airflow" },
                { href: "regex.html", iconName: "search", text: "Regex" }
            ]
        },
        {
            catText: "Cloud",
            links: [
                { href: "aws.html", iconName: "cloud", text: "AWS" },
                { href: "gcp.html", iconName: "cloud-sun", text: "GCP" },
                { href: "azure.html", iconName: "cloud-cog", text: "Azure" },
                { href: "snowflake.html", iconName: "snowflake", text: "Snowflake" },
                { href: "databricks.html", iconName: "box", text: "Databricks" }
            ]
        },
        {
            catText: "CI / CD",
            links: [
                { href: "docker.html", iconName: "container", text: "Docker" },
                { href: "kubernetes.html", iconName: "network", text: "Kubernetes" },
                { href: "terraform.html", iconName: "sliders", text: "Terraform" },
                { href: "github.html", iconName: "git-branch", text: "GitHub" }
            ]
        },
        {
            catText: "Roadmaps",
            links: [
                { href: "../roadmaps/data-engineering.html", iconName: "database", text: "Data Engineering" },
                { href: "../roadmaps/ml-engineer.html", iconName: "brain-circuit", text: "ML Engineer" },
                { href: "../roadmaps/ai-engineer.html", iconName: "bot", text: "AI Engineer" }
            ]
        },
        {
            catText: "Practice",
            links: [
                { href: "../practice.html", iconName: "layout-grid", text: "Practice Hub" },
                { href: "../practice/list-comprehensions.html", iconName: "code", text: "Python Challenges" },
                { href: "../practice/sql-window-functions.html", iconName: "database", text: "SQL Challenges" }
            ]
        }
    ];

    function injectUniversalNav() {
        const existingNav = document.getElementById('ds-nav');
        if (existingNav) {
            existingNav.remove();
        }

        const rootPath = isRoot ? 'index.html' : (prefix + '../index.html');
        const profilePath = isRoot ? './pages/portfolio.html' : (prefix + 'portfolio.html');

        const navHtml = `
            <div class="px-4 md:px-6 py-3.5 flex items-center justify-between w-full relative">
                <!-- LEFT: Logo and Page Title -->
                <div class="flex items-center gap-4 relative z-50">
                    <!-- Mobile Hamburger -->
                    <button id="ds-topnav-mob-btn" aria-label="Menu" class="lg:hidden relative w-10 h-10 flex items-center justify-center transition-all hover:bg-slate-50 rounded-full">
                        <i data-lucide="menu" class="w-5 h-5 text-slate-700"></i>
                    </button>

                    <a href="${rootPath}" class="no-underline group flex items-center gap-3 transition-transform duration-300 hover:scale-105">
                        <div class="flex items-center">
                            <span style="font-family: 'Outfit', sans-serif;" class="text-[24px] md:text-[28px] tracking-tighter flex items-center">
                                <span class="font-light text-slate-500">Data</span>
                                <span class="font-black bg-gradient-to-br from-indigo-600 via-blue-600 to-emerald-500 bg-clip-text text-transparent ml-1.5 inline-block -rotate-3 origin-bottom-left">Cake</span>
                            </span>
                        </div>
                    </a>
                </div>

                <!-- CENTER: Dropdowns (Desktop) -->
                <div id="ds-topnav" class="hidden lg:flex flex-1 justify-center px-4 absolute left-0 right-0 z-40">
                    <div id="ds-topnav-inner" class="flex items-center gap-1"></div>
                </div>

                <!-- RIGHT: Profile Icon -->
                <div class="flex items-center relative z-50">
                    <a href="${profilePath}" id="profile-btn" title="Profile"
                        class="w-9 h-9 flex items-center justify-center rounded-full bg-slate-100 text-slate-600 hover:bg-blue-50 hover:text-blue-600 transition-all border border-slate-200/60 no-underline">
                        <i data-lucide="user" class="w-5 h-5"></i>
                    </a>
                </div>
            </div>

            <!-- Mobile Drawer (hidden by default) -->
            <div id="ds-topnav-mobile-drawer">
                <div id="ds-topnav-overlay"></div>
                <div id="ds-topnav-panel">
                    <div id="ds-topnav-panel-inner" class="flex flex-col gap-2"></div>
                </div>
            </div>
        `;

        const navEl = document.createElement('nav');
        navEl.id = 'ds-nav';
        navEl.className = 'fixed top-0 w-full z-50 bg-white/95 backdrop-blur-xl border-b border-slate-200 transition-colors duration-300';
        navEl.innerHTML = navHtml;
        document.body.insertBefore(navEl, document.body.firstChild);

        // Populate Dropdowns
        const topnavInner = document.getElementById('ds-topnav-inner');
        const mobPanelInner = document.getElementById('ds-topnav-panel-inner');

        navData.forEach((catData, index) => {
            // Desktop
            const ddItem = document.createElement('div');
            ddItem.className = 'group/dd relative inline-block text-left';
            
            const ddBtn = document.createElement('button');
            ddBtn.className = 'inline-flex w-full items-center justify-center gap-1.5 rounded-full px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:text-indigo-600 transition-colors';
            ddBtn.innerHTML = `<span>${catData.catText}</span> <i data-lucide="chevron-down" class="w-4 h-4 text-slate-400 group-hover/dd:text-indigo-500 transition-transform group-hover/dd:rotate-180"></i>`;
            ddItem.appendChild(ddBtn);

            const ddMenu = document.createElement('div');
            ddMenu.className = 'absolute left-1/2 -translate-x-1/2 z-50 mt-1 w-56 origin-top-right rounded-2xl bg-white shadow-xl ring-1 ring-black/5 focus:outline-none opacity-0 invisible group-hover/dd:opacity-100 group-hover/dd:visible transition-all duration-200 border border-slate-200';
            
            const p2 = document.createElement('div');
            p2.className = 'p-2 flex flex-col gap-1';
            
            catData.links.forEach(link => {
                let finalHref = link.href;
                if (!finalHref.startsWith('http')) {
                    if (isRoot && finalHref.startsWith('../')) {
                        finalHref = './pages/' + finalHref.substring(3);
                    } else if (!isRoot && finalHref.startsWith('../')) {
                        finalHref = prefix + finalHref.substring(3);
                    } else {
                        finalHref = prefix + finalHref;
                    }
                }

                const a = document.createElement('a');
                a.href = finalHref;
                a.className = 'group/link flex items-center gap-3 rounded-xl px-3 py-2 text-sm text-slate-700 hover:bg-indigo-50 hover:text-indigo-700 transition-colors no-underline';
                a.innerHTML = `<i data-lucide="${link.iconName}" class="w-4 h-4 text-slate-400 group-hover/link:text-indigo-500"></i> ${link.text}`;
                p2.appendChild(a);
            });
            ddMenu.appendChild(p2);
            ddItem.appendChild(ddMenu);
            topnavInner.appendChild(ddItem);

            // Mobile
            const mobCat = document.createElement('div');
            mobCat.className = 'flex flex-col mb-2';
            mobCat.innerHTML = `<div class="px-3 py-2 text-xs font-bold text-slate-400 uppercase tracking-wider">${catData.catText}</div>`;
            
            catData.links.forEach(link => {
                let finalHref = link.href;
                if (!finalHref.startsWith('http')) {
                    if (isRoot && finalHref.startsWith('../')) {
                        finalHref = './pages/' + finalHref.substring(3);
                    } else if (!isRoot && finalHref.startsWith('../')) {
                        finalHref = prefix + finalHref.substring(3);
                    } else {
                        finalHref = prefix + finalHref;
                    }
                }

                const a = document.createElement('a');
                a.href = finalHref;
                a.className = 'flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-100 transition-colors no-underline';
                a.innerHTML = `<i data-lucide="${link.iconName}" class="w-4 h-4 text-slate-400"></i> ${link.text}`;
                mobCat.appendChild(a);
            });
            mobPanelInner.appendChild(mobCat);
        });

        // Mobile drawer toggles
        const mobBtn = document.getElementById('ds-topnav-mob-btn');
        const mobDrawer = document.getElementById('ds-topnav-mobile-drawer');
        const mobOverlay = document.getElementById('ds-topnav-overlay');
        mobBtn.addEventListener('click', () => mobDrawer.classList.add('open'));
        mobOverlay.addEventListener('click', () => mobDrawer.classList.remove('open'));
    }

    function injectUniversalFooter() {
        if (isRoot) return; // Except in homepage

        const existingFooter = document.querySelector('footer');
        if (existingFooter) existingFooter.remove();

        const footer = document.createElement('footer');
        footer.className = 'mt-32 py-12 border-t border-slate-200 text-center bg-slate-50 transition-colors duration-300 relative z-10 w-full';
        footer.innerHTML = '<p class="text-slate-400 font-bold tracking-widest uppercase text-xs">&copy; 2026 Data Cake</p>';
        document.body.appendChild(footer);
    }

    // Initialize
    injectUniversalNav();
    injectUniversalFooter();

    // Re-initialize icons since we dynamically injected HTML with lucide attributes
    if (window.lucide && window.lucide.createIcons) {
        window.lucide.createIcons();
    }

    // --- Profile Hover Animation ---
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
    
    initProfileHoverLabel();

})();
