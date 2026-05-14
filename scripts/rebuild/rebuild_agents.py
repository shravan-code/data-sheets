import os, sys
from rebuild_core import rebuild_section

if __name__ == "__main__":
    # Ensure we are in the root directory
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(root)
    
    rebuild_section(
        section_name="Agents",
        builder_script="build_agents_guide.py",
        directory_pattern="pages/learn/agents/**/*.html"
    )
