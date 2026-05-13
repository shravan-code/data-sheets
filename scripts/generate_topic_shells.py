import os
import json
import re

# Configuration: which guides to generate shells for
GUIDES = {
    "sql": "data/sql_complete_guide.json",
    "aws": "data/aws_complete_guide.json",
    "kafka": "data/kafka_complete_guide.json",
    "spark": "data/spark_complete_guide.json",
    "pandas": "data/pandas_complete_guide.json",
    "bash": "data/bash_guide.json",
    "powershell": "data/powershell_guide.json",
    "airflow": "data/airflow_complete_guide.json",
    "flink": "data/flink_guide.json",
    "dbt": "data/dbt_guide.json",
    "numpy": "data/numpy_guide.json",
    "regex": "data/regex_guide.json"
}

# Standard slugify function to match json-guide.js
def slugify(text):
    if not text: return ""
    s = str(text).lower().strip()
    s = s.replace("&", "and")
    s = s.replace("+", "plus")
    s = s.replace("#", "sharp")
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip("-")

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <script>(function(){
        document.documentElement.classList.remove('dark');
        localStorage.setItem('ds-theme', 'light');
    })();</script>
    <title>Loading... — Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={darkMode:'class',theme:{extend:{fontFamily:{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link rel="stylesheet" href="../../css/ds-main.css">
    <link id="prism-theme-light" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css">
    <link id="prism-theme-dark" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css">
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-6xl mx-auto">
            <div class="animate-pulse flex flex-col gap-6">
                <div class="h-4 bg-slate-200 dark:bg-slate-800 rounded w-1/4"></div>
                <div class="h-12 bg-slate-200 dark:bg-slate-800 rounded w-1/2"></div>
                <div class="h-64 bg-slate-100 dark:bg-slate-900 rounded-3xl w-full"></div>
                <div class="space-y-4">
                    <div class="h-4 bg-slate-200 dark:bg-slate-800 rounded"></div>
                    <div class="h-4 bg-slate-200 dark:bg-slate-800 rounded w-5/6"></div>
                    <div class="h-4 bg-slate-200 dark:bg-slate-800 rounded w-4/6"></div>
                </div>
            </div>
        </main>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="../../js/json-guide.js" defer></script>
    <script src="../../js/ds-main.js" defer></script>
</body>
</html>"""

def main():
    for guide_type, json_path in GUIDES.items():
        if not os.path.exists(json_path):
            print(f"Skipping {guide_type}: {json_path} not found")
            continue
            
        print(f"Processing {guide_type}...")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Handle both structures
        sections = []
        if "guide" in data:
            sections = data["guide"].get("sections") or data["guide"].get("topics") or []
        else:
            sections = data.get("sections") or data.get("topics") or []
            
        slugs = []
        for section in sections:
            topics = section.get("topics") or section.get("subtopics") or []
            if not topics:
                # If no topics, the section itself might be a topic
                slugs.append(slugify(section.get("title") or section.get("name")))
            else:
                for topic in topics:
                    slugs.append(slugify(topic.get("name") or topic.get("title") or topic.get("topic")))
        
        # Unique slugs
        slugs = list(set([s for s in slugs if s]))
        
        # Create directory
        out_dir = os.path.join("pages", guide_type)
        os.makedirs(out_dir, exist_ok=True)
        
        # Generate files
        count = 0
        for slug in slugs:
            file_path = os.path.join(out_dir, f"{slug}.html")
            # For SQL, we might be overwriting broken files. For others, creating new ones.
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(TEMPLATE)
            count += 1
            
        print(f"  Generated {count} shell pages in {out_dir}")

if __name__ == "__main__":
    main()
