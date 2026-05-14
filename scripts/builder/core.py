import os
import json
import re
from datetime import datetime

PART_ICONS = {
    1: "code", 2: "git-merge", 3: "layers", 4: "command", 5: "codesandbox",
    6: "alert-circle", 7: "refresh-cw", 8: "wrench", 9: "type", 10: "list",
    11: "folder", 12: "zap", 13: "cpu", 14: "test-tube", 15: "gauge",
    16: "component", 17: "globe", 18: "award",
}

def slugify(text):
    s = text.lower()
    s = s.replace(" ", "-").replace("&", "and").replace("/", "-")
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s.strip("-")

def get_global_sidebar(rel_path):
    return f"""
            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer">
                <i data-lucide="code-2" class="w-4 h-4"></i>
                Programming
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/python.html" class="sb-link"><i data-lucide="chevron-right" class="w-3.5 h-3.5 flex-shrink-0"></i>Python</a>
                <a href="{rel_path}pages/learn/sql.html" class="sb-link"><i data-lucide="database" class="w-3.5 h-3.5 text-secondary-fixed flex-shrink-0"></i>SQL</a>
                <a href="{rel_path}pages/learn/bash.html" class="sb-link"><i data-lucide="terminal" class="w-3.5 h-3.5 flex-shrink-0"></i>Bash</a>
                <a href="{rel_path}pages/learn/powershell.html" class="sb-link"><i data-lucide="terminal-square" class="w-3.5 h-3.5 flex-shrink-0"></i>PowerShell</a>
            </nav>

            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer">
                <i data-lucide="layers" class="w-4 h-4"></i>
                Concepts
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/de-fundamentals.html" class="sb-link"><i data-lucide="layers" class="w-3.5 h-3.5 flex-shrink-0"></i>DE Fundamentals</a>
                <a href="{rel_path}pages/learn/dsa-de.html" class="sb-link"><i data-lucide="git-branch-plus" class="w-3.5 h-3.5 flex-shrink-0"></i>DSA for DE</a>
            </nav>

            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer">
                <i data-lucide="calculator" class="w-4 h-4"></i>
                Tools
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/spark.html" class="sb-link"><i data-lucide="zap" class="w-3.5 h-3.5 flex-shrink-0"></i>Spark</a>
                <a href="{rel_path}pages/learn/flink.html" class="sb-link"><i data-lucide="activity" class="w-3.5 h-3.5 flex-shrink-0"></i>Flink</a>
                <a href="{rel_path}pages/learn/kafka.html" class="sb-link"><i data-lucide="radio" class="w-3.5 h-3.5 flex-shrink-0"></i>Kafka</a>
                <a href="{rel_path}pages/learn/dbt.html" class="sb-link"><i data-lucide="blocks" class="w-3.5 h-3.5 flex-shrink-0"></i>dbt</a>
                <a href="{rel_path}pages/learn/pandas.html" class="sb-link"><i data-lucide="table-2" class="w-3.5 h-3.5 flex-shrink-0"></i>Pandas</a>
                <a href="{rel_path}pages/learn/numpy.html" class="sb-link"><i data-lucide="hash" class="w-3.5 h-3.5 flex-shrink-0"></i>NumPy</a>
                <a href="{rel_path}pages/learn/airflow.html" class="sb-link"><i data-lucide="wind" class="w-3.5 h-3.5 flex-shrink-0"></i>Airflow</a>
                <a href="{rel_path}pages/learn/regex.html" class="sb-link"><i data-lucide="search" class="w-3.5 h-3.5 flex-shrink-0"></i>Regex</a>
            </nav>

            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer">
                <i data-lucide="cloud" class="w-4 h-4"></i>
                Cloud
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/aws.html" class="sb-link"><i data-lucide="cloud" class="w-3.5 h-3.5 flex-shrink-0"></i>AWS</a>
                <a href="{rel_path}pages/learn/gcp.html" class="sb-link"><i data-lucide="cloud-sun" class="w-3.5 h-3.5 flex-shrink-0"></i>GCP</a>
                <a href="{rel_path}pages/learn/azure.html" class="sb-link"><i data-lucide="cloud-cog" class="w-3.5 h-3.5 flex-shrink-0"></i>Azure</a>
                <a href="{rel_path}pages/learn/snowflake.html" class="sb-link"><i data-lucide="snowflake" class="w-3.5 h-3.5 flex-shrink-0"></i>Snowflake</a>
                <a href="{rel_path}pages/learn/databricks.html" class="sb-link"><i data-lucide="box" class="w-3.5 h-3.5 flex-shrink-0"></i>Databricks</a>
            </nav>

            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer">
                <i data-lucide="git-pull-request" class="w-4 h-4"></i>
                CI / CD
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/docker.html" class="sb-link"><i data-lucide="container" class="w-3.5 h-3.5 flex-shrink-0"></i>Docker</a>
                <a href="{rel_path}pages/learn/kubernetes.html" class="sb-link"><i data-lucide="network" class="w-3.5 h-3.5 flex-shrink-0"></i>Kubernetes</a>
                <a href="{rel_path}pages/learn/terraform.html" class="sb-link"><i data-lucide="sliders" class="w-3.5 h-3.5 flex-shrink-0"></i>Terraform</a>
                <a href="{rel_path}pages/learn/github.html" class="sb-link"><i data-lucide="git-branch" class="w-3.5 h-3.5 flex-shrink-0"></i>GitHub</a>
            </nav>

            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer">
                <i data-lucide="layout" class="w-4 h-4"></i>
                Design
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/learn/system-design.html" class="sb-link"><i data-lucide="layout-dashboard" class="w-3.5 h-3.5 flex-shrink-0"></i>System Design</a>
                <a href="{rel_path}pages/learn/pipeline-design.html" class="sb-link"><i data-lucide="workflow" class="w-3.5 h-3.5 flex-shrink-0"></i>Pipeline Design</a>
                <a href="{rel_path}pages/learn/de-architectures.html" class="sb-link"><i data-lucide="cpu" class="w-3.5 h-3.5 flex-shrink-0"></i>DE Architectures</a>
                <a href="{rel_path}pages/learn/agents.html" class="sb-link"><i data-lucide="bot" class="w-3.5 h-3.5 flex-shrink-0"></i>AI Agents</a>
            </nav>

            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer">
                <i data-lucide="map" class="w-4 h-4"></i>
                Roadmaps
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/roadmaps/data-engineering.html" class="sb-link"><i data-lucide="database" class="w-3.5 h-3.5 flex-shrink-0"></i>Data Engineering</a>
                <a href="{rel_path}pages/roadmaps/ml-engineer.html" class="sb-link"><i data-lucide="brain-circuit" class="w-3.5 h-3.5 flex-shrink-0"></i>ML Engineer</a>
                <a href="{rel_path}pages/roadmaps/ai-engineer.html" class="sb-link"><i data-lucide="bot" class="w-3.5 h-3.5 flex-shrink-0"></i>AI Engineer</a>
            </nav>

            <div class="sb-section sb-cat text-on-surface-variant cursor-pointer">
                <i data-lucide="hammer" class="w-4 h-4"></i>
                Practice
            </div>
            <nav class="pl-2">
                <a href="{rel_path}pages/practice.html" class="sb-link"><i data-lucide="layout-grid" class="w-3.5 h-3.5 flex-shrink-0"></i>Practice Hub</a>
                <a href="{rel_path}pages/learn/skills.html" class="sb-link"><i data-lucide="award" class="w-3.5 h-3.5 flex-shrink-0"></i>Skills Arena</a>
                <a href="{rel_path}pages/practice/list-comprehensions.html" class="sb-link"><i data-lucide="code" class="w-3.5 h-3.5 flex-shrink-0"></i>Python Challenges</a>
                <a href="{rel_path}pages/practice/sql-window-functions.html" class="sb-link"><i data-lucide="database" class="w-3.5 h-3.5 flex-shrink-0"></i>SQL Challenges</a>
            </nav>

            <div class="mt-4 pt-4 border-t border-outline-variant">
                <a href="{rel_path}pages/portfolio.html" class="sb-section text-on-surface-variant hover:text-secondary-fixed">
                    <i data-lucide="folder-closed" class="w-4 h-4"></i>
                    My Portfolio
                    <i data-lucide="external-link" class="w-3 h-3 ml-auto opacity-50"></i>
                </a>
            </div>"""

