import json
import os

def render_portfolio():
    with open('data/portfolio_data.json', 'r') as f:
        data = json.load(f)

    # Helper to render skills/tags
    def render_badges(badges, color="blue"):
        return "\n".join([f'<span class="px-2 py-0.5 bg-{color}-500/10 text-{color}-500 border border-{color}-500/20 rounded text-[10px] font-bold uppercase tracking-wider">{b.upper()}</span>' for b in badges])

    # 1. Build pages/portfolio.html (HUB PAGE)
    arsenal_html = ""
    for item in data['arsenal']:
        arsenal_html += f"""
                    <div class="path-card {item['color']} group">
                        <div class="accent-bar bg-none from-{item['color']}-500 via-{item['color']}-400 to-accent-{item['color']}"></div>
                        <div class="flex justify-between items-start mb-6 relative z-10">
                            <div class="icon-box">
                                <i data-lucide="{item['icon']}" class="w-8 h-8 text-on-surface group-hover:text-accent-{item['color']} transition-colors"></i>
                            </div>
                            <span class="text-xs font-mono text-on-surface-variant group-hover:text-accent-{item['color']} transition-colors">[{item['id']}]</span>
                        </div>
                        <h3 class="text-xl font-bold path-title mb-2 tracking-tight relative z-10">{item['category']}</h3>
                        <p class="text-sm path-desc mb-8 flex-grow leading-relaxed relative z-10">
                            {item['description']}
                        </p>
                        <div class="exec-module relative z-10">
                            <span class="px-2 py-0.5 bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 rounded text-[10px] font-bold">READY</span>
                            <span class="group-hover:text-accent-{item['color']} transition-colors">STACK_LOADED</span>
                        </div>
                    </div>"""

    journey_html = ""
    for item in data['journey']:
        journey_html += f"""
                    <div class="feature-card group">
                        <div class="icon-box w-14 h-14 rounded-2xl bg-surface-container-high flex items-center justify-center text-{item['color']}-500">
                            <i data-lucide="{item['icon']}" class="w-6 h-6"></i>
                        </div>
                        <div class="flex-1">
                            <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-2">
                                <h3 class="font-bold text-on-surface">{item['role']} @ {item['company']}</h3>
                                <span class="text-[10px] font-mono text-on-surface-variant uppercase tracking-widest">{item['period']}</span>
                            </div>
                            <p class="text-sm text-on-surface-variant leading-relaxed">
                                {item['description']}
                            </p>
                        </div>
                    </div>"""

    portfolio_template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio | {data['profile']['name']}</title>
    <meta name="description" content="{data['profile']['description']}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['JetBrains Mono', 'ui-monospace', 'monospace'],
                        mono: ['JetBrains Mono', 'ui-monospace', 'monospace']
                    }}
                }}
            }}
        }}
    </script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="../css/ds-main.css">
    <link rel="stylesheet" href="../css/ds-home.css">
    <link rel="stylesheet" href="../css/modules/code-blocks.css">
    <script src="../js/modules/universal-nav.js" defer></script>
    <script src="../js/modules/code-blocks.js" defer></script>
