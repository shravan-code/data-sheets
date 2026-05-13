(function () {
    'use strict';

    const CONFIG = {
        'de-fundamentals': {
            label: 'DE Fundamentals',
            title: 'DE Fundamentals',
            badge: 'Concepts Guide',
            description: 'The definitive guide to the foundational principles of Data Engineering.',
            indexPath: '../data/de_fundamentals_guide.json',
            topicPath: '../../data/de_fundamentals_guide.json',
            indexHref: '../de-fundamentals.html',
            accent: 'violet',
            icon: 'layers',
            sidebarLabel: 'Fundamentals'
        },
        'dsa-de': {
            label: 'DSA for DE',
            title: 'DSA Mastery',
            badge: 'DSA Guide',
            description: 'Master the algorithms and data structures that power modern data platforms.',
            indexPath: '../data/dsa_guide.json',
            topicPath: '../../data/dsa_guide.json',
            indexHref: '../dsa-de.html',
            accent: 'emerald',
            icon: 'git-branch-plus',
            sidebarLabel: 'DSA Topics'
        }
    };

    async function loadJson(path) {
        const response = await fetch(path);
        if (!response.ok) throw new Error(`Unable to load guide JSON: ${response.status}`);
        return response.json();
    }

    function esc(value) {
        return String(value ?? '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    /* ── INDEX PAGE ─────────────────────────────────────────────────────────── */

    function renderIndex(root, type, raw) {
        const cfg = CONFIG[type];
        const topics = raw.topics || [];

        document.title = `${cfg.label} — Data Cake`;
        root.innerHTML = `
            <header class="mb-20 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-${cfg.accent}-50 text-${cfg.accent}-700 dark:bg-${cfg.accent}-900/30 dark:text-${cfg.accent}-400 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border border-${cfg.accent}-100 dark:border-${cfg.accent}-800">
                    <i data-lucide="${cfg.icon}" class="w-3 h-3"></i> ${esc(cfg.badge)}
                </div>
                <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-tight">${esc(cfg.title)}</h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium">${esc(raw.description || cfg.description)}</p>
            </header>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                ${topics.map((topic, i) => `
                    <a href="${type}/${esc(topic.id)}.html"
                       class="group flex flex-col gap-2 p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl transition-all hover:border-${cfg.accent}-300 hover:shadow-lg hover:shadow-${cfg.accent}-100/40 no-underline">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 rounded-xl bg-${cfg.accent}-50 dark:bg-${cfg.accent}-900/40 flex items-center justify-center text-${cfg.accent}-600 dark:text-${cfg.accent}-400 group-hover:bg-${cfg.accent}-500 group-hover:text-white transition-all flex-shrink-0">
                                <span class="text-xs font-black">${i + 1}</span>
                            </div>
                            <span class="text-sm font-bold text-slate-800 dark:text-slate-100 group-hover:text-${cfg.accent}-700 transition-colors leading-tight">${esc(topic.title.replace(/^\d+\.\s*/, ''))}</span>
                        </div>
                        ${topic.description ? `<p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed pl-12">${esc(topic.description)}</p>` : ''}
                    </a>
                `).join('')}
            </div>
        `;
    }

    /* ── SIDEBAR INJECTION ──────────────────────────────────────────────────── */

    function buildSidebar(type, raw, currentId) {
        const cfg = CONFIG[type];
        const topics = raw.topics || [];
        const sidebar = document.getElementById('ds-sidebar');
        if (!sidebar) return;

        // Remove any existing guide-topics first (ds-main.js may have already removed it)
        const existing = document.getElementById('guide-topics');
        if (existing) existing.remove();

        // Find the last .flex-1 container inside the sidebar to append to
        const sidebarInner = sidebar.querySelector('.flex-1');
        if (!sidebarInner) return;

        const wrapper = document.createElement('div');
        wrapper.id = 'guide-topics';
        wrapper.className = 'mt-6';
        wrapper.innerHTML = `
            <div class="sb-section sb-cat bg-slate-50 text-slate-700 hover:bg-slate-100 cursor-pointer">
                <span class="w-6 h-6 rounded-md bg-slate-400 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="list" class="w-3 h-3 text-white"></i>
                </span>
                ${esc(cfg.sidebarLabel)}
            </div>
            <nav class="pl-2">
                ${topics.map(t => `
                    <a href="${esc(t.id)}.html" class="sb-link${t.id === currentId ? ' active' : ''}">${esc(t.title)}</a>
                `).join('')}
            </nav>
        `;
        sidebarInner.appendChild(wrapper);
    }


    /* ── TOPIC PAGE ─────────────────────────────────────────────────────────── */

    function renderTopic(main, type, raw, slug) {
        const cfg = CONFIG[type];
        const topics = raw.topics || [];
        const topic = topics.find(t => t.id === slug);
        if (!topic) throw new Error(`Topic not found in JSON: ${slug}`);

        const prev = topic.prev ? topics.find(t => t.id === topic.prev) : null;
        const next = topic.next ? topics.find(t => t.id === topic.next) : null;

        document.title = `${topic.title} — Data Cake`;

        // Update nav bar title
        const navTitle = document.querySelector('#ds-nav .hidden.md\\:flex span.text-sm');
        if (navTitle) navTitle.textContent = topic.title;

        main.innerHTML = `
            <a href="${esc(cfg.indexHref)}" class="inline-flex items-center gap-2 text-sm font-medium text-${cfg.accent}-600 dark:text-${cfg.accent}-400 hover:text-${cfg.accent}-700 dark:hover:text-${cfg.accent}-300 transition-colors mb-6 group no-underline">
                <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
                Back to ${esc(cfg.label)}
            </a>

            <h1 class="font-display font-bold text-4xl md:text-5xl text-slate-900 dark:text-white mb-4 leading-tight">${esc(topic.title)}</h1>
            <p class="text-xl text-slate-600 dark:text-slate-400 mb-12">${esc(topic.description)}</p>

            <div class="prose prose-slate dark:prose-invert prose-lg max-w-none">
                ${topic.content}
            </div>

            <div class="mt-20"></div>

            <div class="nav-container">
                ${prev ? `
                <a href="${esc(prev.id)}.html" class="nav-card prev">
                    <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
                    <span class="nav-title">${esc(prev.title)}</span>
                </a>` : '<div></div>'}

                ${next ? `
                <a href="${esc(next.id)}.html" class="nav-card next">
                    <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
                    <span class="nav-title">${esc(next.title)}</span>
                </a>` : '<div></div>'}
            </div>
        `;
    }

    /* ── TOC ────────────────────────────────────────────────────────────────── */

    function populateToc(root) {
        const toc = document.querySelector('.toc-list');
        const tocWrapper = document.querySelector('.toc-container');
        if (!toc) return;
        const headers = root.querySelectorAll('h2, h3');
        toc.innerHTML = '';
        if (!headers.length) {
            if (tocWrapper) tocWrapper.style.display = 'none';
            return;
        }
        if (tocWrapper) tocWrapper.style.display = window.innerWidth >= 1280 ? 'block' : 'none';
        headers.forEach((header, index) => {
            if (!header.id) header.id = header.textContent.toLowerCase().trim().replace(/\s+/g, '-').replace(/[^\w-]/g, '') + '-' + index;
            const li = document.createElement('li');
            const link = document.createElement('a');
            link.href = `#${header.id}`;
            link.textContent = header.textContent;
            link.className = header.tagName.toLowerCase() === 'h3' ? 'toc-link toc-h3' : 'toc-link';
            li.appendChild(link);
            toc.appendChild(li);
        });
    }

    /* ── BOOT ───────────────────────────────────────────────────────────────── */

    function detectType() {
        // Index page: <div data-guide-type="de-fundamentals">
        const root = document.querySelector('[data-guide-type]');
        if (root) return root.dataset.guideType;

        // Sub-page: infer from pathname
        const match = location.pathname.match(/\/(de-fundamentals|dsa-de)\//);
        return match && match[1];
    }

    document.addEventListener('DOMContentLoaded', async () => {
        const type = detectType();
        if (!type || !CONFIG[type]) return;

        const cfg = CONFIG[type];
        const indexRoot = document.querySelector(`[data-guide-type="${type}"]`);
        const isIndex = !!indexRoot;

        const jsonPath = isIndex
            ? (indexRoot.dataset.guidePath || cfg.indexPath)
            : cfg.topicPath;

        try {
            const raw = await loadJson(jsonPath);

            if (isIndex) {
                renderIndex(indexRoot, type, raw);
            } else {
                const main = document.querySelector('#ds-main-content main');
                if (!main) return;
                const slug = location.pathname.split('/').pop().replace(/\.html$/, '');
                renderTopic(main, type, raw, slug);
                buildSidebar(type, raw, slug);
                populateToc(main);
                if (window.Prism) window.Prism.highlightAll();
            }

            if (window.lucide) window.lucide.createIcons();

            // Re-initialize mermaid after content injection
            // Use a small timeout to allow DOM to settle
            setTimeout(() => {
                if (window.mermaid) {
                    try {
                        window.mermaid.run({ querySelector: '.mermaid' });
                    } catch (e) { /* ignore */ }
                }
            }, 100);
        } catch (error) {
            const target = isIndex ? indexRoot : document.querySelector('#ds-main-content main');
            if (target) {
                target.innerHTML = `<div class="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-rose-700"><h2 class="font-display font-bold text-xl mb-2">Unable to load guide</h2><p class="text-sm">${esc(error.message)}</p></div>`;
            }
        }
    });
})();
