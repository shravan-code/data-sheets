import json
import os

def render_projects_html(topic_data):
    """Render projects specifically."""
    parts = []
    for project in topic_data.get("projects", []):
        parts.append(f'<div class="mb-16 p-8 bg-emerald-50/20 dark:bg-emerald-900/10 border border-emerald-100 dark:border-emerald-900/30 rounded-3xl">')
        parts.append(f'<h2 class="text-2xl font-bold text-emerald-700 dark:text-emerald-400 mt-0">{project["name"]}</h2>')
        parts.append(f'<p class="text-lg text-slate-600 dark:text-slate-400 mb-6">{project["description"]}</p>')
        code = project["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        parts.append(f'<pre><code class="language-bash">{code}</code></pre>')
        parts.append('</div>')
    return "\n".join(parts)

def render_cheatsheet_html(topic_data):
    """Render the side-by-side cheatsheet."""
    parts = []
    for cat in topic_data.get("categories", []):
        parts.append(f"<h2>{cat['category']}</h2>")
        parts.append('<div class="overflow-x-auto my-6">')
        parts.append('<table class="min-w-full border-collapse border border-slate-200 dark:border-slate-800 text-sm">')
        parts.append('<thead class="bg-slate-100 dark:bg-slate-800/50">')
        parts.append('<tr>')
        parts.append('<th class="border border-slate-200 dark:border-slate-800 p-3 text-left font-bold w-1/2">Bash</th>')
        parts.append('<th class="border border-slate-200 dark:border-slate-800 p-3 text-left font-bold text-blue-500 w-1/2">PowerShell</th>')
        parts.append('</tr>')
        parts.append('</thead>')
        parts.append('<tbody>')
        for comp in cat.get("comparisons", []):
            parts.append('<tr class="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">')
            parts.append(f'<td class="border border-slate-200 dark:border-slate-800 p-3">')
            parts.append(f'<div class="text-[10px] uppercase tracking-wider text-slate-400 mb-1">{comp["task"]}</div>')
            parts.append(f'<code>{comp["bash"]}</code></td>')
            parts.append(f'<td class="border border-slate-200 dark:border-slate-800 p-3 text-blue-500/80"><code>{comp["powershell"]}</code></td>')
            parts.append('</tr>')
        parts.append('</tbody></table></div>')
    return "\n".join(parts)

def render_topic_html(topic_data):
    """Render the detailed content for a topic (subpage)."""
    if topic_data["id"] == 16:
        return render_projects_html(topic_data)
    if topic_data["id"] == 17:
        return render_cheatsheet_html(topic_data)
        
    parts = []
    for sub in topic_data.get("subtopics", []):
        parts.append(f"<h2>{sub['name']}</h2>")
        parts.append(f"<p>{sub['explanation']}</p>")
        for ex in sub.get("examples", []):
            parts.append(f"<h3>{ex['title']}</h3>")
            code = ex["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            parts.append(f'<pre><code class="language-bash">{code}</code></pre>')
        parts.append("<hr>")
    return "\n".join(parts)

def build_bash_hub(topics):
    # Group topics into 11 Phases for the roadmap view
    phases = [
        {"name": "Shell Foundations", "topic_ids": [1]},
        {"name": "Variable Mastery", "topic_ids": [2]},
        {"name": "Input & Output", "topic_ids": [4]},
        {"name": "Data Structures", "topic_ids": [3]},
        {"name": "Arithmetic & Logic", "topic_ids": [5]},
        {"name": "Control Flow", "topic_ids": [6]},
        {"name": "Reusable Functions", "topic_ids": [7]},
        {"name": "Text Processing Suite", "topic_ids": [8]},
        {"name": "Regex Mastery", "topic_ids": [12]},
        {"name": "System & Robustness", "topic_ids": [9, 10, 11]},
        {"name": "Advanced & Practical", "topic_ids": [13, 14, 15, 16, 17]}
    ]

    phases_html = ""
    for i, phase in enumerate(phases):
        num = i + 1
        items_html = ""
        for tid in phase["topic_ids"]:
            topic = next((t for t in topics if t["id"] == tid), None)
            if not topic: continue
            
            # Simple icon mapping
            icon = "terminal"
            if tid in [2, 3]: icon = "variable"
            if tid == 5: icon = "calculator"
            if tid == 6: icon = "git-branch"
            if tid == 7: icon = "command"
            if tid == 8: icon = "search"
            if tid == 9: icon = "folder"
            if tid == 10: icon = "cpu"
            if tid == 11: icon = "alert-circle"
            
            slug = topic['topic'].lower().replace(" ", "-").replace("&", "and")
            items_html += f"""
            <a href="bash/{slug}.html" class="flex items-center gap-3 p-3 bg-emerald-50/30 dark:bg-slate-900 border border-emerald-100/50 dark:border-slate-800 rounded-xl transition-all hover:bg-emerald-50 dark:hover:bg-emerald-900/20 hover:border-emerald-200 group/item no-underline">
                <div class="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-600 dark:text-emerald-400 group-hover/item:bg-emerald-600 group-hover/item:text-white transition-all">
                    <i data-lucide="{icon}" class="w-4 h-4"></i>
                </div>
                <span class="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover/item:text-emerald-700 transition-colors">{topic['topic']}</span>
            </a>"""

        phases_html += f"""
        <div class="relative pl-12 pb-12 group last:pb-0">
            <div class="absolute left-[19px] top-0 bottom-0 w-0.5 bg-slate-200 dark:bg-slate-800 group-last:bottom-auto group-last:h-10"></div>
            <div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 flex items-center justify-center z-10 group-hover:border-emerald-500 transition-colors shadow-sm">
                <span class="text-xs font-bold text-slate-500 group-hover:text-emerald-600">{num:02d}</span>
            </div>

            <div class="bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800/60 p-6 rounded-3xl transition-all hover:shadow-xl hover:shadow-emerald-500/5">
                <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-3 font-display">
                    {phase['name']}
                    <span class="text-[10px] uppercase tracking-widest px-2 py-1 bg-emerald-100 text-emerald-700 rounded-lg font-bold border border-emerald-200">Phase {num}</span>
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {items_html}
                </div>
            </div>
        </div>"""

    hub_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Bash Scripting Roadmap \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Master Linux automation and shell scripting with our 11-phase structured Bash roadmap.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <style>
        .roadmap-hero-bg {{
            background-image: radial-gradient(circle at 2px 2px, rgba(0,0,0,0.03) 1px, transparent 0);
            background-size: 24px 24px;
        }}
        .dark .roadmap-hero-bg {{
            background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.03) 1px, transparent 0);
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-5xl mx-auto">
            <!-- HERO -->
            <header class="roadmap-hero-bg mb-20 p-10 md:p-14 rounded-[48px] border-2 border-emerald-100 dark:border-slate-800 bg-white dark:bg-slate-900 relative overflow-hidden shadow-2xl shadow-emerald-500/10">
                <div class="absolute -top-24 -right-24 w-80 h-80 bg-emerald-500/10 blur-[100px] rounded-full"></div>
                <div class="absolute -bottom-24 -left-24 w-80 h-80 bg-emerald-500/5 blur-[100px] rounded-full"></div>
                
                <div class="relative z-10">
                    <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-100 text-emerald-700 rounded-full text-xs font-black uppercase tracking-widest mb-8 border-2 border-emerald-200/50">
                        <i data-lucide="terminal" class="w-4 h-4"></i>
                        Shell Roadmap
                    </div>
                    <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-[1.1]">
                        Bash <span class="bg-gradient-to-r from-emerald-600 to-emerald-400 bg-clip-text text-transparent">Scripting</span>
                    </h1>
                    <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl leading-relaxed mb-0 font-medium italic">
                        "The language of the cloud. From simple pipes to production-grade automation engines."
                    </p>
                </div>
            </header>

            <!-- ROADMAP CONTENT -->
            <div class="max-w-4xl mx-auto">
                {phases_html}
            </div>

            <footer class="mt-20 py-10 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-medium">\u00a9 2026 Data Cake \u2022 Path to Linux Mastery</p>
            </footer>
        </main>
    </div>
</body>
</html>"""

    output_path = os.path.join('pages', 'learn', 'bash.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(hub_template)
    print(f"Built Bash Hub (Roadmap Style): {output_path}")

def build_bash_subpages(topics):
    os.makedirs(os.path.join('pages', 'learn', 'bash'), exist_ok=True)
    
    # Pre-build sidebar HTML
    sidebar_html = '<div class="toc-title mt-8">Bash Topics</div><ul class="toc-list">'
    for t in topics:
        slug = t['topic'].lower().replace(" ", "-").replace("&", "and")
        sidebar_html += f'<li><a href="{slug}.html" class="toc-link">{t["topic"]}</a></li>'
    sidebar_html += '</ul>'

    for i, topic in enumerate(topics):
        slug = topic['topic'].lower().replace(" ", "-").replace("&", "and")
        file_path = os.path.join('pages', 'learn', 'bash', f"{slug}.html")
        
        # Navigation
        prev_topic = topics[i-1] if i > 0 else None
        next_topic = topics[i+1] if i < len(topics)-1 else None
        
        prev_html = ""
        if prev_topic:
            pslug = prev_topic['topic'].lower().replace(" ", "-").replace("&", "and")
            prev_html = f"""
            <a href="{pslug}.html" class="nav-card prev">
                <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
                <span class="nav-title">{prev_topic["topic"]}</span>
            </a>"""
            
        next_html = ""
        if next_topic:
            nslug = next_topic['topic'].lower().replace(" ", "-").replace("&", "and")
            next_html = f"""
            <a href="{nslug}.html" class="nav-card next">
                <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
                <span class="nav-title">{next_topic["topic"]}</span>
            </a>"""

        content = render_topic_html(topic)
        
        # Adjust sidebar to highlight active
        active_sidebar = sidebar_html.replace(f'href="{slug}.html" class="toc-link"', f'href="{slug}.html" class="toc-link active"')

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{topic['topic']} \u2014 Bash Guide</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div class="flex justify-center max-w-[1440px] mx-auto">
        <main class="relative z-10 pt-28 pb-20 px-6 w-full max-w-4xl">
            <a href="../bash.html" class="inline-flex items-center gap-2 text-sm font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300 transition-colors mb-6 group no-underline">
                <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
                Back to Bash
            </a>
            <header class="mb-12">
                <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4 leading-tight tracking-tight">{topic['topic']}</h1>
            </header>

            <article class="prose dark:prose-invert max-w-none pb-20">
                {content}
            </article>

            <div class="nav-container">
                {prev_html}
                {next_html}
            </div>
        </main>

        <aside class="toc-container">
            <div class="toc-title">On this page</div>
            <ul class="toc-list"></ul>
            {active_sidebar}
        </aside>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
</body>
</html>"""
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
    print(f"Built {len(topics)} Bash subpages.")

if __name__ == "__main__":
    data_path = os.path.join('data', 'bash_guide.json')
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            guide = json.load(f)
        
        topics = guide["topics"]
        build_bash_hub(topics)
        build_bash_subpages(topics)
    else:
        print(f"Error: {data_path} not found.")
