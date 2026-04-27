import os
import json
import re

def slugify(text):
    s = text.lower()
    s = s.replace(" ", "-").replace("&", "and").replace("/", "-")
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s.strip("-")

def build_practice_hub(data):
    categories_html = ""
    for cat in data["categories"]:
        exercises_html = ""
        for ex in cat["exercises"]:
            exercises_html += f"""
            <a href="practice/{ex['slug']}.html" class="flex items-center justify-between p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl transition-all hover:border-{cat['color']}-300 hover:bg-{cat['color']}-50/30 group/ex no-underline">
                <div class="flex flex-col">
                    <span class="text-sm font-bold text-slate-700 dark:text-slate-300 group-hover/ex:text-{cat['color']}-600 transition-colors">{ex['title']}</span>
                    <span class="text-xs text-slate-500 mt-1">{ex['description']}</span>
                </div>
                <span class="text-[10px] font-black uppercase tracking-widest px-2 py-1 rounded bg-slate-100 dark:bg-slate-800 text-slate-500">{ex['difficulty']}</span>
            </a>"""

        categories_html += f"""
        <section class="mb-16">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-12 h-12 rounded-2xl bg-{cat['color']}-500/10 flex items-center justify-center text-{cat['color']}-600">
                    <i data-lucide="{cat['icon']}" class="w-6 h-6"></i>
                </div>
                <div>
                    <h2 class="text-2xl font-black text-slate-900 dark:text-white font-display">{cat['name']}</h2>
                    <p class="text-slate-500 text-sm">{cat['description']}</p>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {exercises_html}
            </div>
        </section>"""

    hub_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Practice Hub \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="pt-24 pb-20 px-6 max-w-5xl mx-auto">
            <header class="mb-16 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-violet-50 text-violet-700 rounded-full text-[10px] font-black uppercase tracking-widest mb-6">
                    <i data-lucide="hammer" class="w-3 h-3"></i> Skills Arena
                </div>
                <h1 class="text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tighter font-display">
                    Level Up Your <span class="bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">Craft</span>
                </h1>
                <p class="text-xl text-slate-500 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
                    {data['description']}
                </p>
            </header>

            {categories_html}
        </main>
    </div>
    <script>lucide.createIcons();</script>
</body>
</html>"""
    
    output_path = os.path.join('pages', 'practice.html')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(hub_template)
    print(f"Built Practice Hub: {output_path}")

def build_exercise_pages(data):
    for cat in data["categories"]:
        for ex in cat["exercises"]:
            slug = ex["slug"]
            file_path = os.path.join('pages', 'practice', f"{slug}.html")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{ex['title']} \u2014 Practice</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="pt-28 pb-20 px-6 max-w-4xl mx-auto">
            <a href="../practice.html" class="inline-flex items-center gap-2 text-sm font-bold text-violet-600 hover:text-violet-700 transition-colors mb-8 no-underline">
                <i data-lucide="arrow-left" class="w-4 h-4"></i> Back to Hub
            </a>

            <header class="mb-12">
                <div class="flex items-center gap-3 mb-4">
                    <span class="text-[10px] font-black uppercase tracking-widest px-2 py-1 rounded bg-violet-100 text-violet-600">{cat['name']}</span>
                    <span class="text-[10px] font-black uppercase tracking-widest px-2 py-1 rounded bg-slate-200 text-slate-600">{ex['difficulty']}</span>
                </div>
                <h1 class="text-4xl md:text-5xl font-black text-slate-900 dark:text-white tracking-tighter font-display">{ex['title']}</h1>
            </header>

            <div class="space-y-8">
                <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 shadow-sm">
                    <h2 class="text-lg font-bold mb-4 flex items-center gap-2">
                        <i data-lucide="help-circle" class="w-5 h-5 text-blue-500"></i> The Challenge
                    </h2>
                    <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                        {ex['description']} Imagine you are working on a high-scale data pipeline. Your task is to implement a solution that is both efficient and readable.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-slate-900 rounded-3xl p-8 text-white border border-slate-800">
                        <h3 class="text-sm font-bold uppercase tracking-widest text-slate-500 mb-4">Example Input</h3>
                        <pre class="font-mono text-sm text-indigo-300"><code># Input data here</code></pre>
                    </div>
                    <div class="bg-slate-900 rounded-3xl p-8 text-white border border-slate-800">
                        <h3 class="text-sm font-bold uppercase tracking-widest text-slate-500 mb-4">Expected Output</h3>
                        <pre class="font-mono text-sm text-emerald-400"><code># Output data here</code></pre>
                    </div>
                </div>

                <div class="bg-amber-50 dark:bg-amber-900/10 border border-amber-100 dark:border-amber-900/30 rounded-3xl p-8">
                    <h3 class="text-sm font-bold uppercase tracking-widest text-amber-700 dark:text-amber-500 mb-4 flex items-center gap-2">
                        <i data-lucide="lightbulb" class="w-4 h-4"></i> Pro Tip
                    </h3>
                    <p class="text-amber-800 dark:text-amber-400/80 text-sm italic">
                        Focus on time complexity. Avoid nested loops where possible.
                    </p>
                </div>
            </div>

            <footer class="mt-20 pt-8 border-t border-slate-200 dark:border-slate-800 text-center">
                <button class="px-8 py-3 bg-slate-900 dark:bg-white dark:text-slate-900 text-white font-bold rounded-xl hover:scale-105 transition-transform">
                    Reveal Solution
                </button>
            </footer>
        </main>
    </div>
    <script>lucide.createIcons();</script>
</body>
</html>"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Built Exercise: {file_path}")

if __name__ == "__main__":
    data_file = os.path.join('data', 'practice.json')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        build_practice_hub(data)
        build_exercise_pages(data)
    else:
        print(f"Error: {data_file} not found.")
