import os
import json
import re

PART_ICONS = {
    1:"database",
    2:"plus-square",
    3:"edit-3",
    4:"search",
    5:"lock",
    6:"refresh-cw",
    7:"filter",
    8:"git-merge",
    9:"bar-chart-2",
    10:"layers",
    11:"copy",
    12:"type",
    13:"table",
    14:"code",
    15:"activity",
    16:"clock",
    17:"layout",
    18:"zap",
    19:"gauge",
    20:"cpu",
    21:"component",
    22:"git-branch",
    23:"settings",
    24:"info",
    25:"shield",
    26:"terminal",
    27:"globe",
    28:"codesandbox",
    29:"help-circle",
    30:"award",
}

def slugify(text):
    s = text.lower()
    s = s.replace("","-").replace("&","and").replace("/","-")
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s.strip("-")

def render_sql_table(data, title=""):
    if not data or not isinstance(data, list):
        return""
    
    headers = data[0].keys() if data else []
    if not headers:
        return""
    
    parts = []
    if title:
        parts.append(f'<div class="text-[10px] uppercase tracking-widest text-slate-400 mb-3 font-bold flex items-center gap-2"><i data-lucide="table" class="w-3 h-3"></i> {title}</div>')
    
    parts.append('<div class="overflow-x-auto my-4 rounded-xl border border-slate-200 shadow-sm">')
    parts.append('<table class="min-w-full border-collapse text-sm">')
    parts.append('<thead class="bg-slate-50 border-b border-slate-200">')
    parts.append('<tr>')
    for h in headers:
        parts.append(f'<th class="p-3 text-left font-bold text-slate-700 uppercase tracking-wider text-[10px]">{h}</th>')
    parts.append('</tr>')
    parts.append('</thead>')
    parts.append('<tbody class="divide-y divide-slate-100 bg-white">')
    for row in data:
        parts.append('<tr class="hover:bg-slate-50/50 transition-colors">')
        for h in headers:
            val = row.get(h,"")
            if val is None: val = '<span class="text-slate-300">NULL</span>'
            parts.append(f'<td class="p-3 text-slate-600 font-mono text-xs">{val}</td>')
        parts.append('</tr>')
    parts.append('</tbody></table></div>')
    return"\n".join(parts)

