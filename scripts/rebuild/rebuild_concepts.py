import os, sys
from rebuild_core import rebuild_section

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(root)
    
    sections = [
        ("DE Fundamentals", "build_de_fundamentals.py", "pages/learn/de-fundamentals/**/*.html"),
        ("DSA for DE", "build_dsa.py", "pages/learn/dsa-de/**/*.html"),
        ("System Design", "build_system_design.py", "pages/learn/system-design/**/*.html"),
        ("Pipeline Design", "build_pipeline_design.py", "pages/learn/pipeline-design/**/*.html"),
        ("DE Architectures", None, "pages/learn/de-architectures/**/*.html"), # Static or externally built
    ]
    
    for name, builder, pattern in sections:
        rebuild_section(name, builder, pattern)