def render_topic_content(topic_or_part):
    parts = []
    
    desc = topic_or_part.get("description", "")
    expl = topic_or_part.get("explanation", "")
    
    if desc:
        parts.append(f'<p class="text-lg text-on-surface-variant mb-6 font-medium">{desc}</p>')
    if expl and expl != desc:
        parts.append(f'<p class="text-base text-on-surface-variant mb-8">{expl}</p>')
    
    for sub in topic_or_part.get("subtopics", []):
        parts.append(f'<div class="mb-16">')
        parts.append(f'<h2 class="text-2xl font-bold text-on-surface mb-6 flex items-center gap-3 ml-0.5 border-b border-on-surface/10 pb-2">')
        parts.append(f'{sub["title"]}</h2>')
        
        sub_desc = sub.get("description", "")
        sub_expl = sub.get("explanation", "")
        if sub_desc:
            parts.append(f'<p class="text-on-surface-variant mb-4 leading-relaxed">{sub_desc}</p>')
        if sub_expl and sub_expl != sub_desc:
            parts.append(f'<p class="text-on-surface-variant mb-6 leading-relaxed">{sub_expl}</p>')
        
        if sub.get("code"):
            output_in_comments = False
            raw_output = sub.get("output", "")
            raw_code = sub.get("code", "")
            if raw_output and raw_code:
                output_lines = [l.strip() for l in raw_output.split('\n') if l.strip()]
                if output_lines:
                    code_comments = [line.split('#', 1)[1].strip() for line in raw_code.split('\n') if '#' in line]
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
            
            lang = sub.get("language", "python")
            if output and not output_in_comments:
                parts.append(f'<pre class="language-{lang}"><code>{code}</code></pre>')
                parts.append(f'<div class="ds-output-label">Output</div>')
                parts.append(f'<pre class="language-output"><code>{output}</code></pre>')
            else:
                parts.append(f'<pre class="language-{lang}"><code>{code}</code></pre>')
            
        if sub.get("interview_qa"):
            parts.append(f'<div class="mt-8 p-6 bg-surface-container border border-outline-variant rounded-xl">')
            for i, qa in enumerate(sub["interview_qa"]):
                if i > 0:
                    parts.append('<div class="h-px bg-on-surface/5 my-6"></div>')
                parts.append(f'<div class="grid grid-cols-[2rem_1fr] gap-x-2">')
                parts.append(f'<div class="text-secondary-fixed font-bold text-sm">Q:</div>')
                parts.append(f'<h4 class="text-sm font-bold text-on-surface mb-3 leading-relaxed">{qa["question"]}</h4>')
                parts.append(f'<div class="text-on-surface-variant/50 font-bold text-sm">A:</div>')
                parts.append(f'<p class="text-on-surface-variant text-sm leading-relaxed">{qa["answer"]}</p>')
                parts.append(f'</div>')
            parts.append('</div>')
        parts.append(f'</div>')
        
    if topic_or_part.get("questions"):
        for q in topic_or_part["questions"]:
            parts.append(f'<div class="mb-10 p-6 bg-surface-container border border-outline-variant rounded-xl transition-all hover:border-secondary-fixed">')
            parts.append(f'<h3 class="text-lg font-bold text-secondary-fixed mb-4 flex items-start gap-4">')
            parts.append(f'<span class="flex-shrink-0 w-10 h-10 rounded-xl bg-surface border border-outline-variant flex items-center justify-center text-base font-black text-on-surface">{q.get("id", "?")}</span>')
            parts.append(f'<span class="pt-1.5 text-on-surface leading-relaxed">{q["question"]}</span></h3>')
            parts.append(f'<p class="text-on-surface-variant leading-relaxed pl-14">{q["answer"]}</p>')
            parts.append(f'</div>')

    if topic_or_part.get("interview_qa"):
        parts.append(f'<div class="mt-16 p-6 bg-surface-container border border-outline-variant rounded-xl">')
        parts.append(f'<h2 class="text-lg font-bold text-secondary-fixed mt-0 mb-8">Interview Mastery</h2>')
        for i, qa in enumerate(topic_or_part["interview_qa"]):
            if i > 0:
                parts.append('<div class="h-px bg-on-surface/5 my-6"></div>')
            parts.append(f'<div class="grid grid-cols-[2rem_1fr] gap-x-2">')
            parts.append(f'<div class="text-secondary-fixed font-bold text-sm">Q:</div>')
            parts.append(f'<h3 class="text-sm font-bold text-on-surface mb-3 leading-relaxed">{qa["question"]}</h3>')
            parts.append(f'<div class="text-on-surface-variant/50 font-bold text-sm">A:</div>')
            parts.append(f'<p class="text-on-surface-variant text-sm leading-relaxed">{qa["answer"]}</p>')
            parts.append(f'</div>')
        parts.append('</div>')
        
    return "\n".join(parts)

