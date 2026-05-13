import os
import json
import re

PART_ICONS = {
    1:"code",
    2:"git-merge",
    3:"layers",
    4:"command",
    5:"codesandbox",
    6:"alert-circle",
    7:"refresh-cw",
    8:"wrench",
    9:"type",
    10:"list",
    11:"folder",
    12:"zap",
    13:"cpu",
    14:"test-tube",
    15:"gauge",
    16:"component",
    17:"globe",
    18:"award",
}

def get_global_sidebar(rel_path):
    return f"""
            <div class="sb-section sb-cat bg-blue-50 text-blue-700 hover:bg-blue-100 cursor-pointer">
                <span class="w-6 h-6 rounded-md bg-blue-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="code-2" class="w-3 h-3 text-white"></i>
                </span>
                Programming
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/python.html" class="sb-link"><i data-lucide="code-2" class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>Python</a>
                <a href="{rel_path}pages/learn/sql.html" class="sb-link"><i data-lucide="database" class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>SQL</a>
                <a href="{rel_path}pages/learn/bash.html" class="sb-link"><i data-lucide="terminal" class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>Bash</a>
                <a href="{rel_path}pages/learn/powershell.html" class="sb-link"><i data-lucide="terminal-square" class="w-3.5 h-3.5 text-blue-400 flex-shrink-0"></i>PowerShell</a>
            </nav>

            <div class="sb-section sb-cat bg-emerald-50 text-emerald-700 hover:bg-emerald-100 cursor-pointer collapsed">
                <span class="w-6 h-6 rounded-md bg-emerald-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="layers" class="w-3 h-3 text-white"></i>
                </span>
                Concepts
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/de-fundamentals.html" class="sb-link"><i data-lucide="layers" class="w-3.5 h-3.5 text-emerald-400 flex-shrink-0"></i>DE Fundamentals</a>
                <a href="{rel_path}pages/learn/dsa-de.html" class="sb-link"><i data-lucide="git-branch-plus" class="w-3.5 h-3.5 text-emerald-400 flex-shrink-0"></i>DSA for DE</a>
            </nav>

            <div class="sb-section sb-cat bg-orange-50 text-orange-700 hover:bg-orange-100 cursor-pointer collapsed">
                <span class="w-6 h-6 rounded-md bg-orange-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="wrench" class="w-3 h-3 text-white"></i>
                </span>
                Tools
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/spark.html" class="sb-link"><i data-lucide="zap" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Spark</a>
                <a href="{rel_path}pages/learn/flink.html" class="sb-link"><i data-lucide="activity" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Flink</a>
                <a href="{rel_path}pages/learn/kafka.html" class="sb-link"><i data-lucide="radio" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Kafka</a>
                <a href="{rel_path}pages/learn/dbt.html" class="sb-link"><i data-lucide="blocks" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>dbt</a>
                <a href="{rel_path}pages/learn/pandas.html" class="sb-link"><i data-lucide="table-2" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Pandas</a>
                <a href="{rel_path}pages/learn/numpy.html" class="sb-link"><i data-lucide="hash" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>NumPy</a>
                <a href="{rel_path}pages/learn/airflow.html" class="sb-link"><i data-lucide="wind" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Airflow</a>
                <a href="{rel_path}pages/learn/regex.html" class="sb-link"><i data-lucide="search" class="w-3.5 h-3.5 text-orange-400 flex-shrink-0"></i>Regex</a>
            </nav>

            <div class="sb-section sb-cat bg-cyan-50 text-cyan-700 hover:bg-cyan-100 cursor-pointer collapsed">
                <span class="w-6 h-6 rounded-md bg-cyan-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="cloud" class="w-3 h-3 text-white"></i>
                </span>
                Cloud
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/aws.html" class="sb-link"><i data-lucide="cloud" class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>AWS</a>
                <a href="{rel_path}pages/learn/gcp.html" class="sb-link"><i data-lucide="cloud-sun" class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>GCP</a>
                <a href="{rel_path}pages/learn/azure.html" class="sb-link"><i data-lucide="cloud-cog" class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Azure</a>
                <a href="{rel_path}pages/learn/snowflake.html" class="sb-link"><i data-lucide="snowflake" class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Snowflake</a>
                <a href="{rel_path}pages/learn/databricks.html" class="sb-link"><i data-lucide="box" class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0"></i>Databricks</a>
            </nav>

            <div class="sb-section sb-cat bg-violet-50 text-violet-700 hover:bg-violet-100 cursor-pointer collapsed">
                <span class="w-6 h-6 rounded-md bg-violet-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="git-pull-request" class="w-3 h-3 text-white"></i>
                </span>
                CI / CD
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/docker.html" class="sb-link"><i data-lucide="container" class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Docker</a>
                <a href="{rel_path}pages/learn/kubernetes.html" class="sb-link"><i data-lucide="network" class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Kubernetes</a>
                <a href="{rel_path}pages/learn/terraform.html" class="sb-link"><i data-lucide="sliders" class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Terraform</a>
                <a href="{rel_path}pages/learn/github.html" class="sb-link"><i data-lucide="git-branch" class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>GitHub</a>
            </nav>

            <div class="sb-section sb-cat bg-rose-50 text-rose-700 hover:bg-rose-100 cursor-pointer collapsed">
                <span class="w-6 h-6 rounded-md bg-rose-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="layout" class="w-3 h-3 text-white"></i>
                </span>
                Design
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/system-design.html" class="sb-link"><i data-lucide="layout-dashboard" class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>System Design</a>
                <a href="{rel_path}pages/learn/pipeline-design.html" class="sb-link"><i data-lucide="workflow" class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>Pipeline Design</a>
                <a href="{rel_path}pages/learn/de-architectures.html" class="sb-link"><i data-lucide="cpu" class="w-3.5 h-3.5 text-rose-400 flex-shrink-0"></i>DE Architectures</a>
            </nav>

            <div class="sb-section sb-cat bg-amber-50 text-amber-700 hover:bg-amber-100 cursor-pointer collapsed">
                <span class="w-6 h-6 rounded-md bg-amber-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="map" class="w-3 h-3 text-white"></i>
                </span>
                Roadmaps
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/roadmaps/data-engineering.html" class="sb-link"><i data-lucide="database" class="w-3.5 h-3.5 text-amber-400 flex-shrink-0"></i>Data Engineering</a>
                <a href="{rel_path}pages/roadmaps/ml-engineer.html" class="sb-link"><i data-lucide="brain-circuit" class="w-3.5 h-3.5 text-amber-400 flex-shrink-0"></i>ML Engineer</a>
                <a href="{rel_path}pages/roadmaps/ai-engineer.html" class="sb-link"><i data-lucide="bot" class="w-3.5 h-3.5 text-amber-400 flex-shrink-0"></i>AI Engineer</a>
            </nav>

            <div class="sb-section sb-cat bg-violet-50 text-violet-700 hover:bg-violet-100 cursor-pointer collapsed">
                <span class="w-6 h-6 rounded-md bg-violet-500 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="hammer" class="w-3 h-3 text-white"></i>
                </span>
                Practice
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/practice.html" class="sb-link"><i data-lucide="layout-grid" class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Practice Hub</a>
                <a href="{rel_path}pages/practice/list-comprehensions.html" class="sb-link"><i data-lucide="code" class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>Python Challenges</a>
                <a href="{rel_path}pages/practice/sql-window-functions.html" class="sb-link"><i data-lucide="database" class="w-3.5 h-3.5 text-violet-400 flex-shrink-0"></i>SQL Challenges</a>
            </nav>

            <div class="mt-4 pt-4 border-t border-slate-200">
                <a href="{rel_path}pages/portfolio.html" class="sb-section bg-slate-100 text-slate-700 hover:bg-slate-200">
                    <span class="w-6 h-6 rounded-md bg-slate-500 flex items-center justify-center flex-shrink-0">
                        <i data-lucide="user" class="w-3 h-3 text-white"></i>
                    </span>
                    My Portfolio
                    <i data-lucide="external-link" class="w-2.5 h-2.5 ml-auto opacity-50"></i>
                </a>
            </div>"""

