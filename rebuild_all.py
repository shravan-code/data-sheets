"""
rebuild_all.py
==============
One-shot script that:
1. Strips the old nav / sidebar fragments from every generated HTML file.
2. Injects a brand-new, unified component (nav + sidebar + scroll-to-top).
3. Fixes main-content padding so it doesn't hide behind the sidebar.
4. Rewrites index.html & pages/learn.html & pages/practice.html in-place.
5. Runs all build scripts to regenerate sub-pages and re-injects.

Run:  python rebuild_all.py
"""

import os, re, glob, subprocess, sys

# ---------------------------------------------------------------------------
# SHARED COMPONENT  (call get_nav_sidebar(prefix) to render)
# prefix = relative path from the file back to the project root, e.g. "../../../"
# ---------------------------------------------------------------------------

SHARED_CSS = """\
    <style>
        body{font-family:'Inter',sans-serif;}
        h1,h2,h3,.font-display{font-family:'Outfit',sans-serif;}
        .grid-bg{background-image:linear-gradient(rgba(0,0,0,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.05) 1px,transparent 1px);background-size:40px 40px;}
        .dark .grid-bg{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);}
        /* Sidebar scrollbar matches theme */
        #ds-sidebar{scrollbar-width:thin;scrollbar-color:#cbd5e1 transparent;}
        #ds-sidebar::-webkit-scrollbar{width:4px;}
        #ds-sidebar::-webkit-scrollbar-track{background:transparent;}
        #ds-sidebar::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:999px;}
        .dark #ds-sidebar::-webkit-scrollbar-thumb{background:#334155;}
        /* Scroll-to-top btn */
        #scroll-top{opacity:0;pointer-events:none;transition:opacity .25s;}
        #scroll-top.visible{opacity:1;pointer-events:auto;}
        /* card hover */
        .topic-card{transition:all 0.25s cubic-bezier(.4,0,.2,1);}
        .topic-card:hover{transform:translateY(-4px);}
        .dark .topic-card:hover{box-shadow:0 20px 40px rgba(0,0,0,.5),0 0 20px rgba(59,130,246,.12);border-color:rgba(96,165,250,.3);}
        .topic-card:hover{box-shadow:0 20px 40px rgba(0,0,0,.08);border-color:rgba(96,165,250,.3);}
    </style>"""