class GuideBuilder:
    def __init__(self, section_id, section_name, data_file):
        self.section_id = section_id
        self.section_name = section_name
        self.data_file = data_file
        with open(data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.output_dir = os.path.join('pages', 'learn', section_id)
        self.hub_file = os.path.join('pages', 'learn', f"{section_id}.html")
        
        self._check_lock()
        os.makedirs(self.output_dir, exist_ok=True)

    def _check_lock(self):
        lock_file = os.path.join(os.path.dirname(__file__), '..', '..', '.agents', 'locks.json')
        if not os.path.exists(lock_file):
            return # Ignore if locking system not present
            
        try:
            with open(lock_file, 'r') as f:
                locks = json.load(f)
            
            # Check global lock
            global_lock = locks.get('global_lock', {})
            if global_lock.get('locked'):
                print(f"!!! GLOBAL LOCK ACTIVE !!!")
                print(f"Reason: {global_lock.get('reason')}")
                print(f"Owner:  {global_lock.get('owner')}")
                print(f"Build aborted to prevent conflicts.")
                exit(1)

            # Check module lock
            module_lock = locks.get('modules', {}).get(self.section_id, {})
            if module_lock.get('locked'):
                # If we are the owner, we can proceed
                # (This is a bit tricky to detect automatically, so we'll just warning or skip if locked by others)
                print(f"--- Notice: Module '{self.section_id}' is currently locked ---")
                print(f"Reason: {module_lock.get('reason')}")
                print(f"Owner:  {module_lock.get('owner')}")
                # We'll allow it for now but print a strong warning
                print(f"Proceeding with build as it is read-only for data sources, but avoid manual edits.")
        except Exception as e:
            print(f"Warning: Could not check locks: {e}")

    def get_parts(self):
        parts_dict = self.data["content"]
        final_parts = []
        if "guide" in parts_dict and "parts" in parts_dict["guide"]:
            final_parts.extend(parts_dict["guide"]["parts"])
        for key, val in parts_dict.items():
            if key != "guide" and isinstance(val, dict) and "part" in val:
                final_parts.append(val)
        final_parts.sort(key=lambda x: x["part"])
        return final_parts

    def get_all_topics(self):
        parts = self.get_parts()
        all_topics = []
        for part in parts:
            if part.get("topics"):
                for topic in part["topics"]:
                    topic["part_num"] = part["part"]
                    all_topics.append(topic)
            else:
                part["part_num"] = part["part"]
                all_topics.append(part)
        return all_topics

    def build_hub(self, phases):
        final_parts = self.get_parts()
        all_topics = self.get_all_topics()
        
        phases_html = ""
        for i, phase in enumerate(phases):
            num = i + 1
            items_html = ""
            for pid in phase["part_ids"]:
                part = next((p for p in final_parts if p["part"] == pid), None)
                if not part: continue
                
                part_expl = part.get("explanation", part.get("description", ""))
                if part_expl:
                    items_html += f'<div class="col-span-full mb-4 px-2"><p class="text-xs text-on-surface-variant font-medium tracking-wide opacity-80 uppercase">Part {pid}: {part_expl}</p></div>'

                topics_to_show = part.get("topics", [part])
                for topic in topics_to_show:
                    icon = PART_ICONS.get(pid, "code")
                    slug = slugify(topic["title"])
                    items_html += f"""
                    <a href="{self.section_id}/{slug}.html" class="flex items-center gap-3 p-4 bg-surface-container border border-outline-variant rounded-xl transition-all hover:border-secondary-fixed group/item no-underline">
                        <div class="w-10 h-10 rounded-xl bg-surface border border-outline-variant flex items-center justify-center text-on-surface-variant group-hover/item:text-secondary-fixed transition-colors">
                            <i data-lucide="{icon}" class="w-5 h-5"></i>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-sm font-bold text-on-surface group-hover/item:text-secondary-fixed transition-colors">{topic['title']}</span>
                        </div>
                    </a>"""

            phases_html += f"""
            <section class="mb-12">
                <div class="flex items-center gap-4 mb-8">
                    <div class="w-12 h-12 rounded-xl border border-outline-variant flex items-center justify-center text-secondary-fixed font-bold text-xl bg-surface-container">
                        {num}
                    </div>
                    <h2 class="text-2xl font-bold text-on-surface">{phase['name']}</h2>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {items_html}
                </div>
            </section>"""

        template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <title>{self.section_name} \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{self.data['description']}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['JetBrains Mono','ui-monospace','monospace'],mono:['JetBrains Mono','ui-monospace','monospace']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="../../css/ds-main.css">
    <link rel="stylesheet" href="../../css/modules/code-blocks.css">
    <script src="../../js/modules/universal-nav.js" defer></script>
    <script src="../../js/modules/code-blocks.js" defer></script>
</head>
<body class="bg-surface text-on-surface min-h-screen">
    <div id="nav-universal"></div>
    <div class="flex flex-col lg:flex-row justify-center max-w-[1440px] mx-auto w-full">
        <div id="ds-main-content" class="transition-all duration-300 min-w-0">
            <main class="relative z-10 pt-28 pb-20 px-6 w-full max-w-5xl mx-auto">
                <header class="mb-20 text-center">
                    <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-outline-variant bg-surface-container text-on-surface-variant text-xs font-semibold mb-8">
                        <i data-lucide="award" class="w-3.5 h-3.5"></i> EXPERT DOCUMENTATION
                    </div>
                    <h1 class="text-4xl md:text-5xl font-bold text-on-surface mb-8 leading-tight">
                        {self.section_name.split(' ')[0]} <span class="text-secondary-fixed">{self.section_name.split(' ')[1] if ' ' in self.section_name else ''}</span>
                    </h1>
                    <p class="text-lg text-on-surface-variant max-w-3xl mx-auto leading-relaxed">
                        {self.data['description']}
                    </p>
                </header>
                <div class="space-y-16">
                    {phases_html}
                </div>
            </main>
        </div>
    </div>
    <script src="../../js/ds-main.js"></script>
</body>
</html>"""
        with open(self.hub_file, "w", encoding="utf-8") as f:
            f.write(template)

    def build_subpages(self, category_label="Foundations"):
        all_topics = self.get_all_topics()
        sidebar_html = '<nav class="pl-2">'
        for t in all_topics:
            slug = slugify(t["title"])
            sidebar_html += f'<a href="{slug}.html" class="sb-link">{t["title"]}</a>'
        sidebar_html += '</nav>'
        
        for i, topic in enumerate(all_topics):
            slug = slugify(topic["title"])
            file_path = os.path.join(self.output_dir, f"{slug}.html")
            
            prev_topic = all_topics[i-1] if i > 0 else None
            next_topic = all_topics[i+1] if i < len(all_topics)-1 else None
            
            prev_html = f"""<a href="{slugify(prev_topic['title'])}.html" class="nav-card prev"><span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span><span class="nav-title">{prev_topic["title"]}</span></a>""" if prev_topic else ""
            next_html = f"""<a href="{slugify(next_topic['title'])}.html" class="nav-card next"><span class="nav-label">Next <i data-lucide="arrow-right"></i></span><span class="nav-title">{next_topic["title"]}</span></a>""" if next_topic else ""
            
            content = render_topic_content(topic)
            
            html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <title>{topic['title']} \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['JetBrains Mono','ui-monospace','monospace'],mono:['JetBrains Mono','ui-monospace','monospace']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="../../../css/ds-main.css">
    <link rel="stylesheet" href="../../../css/modules/code-blocks.css">
    <script src="../../../js/modules/universal-nav.js" defer></script>
    <script src="../../../js/modules/code-blocks.js" defer></script>
</head>
<body class="bg-surface text-on-surface min-h-screen">
    <div id="nav-universal"></div>
    <div class="flex flex-col lg:flex-row justify-center max-w-[1440px] mx-auto w-full">
        <div id="ds-main-content" class="transition-all duration-300 min-w-0">
            <main class="relative z-10 pt-28 pb-20 px-6 w-full max-w-4xl">
                <a href="../{self.section_id}.html" class="inline-flex items-center gap-2.5 px-5 py-2.5 bg-surface-container border border-on-surface/10 rounded-xl text-xs font-bold text-on-surface-variant hover:text-secondary-fixed hover:border-secondary-fixed transition-all mb-10 group no-underline">
                    <i data-lucide="arrow-left" class="w-4 h-4 group-hover:-translate-x-1 transition-transform"></i>
                    Back to {self.section_name.split(' ')[0]}
                </a>
                <header class="mb-12">
                    <div class="text-xs font-mono text-on-surface-variant uppercase tracking-[0.2em] mb-2">Section {topic['part_num']}: {topic.get('category', category_label)}</div>
                    <h1 class="text-3xl md:text-5xl font-bold text-on-surface mb-6 leading-tight">{topic['title']}</h1>
                </header>
                <article class="prose max-w-none pb-20">
                    {content}
                </article>
                <div class="nav-container">
                    {prev_html}
                    {next_html}
                </div>
            </main>
        </div>
        <aside class="toc-container"><div class="toc-title">On this page</div><ul class="toc-list"></ul></aside>
    </div>
    <script src="../../../js/ds-main.js" defer></script>
</body>
</html>"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
