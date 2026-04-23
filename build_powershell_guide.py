import json
import os

# Icon mapping for each topic
TOPIC_ICONS = {
    "intro":             "terminal",
    "basics":            "code",
    "variables":         "variable",
    "operators":         "calculator",
    "control_flow":      "git-branch",
    "functions":         "command",
    "pipeline":          "arrow-right-left",
    "error_handling":    "alert-circle",
    "file_system":       "folder",
    "regex":             "search",
    "modules":           "package",
    "remoting":          "wifi",
    "classes":           "layers",
    "wmi_cim":           "cpu",
    "security":          "shield",
    "networking":        "network",
    "scheduled_tasks":   "clock",
    "formatting_output": "monitor",
    "projects":          "folder-kanban",
    "cheatsheet":        "layout",
}

def render_topic_html(topic):
    """Convert a topic dict (from powershell_guide.json) into HTML content."""
    if topic["id"] == "cheatsheet":
        return render_cheatsheet_html(topic)
        
    parts = []
    for sub in topic.get("subtopics", []):
        parts.append(f"<h2>{sub['name']}</h2>\n<br>\n")
        if sub.get("content"):
            parts.append(f"<p>{sub['content']}</p>\n<br>\n")
        for ex in sub.get("examples", []):
            parts.append(f"<h3>{ex['title']}</h3>\n")
            code = ex["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            parts.append(
                f'<pre><code class="language-powershell">\n{code}\n</code></pre>\n<br>\n'
            )
        parts.append("<hr>\n<br>\n")
    return "".join(parts)


def render_cheatsheet_html(topic):
    parts = []
    for sub in topic.get("subtopics", []):
        parts.append(f"<h2>{sub['name']}</h2>\n<br>\n")
        parts.append('<div class="overflow-x-auto my-6">')
        parts.append('<table class="min-w-full border-collapse border border-slate-200 dark:border-slate-800 text-sm">')
        parts.append('<thead class="bg-slate-100 dark:bg-slate-800/50">')
        parts.append('<tr>')
        parts.append('<th class="border border-slate-200 dark:border-slate-800 p-3 text-left font-bold w-1/2">Bash</th>')
        parts.append('<th class="border border-slate-200 dark:border-slate-800 p-3 text-left font-bold text-blue-500 w-1/2">PowerShell</th>')
        parts.append('</tr>')
        parts.append('</thead>')
        parts.append('<tbody>')

        for ex in sub.get("examples", []):
            code = ex["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            lines = code.strip().split('\n')
            for line in lines:
                if '# --- BASH ---' in line:
                    continue
                if not line.strip():
                    continue
                    
                if '|' in line:
                    left, right = line.split('|', 1)
                    left = left.strip()
                    right = right.strip()
                    parts.append('<tr class="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">')
                    parts.append(f'<td class="border border-slate-200 dark:border-slate-800 p-3"><code>{left}</code></td>')
                    parts.append(f'<td class="border border-slate-200 dark:border-slate-800 p-3 text-blue-500/80"><code>{right}</code></td>')
                    parts.append('</tr>')
                else:
                    parts.append('<tr class="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">')
                    parts.append(f'<td class="border border-slate-200 dark:border-slate-800 p-3 text-slate-500 dark:text-slate-400 font-medium" colspan="2">{line.strip()}</td>')
                    parts.append('</tr>')
                    
        parts.append('</tbody>')
        parts.append('</table>')
        parts.append('</div>')
        parts.append("<br>\n")
    return "".join(parts)


def build_powershell_hub(topics):
    cards_html = []
    for i, topic in enumerate(topics):
        icon = TOPIC_ICONS.get(topic["id"], "file-code")
        title = f"{i+1}. {topic['title']}"
        cards_html.append(f"""
    <a href="powershell/{topic['id']}.html" class="topic-card group bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800/60 rounded-2xl p-6 no-underline transition-all hover:shadow-xl hover:shadow-blue-500/5 hover:-translate-y-1">
        <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 group-hover:bg-blue-600 group-hover:text-white transition-all duration-300">
                <i data-lucide="{icon}" class="w-6 h-6"></i>
            </div>
            <div class="flex-1">
                <h3 class="font-display font-bold text-lg text-slate-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{title}</h3>
                <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed line-clamp-2">{topic['description']}</p>
            </div>
        </div>
    </a>""")

    hub_template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <title>PowerShell Scripting — Data Sheets</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Complete PowerShell scripting guide covering syntax, pipeline, error handling, modules, and real-world projects.">
    <script>(function(){{const s=localStorage.getItem('ds-theme');if(s==='light')document.documentElement.classList.remove('dark');else document.documentElement.classList.add('dark');}})();</script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body{{font-family:'Inter',sans-serif;}}
        .font-display,h1,h2,h3{{font-family:'Outfit',sans-serif;}}
        .grid-bg{{background-image:linear-gradient(rgba(0,0,0,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.05) 1px,transparent 1px);background-size:40px 40px;}}
        .dark .grid-bg{{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);}}
        .topic-card{{transition:all 0.2s;}}
        .topic-card:hover{{transform:translateY(-2px);}}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen transition-colors duration-300">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<nav class="fixed top-0 w-full z-50 bg-white/90 dark:bg-slate-950/90 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
        <a href="../../index.html" class="no-underline"><span style="font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:-.02em;" class="text-base md:text-xl text-slate-900 dark:text-slate-100 transition-colors duration-300">Data Sheets</span></a>
        <div class="flex items-center gap-1">
            <a href="../learn.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-900 dark:text-white bg-slate-100 dark:bg-white/10 transition-colors no-underline">Learn</a>
            <a href="../practice.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all no-underline">Practice</a>
        </div>
        <button id="theme-toggle" class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all">
            <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
            <i data-lucide="moon" class="w-5 h-5 block dark:hidden"></i>
        </button>
    </div>
