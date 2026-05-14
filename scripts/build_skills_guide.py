from builder.core import GuideBuilder
import os

def build_skills():
    data_file = os.path.join('data', 'skills_complete_guide.json')
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found.")
        return

    builder = GuideBuilder("skills", "Skills Arena", data_file)
    
    phases = [
        {"name": "Data Mastery", "part_ids": [1]},
        {"name": "Engineering Design", "part_ids": [2]}
    ]
    
    builder.build_hub(phases)
    builder.build_subpages(category_label="Technical Skills")
    print("Successfully built Skills Arena.")

if __name__ == "__main__":
    build_skills()