def slugify(text):
    s = text.lower()
    s = s.replace("","-").replace("&","and").replace("/","-")
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s.strip("-")

def render_topic_content(topic_or_part):
    parts = []
    
    # Description AND Explanation (Don't miss either)
    desc = topic_or_part.get("description","")
    expl = topic_or_part.get("explanation","")
    
    if desc:
        parts.append(f'<p class="text-xl text-slate-600 dark:text-slate-400 mb-6 font-medium">{desc}</p>')
    if expl and expl != desc:
        parts.append(f'<p class="text-lg text-slate-600 dark:text-slate-400 mb-8">{expl}</p>')
    
    # Subtopics
    for sub in topic_or_part.get("subtopics", []):
        parts.append(f'<div class="mb-16">')
        parts.append(f'<h2 class="text-3xl font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-3 font-display">')
        parts.append(f'<span class="w-1.5 h-8 bg-indigo-500 rounded-full"></span>{sub["title"]}</h2>')
        
        sub_desc = sub.get("description","")
        sub_expl = sub.get("explanation","")
        if sub_desc:
            parts.append(f'<p class="text-slate-600 dark:text-slate-400 mb-4">{sub_desc}</p>')
        if sub_expl and sub_expl != sub_desc:
            parts.append(f'<p class="text-slate-600 dark:text-slate-400 mb-6">{sub_expl}</p>')
        
        if sub.get("code"):
            # Check if output is already in comments to avoid redundancy
            output_in_comments = False
            raw_output = sub.get("output","")
            raw_code = sub.get("code","")
            if raw_output and raw_code:
                output_lines = [l.strip() for l in raw_output.split('\n') if l.strip()]
                if output_lines:
                    # Get all comment parts from code
                    code_comments = [line.split('#', 1)[1].strip() for line in raw_code.split('\n') if '#' in line]
                    # Check if all non-empty output lines are represented in comments
                    # We look for exact matches or matches after common prefixes (Output:, ->, etc.)
                    prefixes = ["Output:","Result:","->","=>"]
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

            code = raw_code.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            output = raw_output.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            
            if output and not output_in_comments:
                # Combined Code + Output Card
                parts.append(f'<div class="my-8 group">')
                parts.append(f'<div class="relative rounded-xl overflow-hidden bg-white border border-slate-200 shadow-sm transition-all hover:shadow-md p-6">')
                parts.append(f'<pre class="language-python"><code>{code}</code></pre>')
                parts.append(f'<div class="mt-6 pt-6 border-t border-slate-100 bg-slate-50/50 -mx-6 -mb-6 px-6 pb-6">')
                parts.append(f'<div class="text-[10px] uppercase tracking-widest text-slate-400 mb-3 font-bold flex items-center gap-2"><i data-lucide="terminal" class="w-3 h-3"></i> Output</div>')
                parts.append(f'<pre class="!m-0 !p-0 !bg-transparent !border-0 !shadow-none !rounded-none"><code class="text-indigo-600 font-mono text-sm leading-relaxed">{output}</code></pre>')
                parts.append(f'</div>')
                parts.append(f'</div>')
                parts.append(f'</div>')
            else:
                # Standalone Code Block (uses pre[class*="language-"] style from CSS)
                parts.append(f'<pre class="language-python"><code>{code}</code></pre>')
            
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
            parts.append(f'<span class="flex-shrink-0 w-10 h-10 rounded-xl bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center text-base font-black">{q.get("id","?")}</span>')
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
        
    return"\n".join(parts)

