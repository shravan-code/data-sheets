"""
rebuild_all.py
==============
Injects unified nav + redesigned sidebar + scroll-to-top into every HTML file.
Run: python rebuild_all.py
"""

import os, re, glob, subprocess, sys

# ---------------------------------------------------------------------------
# SHARED CSS
# ---------------------------------------------------------------------------

SHARED_CSS = """\
    <style>
        body{font-family:'Inter',sans-serif;}
        h1,h2,h3,.font-display{font-family:'Outfit',sans-serif;}
        .grid-bg{background-image:linear-gradient(rgba(0,0,0,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.05) 1px,transparent 1px);background-size:40px 40px;}
        .dark .grid-bg{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);}

        /* ── Sidebar ────────────────────────────────── */
        #ds-sidebar{
            scrollbar-width:thin;
            scrollbar-color:#e2e8f0 transparent;
            transition:transform 0.3s cubic-bezier(.4,0,.2,1),opacity 0.3s;
        }
        .dark #ds-sidebar{scrollbar-color:#1e293b transparent;}
        #ds-sidebar::-webkit-scrollbar{width:3px;}
        #ds-sidebar::-webkit-scrollbar-track{background:transparent;}
        #ds-sidebar::-webkit-scrollbar-thumb{background:#e2e8f0;border-radius:999px;}
        .dark #ds-sidebar::-webkit-scrollbar-thumb{background:#1e293b;}

        /* sidebar hidden = translate-x-full; visible = translate-x-0 */
        #ds-sidebar.sidebar-hidden{transform:translateX(-100%);}
        #ds-sidebar.sidebar-visible{transform:translateX(0);}

        /* shift main when sidebar is visible on desktop */
        @media(min-width:1024px){
            body.sidebar-open #ds-main-content{padding-left:16rem;}
        }

        /* sidebar nav links */
        .sb-link{
            display:flex;align-items:center;gap:8px;padding:6px 10px;
            border-radius:8px;font-size:.8125rem;font-weight:500;
            color:#475569;text-decoration:none;
            transition:background 0.15s,color 0.15s;
        }
        .sb-link:hover{background:#f1f5f9;color:#0f172a;}
        .dark .sb-link{color:#94a3b8;}
        .dark .sb-link:hover{background:#1e293b;color:#f1f5f9;}

        /* category labels */
        .sb-cat{
            display:flex;align-items:center;gap:6px;
            font-size:.65rem;font-weight:700;letter-spacing:.1em;
            text-transform:uppercase;padding:0 10px;margin:16px 0 4px;
        }
        .sb-cat::before{content:'';flex:1;height:1px;background:currentColor;opacity:.2;}
        .sb-cat::after{content:'';flex:3;height:1px;background:currentColor;opacity:.2;}

        /* section headers */
        .sb-section{
            display:flex;align-items:center;gap:8px;
            padding:8px 10px;border-radius:10px;
            font-size:.8125rem;font-weight:700;letter-spacing:.03em;
            text-decoration:none;margin-bottom:4px;
            transition:background 0.15s,color 0.15s;
        }
        .sb-section:hover{opacity:.85;}

        /* Scroll-to-top */
        #scroll-top{opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;}
        #scroll-top.visible{opacity:1;pointer-events:auto;transform:scale(1);}

        /* card hover */
        .topic-card{transition:all 0.25s cubic-bezier(.4,0,.2,1);}
        .topic-card:hover{transform:translateY(-4px);}
        .dark .topic-card:hover{box-shadow:0 20px 40px rgba(0,0,0,.5),0 0 20px rgba(59,130,246,.12);border-color:rgba(96,165,250,.3);}
        .topic-card:hover{box-shadow:0 20px 40px rgba(0,0,0,.08);border-color:rgba(96,165,250,.3);}

        /* prose */
        .prose h2{margin-top:2.5rem;margin-bottom:1.25rem;font-weight:700;color:inherit;font-size:2.25rem;letter-spacing:-.02em;}
        .prose h3{margin-top:2rem;margin-bottom:1rem;font-weight:600;color:inherit;font-size:1.6rem;letter-spacing:-.01em;}
        .prose p{margin-bottom:1.25rem;line-height:1.8;opacity:.9;}
        .prose ul{list-style-type:disc;padding-left:1.5rem;margin-bottom:1.25rem;}
        .prose li{margin-bottom:.6rem;}
        .prose code{background:rgba(0,0,0,.05);padding:.2rem .4rem;border-radius:.25rem;font-size:.875em;font-weight:500;}
        .dark .prose code{background:rgba(255,255,255,.1);}
    </style>"""