def get_nav_sidebar(prefix):
    """Return the nav + sidebar HTML string for a given path prefix."""
    return f"""\
<!-- NAV -->
<nav id="ds-nav" class="fixed top-0 w-full z-50 bg-white/95 dark:bg-slate-950/95 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <button id="sidebar-toggle" aria-label="Toggle sidebar" class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
                <i data-lucide="panel-left" class="w-5 h-5"></i>
            </button>
            <a href="{prefix}index.html" class="no-underline">
                <span style="font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:-.02em;" class="text-lg md:text-xl text-slate-900 dark:text-white transition-colors">Data Sheets</span>
            </a>
        </div>
        <button id="theme-toggle" title="Toggle theme" class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
            <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
            <i data-lucide="moon" class="w-5 h-5 block dark:hidden"></i>
        </button>
    </div>
</nav>

<!-- SIDEBAR OVERLAY (mobile) -->
<div id="sidebar-overlay" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 hidden opacity-0 transition-opacity duration-300 lg:hidden"></div>

<!-- SIDEBAR -->
<!-- SIDEBAR -->
<aside id="ds-sidebar" class="fixed top-[57px] md:top-[65px] left-0 h-[calc(100vh-57px)] md:h-[calc(100vh-65px)] w-64 border-r border-slate-200 dark:border-slate-800/60 bg-white dark:bg-slate-950 z-40 overflow-y-auto py-6 px-5 transition-transform duration-300 -translate-x-full lg:translate-x-0">

    <div class="mb-8">
        <a href="{prefix}pages/learn.html" class="flex items-center gap-2 font-bold text-slate-900 dark:text-white text-sm uppercase tracking-wider mb-4 no-underline hover:text-blue-500 dark:hover:text-blue-400 transition-colors">
            <i data-lucide="book-open" class="w-4 h-4"></i> Learn
        </a>

        <div class="mb-5">
            <h5 class="text-[10px] font-bold text-blue-600 dark:text-blue-400 mb-2 uppercase tracking-widest">Programming</h5>
            <ul class="space-y-1.5 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/python.html" class="block py-0.5 hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Python</a></li>
                <li><a href="{prefix}pages/learn/sql.html" class="block py-0.5 hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">SQL</a></li>
                <li><a href="{prefix}pages/learn/bash.html" class="block py-0.5 hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Bash</a></li>
                <li><a href="{prefix}pages/learn/powershell.html" class="block py-0.5 hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">PowerShell</a></li>
            </ul>
        </div>

        <div class="mb-5">
            <h5 class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 mb-2 uppercase tracking-widest">Concepts</h5>
            <ul class="space-y-1.5 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/de-fundamentals.html" class="block py-0.5 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors no-underline">DE Fundamentals</a></li>
                <li><a href="{prefix}pages/learn/dsa-de.html" class="block py-0.5 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors no-underline">DSA for DE</a></li>
            </ul>
        </div>

        <div class="mb-5">
            <h5 class="text-[10px] font-bold text-orange-600 dark:text-orange-400 mb-2 uppercase tracking-widest">Tools</h5>
            <ul class="space-y-1.5 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/spark.html" class="block py-0.5 hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Spark</a></li>
                <li><a href="{prefix}pages/learn/flink.html" class="block py-0.5 hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Flink</a></li>
                <li><a href="{prefix}pages/learn/kafka.html" class="block py-0.5 hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Kafka</a></li>
                <li><a href="{prefix}pages/learn/dbt.html" class="block py-0.5 hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">dbt</a></li>
                <li><a href="{prefix}pages/learn/pandas.html" class="block py-0.5 hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Pandas</a></li>
                <li><a href="{prefix}pages/learn/numpy.html" class="block py-0.5 hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">NumPy</a></li>
                <li><a href="{prefix}pages/learn/airflow.html" class="block py-0.5 hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Airflow</a></li>
            </ul>
        </div>

        <div class="mb-5">
            <h5 class="text-[10px] font-bold text-cyan-600 dark:text-cyan-400 mb-2 uppercase tracking-widest">Cloud</h5>
            <ul class="space-y-1.5 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/aws.html" class="block py-0.5 hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">AWS</a></li>
                <li><a href="{prefix}pages/learn/gcp.html" class="block py-0.5 hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">GCP</a></li>
                <li><a href="{prefix}pages/learn/azure.html" class="block py-0.5 hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">Azure</a></li>
                <li><a href="{prefix}pages/learn/snowflake.html" class="block py-0.5 hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">Snowflake</a></li>
                <li><a href="{prefix}pages/learn/databricks.html" class="block py-0.5 hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">Databricks</a></li>
            </ul>
        </div>

        <div class="mb-5">
            <h5 class="text-[10px] font-bold text-violet-600 dark:text-violet-400 mb-2 uppercase tracking-widest">CI/CD</h5>
            <ul class="space-y-1.5 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/docker.html" class="block py-0.5 hover:text-violet-600 dark:hover:text-violet-400 transition-colors no-underline">Docker</a></li>
                <li><a href="{prefix}pages/learn/kubernetes.html" class="block py-0.5 hover:text-violet-600 dark:hover:text-violet-400 transition-colors no-underline">Kubernetes</a></li>
                <li><a href="{prefix}pages/learn/terraform.html" class="block py-0.5 hover:text-violet-600 dark:hover:text-violet-400 transition-colors no-underline">Terraform</a></li>
                <li><a href="{prefix}pages/learn/github.html" class="block py-0.5 hover:text-violet-600 dark:hover:text-violet-400 transition-colors no-underline">GitHub</a></li>
            </ul>
        </div>

        <div class="mb-5">
            <h5 class="text-[10px] font-bold text-rose-600 dark:text-rose-400 mb-2 uppercase tracking-widest">Design</h5>
            <ul class="space-y-1.5 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/system-design.html" class="block py-0.5 hover:text-rose-600 dark:hover:text-rose-400 transition-colors no-underline">System Design</a></li>
                <li><a href="{prefix}pages/learn/pipeline-design.html" class="block py-0.5 hover:text-rose-600 dark:hover:text-rose-400 transition-colors no-underline">Pipeline Design</a></li>
                <li><a href="{prefix}pages/learn/de-architectures.html" class="block py-0.5 hover:text-rose-600 dark:hover:text-rose-400 transition-colors no-underline">DE Architectures</a></li>
            </ul>
        </div>
    </div>

    <div class="border-t border-slate-200 dark:border-slate-800 pt-5">
        <a href="{prefix}pages/practice.html" class="flex items-center gap-2 font-bold text-slate-900 dark:text-white text-sm uppercase tracking-wider mb-4 no-underline hover:text-blue-500 dark:hover:text-blue-400 transition-colors">
            <i data-lucide="hammer" class="w-4 h-4"></i> Practice
        </a>
        <ul class="space-y-1.5 text-sm text-slate-600 dark:text-slate-400">
            <li><a href="{prefix}pages/practice.html" class="block py-0.5 hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Coming Soon</a></li>
        </ul>
    </div>
</aside>

<!-- SCROLL TO TOP -->
<button id="scroll-top" title="Back to top" class="fixed bottom-6 right-6 z-50 w-11 h-11 flex items-center justify-center rounded-full bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/30 transition-all hover:scale-110">
    <i data-lucide="arrow-up" class="w-5 h-5"></i>
</button>"""

