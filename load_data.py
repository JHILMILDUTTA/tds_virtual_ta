import json
import os

# Correct path to your discourse posts file
json_path = os.path.join("TDS-Project1-Data", "discourse_posts.json")

# Load the JSON data
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Print how many posts are loaded
print(f"Loaded {len(data)} posts.")
print("Example post:")
print(data[0])  # print the first post to preview
