"""
rebuild_core.py
==============
Shared logic for patching documentation pages with the modular UI.
"""

import os, re, glob, subprocess, sys, time

def compute_prefix(html_path):
    norm = html_path.replace('\\', '/')
    depth = len(norm.split('/')) - 1
    return '../' * depth

def get_nav_sidebar(prefix):
    return f"""<div id="nav-universal"></div>"""

def patch_html(path):
    version = int(time.time())
    
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    prefix = compute_prefix(os.path.relpath(path).replace('\\', '/'))

    # 1. Cleanup old injections
    html = re.sub(r'<html\b[^>]*class="[^"]*dark[^"]*"[^>]*>', lambda m: m.group(0).replace('dark', ''), html)
    html = re.sub(r'<!-- NAV -->.*?<!-- SIDEBAR OVERLAY \(mobile\) -->', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*═+\s*SIDEBAR\s*═+\s*-->.*?<!--\s*SCROLL TO TOP\s*-->', '', html, flags=re.DOTALL)
    html = re.sub(r'<!-- SIDEBAR -->.*?</aside>', '', html, flags=re.DOTALL)
    
    # Extract guide topics if they exist (legacy support)
    guide_topics_match = re.search(r'<div class="toc-title mt-8">(.*?)</div>\s*<ul class="toc-list">(.*?)</ul>', html, flags=re.DOTALL)
    if guide_topics_match:
        html = html.replace(guide_topics_match.group(0), '')

    html = re.sub(r'<nav\s+id="ds-nav".*?>.*?</nav>', '', html, flags=re.DOTALL)
    html = re.sub(r'<aside id="ds-sidebar"\b[^>]*?>.*?</aside>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div id="sidebar-overlay"[^>]*?>.*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<button id="scroll-top"[^>]*?>.*?</button>', '', html, flags=re.DOTALL)
    
    # Remove old theme scripts
    html = re.sub(r'<script>\(function\(\){const s=localStorage.getItem\(\'ds-theme\'\);.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*\(function\(\)\s*{\s*const html\s*=\s*document\.documentElement;.*?</script>', '', html, flags=re.DOTALL)
    
    # 2. Inject External CSS & JS
    css_tags = f"""
    <link rel="stylesheet" href="{prefix}css/ds-main.css?v={version}">
    <link rel="stylesheet" href="{prefix}css/modules/code-blocks.css?v={version}">
    <script src="{prefix}js/modules/universal-nav.js?v={version}" defer></script>
    <script src="{prefix}js/modules/code-blocks.js?v={version}" defer></script>
    """
    
    if 'ds-main.css' not in html:
        html = html.replace('</head>', css_tags + '\n</head>', 1)
    else:
        html = re.sub(r'<link rel="stylesheet" href="[^"]*ds-main.css[^"]*">', f'<link rel="stylesheet" href="{prefix}css/ds-main.css?v={version}">', html)
        if 'code-blocks.css' not in html:
            html = html.replace('</head>', css_tags + '\n</head>', 1)

    # 3. Inject Nav placeholder after <body>
    body_match = re.search(r'<body\b[^>]*>', html)
    if body_match:
        pos = body_match.end()
        nav_placeholder = get_nav_sidebar(prefix)
        if 'id="nav-universal"' not in html:
            html = html[:pos] + '\n\n' + nav_placeholder + '\n\n' + html[pos:]

    # 4. Wrap main content if needed
    if 'id="ds-main-content"' not in html:
        html = re.sub(r'(<main\b[^>]*>)', r'<div id="ds-main-content" class="transition-all duration-300 min-w-0">\1', html)
        html = html.replace('</main>', '</main>\n</div>', 1)

    # 5. Inject External JS if not present
    js_tag = f'<script src="{prefix}js/ds-main.js?v={version}" defer></script>'
    if 'ds-main.js' not in html:
        if '</body>' in html:
            html = html.replace('</body>', js_tag + '\n</body>', 1)
        else:
            html += js_tag

    # 6. Ensure light theme by default
    if 'document.documentElement.classList.remove(\'dark\')' not in html:
        theme_init = """<script>(function(){
            document.documentElement.classList.remove('dark');
            localStorage.setItem('ds-theme', 'light');
        })();</script>"""
        html = html.replace('<head>', '<head>\n' + theme_init, 1)

    # Replace "Data Sheets" with "Data Cake"
    html = html.replace('Data Sheets', 'Data Cake')

    # 7. Adaptive Code Blocks (Prism)
    prism_light = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css"
    prism_dark = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css"
    prism_js = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"
    prism_autoloader = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"
    
    if '<pre' in html or '<code' in html:
        if 'id="prism-theme-light"' not in html:
            adaptive_prism = f'<link id="prism-theme-light" rel="stylesheet" href="{prism_light}">\n    <link id="prism-theme-dark" rel="stylesheet" href="{prism_dark}">'
            html = html.replace('</head>', f'    {adaptive_prism}\n</head>', 1)
        if 'prism.min.js' not in html:
            prism_scripts = f'<script src="{prism_js}"></script>\n    <script src="{prism_autoloader}"></script>'
            html = html.replace('</body>', f'    {prism_scripts}\n</body>', 1)

    # 6.5 Clean up H2 titles (remove decorative spans and left borders/padding)
    def clean_h2(m):
        tag_start = m.group(1)
        classes = m.group(2)
        # Remove specific classes
        classes = re.sub(r'\b(border-l|pl-\d+|md:pl-\d+|border-outline-variant|border-b|border-on-surface/(?:10|5)|pb-2)\b', '', classes)
        # Add underline classes (5% for python, 10% for others)
        opacity = "5" if "python" in path.lower() else "10"
        classes += f" border-b border-on-surface/{opacity} pb-2"
        # Clean up double spaces
        classes = re.sub(r'\s+', ' ', classes).strip()
        return f'{tag_start} class="{classes}"'

    html = re.sub(r'(<h2\b[^>]*?)\s+class="([^"]*)"', clean_h2, html)
    html = re.sub(r'(<h2\b[^>]*?>)\s*<span\b[^>]*?class="[^"]*?(?:rounded-full|bg-secondary-fixed|bg-blue-600|bg-blue-500|bg-emerald-500)[^"]*?"[^>]*?></span>', r'\1', html)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def run_builder(script_name):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    script_path = os.path.join(root, 'scripts', script_name)
    if os.path.exists(script_path):
        print(f"  Running {script_name}...")
        r = subprocess.run([sys.executable, script_path], capture_output=True, text=True, cwd=root)
        if r.returncode != 0:
            print(f"    WARN: {script_name} failed:\n{r.stderr[-500:]}")
            return False
        print(f"    OK")
        return True
    return False

def rebuild_section(section_name, builder_script, directory_pattern):
    print(f"--- Rebuilding Section: {section_name} ---")
    
    # 1. Run Generator
    if builder_script:
        run_builder(builder_script)
    
    # 2. Patch HTML files
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    search_path = os.path.join(root, directory_pattern)
    files = glob.glob(search_path, recursive=True)
    
    print(f"  Patching {len(files)} files in {directory_pattern}...")
    for f in files:
        if 'node_modules' in f or 'components' in f: continue
        try:
            patch_html(f)
        except Exception as e:
            print(f"    ERR: {f}: {e}")
    
    print(f"--- {section_name} Done ---\n")