SHARED_JS = """\
<script>
(function() {
    // Theme
    const html = document.documentElement;
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = html.classList.toggle('dark');
            localStorage.setItem('ds-theme', isDark ? 'dark' : 'light');
        });
    }

    // Sidebar toggle
    const sidebarBtn = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('ds-sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    function openSidebar() {
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
        requestAnimationFrame(() => overlay.classList.remove('opacity-0'));
    }
    function closeSidebar() {
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('opacity-0');
        setTimeout(() => overlay.classList.add('hidden'), 300);
    }

    if (sidebarBtn) {
        sidebarBtn.addEventListener('click', () => {
            if (sidebar.classList.contains('-translate-x-full')) openSidebar();
            else closeSidebar();
        });
    }
    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }

    // Scroll-to-top
    const scrollBtn = document.getElementById('scroll-top');
    if (scrollBtn) {
        window.addEventListener('scroll', () => {
            scrollBtn.classList.toggle('visible', window.scrollY > 300);
        });
        scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // Lucide icons
    if (typeof lucide !== 'undefined') lucide.createIcons();
})();
</script>"""


# ---------------------------------------------------------------------------
# Helper: strip old nav + sidebar + inject new ones
# ---------------------------------------------------------------------------

def compute_prefix(html_path):
    """
    Compute prefix (relative path to project root) from an HTML file path.
    e.g. pages/learn/bash/intro.html  -> ../../../
         pages/learn/bash.html        -> ../../
         pages/learn.html             -> ../
         index.html                   -> ''
    """
    norm = html_path.replace('\\', '/')
    parts = norm.split('/')
    # depth = number of directory separators
    depth = len(parts) - 1
    return '../' * depth