</nav>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-5xl mx-auto">
    <a href="../learn.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to Learn
    </a>

    <header class="mb-12">
        <div class="flex items-center gap-4 mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400">
                <i data-lucide="terminal" class="w-7 h-7"></i>
            </div>
            <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white leading-tight tracking-tight">PowerShell Scripting</h1>
        </div>
        <p class="text-xl text-slate-600 dark:text-slate-400 max-w-3xl leading-relaxed">Master Windows automation and cross-platform scripting. From cmdlets and pipelines to remoting, modules, and real-world projects.</p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        {"".join(cards_html)}
    </div>
</main>

<script>
    lucide.createIcons();
    document.getElementById('theme-toggle').addEventListener('click',()=>{{
        const d=document.documentElement.classList.toggle('dark');
        localStorage.setItem('ds-theme', d?'dark':'light');
    }});
</script>
</body>
</html>"""

    os.makedirs("pages/learn", exist_ok=True)
    with open("pages/learn/powershell.html", "w", encoding="utf-8") as f:
        f.write(hub_template)
    print("Built PowerShell Hub: pages/learn/powershell.html")


def build_powershell_subpages(topics):
    os.makedirs("pages/learn/powershell", exist_ok=True)

    for i, topic in enumerate(topics):
        prev_topic = topics[i - 1] if i > 0 else None
        next_topic = topics[i + 1] if i < len(topics) - 1 else None
        
        title = f"{i+1}. {topic['title']}"

        prev_html = f"""
            <a href="{prev_topic['id']}.html" class="flex flex-col items-start no-underline group">
                <span class="text-xs text-slate-500 mb-1 flex items-center gap-1"><i data-lucide="arrow-left" class="w-3 h-3"></i> Previous</span>
                <span class="text-sm font-bold text-slate-900 dark:text-white group-hover:text-blue-600 transition-colors text-left">{i}. {prev_topic['title']}</span>
            </a>""" if prev_topic else "<div></div>"

        next_html = f"""
            <a href="{next_topic['id']}.html" class="flex flex-col items-end no-underline group text-right">
                <span class="text-xs text-slate-500 mb-1 flex items-center gap-1">Next <i data-lucide="arrow-right" class="w-3 h-3"></i></span>
                <span class="text-sm font-bold text-slate-900 dark:text-white group-hover:text-blue-600 transition-colors text-right">{i+2}. {next_topic['title']}</span>
            </a>""" if next_topic else "<div></div>"

        content_html = render_topic_html(topic)

        html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <title>{title} — PowerShell Scripting</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{topic['description']}">
    <script>(function(){{const s=localStorage.getItem('ds-theme');if(s==='light')document.documentElement.classList.remove('dark');else document.documentElement.classList.add('dark');}})();</script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body{{font-family:'Inter',sans-serif;}}
        .font-display,h1,h2,h3{{font-family:'Outfit',sans-serif;}}
        .grid-bg{{background-image:linear-gradient(rgba(0,0,0,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.05) 1px,transparent 1px);background-size:40px 40px;}}
        .dark .grid-bg{{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);}}

        .prose h2{{margin-top:2.5rem;margin-bottom:1.25rem;font-weight:700;color:inherit;font-size:2.25rem;letter-spacing:-0.02em;}}
        .prose h3{{margin-top:2rem;margin-bottom:1rem;font-weight:600;color:inherit;font-size:1.6rem;letter-spacing:-0.01em;}}
        .prose p{{margin-bottom:1.25rem;line-height:1.8;opacity:0.9;}}
        .prose ul{{list-style-type:disc;padding-left:1.5rem;margin-bottom:1.25rem;}}
        .prose li{{margin-bottom:0.6rem;}}
        .prose code{{background:rgba(0,0,0,0.05);padding:0.2rem 0.4rem;border-radius:0.25rem;font-size:0.875em;font-weight:500;}}
        .dark .prose code{{background:rgba(255,255,255,0.1);}}

        pre[class*="language-"] {{
            border-radius: 0.75rem !important;
            margin: 1.5rem 0 !important;
            background: #0f172a !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
        }}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen transition-colors duration-300">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<nav class="fixed top-0 w-full z-50 bg-white/90 dark:bg-slate-950/90 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
        <a href="../../../index.html" class="no-underline"><span style="font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:-.02em;" class="text-base md:text-xl text-slate-900 dark:text-slate-100 transition-colors duration-300">Data Sheets</span></a>
        <div class="flex items-center gap-1">
            <a href="../../learn.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-900 dark:text-white bg-slate-100 dark:bg-white/10 transition-colors no-underline">Learn</a>
            <a href="../../practice.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all no-underline">Practice</a>
        </div>
        <button id="theme-toggle" class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all">
            <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
            <i data-lucide="moon" class="w-5 h-5 block dark:hidden"></i>
        </button>
    </div>
</nav>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-4xl mx-auto">
    <a href="../powershell.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to PowerShell Scripting
    </a>

    <header class="mb-12">
        <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4 leading-tight tracking-tight">{title}</h1>
        <p class="text-xl text-slate-600 dark:text-slate-400 font-medium">{topic['description']}</p>
    </header>

    <article class="prose dark:prose-invert max-w-none pb-20">
        {content_html}
    </article>

    <div class="mt-16 pt-8 border-t border-slate-200 dark:border-slate-800 flex justify-between items-center">
        {prev_html}
        {next_html}
    </div>
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-powershell.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
<script>
    lucide.createIcons();
    document.getElementById('theme-toggle').addEventListener('click',()=>{{
        const d=document.documentElement.classList.toggle('dark');
        localStorage.setItem('ds-theme', d?'dark':'light');
    }});
</script>
</body>
</html>"""

        file_path = f"pages/learn/powershell/{topic['id']}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Built subpage: {file_path}")


if __name__ == "__main__":
    with open("powershell_guide.json", "r", encoding="utf-8") as f:
        guide = json.load(f)

    topics = guide["topics"]
    build_powershell_hub(topics)
    build_powershell_subpages(topics)
    print(f"\nDone! Built 1 hub + {len(topics)} subpages.")


import glob
import os


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
            content = content.replace('</nav>', '</nav>\n' + sidebar_rendered + '\n<div class="lg:pl-64 w-full">')
            content = content.replace('</body>', '</div>\n</body>')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

inject_sidebar_into_all_html()
