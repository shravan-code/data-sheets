import os
import glob
import re

NAV_SIDEBAR_CODE = """
# Common Layout Template
def get_layout(prefix):
    return f'''
<style>
    .custom-scrollbar::-webkit-scrollbar {{ width: 6px; }}
    .custom-scrollbar::-webkit-scrollbar-track {{ background: transparent; }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 10px; }}
    .dark .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #334155; }}
</style>

<nav class="fixed top-0 w-full z-50 bg-white/90 dark:bg-slate-950/90 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
        <div class="flex items-center gap-4">
            <button id="mobile-menu-btn" class="lg:hidden w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
                <i data-lucide="menu" class="w-5 h-5"></i>
            </button>
            <a href="{prefix}index.html" class="no-underline"><span style="font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:-.02em;" class="text-base md:text-xl text-slate-900 dark:text-slate-100 transition-colors duration-300">Data Sheets</span></a>
        </div>
        <button id="theme-toggle" class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
            <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
            <i data-lucide="moon" class="w-5 h-5 block dark:hidden"></i>
        </button>
    </div>
</nav>

<!-- SIDEBAR -->
<aside id="sidebar" class="fixed top-[60px] md:top-[72px] left-0 h-[calc(100vh-60px)] md:h-[calc(100vh-72px)] w-64 border-r border-slate-200 dark:border-slate-800/60 bg-white dark:bg-slate-950 z-40 transform -translate-x-full lg:translate-x-0 transition-transform duration-300 overflow-y-auto py-8 px-6 custom-scrollbar">
    <div class="mb-8">
        <a href="{prefix}pages/learn.html" class="font-display font-bold text-slate-900 dark:text-white mb-4 text-sm uppercase tracking-wider block no-underline hover:text-blue-600 dark:hover:text-blue-400">Learn</a>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-blue-600 dark:text-blue-400 mb-2 uppercase tracking-wider">Programming</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/python.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Python</a></li>
                <li><a href="{prefix}pages/learn/sql.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">SQL</a></li>
                <li><a href="{prefix}pages/learn/bash.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Bash</a></li>
                <li><a href="{prefix}pages/learn/powershell.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">PowerShell</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 mb-2 uppercase tracking-wider">Concepts</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/de-fundamentals.html" class="hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors no-underline">DE Fundamentals</a></li>
                <li><a href="{prefix}pages/learn/dsa-de.html" class="hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors no-underline">DSA for DE</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-orange-600 dark:text-orange-400 mb-2 uppercase tracking-wider">Tools</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/spark.html" class="hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Spark</a></li>
                <li><a href="{prefix}pages/learn/flink.html" class="hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Flink</a></li>
                <li><a href="{prefix}pages/learn/kafka.html" class="hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Kafka</a></li>
                <li><a href="{prefix}pages/learn/dbt.html" class="hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">dbt</a></li>
                <li><a href="{prefix}pages/learn/pandas.html" class="hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Pandas</a></li>
                <li><a href="{prefix}pages/learn/numpy.html" class="hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">NumPy</a></li>
                <li><a href="{prefix}pages/learn/airflow.html" class="hover:text-orange-600 dark:hover:text-orange-400 transition-colors no-underline">Airflow</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-cyan-600 dark:text-cyan-400 mb-2 uppercase tracking-wider">Cloud</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/aws.html" class="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">AWS</a></li>
                <li><a href="{prefix}pages/learn/gcp.html" class="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">GCP</a></li>
                <li><a href="{prefix}pages/learn/azure.html" class="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">Azure</a></li>
                <li><a href="{prefix}pages/learn/snowflake.html" class="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">Snowflake</a></li>
                <li><a href="{prefix}pages/learn/databricks.html" class="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors no-underline">Databricks</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-violet-600 dark:text-violet-400 mb-2 uppercase tracking-wider">CI/CD</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/docker.html" class="hover:text-violet-600 dark:hover:text-violet-400 transition-colors no-underline">Docker</a></li>
                <li><a href="{prefix}pages/learn/kubernetes.html" class="hover:text-violet-600 dark:hover:text-violet-400 transition-colors no-underline">Kubernetes</a></li>
                <li><a href="{prefix}pages/learn/terraform.html" class="hover:text-violet-600 dark:hover:text-violet-400 transition-colors no-underline">Terraform</a></li>
                <li><a href="{prefix}pages/learn/github.html" class="hover:text-violet-600 dark:hover:text-violet-400 transition-colors no-underline">GitHub</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-rose-600 dark:text-rose-400 mb-2 uppercase tracking-wider">Design</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}pages/learn/system-design.html" class="hover:text-rose-600 dark:hover:text-rose-400 transition-colors no-underline">System Design</a></li>
                <li><a href="{prefix}pages/learn/pipeline-design.html" class="hover:text-rose-600 dark:hover:text-rose-400 transition-colors no-underline">Pipeline Design</a></li>
                <li><a href="{prefix}pages/learn/de-architectures.html" class="hover:text-rose-600 dark:hover:text-rose-400 transition-colors no-underline">DE Architectures</a></li>
            </ul>
        </div>
    </div>
    <div>
        <a href="{prefix}pages/practice.html" class="font-display font-bold text-slate-900 dark:text-white mb-4 text-sm uppercase tracking-wider block no-underline hover:text-blue-600 dark:hover:text-blue-400">Practice</a>
        <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
            <li><a href="{prefix}pages/practice.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Coming Soon</a></li>
        </ul>
    </div>
</aside>

<!-- Overlay for mobile -->
<div id="sidebar-overlay" class="fixed inset-0 bg-slate-900/50 dark:bg-black/50 z-30 hidden lg:hidden backdrop-blur-sm transition-opacity opacity-0"></div>
'''

JS_CODE = '''
<script>
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if(btn && sidebar && overlay) {
        btn.addEventListener('click', () => {
            sidebar.classList.toggle('-translate-x-full');
            overlay.classList.toggle('hidden');
            setTimeout(() => overlay.classList.toggle('opacity-0'), 10);
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('opacity-0');
            setTimeout(() => overlay.classList.add('hidden'), 300);
        });
    }
});
</script>
'''
"""

