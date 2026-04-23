import json
import os

def generate_html_content(t):
    html = []
    
    # Handle standard subtopics
    if 'subtopics' in t:
        for sub in t.get('subtopics', []):
            html.append(f"<h2>{sub['name']}</h2>")
            html.append("<br>")
            html.append(f"<p>{sub['explanation']}</p>")
            html.append("<br>")
            
            for ex in sub.get('examples', []):
                if ex.get('title'):
                    html.append(f"<h3>{ex['title']}</h3>")
                
                code = ex['code'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                # Determine language - usually bash
                lang = 'bash'
                if 'python' in code.lower() and 'import' in code.lower():
                    lang = 'python'
                elif 'yaml' in code.lower() and ':' in code:
                    lang = 'yaml'
                    
                html.append(f'<pre><code class="language-{lang}">\n{code}\n</code></pre>')
                html.append("<br>")
            
            html.append("<hr>")
            html.append("<br>")
            
    # Handle projects
    if 'projects' in t:
        for proj in t.get('projects', []):
            html.append(f"<h2>{proj['name']}</h2>")
            html.append("<br>")
            html.append(f"<p>{proj['description']}</p>")
            html.append("<br>")
            
            code = proj['code'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html.append(f'<pre><code class="language-bash">\n{code}\n</code></pre>')
            html.append("<br>")
            html.append("<hr>")
            html.append("<br>")

    # Handle cheatsheet
    if 'categories' in t:
        for cat in t.get('categories', []):
            html.append(f"<h2>{cat['category']}</h2>")
            html.append("<br>")
            html.append('<div class="overflow-x-auto my-6">')
            html.append('<table class="min-w-full border-collapse border border-slate-200 dark:border-slate-800 text-sm">')
            html.append('<thead class="bg-slate-100 dark:bg-slate-800/50">')
            html.append('<tr>')
            html.append('<th class="border border-slate-200 dark:border-slate-800 p-3 text-left font-bold">Task</th>')
            html.append('<th class="border border-slate-200 dark:border-slate-800 p-3 text-left font-bold">Bash</th>')
            html.append('<th class="border border-slate-200 dark:border-slate-800 p-3 text-left font-bold text-blue-500">PowerShell</th>')
            html.append('</tr>')
            html.append('</thead>')
            html.append('<tbody>')
            
            for comp in cat.get('comparisons', []):
                html.append('<tr class="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">')
                html.append(f'<td class="border border-slate-200 dark:border-slate-800 p-3 font-medium">{comp["task"]}</td>')
                html.append(f'<td class="border border-slate-200 dark:border-slate-800 p-3"><code>{comp["bash"]}</code></td>')
                html.append(f'<td class="border border-slate-200 dark:border-slate-800 p-3 text-blue-500/80"><code>{comp["powershell"]}</code></td>')
                html.append('</tr>')
                
            html.append('</tbody>')
            html.append('</table>')
            html.append('</div>')
            html.append("<br>")
    
    return "\n".join(html)

def main():
    with open('bash_guide.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    topics = data.get('topics', [])
    
    icons = [
        "terminal", "variable", "type", "hard-drive", "calculator", "git-branch",
        "command", "scissors", "folder", "cpu", "alert-circle", "search",
        "bug", "zap", "check-circle", "folder-kanban", "layout"
    ]
    
    subpages_list = []
    for i, t in enumerate(topics):
        topic_name = t['topic']
        topic_id = topic_name.lower().replace(" & ", "-").replace(" ", "-")
        
        content = generate_html_content(t)
        
        # Get description
        if 'description' in t:
            desc = t['description']
        elif 'subtopics' in t and len(t['subtopics']) > 0:
            desc = t['subtopics'][0]['explanation'][:120] + "..." if len(t['subtopics'][0]['explanation']) > 120 else t['subtopics'][0]['explanation']
        elif 'projects' in t and len(t['projects']) > 0:
            desc = t['projects'][0]['description'][:120] + "..." if len(t['projects'][0]['description']) > 120 else t['projects'][0]['description']
        else:
            desc = "Comprehensive guide on " + topic_name
            
        subpages_list.append({
            "id": topic_id,
            "title": f"{i+1}. {topic_name}",
            "icon": icons[i] if i < len(icons) else "terminal",
            "description": desc,
            "content": content
        })

    with open('bash_subpages_data.json', 'w', encoding='utf-8') as f:
        json.dump(subpages_list, f, indent=4)
    
    print(f"Successfully processed {len(subpages_list)} topics into bash_subpages_data.json")

if __name__ == "__main__":
    main()
