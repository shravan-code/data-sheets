import os
import re

def fix_lucide():
    old_script = 'https://unpkg.com/lucide@0.395.0'
    new_script = 'https://unpkg.com/lucide@0.395.0'
    
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.html', '.py', '.js')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if old_script in content:
                        new_content = content.replace(old_script, new_script)
                        # Also fix the missing 'dataset' icon name while we are at it
                        new_content = new_content.replace('data-lucide="database"', 'data-lucide="database"')
                        
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                        print(f"Fixed: {path}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")
    
    print(f"\nDone! Updated {count} files.")

if __name__ == "__main__":
    fix_lucide()
