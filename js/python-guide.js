(function () {
    'use strict';

    const GUIDE_PATH_INDEX = '../data/python_complete_guide.json';
    const GUIDE_PATH_TOPIC = '../../data/python_complete_guide.json';

    function esc(value) {
        return String(value ?? '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function slugify(title) {
        return String(title || '')
            .toLowerCase()
            .trim()
            .replace(/&/g, 'and')
            .replace(/q&a/g, 'qanda')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    function topicSlug(topic) {
        const known = {
            'Dunder / Magic Methods': 'dunder---magic-methods',
            'Strings \u2014 All Methods': 'strings--all-methods',
            'Lists \u2014 All Methods': 'lists--all-methods',
            'Tuples \u2014 All Methods': 'tuples--all-methods',
            'Dictionaries \u2014 All Methods': 'dictionaries--all-methods',
            'Sets \u2014 All Methods': 'sets--all-methods',
            'Dataclasses \u2014 Complete Coverage': 'dataclasses--complete-coverage',
            'Protocol \u2014 Structural Subtyping': 'protocol--structural-subtyping',
            'deque \u2014 Double-Ended Queue': 'deque--double-ended-queue',
            'os Module \u2014 Complete': 'os-module--complete',
            'pathlib \u2014 Complete Reference': 'pathlib--complete-reference',
            'total_ordering and cmp_to_key': 'totalordering-and-cmptokey',
            'Interview Master: Top 50 Python Interview Q&A': 'interview-master-top-50-python-interview-qanda'
        };
        return known[topic.title] || slugify(topic.title);
    }

    function getParts(guide) {
        const content = guide.content || {};
        const byPart = new Map();
        ((content.guide || guide).parts || []).forEach((part) => byPart.set(part.part, part));
        Object.values(content).forEach((value) => {
            if (value && value.part && Array.isArray(value.topics)) byPart.set(value.part, value);
            if (value && value.part && Array.isArray(value.questions)) {
                byPart.set(value.part, {
                    part: value.part,
                    title: value.title,
                    topics: [{
                        id: `${value.part}.1`,
                        title: value.title,
                        explanation: 'High-signal Python interview questions and answers for review.',
                        subtopics: [],
                        interview_qa: value.questions
                    }]
                });
            }
        });
        return Array.from(byPart.values()).sort((a, b) => Number(a.part) - Number(b.part));
    }

    function flattenTopics(guide) {
        return getParts(guide).flatMap((part) =>
            (part.topics || []).map((topic) => ({ part, topic, slug: topicSlug(topic) }))
        );
    }

    async function loadGuide(path) {
        const response = await fetch(path);
        if (!response.ok) throw new Error(`Unable to load Python guide JSON: ${response.status}`);
        return response.json();
    }

    function iconForPart(partTitle) {
        const title = String(partTitle || '').toLowerCase();
        if (title.includes('control')) return 'git-merge';
        if (title.includes('data')) return 'layers';
        if (title.includes('function')) return 'command';
        if (title.includes('object')) return 'codesandbox';
        if (title.includes('error')) return 'alert-circle';
        if (title.includes('typing')) return 'type';
        if (title.includes('file') || title.includes('system')) return 'folder';
        if (title.includes('performance') || title.includes('concurrency')) return 'zap';
        if (title.includes('internal')) return 'cpu';
        if (title.includes('testing')) return 'test-tube';
        return 'code';
    }

    function renderIndex(root, guide) {
        const data = (guide.content || {}).guide || guide;
        const parts = getParts(guide);
        document.title = 'Python Mastery - Data Cake';

        root.innerHTML = `
            <header class="mb-20 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border border-indigo-100 dark:border-indigo-800">
                    <i data-lucide="award" class="w-3 h-3"></i> Expert Documentation
                </div>
                <h1 class="font-display text-6xl md:text-8xl font-black text-slate-900 dark:text-white mb-8 tracking-tighter leading-tight">
                    Python <span class="bg-gradient-to-r from-indigo-600 via-blue-600 to-indigo-400 bg-clip-text text-transparent">Mastery</span>
                </h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium">${esc(data.description || guide.description)}</p>
            </header>
            <div class="space-y-16">
                ${parts.map((part) => {
                    const icon = iconForPart(part.title);
                    return `
                        <section id="part-${esc(part.part)}" class="mb-12">
                            <div class="flex items-center gap-4 mb-8">
                                <div class="w-12 h-12 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-600">
                                    <span class="text-xl font-black">${esc(part.part)}</span>
                                </div>
                                <h2 class="text-3xl font-black text-slate-900 dark:text-white font-display tracking-tight">${esc(part.title)}</h2>
                            </div>
                            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                                ${(part.topics || []).map((topic) => `
                                    <a href="python/${esc(topicSlug(topic))}.html" class="flex items-center gap-3 p-4 bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800 rounded-2xl transition-all hover:bg-indigo-50/50 dark:hover:bg-indigo-900/20 hover:border-indigo-200 group/item no-underline shadow-sm hover:shadow-md">
                                        <div class="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 group-hover/item:bg-indigo-600 group-hover/item:text-white transition-all">
                                            <i data-lucide="${icon}" class="w-5 h-5"></i>
                                        </div>
                                        <span class="text-sm font-bold text-slate-700 dark:text-slate-300 group-hover/item:text-indigo-700 transition-colors">${esc(topic.title)}</span>
                                    </a>
                                `).join('')}
                            </div>
                        </section>
                    `;
                }).join('')}
            </div>
            <footer class="mt-32 py-12 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-bold tracking-widest uppercase text-[10px]">Data Cake Documentation - 2026</p>
            </footer>
        `;
    }

    function renderCodeBlock(item) {
        if (!item.code) return '';
        return `
            <div class="my-8 group">
                <div class="relative rounded-xl overflow-hidden bg-white border border-slate-200 shadow-sm transition-all hover:shadow-md p-6">
                    <pre class="language-python"><code>${esc(item.code)}</code></pre>
                    ${item.output ? `
                        <div class="mt-6 pt-6 border-t border-slate-100 bg-slate-50/50 -mx-6 -mb-6 px-6 pb-6">
                            <div class="text-[10px] uppercase tracking-widest text-slate-400 mb-3 font-bold flex items-center gap-2"><i data-lucide="terminal" class="w-3 h-3"></i> Output</div>
                            <pre class="!m-0 !p-0 !bg-transparent !border-0 !shadow-none !rounded-none"><code class="text-indigo-600 font-mono text-sm leading-relaxed">${esc(item.output)}</code></pre>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    function renderInterviewQa(items) {
        if (!items || !items.length) return '';
        return `
            <section class="mt-12">
                <h2 class="text-3xl font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-3 font-display">
                    <span class="w-1.5 h-8 bg-indigo-500 rounded-full"></span>Interview Q&A
                </h2>
                <div class="space-y-3">
                    ${items.map((item, index) => `
                        <details class="group rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/40 p-4">
                            <summary class="cursor-pointer list-none flex items-start gap-3">
                                <span class="w-8 h-8 rounded-lg bg-indigo-100 dark:bg-indigo-900/60 text-indigo-700 dark:text-indigo-300 flex items-center justify-center text-xs font-black flex-shrink-0">${index + 1}</span>
                                <span class="flex-1 text-sm font-bold text-slate-800 dark:text-slate-100">${esc(item.question)}</span>
                                <i data-lucide="chevron-down" class="w-4 h-4 text-slate-400 group-open:rotate-180 transition-transform"></i>
                            </summary>
                            <p class="text-sm text-slate-600 dark:text-slate-300 leading-7 mt-4 pl-11">${esc(item.answer)}</p>
                        </details>
                    `).join('')}
                </div>
            </section>
        `;
    }

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
            if (!header.id) {
                header.id = header.textContent.toLowerCase().trim()
                    .replace(/\s+/g, '-')
                    .replace(/[^\w-]/g, '') + '-' + index;
            }

            const li = document.createElement('li');
            const link = document.createElement('a');
            link.href = `#${header.id}`;
            link.textContent = header.textContent;
            link.className = header.tagName.toLowerCase() === 'h3' ? 'toc-link toc-h3' : 'toc-link';
            li.appendChild(link);
            toc.appendChild(li);
        });
    }

    function renderTopic(root, guide, item) {
        const { part, topic } = item;
        const currentIndex = flattenTopics(guide).findIndex((entry) => entry.slug === item.slug);
        const topics = flattenTopics(guide);
        const previous = topics[currentIndex - 1];
        const next = topics[currentIndex + 1];

        document.title = `${topic.title} - Python - Data Cake`;
        const navTitle = document.querySelector('#ds-nav .hidden.md\\:flex span.text-sm');
        if (navTitle) navTitle.textContent = topic.title;

        root.innerHTML = `
            <a href="../python.html#part-${esc(part.part)}" class="inline-flex items-center gap-2 text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors mb-6 group no-underline">
                <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>Back to Python
            </a>
            <header class="mb-12">
                <div class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-4 flex items-center gap-2">
                    <span class="w-8 h-[1px] bg-slate-300"></span>Section ${esc(part.part)}: ${esc(part.title)}
                </div>
                <h1 class="text-4xl md:text-6xl font-black text-slate-900 dark:text-white leading-tight tracking-tighter font-display">${esc(topic.title)}</h1>
            </header>
            <article class="prose dark:prose-invert max-w-none pb-20">
                <p class="text-lg text-slate-600 dark:text-slate-400 mb-8">${esc(topic.explanation)}</p>
                ${(topic.subtopics || []).map((subtopic) => `
                    <section class="mb-16">
                        <h2 class="text-3xl font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-3 font-display">
                            <span class="w-1.5 h-8 bg-indigo-500 rounded-full"></span>${esc(subtopic.title)}
                        </h2>
                        ${subtopic.explanation ? `<p class="text-slate-600 dark:text-slate-400 mb-6">${esc(subtopic.explanation)}</p>` : ''}
                        ${renderCodeBlock(subtopic)}
                    </section>
                `).join('')}
                ${renderInterviewQa(topic.interview_qa)}
                <div class="mt-16 flex flex-col sm:flex-row justify-between gap-4 border-t border-slate-200 dark:border-slate-800 pt-8">
                    ${previous ? `<a href="${esc(previous.slug)}.html" class="no-underline text-sm font-bold text-indigo-600 hover:text-indigo-700"><i data-lucide="arrow-left" class="inline w-4 h-4 mr-1"></i>${esc(previous.topic.title)}</a>` : '<span></span>'}
                    ${next ? `<a href="${esc(next.slug)}.html" class="no-underline text-sm font-bold text-indigo-600 hover:text-indigo-700 sm:text-right">${esc(next.topic.title)}<i data-lucide="arrow-right" class="inline w-4 h-4 ml-1"></i></a>` : '<span></span>'}
                </div>
            </article>
        `;
    }

    async function initIndex() {
        const root = document.getElementById('python-guide');
        if (!root) return false;
        try {
            renderIndex(root, await loadGuide(root.dataset.guidePath || GUIDE_PATH_INDEX));
            if (window.lucide) window.lucide.createIcons();
        } catch (error) {
            root.innerHTML = `<div class="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-rose-700"><h2 class="font-display font-bold text-xl mb-2">Unable to load Python guide</h2><p class="text-sm">${esc(error.message)}</p></div>`;
        }
        return true;
    }

    async function initTopic() {
        const main = document.querySelector('#ds-main-content main');
        if (!main || !location.pathname.includes('/python/')) return;

        const slug = location.pathname.split('/').pop().replace(/\.html$/, '');
        const loading = document.createElement('div');
        loading.className = 'rounded-2xl border border-slate-200 bg-white p-8 text-sm font-semibold text-slate-500';
        loading.textContent = 'Loading Python topic from JSON...';
        main.replaceChildren(loading);

        try {
            const guide = await loadGuide(GUIDE_PATH_TOPIC);
            const item = flattenTopics(guide).find((entry) => entry.slug === slug);
            if (!item) throw new Error(`Topic not found in JSON: ${slug}`);
            renderTopic(main, guide, item);
            populateToc(main);
            if (window.Prism) window.Prism.highlightAll();
            if (window.lucide) window.lucide.createIcons();
        } catch (error) {
            main.innerHTML = `<div class="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-rose-700"><h2 class="font-display font-bold text-xl mb-2">Unable to load Python topic</h2><p class="text-sm">${esc(error.message)}</p></div>`;
        }
    }

    document.addEventListener('DOMContentLoaded', async () => {
        if (await initIndex()) return;
        initTopic();
    });
})();
