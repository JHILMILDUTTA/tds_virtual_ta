import json
import os
import re

# Path to the raw data file
json_path = os.path.join("TDS-Project1-Data", "discourse_posts.json")

with open(json_path, "r", encoding="utf-8") as f:
    raw_posts = json.load(f)

processed_chunks = []

for post in raw_posts:
    content = post.get("content", "")
    
    # Remove @mentions like @s.anand
    content = re.sub(r"@\w+", "", content)
    
    # Combine useful fields
    title = post.get("topic_title", "")
    url = post.get("url", "")
    author = post.get("author", "")
    # title = title.strip() if title else "No Title"
    title = post.get("topic_title", "")
    content = content.strip()
    
    # Skip empty posts
    if not content.strip():
        continue
    
    # Create one clean chunk per post
    chunk = {
    "text": f"{title}\n\n{content.strip()}",
    "metadata": {
        "url": url,
        "author": author,
        "source": "discourse_posts.json",
        "title": title if title else "No Title"
    }
}


    processed_chunks.append(chunk)


print(f"Created {len(processed_chunks)} cleaned chunks.")
print("Example chunk:")
print(processed_chunks[0])

import json

with open("processed_chunks.json", "w", encoding="utf-8") as f:
    json.dump(processed_chunks, f, indent=2, ensure_ascii=False)