def update_python_files():
    py_files = glob.glob('build_*.py') + ['generate_pages.py']
    for f in py_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove the old inject_sidebar_into_all_html and its call
        if 'def inject_sidebar_into_all_html():' in content:
            content = content[:content.find('def inject_sidebar_into_all_html():')]
        content = re.sub(r'inject_sidebar_into_all_html\(\)\s*', '', content)
        
        # Replace NAV_TEMPLATE with get_layout
        if 'NAV_TEMPLATE =' in content:
            # We remove NAV_TEMPLATE = """...""" completely.
            content = re.sub(r'NAV_TEMPLATE\s*=\s*\"\"\"[\s\S]*?\"\"\"', '', content)
        
        if 'def get_layout' not in content:
            content = NAV_SIDEBAR_CODE + "\n\n" + content

        # Now replace {NAV_HTML} with {LAYOUT_HTML}
        content = content.replace('{NAV_HTML}', '{LAYOUT_HTML}')
        content = content.replace('nav_html = NAV_TEMPLATE.replace("{ROOT_PATH}", root_path)', 'layout_html = get_layout(root_path)')
        content = content.replace('nav_html = NAV_TEMPLATE.replace("{ROOT_PATH}", "")', 'layout_html = get_layout("")')
        content = content.replace('nav_html = NAV_TEMPLATE.replace("{ROOT_PATH}", "../")', 'layout_html = get_layout("../")')
        content = content.replace('nav_html = NAV_TEMPLATE.replace("{ROOT_PATH}", "../../")', 'layout_html = get_layout("../../")')
        content = content.replace('nav_html = NAV_TEMPLATE.replace("{ROOT_PATH}", "../../../")', 'layout_html = get_layout("../../../")')
        
        # Wait, build scripts replace `{NAV_HTML}` using .replace("{NAV_HTML}", nav_html)
        content = content.replace('"{NAV_HTML}", nav_html', '"{LAYOUT_HTML}", layout_html')
        content = content.replace('"{NAV_HTML}",nav_html', '"{LAYOUT_HTML}", layout_html')

        # Add lg:pl-64 to <main> and wrap it in a div?
        # Actually, we can just add `lg:pl-[17rem]` to `<main class="...">`
        if '<main class="' in content:
            # Find all <main class="..."> and add lg:pl-[17.5rem] if not present
            def main_replacer(match):
                cls = match.group(1)
                if 'lg:pl-72' not in cls:
                    return f'<main class="{cls} lg:pl-72">'
                return match.group(0)
            content = re.sub(r'<main class="([^"]+)">', main_replacer, content)

        # Inject JS before </body>
        if JS_CODE.strip() not in content:
            content = content.replace('</body>', JS_CODE.strip() + '\n</body>')

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")

update_python_files()
