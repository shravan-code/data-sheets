import os
import json
import re

# Configuration
OUTPUT_DIR = "pages/learn/pipeline-design"
INDEX_FILE = "pages/learn/pipeline-design.html"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load parsed content
data_path = os.path.join('data', 'subpages_data.json')
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit(1)

with open(data_path, 'r', encoding='utf-8') as f:
    subpages = json.load(f)

def generate_index():
    cards_html = ""
    for page in subpages:
        cards_html += f"""
        <a href="pipeline-design/{page['id']}.html" class="topic-card group relative p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800/60 rounded-2xl no-underline transition-all hover:shadow-xl hover:shadow-blue-500/5 hover:border-blue-500/30 overflow-hidden">
            <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <i data-lucide="{page['icon']}" class="w-16 h-16 text-blue-600"></i>
            </div>
            <div class="relative z-10">
                <div class="w-10 h-10 rounded-lg bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <i data-lucide="{page['icon']}" class="w-5 h-5"></i>
                </div>
                <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-2">{page['title']}</h3>
                <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed mb-4">{page['description']}</p>
                <div class="flex items-center text-xs font-semibold text-blue-600 dark:text-blue-400 gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    Explore Module <i data-lucide="arrow-right" class="w-3 h-3"></i>
                </div>
            </div>
        </a>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Data Pipeline Design — Data Sheets</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>
<div class="fixed top-0 left-0 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none z-0"></div>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-5xl mx-auto">
    <a href="../learn.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to Learn
    </a>

    <div class="flex items-start gap-5 mb-10">
        <div class="w-16 h-16 rounded-xl flex items-center justify-center bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400">
            <i data-lucide="layout" class="w-8 h-8"></i>
        </div>
        <div>
            <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold mb-2 bg-blue-100 dark:bg-blue-500/20 text-blue-700 dark:text-blue-300">Data Engineering</span>
            <h1 class="font-display font-bold text-4xl text-slate-900 dark:text-white leading-tight">Data Pipeline Design</h1>
            <p class="text-slate-600 dark:text-slate-400 mt-2 text-lg">Master the architecture, patterns, and best practices for building robust data lifecycles.</p>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {cards_html}
    </div>
</main>
</body>
</html>"""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)

def generate_subpages():
    for i, page in enumerate(subpages):
        prev_page = subpages[i-1] if i > 0 else None
        next_page = subpages[i+1] if i < len(subpages)-1 else None
        
        nav_buttons = ""
        if next_page:
            nav_buttons += f"""
            <a href="{next_page['id']}.html" class="flex flex-col items-end no-underline group text-right">
                <span class="text-xs text-slate-500 mb-1 flex items-center gap-1">Next <i data-lucide="arrow-right" class="w-3 h-3"></i></span>
                <span class="text-sm font-bold text-slate-900 dark:text-white group-hover:text-blue-600 transition-colors text-right">{next_page['title']}</span>
            </a>
            """
        else:
            nav_buttons += "<div></div>"

        content = page['content']
        content = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', r'<div class="my-8 p-6 border border-slate-200 dark:border-slate-700 rounded-xl not-prose bg-white dark:bg-slate-900/50"><div class="mermaid text-center">\1</div></div>', content, flags=re.DOTALL)
        
        # Build list of all topics for the sidebar
        topics_html = '<div class="toc-title mt-8">Pipeline Topics</div><ul class="toc-list">'
        for p in subpages:
            active_cls = "active" if p['id'] == page['id'] else ""
            topics_html += f'<li><a href="{p["id"]}.html" class="toc-link {active_cls}">{p["title"]}</a></li>'
        topics_html += '</ul>'

        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{page['title']} — Data Pipeline Design</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: document.documentElement.classList.contains('dark') ? 'dark' : 'default',
            fontFamily: 'Inter',
            themeVariables: {{ fontFamily: 'Inter', fontSize: '13px' }}
        }});
    </script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<div class="flex justify-center max-w-[1440px] mx-auto">
    <main class="relative z-10 pt-28 pb-20 px-6 w-full max-w-4xl">
        <a href="../pipeline-design.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
            <i data-lucide="arrow-left" class="w-4 h-4"></i>
            Back to Pipeline Design
        </a>

        <header class="mb-12">
            <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4 leading-tight tracking-tight">{page['title']}</h1>
            <p class="text-xl text-slate-600 dark:text-slate-400 font-medium">{page['description']}</p>
        </header>

        <article class="prose dark:prose-invert max-w-none pb-20">
            {content}
        </article>

        <div class="mt-16 pt-8 border-t border-slate-200 dark:border-slate-800 flex justify-between items-center">
            <div></div>
            {nav_buttons}
        </div>
    </main>

    <aside class="toc-container">
        <div class="toc-title">On this page</div>
        <ul class="toc-list"></ul>
        {topics_html}
    </aside>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
</body>
</html>"""
        
        file_path = os.path.join(OUTPUT_DIR, f"{page['id']}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(template)

if __name__ == "__main__":
    generate_index()
    generate_subpages()
    print(f"Generated Corrected Index and {len(subpages)} subpages.")