def patch_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    prefix = compute_prefix(os.path.relpath(path).replace('\\', '/'))

    # 1. Remove existing <nav ...>...</nav> block (greedy-safe: non-greedy)
    html = re.sub(r'<nav\b[^>]*>.*?</nav>', '', html, flags=re.DOTALL)

    # 2. Remove existing sidebar <aside ...>...</aside>
    html = re.sub(r'<!-- SIDEBAR -->.*?</aside>', '', html, flags=re.DOTALL)
    html = re.sub(r'<aside\b[^>]*>.*?</aside>', '', html, flags=re.DOTALL)

    # 3. Remove sidebar overlay divs
    html = re.sub(r'<div id="sidebar-overlay"[^>]*>.*?</div>', '', html, flags=re.DOTALL)

    # 4. Remove old scroll-to-top button
    html = re.sub(r'<button id="scroll-top"[^>]*>.*?</button>', '', html, flags=re.DOTALL)

    # 5. Remove old wrapper divs that were added by the old sidebar script
    html = re.sub(r'<div class="lg:pl-\d+ w-full">', '', html)
    html = re.sub(r'<!-- old sidebar wrapper -->', '', html)

    # 6. Remove old theme toggle JS (standalone), old lucide.createIcons() calls
    html = re.sub(r'<script>\s*lucide\.createIcons\(\);[\s\S]*?</script>', '', html)
    html = re.sub(r'document\.getElementById\(\'theme-toggle\'\)\.addEventListener[\s\S]*?;\s*\}[\s\)\;]*\n?', '', html)

    # 7. Inject shared CSS into <head> (before </head>)
    if SHARED_CSS not in html:
        html = html.replace('</head>', SHARED_CSS + '\n</head>', 1)

    # 8. Inject nav+sidebar right after <body ...>
    nav_sidebar = get_nav_sidebar(prefix)
    body_match = re.search(r'<body\b[^>]*>', html)
    if body_match:
        insert_pos = body_match.end()
        # Only inject if nav not already present
        if 'id="ds-nav"' not in html:
            html = html[:insert_pos] + '\n\n' + nav_sidebar + '\n\n' + html[insert_pos:]

    # 9. Fix main content: add left padding for sidebar on lg screens
    #    - Add lg:pl-64 pt-[57px] if not present
    def fix_main(m):
        tag = m.group(0)
        if 'lg:pl-64' not in tag:
            tag = tag.replace('<main ', '<main data-sb-padded="1" ')
            tag = re.sub(r'class="', 'class="lg:pl-64 ', tag)
        # Also fix top padding: ensure pt >= 16 (pt-16 = 64px)
        if 'pt-' not in tag:
            tag = re.sub(r'class="', 'class="pt-16 ', tag)
        return tag
    html = re.sub(r'<main\b[^>]*>', fix_main, html)

    # 10. Inject SHARED_JS before </body>
    if 'id="scroll-top"' not in html or SHARED_JS not in html:
        html = html.replace('</body>', SHARED_JS + '\n</body>', 1)

    # 11. Ensure theme init script is present
    theme_init = "<script>(function(){const s=localStorage.getItem('ds-theme');if(s==='light')document.documentElement.classList.remove('dark');else document.documentElement.classList.add('dark');})();</script>"
    if theme_init not in html and "ds-theme" not in html:
        html = html.replace('<head>', '<head>\n' + theme_init, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


# ---------------------------------------------------------------------------
# Fix practice.html specifically (it was dark-only, needs dual-theme)
# ---------------------------------------------------------------------------

def fix_practice_theme():
    path = 'pages/practice.html'
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace hardcoded dark body with dual-theme
    html = html.replace(
        'class="bg-slate-950 text-slate-200 min-h-screen"',
        'class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen transition-colors duration-300"'
    )
    # Replace dark-only grid-bg style
    html = html.replace(
        '.grid-bg{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:40px 40px;}',
        '.grid-bg{background-image:linear-gradient(rgba(0,0,0,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.05) 1px,transparent 1px);background-size:40px 40px;}\n        .dark .grid-bg{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);}'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


# ---------------------------------------------------------------------------
# Run all build scripts to regenerate sub-pages
# ---------------------------------------------------------------------------

def run_builders():
    builders = [
        'generate_pages.py',
        'build_bash_guide.py',
        'build_powershell_guide.py',
        'build_de_fundamentals.py',
        'build_dsa.py',
        'build_system_design.py',
        'build_pipeline_design.py',
    ]
    for script in builders:
        if os.path.exists(script):
            print(f"  Running {script}...")
            # Run but suppress the inject_sidebar_into_all_html that was appended
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    WARNING: {script} returned {result.returncode}")
                print(result.stderr[-500:] if result.stderr else '')
            else:
                print(f"    OK")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)

    print("Step 1: Fixing practice.html theme...")
    fix_practice_theme()

    print("Step 2: Running all build scripts...")
    run_builders()

    print("Step 3: Patching all HTML files with new nav/sidebar/scroll-top...")
    all_html = glob.glob('**/*.html', recursive=True)
    # Exclude node_modules etc.
    all_html = [p for p in all_html if 'node_modules' not in p]
    for path in sorted(all_html):
        try:
            patch_html(path)
            print(f"  Patched: {path}")
        except Exception as e:
            print(f"  ERROR patching {path}: {e}")

    print(f"\nDone. Patched {len(all_html)} HTML files.")
    print("Sidebar links all use absolute paths from root so they're correct at any depth.")