def build_python_hub(data):
    parts_dict = data["content"]
    
    final_parts = []
    if"guide" in parts_dict and"parts" in parts_dict["guide"]:
        final_parts.extend(parts_dict["guide"]["parts"])
    
    for key, val in parts_dict.items():
        if key !="guide" and isinstance(val, dict) and"part" in val:
            final_parts.append(val)
            
    final_parts.sort(key=lambda x: x["part"])
    
    all_topics = []
    for part in final_parts:
        if part.get("topics"):
            for topic in part["topics"]:
                all_topics.append(topic)
        else:
            all_topics.append(part)

    # Pre-build sidebar HTML
    sidebar_html ="""
        <div id="guide-topics" class="mt-6">
            <div class="sb-section sb-cat bg-slate-50 text-slate-700 hover:bg-slate-100 cursor-pointer">
                <span class="w-6 h-6 rounded-md bg-slate-400 flex items-center justify-center flex-shrink-0">
                    <i data-lucide="list" class="w-3 h-3 text-white"></i>
                </span>
                Python Guide
            </div>
            <nav class="pl-2">"""
    for t in all_topics:
        slug = slugify(t["title"])
        sidebar_html += f'<a href="python/{slug}.html" class="sb-link">{t["title"]}</a>'
    sidebar_html += '</nav></div>'

    # Phase mapping (11 phases)
    phases = [
        {"name":"Foundations","part_ids": [1]},
        {"name":"Control & Iteration","part_ids": [2]},
        {"name":"Data Structures","part_ids": [3]},
        {"name":"Functional Programming","part_ids": [4]},
        {"name":"Object-Oriented Design","part_ids": [5]},
        {"name":"Robustness & Iterators","part_ids": [6, 7]},
        {"name":"Type System & Internal Tools","part_ids": [8, 9]},
        {"name":"System & File Ops","part_ids": [10, 11]},
        {"name":"Performance & Concurrency","part_ids": [12, 15]},
        {"name":"Internals & Architecture","part_ids": [13, 16]},
        {"name":"Testing & Real-World","part_ids": [14, 17, 18]}
    ]
    
    phases_html =""
    for i, phase in enumerate(phases):
        num = i + 1
        items_html =""
        for pid in phase["part_ids"]:
            part = next((p for p in final_parts if p["part"] == pid), None)
            if not part: continue
            
            # Add Part explanation if it exists
            part_expl = part.get("explanation", part.get("description",""))
            if part_expl:
                items_html += f'<div class="col-span-full mb-4 px-2"><p class="text-sm text-slate-400 italic font-medium tracking-wide opacity-80 uppercase">Part {pid}: {part_expl}</p></div>'

            if part.get("topics"):
                for topic in part["topics"]:
                    icon = PART_ICONS.get(pid,"code")
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
                icon = PART_ICONS.get(pid,"code")
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
        <section class="mb-12">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-12 h-12 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-600">
                    <span class="text-xl font-black">{num}</span>
                </div>
                <h2 class="text-3xl font-black text-slate-900 dark:text-white font-display tracking-tight">{phase['name']}</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {items_html}
            </div>
        </section>"""

    global_sidebar = get_global_sidebar("../../")

    hub_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Python Mastery — Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{data['description']}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="../../css/ds-main.css">
    <link rel="stylesheet" href="../../css/layout-fixes.css">
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <!-- NAV -->
    

    <!-- SIDEBAR OVERLAY (mobile) -->
    

    <!-- SIDEBAR -->
    

    <div id="ds-main-content" class="transition-all duration-300">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-6xl mx-auto">
            <!-- HERO -->
            <header class="mb-20 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border border-indigo-100 dark:border-indigo-800">
                    <i data-lucide="award" class="w-3 h-3"></i> Expert Documentation
                </div>
                <h1 class="font-display text-6xl md:text-8xl font-black text-slate-900 dark:text-white mb-8 tracking-tighter leading-tight">
                    Python <span class="bg-gradient-to-r from-indigo-600 via-blue-600 to-indigo-400 bg-clip-text text-transparent">Mastery</span>
                </h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium">
                    {data['description']}
                </p>
            </header>

            <!-- CARD CONTENT -->
            <div class="space-y-16">
                {phases_html}
            </div>

            
        </main>
    </div>
    <script src="../../js/ds-main.js"></script>
    <script>lucide.createIcons();</script>
</body>
</html>"""
    
    output_path = os.path.join('pages', 'learn', 'python.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path,"w", encoding="utf-8") as f:
        f.write(hub_template)
    print(f"Built Python Hub: {output_path}")

def build_python_subpages(data):
    parts_dict = data["content"]
    final_parts = []
    if"guide" in parts_dict and"parts" in parts_dict["guide"]:
        final_parts.extend(parts_dict["guide"]["parts"])
    
    for key, val in parts_dict.items():
        if key !="guide" and isinstance(val, dict) and"part" in val:
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
    sidebar_html ="""
        <div class="sb-section sb-cat bg-slate-50 text-slate-700 hover:bg-slate-100 cursor-pointer">
            <span class="w-6 h-6 rounded-md bg-slate-400 flex items-center justify-center flex-shrink-0">
                <i data-lucide="list" class="w-3 h-3 text-white"></i>
            </span>
            Python Guide
        </div>
        <nav class="pl-2">"""
    for t in all_topics:
        slug = slugify(t["title"])
        sidebar_html += f'<a href="{slug}.html" class="sb-link">{t["title"]}</a>'
    sidebar_html += '</nav>'
    
    for i, topic in enumerate(all_topics):
        slug = slugify(topic["title"])
        file_path = os.path.join('pages', 'learn', 'python', f"{slug}.html")
        
        # Navigation
        prev_topic = all_topics[i-1] if i > 0 else None
        next_topic = all_topics[i+1] if i < len(all_topics)-1 else None
        
        prev_html =""
        if prev_topic:
            pslug = slugify(prev_topic['title'])
            prev_html = f"""
            <a href="{pslug}.html" class="nav-card prev">
                <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
                <span class="nav-title">{prev_topic["title"]}</span>
            </a>"""
            
        next_html =""
        if next_topic:
            nslug = slugify(next_topic['title'])
            next_html = f"""
            <a href="{nslug}.html" class="nav-card next">
                <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
                <span class="nav-title">{next_topic["title"]}</span>
            </a>"""
            
        # Aggregated content for Interview Master (Part 18) - NO LIMIT
        if"interview-master" in slug:
            aggregated_questions = []
            if"questions" in topic:
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
            
        active_sidebar = sidebar_html.replace(f'href="{slug}.html" class="sb-link"', f'href="{slug}.html" class="sb-link active"')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{topic['title']} — Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <link rel="stylesheet" href="../../../css/ds-main.css">
    <link rel="stylesheet" href="../../../css/layout-fixes.css">
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <!-- NAV -->
    

    <!-- SIDEBAR OVERLAY (mobile) -->
    

    <!-- SIDEBAR -->
    

    <div class="flex flex-col lg:flex-row justify-center max-w-[1440px] mx-auto w-full">
        <div id="ds-main-content" class="transition-all duration-300 min-w-0">
            <main class="relative z-10 pt-28 pb-20 px-6 w-full max-w-4xl">
                <a href="../python.html#{slug}" class="inline-flex items-center gap-2 text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors mb-6 group no-underline">
                    <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
                    Back to Python
                </a>

                <header class="mb-12">
                    <div class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-4 flex items-center gap-2">
                        <span class="w-8 h-[1px] bg-slate-300"></span>
                        Section {topic['part_num']}: {topic.get('category', 'Foundations')}
                    </div>
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
        </div>

        <aside class="toc-container">
            <div class="toc-title">On this page</div>
            <ul class="toc-list"></ul>
        </aside>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script>lucide.createIcons();</script>
    <script src="../../../js/ds-main.js" defer></script>
</body>
</html>"""
        
        with open(file_path,"w", encoding="utf-8") as f:
            f.write(html)
            
    print(f"Built {len(all_topics)} Python subpages.")

if __name__ =="__main__":
    import sys, os, json, re
    data_file = os.path.join('data', 'python_complete_guide.json')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        build_python_hub(data)
        build_python_subpages(data)
    else:
        print(f"Error: {data_file} not found.")
