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
        parts.append(f'<div class="mb-16">')
        parts.append(f'<h2 class="text-3xl font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-3 font-display">')
        parts.append(f'<span class="w-1.5 h-8 bg-blue-500 rounded-full"></span>{sub["name"]}</h2>\n')
        
        if sub.get("content"):
            parts.append(f'<p class="text-slate-600 dark:text-slate-400 mb-8">{sub["content"]}</p>\n')
            
        for ex in sub.get("examples", []):
            parts.append(f'<h3 class="text-xl font-bold text-slate-800 dark:text-slate-200 mb-4">{ex["title"]}</h3>\n')
            
            raw_code = ex.get("code", "")
            raw_output = ex.get("output", "")
            
            # Check if output is already in comments
            output_in_comments = False
            if raw_output and raw_code:
                output_lines = [l.strip() for l in raw_output.split('\n') if l.strip()]
                if output_lines:
                    # PowerShell comments can be # or <# #> but we check # for simple cases
                    code_comments = [line.split('#', 1)[1].strip() for line in raw_code.split('\n') if '#' in line]
                    # Check if all non-empty output lines are represented in comments
                    prefixes = ["Output:", "Result:", "->", "=>"]
                    found_count = 0
                    for o_line in output_lines:
                        matched = False
                        for c in code_comments:
                            c_clean = c.strip()
                            if o_line == c_clean:
                                matched = True; break
                            for p in prefixes:
                                if c_clean.startswith(p) and c_clean[len(p):].strip() == o_line:
                                    matched = True; break
                            if matched: break
                        if matched: found_count += 1
                    
                    if found_count == len(output_lines):
                        output_in_comments = True

            code = raw_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            output = raw_output.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            
            if output and not output_in_comments:
                # Combined Code + Output Card
                parts.append(f'<div class="my-8 group">')
                parts.append(f'<div class="relative rounded-xl overflow-hidden bg-white border border-slate-200 shadow-sm transition-all hover:shadow-md p-6">')
                parts.append(f'<pre class="language-powershell"><code>{code}</code></pre>')
                parts.append(f'<div class="mt-6 pt-6 border-t border-slate-100 bg-slate-50/50 -mx-6 -mb-6 px-6 pb-6">')
                parts.append(f'<div class="text-[10px] uppercase tracking-widest text-slate-400 mb-3 font-bold flex items-center gap-2"><i data-lucide="terminal" class="w-3 h-3"></i> Output</div>')
                parts.append(f'<pre class="!m-0 !p-0 !bg-transparent !border-0 !shadow-none !rounded-none"><code class="text-blue-600 font-mono text-sm leading-relaxed">{output}</code></pre>')
                parts.append(f'</div>')
                parts.append(f'</div>')
                parts.append(f'</div>')
            else:
                # Standalone Code Block
                parts.append(f'<div class="my-6">')
                parts.append(f'<pre class="language-powershell"><code>{code}</code></pre>')
                parts.append(f'</div>')
        
        parts.append(f'</div>\n')
        
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
        <section class="mb-12">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-600">
                    <span class="text-sm font-black">{num}</span>
                </div>
                <h2 class="text-2xl font-bold text-slate-900 dark:text-white font-display tracking-tight">{phase['name']}</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {items_html}
            </div>
        </section>"""

    hub_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>PowerShell Scripting \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Master Windows automation and cross-platform scripting with our structured PowerShell guide.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-5xl mx-auto">
            <!-- HERO -->
            <header class="mb-20 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border-2 border-blue-200/50">
                    <i data-lucide="terminal" class="w-3 h-3"></i> Automation Guide
                </div>
                <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-tight">
                    PowerShell <span class="bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">Scripting</span>
                </h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium italic">
                    "Master the art of automation. From local cmdlets to enterprise-scale remote orchestration."
                </p>
            </header>

            <!-- CARD CONTENT -->
            <div class="space-y-16">
                {phases_html}
            </div>

            <footer class="mt-20 py-10 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-medium text-xs tracking-widest uppercase text-[10px]">\u00a9 2026 Data Cake \u2022 Automation Mastery</p>
            </footer>
        </main>
    </div>
    <script>lucide.createIcons();</script>
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
        <a href="../powershell.html" class="inline-flex items-center gap-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors mb-6 group no-underline">
            <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
            Back to PowerShell
        </a>
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
