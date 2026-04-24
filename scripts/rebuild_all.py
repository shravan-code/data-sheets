"""
rebuild_all.py
==============
Organizes the build process and patches all HTML files to use the shared layout.
"""

import os, re, glob, subprocess, sys

# ---------------------------------------------------------------------------
# NAV + SIDEBAR HTML  (prefix = relative path back to project root)
# ---------------------------------------------------------------------------

def get_nav_sidebar(prefix, page_title=""):
    return f"""\
<!-- NAV -->
<nav id="ds-nav" class="fixed top-0 w-full z-50 bg-white/95 dark:bg-slate-950/95 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="px-4 md:px-6 py-3.5 flex items-center">
        <!-- LEFT: Sidebar Toggle -->
        <div class="flex-1 flex items-center">
            <button id="sidebar-toggle" aria-label="Toggle sidebar">
                <span class="line"></span>
                <span class="line"></span>
            </button>
        </div>

        <!-- CENTER: Logo and Page Title -->
        <div class="flex-none flex items-center justify-center gap-3 md:gap-4 mx-4">
            <a href="{prefix}index.html" class="no-underline group flex items-center gap-3 transition-transform duration-300 group-hover:scale-105">
                <div class="flex items-center">
                    <span style="font-family: 'Outfit', sans-serif;" class="text-[28px] tracking-tighter flex items-center">
                        <span class="font-light text-slate-500 dark:text-slate-400">Data</span>
                        <span class="font-black bg-gradient-to-br from-indigo-600 via-blue-600 to-emerald-500 dark:from-indigo-400 dark:via-blue-400 dark:to-emerald-300 bg-clip-text text-transparent ml-1.5 inline-block -rotate-3 origin-bottom-left">Cake</span>
                    </span>
                </div>
            </a>
            {f'''<div class="hidden sm:flex items-center gap-3">
                <div class="h-4 w-[1px] bg-slate-200 dark:bg-slate-800"></div>
                <span class="text-sm font-semibold text-slate-500 dark:text-slate-400 whitespace-nowrap">
                    {page_title}
                </span>
            </div>''' if page_title else ''}
        </div>

        <!-- RIGHT: Theme Toggle -->
        <div class="flex-1 flex justify-end">
            <button id="theme-toggle" title="Toggle theme"
                class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/70 transition-all">
                <i data-lucide="sun"  class="w-[18px] h-[18px] hidden dark:block"></i>
                <i data-lucide="moon" class="w-[18px] h-[18px] block dark:hidden"></i>
            </button>
        </div>
    </div>
</nav>

<!-- SIDEBAR OVERLAY (mobile) -->
<div id="sidebar-overlay"
    class="fixed inset-0 bg-black/50 backdrop-blur-[2px] z-40 opacity-0 pointer-events-none transition-opacity duration-300"></div>

<!-- SIDEBAR -->
<aside id="ds-sidebar"
    class="sidebar-hidden fixed top-[57px] left-0 h-[calc(100vh-57px)] w-60 z-40 overflow-y-auto
           bg-white dark:bg-[#0c111d] border-r border-slate-200/80 dark:border-slate-800/60
           shadow-xl shadow-slate-200/50 dark:shadow-slate-950/80">

    <div class="h-0.5 w-full bg-gradient-to-r from-blue-500 via-violet-500 to-rose-500"></div>

    <div class="py-5 px-3 flex flex-col h-full">
        <div class="flex-1">
            <a href="{prefix}pages/learn.html" class="sb-section bg-blue-50 dark:bg-blue-500/10 text-blue-700 dark:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-500/20">
                <span class="w-6 h-6 rounded-md bg-blue-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="book-open" class="w-3 h-3 text-white"></i>
                </span>
                Learn
            </a>

            <div class="sb-cat text-blue-500 dark:text-blue-400">Programming</div>
            <nav>
                <a href="{prefix}pages/learn/python.html"     class="sb-link"><i data-lucide="code-2"       class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>Python</a>
                <a href="{prefix}pages/learn/sql.html"        class="sb-link"><i data-lucide="database"     class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>SQL</a>
                <a href="{prefix}pages/learn/bash.html"       class="sb-link"><i data-lucide="terminal"     class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>Bash</a>
                <a href="{prefix}pages/learn/powershell.html" class="sb-link"><i data-lucide="terminal-square" class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>PowerShell</a>
            </nav>

            <div class="sb-cat text-emerald-500 dark:text-emerald-400">Concepts</div>
            <nav>
                <a href="{prefix}pages/learn/de-fundamentals.html" class="sb-link"><i data-lucide="layers"       class="w-3.5 h-3.5 text-emerald-400 flex-shrink-0"></i>DE Fundamentals</a>
                <a href="{prefix}pages/learn/dsa-de.html"          class="sb-link"><i data-lucide="git-branch-plus" class="w-3.5 h-3.5 text-emerald-400 flex-shrink-0"></i>DSA for DE</a>
            </nav>

            <div class="sb-cat text-orange-500 dark:text-orange-400">Tools</div>
            <nav>
                <a href="{prefix}pages/learn/spark.html"   class="sb-link"><i data-lucide="zap"      class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Spark</a>
                <a href="{prefix}pages/learn/flink.html"   class="sb-link"><i data-lucide="activity" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Flink</a>
                <a href="{prefix}pages/learn/kafka.html"   class="sb-link"><i data-lucide="radio"    class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Kafka</a>
                <a href="{prefix}pages/learn/dbt.html"     class="sb-link"><i data-lucide="blocks"   class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>dbt</a>
                <a href="{prefix}pages/learn/pandas.html"  class="sb-link"><i data-lucide="table-2"  class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Pandas</a>
                <a href="{prefix}pages/learn/numpy.html"   class="sb-link"><i data-lucide="hash"     class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>NumPy</a>
                <a href="{prefix}pages/learn/airflow.html" class="sb-link"><i data-lucide="wind"     class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Airflow</a>
            </nav>

            <div class="sb-cat text-cyan-500 dark:text-cyan-400">Cloud</div>
            <nav>
                <a href="{prefix}pages/learn/aws.html"        class="sb-link"><i data-lucide="cloud"         class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>AWS</a>
                <a href="{prefix}pages/learn/gcp.html"        class="sb-link"><i data-lucide="cloud-sun"     class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>GCP</a>
                <a href="{prefix}pages/learn/azure.html"      class="sb-link"><i data-lucide="cloud-cog"     class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Azure</a>
                <a href="{prefix}pages/learn/snowflake.html"  class="sb-link"><i data-lucide="snowflake"     class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Snowflake</a>
                <a href="{prefix}pages/learn/databricks.html" class="sb-link"><i data-lucide="box"           class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Databricks</a>
            </nav>

            <div class="sb-cat text-violet-500 dark:text-violet-400">CI / CD</div>
            <nav>
                <a href="{prefix}pages/learn/docker.html"     class="sb-link"><i data-lucide="container"     class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Docker</a>
                <a href="{prefix}pages/learn/kubernetes.html" class="sb-link"><i data-lucide="network"       class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Kubernetes</a>
                <a href="{prefix}pages/learn/terraform.html"  class="sb-link"><i data-lucide="sliders"       class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Terraform</a>
                <a href="{prefix}pages/learn/github.html"     class="sb-link"><i data-lucide="git-branch"    class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>GitHub</a>
            </nav>

            <div class="sb-cat text-rose-500 dark:text-rose-400">Design</div>
            <nav>
                <a href="{prefix}pages/learn/system-design.html"   class="sb-link"><i data-lucide="layout-dashboard" class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>System Design</a>
                <a href="{prefix}pages/learn/pipeline-design.html" class="sb-link"><i data-lucide="workflow"          class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>Pipeline Design</a>
                <a href="{prefix}pages/learn/de-architectures.html" class="sb-link"><i data-lucide="cpu"             class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>DE Architectures</a>
            </nav>

            <div class="mt-5 mb-1 border-t border-slate-200 dark:border-slate-800/60 pt-5">
                <a href="{prefix}pages/practice.html" class="sb-section bg-violet-50 dark:bg-violet-500/10 text-violet-700 dark:text-violet-300 hover:bg-violet-100 dark:hover:bg-violet-500/20">
                    <span class="w-6 h-6 rounded-md bg-violet-500 flex items-center justify-center flex-shrink-0">
                        <i data-lucide="hammer" class="w-3 h-3 text-white"></i>
                    </span>
                    Practice
                    <span class="ml-auto text-[10px] bg-violet-100 dark:bg-violet-500/20 text-violet-600 dark:text-violet-300 px-1.5 py-0.5 rounded-full font-semibold">Soon</span>
                </a>
            </div>
        </div>

        <div class="portfolio-link mt-auto">
            <a href="{prefix}pages/portfolio.html" class="sb-link">
                <i data-lucide="user" class="w-3.5 h-3.5 flex-shrink-0"></i>
                My Portfolio
                <i data-lucide="external-link" class="w-2.5 h-2.5 ml-auto opacity-50"></i>
            </a>
        </div>
    </div>
</aside>

<button id="scroll-top" title="Back to top"
    class="fixed bottom-6 right-6 z-50 w-10 h-10 flex items-center justify-center rounded-full
           bg-gradient-to-br from-blue-500 to-violet-600 text-white
           shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-110 scale-90 transition-all duration-200">
    <i data-lucide="arrow-up" class="w-4 h-4"></i>
</button>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compute_prefix(html_path):
    norm = html_path.replace('\\', '/')
    # For scripts/rebuild_all.py, the root is ../
    # But if we run from root, it's different.
    # Let's assume we run from the project root.
    depth = len(norm.split('/')) - 1
    return '../' * depth


def patch_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    prefix = compute_prefix(os.path.relpath(path).replace('\\', '/'))

    # 1. Cleanup old injections (aggressive)
    html = re.sub(r'<!-- NAV -->.*?<!-- SIDEBAR OVERLAY \(mobile\) -->', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*═+\s*SIDEBAR\s*═+\s*-->.*?<!--\s*SCROLL TO TOP\s*-->', '', html, flags=re.DOTALL)
    html = re.sub(r'<!-- SIDEBAR -->.*?</aside>', '', html, flags=re.DOTALL)
    html = re.sub(r'<nav\s+id="ds-nav".*?>.*?</nav>', '', html, flags=re.DOTALL)
    html = re.sub(r'<aside id="ds-sidebar"\b[^>]*?>.*?</aside>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div id="sidebar-overlay"[^>]*?>.*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<button id="scroll-top"[^>]*?>.*?</button>', '', html, flags=re.DOTALL)
    
    # Remove any stray Lucide initialization scripts or layout-fixes if they are redundant
    html = re.sub(r'<script src="[^"]*layout-fixes\.js"[^>]*></script>', '', html)
    html = re.sub(r'<link rel="stylesheet" href="[^"]*layout-fixes\.css">', '', html)
    
    # Remove inline styles and scripts previously injected
    html = re.sub(r'<style>\s*/\* DS_SHARED_SIDEBAR_STYLES \*/.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*\(function\(\)\s*{\s*const html\s*=\s*document\.documentElement;.*?</script>', '', html, flags=re.DOTALL)

    # 1.5 Extract Page Title for Nav
    # Try to get first part of title (before | or —)
    title_match = re.search(r'<title>(.*?)</title>', html)
    page_title = ""
    if title_match:
        full_title = title_match.group(1).split('|')[0].split('—')[0].strip()
        # Hide title on homepage only
        if 'index.html' not in path:
            page_title = full_title

    # 2. Inject External CSS and PWA Manifest if not present
    css_tag = f'<link rel="stylesheet" href="{prefix}css/ds-main.css">'
    pwa_tags = f'<link rel="manifest" href="{prefix}manifest.json">\n    <meta name="theme-color" content="#ffffff">'
    
    if 'ds-main.css' not in html:
        html = html.replace('</head>', css_tag + '\n</head>', 1)
    else:
        # Update existing link to correct prefix
        html = re.sub(r'<link rel="stylesheet" href="[^"]*ds-main.css">', css_tag, html)

    if 'manifest.json' not in html:
        html = html.replace('</head>', pwa_tags + '\n</head>', 1)

    # 3. Inject Nav + Sidebar after <body>
    body_match = re.search(r'<body\b[^>]*>', html)
    if body_match:
        pos = body_match.end()
        html = html[:pos] + '\n\n' + get_nav_sidebar(prefix, page_title) + '\n\n' + html[pos:]

    # 4. Wrap main content if needed
    if 'id="ds-main-content"' not in html:
        html = re.sub(r'(<main\b[^>]*>)', r'<div id="ds-main-content" class="transition-all duration-300 w-full min-w-0">\1', html)
        html = html.replace('</main>', '</main>\n</div>', 1)

    # 4.5 Fix flex container centering bug on mobile
    html = html.replace('class="flex justify-center max-w-[1440px] mx-auto"', 'class="flex justify-center max-w-[1440px] mx-auto w-full"')

    # 5. Inject External JS if not present
    js_tag = f'<script src="{prefix}js/ds-main.js" defer></script>'
    if 'ds-main.js' not in html:
        if '</body>' in html:
            html = html.replace('</body>', js_tag + '\n</body>', 1)
        else:
            html += js_tag
    else:
        # Update existing script to correct prefix
        html = re.sub(r'<script src="[^"]*ds-main.js"[^>]*></script>', js_tag, html)

    # 6. Ensure theme init script is at the top of head
    theme_init = """<script>(function(){
        const s=localStorage.getItem('ds-theme');
        const isL = s==='light';
        if(isL) document.documentElement.classList.remove('dark');
        else document.documentElement.classList.add('dark');
        
        // Immediate Prism theme sync
        window.addEventListener('DOMContentLoaded', () => {
            const l = document.getElementById('prism-theme-light');
            const d = document.getElementById('prism-theme-dark');
            if(l && d) {
                l.disabled = !isL;
                d.disabled = isL;
            }
        });
    })();</script>"""
    if 'localStorage.getItem(\'ds-theme\')' not in html:
        html = html.replace('<head>', '<head>\n' + theme_init, 1)

    # 7. Adaptive Code Blocks (Prism)
    prism_light = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css"
    prism_dark = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css"
    
    # Replace existing prism link with adaptive pair
    prism_match = re.search(r'<link rel="stylesheet" href="[^"]*prism[^"]*\.css">', html)
    if prism_match:
        adaptive_prism = f'<link id="prism-theme-light" rel="stylesheet" href="{prism_light}" disabled>\n    <link id="prism-theme-dark" rel="stylesheet" href="{prism_dark}">'
        html = html[:prism_match.start()] + adaptive_prism + html[prism_match.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def run_builders():
    # Builders are now in scripts/
    builders = [
        'generate_pages.py', 'build_bash_guide.py', 'build_powershell_guide.py',
        'build_de_fundamentals.py', 'build_dsa.py', 'build_system_design.py', 'build_pipeline_design.py',
    ]
    for script in builders:
        script_path = os.path.join('scripts', script)
        if os.path.exists(script_path):
            print(f"  Running {script}...")
            # We run from root so scripts need to know where data is
            r = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            if r.returncode != 0:
                print(f"    WARN: {script} failed:\n{r.stderr[-500:]}")
            else:
                print(f"    OK")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Ensure we are in the root directory (one level up from scripts/)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)

    print(f"Working directory: {os.getcwd()}")

    print("Step 1: Regenerate sub-pages...")
    run_builders()

    print("Step 2: Patch all HTML files...")
    all_html = [p for p in glob.glob('**/*.html', recursive=True) if 'node_modules' not in p and 'components' not in p]
    for path in sorted(all_html):
        try:
            patch_html(path)
            print(f"  OK: {path}")
        except Exception as e:
            print(f"  ERR: {path}: {e}")

    print(f"\nDone — {len(all_html)} files patched.")
