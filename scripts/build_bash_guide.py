import json
import os

def build_bash_hub():
    # Data is now in data/
    data_path = os.path.join('data', 'bash_subpages_data.json')
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        subpages = json.load(f)
        
    cards_html = []
    for page in subpages:
        cards_html.append(f"""
    <a href="bash/{page['id']}.html" class="topic-card group bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800/60 rounded-2xl p-6 no-underline transition-all hover:shadow-xl hover:shadow-blue-500/5 hover:-translate-y-1">
        <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 group-hover:bg-blue-600 group-hover:text-white transition-all duration-300">
                <i data-lucide="{page['icon']}" class="w-6 h-6"></i>
            </div>
            <div class="flex-1">
                <h3 class="font-display font-bold text-lg text-slate-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{page['title']}</h3>
                <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed line-clamp-2">{page['description']}</p>
            </div>
        </div>
    </a>""")

    hub_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Bash Scripting — Data Sheets</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-5xl mx-auto">
    <a href="../learn.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to Learn
    </a>

    <header class="mb-12">
        <div class="flex items-center gap-4 mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400">
                <i data-lucide="terminal" class="w-7 h-7"></i>
            </div>
            <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white leading-tight tracking-tight">Bash Scripting</h1>
        </div>
        <p class="text-xl text-slate-600 dark:text-slate-400 max-w-3xl leading-relaxed">Master the art of automation. From basic commands to complex system scripts and cross-platform comparisons.</p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        {"".join(cards_html)}
    </div>
</main>
</body>
</html>"""

    output_path = os.path.join('pages', 'learn', 'bash.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(hub_template)
    print(f"Built Bash Hub: {output_path}")

def build_bash_subpages():
    data_path = os.path.join('data', 'bash_subpages_data.json')
    if not os.path.exists(data_path):
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        subpages = json.load(f)
        
    os.makedirs(os.path.join('pages', 'learn', 'bash'), exist_ok=True)

    for i, page in enumerate(subpages):
        prev_page = subpages[i-1] if i > 0 else None
        next_page = subpages[i+1] if i < len(subpages)-1 else None
        
        prev_html = f"""
            <a href="{prev_page['id']}.html" class="flex flex-col items-start no-underline group">
                <span class="text-xs text-slate-500 mb-1 flex items-center gap-1"><i data-lucide="arrow-left" class="w-3 h-3"></i> Previous</span>
                <span class="text-sm font-bold text-slate-900 dark:text-white group-hover:text-blue-600 transition-colors text-left">{prev_page['title']}</span>
            </a>""" if prev_page else "<div></div>"
            
        next_html = f"""
            <a href="{next_page['id']}.html" class="flex flex-col items-end no-underline group text-right">
                <span class="text-xs text-slate-500 mb-1 flex items-center gap-1">Next <i data-lucide="arrow-right" class="w-3 h-3"></i></span>
                <span class="text-sm font-bold text-slate-900 dark:text-white group-hover:text-blue-600 transition-colors text-right">{next_page['title']}</span>
            </a>""" if next_page else "<div></div>"

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{page['title']} — Bash Scripting</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-4xl mx-auto">
    <a href="../bash.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to Bash Scripting
    </a>

    <header class="mb-12">
        <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4 leading-tight tracking-tight">{page['title']}</h1>
        <p class="text-xl text-slate-600 dark:text-slate-400 font-medium">{page['description']}</p>
    </header>

    <article class="prose dark:prose-invert max-w-none pb-20">
        {page['content']}
    </article>

    <div class="mt-16 pt-8 border-t border-slate-200 dark:border-slate-800 flex justify-between items-center">
        {prev_html}
        {next_html}
    </div>
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
</body>
</html>"""
        
        file_path = os.path.join('pages', 'learn', 'bash', f"{page['id']}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Built subpage: {file_path}")

if __name__ == "__main__":
    build_bash_hub()
    build_bash_subpages()
