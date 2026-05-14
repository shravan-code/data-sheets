import os, sys
import subprocess

if __name__ == "__main__":
    # Ensure we are in the root directory
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(root)
    
    print("Rebuilding Portfolio Section...")
    r = subprocess.run([sys.executable, "scripts/build_portfolio.py"])
    if r.returncode == 0:
        print("Portfolio pages generated successfully.")
    else:
        print("Error generating portfolio pages.")
