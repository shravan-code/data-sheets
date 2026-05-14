import os, sys
from rebuild_core import rebuild_section

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(root)
    
    sections = [
        ("Practice", "build_practice.py", "pages/practice/**/*.html"),
        ("Roadmaps", "build_roadmaps.py", "pages/roadmaps/**/*.html"),
        ("PowerShell", "build_powershell_guide.py", "pages/learn/powershell/**/*.html"),
    ]
    
    for name, builder, pattern in sections:
        rebuild_section(name, builder, pattern)