def render_example(ex):
    if isinstance(ex, str):
        ex_clean = ex.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        return f'<div class="my-8 group"><div class="relative rounded-xl overflow-hidden bg-white border border-slate-200 shadow-sm transition-all hover:shadow-md p-6"><pre class="language-sql"><code>{ex_clean}</code></pre></div></div>'
    
    parts = []
    if ex.get("description"):
        parts.append(f'<h3 class="text-xl font-bold text-slate-800 dark:text-slate-200 mb-4">{ex["description"]}</h3>')
    
    if ex.get("sql"):
        sql = ex["sql"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        
        # Determine output type
        output_html =""
        if ex.get("output_table") is not None:
            output_html = render_sql_table(ex["output_table"],"Output Table")
        elif ex.get("output") is not None:
            if isinstance(ex["output"], list):
                output_html = render_sql_table(ex["output"],"Output Result")
            else:
                out_str = str(ex["output"]).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                output_html = f"""
                <div class="mt-6 pt-6 border-t border-slate-100 bg-slate-50/50 -mx-6 -mb-6 px-6 pb-6">
                    <div class="text-[10px] uppercase tracking-widest text-slate-400 mb-3 font-bold flex items-center gap-2"><i data-lucide="terminal" class="w-3 h-3"></i> Output</div>
                    <pre class="!m-0 !p-0 !bg-transparent !border-0 !shadow-none !rounded-none"><code class="text-blue-600 font-mono text-sm leading-relaxed">{out_str}</code></pre>
                </div>"""
        
        # Before/After tables
        before_after_html =""
        if ex.get("before"):
            before_after_html += render_sql_table(ex["before"],"Before")
        if ex.get("after"):
            before_after_html += render_sql_table(ex["after"],"After")

        # Combine into a card
        parts.append(f'<div class="my-8 group">')
        parts.append(f'<div class="relative rounded-xl overflow-hidden bg-white border border-slate-200 shadow-sm transition-all hover:shadow-md p-6">')
        if before_after_html:
            parts.append('<div class="mb-6 space-y-4">' + before_after_html + '</div>')
        parts.append(f'<pre class="language-sql"><code>{sql}</code></pre>')
        if output_html:
            parts.append(output_html)
        parts.append(f'</div></div>')
    
    # Handle direct table in example
    if ex.get("tables"):
        for name, data in ex["tables"].items():
            parts.append(render_sql_table(data, f"Table: {name}"))
            
    if ex.get("note"):
        parts.append(f'<p class="text-sm italic text-slate-500 mb-4 bg-slate-100 p-3 rounded-lg border-l-4 border-blue-400">{ex["note"]}</p>')

    return"\n".join(parts)

def render_topic_content(topic):
    parts = []
    
    # 1. Primary Explanation/Description
    for key in ["explanation","description"]:
        if topic.get(key):
            parts.append(f'<p class="text-xl text-slate-600 dark:text-slate-400 mb-8 leading-relaxed font-medium">{topic[key]}</p>')
            
    # 2. Core Conceptual Sections (Theory First)
    theory_sections = {"normal_forms":"Normal Forms","anomalies":"Database Anomalies","benefits":"Key Benefits","use_cases":"Common Use Cases","structure":"Logical Structure","components":"Core Components","difference_from_star":"Snowflake vs Star Schema","lock_types":"Locking Mechanisms","levels":"Isolation Levels","types":"Available Types","key_nodes":"Internal Structure","frame_options":"Window Frame Options","rows_vs_range":"ROWS vs RANGE Comparison"
    }
    
    for key, title in theory_sections.items():
        if topic.get(key):
            parts.append(f'<h2 class="text-3xl font-black text-slate-900 mb-6 mt-16 flex items-center gap-4 tracking-tight"><span class="w-2 h-10 bg-blue-600 rounded-full"></span>{title}</h2>')
            val = topic[key]
            
            # Special case for Normal Forms
            if key =="normal_forms":
                parts.append('<div class="space-y-10 my-8">')
                for nf in val:
                    parts.append(f"""
                    <div class="p-8 bg-white border border-slate-200 rounded-3xl shadow-sm hover:shadow-md transition-shadow">
                        <h3 class="text-2xl font-black text-slate-900 mb-3">{nf.get('form', 'Normal Form')}</h3>
                        <p class="text-slate-600 mb-8 text-lg leading-relaxed">{nf.get('rule', '')}</p>""")
                    if nf.get("applies_to"):
                         parts.append(f'<div class="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 text-blue-600 rounded-lg text-xs font-bold mb-6"><i data-lucide="info" class="w-3 h-3"></i> Applies to: {nf["applies_to"]}</div>')
                         
                    if nf.get("bad_example"):
                        parts.append(f'<div class="text-[10px] uppercase tracking-widest text-rose-500 font-black mb-3 ml-1">The Bad Approach</div>')
                        if isinstance(nf["bad_example"], (dict, list)):
                            json_bad = json.dumps(nf["bad_example"], indent=2).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                            parts.append(f'<div class="rounded-2xl overflow-hidden mb-8 border border-rose-100"><pre class="language-json !bg-rose-50/30 !m-0"><code>{json_bad}</code></pre></div>')
                        else:
                            parts.append(f'<div class="p-5 bg-rose-50/50 text-rose-700 rounded-2xl mb-8 border border-rose-100 font-mono text-sm leading-relaxed">{nf["bad_example"]}</div>')
                    
                    if nf.get("good_example"):
                        parts.append(f'<div class="text-[10px] uppercase tracking-widest text-emerald-500 font-black mb-3 ml-1">The Correct Way</div>')
                        if isinstance(nf["good_example"], list):
                            parts.append(render_sql_table(nf["good_example"]))
                        elif isinstance(nf["good_example"], dict):
                            json_good = json.dumps(nf["good_example"], indent=2).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                            parts.append(f'<div class="rounded-2xl overflow-hidden mb-8 border border-emerald-100"><pre class="language-json !bg-emerald-50/30 !m-0"><code>{json_good}</code></pre></div>')
                        else:
                            parts.append(f'<div class="p-5 bg-emerald-50/50 text-emerald-700 rounded-2xl mb-8 border border-emerald-100 font-mono text-sm leading-relaxed">{nf["good_example"]}</div>')
                    
                    if nf.get("fix"):
                         parts.append(f'<div class="p-4 bg-blue-50 text-blue-700 rounded-xl text-sm font-medium border border-blue-100"><span class="font-black mr-2">FIX:</span>{nf["fix"]}</div>')
                    
                    parts.append('</div>')
                parts.append('</div>')
            
            elif isinstance(val, list):
                if len(val) > 0 and isinstance(val[0], dict):
                    parts.append(render_sql_table(val))
                else:
                    parts.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-12">')
                    for item in val:
                        parts.append(f"""
                        <div class="flex items-start gap-4 p-5 bg-white border border-slate-200 rounded-2xl shadow-sm">
                            <div class="w-6 h-6 rounded-full bg-blue-50 flex items-center justify-center text-blue-500 flex-shrink-0 mt-0.5">
                                <i data-lucide="check-circle" class="w-4 h-4"></i>
                            </div>
                            <span class="text-slate-600 text-sm leading-relaxed">{item}</span>
                        </div>""")
                    parts.append('</div>')
            else:
                parts.append(f'<p class="text-slate-600 dark:text-slate-400 mb-12 text-lg leading-relaxed">{val}</p>')

    # 3. Syntax
    if topic.get("syntax"):
        syntax = topic["syntax"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        parts.append(f'<div class="bg-slate-900 rounded-2xl p-8 mb-12 border border-slate-800 shadow-xl">')
        parts.append(f'<div class="text-[10px] uppercase tracking-widest text-blue-400 mb-4 font-black">General Syntax</div>')
        parts.append(f'<pre class="!m-0 !p-0 !bg-transparent text-emerald-400 font-mono text-base leading-relaxed"><code>{syntax}</code></pre>')
        parts.append('</div>')

    # Specific key handlers
    if topic.get("properties"):
        parts.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">')
        for p in topic["properties"]:
            title = p.get('property', p.get('name', p.get('feature', 'Property')))
            desc = p.get('description', p.get('explanation', p.get('meaning', p.get('detail', ''))))
            parts.append(f"""
            <div class="p-4 bg-white border border-slate-200 rounded-xl shadow-sm">
                <h3 class="font-bold text-slate-900 mb-1 text-base">{title}</h3>
                <div class="text-sm text-slate-600">{desc}</div>
            </div>""")
        parts.append('</div>')

    if topic.get("comparison_table"):
        parts.append(render_sql_table(topic["comparison_table"],"Comparison"))

    if topic.get("categories"):
        for cat in topic["categories"]:
            parts.append(f'<h2 class="text-2xl font-bold text-slate-800 mb-4 mt-12 flex items-center gap-3"><span class="w-1.5 h-8 bg-blue-500 rounded-full"></span>{cat["category"]}</h2>')
            if cat.get("types"):
                parts.append(render_sql_table(cat["types"]))

    if topic.get("written_order"):
        parts.append('<div class="flex flex-wrap gap-2 mb-8">')
        for i, clause in enumerate(topic["written_order"]):
            parts.append(f'<span class="px-3 py-1 bg-slate-100 text-slate-700 rounded-md font-mono text-xs border border-slate-200">{clause}</span>')
            if i < len(topic["written_order"]) - 1:
                parts.append('<span class="text-slate-400 self-center">→</span>')
        parts.append('</div>')

    if topic.get("execution_order"):
        parts.append(render_sql_table(topic["execution_order"],"Execution Order"))

    # Examples
    if topic.get("example"):
        parts.append(render_example(topic["example"]))
    
    if topic.get("examples"):
        for ex in topic["examples"]:
            parts.append(render_example(ex))

    # Questions
    if topic.get("questions"):
        for q in topic["questions"]:
            parts.append(f'<div class="mb-10 p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm hover:shadow-md transition-shadow">')
            q_id = q.get("id", q.get("q_no","?"))
            parts.append(f'<h3 class="text-xl font-bold text-blue-600 dark:text-blue-400 mb-4 flex items-start gap-4 font-display">')
            parts.append(f'<span class="flex-shrink-0 w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center text-base font-black">{q_id}</span>')
            parts.append(f'<span class="pt-1.5">{q["question"]}</span></h3>')
            
            if q.get("sql"):
                sql = q["sql"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                parts.append(f'<pre class="language-sql mb-4"><code>{sql}</code></pre>')
                
            if q.get("alternative"):
                alt = q["alternative"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                parts.append(f'<div class="text-[10px] uppercase tracking-widest text-slate-400 mb-2 font-bold">Alternative Approach</div>')
                parts.append(f'<pre class="language-sql mb-4"><code>{alt}</code></pre>')

            if q.get("answer"):
                parts.append(f'<p class="text-slate-600 dark:text-slate-400 leading-relaxed pl-14 text-lg">A: {q["answer"]}</p>')
            parts.append(f'</div>')

    # 4. Pros & Cons
    if topic.get("pros") or topic.get("cons"):
        parts.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-12">')
        if topic.get("pros"):
            parts.append('<div class="p-6 bg-emerald-50/50 border border-emerald-100 rounded-3xl">')
            parts.append('<div class="flex items-center gap-2 text-emerald-700 font-black uppercase tracking-widest text-[10px] mb-4"><i data-lucide="check-circle" class="w-4 h-4"></i> Pros / Advantages</div>')
            parts.append('<ul class="space-y-3">')
            for p in topic["pros"]:
                parts.append(f'<li class="text-sm text-emerald-800 flex items-start gap-2"><span class="mt-1.5 w-1 h-1 rounded-full bg-emerald-400 flex-shrink-0"></span>{p}</li>')
            parts.append('</ul></div>')
        
        if topic.get("cons"):
            parts.append('<div class="p-6 bg-rose-50/50 border border-rose-100 rounded-3xl">')
            parts.append('<div class="flex items-center gap-2 text-rose-700 font-black uppercase tracking-widest text-[10px] mb-4"><i data-lucide="x-circle" class="w-4 h-4"></i> Cons / Limitations</div>')
            parts.append('<ul class="space-y-3">')
            for c in topic["cons"]:
                parts.append(f'<li class="text-sm text-rose-800 flex items-start gap-2"><span class="mt-1.5 w-1 h-1 rounded-full bg-rose-400 flex-shrink-0"></span>{c}</li>')
            parts.append('</ul></div>')
        parts.append('</div>')

    # 5. Tips & Tricks
    if topic.get("tips"):
        parts.append('<div class="my-12 p-8 bg-gradient-to-br from-indigo-600 to-blue-700 rounded-3xl text-white shadow-xl relative overflow-hidden">')
        parts.append('<div class="relative z-10">')
        parts.append('<div class="flex items-center gap-2 text-indigo-100 font-black uppercase tracking-widest text-[10px] mb-4"><i data-lucide="zap" class="w-4 h-4"></i> Pro Tips & Tricks</div>')
        parts.append('<ul class="grid grid-cols-1 md:grid-cols-2 gap-4">')
        for tip in topic["tips"]:
            parts.append(f'<li class="text-sm text-white/90 flex items-start gap-3 bg-white/10 p-4 rounded-xl backdrop-blur-sm"><i data-lucide="lightbulb" class="w-4 h-4 text-yellow-300 flex-shrink-0 mt-0.5"></i>{tip}</li>')
        parts.append('</ul></div>')
        parts.append('<i data-lucide="sparkles" class="absolute -right-4 -bottom-4 w-32 h-32 text-white/5 rotate-12"></i>')
        parts.append('</div>')

    # 6. Common Issues & Solutions
    if topic.get("common_issues"):
        parts.append('<div class="my-16">')
        parts.append('<h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2"><i data-lucide="alert-triangle" class="w-5 h-5 text-amber-500"></i> Troubleshooting & Common Issues</h3>')
        parts.append('<div class="space-y-4">')
        for issue in topic["common_issues"]:
            parts.append(f"""
            <div class="border border-slate-200 rounded-2xl overflow-hidden">
                <div class="px-6 py-4 bg-slate-50 border-b border-slate-200 font-bold text-slate-700 flex items-center gap-3">
                    <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                    Issue: {issue['issue']}
                </div>
                <div class="p-6 bg-white text-slate-600 text-sm leading-relaxed">
                    <span class="font-black text-blue-600 mr-2 uppercase text-[10px]">Solution:</span> {issue['solution']}
                </div>
            </div>""")
        parts.append('</div></div>')

    # 7. Specialized handlers for dialects
    dialects = ["postgresql","mysql","mssql"]
    if any(d in topic for d in dialects):
        parts.append('<div class="grid grid-cols-1 gap-6 mb-12">')
        for d in dialects:
            if topic.get(d):
                code = str(topic[d]).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                parts.append(f"""
                <div class="rounded-xl overflow-hidden border border-slate-200 shadow-sm bg-white">
                    <div class="px-4 py-2 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
                        <span class="text-[10px] font-bold uppercase tracking-widest text-slate-500">{d.upper()}</span>
                        <i data-lucide="database" class="w-3 h-3 text-slate-400"></i>
                    </div>
                    <div class="p-4">
                        <pre class="language-sql !bg-transparent !m-0 !p-0"><code>{code}</code></pre>
                    </div>
                </div>""")
        parts.append('</div>')

    if topic.get("note"):
         parts.append(f'<div class="p-4 bg-amber-50 border-l-4 border-amber-400 text-amber-900 text-sm mb-8 rounded-r-xl">{topic["note"]}</div>')

    # Catch-all for other keys to ensure full data coverage
    exclude_keys = ["name","title","topic","explanation","description","syntax","properties","comparison_table","categories","written_order","execution_order","example","examples","questions","note","setup_note","setup_table","setup_tables","section_title","section_id","postgresql","mysql","mssql","id","pros","cons","tips","common_issues","sql","code","query","pattern"] + list(theory_sections.keys())
    
    for key, value in topic.items():
        if key not in exclude_keys and value:
            key_title = key.replace("_","").title()
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                parts.append(f'<h4 class="text-lg font-bold text-slate-800 mb-2 mt-6">{key_title}</h4>')
                parts.append(render_sql_table(value))
            elif isinstance(value, dict):
                parts.append(f'<h4 class="text-lg font-bold text-slate-800 mb-2 mt-6">{key_title}</h4>')
                json_str = json.dumps(value, indent=2).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                parts.append(f'<pre class="language-json"><code>{json_str}</code></pre>')
            else:
                parts.append(f'<div class="mt-8">')
                parts.append(f'<span class="text-[10px] font-black uppercase tracking-widest text-slate-400 block mb-2">{key_title}</span>')
                
                # Check if value looks like SQL
                if isinstance(value, str) and ("SELECT" in value.upper() or"CREATE" in value.upper() or"UPDATE" in value.upper()):
                    code = value.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                    parts.append(f'<div class="rounded-xl overflow-hidden border border-slate-200"><pre class="language-sql !m-0"><code>{code}</code></pre></div>')
                else:
                    parts.append(f'<p class="text-slate-600 italic border-l-2 border-slate-200 pl-4">{value}</p>')
                parts.append(f'</div>')

    return"\n".join(parts)

def build_sql_hub(data):
    sections = data["guide"]["sections"]
    
    # 11 Phases for the roadmap
    phases = [
        {"name":"Foundations","section_ids": [1]},
        {"name":"Core Language","section_ids": [2, 3, 4, 5, 6]},
        {"name":"Filtering & Joins","section_ids": [7, 8]},
        {"name":"Aggregations & Subqueries","section_ids": [9, 10]},
        {"name":"Set Ops & Data Types","section_ids": [11, 12, 13]},
        {"name":"Programming & Logic","section_ids": [14, 15, 16]},
        {"name":"Advanced Window Functions","section_ids": [17, 18]},
        {"name":"Optimization & Internals","section_ids": [19, 20]},
        {"name":"Design & Hierarchy","section_ids": [21, 22]},
        {"name":"System & Metadata","section_ids": [23, 24, 25]},
        {"name":"Professional SQL","section_ids": [26, 27, 28, 29, 30]}
    ]
    
    phases_html =""
    for i, phase in enumerate(phases):
        num = i + 1
        items_html =""
        for sid in phase["section_ids"]:
            section = next((s for s in sections if s["id"] == sid), None)
            if not section: continue
            
            icon = PART_ICONS.get(sid,"database")
            
            # For large sections like interview questions, maybe link to the section title
            if section.get("topics"):
                for topic in section["topics"]:
                    title = topic.get("name", topic.get("title", topic.get("topic","Topic")))
                    slug = slugify(title)
                    items_html += f"""
                    <a href="sql/{slug}.html" id="{slug}" style="scroll-margin-top: 100px;" class="flex items-center gap-3 p-4 bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800 rounded-2xl transition-all hover:bg-blue-50/50 dark:hover:bg-blue-900/20 hover:border-blue-200 group/item no-underline shadow-sm hover:shadow-md">
                        <div class="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-900/50 flex items-center justify-center text-blue-600 dark:text-blue-400 group-hover/item:bg-blue-600 group-hover/item:text-white transition-all">
                            <i data-lucide="{icon}" class="w-5 h-5"></i>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-sm font-bold text-slate-700 dark:text-slate-300 group-hover/item:text-blue-700 transition-colors">{title}</span>
                        </div>
                    </a>"""
            else:
                title = section.get("title","Section")
                slug = slugify(title)
                items_html += f"""
                <a href="sql/{slug}.html" id="{slug}" style="scroll-margin-top: 100px;" class="flex items-center gap-3 p-4 bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800 rounded-2xl transition-all hover:bg-blue-50/50 dark:hover:bg-blue-900/20 hover:border-blue-200 group/item no-underline shadow-sm hover:shadow-md">
                    <div class="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-900/50 flex items-center justify-center text-blue-600 dark:text-blue-400 group-hover/item:bg-blue-600 group-hover/item:text-white transition-all">
                        <i data-lucide="{icon}" class="w-5 h-5"></i>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-sm font-bold text-slate-700 dark:text-slate-300 group-hover/item:text-blue-700 transition-colors">{title}</span>
                    </div>
                </a>"""

        phases_html += f"""
        <section class="mb-12">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center text-blue-600">
                    <span class="text-xl font-black">{num}</span>
                </div>
                <h2 class="text-3xl font-black text-slate-900 dark:text-white font-display tracking-tight">{phase['name']}</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {items_html}
            </div>
        </section>"""

    hub_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>SQL Mastery \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Master SQL from fundamentals to advanced query optimization for data engineering.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-6xl mx-auto">
            <!-- HERO -->
            <header class="mb-20 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border border-blue-100 dark:border-blue-800">
                    <i data-lucide="database" class="w-3 h-3"></i> SQL Documentation
                </div>
                <h1 class="font-display text-6xl md:text-8xl font-black text-slate-900 dark:text-white mb-8 tracking-tighter leading-tight">
                    SQL <span class="bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-400 bg-clip-text text-transparent">Mastery</span>
                </h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium">
                    The bedrock of data engineering. From basic CRUD to advanced window functions and performance tuning.
                </p>
            </header>

            <!-- CARD CONTENT -->
            <div class="space-y-16">
                {phases_html}
            </div>

            
        </main>
    </div>
    <script>lucide.createIcons();</script>
</body>
</html>"""
    
    output_path = os.path.join('pages', 'learn', 'sql.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path,"w", encoding="utf-8") as f:
        f.write(hub_template)
    print(f"Built SQL Hub: {output_path}")

def build_sql_subpages(data):
    sections = data["guide"]["sections"]
    all_topics = []
    
    for section in sections:
        if section.get("topics"):
            for topic in section["topics"]:
                topic["section_title"] = section["title"]
                topic["section_id"] = section["id"]
                # Carry over setup tables to each topic
                topic["setup_table"] = section.get("setup_table")
                topic["setup_tables"] = section.get("setup_tables")
                topic["setup_note"] = section.get("setup_note")
                all_topics.append(topic)
        else:
            section["section_title"] = section["title"]
            section["section_id"] = section["id"]
            all_topics.append(section)
            
    os.makedirs(os.path.join('pages', 'learn', 'sql'), exist_ok=True)
    
    # Sidebar
    sidebar_html = '<div class="toc-title mt-8">SQL Guide</div><ul class="toc-list">'
    for t in all_topics:
        title = t.get("name", t.get("title", t.get("topic","Topic")))
        slug = slugify(title)
        sidebar_html += f'<li><a href="{slug}.html" class="toc-link">{title}</a></li>'
    sidebar_html += '</ul>'
    
    for i, topic in enumerate(all_topics):
        title = topic.get("name", topic.get("title", topic.get("topic","Topic")))
        slug = slugify(title)
        file_path = os.path.join('pages', 'learn', 'sql', f"{slug}.html")
        
        # Navigation
        prev_topic = all_topics[i-1] if i > 0 else None
        next_topic = all_topics[i+1] if i < len(all_topics)-1 else None
        
        prev_html =""
        if prev_topic:
            p_title = prev_topic.get("name", prev_topic.get("title", prev_topic.get("topic","Topic")))
            pslug = slugify(p_title)
            prev_html = f"""
            <a href="{pslug}.html" class="nav-card prev">
                <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
                <span class="nav-title">{p_title}</span>
            </a>"""
            
        next_html =""
        if next_topic:
            n_title = next_topic.get("name", next_topic.get("title", next_topic.get("topic","Topic")))
            nslug = slugify(n_title)
            next_html = f"""
            <a href="{nslug}.html" class="nav-card next">
                <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
                <span class="nav-title">{n_title}</span>
            </a>"""
            
        # Topic Header
        content_parts = []
        
        # Setup tables at the very top
        if topic.get("setup_note"):
            content_parts.append(f'<div class="p-4 bg-blue-50 border-l-4 border-blue-400 text-blue-900 text-sm mb-8 rounded-r-xl">{topic["setup_note"]}</div>')

        if topic.get("setup_table"):
            content_parts.append('<div class="mb-12">')
            content_parts.append(f'<h3 class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Base Table Context: {topic["setup_table"]["name"]}</h3>')
            content_parts.append(render_sql_table(topic["setup_table"]["data"]))
            content_parts.append('</div>')

        if topic.get("setup_tables"):
            content_parts.append('<div class="mb-12 space-y-8">')
            for name, data in topic["setup_tables"].items():
                content_parts.append(f'<div><h3 class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Base Table Context: {name}</h3>')
                content_parts.append(render_sql_table(data))
                content_parts.append('</div>')
            content_parts.append('</div>')

        content_parts.append(render_topic_content(topic))
        content ="\n".join(content_parts)
            
        active_sidebar = sidebar_html.replace(f'href="{slug}.html" class="toc-link"', f'href="{slug}.html" class="toc-link active"')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title} \u2014 SQL Guide</title>
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
            <a href="../sql.html#{slug}" class="inline-flex items-center gap-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors mb-6 group no-underline">
                <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
                Back to SQL
            </a>
            <header class="mb-12">
                <div class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-4 flex items-center gap-2">
                    <span class="w-8 h-[1px] bg-slate-300"></span>
                    Section {topic.get('section_id', '?')}: {topic.get('section_title', 'General')}
                </div>
                <h1 class="text-4xl md:text-6xl font-black text-slate-900 dark:text-white leading-tight tracking-tighter font-display">
                    {title}
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
            
        </aside>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
    <script>lucide.createIcons();</script>
</body>
</html>"""
        
        with open(file_path,"w", encoding="utf-8") as f:
            f.write(html)
            
    print(f"Built {len(all_topics)} SQL subpages.")

if __name__ =="__main__":
    data_file = os.path.join('data', 'sql_complete_guide.json')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        build_sql_hub(data)
        build_sql_subpages(data)
    else:
        print(f"Error: {data_file} not found.")
