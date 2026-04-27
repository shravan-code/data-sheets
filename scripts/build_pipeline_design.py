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

roadmap_phases = [
    {
        "name": "Phase 1 — Core Foundations",
        "items": [
            {"name": "What is a Data Pipeline?", "id": "fundamentals"},
            {"name": "Pipeline Components", "id": "fundamentals"},
            {"name": "Idempotency & Replayability", "id": "fundamentals"},
            {"name": "SLA & Monitoring Basics", "id": "fundamentals"}
        ]
    },
    {
        "name": "Phase 2 — Architecture Strategies",
        "items": [
            {"name": "Batch vs Streaming vs Hybrid", "id": "pipeline-types"},
            {"name": "ETL vs ELT Patterns", "id": "pipeline-types"},
            {"name": "Reverse ETL", "id": "pipeline-types"},
            {"name": "Lambda & Kappa Architectures", "id": "pipeline-design-patterns"}
        ]
    },
    {
        "name": "Phase 3 — Ingestion Layer",
        "items": [
            {"name": "Log-based CDC (Debezium)", "id": "cdc-pipeline-design"},
            {"name": "API & Webhook Ingestion", "id": "ingestion-layer-design"},
            {"name": "File-based Ingestion (S3)", "id": "ingestion-layer-design"},
            {"name": "Incremental vs Full Loads", "id": "ingestion-layer-design"}
        ]
    },
    {
        "name": "Phase 4 — Processing Layer",
        "items": [
            {"name": "Stateless vs Stateful", "id": "processing-layer-design"},
            {"name": "Transformation Patterns", "id": "processing-layer-design"},
            {"name": "Error Handling & DLQs", "id": "processing-layer-design"},
            {"name": "Parallel Processing Design", "id": "processing-layer-design"}
        ]
    },
    {
        "name": "Phase 5 — Storage Layer",
        "items": [
            {"name": "Medallion Architecture", "id": "storage-layer-design"},
            {"name": "Partitioning Strategies", "id": "storage-layer-design"},
            {"name": "File Formats (Parquet/Avro)", "id": "storage-layer-design"},
            {"name": "Compaction & Vacuuming", "id": "storage-layer-design"}
        ]
    },
    {
        "name": "Phase 6 — Batch Design",
        "items": [
            {"name": "Airflow DAG Anatomy", "id": "batch-pipeline-design"},
            {"name": "Scheduling & Windowing", "id": "batch-pipeline-design"},
            {"name": "Upsert Patterns (Merge)", "id": "batch-pipeline-design"},
            {"name": "Backfill Strategies", "id": "batch-pipeline-design"}
        ]
    },
    {
        "name": "Phase 7 — Streaming Design",
        "items": [
            {"name": "Event Time vs Processing Time", "id": "streaming-pipeline-design"},
            {"name": "Streaming Windows", "id": "streaming-pipeline-design"},
            {"name": "Watermarking & Late Data", "id": "streaming-pipeline-design"},
            {"name": "Exactly-once Semantics", "id": "streaming-pipeline-design"}
        ]
    },
    {
        "name": "Phase 8 — Orchestration",
        "items": [
            {"name": "DAG Design Principles", "id": "orchestration-design"},
            {"name": "Dynamic DAG Generation", "id": "orchestration-design"},
            {"name": "Cross-DAG Dependencies", "id": "orchestration-design"},
            {"name": "Retry & Timeout Policies", "id": "orchestration-design"}
        ]
    },
    {
        "name": "Phase 9 — Data Quality",
        "items": [
            {"name": "Validation at Ingestion", "id": "data-quality-in-pipelines"},
            {"name": "Data Quality Gates", "id": "data-quality-in-pipelines"},
            {"name": "Quarantine Pattern", "id": "data-quality-in-pipelines"},
            {"name": "Schema Enforcement", "id": "data-quality-in-pipelines"}
        ]
    },
    {
        "name": "Phase 10 — Pipeline Observability",
        "items": [
            {"name": "Structured Logging", "id": "pipeline-observability"},
            {"name": "Prometheus Metrics", "id": "pipeline-observability"},
            {"name": "Data Lineage Tracking", "id": "pipeline-observability"},
            {"name": "Health Dashboards", "id": "pipeline-observability"}
        ]
    },
    {
        "name": "Phase 11 — Optimization & Security",
        "items": [
            {"name": "Handling Data Skew", "id": "performance-optimization"},
            {"name": "Pushdown Optimization", "id": "performance-optimization"},
            {"name": "PII Masking & Redaction", "id": "security-in-pipelines"},
            {"name": "Secrets Management", "id": "security-in-pipelines"}
        ]
    }
]

