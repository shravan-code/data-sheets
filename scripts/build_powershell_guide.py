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
        parts.append(f"<h2>{sub['name']}</h2>\n")
        if sub.get("content"):
            parts.append(f"<p>{sub['content']}</p>\n")
        for ex in sub.get("examples", []):
            parts.append(f"<h3>{ex['title']}</h3>\n")
            code = ex["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            parts.append(
                f'<pre><code class="language-powershell">\n{code}\n</code></pre>\n'
            )
        parts.append("<hr>\n")
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
    # Group topics into 11 Phases for the full premium roadmap experience
    phases = [
        {"name": "Getting Started", "topic_ids": ["intro"]},
        {"name": "Syntax Fundamentals", "topic_ids": ["basics"]},
        {"name": "Variables & Objects", "topic_ids": ["variables"]},
        {"name": "Logic & Flow Control", "topic_ids": ["operators", "control_flow"]},
        {"name": "The Power of Pipeline", "topic_ids": ["pipeline", "formatting_output"]},
        {"name": "Professional Scripting", "topic_ids": ["functions", "error_handling"]},
        {"name": "Modular Automation", "topic_ids": ["modules"]},
        {"name": "System & Infrastructure", "topic_ids": ["wmi_cim", "remoting", "scheduled_tasks"]},
        {"name": "Security & Networking", "topic_ids": ["security", "networking"]},
        {"name": "Advanced Data & OOP", "topic_ids": ["classes", "regex"]},
        {"name": "Practical Projects", "topic_ids": ["projects", "cheatsheet"]}
    ]

    phases_html = ""
    for i, phase in enumerate(phases):
        num = i + 1
        items_html = ""
        for tid in phase["topic_ids"]:
            topic = next((t for t in topics if t["id"] == tid), None)
            if not topic: continue
            
            icon = TOPIC_ICONS.get(tid, "file-code")
            items_html += f"""
            <a href="powershell/{tid}.html" class="flex items-center gap-3 p-3 bg-blue-50/30 dark:bg-slate-900 border border-blue-100/50 dark:border-slate-800 rounded-xl transition-all hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:border-blue-200 group/item no-underline">
                <div class="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center text-blue-600 dark:text-blue-400 group-hover/item:bg-blue-600 group-hover/item:text-white transition-all">
                    <i data-lucide="{icon}" class="w-4 h-4"></i>
                </div>
                <span class="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover/item:text-blue-700 transition-colors">{topic['title']}</span>
            </a>"""

        phases_html += f"""
        <div class="relative pl-12 pb-12 group last:pb-0">
            <div class="absolute left-[19px] top-0 bottom-0 w-0.5 bg-slate-200 dark:bg-slate-800 group-last:bottom-auto group-last:h-10"></div>
            <div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 flex items-center justify-center z-10 group-hover:border-blue-500 transition-colors shadow-sm">
                <span class="text-xs font-bold text-slate-500 group-hover:text-blue-600">{num:02d}</span>
            </div>

            <div class="bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800/60 p-6 rounded-3xl transition-all hover:shadow-xl hover:shadow-blue-500/5">
                <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-3 font-display">
                    {phase['name']}
                    <span class="text-[10px] uppercase tracking-widest px-2 py-1 bg-blue-100 text-blue-700 rounded-lg font-bold border border-blue-200">Phase {num}</span>
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {items_html}
                </div>
            </div>
        </div>"""

    hub_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>PowerShell Roadmap \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Master Windows automation and cross-platform scripting with our 11-phase structured PowerShell roadmap.">
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
            <header class="roadmap-hero-bg mb-20 p-10 md:p-14 rounded-[48px] border-2 border-blue-100 dark:border-slate-800 bg-white dark:bg-slate-900 relative overflow-hidden shadow-2xl shadow-blue-500/10">
                <div class="absolute -top-24 -right-24 w-80 h-80 bg-blue-500/10 blur-[100px] rounded-full"></div>
                <div class="absolute -bottom-24 -left-24 w-80 h-80 bg-blue-500/5 blur-[100px] rounded-full"></div>
                
                <div class="relative z-10">
                    <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs font-black uppercase tracking-widest mb-8 border-2 border-blue-200/50">
                        <i data-lucide="terminal" class="w-4 h-4"></i>
                        Skill Roadmap
                    </div>
                    <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-[1.1]">
                        PowerShell <span class="bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">Scripting</span>
                    </h1>
                    <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl leading-relaxed mb-0 font-medium italic">
                        "Master the art of automation. From local cmdlets to enterprise-scale remote orchestration."
                    </p>
                </div>
            </header>

            <!-- ROADMAP CONTENT -->
            <div class="max-w-4xl mx-auto">
                {phases_html}
            </div>

            <footer class="mt-20 py-10 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-medium">\u00a9 2026 Data Cake \u2022 Path to Automation Mastery</p>
            </footer>
        </main>
    </div>
</body>
</html>"""

    output_path = os.path.join('pages', 'learn', 'powershell.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(hub_template)
    print(f"Built PowerShell Hub (Roadmap Style): {output_path}")


def build_powershell_subpages(topics):
    os.makedirs(os.path.join('pages', 'learn', 'powershell'), exist_ok=True)

    for i, topic in enumerate(topics):
        # Build list of all topics for the sidebar
        topics_html = '<div class="toc-title mt-8">PowerShell Topics</div><ul class="toc-list">'
        for t in topics:
            active_cls = "active" if t['id'] == topic['id'] else ""
            topics_html += f'<li><a href="{t["id"]}.html" class="toc-link {active_cls}">{t["title"]}</a></li>'
        topics_html += '</ul>'

        prev_topic = topics[i - 1] if i > 0 else None
        next_topic = topics[i + 1] if i < len(topics) - 1 else None
        
        title = f"{i+1}. {topic['title']}"

        prev_html = f"""
            <a href="{prev_topic['id']}.html" class="nav-card prev">
                <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
                <span class="nav-title">{prev_topic['title']}</span>
            </a>""" if prev_topic else "<div></div>"

        next_html = f"""
            <a href="{next_topic['id']}.html" class="nav-card next">
                <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
                <span class="nav-title">{next_topic['title']}</span>
            </a>""" if next_topic else "<div></div>"

        content_html = render_topic_html(topic)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title} — PowerShell Scripting</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{topic['description']}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<div class="flex justify-center max-w-[1440px] mx-auto">
    <main class="relative z-10 pt-28 pb-20 px-6 w-full max-w-4xl">
        <header class="mb-12">
            <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4 leading-tight tracking-tight">{title}</h1>
            <p class="text-xl text-slate-600 dark:text-slate-400 font-medium">{topic['description']}</p>
        </header>

        <article class="prose dark:prose-invert max-w-none pb-20">
            {content_html}
        </article>

        <div class="nav-container">
            {prev_html}
            {next_html}
        </div>
    </main>

    <aside class="toc-container">
        <div class="toc-title">On this page</div>
        <ul class="toc-list"></ul>
        {topics_html}
    </aside>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-powershell.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
</body>
</html>"""

        file_path = os.path.join('pages', 'learn', 'powershell', f"{topic['id']}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Built subpage: {file_path}")


if __name__ == "__main__":
    data_path = os.path.join('data', 'powershell_guide.json')
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            guide = json.load(f)

        topics = guide["topics"]
        build_powershell_hub(topics)
        build_powershell_subpages(topics)
        print(f"\nDone! Built 1 hub + {len(topics)} subpages.")
    else:
        print(f"Error: {data_path} not found.")