# ---------------------------------------------------------------------------
# NAV + SIDEBAR HTML  (prefix = relative path back to project root)
# ---------------------------------------------------------------------------

def get_nav_sidebar(prefix):
    return f"""\
<!-- NAV -->
<nav id="ds-nav" class="fixed top-0 w-full z-50 bg-white/95 dark:bg-slate-950/95 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="px-4 md:px-6 py-3.5 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <!-- Toggle button: shows menu/x icon -->
            <button id="sidebar-toggle" aria-label="Toggle sidebar"
                class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/70 transition-all duration-200 relative">
                <i id="sb-icon-open"  data-lucide="layout-sidebar" class="w-[18px] h-[18px] absolute transition-all duration-200"></i>
                <i id="sb-icon-close" data-lucide="sidebar-close"  class="w-[18px] h-[18px] absolute transition-all duration-200 opacity-0 scale-75"></i>
            </button>
            <a href="{prefix}index.html" class="no-underline flex items-center gap-2">
                <span class="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center">
                    <i data-lucide="database" class="w-3.5 h-3.5 text-white"></i>
                </span>
                <span style="font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:-.02em;"
                    class="text-lg text-slate-900 dark:text-white">Data Sheets</span>
            </a>
        </div>
        <button id="theme-toggle" title="Toggle theme"
            class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/70 transition-all">
            <i data-lucide="sun"  class="w-[18px] h-[18px] hidden dark:block"></i>
            <i data-lucide="moon" class="w-[18px] h-[18px] block dark:hidden"></i>
        </button>
    </div>
</nav>

<!-- SIDEBAR OVERLAY (mobile) -->
<div id="sidebar-overlay"
    class="fixed inset-0 bg-black/50 backdrop-blur-[2px] z-40 opacity-0 pointer-events-none transition-opacity duration-300"></div>

<!-- ═══════════════════════════ SIDEBAR ═══════════════════════════ -->
<aside id="ds-sidebar"
    class="sidebar-hidden fixed top-[57px] left-0 h-[calc(100vh-57px)] w-60 z-40 overflow-y-auto
           bg-white dark:bg-[#0c111d] border-r border-slate-200/80 dark:border-slate-800/60
           shadow-xl shadow-slate-200/50 dark:shadow-slate-950/80">

    <!-- Gradient accent bar at top -->
    <div class="h-0.5 w-full bg-gradient-to-r from-blue-500 via-violet-500 to-rose-500"></div>

    <div class="py-5 px-3">

        <!-- ── LEARN section ── -->
        <a href="{prefix}pages/learn.html" class="sb-section bg-blue-50 dark:bg-blue-500/10 text-blue-700 dark:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-500/20">
            <span class="w-6 h-6 rounded-md bg-blue-500 flex items-center justify-center flex-shrink-0">
                <i data-lucide="book-open" class="w-3 h-3 text-white"></i>
            </span>
            Learn
        </a>

        <!-- Programming -->
        <div class="sb-cat text-blue-500 dark:text-blue-400">Programming</div>
        <nav>
            <a href="{prefix}pages/learn/python.html"     class="sb-link"><i data-lucide="code-2"       class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>Python</a>
            <a href="{prefix}pages/learn/sql.html"        class="sb-link"><i data-lucide="database"     class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>SQL</a>
            <a href="{prefix}pages/learn/bash.html"       class="sb-link"><i data-lucide="terminal"     class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>Bash</a>
            <a href="{prefix}pages/learn/powershell.html" class="sb-link"><i data-lucide="terminal-square" class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>PowerShell</a>
        </nav>

        <!-- Concepts -->
        <div class="sb-cat text-emerald-500 dark:text-emerald-400">Concepts</div>
        <nav>
            <a href="{prefix}pages/learn/de-fundamentals.html" class="sb-link"><i data-lucide="layers"       class="w-3.5 h-3.5 text-emerald-400 flex-shrink-0"></i>DE Fundamentals</a>
            <a href="{prefix}pages/learn/dsa-de.html"          class="sb-link"><i data-lucide="git-branch-plus" class="w-3.5 h-3.5 text-emerald-400 flex-shrink-0"></i>DSA for DE</a>
        </nav>

        <!-- Tools -->
        <div class="sb-cat text-orange-500 dark:text-orange-400">Tools</div>
        <nav>
            <a href="{prefix}pages/learn/spark.html"   class="sb-link"><i data-lucide="zap"      class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Spark</a>
            <a href="{prefix}pages/learn/flink.html"   class="sb-link"><i data-lucide="activity" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Flink</a>
            <a href="{prefix}pages/learn/kafka.html"   class="sb-link"><i data-lucide="radio"    class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Kafka</a>
            <a href="{prefix}pages/learn/dbt.html"     class="sb-link"><i data-lucide="blocks"   class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>dbt</a>
            <a href="{prefix}pages/learn/pandas.html"  class="sb-link"><i data-lucide="table-2"  class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Pandas</a>
            <a href="{prefix}pages/learn/numpy.html"   class="sb-link"><i data-lucide="sigma"    class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>NumPy</a>
            <a href="{prefix}pages/learn/airflow.html" class="sb-link"><i data-lucide="wind"     class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Airflow</a>
        </nav>

        <!-- Cloud -->
        <div class="sb-cat text-cyan-500 dark:text-cyan-400">Cloud</div>
        <nav>
            <a href="{prefix}pages/learn/aws.html"        class="sb-link"><i data-lucide="cloud"         class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>AWS</a>
            <a href="{prefix}pages/learn/gcp.html"        class="sb-link"><i data-lucide="cloud-sun"     class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>GCP</a>
            <a href="{prefix}pages/learn/azure.html"      class="sb-link"><i data-lucide="cloud-cog"     class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Azure</a>
            <a href="{prefix}pages/learn/snowflake.html"  class="sb-link"><i data-lucide="snowflake"     class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Snowflake</a>
            <a href="{prefix}pages/learn/databricks.html" class="sb-link"><i data-lucide="box"           class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Databricks</a>
        </nav>

        <!-- CI/CD -->
        <div class="sb-cat text-violet-500 dark:text-violet-400">CI / CD</div>
        <nav>
            <a href="{prefix}pages/learn/docker.html"     class="sb-link"><i data-lucide="container"     class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Docker</a>
            <a href="{prefix}pages/learn/kubernetes.html" class="sb-link"><i data-lucide="network"       class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Kubernetes</a>
            <a href="{prefix}pages/learn/terraform.html"  class="sb-link"><i data-lucide="sliders"       class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Terraform</a>
            <a href="{prefix}pages/learn/github.html"     class="sb-link"><i data-lucide="git-branch"    class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>GitHub</a>
        </nav>

        <!-- Design -->
        <div class="sb-cat text-rose-500 dark:text-rose-400">Design</div>
        <nav>
            <a href="{prefix}pages/learn/system-design.html"   class="sb-link"><i data-lucide="layout-dashboard" class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>System Design</a>
            <a href="{prefix}pages/learn/pipeline-design.html" class="sb-link"><i data-lucide="workflow"          class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>Pipeline Design</a>
            <a href="{prefix}pages/learn/de-architectures.html" class="sb-link"><i data-lucide="cpu"             class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>DE Architectures</a>
        </nav>

        <!-- ── PRACTICE section ── -->
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
</aside>

<!-- SCROLL TO TOP -->
<button id="scroll-top" title="Back to top"
    class="fixed bottom-6 right-6 z-50 w-10 h-10 flex items-center justify-center rounded-full
           bg-gradient-to-br from-blue-500 to-violet-600 text-white
           shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-110 scale-90 transition-all duration-200">
    <i data-lucide="arrow-up" class="w-4 h-4"></i>
</button>"""


