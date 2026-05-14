import os, sys
from rebuild_core import rebuild_section

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(root)
    
    rebuild_section(
        section_name="SQL",
        builder_script="build_sql_guide.py",
        directory_pattern="pages/learn/sql/**/*.html"
    )