hub_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Pipeline Design Mastery — Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Architecting robust, scalable, and observable data lifecycles for the modern data stack.">
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
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-amber-100 text-amber-700 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border-2 border-amber-200/50">
                    <i data-lucide="map" class="w-3 h-3"></i> Pipeline Architecture
                </div>
                <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-tight">
                    Pipeline <span class="bg-gradient-to-r from-amber-600 to-orange-400 bg-clip-text text-transparent">Design</span>
                </h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium italic">
                    "Architecting robust, scalable, and observable data lifecycles for the modern data stack."
                </p>
            </header>

            <!-- CARD CONTENT -->
            <div class="space-y-16">
                {phases_html}
            </div>
            
            <footer class="mt-20 py-10 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-medium text-xs tracking-widest uppercase text-[10px]">\u00a9 2026 Data Cake \u2022 Pipeline Mastery</p>
            </footer>
        </main>
    </div>
    <script>lucide.createIcons();</script>
</body>
</html>'''

def generate_index():
    phases_html = ""
    for i, phase in enumerate(roadmap_phases):
        num = i + 1
        items_html = ""
        for item in phase['items']:
            items_html += f"""
            <a href="pipeline-design/{item['id']}.html" class="flex items-center gap-3 p-3 bg-amber-50/30 dark:bg-slate-900 border border-amber-100/50 dark:border-slate-800 rounded-xl transition-all hover:bg-amber-50 dark:hover:bg-amber-900/20 hover:border-amber-200 group/item no-underline">
                <div class="w-2 h-2 rounded-full bg-amber-400 group-hover/item:scale-125 transition-transform"></div>
                <span class="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover/item:text-amber-700 transition-colors">{item['name']}</span>
            </a>"""

        phases_html += f"""
        <section class="mb-12">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center text-amber-600">
                    <span class="text-sm font-black">{num}</span>
                </div>
                <h2 class="text-2xl font-bold text-slate-900 dark:text-white font-display tracking-tight">{phase['name'].split(' — ')[1]}</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {items_html}
            </div>
        </section>"""

    hub_content = hub_template.format(phases_html=phases_html)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(hub_content)

def generate_subpages():
    for i, page in enumerate(subpages):
        prev_page = subpages[i-1] if i > 0 else None
        next_page = subpages[i+1] if i < len(subpages)-1 else None
        
        prev_html = f"""
            <a href="{prev_page['id']}.html" class="nav-card prev">
                <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
                <span class="nav-title">{prev_page['title']}</span>
            </a>""" if prev_page else "<div></div>"

        next_html = f"""
            <a href="{next_page['id']}.html" class="nav-card next">
                <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
                <span class="nav-title">{next_page['title']}</span>
            </a>""" if next_page else "<div></div>"

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
    <script src="https://unpkg.com/lucide@0.395.0"></script>
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
        <a href="../pipeline-design.html" class="inline-flex items-center gap-2 text-sm font-medium text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 transition-colors mb-6 group no-underline">
            <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
            Back to Pipeline Design
        </a>

        <header class="mb-12">
            <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4 leading-tight tracking-tight">{page['title']}</h1>
            <p class="text-xl text-slate-600 dark:text-slate-400 font-medium">{page['description']}</p>
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
    print(f"Generated Pipeline Design Roadmap and {len(subpages)} subpages.")