</head>
<body class="bg-surface text-on-surface min-h-screen flex flex-col overflow-x-hidden">
    <div id="nav-universal"></div>
    <div id="ds-main-content" class="transition-all duration-300 min-w-0">
        <main class="flex-1 w-full">
            <section class="w-full border-b border-outline-variant relative overflow-hidden">
                <div class="absolute top-0 right-0 w-1/2 h-full border-l border-outline-variant opacity-20 pointer-events-none grid-bg"></div>
                <div class="w-full max-w-[1200px] mx-auto px-4 md:px-10 py-16 md:py-20 relative z-10 flex flex-col md:flex-row items-center gap-12">
                    <div class="flex-shrink-0 relative group">
                        <div class="w-48 h-48 md:w-56 md:h-56 rounded-full overflow-hidden border-4 border-surface-container shadow-2xl relative z-10 transition-transform duration-500 group-hover:scale-105">
                            <img src="../assets/images/profile-pic.jpeg" alt="{data['profile']['name']}" class="w-full h-full object-cover dark:grayscale transition-all duration-700">
                        </div>
                        <div class="absolute -inset-2 bg-gradient-to-tr from-blue-500 to-emerald-500 rounded-full blur opacity-20 group-hover:opacity-40 transition-opacity"></div>
                    </div>
                    <div class="max-w-2xl text-center md:text-left">
                        <div class="flex items-center justify-center md:justify-start gap-2 mb-6">
                            <i data-lucide="terminal" class="w-4 h-4 text-on-surface"></i>
                            <span class="text-sm text-on-surface font-mono font-bold bg-surface-container px-2 py-1 rounded-md ring-1 ring-outline-variant">&gt; whoami</span>
                        </div>
                        <h1 class="text-4xl md:text-6xl font-bold text-on-surface mb-6 leading-tight">
                            {data['profile']['name']}
                        </h1>
                        <p class="text-lg text-on-surface-variant mb-10 border-l-2 border-outline-variant pl-6 leading-relaxed max-w-xl mx-auto md:mx-0 text-left">
                            {data['profile']['description']}
                        </p>
                        <div class="flex flex-wrap justify-center md:justify-start gap-4">
                            <a href="mailto:{data['profile']['email']}" class="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-xl font-bold shadow-lg shadow-blue-500/20 hover:scale-105 transition-transform">
                                <i data-lucide="mail" class="w-4 h-4"></i>
                                Contact Me
                            </a>
                            <div class="flex items-center gap-2">
                                <a href="{data['profile']['linkedin']}" target="_blank" class="w-12 h-12 flex items-center justify-center rounded-xl bg-surface-container border border-outline-variant hover:border-blue-500/50 hover:text-blue-500 transition-all">
                                    <i data-lucide="linkedin" class="w-5 h-5"></i>
                                </a>
                                <a href="{data['profile']['github']}" target="_blank" class="w-12 h-12 flex items-center justify-center rounded-xl bg-surface-container border border-outline-variant hover:border-on-surface transition-all">
                                    <i data-lucide="github" class="w-5 h-5"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <section class="w-full max-w-[1200px] mx-auto px-4 md:px-10 py-16 md:py-24">
                <div class="flex items-center gap-2 mb-10 border-b border-outline-variant pb-4">
                    <span class="text-sm font-mono text-on-surface-variant">#</span>
                    <h2 class="text-sm font-mono text-on-surface-variant uppercase tracking-[0.2em] border-b border-on-surface/10 pb-2">Technical_Arsenal</h2>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {arsenal_html}
                </div>
            </section>
            <section class="w-full max-w-[1200px] mx-auto px-4 md:px-10 pb-24">
                <div class="flex items-center gap-2 mb-10 border-b border-outline-variant pb-4">
                    <span class="text-sm font-mono text-on-surface-variant">#</span>
                    <h2 class="text-sm font-mono text-on-surface-variant uppercase tracking-[0.2em] border-b border-on-surface/10 pb-2">The_Journey</h2>
                </div>
                <div class="space-y-6">
                    {journey_html}
                </div>
            </section>
            <section class="w-full max-w-[1200px] mx-auto px-4 md:px-10 pb-32">
                <div class="flex items-center gap-2 mb-10 border-b border-outline-variant pb-4">
                    <span class="text-sm font-mono text-on-surface-variant">#</span>
                    <h2 class="text-sm font-mono text-on-surface-variant uppercase tracking-[0.2em] border-b border-on-surface/10 pb-2">Explore_Work</h2>
                </div>
                <div class="flex flex-col sm:flex-row gap-6">
                    <a href="my-portfolio/projects-experienced.html" class="feature-card flex-1 group no-underline">
                        <div class="icon-box w-11 h-11 rounded-xl bg-surface-container-high flex items-center justify-center text-blue-500 transition-all">
                            <i data-lucide="terminal" class="w-5 h-5"></i>
                        </div>
                        <div>
                            <div class="font-bold text-on-surface text-sm">Professional Work</div>
                            <div class="text-xs text-on-surface-variant mt-0.5">Production-grade enterprise solutions</div>
                        </div>
                        <i data-lucide="arrow-right" class="card-arrow w-5 h-5"></i>
                    </a>
                    <a href="my-portfolio/projects-self.html" class="feature-card flex-1 group no-underline">
                        <div class="icon-box w-11 h-11 rounded-xl bg-surface-container-high flex items-center justify-center text-emerald-500 transition-all">
                            <i data-lucide="sparkles" class="w-5 h-5"></i>
                        </div>
                        <div>
                            <div class="font-bold text-on-surface text-sm">Personal Sandbox</div>
                            <div class="text-xs text-on-surface-variant mt-0.5">Experiments in AI and Distributed Systems</div>
                        </div>
                        <i data-lucide="arrow-right" class="card-arrow w-5 h-5"></i>
                    </a>
                </div>
            </section>
        </main>
        <footer class="bg-surface border-t border-outline-variant w-full mt-auto">
            <div class="flex flex-col md:flex-row justify-between items-center px-4 md:px-10 py-8 w-full max-w-[1200px] mx-auto gap-4">
                <div class="flex flex-col items-center md:items-start gap-1">
                    <div class="flex items-center gap-2 text-on-surface">
                        <i data-lucide="code-2" class="w-5 h-5"></i>
                        <span class="font-bold text-lg uppercase tracking-wider">Data Cake</span>
                    </div>
                    <span class="text-[10px] uppercase font-mono tracking-widest text-on-surface-variant opacity-60">&copy; 2026 {data['profile']['name']}. Engineered with Data Cake</span>
                </div>
            </div>
        </footer>
    </div>
    <script src="../js/ds-main.js" defer></script>
    <script>
        window.addEventListener('DOMContentLoaded', () => {{
            if(window.lucide) lucide.createIcons();
        }});
    </script>
