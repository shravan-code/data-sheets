(function () {
    'use strict';

    const CONFIG = {
        sql: {
            label: 'SQL',
            title: 'SQL Mastery',
            badge: 'SQL Documentation',
            description: 'The bedrock of data engineering. From basic CRUD to advanced window functions and performance tuning.',
            indexPath: '../data/sql_complete_guide.json',
            topicPath: '../../data/sql_complete_guide.json',
            indexHref: '../sql.html',
            accent: 'blue',
            icon: 'database',
            lang: 'sql'
        },
        bash: {
            label: 'Bash',
            title: 'Bash Scripting',
            badge: 'Shell Guide',
            description: 'The language of the cloud. From simple pipes to production-grade automation engines.',
            indexPath: '../data/bash_guide.json',
            topicPath: '../../data/bash_guide.json',
            indexHref: '../bash.html',
            accent: 'emerald',
            icon: 'terminal',
            lang: 'bash'
        },
        powershell: {
            label: 'PowerShell',
            title: 'PowerShell Scripting',
            badge: 'Automation Guide',
            description: 'Master the art of automation. From local cmdlets to enterprise-scale remote orchestration.',
            indexPath: '../data/powershell_guide.json',
            topicPath: '../../data/powershell_guide.json',
            indexHref: '../powershell.html',
            accent: 'blue',
            icon: 'terminal',
            lang: 'powershell'
        },
        airflow: {
            label: 'Apache Airflow',
            title: 'Apache Airflow',
            badge: 'Workflow Orchestration',
            description: 'A comprehensive guide covering DAGs, operators, sensors, executors, XCom, security, Kubernetes deployment, and top interview questions.',
            indexPath: '../data/airflow_complete_guide.json',
            topicPath: '../../data/airflow_complete_guide.json',
            indexHref: '../airflow.html',
            accent: 'orange',
            icon: 'wind',
            lang: 'python'
        },
        spark: {
            label: 'Apache Spark',
            title: 'Apache Spark (PySpark)',
            badge: 'Distributed Computing',
            description: 'Distributed data processing with Apache Spark and PySpark for large-scale data engineering.',
            indexPath: '../data/spark_complete_guide.json',
            topicPath: '../../data/spark_complete_guide.json',
            indexHref: '../spark.html',
            accent: 'orange',
            icon: 'zap',
            lang: 'python'
        },
        flink: {
            label: 'Apache Flink',
            title: 'Apache Flink',
            badge: 'Stream Processing',
            description: 'Real-time stream and batch processing with Apache Flink for data engineering pipelines.',
            indexPath: '../data/flink_guide.json',
            topicPath: '../../data/flink_guide.json',
            indexHref: '../flink.html',
            accent: 'orange',
            icon: 'activity',
            lang: 'python'
        },
        kafka: {
            label: 'Apache Kafka',
            title: 'Apache Kafka',
            badge: 'Event Streaming',
            description: 'Distributed event streaming platform for building real-time data pipelines and applications.',
            indexPath: '../data/kafka_complete_guide.json',
            topicPath: '../../data/kafka_complete_guide.json',
            indexHref: '../kafka.html',
            accent: 'orange',
            icon: 'radio',
            lang: 'python'
        },
        dbt: {
            label: 'dbt',
            title: 'dbt (data build tool)',
            badge: 'Data Transformation',
            description: 'Transform your data in the warehouse with dbt — the T in the modern ELT stack.',
            indexPath: '../data/dbt_guide.json',
            topicPath: '../../data/dbt_guide.json',
            indexHref: '../dbt.html',
            accent: 'orange',
            icon: 'blocks',
            lang: 'sql'
        },
        pandas: {
            label: 'Pandas',
            title: 'Pandas',
            badge: 'Data Analysis',
            description: 'Powerful Python data analysis and manipulation with DataFrames for data engineering workflows.',
            indexPath: '../data/pandas_complete_guide.json',
            topicPath: '../../data/pandas_complete_guide.json',
            indexHref: '../pandas.html',
            accent: 'orange',
            icon: 'table-2',
            lang: 'python'
        },
        numpy: {
            label: 'NumPy',
            title: 'NumPy',
            badge: 'Numerical Computing',
            description: 'Numerical computing in Python with arrays, linear algebra, and statistical operations.',
            indexPath: '../data/numpy_guide.json',
            topicPath: '../../data/numpy_guide.json',
            indexHref: '../numpy.html',
            accent: 'orange',
            icon: 'hash',
            lang: 'python'
        },
        regex: {
            label: 'Regex',
            title: 'Regular Expressions',
            badge: 'Pattern Matching',
            description: 'Master regular expressions for data validation, extraction, and transformation in data engineering.',
            indexPath: '../data/regex_guide.json',
            topicPath: '../../data/regex_guide.json',
            indexHref: '../regex.html',
            accent: 'orange',
            icon: 'search',
            lang: 'python'
        },
        aws: {
            label: 'AWS',
            title: 'AWS for Data Engineering',
            badge: 'Cloud Documentation',
            description: 'Comprehensive guide to AWS services for data engineering: S3, Glue, Redshift, EMR, Kinesis, and more.',
            indexPath: '../data/aws_complete_guide.json',
            topicPath: '../../data/aws_complete_guide.json',
            indexHref: '../aws.html',
            accent: 'cyan',
            icon: 'cloud',
            lang: 'python'
        }
    };

    const SQL_SLUGS = {
        'MERGE / UPSERT': 'merge---upsert',
        'LIMIT / OFFSET': 'limit---offset',
        'AND / OR / NOT': 'and---or---not',
        'IN / NOT IN': 'in---not-in',
        'LIKE / ILIKE': 'like---ilike',
        'IS NULL / IS NOT NULL': 'is-null---is-not-null',
        'EXISTS / NOT EXISTS': 'exists---not-exists',
        'ROW_NUMBER': 'rownumber',
        'DENSE_RANK': 'denserank',
        'FIRST_VALUE': 'firstvalue',
        'LAST_VALUE': 'lastvalue',
        'NTH_VALUE': 'nthvalue',
        'SUM / AVG / COUNT as Window Functions': 'sum---avg---count-as-window-functions',
        'EXCEPT / MINUS': 'except---minus',
        'LENGTH / CHAR_LENGTH': 'length---charlength',
        'UPPER / LOWER': 'upper---lower',
        'TRIM / LTRIM / RTRIM': 'trim---ltrim---rtrim',
        'POSITION / LOCATE': 'position---locate',
        'SPLIT_PART': 'splitpart',
        'REGEXP_MATCH / REGEXP_REPLACE': 'regexpmatch---regexpreplace',
        'CEIL / FLOOR': 'ceil---floor',
        'CURRENT_DATE / NOW': 'currentdate---now',
        'DATE_PART / EXTRACT': 'datepart---extract',
        'DATE_TRUNC': 'datetrunc',
        'DATE_ADD / DATE_SUB / INTERVAL': 'dateadd---datesub---interval',
        'TO_DATE / TO_TIMESTAMP': 'todate---totimestamp',
        'CAST / CONVERT': 'cast---convert',
        'TRY_CAST': 'trycast',
        'When to Use / Avoid Indexes': 'when-to-use---avoid-indexes',
        'When to use / avoid Indexes': 'when-to-use---avoid-indexes',
        'EXPLAIN / EXPLAIN ANALYZE': 'explain---explain-analyze',
        'N+1 Problem': 'n1-problem',
        'Presto / Trino SQL': 'presto---trino-sql'
    };

    const SLUG_ALIASES = {
        bash: {
            'data-types-strings': 'data-types-and-strings',
            'file-directory-operations': 'file-and-directory-operations',
            'input-output': 'input-and-output',
            'operators-arithmetic': 'operators-and-arithmetic'
        }
    };

    function esc(value) {
        return String(value ?? '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function md(text) {
        if (!text) return '';
        // If marked is available, use it, otherwise fallback to esc
        if (typeof marked !== 'undefined' && marked.parse) {
            return marked.parse(text);
        }
        return esc(text);
    }

    function slugify(value) {
        return String(value || '')
            .toLowerCase()
            .trim()
            .replace(/&/g, 'and')
            .replace(/\+/g, 'plus')
            .replace(/#/g, 'sharp')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    function slugFor(type, item) {
        if (type === 'powershell') return item.id || slugify(item.title);
        const title = item.title || item.name || item.topic;
        if (type === 'sql' && SQL_SLUGS[title]) return SQL_SLUGS[title];
        return slugify(title);
    }

    async function loadJson(path) {
        const response = await fetch(path);
        if (!response.ok) throw new Error(`Unable to load guide JSON: ${response.status}`);
        return response.json();
    }

    const GENERIC_TOOLS = ['airflow', 'spark', 'flink', 'kafka', 'dbt', 'pandas', 'numpy', 'regex', 'aws'];

    function normalize(type, raw) {
        if (GENERIC_TOOLS.includes(type)) {
            const sections = (raw.guide ? (raw.guide.sections || raw.guide.topics) : (raw.sections || raw.topics)) || [];
            return sections.map((section) => ({
                id: section.id,
                title: section.title,
                description: section.description || '',
                topics: (section.topics || section.subtopics || []).map((topic) => ({
                    ...topic,
                    title: topic.title || topic.name,
                    slug: topic.slug || slugify(topic.title || topic.name),
                    section
                }))
            }));
        }

        if (type === 'sql') {
            const sections = raw.guide.sections || [];
            return sections.map((section) => {
                const topics = section.topics || [{ ...section, name: section.title, special: true }];
                return {
                    id: section.id,
                    title: section.title,
                    description: section.description || '',
                    topics: topics.map((topic) => ({
                        ...topic,
                        title: topic.name || topic.title,
                        slug: slugFor(type, topic),
                        section
                    }))
                };
            });
        }

        if (type === 'bash') {
            return (raw.topics || []).map((topic) => ({
                id: topic.id,
                title: topic.topic,
                topics: [{ ...topic, title: topic.topic, slug: slugFor(type, topic), section: { id: topic.id, title: topic.topic } }]
            }));
        }

        return (raw.topics || []).map((topic, index) => ({
            id: index + 1,
            title: topic.title,
            topics: [{ ...topic, slug: slugFor(type, topic), section: { id: index + 1, title: topic.title } }]
        }));
    }

    function flatten(sections) {
        return sections.flatMap((section) => section.topics);
    }

    function renderIndex(root, type, raw) {
        const cfg = CONFIG[type];
        const sections = normalize(type, raw);

        document.title = `${cfg.label} - Data Cake`;
        root.innerHTML = `
            <header class="mb-20 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-${cfg.accent}-50 text-${cfg.accent}-700 dark:bg-${cfg.accent}-900/30 dark:text-${cfg.accent}-400 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border border-${cfg.accent}-100 dark:border-${cfg.accent}-800">
                    <i data-lucide="${cfg.icon}" class="w-3 h-3"></i> ${esc(cfg.badge)}
                </div>
                <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-tight">${esc(cfg.title)}</h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium">${esc(raw.description || raw.guide?.title || cfg.description)}</p>
            </header>
            <div class="space-y-12">
                ${sections.map((section) => `
                    <section id="section-${esc(section.id)}" class="mb-12">
                        <div class="flex items-center gap-4 mb-8">
                            <div class="w-10 h-10 rounded-xl bg-${cfg.accent}-500/10 flex items-center justify-center text-${cfg.accent}-600"><span class="text-sm font-black">${esc(section.id)}</span></div>
                            <h2 class="text-2xl font-bold text-slate-900 dark:text-white font-display tracking-tight">${esc(section.title)}</h2>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                            ${section.topics.map((topic) => `
                                <a href="${type}/${esc(topic.slug)}.html" class="flex items-center gap-3 p-3 bg-${cfg.accent}-50/30 dark:bg-slate-900 border border-${cfg.accent}-100/50 dark:border-slate-800 rounded-xl transition-all hover:bg-${cfg.accent}-50 dark:hover:bg-${cfg.accent}-900/20 hover:border-${cfg.accent}-200 group/item no-underline">
                                    <div class="w-8 h-8 rounded-lg bg-${cfg.accent}-100 dark:bg-${cfg.accent}-900/50 flex items-center justify-center text-${cfg.accent}-600 dark:text-${cfg.accent}-400 group-hover/item:bg-${cfg.accent}-600 group-hover/item:text-white transition-all"><i data-lucide="${cfg.icon}" class="w-4 h-4"></i></div>
                                    <span class="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover/item:text-${cfg.accent}-700 transition-colors">${esc(topic.title)}</span>
                                </a>
                            `).join('')}
                        </div>
                    </section>
                `).join('')}
            </div>
        `;
    }

    function renderCode(code, lang, output) {
        if (!code) return '';
        return `
            <div class="my-6">
                <pre class="language-${lang}"><code>${esc(code)}</code></pre>
                ${output ? `<div class="mt-3 rounded-lg bg-slate-50 border border-slate-100 p-4"><div class="text-[10px] uppercase tracking-widest text-slate-400 mb-2 font-bold">Output</div><pre class="!m-0 !bg-transparent !p-0"><code>${esc(output)}</code></pre></div>` : ''}
            </div>
        `;
    }

    function renderTable(rows) {
        if (!Array.isArray(rows) || !rows.length) return '';
        const headers = Object.keys(rows[0]);
        return `<div class="overflow-x-auto my-6 rounded-xl border border-slate-200"><table class="w-full text-sm"><thead class="bg-slate-50"><tr>${headers.map((h) => `<th class="px-4 py-3 text-left font-bold text-slate-700 uppercase text-xs">${esc(h.replace(/_/g, ' '))}</th>`).join('')}</tr></thead><tbody>${rows.map((row) => `<tr class="border-t border-slate-100">${headers.map((h) => `<td class="px-4 py-3 align-top text-slate-600"><pre class="whitespace-pre-wrap font-sans text-sm">${esc(row[h])}</pre></td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    }

    function renderList(title, items, color) {
        if (!Array.isArray(items) || !items.length) return '';
        return `<div class="my-6 rounded-xl border border-${color}-100 bg-${color}-50/50 p-5 shadow-sm transition-all hover:shadow-md"><h3 class="font-bold text-${color}-800 mb-3 flex items-center gap-2"><span class="w-1.5 h-4 bg-${color}-500 rounded-full"></span>${esc(title)}</h3><ul class="space-y-2.5">${items.map((item) => `<li class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed flex items-start gap-2.5"><span class="w-1.5 h-1.5 bg-${color}-400 rounded-full mt-2 flex-shrink-0"></span><span>${esc(typeof item === 'string' ? item : JSON.stringify(item))}</span></li>`).join('')}</ul></div>`;
    }

    function renderNote(content, type = 'blue') {
        if (!content) return '';
        const icons = { blue: 'info', amber: 'alert-triangle', rose: 'alert-circle', emerald: 'check-circle' };
        return `<div class="my-8 rounded-2xl border-l-4 border-${type}-500 bg-${type}-50/30 dark:bg-${type}-900/10 p-6 flex gap-4"><div class="text-${type}-500 flex-shrink-0"><i data-lucide="${icons[type] || 'info'}" class="w-6 h-6"></i></div><div class="text-sm leading-relaxed text-slate-700 dark:text-slate-300"><strong class="block text-slate-900 dark:text-white mb-1 uppercase tracking-wider text-[10px] font-black font-display text-${type}-600">${type === 'blue' ? 'Pro Tip' : type === 'amber' ? 'Warning' : 'Note'}</strong>${esc(content)}</div></div>`;
    }

    function renderDiagram(code) {
        if (!code) return '';
        return `<div class="my-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 shadow-sm overflow-hidden"><div class="mermaid flex justify-center">${code}</div></div>`;
    }

    function renderComponents(components, cfg) {
        if (!Array.isArray(components) || !components.length) return '';
        return `
            <div class="grid grid-cols-1 gap-6 my-10">
                ${components.map(c => `
                    <div class="group relative bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 transition-all hover:border-${cfg.accent}-300 hover:shadow-xl hover:shadow-${cfg.accent}-500/5">
                        <div class="absolute top-0 right-0 p-4 opacity-5 text-slate-400 group-hover:opacity-20 transition-opacity"><i data-lucide="${cfg.icon}" class="w-12 h-12"></i></div>
                        <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3 font-display flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-${cfg.accent}-500"></span>
                            ${esc(c.component || c.title || c.name)}
                        </h3>
                        <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed mb-4">${esc(c.description || c.explanation)}</p>
                        ${c.examples ? `<div class="mt-4"><div class="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">Examples</div><div class="flex flex-wrap gap-2">${(Array.isArray(c.examples) ? c.examples : [c.examples]).map(ex => `<span class="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 text-[11px] font-bold rounded-md border border-slate-200/50 dark:border-slate-700/50">${esc(typeof ex === 'string' ? ex : JSON.stringify(ex))}</span>`).join('')}</div></div>` : ''}
                        ${c.use_case ? `<div class="mt-4"><div class="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">Use Case</div><p class="text-xs text-${cfg.accent}-600 dark:text-${cfg.accent}-400 font-semibold italic">"${esc(c.use_case)}"</p></div>` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }

    function renderSqlTopic(topic, cfg) {
        return `
            ${topic.explanation ? `<div class="text-xl text-slate-600 dark:text-slate-400 mb-8 leading-relaxed font-medium prose prose-slate dark:prose-invert max-w-none">${md(topic.explanation)}</div>` : ''}
            ${topic.description ? `<div class="text-xl text-slate-600 dark:text-slate-400 mb-8 leading-relaxed font-medium prose prose-slate dark:prose-invert max-w-none">${md(topic.description)}</div>` : ''}
            
            ${renderDiagram(topic.diagram)}
            ${renderNote(topic.pro_tip, 'blue')}
            ${renderNote(topic.warning, 'amber')}
            
            ${renderTable(topic.comparison_table)}
            ${renderTable(topic.cheatsheet)}
            ${renderComponents(topic.components || topic.architectures, cfg)}
            
            ${(topic.examples || []).map((example) => `
                <section class="mb-12 group">
                    <div class="flex items-center gap-3 mb-4">
                        <span class="w-8 h-[2px] bg-${cfg.accent}-500/30 group-hover:w-12 transition-all"></span>
                        <h2 class="text-2xl font-bold text-slate-900 dark:text-white font-display">${esc(example.description || example.title || 'Example')}</h2>
                    </div>
                    ${example.explanation ? `<div class="text-slate-600 dark:text-slate-400 mb-4 text-sm leading-relaxed prose prose-sm dark:prose-invert max-w-none">${md(example.explanation)}</div>` : ''}
                    ${renderCode(example.sql || example.code, cfg.lang, example.output)}
                </section>
            `).join('')}
            
            ${topic.example ? `<section class="mb-10"><h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">${esc(topic.example.description || 'Example')}</h2>${topic.example.sql || topic.example.code ? renderCode(topic.example.sql || topic.example.code, cfg.lang, topic.example.output) : `<pre class="rounded-xl bg-slate-50 p-4 overflow-x-auto"><code>${esc(JSON.stringify(topic.example, null, 2))}</code></pre>`}</section>` : ''}
            ${Array.isArray(topic.questions) ? renderQuestions(topic.questions) : ''}
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
                ${renderList('Pros', topic.pros || topic.advantages, 'emerald')}
                ${renderList('Cons', topic.cons || topic.limitations, 'rose')}
            </div>
            ${renderList('Best Practices & Tips', topic.tips || topic.best_practices, 'blue')}
            ${renderList('Common Issues & Pitfalls', topic.common_issues, 'amber')}
        `;
    }

    function renderQuestions(questions) {
        return `<section class="space-y-3">${questions.map((q, index) => `<details class="group rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/40 p-4"><summary class="cursor-pointer list-none flex items-start gap-3"><span class="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-black flex-shrink-0">${esc(q.q_no || q.id || index + 1)}</span><span class="flex-1 text-sm font-bold text-slate-800 dark:text-slate-100">${esc(q.question || q.prompt)}</span></summary><p class="text-sm text-slate-600 dark:text-slate-300 leading-7 mt-4 pl-11">${esc(q.answer || q.solution || q.sql || '')}</p>${q.sql ? renderCode(q.sql, 'sql', q.output) : ''}</details>`).join('')}</section>`;
    }

    function renderShellTopic(topic, cfg) {
        const subtopics = topic.subtopics || [];
        return `
            ${(topic.description || topic.explanation) ? `<div class="text-xl text-slate-600 dark:text-slate-400 mb-8 leading-relaxed font-medium prose prose-slate dark:prose-invert max-w-none">${md(topic.description || topic.explanation)}</div>` : ''}
            
            ${renderDiagram(topic.diagram)}
            ${renderNote(topic.pro_tip, 'blue')}
            ${renderComponents(topic.components || topic.services || topic.features || topic.concepts, cfg)}
            ${renderTable(topic.comparison_table)}
            
            ${subtopics.map((subtopic) => `
                <section class="mb-16 group">
                    <h2 class="text-3xl font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-3 font-display transition-transform group-hover:translate-x-2"><span class="w-1.5 h-8 bg-${cfg.accent}-500 rounded-full"></span>${esc(subtopic.name || subtopic.title)}</h2>
                    ${(subtopic.explanation || subtopic.content) ? `<div class="text-slate-600 dark:text-slate-400 mb-8 leading-relaxed prose prose-slate dark:prose-invert max-w-none">${md(subtopic.explanation || subtopic.content)}</div>` : ''}
                    ${renderDiagram(subtopic.diagram)}
                    ${renderComponents(subtopic.components, cfg)}
                    ${(subtopic.examples || []).map((example) => `
                        <div class="mb-8">
                            <h3 class="text-xl font-bold text-slate-800 dark:text-slate-200 mb-4 flex items-center gap-2"><i data-lucide="code-2" class="w-5 h-5 text-${cfg.accent}-500"></i> ${esc(example.title || 'Example')}</h3>
                            ${example.explanation ? `<div class="text-sm text-slate-500 mb-3 prose prose-sm dark:prose-invert max-w-none">${md(example.explanation)}</div>` : ''}
                            ${renderCode(example.code, cfg.lang, example.output)}
                        </div>
                    `).join('')}
                </section>
            `).join('')}
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
                ${renderList('Pros', topic.pros || topic.advantages || topic.key_benefits, 'emerald')}
                ${renderList('Cons', topic.cons || topic.limitations, 'rose')}
            </div>
            ${renderList('Best Practices & Tips', topic.tips || topic.best_practices, 'blue')}
        `;
    }

    function renderTopic(main, type, raw, slug) {
        const cfg = CONFIG[type];
        const sections = normalize(type, raw);
        const topics = flatten(sections);
        const canonicalSlug = (SLUG_ALIASES[type] && SLUG_ALIASES[type][slug]) || slug;
        const topic = topics.find((item) => item.slug === canonicalSlug);
        if (!topic) throw new Error(`Topic not found in JSON: ${slug}`);
        const index = topics.indexOf(topic);
        const previous = topics[index - 1];
        const next = topics[index + 1];

        document.title = `${topic.title} - ${cfg.label} - Data Cake`;
        const navTitle = document.querySelector('#ds-nav .hidden.md\\:flex span.text-sm');
        if (navTitle) navTitle.textContent = topic.title;

        main.innerHTML = `
            <a href="${cfg.indexHref}#section-${esc(topic.section.id)}" class="inline-flex items-center gap-2 text-sm font-medium text-${cfg.accent}-600 dark:text-${cfg.accent}-400 hover:text-${cfg.accent}-700 dark:hover:text-${cfg.accent}-300 transition-colors mb-6 group no-underline"><i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>Back to ${esc(cfg.label)}</a>
            <header class="mb-12">
                <div class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-4 flex items-center gap-2"><span class="w-8 h-[1px] bg-slate-300"></span>Section ${esc(topic.section.id)}: ${esc(topic.section.title)}</div>
                <h1 class="text-4xl md:text-6xl font-black text-slate-900 dark:text-white leading-tight tracking-tighter font-display">${esc(topic.title)}</h1>
            </header>
            <article class="prose dark:prose-invert max-w-none pb-20">
                ${type === 'sql' ? renderSqlTopic(topic, cfg) : renderShellTopic(topic, cfg)}
                <div class="mt-16 flex flex-col sm:flex-row justify-between gap-4 border-t border-slate-200 dark:border-slate-800 pt-8">
                    ${previous ? `<a href="${esc(previous.slug)}.html" class="no-underline text-sm font-bold text-${cfg.accent}-600 hover:text-${cfg.accent}-700"><i data-lucide="arrow-left" class="inline w-4 h-4 mr-1"></i>${esc(previous.title)}</a>` : '<span></span>'}
                    ${next ? `<a href="${esc(next.slug)}.html" class="no-underline text-sm font-bold text-${cfg.accent}-600 hover:text-${cfg.accent}-700 sm:text-right">${esc(next.title)}<i data-lucide="arrow-right" class="inline w-4 h-4 ml-1"></i></a>` : '<span></span>'}
                </div>
            </article>
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

    function detectType() {
        const root = document.querySelector('[data-guide-type]');
        if (root) return root.dataset.guideType;
        const match = location.pathname.match(/\/(sql|bash|powershell|airflow|spark|flink|kafka|dbt|pandas|numpy|regex|aws)\//);
        return match && match[1];
    }

    document.addEventListener('DOMContentLoaded', async () => {
        const type = detectType();
        if (!type || !CONFIG[type]) return;
        const cfg = CONFIG[type];
        const root = document.querySelector(`[data-guide-type="${type}"]`);
        const main = root || document.querySelector('#ds-main-content main');
        if (!main) return;

        try {
            const path = root ? (root.dataset.guidePath || cfg.indexPath) : cfg.topicPath;
            const raw = await loadJson(path);
            if (root) renderIndex(root, type, raw);
            else renderTopic(main, type, raw, location.pathname.split('/').pop().replace(/\.html$/, ''));
            populateToc(main);
            if (window.Prism) window.Prism.highlightAll();
            if (window.lucide) window.lucide.createIcons();
            if (window.mermaid) {
                window.mermaid.initialize({ startOnLoad: true, theme: document.documentElement.classList.contains('dark') ? 'dark' : 'default' });
                window.mermaid.contentLoaded();
            }
        } catch (error) {
            main.innerHTML = `<div class="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-rose-700"><h2 class="font-display font-bold text-xl mb-2">Unable to load guide</h2><p class="text-sm">${esc(error.message)}</p></div>`;
        }
    });
})();
