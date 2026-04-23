import glob

correct_func = """
def inject_sidebar_into_all_html():
    SIDEBAR_TEMPLATE = '''
<!-- SIDEBAR -->
<aside class="fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 border-r border-slate-200 dark:border-slate-800/60 bg-white/50 dark:bg-slate-950/50 backdrop-blur-xl z-40 hidden lg:block overflow-y-auto py-8 px-6">
    <div class="mb-8">
        <a href="{prefix}learn.html" class="font-display font-bold text-slate-900 dark:text-white mb-4 text-sm uppercase tracking-wider block no-underline hover:text-blue-600 dark:hover:text-blue-400">Learn</a>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Programming</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/python.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Python</a></li>
                <li><a href="{prefix}learn/sql.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">SQL</a></li>
                <li><a href="{prefix}learn/bash.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Bash</a></li>
                <li><a href="{prefix}learn/powershell.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">PowerShell</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Concepts</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/de-fundamentals.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DE Fundamentals</a></li>
                <li><a href="{prefix}learn/dsa-de.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DSA for DE</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Tools</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/spark.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Spark</a></li>
                <li><a href="{prefix}learn/flink.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Flink</a></li>
                <li><a href="{prefix}learn/kafka.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Kafka</a></li>
                <li><a href="{prefix}learn/dbt.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">dbt</a></li>
                <li><a href="{prefix}learn/pandas.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Pandas</a></li>
                <li><a href="{prefix}learn/numpy.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">NumPy</a></li>
                <li><a href="{prefix}learn/airflow.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Airflow</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Cloud</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/aws.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">AWS</a></li>
                <li><a href="{prefix}learn/gcp.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">GCP</a></li>
                <li><a href="{prefix}learn/azure.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Azure</a></li>
                <li><a href="{prefix}learn/snowflake.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Snowflake</a></li>
                <li><a href="{prefix}learn/databricks.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Databricks</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">CI/CD</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/docker.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Docker</a></li>
                <li><a href="{prefix}learn/kubernetes.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Kubernetes</a></li>
                <li><a href="{prefix}learn/terraform.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Terraform</a></li>
                <li><a href="{prefix}learn/github.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">GitHub</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Design</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/system-design.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">System Design</a></li>
                <li><a href="{prefix}learn/pipeline-design.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Pipeline Design</a></li>
                <li><a href="{prefix}learn/de-architectures.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DE Architectures</a></li>
            </ul>
        </div>
    </div>
    <div>
        <a href="{prefix}practice.html" class="font-display font-bold text-slate-900 dark:text-white mb-4 text-sm uppercase tracking-wider block no-underline hover:text-blue-600 dark:hover:text-blue-400">Practice</a>
        <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
            <li><a href="{prefix}practice.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Coming Soon</a></li>
        </ul>
    </div>
</aside>
'''
    html_files = glob.glob('pages/**/*.html', recursive=True)
    for html_file in html_files:
        if html_file.replace(chr(92)*2, '/').replace(chr(92), '/') in ['pages/learn.html', 'pages/practice.html']:
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '<!-- SIDEBAR -->' in content:
            continue
            
        normalized = html_file.replace(chr(92)*2, '/').replace(chr(92), '/')
        depth = len(normalized.split('/')) - 1
        prefix = '../' * (depth - 1)
        
        sidebar_rendered = SIDEBAR_TEMPLATE.replace('{prefix}', prefix)
        
        if '</nav>' in content:
            content = content.replace('</nav>', '</nav>\\n' + sidebar_rendered + '\\n<div class="lg:pl-64 w-full">')
            content = content.replace('</body>', '</div>\\n</body>')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

inject_sidebar_into_all_html()
"""

py_files = glob.glob('build_*.py') + ['generate_pages.py']
for f in py_files:
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    if 'def inject_sidebar_into_all_html():' in c:
        idx = c.find('def inject_sidebar_into_all_html():')
        c = c[:idx] + correct_func
        with open(f, 'w', encoding='utf-8') as file:
            file.write(c)
