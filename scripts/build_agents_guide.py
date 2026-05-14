from builder.core import GuideBuilder
import os

def build_agents():
    data_file = os.path.join('data', 'agents_complete_guide.json')
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found.")
        return

    builder = GuideBuilder("agents", "Agents Mastery", data_file)
    
    phases = [
        {"name": "Foundations", "part_ids": [1]},
        {"name": "Architectures", "part_ids": [2]}
    ]
    
    builder.build_hub(phases)
    builder.build_subpages(category_label="AI Agents")
    print("Successfully built Agents Mastery.")

if __name__ == "__main__":
    build_agents()
