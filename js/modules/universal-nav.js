/* Universal Nav Module */

(function() {
    function getPrefix() {
        const path = window.location.pathname.replace(/\\/g, '/');
        const parts = path.split('/').filter(Boolean);
        
        // Find 'pages' index to determine depth
        const pagesIdx = parts.indexOf('pages');
        if (pagesIdx === -1) return ''; // Root level
        
        const depth = parts.length - 1 - pagesIdx;
        return '../'.repeat(depth + 1);
    }

    function initUniversalNav() {
        const prefix = getPrefix();
        const rootPrefix = prefix === '' ? '' : prefix;
        const pagesPrefix = prefix === '' ? 'pages/' : prefix + 'pages/';

        const navHtml = `
<nav id="ds-nav" class="bg-surface/80 backdrop-blur-md border-b border-outline-variant sticky top-0 z-50">
    <div class="flex items-center justify-between h-14 w-full px-3 md:px-6">
        <div class="flex items-center gap-2">
            <button id="topbar-toggle" aria-label="Toggle navigation" class="lg:hidden w-10 h-10 flex items-center justify-center text-on-surface-variant hover:text-on-surface transition-colors">
                <i data-lucide="menu" class="w-6 h-6"></i>
            </button>
            <a href="${rootPrefix}index.html" class="flex items-center gap-2.5 group no-underline relative">
                <div class="relative flex items-center justify-center">
                    <i data-lucide="code-2" class="w-5 h-5 text-on-surface transition-all duration-500 group-hover:text-accent-emerald group-hover:scale-110"></i>
                    <div class="absolute inset-0 bg-accent-emerald/20 blur-md opacity-0 group-hover:opacity-100 transition-opacity"></div>
                </div>
                <span class="font-black text-lg text-on-surface uppercase tracking-widest group-hover:text-accent-emerald transition-colors">Data Cake</span>
            </a>
        </div>
        
        <div class="hidden lg:flex items-center gap-1 flex-1 justify-center mx-4">
            <div class="tb-group">
                <button class="tb-btn" data-category="Programming">Programming<i data-lucide="chevron-down" class="w-3 h-3 tb-chevron"></i></button>
                <div class="tb-dropdown">
                    <a href="${pagesPrefix}learn/python.html" class="tb-link">Python</a>
                    <a href="${pagesPrefix}learn/sql.html" class="tb-link">SQL</a>
                    <a href="${pagesPrefix}learn/bash.html" class="tb-link">Bash</a>
                    <a href="${pagesPrefix}learn/powershell.html" class="tb-link">PowerShell</a>
                </div>
            </div>
            <div class="tb-group">
                <button class="tb-btn" data-category="Concepts">Concepts<i data-lucide="chevron-down" class="w-3 h-3 tb-chevron"></i></button>
                <div class="tb-dropdown">
                    <a href="${pagesPrefix}learn/de-fundamentals.html" class="tb-link">DE Fundamentals</a>
                    <a href="${pagesPrefix}learn/dsa-de.html" class="tb-link">DSA for DE</a>
                    <a href="${pagesPrefix}learn/system-design.html" class="tb-link">System Design</a>
                    <a href="${pagesPrefix}learn/pipeline-design.html" class="tb-link">Pipeline Design</a>
                    <a href="${pagesPrefix}learn/de-architectures.html" class="tb-link">DE Architectures</a>
                    <a href="${pagesPrefix}learn/agents.html" class="tb-link">AI Agents</a>
                </div>
            </div>
            <div class="tb-group">
                <button class="tb-btn" data-category="Tools">Tools<i data-lucide="chevron-down" class="w-3 h-3 tb-chevron"></i></button>
                <div class="tb-dropdown">
                    <a href="${pagesPrefix}learn/spark.html" class="tb-link">Spark</a>
                    <a href="${pagesPrefix}learn/flink.html" class="tb-link">Flink</a>
                    <a href="${pagesPrefix}learn/kafka.html" class="tb-link">Kafka</a>
                    <a href="${pagesPrefix}learn/dbt.html" class="tb-link">dbt</a>
                    <a href="${pagesPrefix}learn/pandas.html" class="tb-link">Pandas</a>
                    <a href="${pagesPrefix}learn/numpy.html" class="tb-link">NumPy</a>
                    <a href="${pagesPrefix}learn/airflow.html" class="tb-link">Airflow</a>
                    <a href="${pagesPrefix}learn/regex.html" class="tb-link">Regex</a>
                </div>
            </div>
            <div class="tb-group">
                <button class="tb-btn" data-category="Cloud">Cloud<i data-lucide="chevron-down" class="w-3 h-3 tb-chevron"></i></button>
                <div class="tb-dropdown">
                    <a href="${pagesPrefix}learn/aws.html" class="tb-link">AWS</a>
                    <a href="${pagesPrefix}learn/gcp.html" class="tb-link">GCP</a>
                    <a href="${pagesPrefix}learn/azure.html" class="tb-link">Azure</a>
                    <a href="${pagesPrefix}learn/snowflake.html" class="tb-link">Snowflake</a>
                    <a href="${pagesPrefix}learn/databricks.html" class="tb-link">Databricks</a>
                </div>
            </div>
            <div class="tb-group">
                <button class="tb-btn" data-category="CICD">CI/CD<i data-lucide="chevron-down" class="w-3 h-3 tb-chevron"></i></button>
                <div class="tb-dropdown">
                    <a href="${pagesPrefix}learn/docker.html" class="tb-link">Docker</a>
                    <a href="${pagesPrefix}learn/kubernetes.html" class="tb-link">Kubernetes</a>
                    <a href="${pagesPrefix}learn/terraform.html" class="tb-link">Terraform</a>
                    <a href="${pagesPrefix}learn/github.html" class="tb-link">GitHub</a>
                </div>
            </div>
            <div class="tb-group">
                <button class="tb-btn" data-category="Roadmaps">Roadmaps<i data-lucide="chevron-down" class="w-3 h-3 tb-chevron"></i></button>
                <div class="tb-dropdown">
                    <a href="${pagesPrefix}roadmaps/data-engineering.html" class="tb-link">Data Engineering</a>
                    <a href="${pagesPrefix}roadmaps/ml-engineer.html" class="tb-link">ML Engineer</a>
                    <a href="${pagesPrefix}roadmaps/ai-engineer.html" class="tb-link">AI Engineer</a>
                </div>
            </div>
            <div class="tb-group">
                <button class="tb-btn" data-category="Practice">Practice<i data-lucide="chevron-down" class="w-3 h-3 tb-chevron"></i></button>
                <div class="tb-dropdown">
                    <a href="${pagesPrefix}practice.html" class="tb-link">Practice Hub</a>
                    <a href="${pagesPrefix}learn/skills.html" class="tb-link">Skills Arena</a>
                    <a href="${pagesPrefix}practice/list-comprehensions.html" class="tb-link">Python Challenges</a>
                    <a href="${pagesPrefix}practice/sql-window-functions.html" class="tb-link">SQL Challenges</a>
                </div>
            </div>
        </div>

        <div class="flex items-center gap-1.5">
            <button id="theme-toggle" title="Toggle theme"
                class="w-10 h-10 flex items-center justify-center hover:bg-surface-container rounded-xl transition-colors text-on-surface-variant hover:text-on-surface">
                <i data-lucide="sun" class="w-5 h-5 theme-sun"></i>
                <i data-lucide="moon" class="w-5 h-5 theme-moon"></i>
            </button>
            <a href="${pagesPrefix}portfolio.html" id="profile-btn" title="Profile"
                class="w-10 h-10 flex items-center justify-center text-on-surface-variant hover:text-on-surface transition-colors no-underline">
                <i data-lucide="user-circle-2" class="w-6 h-6"></i>
            </a>
        </div>
    </div>
</nav>

<div id="mobile-sidebar-overlay" class="fixed inset-0 bg-surface/80 backdrop-blur-sm z-40 opacity-0 pointer-events-none transition-opacity duration-300 lg:hidden"></div>
<aside id="mobile-sidebar" class="fixed top-0 left-0 h-full w-72 z-50 overflow-y-auto bg-surface border-r border-outline-variant transform -translate-x-full transition-transform duration-300 lg:hidden">
    <div class="flex items-center justify-between px-4 h-14 border-b border-outline-variant">
        <span class="font-bold text-on-surface uppercase tracking-wider text-sm">Navigation</span>
        <button id="mobile-sidebar-close" class="w-8 h-8 flex items-center justify-center text-on-surface-variant hover:text-on-surface">
            <i data-lucide="x" class="w-5 h-5"></i>
        </button>
    </div>
    <div class="py-4 px-3">
        <div class="mb-4">
            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer collapsed">
                <i data-lucide="code-2" class="w-4 h-4"></i> Programming
            </div>
            <nav class="pl-2 hidden">
                <a href="${pagesPrefix}learn/python.html" class="sb-link">Python</a>
                <a href="${pagesPrefix}learn/sql.html" class="sb-link">SQL</a>
                <a href="${pagesPrefix}learn/bash.html" class="sb-link">Bash</a>
                <a href="${pagesPrefix}learn/powershell.html" class="sb-link">PowerShell</a>
            </nav>
        </div>
        <div class="mb-4">
            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer collapsed">
                <i data-lucide="layers" class="w-4 h-4"></i> Concepts
            </div>
            <nav class="pl-2 hidden">
                <a href="${pagesPrefix}learn/de-fundamentals.html" class="sb-link">DE Fundamentals</a>
                <a href="${pagesPrefix}learn/dsa-de.html" class="sb-link">DSA for DE</a>
                <a href="${pagesPrefix}learn/system-design.html" class="sb-link">System Design</a>
                <a href="${pagesPrefix}learn/pipeline-design.html" class="sb-link">Pipeline Design</a>
                <a href="${pagesPrefix}learn/de-architectures.html" class="sb-link">DE Architectures</a>
                <a href="${pagesPrefix}learn/agents.html" class="sb-link">AI Agents</a>
            </nav>
        </div>
        <div class="mb-4">
            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer collapsed">
                <i data-lucide="calculator" class="w-4 h-4"></i> Tools
            </div>
            <nav class="pl-2 hidden">
                <a href="${pagesPrefix}learn/spark.html" class="sb-link">Spark</a>
                <a href="${pagesPrefix}learn/flink.html" class="sb-link">Flink</a>
                <a href="${pagesPrefix}learn/kafka.html" class="sb-link">Kafka</a>
                <a href="${pagesPrefix}learn/dbt.html" class="sb-link">dbt</a>
                <a href="${pagesPrefix}learn/pandas.html" class="sb-link">Pandas</a>
                <a href="${pagesPrefix}learn/numpy.html" class="sb-link">NumPy</a>
                <a href="${pagesPrefix}learn/airflow.html" class="sb-link">Airflow</a>
                <a href="${pagesPrefix}learn/regex.html" class="sb-link">Regex</a>
            </nav>
        </div>
        <div class="mb-4">
            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer collapsed">
                <i data-lucide="cloud" class="w-4 h-4"></i> Cloud
            </div>
            <nav class="pl-2 hidden">
                <a href="${pagesPrefix}learn/aws.html" class="sb-link">AWS</a>
                <a href="${pagesPrefix}learn/gcp.html" class="sb-link">GCP</a>
                <a href="${pagesPrefix}learn/azure.html" class="sb-link">Azure</a>
                <a href="${pagesPrefix}learn/snowflake.html" class="sb-link">Snowflake</a>
                <a href="${pagesPrefix}learn/databricks.html" class="sb-link">Databricks</a>
            </nav>
        </div>
        <div class="mb-4">
            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer collapsed">
                <i data-lucide="git-pull-request" class="w-4 h-4"></i> CI / CD
            </div>
            <nav class="pl-2 hidden">
                <a href="${pagesPrefix}learn/docker.html" class="sb-link">Docker</a>
                <a href="${pagesPrefix}learn/kubernetes.html" class="sb-link">Kubernetes</a>
                <a href="${pagesPrefix}learn/terraform.html" class="sb-link">Terraform</a>
                <a href="${pagesPrefix}learn/github.html" class="sb-link">GitHub</a>
            </nav>
        </div>
        <div class="mb-4">
            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer collapsed">
                <i data-lucide="map" class="w-4 h-4"></i> Roadmaps
            </div>
            <nav class="pl-2 hidden">
                <a href="${pagesPrefix}roadmaps/data-engineering.html" class="sb-link">Data Engineering</a>
                <a href="${pagesPrefix}roadmaps/ml-engineer.html" class="sb-link">ML Engineer</a>
                <a href="${pagesPrefix}roadmaps/ai-engineer.html" class="sb-link">AI Engineer</a>
            </nav>
        </div>
        <div class="mb-4">
            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer collapsed">
                <i data-lucide="hammer" class="w-4 h-4"></i> Practice
            </div>
            <nav class="pl-2 hidden">
                <a href="${pagesPrefix}practice.html" class="sb-link">Practice Hub</a>
                <a href="${pagesPrefix}learn/skills.html" class="sb-link">Skills Arena</a>
                <a href="${pagesPrefix}practice/list-comprehensions.html" class="sb-link">Python Challenges</a>
                <a href="${pagesPrefix}practice/sql-window-functions.html" class="sb-link">SQL Challenges</a>
            </nav>
        </div>
        <div class="mt-6 pt-4 border-t border-outline-variant">
            <a href="${pagesPrefix}portfolio.html" class="sb-section text-on-surface-variant hover:text-on-surface no-underline">
                <i data-lucide="folder-closed" class="w-4 h-4"></i>
                My Portfolio
            </a>
        </div>
        <div id="guide-topics" class="mt-6 hidden"></div>
    </div>
</aside>

<button id="scroll-top" title="Back to top"
    class="fixed bottom-6 right-6 z-50 w-10 h-10 flex items-center justify-center rounded-full
           bg-on-surface text-surface shadow-lg hover:scale-110 scale-90 transition-all duration-200">
    <i data-lucide="arrow-up" class="w-4 h-4"></i>
</button>
        `;

        const existingNav = document.getElementById('ds-nav');
        if (existingNav) {
            existingNav.outerHTML = navHtml;
        } else {
            // If no nav found, prepend to body
            const wrapper = document.createElement('div');
            wrapper.innerHTML = navHtml;
            while (wrapper.firstChild) {
                document.body.prepend(wrapper.lastChild);
            }
        }
        
        // Re-init scripts that depend on this markup
        if (window.dsInitMobileSidebar) window.dsInitMobileSidebar();
        if (window.dsInitThemeToggle) window.dsInitThemeToggle();
        if (window.dsInitProfilePill) window.dsInitProfilePill();
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initUniversalNav);
    } else {
        initUniversalNav();
    }
})();
