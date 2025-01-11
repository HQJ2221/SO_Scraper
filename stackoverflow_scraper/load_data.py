import os
import json


data = []
for root, _, files in os.walk("filtered_files"):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root, file), "r") as f:
                # print(f"Reading file {file}")
                data.extend(json.loads(f.read()))

print(f"Total data: {len(data)}")

with open("all_data.json", 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
