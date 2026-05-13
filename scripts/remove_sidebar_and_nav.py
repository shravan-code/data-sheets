import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Remove <nav id="ds-nav"> ... </nav> block
    # We use a pattern that matches <nav id="ds-nav" ... > to </nav>
    # Note: re.DOTALL is important.
    content = re.sub(r'<nav id="ds-nav".*?</nav>', '', content, flags=re.DOTALL)

    # 2. Remove <aside id="ds-sidebar"> ... </aside>
    content = re.sub(r'<aside id="ds-sidebar".*?</aside>', '', content, flags=re.DOTALL)

    # 3. Remove <div id="sidebar-overlay"> ... </div>
    content = re.sub(r'<div id="sidebar-overlay".*?</div>', '', content, flags=re.DOTALL)

    # 4. Remove sidebar-toggle button just in case
    content = re.sub(r'<button id="sidebar-toggle".*?</button>', '', content, flags=re.DOTALL)

    # 5. Remove lg:pl-60 classes
    content = re.sub(r'\blg:pl-60\b', '', content)

    # 6. Remove any existing footer
    content = re.sub(r'<footer.*?</footer>', '', content, flags=re.DOTALL)

    # Cleanup any extra spaces inside class="" that we might have created
    content = re.sub(r'class="\s+', 'class="', content)
    content = re.sub(r'\s+"', '"', content) # if class ends with space
    content = re.sub(r'class=""', '', content) # remove empty class

    # Because some python scripts use `{global_sidebar}` or `{sidebar_html}`,
    # they might still exist in f-strings.
    content = re.sub(r'\{global_sidebar\}', '', content)
    content = re.sub(r'\{active_sidebar\}', '', content)
    content = re.sub(r'\{sidebar_html\}', '', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for dirpath, _, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.html') or filename.endswith('.py'):
                # skip this script itself
                if filename == "remove_sidebar_and_nav.py":
                    continue
                filepath = os.path.join(dirpath, filename)
                process_file(filepath)

if __name__ == "__main__":
    main()
