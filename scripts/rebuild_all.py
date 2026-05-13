"""
rebuild_all.py
==============
Organizes the build process and patches all HTML files to use the shared layout."""

import os, re, glob, subprocess, sys

# ---------------------------------------------------------------------------
# NAV + SIDEBAR HTML  (prefix = relative path back to project root)
# ---------------------------------------------------------------------------

def get_nav_sidebar(prefix, page_title="", guide_topics_html=""):
    return f"""\
<!-- NAV -->


<!-- SIDEBAR OVERLAY (mobile) -->


<!-- SIDEBAR -->


<button id="scroll-top" title="Back to top"
    class="fixed bottom-6 right-6 z-50 w-10 h-10 flex items-center justify-center rounded-full
           bg-gradient-to-br from-blue-500 to-violet-600 text-white
           shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-110 scale-90 transition-all duration-200">
    <i data-lucide="arrow-up" class="w-4 h-4"></i>
</button>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compute_prefix(html_path):
    norm = html_path.replace('\\', '/')
    # For scripts/rebuild_all.py, the root is ../
    # But if we run from root, it's different.
    # Let's assume we run from the project root.
    depth = len(norm.split('/')) - 1
    return '../' * depth


def patch_html(path):
    import time
    # Use a timestamp as a version for cache busting
    version = int(time.time())
    
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    prefix = compute_prefix(os.path.relpath(path).replace('\\', '/'))

    # 1. Cleanup old injections (aggressive)
    html = re.sub(r'<html\b[^>]*class="[^"]*dark[^"]*"[^>]*>', lambda m: m.group(0).replace('dark', ''), html)
    html = re.sub(r'<!-- NAV -->.*?<!-- SIDEBAR OVERLAY \(mobile\) -->', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*═+\s*SIDEBAR\s*═+\s*-->.*?<!--\s*SCROLL TO TOP\s*-->', '', html, flags=re.DOTALL)
    html = re.sub(r'<!-- SIDEBAR -->.*?</aside>', '', html, flags=re.DOTALL)
    # Extract guide topics if they exist before wiping the container
    # Extract guide topics (e.g."Bash Topics" or"Fundamentals")
    # We look for the 'mt-8' class which we use for guide-wide navigation, 
    # and we ignore"On this page" which is for local page headers.
    guide_topics_match = re.search(r'<div class="toc-title mt-8">(.*?)</div>\s*<ul class="toc-list">(.*?)</ul>', html, flags=re.DOTALL)
    
    guide_topics_html =""
    if guide_topics_match:
        title = guide_topics_match.group(1).strip()
        list_items = guide_topics_match.group(2)
            
        # Convert toc-link to sb-link and remove <li> tags
        list_items = list_items.replace('<li>', '').replace('</li>', '')
        list_items = list_items.replace('toc-link', 'sb-link')
        
        # Standardize the injected section to look like other sb-cat sections
        guide_topics_html = f"""
        <div class="sb-section sb-cat bg-slate-50 text-slate-700 hover:bg-slate-100 cursor-pointer">
            <span class="w-6 h-6 rounded-md bg-slate-400 flex items-center justify-center flex-shrink-0">
                <i data-lucide="list" class="w-3 h-3 text-white"></i>
            </span>
            {title}
        </div>
        <nav class="pl-2">
            {list_items}
        </nav>"""
        # Remove it from the original content
        html = html.replace(guide_topics_match.group(0), '')

    html = re.sub(r'<nav\s+id="ds-nav".*?>.*?</nav>', '', html, flags=re.DOTALL)
    html = re.sub(r'', '', html, flags=re.DOTALL)
    html = re.sub(r'', '', html, flags=re.DOTALL)
    html = re.sub(r'<button id="scroll-top"[^>]*?>.*?</button>', '', html, flags=re.DOTALL)
    # DO NOT REMOVE toc-container ANYMORE
    # html = re.sub(r'<aside class="toc-container">.*?</aside>', '', html, flags=re.DOTALL)
    
    # Remove breadcrumb links (Back to Learn / Back to Home / Back to Guide)
    # html = re.sub(r'<a\s+href="[^"]*"(?:\s+class="[^"]*")?>\s*<i\s+data-lucide="arrow-left"[^>]*></i>\s*Back to.*?</a>', '', html, flags=re.DOTALL)
    
    # Remove any old theme initialization scripts
    html = re.sub(r'<script>\(function\(\){const s=localStorage.getItem\(\'ds-theme\'\);.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*\(function\(\)\s*{\s*const html\s*=\s*document\.documentElement;.*?</script>', '', html, flags=re.DOTALL)
    
    # Remove any stray Lucide initialization scripts or layout-fixes if they are redundant
    html = re.sub(r'<script src="[^"]*layout-fixes\.js"[^>]*></script>', '', html)
    html = re.sub(r'<link rel="stylesheet" href="[^"]*layout-fixes\.css">', '', html)
    
    # Remove inline styles and scripts previously injected
    html = re.sub(r'<style>\s*/\* DS_SHARED_SIDEBAR_STYLES \*/.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*\(function\(\)\s*{\s*const html\s*=\s*document\.documentElement;.*?</script>', '', html, flags=re.DOTALL)

    # 1.5 Extract Page Title for Nav
    # Try to get first part of title (before | or —)
    title_match = re.search(r'<title>(.*?)</title>', html)
    page_title =""
    if title_match:
        full_title = title_match.group(1).split('|')[0].split('—')[0].strip()
        # Hide title on homepage only
        if 'index.html' not in path:
            page_title = full_title

    # 2. Inject External CSS
    css_tag = f'<link rel="stylesheet" href="{prefix}css/ds-main.css?v={version}">'
    
    if 'ds-main.css' not in html:
        html = html.replace('</head>', css_tag + '\n</head>', 1)
    else:
        # Update existing link to correct prefix and add version
        html = re.sub(r'<link rel="stylesheet" href="[^"]*ds-main.css[^"]*">', css_tag, html)

    # 3. Inject Nav + Sidebar after <body>
    body_match = re.search(r'<body\b[^>]*>', html)
    if body_match:
        pos = body_match.end()
        # Pass guide_topics_html to the sidebar generator
        nav_sidebar = get_nav_sidebar(prefix, page_title, guide_topics_html)
        
        # Ensure guide-topics is visible if content exists
        if guide_topics_html:
            nav_sidebar = nav_sidebar.replace('id="guide-topics" class="mt-6 hidden"', 'id="guide-topics" class="mt-6"')
            
        html = html[:pos] + '\n\n' + nav_sidebar + '\n\n' + html[pos:]

    # 4. Wrap main content if needed
    if 'id="ds-main-content"' not in html:
        html = re.sub(r'(<main\b[^>]*>)', r'<div id="ds-main-content" class="transition-all duration-300 min-w-0">\1', html)
        html = html.replace('</main>', '</main>\n</div>', 1)

    # 4.5 Fix flex container centering bug on mobile
    html = html.replace('class="flex justify-center max-w-[1440px] mx-auto"', 'class="flex flex-col lg:flex-row justify-center max-w-[1440px] mx-auto w-full"')

    # 5. Inject External JS if not present
    js_tag = f'<script src="{prefix}js/ds-main.js?v={version}" defer></script>'
    if 'ds-main.js' not in html:
        if '</body>' in html:
            html = html.replace('</body>', js_tag + '\n</body>', 1)
        else:
            html += js_tag
    else:
        # Update existing script to correct prefix and add version
        html = re.sub(r'<script src="[^"]*ds-main.js[^"]*"[^>]*></script>', js_tag, html)

    # 6. Ensure light theme by default
    if 'document.documentElement.classList.remove(\'dark\')' not in html:
        theme_init ="""<script>(function(){
            document.documentElement.classList.remove('dark');
            localStorage.setItem('ds-theme', 'light');
        })();</script>"""
        html = html.replace('<head>', '<head>\n' + theme_init, 1)

    # Replace"Data Sheets" with"Data Cake" in titles
    html = html.replace('Data Sheets', 'Data Cake')

    # Redirect removed Learn page to Home
    html = html.replace(f'href="{prefix}pages/learn.html"', f'href="{prefix}index.html"')
    html = html.replace('Back to Learn', 'Back to Home')

    # 7. Adaptive Code Blocks (Prism)
    prism_light ="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css"
    prism_dark ="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css"
    prism_js ="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"
    prism_autoloader ="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"
    
    if '<pre' in html or '<code' in html:
        # 7a. Inject Adaptive CSS
        if 'id="prism-theme-light"' not in html:
            adaptive_prism = f'<link id="prism-theme-light" rel="stylesheet" href="{prism_light}">\n    <link id="prism-theme-dark" rel="stylesheet" href="{prism_dark}">'
            # Force injection into head
            html = html.replace('</head>', f'    {adaptive_prism}\n</head>', 1)
        
        # 7b. Inject Prism JS if missing
        if 'prism.min.js' not in html:
            prism_scripts = f'<script src="{prism_js}"></script>\n    <script src="{prism_autoloader}"></script>'
            html = html.replace('</body>', f'    {prism_scripts}\n</body>', 1)

    # 8. Clean up redundant/old prism links if any
    # Remove any prism links that don't have our IDs
    html = re.sub(r'<link rel="stylesheet" href="[^"]*prism(?!\-theme)[^"]*\.css">', '', html)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def run_builders():
    # Builders are now in scripts/
    builders = [
        'build_roadmaps.py', 'build_bash_guide.py', 'build_powershell_guide.py', 'build_python_guide.py',
        'build_sql_guide.py',
        'build_de_fundamentals.py', 'build_dsa.py', 'build_system_design.py', 'build_pipeline_design.py',
        'build_practice.py',
    ]
    for script in builders:
        script_path = os.path.join('scripts', script)
        if os.path.exists(script_path):
            print(f"  Running {script}...")
            # We run from root so scripts need to know where data is
            r = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            if r.returncode != 0:
                print(f"    WARN: {script} failed:\n{r.stderr[-500:]}")
            else:
                print(f"    OK")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Ensure we are in the root directory (one level up from scripts/)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)

    print(f"Working directory: {os.getcwd()}")

    print("Step 1: Regenerate sub-pages...")
    run_builders()

    print("Step 2: Patch all HTML files...")
    all_html = [p for p in glob.glob('**/*.html', recursive=True) if 'node_modules' not in p and 'components' not in p]
    for path in sorted(all_html):
        try:
            patch_html(path)
            print(f"  OK: {path}")
        except Exception as e:
            print(f"  ERR: {path}: {e}")

    print(f"\nDone — {len(all_html)} files patched.")
