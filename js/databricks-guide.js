(function () {
    function escapeHtml(value) {
        return String(value ?? '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function sectionHref(section, basePath) {
        return `${basePath || 'databricks'}/${section.slug}.html`;
    }

    function ensurePrismAssets() {
        if (!document.getElementById('prism-theme-light')) {
            const light = document.createElement('link');
            light.id = 'prism-theme-light';
            light.rel = 'stylesheet';
            light.href = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css';
            document.head.appendChild(light);
        }

        if (!window.Prism && !document.querySelector('script[data-dbx-prism]')) {
            const prism = document.createElement('script');
            prism.src = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js';
            prism.dataset.dbxPrism = '1';
            prism.onload = () => {
                const sql = document.createElement('script');
                sql.src = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js';
                const python = document.createElement('script');
                python.src = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js';
                python.onload = () => {
                    const bash = document.createElement('script');
                    bash.src = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js';
                    bash.onload = () => window.Prism && window.Prism.highlightAll();
                    document.body.appendChild(bash);
                };
                document.body.appendChild(python);
            };
            document.body.appendChild(prism);
        } else if (window.Prism) {
            window.Prism.highlightAll();
        }
    }

    function codeLanguage(code) {
        const value = String(code || '').trim().toLowerCase();
        if (/^(select|create|alter|merge|copy|grant|describe|optimize|vacuum|restore)\b/.test(value)) return 'sql';
        if (value.includes('spark.') || value.includes('dbutils.') || value.includes('import ') || value.includes('def ') || value.includes('@dlt')) return 'python';
        if (value.includes('databricks bundle') || value.includes('terraform') || value.startsWith('%') || value.startsWith('POST') || value.startsWith('GET')) return 'bash';
        return 'sql';
    }

    function renderCodeBlock(code, title) {
        const lang = codeLanguage(code);
        const langIcon = { sql: 'database', python: 'code-2', bash: 'terminal' }[lang] || 'file-code';
        const langColor = { sql: 'text-blue-600 bg-blue-50', python: 'text-amber-600 bg-amber-50', bash: 'text-emerald-600 bg-emerald-50' }[lang] || 'text-slate-600 bg-slate-50';
        return `
            <div class="my-6 group">
                <div class="relative rounded-xl overflow-hidden bg-white border border-slate-200 shadow-sm transition-all hover:shadow-md">
                    <div class="flex items-center justify-between px-4 py-2.5 bg-slate-50/80 border-b border-slate-200">
                        <div class="flex items-center gap-2">
                            <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md ${langColor} text-[10px] font-bold uppercase tracking-wide">
                                <i data-lucide="${langIcon}" class="w-3 h-3"></i>${lang}
                            </span>
                            ${title ? `<span class="text-xs font-semibold text-slate-500">${escapeHtml(title)}</span>` : ''}
                        </div>
                        <button class="copy-btn text-xs text-slate-400 hover:text-slate-600 transition-colors flex items-center gap-1" onclick="copyCode(this)">
                            <i data-lucide="copy" class="w-3 h-3"></i>Copy
                        </button>
                    </div>
                    <div class="relative">
                        <pre class="language-${lang} !m-0 !rounded-t-none"><code>${escapeHtml(code)}</code></pre>
                    </div>
                </div>
            </div>
        `;
    }

    function renderExamples(examples) {
        return (examples || []).map((example, idx) => `
            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 p-5 shadow-sm hover:shadow-md transition-all">
                <div class="flex items-start gap-3 mb-3">
                    <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 text-white flex items-center justify-center flex-shrink-0 text-sm font-black">${idx + 1}</div>
                    <div>
                        <h4 class="font-bold text-slate-900 dark:text-white text-base">${escapeHtml(example.title)}</h4>
                        <p class="text-sm text-slate-600 dark:text-slate-300 leading-relaxed mt-1">${escapeHtml(example.explanation)}</p>
                    </div>
                </div>
                ${renderCodeBlock(example.code, '')}
            </div>
        `).join('');
    }

    function renderDrawbacks(items) {
        return (items || []).map((item) => `
            <div class="rounded-xl border border-amber-200 dark:border-amber-900/70 bg-gradient-to-r from-amber-50/70 to-orange-50/30 dark:from-amber-950/20 dark:to-transparent p-5">
                <div class="flex items-start gap-3">
                    <div class="w-8 h-8 rounded-lg bg-amber-100 dark:bg-amber-900/60 text-amber-700 dark:text-amber-300 flex items-center justify-center flex-shrink-0">
                        <i data-lucide="alert-triangle" class="w-4 h-4"></i>
                    </div>
                    <div>
                        <p class="text-sm font-bold text-amber-800 dark:text-amber-300 mb-1">Challenge</p>
                        <p class="text-sm text-slate-700 dark:text-slate-300">${escapeHtml(item.drawback)}</p>
                    </div>
                </div>
                <div class="mt-3 pl-11">
                    <div class="flex items-start gap-3">
                        <div class="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300 flex items-center justify-center flex-shrink-0">
                            <i data-lucide="check-circle" class="w-4 h-4"></i>
                        </div>
                        <div>
                            <p class="text-sm font-bold text-emerald-800 dark:text-emerald-300 mb-1">Solution</p>
                            <p class="text-sm text-slate-700 dark:text-slate-300">${escapeHtml(item.solution)}</p>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    function renderInterviewQuestions(questions) {
        const categories = [...new Set(questions.map(q => q.category))];
        const catColors = {
            'Conceptual': 'from-blue-500 to-indigo-600',
            'Architecture': 'from-violet-500 to-purple-600',
            'Comparison': 'from-cyan-500 to-blue-600',
            'Workspace': 'from-emerald-500 to-teal-600',
            'Clusters': 'from-orange-500 to-red-600',
            'DBFS': 'from-amber-500 to-yellow-600',
            'Delta Lake': 'from-blue-600 to-indigo-700',
            'Unity Catalog': 'from-rose-500 to-pink-600',
            'Databricks SQL': 'from-sky-500 to-blue-600',
            'DLT': 'from-purple-500 to-violet-600',
            'Workflows': 'from-teal-500 to-emerald-600',
            'CI/CD': 'from-green-500 to-lime-600',
            'MLflow': 'from-fuchsia-500 to-pink-600',
            'ML/AI': 'from-violet-500 to-fuchsia-600',
            'Performance': 'from-amber-500 to-orange-600',
            'Security': 'from-red-500 to-rose-600',
            'AWS': 'from-orange-400 to-amber-500',
            'Azure': 'from-blue-400 to-cyan-500',
            'Ingestion': 'from-green-500 to-emerald-600',
            'Administration': 'from-slate-500 to-gray-600',
            'Scenario': 'from-indigo-500 to-violet-600',
            'Integrations': 'from-pink-500 to-rose-600',
        };
        const catIcons = {
            'Conceptual': 'lightbulb', 'Architecture': 'cpu', 'Comparison': 'scale',
            'Workspace': 'layout-grid', 'Clusters': 'server', 'DBFS': 'folder',
            'Delta Lake': 'database', 'Unity Catalog': 'shield-check',
            'Databricks SQL': 'table-2', 'DLT': 'workflow', 'Workflows': 'git-branch',
            'CI/CD': 'rocket', 'MLflow': 'line-chart', 'ML/AI': 'brain-circuit',
            'Performance': 'gauge', 'Security': 'lock', 'AWS': 'cloud',
            'Azure': 'cloud-cog', 'Ingestion': 'download-cloud',
            'Administration': 'settings', 'Scenario': 'case', 'Integrations': 'plug',
        };

        const byCategory = {};
        questions.forEach(q => { if (!byCategory[q.category]) byCategory[q.category] = []; byCategory[q.category].push(q); });

        return `
            <section class="space-y-6">
                <div class="flex items-center gap-4 mb-8">
                    <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 text-white flex items-center justify-center">
                        <i data-lucide="award" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <h2 class="font-display font-bold text-2xl text-slate-900 dark:text-white">Interview Preparation</h2>
                        <p class="text-sm text-slate-500">${questions.length} questions across ${categories.length} topics</p>
                    </div>
                </div>
                <div class="space-y-8">
                    ${categories.map(cat => `
                        <div>
                            <div class="flex items-center gap-3 mb-4">
                                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-gradient-to-r ${catColors[cat] || 'from-slate-500 to-gray-600'} text-white text-xs font-bold">
                                    <i data-lucide="${catIcons[cat] || 'book-open'}" class="w-3 h-3"></i>${escapeHtml(cat)}
                                </span>
                                <span class="text-xs font-semibold text-slate-400">${byCategory[cat].length} questions</span>
                            </div>
                            <div class="space-y-3">
                                ${byCategory[cat].map((item) => `
                                    <details class="group rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/40 p-4 hover:shadow-sm transition-all">
                                        <summary class="cursor-pointer list-none flex items-start gap-3">
                                            <span class="w-8 h-8 rounded-lg bg-gradient-to-br ${catColors[cat] || 'from-slate-500 to-gray-600'} text-white flex items-center justify-center text-xs font-black flex-shrink-0">${item.id}</span>
                                            <span class="flex-1"><span class="block text-sm font-bold text-slate-800 dark:text-slate-100">${escapeHtml(item.question)}</span></span>
                                            <i data-lucide="chevron-down" class="w-4 h-4 text-slate-400 group-open:rotate-180 transition-transform mt-1"></i>
                                        </summary>
                                        <div class="mt-4 pl-11">
                                            <div class="flex items-start gap-2">
                                                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300 text-[10px] font-bold uppercase">Answer</span>
                                            </div>
                                            <p class="text-sm text-slate-600 dark:text-slate-300 leading-7 mt-2">${escapeHtml(item.answer)}</p>
                                        </div>
                                    </details>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </section>
        `;
    }

    function renderTopicPills(topics) {
        const icons = ['book-open', 'database', 'server', 'shield', 'workflow', 'zap', 'brain', 'code', 'lock', 'cloud', 'git-branch', 'table-2'];
        return (topics || []).map((topic, i) => `
            <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-cyan-50 dark:bg-cyan-950/30 border border-cyan-100 dark:border-cyan-900 text-xs font-semibold text-cyan-700 dark:text-cyan-300 hover:bg-cyan-100 dark:hover:bg-cyan-900/50 transition-colors cursor-default">
                <i data-lucide="${icons[i % icons.length]}" class="w-3 h-3"></i>${escapeHtml(topic)}
            </span>
        `).join('');
    }

    function iconForTopic(topic) {
        const text = topic.toLowerCase();
        if (/what is|overview/.test(text)) return 'book-open';
        if (/architecture|control plane|data plane/.test(text)) return 'cpu';
        if (/cluster|runtime|photon|node|autoscaling/.test(text)) return 'server';
        if (/delta|merge|vacuum|optimize|zorder|time travel|transaction/.test(text)) return 'database';
        if (/unity catalog|metastore|privilege|permission|lineage|audit/.test(text)) return 'shield-check';
        if (/sql|warehouse|dashboard|query|alert|caching/.test(text)) return 'table-2';
        if (/dlt|live tables|expect|apply changes/.test(text)) return 'workflow';
        if (/job|workflow|task|schedule|dag|airflow/.test(text)) return 'git-branch';
        if (/git|ci\/cd|bundle|terraform|deployment/.test(text)) return 'rocket';
        if (/mlflow|model|feature|automl|vector|llm|mosaic|serving/.test(text)) return 'brain-circuit';
        if (/performance|partition|skew|broadcast|shuffle|cache|predicate/.test(text)) return 'gauge';
        if (/security|network|identity|secret|encryption|private|compliance/.test(text)) return 'lock';
        if (/aws|s3|iam|vpc|redshift|kinesis/.test(text)) return 'cloud';
        if (/azure|adls|vnet|key vault|synapse|data factory/.test(text)) return 'cloud-cog';
        if (/ingestion|auto loader|cloudfiles|kafka|copy into|streaming/.test(text)) return 'download-cloud';
        if (/administration|user|group|cost|usage|support/.test(text)) return 'settings';
        if (/medallion|cdc|scd|data mesh|federated|sharing/.test(text)) return 'layers';
        if (/dbt|tableau|power bi|fivetran|airbyte|great expectations/.test(text)) return 'plug';
        if (/interview|question/.test(text)) return 'award';
        return 'box';
    }

    function topicDetail(topic, section) {
        const text = topic.toLowerCase();
        const sectionTitle = section.title.toLowerCase();
        let means = `${topic} is an important part of ${section.title}. Understanding this concept will help you work more effectively with Databricks in real projects.`;
        let matters = `This knowledge is essential for designing, debugging, securing, and operating Databricks workloads in production environments.`;
        let use = `Start by identifying the workload type, data sensitivity, runtime requirements, and operational ownership, then apply the appropriate Databricks features.`;
        let tip = `Try explaining this concept to a colleague in simple terms. If you can teach it, you truly understand it.`;

        if (text.includes('what is')) {
            means = `${topic.replace(/^what is\s+/i, '')} is the core definition you should master before diving deeper into Databricks.`;
            matters = `Clear definitions help in interviews, architecture reviews, and team discussions.`;
            use = `Explain it with three parts: the problem it solves, the Databricks component involved, and a realistic example.`;
            tip = `Use the Feynman technique: explain it simply, identify gaps, refine your understanding.`;
        } else if (text.includes('architecture') || text.includes('control plane') || text.includes('data plane')) {
            means = `${topic} describes how Databricks organizes user services, metadata, orchestration, compute, networking, and storage.`;
            matters = `Architecture knowledge is critical for security reviews, private networking, cost planning, and troubleshooting.`;
            use = `Draw the flow from users to control plane, then to compute, then to cloud storage governed by Unity Catalog.`;
            tip = `Sketch the architecture from memory, then compare with official documentation to identify gaps.`;
        } else if (text.includes('cluster') || text.includes('runtime') || text.includes('photon') || text.includes('node') || text.includes('autoscaling')) {
            means = `${topic} controls how Databricks compute is created, optimized, scaled, isolated, and billed.`;
            matters = `Most performance and cost issues stem from compute choices: wrong runtime, wrong nodes, no auto-termination, or mixed workloads.`;
            use = `Use job clusters for production, all-purpose for exploration, SQL warehouses for BI, and policies to enforce defaults.`;
            tip = `Always enable auto-termination and use the smallest cluster that meets your SLA requirements.`;
        } else if (text.includes('delta') || text.includes('merge') || text.includes('vacuum') || text.includes('optimize') || text.includes('zorder') || text.includes('time travel') || text.includes('transaction')) {
            means = `${topic} is part of Delta Lake's reliability and performance layer on top of cloud storage.`;
            matters = `Delta prevents corrupted data, enables safe upserts, supports audit/recovery, and makes lakehouse queries faster.`;
            use = `Use MERGE for CDC, DESCRIBE HISTORY for audit, RESTORE for recovery, OPTIMIZE for compaction, and VACUUM carefully.`;
            tip = `Practice running DESCRIBE HISTORY on a Delta table to see how the transaction log records every operation.`;
        } else if (text.includes('unity catalog') || text.includes('metastore') || text.includes('privilege') || text.includes('permission') || text.includes('lineage') || text.includes('audit') || text.includes('external location') || text.includes('storage credential')) {
            means = `${topic} belongs to Databricks' governance model for controlling data, files, models, lineage, and access.`;
            matters = `Governance decides who sees data, where it's accessed, how access is audited, and how sensitive datasets are protected.`;
            use = `Model access with groups, catalogs, schemas, external locations, storage credentials, grants, row filters, and column masks.`;
            tip = `Use GRANT commands in a test catalog to practice the permission hierarchy before applying to production.`;
        } else if (text.includes('sql') || text.includes('warehouse') || text.includes('dashboard') || text.includes('query') || text.includes('alert') || text.includes('caching')) {
            means = `${topic} supports analytics and BI workloads on governed lakehouse data.`;
            matters = `Databricks SQL is how analysts consume curated Delta tables without managing Spark notebooks.`;
            use = `Serve Gold tables through SQL warehouses, inspect query profiles, enable auto-stop, and use alerts for checks.`;
            tip = `Use the Query Profile to identify bottlenecks before optimizing your SQL queries.`;
        } else if (text.includes('dlt') || text.includes('live tables') || text.includes('expect') || text.includes('apply changes')) {
            means = `${topic} is part of Delta Live Tables, Databricks' declarative framework for reliable pipelines.`;
            matters = `DLT reduces custom orchestration code and makes data quality, dependencies, and lineage easier to manage.`;
            use = `Define tables with decorators, add expectations for quality, choose triggered or continuous mode, and use APPLY CHANGES for CDC.`;
            tip = `Start with simple DLT pipelines using expectations, then gradually add streaming and CDC patterns.`;
        } else if (text.includes('job') || text.includes('workflow') || text.includes('task') || text.includes('schedule') || text.includes('dag') || text.includes('airflow')) {
            means = `${topic} explains how production Databricks workloads are orchestrated, parameterized, retried, and monitored.`;
            matters = `Reliable jobs need clear dependencies, isolated compute, observable runs, retries, alerts, and safe rerun behavior.`;
            use = `Break workflows into small tasks, pass parameters explicitly, prefer job clusters, configure retries/alerts, and use repair runs.`;
            tip = `Design each task to be idempotent so you can safely rerun after failures.`;
        } else if (text.includes('git') || text.includes('ci/cd') || text.includes('bundle') || text.includes('terraform') || text.includes('deployment')) {
            means = `${topic} is about making Databricks changes repeatable, reviewable, and promotable across environments.`;
            matters = `Without CI/CD, production notebooks, jobs, permissions, and clusters drift from source control and become hard to audit.`;
            use = `Use Git branches, pull requests, Databricks Asset Bundles, service principals, Terraform, and promotion gates.`;
            tip = `Practice deploying a simple job through DABs in a dev workspace before applying to production.`;
        } else if (text.includes('mlflow') || text.includes('model') || text.includes('feature') || text.includes('automl') || text.includes('vector') || text.includes('llm') || text.includes('mosaic') || text.includes('serving')) {
            means = `${topic} belongs to Databricks' ML and AI workflow, from features and experiments to model governance and serving.`;
            matters = `ML systems need reproducibility, feature consistency, model versioning, scalable inference, and governance.`;
            use = `Track experiments with MLflow, register models in Unity Catalog, use Feature Store, and deploy with Model Serving.`;
            tip = `Log the training data version alongside every experiment run for full reproducibility.`;
        } else if (text.includes('performance') || text.includes('partition') || text.includes('skew') || text.includes('broadcast') || text.includes('shuffle') || text.includes('cache') || text.includes('predicate')) {
            means = `${topic} is a performance optimization concept focused on reducing reads, shuffles, spills, or wasted compute.`;
            matters = `Performance tuning improves reliability and cost because faster jobs use fewer DBUs and are less likely to miss SLAs.`;
            use = `Check Spark UI or query profiles, reduce scanned data, fix small files, choose better joins, handle skew, and size clusters based on evidence.`;
            tip = `Always benchmark before and after optimization to measure actual impact.`;
        } else if (text.includes('security') || text.includes('network') || text.includes('identity') || text.includes('secret') || text.includes('encryption') || text.includes('private') || text.includes('compliance')) {
            means = `${topic} is part of Databricks' security posture across identity, data access, network boundaries, encryption, and auditability.`;
            matters = `Security mistakes can expose sensitive data, allow uncontrolled egress, or make compliance audits fail.`;
            use = `Use least privilege, Unity Catalog, private networking, secret scopes, managed identities, audit logs, and cluster policies.`;
            tip = `Never hardcode secrets. Always use secret scopes with proper output redaction.`;
        } else if (text.includes('aws') || text.includes('s3') || text.includes('iam') || text.includes('vpc') || text.includes('redshift') || text.includes('kinesis')) {
            means = `${topic} explains how Databricks integrates with AWS networking, identity, storage, streaming, and warehouse services.`;
            matters = `Correct AWS integration avoids broken S3 access, insecure IAM roles, networking failures, and expensive data movement.`;
            use = `Use Unity Catalog storage credentials, external locations, least-privilege IAM roles, PrivateLink where needed, and validated VPC routing.`;
            tip = `Test IAM roles with minimal permissions first, then gradually add required actions.`;
        } else if (text.includes('azure') || text.includes('adls') || text.includes('vnet') || text.includes('key vault') || text.includes('synapse') || text.includes('data factory')) {
            means = `${topic} explains how Azure Databricks integrates with Microsoft identity, networking, storage, orchestration, monitoring, and DevOps tools.`;
            matters = `Azure deployments often depend on correct Entra ID groups, managed identities, ADLS permissions, VNets, and private endpoints.`;
            use = `Use managed identities, ADLS external locations, Azure Key Vault-backed secrets, Data Factory orchestration, Azure DevOps CI/CD, and Azure Monitor integration.`;
            tip = `Use managed identities over service principals when possible for simpler credential management.`;
        } else if (text.includes('ingestion') || text.includes('auto loader') || text.includes('cloudfiles') || text.includes('kafka') || text.includes('copy into') || text.includes('streaming')) {
            means = `${topic} is about bringing data into the lakehouse reliably from files, streams, databases, or partner tools.`;
            matters = `Ingestion quality affects every downstream table; missed files, duplicates, schema drift, and bad checkpoints create hard-to-debug issues.`;
            use = `Use Auto Loader for scalable file ingestion, COPY INTO for simple SQL loads, Structured Streaming for events, checkpoints for progress, and schema controls for drift.`;
            tip = `Use file notification mode for high-scale ingestion to avoid expensive directory listings.`;
        } else if (text.includes('administration') || text.includes('user') || text.includes('group') || text.includes('cost') || text.includes('usage') || text.includes('support')) {
            means = `${topic} is an admin responsibility for keeping Databricks secure, organized, supportable, and cost-controlled.`;
            matters = `Good administration prevents workspace sprawl, over-permissioned users, untagged spend, uncontrolled compute, and weak audit trails.`;
            use = `Automate users/groups, use service principals for jobs, enforce cluster policies, monitor system tables, and tag resources for chargeback.`;
            tip = `Set up billing alerts and usage dashboards early to catch cost anomalies before they become expensive.`;
        } else if (text.includes('medallion') || text.includes('cdc') || text.includes('scd') || text.includes('data mesh') || text.includes('federated') || text.includes('sharing')) {
            means = `${topic} is a real-world architecture pattern for organizing data products and pipelines on Databricks.`;
            matters = `Patterns help teams build repeatable solutions instead of custom one-off pipelines for every source and consumer.`;
            use = `Choose the pattern based on latency, governance, history tracking, domain ownership, and whether data should be copied, shared, or queried in place.`;
            tip = `Start with a simple medallion architecture before adopting more complex patterns like data mesh.`;
        } else if (text.includes('dbt') || text.includes('tableau') || text.includes('power bi') || text.includes('fivetran') || text.includes('airbyte') || text.includes('great expectations')) {
            means = `${topic} connects Databricks with a specialized tool in the data ecosystem.`;
            matters = `Integrations let teams keep best-of-breed tools while using Databricks as the governed compute and lakehouse layer.`;
            use = `Define which tool owns ingestion, transformation, quality, orchestration, serving, or infrastructure so responsibilities do not overlap.`;
            tip = `Use dbt for SQL transformations on Databricks SQL, and DLT for Spark-based pipelines.`;
        } else if (/interview|question/.test(text)) {
            means = `${topic} is a category of questions interviewers use to test whether you can apply Databricks concepts in real scenarios.`;
            matters = `Strong answers combine definitions, tradeoffs, production experience, and a short example.`;
            use = `Answer with this structure: define the concept, explain when to use it, mention a drawback, and give the practical solution.`;
            tip = `Practice answering out loud, as if explaining to an interviewer. Record yourself to improve delivery.`;
        }

        return { means, matters, use, tip };
    }

    function renderTopicDetails(section) {
        return (section.topics || []).map((topic, index) => {
            const detail = topicDetail(topic, section);
            const icon = iconForTopic(topic);
            return `
                <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 p-5 shadow-sm hover:shadow-md transition-all">
                    <div class="flex items-start gap-4">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 text-white flex items-center justify-center flex-shrink-0">
                            <i data-lucide="${escapeHtml(icon)}" class="w-5 h-5"></i>
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="text-[10px] font-black tracking-widest uppercase text-cyan-600 dark:text-cyan-400">Topic ${String(index + 1).padStart(2, '0')}</span>
                            </div>
                            <h3 class="font-display font-bold text-lg text-slate-900 dark:text-white mb-3">${escapeHtml(topic)}</h3>
                            <div class="space-y-3">
                                <div class="flex items-start gap-2">
                                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-[10px] font-bold uppercase mt-0.5">Meaning</span>
                                    <p class="text-sm text-slate-600 dark:text-slate-300 leading-7">${escapeHtml(detail.means)}</p>
                                </div>
                                <div class="flex items-start gap-2">
                                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300 text-[10px] font-bold uppercase mt-0.5">Why It Matters</span>
                                    <p class="text-sm text-slate-600 dark:text-slate-300 leading-7">${escapeHtml(detail.matters)}</p>
                                </div>
                                <div class="flex items-start gap-2">
                                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-violet-100 dark:bg-violet-900/50 text-violet-700 dark:text-violet-300 text-[10px] font-bold uppercase mt-0.5">How To Use</span>
                                    <p class="text-sm text-slate-600 dark:text-slate-300 leading-7">${escapeHtml(detail.use)}</p>
                                </div>
                                <div class="flex items-start gap-2 bg-amber-50/50 dark:bg-amber-950/20 rounded-lg p-3 border border-amber-100 dark:border-amber-900/50">
                                    <i data-lucide="lightbulb" class="w-4 h-4 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5"></i>
                                    <p class="text-sm text-amber-800 dark:text-amber-300 font-medium">${escapeHtml(detail.tip)}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    function flowSteps(section) {
        const map = {
            'fundamentals': ['Sources', 'Ingest', 'Bronze', 'Silver', 'Gold', 'Consume'],
            'workspace-ui': ['Workspace', 'Repos', 'Notebook', 'Run', 'Review'],
            'clusters': ['Policy', 'Runtime', 'Cluster', 'Autoscale', 'Terminate'],
            'dbfs': ['Files', 'Volumes', 'External Location', 'Credential', 'Cloud Storage'],
            'delta-lake': ['Write Files', '_delta_log', 'Snapshot', 'Optimize', 'Time Travel'],
            'unity-catalog': ['Metastore', 'Catalog', 'Schema', 'Object', 'Grant/Audit'],
            'databricks-sql': ['Gold Tables', 'SQL Warehouse', 'Query Profile', 'Dashboard', 'Alert'],
            'delta-live-tables': ['Source', 'DLT View', 'Expectation', 'Table', 'Event Log'],
            'workflows-jobs': ['Trigger', 'Task DAG', 'Job Cluster', 'Monitor', 'Repair'],
            'repos-cicd': ['Git', 'Test', 'Bundle', 'Deploy', 'Promote'],
            'mlflow': ['Experiment', 'Run', 'Metrics', 'Registry', 'Serve'],
            'ml-ai': ['Features', 'Train', 'Register', 'Vector Search', 'Serving'],
            'performance-optimization': ['Profile', 'Prune', 'Join Tune', 'Compact', 'Scale'],
            'security': ['Identity', 'Network', 'Secrets', 'UC Grants', 'Audit'],
            'databricks-on-aws': ['VPC', 'IAM Role', 'S3', 'PrivateLink', 'Workload'],
            'databricks-on-azure': ['VNet', 'Entra ID', 'ADLS', 'Key Vault', 'Monitor'],
            'data-ingestion': ['Source', 'Auto Loader', 'Checkpoint', 'Bronze', 'Quality'],
            'administration': ['Account', 'Groups', 'Policies', 'Usage', 'Chargeback'],
            'advanced-patterns': ['Bronze', 'Silver', 'Gold', 'Share', 'Domain'],
            'integrations': ['Tool', 'Connector', 'Databricks', 'Delta', 'Consumer'],
            'interview-preparation': ['Concept', 'Tradeoff', 'Example', 'Scenario', 'Answer']
        };
        return map[section.slug] || ['Understand', 'Configure', 'Run', 'Monitor', 'Improve'];
    }

    function renderFlowChart(section) {
        const steps = flowSteps(section);
        const gradients = [
            'from-cyan-500 to-blue-600',
            'from-blue-500 to-indigo-600',
            'from-indigo-500 to-violet-600',
            'from-violet-500 to-purple-600',
            'from-purple-500 to-fuchsia-600',
            'from-fuchsia-500 to-pink-600',
        ];
        return `
            <section class="rounded-2xl border border-slate-200 bg-white p-6 mb-8 shadow-sm">
                <div class="flex items-center gap-3 mb-6">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 text-white flex items-center justify-center"><i data-lucide="workflow" class="w-5 h-5"></i></div>
                    <div><h2 class="font-display font-bold text-xl text-slate-900">How It Flows</h2><p class="text-xs text-slate-500">A simple mental model for this section.</p></div>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
                    ${steps.map((step, index) => `
                        <div class="relative">
                            <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center group hover:shadow-md transition-all">
                                <div class="mx-auto mb-2 w-9 h-9 rounded-full bg-gradient-to-br ${gradients[index % gradients.length]} text-white flex items-center justify-center text-xs font-black">${index + 1}</div>
                                <div class="font-bold text-sm text-slate-800">${escapeHtml(step)}</div>
                            </div>
                            ${index < steps.length - 1 ? '<div class="hidden md:block absolute top-1/2 -right-2 w-4 h-0.5 bg-gradient-to-r from-cyan-300 to-blue-300"></div>' : ''}
                        </div>
                    `).join('')}
                </div>
            </section>
        `;
    }

    function renderSectionArticle(section) {
        return `
            <article class="prose dark:prose-invert max-w-none bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 transition-colors shadow-sm dark:shadow-none">
                <div class="flex items-start gap-4 mb-6">
                    <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 text-white flex items-center justify-center flex-shrink-0 shadow-lg shadow-cyan-500/20">
                        <i data-lucide="${escapeHtml(section.icon || 'book-open')}" class="w-7 h-7"></i>
                    </div>
                    <div>
                        <p class="text-xs font-black uppercase tracking-widest text-cyan-600 dark:text-cyan-400 mb-1">Section ${section.id}</p>
                        <h1 class="font-display font-bold text-3xl md:text-4xl text-slate-900 dark:text-white transition-colors">${escapeHtml(section.title)}</h1>
                    </div>
                </div>
                <div class="rounded-xl bg-gradient-to-r from-cyan-50/80 to-blue-50/50 dark:from-cyan-950/30 dark:to-blue-950/20 border border-cyan-100 dark:border-cyan-900/50 p-5 mb-6">
                    <p class="text-slate-600 dark:text-slate-300 text-sm leading-7 mb-0">${escapeHtml(section.detailed_explanation)}</p>
                </div>
                ${renderFlowChart(section)}
                <div class="rounded-2xl bg-gradient-to-r from-violet-50/70 to-purple-50/50 dark:from-violet-950/20 dark:to-purple-950/20 border border-violet-100 dark:border-violet-900/70 p-5 mb-6">
                    <div class="flex items-center gap-2 mb-3">
                        <i data-lucide="map" class="w-4 h-4 text-violet-600 dark:text-violet-400"></i>
                        <h2 class="font-display font-bold text-lg text-slate-900 dark:text-white">Learning Map</h2>
                    </div>
                    <p class="text-sm text-slate-600 dark:text-slate-300 leading-7 mb-4">Read this page as a guided path: understand the idea, see why it matters in production, then connect it to the examples and tradeoffs.</p>
                    <div class="flex flex-wrap gap-2">${renderTopicPills(section.topics)}</div>
                </div>
                <div class="flex items-center gap-2 mb-4">
                    <i data-lucide="book-open" class="w-5 h-5 text-cyan-600 dark:text-cyan-400"></i>
                    <h2 class="font-display font-bold text-xl text-slate-900 dark:text-white mb-0">Topics Explained</h2>
                </div>
                <div class="grid grid-cols-1 gap-4 mb-8">${renderTopicDetails(section)}</div>
                ${(section.examples || []).length ? `
                    <div class="flex items-center gap-2 mb-4">
                        <i data-lucide="terminal" class="w-5 h-5 text-emerald-600 dark:text-emerald-400"></i>
                        <h2 class="font-display font-bold text-xl text-slate-900 dark:text-white mb-0">Hands-On Examples</h2>
                    </div>
                    <div class="grid grid-cols-1 gap-4 mb-8">${renderExamples(section.examples)}</div>
                ` : ''}
                ${(section.drawbacks_and_solutions || []).length ? `
                    <div class="flex items-center gap-2 mb-4">
                        <i data-lucide="alert-triangle" class="w-5 h-5 text-amber-600 dark:text-amber-400"></i>
                        <h2 class="font-display font-bold text-xl text-slate-900 dark:text-white mb-0">Challenges & Solutions</h2>
                    </div>
                    <div class="grid grid-cols-1 gap-3 mb-8">${renderDrawbacks(section.drawbacks_and_solutions)}</div>
                ` : ''}
            </article>
        `;
    }

    function populateToc(root) {
        const toc = document.querySelector('.toc-list');
        if (!toc) return;
        const headers = root.querySelectorAll('h2, h3');
        toc.innerHTML = '';
        headers.forEach((header, index) => {
            if (!header.id) {
                header.id = header.textContent.toLowerCase().trim().replace(/\s+/g, '-').replace(/[^\w-]/g, '') + '-' + index;
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

    function categoryMap() {
        return {
            'fundamentals':              { cat: 'Data Engineering', icon: 'database', accent: 'blue' },
            'dbfs':                      { cat: 'Data Engineering', icon: 'folder-open', accent: 'blue' },
            'delta-lake':                { cat: 'Data Engineering', icon: 'layers', accent: 'blue' },
            'databricks-sql':            { cat: 'Data Engineering', icon: 'table-2', accent: 'blue' },
            'delta-live-tables':         { cat: 'Data Engineering', icon: 'git-branch', accent: 'blue' },
            'data-ingestion':            { cat: 'Data Engineering', icon: 'download-cloud', accent: 'blue' },
            'mlflow':                    { cat: 'ML & AI', icon: 'brain-circuit', accent: 'violet' },
            'ml-ai':                     { cat: 'ML & AI', icon: 'bot', accent: 'violet' },
            'unity-catalog':             { cat: 'Security & Governance', icon: 'shield-check', accent: 'amber' },
            'security':                  { cat: 'Security & Governance', icon: 'lock', accent: 'amber' },
            'workspace-ui':              { cat: 'Platform & Compute', icon: 'layout-grid', accent: 'cyan' },
            'clusters':                  { cat: 'Platform & Compute', icon: 'server', accent: 'cyan' },
            'performance-optimization':  { cat: 'Platform & Compute', icon: 'gauge', accent: 'cyan' },
            'administration':            { cat: 'Platform & Compute', icon: 'settings', accent: 'cyan' },
            'repos-cicd':                { cat: 'DevOps', icon: 'git-branch', accent: 'emerald' },
            'workflows-jobs':            { cat: 'DevOps', icon: 'workflow', accent: 'emerald' },
            'databricks-on-aws':         { cat: 'Cloud', icon: 'cloud', accent: 'sky' },
            'databricks-on-azure':       { cat: 'Cloud', icon: 'cloud-cog', accent: 'sky' },
            'integrations':              { cat: 'Cloud', icon: 'plug', accent: 'sky' },
            'advanced-patterns':         { cat: 'Architecture', icon: 'cpu', accent: 'rose' },
            'interview-preparation':     { cat: 'Interview Prep', icon: 'book-open-check', accent: 'rose' },
        };
    }

    const accentClasses = {
        blue:     { bg: 'bg-blue-50', border: 'border-blue-100', text: 'text-blue-700', ring: 'ring-blue-300', pill: 'bg-blue-50 text-blue-700 border-blue-100', card: 'bg-blue-50/60', hover: 'text-blue-700', numBg: 'bg-blue-100', numText: 'text-blue-700', gradient: 'from-blue-500 to-indigo-600' },
        violet:   { bg: 'bg-violet-50', border: 'border-violet-100', text: 'text-violet-700', ring: 'ring-violet-300', pill: 'bg-violet-50 text-violet-700 border-violet-100', card: 'bg-violet-50/60', hover: 'text-violet-700', numBg: 'bg-violet-100', numText: 'text-violet-700', gradient: 'from-violet-500 to-purple-600' },
        amber:    { bg: 'bg-amber-50', border: 'border-amber-100', text: 'text-amber-700', ring: 'ring-amber-300', pill: 'bg-amber-50 text-amber-700 border-amber-100', card: 'bg-amber-50/60', hover: 'text-amber-700', numBg: 'bg-amber-100', numText: 'text-amber-700', gradient: 'from-amber-500 to-orange-600' },
        cyan:     { bg: 'bg-cyan-50', border: 'border-cyan-100', text: 'text-cyan-700', ring: 'ring-cyan-300', pill: 'bg-cyan-50 text-cyan-700 border-cyan-100', card: 'bg-cyan-50/60', hover: 'text-cyan-700', numBg: 'bg-cyan-100', numText: 'text-cyan-700', gradient: 'from-cyan-500 to-blue-600' },
        emerald:  { bg: 'bg-emerald-50', border: 'border-emerald-100', text: 'text-emerald-700', ring: 'ring-emerald-300', pill: 'bg-emerald-50 text-emerald-700 border-emerald-100', card: 'bg-emerald-50/60', hover: 'text-emerald-700', numBg: 'bg-emerald-100', numText: 'text-emerald-700', gradient: 'from-emerald-500 to-teal-600' },
        sky:      { bg: 'bg-sky-50', border: 'border-sky-100', text: 'text-sky-700', ring: 'ring-sky-300', pill: 'bg-sky-50 text-sky-700 border-sky-100', card: 'bg-sky-50/60', hover: 'text-sky-700', numBg: 'bg-sky-100', numText: 'text-sky-700', gradient: 'from-sky-500 to-blue-600' },
        rose:     { bg: 'bg-rose-50', border: 'border-rose-100', text: 'text-rose-700', ring: 'ring-rose-300', pill: 'bg-rose-50 text-rose-700 border-rose-100', card: 'bg-rose-50/60', hover: 'text-rose-700', numBg: 'bg-rose-100', numText: 'text-rose-700', gradient: 'from-rose-500 to-pink-600' },
    };

    function renderIndex(root, guide) {
        const sections = guide.sections || [];
        const questions = guide.top_100_interview_questions || [];
        const diagrams = guide.diagrams || [];
        const basePath = root.dataset.sectionBase || 'databricks';
        const map = categoryMap();
        const order = ['Data Engineering', 'ML & AI', 'Security & Governance', 'Platform & Compute', 'DevOps', 'Cloud', 'Architecture', 'Interview Prep'];
        const grouped = {};
        sections.forEach(s => {
            const info = map[s.slug] || { cat: 'Other', icon: 'box', accent: 'blue' };
            if (!grouped[info.cat]) grouped[info.cat] = { icon: info.icon, accent: info.accent, sections: [] };
            grouped[info.cat].sections.push(s);
        });

        const catCards = order
            .filter(cat => grouped[cat])
            .map(cat => {
                const g = grouped[cat];
                const ac = accentClasses[g.accent] || accentClasses.blue;
                const cards = g.sections.map(section => `
                    <a href="${escapeHtml(sectionHref(section, basePath))}" data-databricks-topic-card="${escapeHtml(section.slug)}" class="no-underline group block bg-white border border-slate-200/80 rounded-2xl p-5 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                        <div class="flex items-start gap-4">
                            <div class="w-10 h-10 rounded-xl bg-gradient-to-br ${ac.gradient} text-white flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform shadow-sm">
                                <i data-lucide="${escapeHtml(iconForTopic(section.topics[0] || ''))}" class="w-5 h-5"></i>
                            </div>
                            <div class="flex-1 min-w-0">
                                <h2 class="font-bold text-slate-800 text-sm group-hover:${ac.hover} transition-colors leading-snug mb-0.5">${escapeHtml(section.title)}</h2>
                                <p class="text-slate-400 text-xs">${(section.topics || []).length} topics</p>
                            </div>
                            <i data-lucide="arrow-right" class="w-4 h-4 text-slate-300 group-hover:${ac.hover} group-hover:translate-x-1 transition-all flex-shrink-0 mt-0.5"></i>
                        </div>
                    </a>
                `).join('');
                return `
                    <section>
                        <div class="flex items-center gap-3 mb-4">
                            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full ${ac.pill} text-xs font-bold uppercase tracking-wide border"><i data-lucide="${escapeHtml(g.icon)}" class="w-3 h-3"></i>${escapeHtml(cat)}</span>
                            <span class="text-xs font-semibold text-slate-400">${g.sections.length} ${g.sections.length === 1 ? 'topic' : 'topics'}</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">${cards}</div>
                    </section>
                `;
            }).join('');

        root.innerHTML = `
            <div class="space-y-10">${catCards}</div>
        `;

        root.querySelectorAll('[data-databricks-topic-card]').forEach((card) => {
            card.addEventListener('click', () => {
                sessionStorage.setItem('databricks:last-topic', card.dataset.databricksTopicCard || '');
            });
        });

        const lastTopic = sessionStorage.getItem('databricks:last-topic');
        if (lastTopic) {
            const card = Array.from(root.querySelectorAll('[data-databricks-topic-card]'))
                .find((item) => item.dataset.databricksTopicCard === lastTopic);
            if (card) {
                const slug = lastTopic;
                const info = map[slug] || { accent: 'blue' };
                const ac = accentClasses[info.accent] || accentClasses.blue;
                card.classList.add('ring-2', ac.ring, ac.border.replace('border-', 'border-'), ac.card);
                requestAnimationFrame(() => card.scrollIntoView({ block: 'center' }));
            }
        }
    }

    function ensureSectionSidebar(sections, currentSlug) {
        const guideNav = document.querySelector('#guide-topics nav');
        if (guideNav) {
            guideNav.querySelectorAll('.sb-link').forEach((link) => {
                const href = link.getAttribute('href');
                if (href === `${currentSlug}.html`) {
                    link.classList.add('active');
                }
            });
        }
    }

    function renderSection(root, guide) {
        const slug = root.dataset.sectionSlug;
        const sections = guide.sections || [];
        ensureSectionSidebar(sections, slug);
        const section = sections.find((item) => item.slug === slug);
        const indexHref = root.dataset.indexHref || '../databricks.html';

        if (!section) {
            root.innerHTML = `<div class="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-rose-700">Section not found: ${escapeHtml(slug)}</div>`;
            return;
        }

        document.title = `${section.title} — Databricks — Data Cake`;
        const previous = sections[sections.indexOf(section) - 1];
        const next = sections[sections.indexOf(section) + 1];

        root.innerHTML = `
            <a href="${escapeHtml(indexHref)}" data-databricks-back="${escapeHtml(section.slug)}" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200"><i data-lucide="arrow-left" class="w-4 h-4"></i>Back to Databricks Topics</a>
            ${renderSectionArticle(section)}
            ${section.slug === 'interview-preparation' ? renderInterviewQuestions(guide.top_100_interview_questions || []) : ''}
            <nav class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
                ${previous ? `<a href="${escapeHtml(previous.slug)}.html" class="p-5 rounded-2xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 no-underline hover:border-cyan-200 transition-colors"><span class="text-xs font-bold uppercase text-slate-400">Previous</span><span class="block font-bold text-slate-800 dark:text-slate-100 mt-1">${escapeHtml(previous.title)}</span></a>` : '<div></div>'}
                ${next ? `<a href="${escapeHtml(next.slug)}.html" class="p-5 rounded-2xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 no-underline hover:border-cyan-200 transition-colors sm:text-right"><span class="text-xs font-bold uppercase text-slate-400">Next</span><span class="block font-bold text-slate-800 dark:text-slate-100 mt-1">${escapeHtml(next.title)}</span></a>` : '<div></div>'}
            </nav>
        `;

        const backLink = root.querySelector('[data-databricks-back]');
        if (backLink) {
            backLink.addEventListener('click', () => {
                sessionStorage.setItem('databricks:last-topic', section.slug);
            });
        }

        populateToc(root);
        if (typeof lucide !== 'undefined') lucide.createIcons();
        ensurePrismAssets();
    }

    // Global copy function for code blocks
    window.copyCode = function(btn) {
        const pre = btn.closest('.group').querySelector('pre code');
        if (pre) {
            navigator.clipboard.writeText(pre.textContent);
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i data-lucide="check" class="w-3 h-3"></i>Copied!';
            btn.classList.add('text-emerald-600');
            if (typeof lucide !== 'undefined') lucide.createIcons();
            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.classList.remove('text-emerald-600');
                if (typeof lucide !== 'undefined') lucide.createIcons();
            }, 2000);
        }
    };

    document.addEventListener('DOMContentLoaded', async () => {
        const root = document.getElementById('databricks-guide');
        if (!root) return;

        try {
            const response = await fetch(root.dataset.guidePath || '../../data/databricks_complete_guide.json');
            if (!response.ok) throw new Error(`Unable to load guide JSON: ${response.status}`);
            const guide = await response.json();

            if (root.dataset.mode === 'section') renderSection(root, guide);
            else renderIndex(root, guide);

            if (typeof lucide !== 'undefined') lucide.createIcons();
        } catch (error) {
            root.innerHTML = `<div class="bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900 rounded-2xl p-8 text-rose-700 dark:text-rose-300"><h2 class="font-display font-bold text-xl mb-2">Unable to load Databricks guide</h2><p class="text-sm">${escapeHtml(error.message)}</p></div>`;
        }
    });
})();