</body>
</html>"""

    with open('pages/portfolio.html', 'w') as f:
        f.write(portfolio_template)

    # 2. Build sub-pages (DOCUMENTATION STYLE)
    def build_project_page(filename, projects, title_accent, back_link="../portfolio.html"):
        project_sections = ""
        toc_items = ""
        
        for p in projects:
            p_id = p['title'].lower().replace(' ', '-')
            toc_items += f'<li class="toc-item"><a href="#{p_id}" class="toc-link">{p["title"]}</a></li>'
            
            project_sections += f"""
                <section id="{p_id}" class="mb-24 scroll-mt-24">
                    <div class="flex items-center gap-4 mb-6">
                        <div class="w-12 h-12 rounded-2xl bg-{p['color']}-500/10 flex items-center justify-center border border-{p['color']}-500/20">
                            <i data-lucide="{p['icon']}" class="w-6 h-6 text-{p['color']}-500"></i>
                        </div>
                        <h2 class="text-2xl md:text-3xl font-bold text-on-surface tracking-tight">{p['title']}</h2>
                    </div>
                    
                    <div class="prose max-w-none mb-8">
                        <p class="text-lg text-on-surface-variant leading-relaxed">
                            {p['description']}
                        </p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                        <div class="p-6 bg-surface-container border border-outline-variant rounded-2xl">
                            <h4 class="text-[10px] font-black uppercase tracking-widest text-on-surface-variant mb-4 flex items-center gap-2">
                                <i data-lucide="zap" class="w-3.5 h-3.5"></i> Core Impact
                            </h4>
                            <p class="text-sm font-bold text-on-surface leading-snug">{p['impact']}</p>
                        </div>
                        <div class="p-6 bg-surface-container border border-outline-variant rounded-2xl">
                            <h4 class="text-[10px] font-black uppercase tracking-widest text-on-surface-variant mb-4 flex items-center gap-2">
                                <i data-lucide="cpu" class="w-3.5 h-3.5"></i> Status
                            </h4>
                            <p class="text-sm font-bold text-secondary-fixed leading-snug tracking-wider">{p['status']}</p>
                        </div>
                        <div class="p-6 bg-surface-container border border-outline-variant rounded-2xl">
                            <h4 class="text-[10px] font-black uppercase tracking-widest text-on-surface-variant mb-4 flex items-center gap-2">
                                <i data-lucide="layers" class="w-3.5 h-3.5"></i> Stack
                            </h4>
                            <div class="flex flex-wrap gap-2">
                                {render_badges(p['tags'], p['color'])}
                            </div>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <h4 class="text-xs font-black text-on-surface-variant uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
                            <span class="w-4 h-px bg-outline-variant"></span> Technical Highlights
                        </h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {"".join([f'<div class="flex items-start gap-3 p-4 bg-surface-container/50 border border-outline-variant/50 rounded-xl hover:border-{p["color"]}-500/30 transition-colors"><i data-lucide="check-circle" class="w-4 h-4 text-{p["color"]}-500 flex-shrink-0 mt-0.5"></i><p class="text-sm text-on-surface-variant leading-relaxed">{detail}</p></div>' for detail in p['details']])}
                        </div>
                    </div>
                </section>"""

        template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_accent} | {data['profile']['name']}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['JetBrains Mono', 'ui-monospace', 'monospace'],
                        mono: ['JetBrains Mono', 'ui-monospace', 'monospace']
                    }}
                }}
            }}
        }}
    </script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <link rel="stylesheet" href="../../css/ds-main.css">
    <link rel="stylesheet" href="../../css/ds-home.css">
    <link rel="stylesheet" href="../../css/modules/code-blocks.css">
    <script src="../../js/modules/universal-nav.js" defer></script>
    <script src="../../js/modules/code-blocks.js" defer></script>
</head>
<body class="bg-surface text-on-surface min-h-screen">
    <div id="nav-universal"></div>
    <div class="flex flex-col lg:flex-row justify-center max-w-[1440px] mx-auto w-full">
        <div id="ds-main-content" class="transition-all duration-300 min-w-0">
            <main class="relative z-10 pt-16 pb-20 px-6 w-full max-w-4xl">
                <a href="{back_link}" class="inline-flex items-center gap-2.5 px-5 py-2.5 bg-surface-container border border-on-surface/10 rounded-xl text-xs font-bold text-on-surface-variant hover:text-secondary-fixed hover:border-secondary-fixed transition-all mb-10 group no-underline">
                    <i data-lucide="arrow-left" class="w-4 h-4 group-hover:-translate-x-1 transition-transform"></i>
                    Back to Portfolio
                </a>
                
                <header class="mb-20">
                    <div class="text-[10px] font-mono text-on-surface-variant uppercase tracking-[0.3em] mb-4">Shravan Kumar Tela / Projects</div>
                    <h1 class="text-4xl md:text-5xl font-bold text-on-surface mb-6 leading-tight">
                        {title_accent.split(' ')[0]} <span class="text-secondary-fixed">{title_accent.split(' ')[1]}</span>
                    </h1>
                </header>

                <article class="prose max-w-none">
                    {project_sections}
                </article>

                <div class="mt-20 pt-10 border-t border-outline-variant flex justify-center">
                    <a href="../portfolio.html" class="px-8 py-4 bg-surface-container border border-outline-variant rounded-2xl font-bold hover:border-secondary-fixed transition-all">
                        Explore More Sections
                    </a>
                </div>
            </main>
        </div>
        <aside class="toc-container">
            <div class="toc-title">On this page</div>
            <ul class="toc-list">
                {toc_items}
            </ul>
        </aside>
    </div>
    <script src="../../js/ds-main.js" defer></script>
    <script>
        window.addEventListener('DOMContentLoaded', () => {{
            if(window.lucide) lucide.createIcons();
        }});
    </script>
</body>
</html>"""
        
        with open(filename, 'w') as f:
            f.write(template)

    build_project_page('pages/my-portfolio/projects-experienced.html', data['projects']['professional'], "Professional Work")
    build_project_page('pages/my-portfolio/projects-self.html', data['projects']['self_taught'], "Personal Sandbox")

if __name__ == "__main__":
    render_portfolio()