# ---------------------------------------------------------------------------
# SHARED JS  — theme, sidebar toggle (all screens), scroll-to-top
# ---------------------------------------------------------------------------

SHARED_JS = """\
<script>
(function() {
    const html  = document.documentElement;
    const body  = document.body;

    /* ── Theme ──────────────────────────────────── */
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = html.classList.toggle('dark');
            localStorage.setItem('ds-theme', isDark ? 'dark' : 'light');
        });
    }

    /* ── Sidebar state ───────────────────────────── */
    const sidebar  = document.getElementById('ds-sidebar');
    const overlay  = document.getElementById('sidebar-overlay');
    const togBtn   = document.getElementById('sidebar-toggle');
    const iconOpen  = document.getElementById('sb-icon-open');
    const iconClose = document.getElementById('sb-icon-close');

    // Restore persisted state (default: open on desktop, closed on mobile)
    const isDesktop = () => window.innerWidth >= 1024;
    const stored = localStorage.getItem('ds-sidebar');
    let sidebarOpen = stored !== null ? stored === 'open' : isDesktop();

    function applyState(animate) {
        if (!sidebar) return;
        if (sidebarOpen) {
            sidebar.classList.remove('sidebar-hidden');
            sidebar.classList.add('sidebar-visible');
            body.classList.add('sidebar-open');
            if (overlay) { overlay.style.opacity = '0'; overlay.style.pointerEvents = 'none'; }
            if (!isDesktop() && overlay) { overlay.style.opacity = '1'; overlay.style.pointerEvents = 'auto'; }
            if (iconOpen)  { iconOpen.style.opacity  = '0'; iconOpen.style.transform  = 'scale(.7)'; }
            if (iconClose) { iconClose.style.opacity = '1'; iconClose.style.transform = 'scale(1)'; }
        } else {
            sidebar.classList.add('sidebar-hidden');
            sidebar.classList.remove('sidebar-visible');
            body.classList.remove('sidebar-open');
            if (overlay) { overlay.style.opacity = '0'; overlay.style.pointerEvents = 'none'; }
            if (iconOpen)  { iconOpen.style.opacity  = '1'; iconOpen.style.transform  = 'scale(1)'; }
            if (iconClose) { iconClose.style.opacity = '0'; iconClose.style.transform = 'scale(.7)'; }
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

    // On resize: if going to desktop re-open by default if never set
    window.addEventListener('resize', () => {
        if (isDesktop() && localStorage.getItem('ds-sidebar') === null) {
            sidebarOpen = true;
            applyState(false);
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

    /* ── Lucide icons ────────────────────────────── */
    if (typeof lucide !== 'undefined') lucide.createIcons();
})();
</script>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compute_prefix(html_path):
    norm = html_path.replace('\\', '/')
    depth = len(norm.split('/')) - 1
    return '../' * depth


def patch_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    prefix = compute_prefix(os.path.relpath(path).replace('\\', '/'))

    # 1. Remove old nav
    html = re.sub(r'<nav\b[^>]*>.*?</nav>', '', html, flags=re.DOTALL)
    # 2. Remove old sidebar (any aside)
    html = re.sub(r'<!-- SIDEBAR -->.*?</aside>', '', html, flags=re.DOTALL)
    html = re.sub(r'<aside\b[^>]*>.*?</aside>', '', html, flags=re.DOTALL)
    # 3. Remove overlay
    html = re.sub(r'<div id="sidebar-overlay"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
    # 4. Remove old scroll-top button
    html = re.sub(r'<button id="scroll-top"[^>]*>.*?</button>', '', html, flags=re.DOTALL)
    # 5. Remove old wrapper divs
    html = re.sub(r'<div class="lg:pl-\d+ w-full">', '', html)
    # 6. Remove old inline JS blocks
    html = re.sub(r'<script>\s*lucide\.createIcons\(\);[\s\S]*?</script>', '', html)
    html = re.sub(r'<script>\s*\(function\(\)\s*\{[\s\S]*?ds-sidebar[\s\S]*?\}\)\(\);\s*</script>', '', html)

    # 7. Inject shared CSS
    if 'sidebar-hidden' not in html:
        html = html.replace('</head>', SHARED_CSS + '\n</head>', 1)

    # 8. Inject nav+sidebar after <body>
    if 'id="ds-nav"' not in html:
        body_match = re.search(r'<body\b[^>]*>', html)
        if body_match:
            pos = body_match.end()
            html = html[:pos] + '\n\n' + get_nav_sidebar(prefix) + '\n\n' + html[pos:]

    # 9. Wrap main content so it gets padding-left when sidebar opens on desktop
    #    Inject a wrapper div id="ds-main-content" around <main> if not already there
    if 'id="ds-main-content"' not in html:
        html = re.sub(r'(<main\b[^>]*>)', r'<div id="ds-main-content" class="transition-all duration-300">\1', html)
        html = html.replace('</main>', '</main>\n</div>', 1)

    # 10. Ensure top padding on main (nav height ~57px)
    def fix_main(m):
        tag = m.group(0)
        if 'pt-' not in tag:
            tag = re.sub(r'class="', 'class="pt-16 ', tag)
        return tag
    html = re.sub(r'<main\b[^>]*>', fix_main, html)

    # 11. Inject shared JS before </body>
    if 'ds-sidebar-state' not in html:
        html = html.replace('</body>', SHARED_JS + '\n</body>', 1)

    # 12. Theme init
    theme_init = "<script>(function(){const s=localStorage.getItem('ds-theme');if(s==='light')document.documentElement.classList.remove('dark');else document.documentElement.classList.add('dark');})();</script>"
    if 'ds-theme' not in html:
        html = html.replace('<head>', '<head>\n' + theme_init, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def fix_practice_theme():
    path = 'pages/practice.html'
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace(
        'class="bg-slate-950 text-slate-200 min-h-screen"',
        'class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen transition-colors duration-300"'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def run_builders():
    builders = [
        'generate_pages.py', 'build_bash_guide.py', 'build_powershell_guide.py',
        'build_de_fundamentals.py', 'build_dsa.py', 'build_system_design.py', 'build_pipeline_design.py',
    ]
    for script in builders:
        if os.path.exists(script):
            print(f"  Running {script}...")
            r = subprocess.run([sys.executable, script], capture_output=True, text=True)
            print(f"    {'OK' if r.returncode == 0 else 'WARN: ' + r.stderr[-200:]}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)

    print("Step 1: Fix practice.html theme...")
    fix_practice_theme()

    print("Step 2: Regenerate sub-pages...")
    run_builders()

    print("Step 3: Patch all HTML files...")
    all_html = [p for p in glob.glob('**/*.html', recursive=True) if 'node_modules' not in p]
    for path in sorted(all_html):
        try:
            patch_html(path)
            print(f"  OK: {path}")
        except Exception as e:
            print(f"  ERR: {path}: {e}")

    print(f"\nDone — {len(all_html)} files patched.")
