"""
rebuild_all.py
==============
Master controller to rebuild the entire website using modular rebuilder scripts.
"""

import os, sys, subprocess

def run_script(script_name):
    print(f"Executing {script_name}...")
    root = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root, script_name)
    r = subprocess.run([sys.executable, script_path])
    if r.returncode != 0:
        print(f"Error executing {script_name}")

if __name__ == "__main__":
    scripts = [
        "rebuild_python.py",
        "rebuild_sql.py",
        "rebuild_bash.py",
        "rebuild_concepts.py",
        "rebuild_practice_roadmaps.py",
        "rebuild_agents.py",
        "rebuild_skills.py",
        "rebuild_portfolio.py",
        # Add more here as they are created
    ]
    
    # Also handle the miscellaneous pages (index, portfolio, etc.)
    from rebuild_core import patch_html
    import glob
    
    print("Patching root and miscellaneous pages...")
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    misc_files = [
        "index.html",
        "pages/portfolio.html",
        "pages/practice.html",
    ]
    for f in misc_files:
        path = os.path.join(root, f)
        if os.path.exists(path):
            print(f"  Patching {f}...")
            patch_html(path)

    for script in scripts:
        run_script(script)
        
    print("\nFull rebuild complete.")
