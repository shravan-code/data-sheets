import os
import glob
import urllib.parse
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        if tag in ['a', 'link', 'script', 'img']:
            link_attr = 'href' if tag in ['a', 'link'] else 'src'
            for attr, value in attrs:
                if attr == link_attr and value:
                    self.links.append((tag, link_attr, value))
        for attr, value in attrs:
            if attr == 'id' and value:
                self.ids.append(value)

def check_links():
    root_dir = os.path.abspath('d:\\shra1\\github\\data-sheets')
    html_files = glob.glob(os.path.join(root_dir, '**/*.html'), recursive=True)
    
    # Pre-parse all files to get their IDs
    file_ids = {}
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            parser = LinkParser()
            parser.feed(content)
            file_ids[os.path.abspath(file_path)] = set(parser.ids)
        except Exception:
            pass

    broken_links = []
    
    for file_path in html_files:
        abs_file_path = os.path.abspath(file_path)
        dir_name = os.path.dirname(abs_file_path)
        
        try:
            with open(abs_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            continue
            
        parser = LinkParser()
        parser.feed(content)
        
        for tag, attr, href in parser.links:
            # Skip mailto, tel, and external links
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:')):
                continue
                
            parsed_href = urllib.parse.urlparse(href)
            target_path = parsed_href.path
            fragment = parsed_href.fragment
            
            target_abs_path = abs_file_path
            if target_path:
                if target_path.startswith('/'):
                    if target_path.startswith('/data-sheets/'):
                        target_abs_path = os.path.join(root_dir, target_path.replace('/data-sheets/', '', 1))
                    else:
                        target_abs_path = os.path.join(root_dir, target_path.lstrip('/'))
                else:
                    target_abs_path = os.path.normpath(os.path.join(dir_name, urllib.parse.unquote(target_path)))
            
            if not os.path.exists(target_abs_path):
                broken_links.append({
                    'source': file_path,
                    'tag': tag,
                    'attr': attr,
                    'href': href,
                    'issue': f'File not found: {target_abs_path}'
                })
            elif fragment:
                # Check if the fragment exists in the target file
                if target_abs_path in file_ids:
                    if fragment not in file_ids[target_abs_path]:
                        broken_links.append({
                            'source': file_path,
                            'tag': tag,
                            'attr': attr,
                            'href': href,
                            'issue': f'Fragment #{fragment} not found in {target_abs_path}'
                        })
                
    if broken_links:
        print(f"Found {len(broken_links)} broken links:")
        for link in broken_links:
            print(f"Source: {link['source']}")
            print(f"  Tag: <{link['tag']} {link['attr']}=\"{link['href']}\">")
            print(f"  Issue: {link['issue']}")
            print()
    else:
        print("All local links are working perfectly (including anchors)!")

if __name__ == '__main__':
    check_links()
