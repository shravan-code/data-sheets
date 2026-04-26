import os
import json
import re

PART_ICONS = {
    1: "code",
    2: "git-merge",
    3: "layers",
    4: "command",
    5: "codesandbox",
    6: "alert-circle",
    7: "refresh-cw",
    8: "wrench",
    9: "type",
    10: "list",
    11: "folder",
    12: "zap",
    13: "cpu",
    14: "test-tube",
    15: "gauge",
    16: "component",
    17: "globe",
    18: "award",
}

def slugify(text):
    s = text.lower()
    s = s.replace(" ", "-").replace("&", "and").replace("/", "-")
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s.strip("-")

def render_topic_content(topic_or_part):
    parts = []
    
    # Description AND Explanation (Don't miss either)
    desc = topic_or_part.get("description", "")
    expl = topic_or_part.get("explanation", "")
    
    if desc:
        parts.append(f'<p class="text-xl text-slate-600 dark:text-slate-400 mb-6 font-medium">{desc}</p>')
    if expl and expl != desc:
        parts.append(f'<p class="text-lg text-slate-600 dark:text-slate-400 mb-8">{expl}</p>')
    
    # Subtopics
    for sub in topic_or_part.get("subtopics", []):
        parts.append(f'<div class="mb-16">')
        parts.append(f'<h2 class="text-3xl font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-3 font-display">')
        parts.append(f'<span class="w-1.5 h-8 bg-indigo-500 rounded-full"></span>{sub["title"]}</h2>')
        
        sub_desc = sub.get("description", "")
        sub_expl = sub.get("explanation", "")
        if sub_desc:
            parts.append(f'<p class="text-slate-600 dark:text-slate-400 mb-4">{sub_desc}</p>')
        if sub_expl and sub_expl != sub_desc:
            parts.append(f'<p class="text-slate-600 dark:text-slate-400 mb-6">{sub_expl}</p>')
        
        if sub.get("code"):
            code = sub["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            parts.append(f'<div class="relative group my-8">')
            parts.append(f'<div class="absolute -inset-2 bg-indigo-500/5 rounded-2xl blur opacity-0 group-hover:opacity-100 transition duration-500"></div>')
            parts.append(f'<pre class="relative rounded-xl overflow-hidden bg-slate-900 shadow-xl border border-slate-800"><code class="language-python">{code}</code></pre>')
            parts.append(f'</div>')
            
        if sub.get("output"):
            output = sub["output"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            parts.append(f'<div class="mt-4 p-5 bg-slate-100 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-xl">')
            parts.append(f'<div class="text-[10px] uppercase tracking-widest text-slate-400 mb-3 font-bold flex items-center gap-2"><i data-lucide="terminal" class="w-3 h-3"></i> Output</div>')
            parts.append(f'<pre class="text-indigo-600 dark:text-indigo-400 font-mono text-sm leading-relaxed"><code>{output}</code></pre>')
            parts.append(f'</div>')
            
        # Check for nested interview_qa in subtopics
        if sub.get("interview_qa"):
            parts.append(f'<div class="mt-8 p-6 bg-slate-50 dark:bg-slate-800/30 border border-slate-200 dark:border-slate-800 rounded-2xl">')
            for qa in sub["interview_qa"]:
                parts.append(f'<div class="mb-4 last:mb-0">')
                parts.append(f'<h4 class="text-md font-bold text-slate-900 dark:text-white mb-1">Q: {qa["question"]}</h4>')
                parts.append(f'<p class="text-slate-600 dark:text-slate-400 text-sm">A: {qa["answer"]}</p>')
                parts.append(f'</div>')
            parts.append('</div>')
            
        parts.append(f'</div>')
        
    # Questions (e.g. for Part 18)
    if topic_or_part.get("questions"):
        for q in topic_or_part["questions"]:
            parts.append(f'<div class="mb-10 p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm hover:shadow-md transition-shadow">')
            parts.append(f'<h3 class="text-xl font-bold text-indigo-600 dark:text-indigo-400 mb-4 flex items-start gap-4 font-display">')
            parts.append(f'<span class="flex-shrink-0 w-10 h-10 rounded-xl bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center text-base font-black">{q.get("id", "?")}</span>')
            parts.append(f'<span class="pt-1.5">{q["question"]}</span></h3>')
            parts.append(f'<p class="text-slate-600 dark:text-slate-400 leading-relaxed pl-14 text-lg">{q["answer"]}</p>')
            parts.append(f'</div>')

    # Interview Q&A (at topic level)
    if topic_or_part.get("interview_qa"):
        parts.append(f'<div class="mt-24 p-10 bg-gradient-to-br from-indigo-50/50 to-white dark:from-indigo-900/10 dark:to-slate-900 border border-indigo-100 dark:border-indigo-900/30 rounded-[40px]">')
        parts.append(f'<h2 class="text-3xl font-black text-indigo-700 dark:text-indigo-400 mt-0 mb-10 flex items-center gap-3 font-display tracking-tight">')
        parts.append(f'<i data-lucide="help-circle" class="w-8 h-8"></i> Interview Mastery</h2>')
        
        for qa in topic_or_part["interview_qa"]:
            parts.append(f'<div class="mb-10 last:mb-0 group">')
            parts.append(f'<h3 class="text-xl font-bold text-slate-900 dark:text-white mb-4 group-hover:text-indigo-600 transition-colors">Q: {qa["question"]}</h3>')
            parts.append(f'<div class="flex gap-4">')
            parts.append(f'<div class="w-1 bg-indigo-200 dark:bg-indigo-800 rounded-full"></div>')
            parts.append(f'<p class="text-slate-600 dark:text-slate-400 text-lg leading-relaxed">A: {qa["answer"]}</p>')
            parts.append(f'</div>')
            parts.append(f'</div>')
        parts.append('</div>')
        
    return "\n".join(parts)

def build_python_hub(data):
    parts_dict = data["content"]
    
    final_parts = []
    if "guide" in parts_dict and "parts" in parts_dict["guide"]:
        final_parts.extend(parts_dict["guide"]["parts"])
    
    for key, val in parts_dict.items():
        if key != "guide" and isinstance(val, dict) and "part" in val:
            final_parts.append(val)
            
    final_parts.sort(key=lambda x: x["part"])
    
    # Phase mapping (11 phases)
    phases = [
        {"name": "Foundations", "part_ids": [1]},
        {"name": "Control & Iteration", "part_ids": [2]},
        {"name": "Data Structures", "part_ids": [3]},
        {"name": "Functional Programming", "part_ids": [4]},
        {"name": "Object-Oriented Design", "part_ids": [5]},
        {"name": "Robustness & Iterators", "part_ids": [6, 7]},
        {"name": "Type System & Internal Tools", "part_ids": [8, 9]},
        {"name": "System & File Ops", "part_ids": [10, 11]},
        {"name": "Performance & Concurrency", "part_ids": [12, 15]},
        {"name": "Internals & Architecture", "part_ids": [13, 16]},
        {"name": "Testing & Real-World", "part_ids": [14, 17, 18]}
    ]
    
    phases_html = ""
    for i, phase in enumerate(phases):
        num = i + 1
        items_html = ""
        for pid in phase["part_ids"]:
            part = next((p for p in final_parts if p["part"] == pid), None)
            if not part: continue
            
            # Add Part explanation if it exists
            part_expl = part.get("explanation", part.get("description", ""))
            if part_expl:
                items_html += f'<div class="col-span-full mb-4 px-2"><p class="text-sm text-slate-400 italic font-medium tracking-wide opacity-80 uppercase">Part {pid}: {part_expl}</p></div>'

            if part.get("topics"):
                for topic in part["topics"]:
                    icon = PART_ICONS.get(pid, "code")
                    slug = slugify(topic["title"])
                    items_html += f"""
                    <a href="python/{slug}.html" class="flex items-center gap-3 p-4 bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800 rounded-2xl transition-all hover:bg-indigo-50/50 dark:hover:bg-indigo-900/20 hover:border-indigo-200 group/item no-underline shadow-sm hover:shadow-md">
                        <div class="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 group-hover/item:bg-indigo-600 group-hover/item:text-white transition-all">
                            <i data-lucide="{icon}" class="w-5 h-5"></i>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-sm font-bold text-slate-700 dark:text-slate-300 group-hover/item:text-indigo-700 transition-colors">{topic['title']}</span>
                        </div>
                    </a>"""
            else:
                icon = PART_ICONS.get(pid, "code")
                slug = slugify(part["title"])
                items_html += f"""
                <a href="python/{slug}.html" class="flex items-center gap-3 p-4 bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800 rounded-2xl transition-all hover:bg-indigo-50/50 dark:hover:bg-indigo-900/20 hover:border-indigo-200 group/item no-underline shadow-sm hover:shadow-md">
                    <div class="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 group-hover/item:bg-indigo-600 group-hover/item:text-white transition-all">
                        <i data-lucide="{icon}" class="w-5 h-5"></i>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-sm font-bold text-slate-700 dark:text-slate-300 group-hover/item:text-indigo-700 transition-colors">{part['title']}</span>
                    </div>
                </a>"""

        phases_html += f"""
        <div class="relative pl-12 pb-16 group last:pb-0">
            <div class="absolute left-[19px] top-0 bottom-0 w-1 bg-gradient-to-b from-indigo-200 to-transparent dark:from-slate-800 group-last:bottom-auto group-last:h-12"></div>
            <div class="absolute left-0 top-0 w-10 h-10 rounded-2xl bg-white dark:bg-slate-900 border-2 border-indigo-100 dark:border-slate-800 flex items-center justify-center z-10 group-hover:border-indigo-500 transition-all shadow-lg group-hover:scale-110">
                <span class="text-sm font-black text-indigo-600">{num}</span>
            </div>

            <div class="bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm border border-slate-200/60 dark:border-slate-800/60 p-8 rounded-[32px] transition-all hover:shadow-2xl hover:shadow-indigo-500/5 hover:bg-white dark:hover:bg-slate-900">
                <h3 class="text-2xl font-black text-slate-900 dark:text-white mb-8 flex items-center gap-4 font-display tracking-tight">
                    {phase['name']}
                    <span class="text-[10px] uppercase tracking-[0.2em] px-3 py-1.5 bg-indigo-600 text-white rounded-full font-black shadow-lg shadow-indigo-500/20">Phase {num}</span>
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {items_html}
                </div>
            </div>
        </div>"""

    hub_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Python Mastery Roadmap \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{data['description']}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <style>
        .roadmap-hero-bg {{
            background-image: radial-gradient(circle at 2px 2px, rgba(99, 102, 241, 0.05) 1px, transparent 0);
            background-size: 32px 32px;
        }}
        .dark .roadmap-hero-bg {{
            background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.02) 1px, transparent 0);
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-6xl mx-auto">
            <!-- HERO -->
            <header class="roadmap-hero-bg mb-24 p-12 md:p-20 rounded-[64px] border border-indigo-100 dark:border-slate-800 bg-white dark:bg-slate-900 relative overflow-hidden shadow-[0_32px_64px_-16px_rgba(0,0,0,0.05)]">
                <div class="absolute -top-24 -right-24 w-96 h-96 bg-indigo-500/10 blur-[120px] rounded-full"></div>
                <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-500/5 blur-[120px] rounded-full"></div>
                
                <div class="relative z-10 text-center">
                    <div class="inline-flex items-center gap-2 px-5 py-2 bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400 rounded-full text-[10px] font-black uppercase tracking-[0.2em] mb-10 border border-indigo-100 dark:border-indigo-800">
                        <i data-lucide="award" class="w-4 h-4"></i>
                        The definitive Python Guide
                    </div>
                    <h1 class="font-display text-6xl md:text-8xl font-black text-slate-900 dark:text-white mb-8 tracking-tighter leading-none">
                        Python <span class="bg-gradient-to-r from-indigo-600 via-blue-600 to-indigo-400 bg-clip-text text-transparent">Mastery</span>
                    </h1>
                    <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium italic">
                        "{data['description']}"
                    </p>
                </div>
            </header>

            <!-- ROADMAP CONTENT -->
            <div class="max-w-4xl mx-auto">
                {phases_html}
            </div>

            <footer class="mt-32 py-12 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-bold tracking-widest uppercase text-xs">Developed for Data Cake \u2022 2026</p>
            </footer>
        </main>
    </div>
    <script>lucide.createIcons();</script>
</body>
</html>"""
    
    output_path = os.path.join('pages', 'learn', 'python.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(hub_template)
    print(f"Built Python Hub: {output_path}")

def build_python_subpages(data):
    parts_dict = data["content"]
    final_parts = []
    if "guide" in parts_dict and "parts" in parts_dict["guide"]:
        final_parts.extend(parts_dict["guide"]["parts"])
    
    for key, val in parts_dict.items():
        if key != "guide" and isinstance(val, dict) and "part" in val:
            final_parts.append(val)
    final_parts.sort(key=lambda x: x["part"])

    all_topics = []
    for part in final_parts:
        if part.get("topics"):
            for topic in part["topics"]:
                topic["part_num"] = part["part"]
                all_topics.append(topic)
        else:
            part["part_num"] = part["part"]
            all_topics.append(part)
            
    os.makedirs(os.path.join('pages', 'learn', 'python'), exist_ok=True)
    
    # Pre-build sidebar HTML
    sidebar_html = '<div class="toc-title mt-8">Python Guide</div><ul class="toc-list">'
    for t in all_topics:
        slug = slugify(t["title"])
        sidebar_html += f'<li><a href="{slug}.html" class="toc-link">{t["title"]}</a></li>'
    sidebar_html += '</ul>'
    
    for i, topic in enumerate(all_topics):
        slug = slugify(topic["title"])
        file_path = os.path.join('pages', 'learn', 'python', f"{slug}.html")
        
        # Navigation
        prev_topic = all_topics[i-1] if i > 0 else None
        next_topic = all_topics[i+1] if i < len(all_topics)-1 else None
        
        prev_html = ""
        if prev_topic:
            pslug = slugify(prev_topic['title'])
            prev_html = f"""
            <a href="{pslug}.html" class="nav-card prev">
                <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
                <span class="nav-title">{prev_topic["title"]}</span>
            </a>"""
            
        next_html = ""
        if next_topic:
            nslug = slugify(next_topic['title'])
            next_html = f"""
            <a href="{nslug}.html" class="nav-card next">
                <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
                <span class="nav-title">{next_topic["title"]}</span>
            </a>"""
            
        # Aggregated content for Interview Master (Part 18) - NO LIMIT
        if "interview-master" in slug:
            aggregated_questions = []
            if "questions" in topic:
                aggregated_questions.extend(topic["questions"])
            
            # Gather from ALL other topics in ALL parts
            other_qa = []
            for t in all_topics:
                # Top-level interview_qa
                if t.get("interview_qa"):
                    for qa in t["interview_qa"]:
                        if not any(q["question"] == qa["question"] for q in aggregated_questions):
                            other_qa.append(qa)
                # Nested interview_qa in subtopics
                if t.get("subtopics"):
                    for sub in t["subtopics"]:
                        if sub.get("interview_qa"):
                            for qa in sub["interview_qa"]:
                                if not any(q["question"] == qa["question"] for q in aggregated_questions):
                                    other_qa.append(qa)
            
            for qa in other_qa:
                qa_copy = qa.copy()
                qa_copy["id"] = len(aggregated_questions) + 1
                aggregated_questions.append(qa_copy)
            
            topic_to_render = topic.copy()
            topic_to_render["questions"] = aggregated_questions
            content = render_topic_content(topic_to_render)
        else:
            content = render_topic_content(topic)
            
        active_sidebar = sidebar_html.replace(f'href="{slug}.html" class="toc-link"', f'href="{slug}.html" class="toc-link active"')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{topic['title']} \u2014 Python Guide</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        pre[class*="language-"] {{
            margin: 0 !important;
            padding: 1.5rem !important;
            border-radius: 0.75rem !important;
            font-size: 0.9rem !important;
            line-height: 1.6 !important;
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div class="flex justify-center max-w-[1440px] mx-auto">
        <main class="relative z-10 pt-28 pb-20 px-6 w-full max-w-4xl">
            <a href="../python.html" class="inline-flex items-center gap-2 text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors mb-6 group no-underline">
                <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
                Back to Python
            </a>
            <header class="mb-12">
                <h1 class="text-4xl md:text-6xl font-black text-slate-900 dark:text-white leading-tight tracking-tighter font-display">
                    {topic['title']}
                </h1>
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
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script>lucide.createIcons();</script>
</body>
</html>"""
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
            
    print(f"Built {len(all_topics)} Python subpages.")

if __name__ == "__main__":
    import sys, os, json, re
    data_file = os.path.join('data', 'python_complete_guide.json')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        build_python_hub(data)
        build_python_subpages(data)
    else:
        print(f"Error: {data_file} not found.")
