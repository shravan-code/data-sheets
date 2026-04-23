import re
import json

def markdown_to_html(md_text):
    def apply_inline(text):
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        return text

    def parse_table(table_md):
        lines = [l.strip() for l in table_md.strip().split('\n') if l.strip()]
        if len(lines) < 2: return table_md
        
        html = '<div class="overflow-x-auto my-6"><table class="min-w-full text-sm text-left border-collapse border border-slate-200 dark:border-slate-800">'
        
        # Header
        header_cells = [c.strip() for c in lines[0].split('|') if c.strip()]
        html += '<thead class="bg-slate-50 dark:bg-slate-800/50"><tr>'
        for cell in header_cells:
            html += f'<th class="px-4 py-2 border border-slate-200 dark:border-slate-700 font-bold">{apply_inline(cell)}</th>'
        html += '</tr></thead>'
        
        # Body
        html += '<tbody>'
        start_idx = 1
        if len(lines) > 1 and ('---' in lines[1] or '===' in lines[1]):
            start_idx = 2
            
        for line in lines[start_idx:]:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if not cells: continue
            html += '<tr>'
            for cell in cells:
                html += f'<td class="px-4 py-2 border border-slate-200 dark:border-slate-700">{apply_inline(cell)}</td>'
            html += '</tr>'
        html += '</tbody></table></div>'
        return html

    lines = md_text.split('\n')
    output = []
    in_code = False
    in_table = False
    table_lines = []
    in_list = False
    p_lines = []
    
    def flush_p():
        if p_lines:
            content = ' '.join(p_lines).strip()
            if content:
                output.append(f'<p>{apply_inline(content)}</p>')
            p_lines.clear()

    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('```'):
            flush_p()
            if in_table:
                output.append(parse_table('\n'.join(table_lines)))
                in_table = False
                table_lines = []
            if in_list:
                output.append('</ul>')
                in_list = False
                
            if not in_code:
                lang = stripped.replace('```', '') or 'text'
                output.append(f'<pre><code class="language-{lang}">')
                in_code = True
            else:
                output.append('</code></pre>')
                in_code = False
            continue
            
        if in_code:
            output.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            continue

        if stripped.startswith('|'):
            flush_p()
            if in_list:
                output.append('</ul>')
                in_list = False
            in_table = True
            table_lines.append(line)
            continue
        elif in_table:
            output.append(parse_table('\n'.join(table_lines)))
            in_table = False
            table_lines = []

        is_list_item = stripped.startswith('- ') or stripped.startswith('* ') or re.match(r'^\d+\.', stripped)
        if is_list_item:
            flush_p()
            if not in_list:
                output.append('<ul class="list-disc pl-5 my-4">')
                in_list = True
            if stripped.startswith('- ') or stripped.startswith('* '):
                item_content = stripped[2:]
            else:
                dot_idx = stripped.find('.')
                item_content = stripped[dot_idx+1:].strip()
            output.append(f'<li>{apply_inline(item_content)}</li>')
            continue
        elif in_list:
            output.append('</ul>')
            in_list = False

        if stripped.startswith('## '):
            flush_p()
            output.append(f'<h2>{apply_inline(stripped[3:])}</h2>')
        elif stripped.startswith('### '):
            flush_p()
            output.append(f'<h3>{apply_inline(stripped[4:])}</h3>')
        elif stripped.startswith('# '):
            flush_p()
            output.append(f'<h2>{apply_inline(stripped[2:])}</h2>')
        elif stripped.startswith('> '):
            flush_p()
            output.append(f'<blockquote>{apply_inline(stripped[2:])}</blockquote>')
        elif stripped == '---':
            flush_p()
            output.append('<hr>')
        elif stripped == '':
            flush_p()
            output.append('<br>')
        else:
            p_lines.append(line)
            
    flush_p()
    if in_table: output.append(parse_table('\n'.join(table_lines)))
    if in_list: output.append('</ul>')
    if in_code: output.append('</code></pre>')
    
    return '\n'.join(output)

# Read the guide
with open('data_pipeline_guide.md', 'r', encoding='utf-8') as f:
    full_content = f.read()

main_titles = [
    "Fundamentals", "Pipeline Types", "Ingestion Layer Design", "Processing Layer Design",
    "Storage Layer Design", "Batch Pipeline Design", "Streaming Pipeline Design",
    "CDC Pipeline Design", "Orchestration Design", "Data Quality in Pipelines",
    "Pipeline Observability", "Performance & Optimization", "Security in Pipelines",
    "Pipeline Design Patterns", "Classic Pipeline Design Problems"
]

icons = [
    "book-open", "layers", "download-cloud", "cpu", "database", "calendar", "zap",
    "refresh-cw", "git-branch", "check-circle", "activity", "fast-forward", "shield", "copy", "hammer"
]

descriptions = [
    "Core concepts, components, and design principles of data pipelines.",
    "Batch, Streaming, Micro-batch, and Hybrid architectures.",
    "How data enters the system: CDC, API, Files, and Events.",
    "Stateless vs Stateful, Transformations, and Error Handling.",
    "Medallion architecture, partitioning, and file formats.",
    "Scheduling, windowing, and incremental batch patterns.",
    "Event time, windowing, and exactly-once semantics.",
    "Log-based CDC, Debezium, and handling schema changes.",
    "DAGs, retry strategies, and dependency management.",
    "Validation, schema enforcement, and quarantine patterns.",
    "Logging, metrics, lineage, and health dashboards.",
    "Parallelism, data skew, and cost optimization.",
    "Encryption, PII masking, and secrets management.",
    "Classic architecture patterns: Medallion, Lambda, Kappa.",
    "Practical scenarios and architectural challenges."
]

# Find matches only for these titles
sections = []
for i, title in enumerate(main_titles):
    pattern = re.compile(rf'^# {i+1}\. {re.escape(title)}', re.MULTILINE)
    match = pattern.search(full_content)
    if match:
        sections.append({
            "num": i+1,
            "title": title,
            "start": match.start(),
            "end": match.end()
        })

print(f"Found {len(sections)} main sections.")

subpages_list = []
for i in range(len(sections)):
    sec = sections[i]
    content_start = sec["end"]
    content_end = sections[i+1]["start"] if i+1 < len(sections) else len(full_content)
    
    content_md = full_content[content_start:content_end].strip()
    html_content = markdown_to_html(content_md)
    
    idx = sec["num"] - 1
    subpages_list.append({
        "id": sec["title"].lower().replace(" & ", "-").replace(" ", "-"),
        "title": f"{sec['num']}. {sec['title']}",
        "icon": icons[idx],
        "description": descriptions[idx],
        "content": html_content
    })

# Save to JSON
with open('subpages_data.json', 'w', encoding='utf-8') as f:
    json.dump(subpages_list, f, indent=4)

print(f"Successfully processed {len(subpages_list)} sections into subpages_data.json")
