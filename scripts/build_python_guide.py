from builder.core import GuideBuilder, slugify, render_topic_content, get_global_sidebar
import os
import json

def build_python():
    data_file = os.path.join('data', 'python_complete_guide.json')
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found.")
        return

    builder = GuideBuilder("python", "Python Mastery", data_file)
    
    # Phase mapping (11 phases)
    phases = [
        {"name": "Foundations", "part_ids": [1]},
        {"name": "Control & Iteration", "part_ids": [2]},
        {"name": "Data Structures", "part_ids": [3]},
        {"name": "Functional Programming", "part_ids": [4]},
        {"name": "Object-Oriented Design", "part_ids": [5]},
        {"name": "Robustness & Iterators", "part_ids": [6, 7]},
        {"name": "Type System & Internal Tools", "part_ids": [8, 9]},
        {"name": "System & File Ops", "part_ids": [10, 11]},
        {"name": "Performance & Concurrency", "part_ids": [12, 15]},
        {"name": "Internals & Architecture", "part_ids": [13, 16]},
        {"name": "Testing & Real-World", "part_ids": [14, 17, 18]}
    ]
    
    builder.build_hub(phases)
    builder.build_subpages(category_label="Programming")

if __name__ == "__main__":
    build_python()
