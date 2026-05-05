/* airflow-guide.js — Dynamic renderer for Airflow section detail pages */
(function () {
    'use strict';

    function esc(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    /* ── Slugs matching the section HTML file names ── */
    const SECTION_SLUGS = [
        'fundamentals',
        'installation-setup',
        'dags',
        'operators',
        'taskflow-api',
        'sensors',
        'xcom',
        'connections-hooks',
        'variables-templating',
        'executors',
        'task-dependencies',
        'subdags-task-groups',
        'dynamic-dags',
        'pools-queues',
        'slas-alerts-monitoring',
        'security',
        'testing-cicd',
        'performance-scaling',
        'airflow-on-kubernetes',
        'cloud-managed-airflow',
        'integrations',
        'advanced-patterns',
        'interview-preparation',
    ];

    /* ── Section icon map ── */
    const SECTION_ICONS = {
        1: 'wind', 2: 'terminal', 3: 'git-branch', 4: 'cpu',
        5: 'code-2', 6: 'radio', 7: 'arrow-left-right', 8: 'plug',
        9: 'settings-2', 10: 'server', 11: 'git-merge', 12: 'layers',
        13: 'repeat', 14: 'database', 15: 'bell', 16: 'shield',
        17: 'test-tube-2', 18: 'gauge', 19: 'cloud', 20: 'cloud-cog',
        21: 'blocks', 22: 'sparkles', 23: 'award',
    };

    /* ─────────────── Code block renderer ─────────────── */
    function renderCode(code) {
        if (!code) return '';
        return `
            <div class="relative group/code mt-4 mb-2">
                <div class="flex items-center justify-between bg-slate-800 dark:bg-slate-950 px-4 py-2 rounded-t-xl">
                    <span class="text-[10px] font-black uppercase tracking-widest text-slate-400">Python</span>
                    <button onclick="airflowCopyCode(this)" class="flex items-center gap-1 text-[10px] font-bold text-slate-400 hover:text-white transition-colors px-2 py-1 rounded-md hover:bg-white/10">
                        <i data-lucide="copy" class="w-3 h-3"></i> Copy
                    </button>
                </div>
                <pre class="bg-slate-900 dark:bg-slate-950 text-slate-100 text-sm leading-7 p-5 rounded-b-xl overflow-x-auto m-0 border border-slate-700/50"><code>${esc(code)}</code></pre>
            </div>`;
    }

    /* ─────────────── Bullet list renderer ─────────────── */
    function renderList(items, color = 'orange') {
        if (!items || !items.length) return '';
        if (typeof items === 'string') items = [items];
        const colorMap = {
            orange: 'text-orange-500',
            emerald: 'text-emerald-500',
            red: 'text-red-500',
            amber: 'text-amber-500',
        };
        const cls = colorMap[color] || colorMap.orange;
        return `<ul class="space-y-2 mt-3">
            ${items.map(it => {
                let content = '';
                if (typeof it === 'object' && it !== null) {
                    if (it.param && it.description) {
                        content = `<strong>${esc(it.param)}</strong>${it.default ? ` <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded ml-1">def: ${esc(it.default)}</span>` : ''}: ${esc(it.description)}`;
                    } else if (it.key && it.description) {
                        content = `<strong>${esc(it.key)}</strong>${it.default ? ` <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded ml-1">def: ${esc(it.default)}</span>` : ''}: ${esc(it.description)}`;
                    } else if (it.name && it.description) {
                        content = `<strong>${esc(it.name)}</strong>: ${esc(it.description)}`;
                    } else {
                        const k = Object.keys(it)[0];
                        if (k && it[k]) {
                            content = `<strong>${esc(k)}</strong>: ${esc(String(it[k]))}`;
                        } else {
                            content = esc(JSON.stringify(it));
                        }
                    }
                } else {
                    content = esc(it);
                }
                return `<li class="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-300 leading-6">
                    <i data-lucide="chevron-right" class="w-4 h-4 mt-0.5 flex-shrink-0 ${cls}"></i>
                    <span>${content}</span>
                </li>`;
            }).join('')}
        </ul>`;
    }

    /* ─────────────── Comparison table renderer ─────────────── */
    function renderTable(rows) {
        if (!rows || !rows.length) return '';
        const headers = rows[0] ? Object.keys(rows[0]) : [];
        return `
            <div class="overflow-x-auto mt-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm">
                <table class="w-full text-sm">
                    <thead class="bg-orange-50 dark:bg-orange-950/30">
                        <tr>${headers.map(h => `<th class="px-4 py-3 text-left font-bold text-slate-700 dark:text-slate-200 text-xs uppercase tracking-wide border-b border-slate-200 dark:border-slate-700">${esc(h.replace(/_/g,' '))}</th>`).join('')}</tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                        ${rows.map((row, ri) => `<tr class="${ri % 2 === 0 ? 'bg-white dark:bg-slate-900' : 'bg-slate-50/60 dark:bg-slate-800/40'}">
                            ${headers.map(h => `<td class="px-4 py-3 text-slate-600 dark:text-slate-300">${esc(row[h])}</td>`).join('')}
                        </tr>`).join('')}
                    </tbody>
                </table>
            </div>`;
    }

    /* ─────────────── Single topic card ─────────────── */
    function renderTopic(t, idx, sectionIcon) {
        const hasCode = t.example && (t.example.code || Object.values(t.example).find(v => typeof v === 'string' && v.includes('\n')));
        const codeStr = t.example ? (t.example.code || Object.values(t.example).find(v => typeof v === 'string' && v.includes('\n'))) : null;

        let body = '';

        // explanation
        if (t.explanation) {
            body += `<p class="text-slate-600 dark:text-slate-300 text-sm leading-7">${esc(t.explanation)}</p>`;
        }

        // key_features / what_airflow_is_not / built_in_roles / advantages / benefits
        if (t.key_features?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Key Features</span>${renderList(t.key_features)}</div>`;
        if (t.what_airflow_is_not?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-red-500">What Airflow is NOT</span>${renderList(t.what_airflow_is_not, 'red')}</div>`;
        if (t.dag_properties?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">DAG Properties</span>${renderList(t.dag_properties)}</div>`;
        if (t.base_sensor_params?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Parameters</span>${renderList(t.base_sensor_params)}</div>`;
        if (t.xcom_limits?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-amber-500">XCom Limits</span>${renderList(t.xcom_limits, 'amber')}</div>`;
        if (t.connection_fields?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Connection Fields</span>${renderList(t.connection_fields)}</div>`;
        if (t.built_in_roles?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Built-in Roles</span>${renderList(t.built_in_roles)}</div>`;
        if (t.advantages?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-emerald-500">Advantages</span>${renderList(t.advantages, 'emerald')}</div>`;
        if (t.benefits?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-emerald-500">Benefits</span>${renderList(t.benefits, 'emerald')}</div>`;
        if (t.use_cases?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Use Cases</span>${renderList(t.use_cases)}</div>`;
        if (t.use_case) body += `<div class="mt-3 p-3 bg-orange-50 dark:bg-orange-950/20 border border-orange-100 dark:border-orange-900/50 rounded-lg"><span class="text-xs font-black uppercase tracking-widest text-orange-500 block mb-1">Best For</span><p class="text-sm text-slate-600 dark:text-slate-300">${esc(t.use_case)}</p></div>`;
        if (t.best_for) body += `<div class="mt-3 p-3 bg-orange-50 dark:bg-orange-950/20 border border-orange-100 dark:border-orange-900/50 rounded-lg"><span class="text-xs font-black uppercase tracking-widest text-orange-500 block mb-1">Best For</span><p class="text-sm text-slate-600 dark:text-slate-300">${esc(t.best_for)}</p></div>`;

        // steps / config / scheduler_ha / key_settings / install_with_extras
        if (t.steps?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Steps</span>${renderList(t.steps)}</div>`;
        if (t.install_with_extras?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Install Extras</span>${renderList(t.install_with_extras)}</div>`;
        if (t.config?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Config</span>${renderList(t.config)}</div>`;
        if (t.key_settings?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Key Settings</span>${renderList(t.key_settings)}</div>`;
        if (t.scheduler_ha?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Scheduler HA</span>${renderList(t.scheduler_ha)}</div>`;
        if (t.setup?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Setup Steps</span>${renderList(t.setup)}</div>`;
        if (t.limitations?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-red-500">Limitations</span>${renderList(t.limitations, 'red')}</div>`;
        if (t.drawbacks?.length) {
            const dArr = Array.isArray(t.drawbacks) ? t.drawbacks : [t.drawbacks];
            body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-red-500">Drawbacks</span>${renderList(dArr, 'red')}</div>`;
        }
        if (t.solutions?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-emerald-500">Solutions</span>${renderList(t.solutions, 'emerald')}</div>`;
        if (t.why_airflow_wins?.length) body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-emerald-500">Why Airflow Wins</span>${renderList(t.why_airflow_wins, 'emerald')}</div>`;

        // comparison_table
        if (t.comparison_table?.length) body += `<div class="mt-4"><span class="text-xs font-black uppercase tracking-widest text-orange-500 block mb-2">Comparison</span>${renderTable(t.comparison_table)}</div>`;

        // object comparison (e.g. Poke vs Reschedule Mode)
        if (t.comparison && typeof t.comparison === 'object' && !Array.isArray(t.comparison)) {
            let compBody = '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">';
            for (const key of Object.keys(t.comparison)) {
                const obj = t.comparison[key];
                const title = key.replace(/_/g, ' ');
                compBody += `<div class="p-5 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-200 dark:border-slate-700/50">
                    <h4 class="font-black text-slate-900 dark:text-white capitalize mb-3 text-lg">${esc(title)}</h4>
                    <ul class="space-y-3">`;
                for (const subKey of Object.keys(obj)) {
                    compBody += `<li class="text-sm text-slate-600 dark:text-slate-300 flex items-start gap-2">
                        <i data-lucide="check-circle-2" class="w-4 h-4 mt-0.5 text-emerald-500 flex-shrink-0"></i>
                        <span><strong class="capitalize">${esc(subKey.replace(/_/g, ' '))}</strong>: ${esc(obj[subKey])}</span>
                    </li>`;
                }
                compBody += `</ul></div>`;
            }
            compBody += '</div>';
            body += compBody;
        }

        // architecture_diagram (array of strings)
        if (t.architecture_diagram?.length) {
            body += `<div class="mt-4 p-4 bg-slate-900 dark:bg-slate-950 rounded-xl border border-slate-700"><span class="text-xs font-black uppercase tracking-widest text-orange-400 block mb-2">Architecture</span><pre class="text-xs text-slate-300 leading-6 overflow-x-auto">${esc(t.architecture_diagram.join('\n'))}</pre></div>`;
        }

        // nested_task_groups
        if (t.nested_task_groups) {
            body += `<div class="mt-3 p-3 bg-slate-50 dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700"><span class="text-xs font-black uppercase tracking-widest text-orange-500 block mb-1">Nested Task Groups</span><p class="text-sm text-slate-600 dark:text-slate-300">${esc(t.nested_task_groups)}</p></div>`;
        }

        // methods array (e.g., Managing Connections)
        if (t.methods && Array.isArray(t.methods)) {
            let mBody = '<div class="mt-4 space-y-3">';
            for (const m of t.methods) {
                mBody += `<div class="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700">`;
                if (m.method) mBody += `<h5 class="font-bold text-slate-800 dark:text-slate-100 mb-2">${esc(m.method)}</h5>`;
                if (m.description) mBody += `<p class="text-sm text-slate-600 dark:text-slate-300 mb-2">${esc(m.description)}</p>`;
                if (m.benefit) mBody += `<p class="text-sm text-emerald-600 dark:text-emerald-400 mt-2"><i data-lucide="check-circle-2" class="w-3 h-3 inline mr-1"></i>${esc(m.benefit)}</p>`;
                if (m.drawback) mBody += `<p class="text-sm text-red-600 dark:text-red-400 mt-2"><i data-lucide="x-circle" class="w-3 h-3 inline mr-1"></i>${esc(m.drawback)}</p>`;
                if (m.example) mBody += `<div class="mt-3"><span class="text-[10px] font-black uppercase tracking-widest text-slate-400 block mb-1">Example</span>${renderCode(m.example)}</div>`;
                mBody += `</div>`;
            }
            mBody += '</div>';
            body += `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-orange-500">Methods</span>${mBody}</div>`;
        }

        // code examples (singular and plural)
        if (t.examples && typeof t.examples === 'object') {
            const exKeys = Object.keys(t.examples);
            for (const k of exKeys) {
                const v = t.examples[k];
                if (typeof v === 'string') {
                    body += `<div class="mt-5"><span class="text-[10px] font-black uppercase tracking-widest text-slate-400 block mb-2">${esc(k.replace(/_/g,' '))}</span>${renderCode(v)}</div>`;
                }
            }
        }
        if (t.example) {
            if (typeof t.example === 'string') {
                body += `<div class="mt-5"><span class="text-[10px] font-black uppercase tracking-widest text-slate-400 block mb-2">Example</span>${renderCode(t.example)}</div>`;
            } else if (typeof t.example === 'object') {
                const exKeys = Object.keys(t.example);
                for (const k of exKeys) {
                    const v = t.example[k];
                    if (typeof v === 'string') {
                        body += `<div class="mt-5"><span class="text-[10px] font-black uppercase tracking-widest text-slate-400 block mb-2">${esc(k.replace(/_/g,' '))}</span>${renderCode(v)}</div>`;
                    }
                }
            }
        }

        return `
            <div class="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-10 h-10 rounded-xl bg-orange-50 dark:bg-orange-900/30 flex items-center justify-center text-orange-600 dark:text-orange-400 flex-shrink-0">
                        <i data-lucide="${sectionIcon}" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <span class="text-[10px] font-black uppercase tracking-widest text-slate-400">Topic ${idx + 1}</span>
                        <h3 class="text-base font-black text-slate-900 dark:text-white leading-tight">${esc(t.name)}</h3>
                    </div>
                </div>
                <div>${body}</div>
            </div>`;
    }

    /* ─────────────── Interview Q&A renderer ─────────────── */
    function renderInterview(questions) {
        return questions.map(q => `
            <details class="group bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800 rounded-2xl shadow-sm hover:shadow-md hover:border-orange-200 transition-all">
                <summary class="flex items-start gap-3 p-5 cursor-pointer list-none">
                    <span class="w-9 h-9 rounded-xl bg-orange-50 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 flex items-center justify-center text-xs font-black flex-shrink-0">${q.q_no}</span>
                    <span class="text-sm font-bold text-slate-700 dark:text-slate-300 flex-1 group-open:text-orange-600 dark:group-open:text-orange-400 transition-colors leading-snug pt-1.5">${esc(q.question)}</span>
                    <i data-lucide="chevron-down" class="w-4 h-4 text-slate-400 flex-shrink-0 mt-2 group-open:rotate-180 transition-transform duration-200"></i>
                </summary>
                <div class="px-5 pb-5 border-t border-slate-100 dark:border-slate-800">
                    <p class="text-sm text-slate-600 dark:text-slate-300 leading-7 pt-4">${esc(q.answer)}</p>
                    ${q.drawbacks?.length ? `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-red-500">Watch Out</span>${renderList(q.drawbacks, 'red')}</div>` : ''}
                    ${q.solutions?.length ? `<div class="mt-3"><span class="text-xs font-black uppercase tracking-widest text-emerald-500">Solutions</span>${renderList(q.solutions, 'emerald')}</div>` : ''}
                </div>
            </details>`).join('');
    }

    /* ─────────────── Main section renderer ─────────────── */
    function renderSection(root, guide) {
        const sectionId = parseInt(root.dataset.sectionId, 10);
        const indexHref = root.dataset.indexHref || '../airflow.html';
        const section = guide.sections.find(s => s.id === sectionId);

        if (!section) {
            root.innerHTML = `<div class="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-rose-700">Section not found (id=${sectionId})</div>`;
            return;
        }

        const icon = SECTION_ICONS[section.id] || 'book-open';
        const prev = guide.sections[guide.sections.indexOf(section) - 1];
        const next = guide.sections[guide.sections.indexOf(section) + 1];
        const prevSlug = prev ? SECTION_SLUGS[prev.id - 1] : null;
        const nextSlug = next ? SECTION_SLUGS[next.id - 1] : null;

        document.title = `${section.title} — Airflow — Data Cake`;

        let content = '';

        if (section.id === 23) {
            // Interview section
            content = `<div class="grid grid-cols-1 gap-3">${renderInterview(section.questions || [])}</div>`;
        } else {
            content = `<div class="grid grid-cols-1 gap-6">${(section.topics || []).map((t, i) => renderTopic(t, i, icon)).join('')}</div>`;
        }

        root.classList.remove('flex', 'items-center', 'justify-center', 'min-h-64');

        root.innerHTML = `
            <a href="${esc(indexHref)}" class="inline-flex items-center gap-2 text-sm font-bold text-orange-500 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300 transition-colors mb-8 group no-underline">
                <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
                Back to Airflow
            </a>
            <header class="mb-12">
                <div class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-4 flex items-center gap-2">
                    <span class="w-8 h-[1px] bg-slate-300 dark:bg-slate-700"></span>
                    Apache Airflow &mdash; Section ${section.id}
                </div>
                <h1 class="text-4xl md:text-6xl font-black text-slate-900 dark:text-white leading-tight tracking-tighter font-display">${esc(section.title)}</h1>
            </header>
            ${content}
            <div class="mt-8 p-8 bg-gradient-to-br from-orange-500 via-amber-500 to-orange-400 rounded-3xl text-white shadow-xl relative overflow-hidden">
                <div class="relative z-10">
                    <div class="flex items-center gap-2 text-orange-100 font-black uppercase tracking-widest text-[10px] mb-4">
                        <i data-lucide="zap" class="w-4 h-4"></i> Pro Tip
                    </div>
                    <p class="text-sm text-white/90 leading-7">Always design your DAGs to be <strong>idempotent</strong> — re-running the same task for the same interval should produce the same result. This makes debugging and backfilling safe.</p>
                </div>
                <i data-lucide="wind" class="absolute -right-4 -bottom-4 w-32 h-32 text-white/5 rotate-12"></i>
            </div>
            <nav class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
                ${prev && prevSlug ? `<a href="${prevSlug}.html" class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 no-underline hover:border-orange-200 transition-colors group">
                    <span class="flex items-center gap-1 text-xs font-bold uppercase text-slate-400 mb-1"><i data-lucide="arrow-left" class="w-3 h-3 transition-transform group-hover:-translate-x-1"></i> Previous</span>
                    <span class="block font-bold text-slate-800 dark:text-slate-100">${esc(prev.title)}</span>
                </a>` : '<div></div>'}
                ${next && nextSlug ? `<a href="${nextSlug}.html" class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 no-underline hover:border-orange-200 transition-colors sm:text-right group">
                    <span class="flex items-center gap-1 text-xs font-bold uppercase text-slate-400 mb-1 sm:justify-end">Next <i data-lucide="arrow-right" class="w-3 h-3 transition-transform group-hover:translate-x-1"></i></span>
                    <span class="block font-bold text-slate-800 dark:text-slate-100">${esc(next.title)}</span>
                </a>` : '<div></div>'}
            </nav>`;

                if (typeof lucide !== 'undefined') lucide.createIcons();
        populateToc(root);
    }

    function populateToc(root) {
        const toc = document.querySelector('.toc-list');
        if (!toc) return;
        const headers = root.querySelectorAll('h2, h3');
        toc.innerHTML = '';
        headers.forEach((header) => {
            if (!header.id) {
                header.id = header.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
            }
            const li = document.createElement('li');
            li.className = 'toc-item';
            const link = document.createElement('a');
            link.href = '#' + header.id;
            link.textContent = header.textContent;
            link.className = header.tagName.toLowerCase() === 'h3' ? 'toc-link toc-h3' : 'toc-link';
            
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

            li.appendChild(link);
            toc.appendChild(li);
        });
    }

    /* ─────────────── Boot ─────────────── */
    document.addEventListener('DOMContentLoaded', async () => {
        const root = document.getElementById('airflow-guide');
        if (!root) return;

        try {
            const guidePath = root.dataset.guidePath || '../../data/airflow_complete_guide.json';
            const resp = await fetch(guidePath);
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            const guide = data.guide;

            renderSection(root, guide);
            populateToc(root);
        } catch (err) {
            if (document.getElementById('airflow-guide')) {
                document.getElementById('airflow-guide').innerHTML =
                    `<div class="bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900 rounded-2xl p-8 text-rose-700 dark:text-rose-300">
                        <h2 class="font-bold text-lg mb-2">Failed to load guide</h2>
                        <p class="text-sm">${esc(err.message)}</p>
                     </div>`;
            }
        }
    });

    /* ─────────────── Global copy function ─────────────── */
    window.airflowCopyCode = function (btn) {
        const code = btn.closest('.relative').querySelector('code');
        if (!code) return;
        navigator.clipboard.writeText(code.textContent);
        const orig = btn.innerHTML;
        btn.innerHTML = '<i data-lucide="check" class="w-3 h-3"></i> Copied!';
        btn.classList.add('text-emerald-400');
        if (typeof lucide !== 'undefined') lucide.createIcons();
        setTimeout(() => { 
            btn.innerHTML = orig; 
            btn.classList.remove('text-emerald-400');         
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }, 2000);
    }
})();
