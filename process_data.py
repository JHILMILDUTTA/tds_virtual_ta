# import json
# import os
# import re

# # Path to the raw data file
# json_path = os.path.join("TDS-Project1-Data", "discourse_posts.json")

# with open(json_path, "r", encoding="utf-8") as f:
#     raw_posts = json.load(f)

# processed_chunks = []

# for post in raw_posts:
#     content = post.get("content", "")
    
#     # Remove @mentions like @s.anand
#     content = re.sub(r"@\w+", "", content)
    
#     # Combine useful fields
#     title = post.get("topic_title", "")
#     url = post.get("url", "")
#     author = post.get("author", "")
#     # title = title.strip() if title else "No Title"
#     title = post.get("topic_title", "")
#     content = content.strip()
    
#     # Skip empty posts
#     if not content.strip():
#         continue
    
#     # Create one clean chunk per post
#     chunk = {
#     "text": f"{title}\n\n{content.strip()}",
#     "metadata": {
#         "url": url,
#         "author": author,
#         "source": "discourse_posts.json",
#         "title": title if title else "No Title"
#     }
# }


#     processed_chunks.append(chunk)


# print(f"Created {len(processed_chunks)} cleaned chunks.")
# print("Example chunk:")
# print(processed_chunks[0])

# import json

# with open("processed_chunks.json", "w", encoding="utf-8") as f:
#     json.dump(processed_chunks, f, indent=2, ensure_ascii=False)




# # import json
# # import os
# # import re
# # from pathlib import Path

# # # 1. Path Handling - Use absolute paths
# # DATA_DIR = Path(__file__).parent / "TDS-Project1-Data"
# # JSON_PATH = DATA_DIR / "discourse_posts.json"
# # OUTPUT_PATH = DATA_DIR / "processed_chunks.json"

# # # 2. Memory-Efficient Processing
# # def process_posts():
# #     processed_chunks = []
    
# #     with open(JSON_PATH, "r", encoding="utf-8") as f:
# #         for line in f:  # Stream file line-by-line
# #             post = json.loads(line)
# #             content = post.get("content", "")
            
# #             # Improved mention removal (@user123_)
# #             content = re.sub(r"@[\w_]+", "", content).strip()
            
# #             if not content:
# #                 continue
                
# #             # Clean title
# #             title = post.get("topic_title", "").strip() or "No Title"
            
# #             processed_chunks.append({
# #                 "text": f"{title}\n\n{content}",
# #                 "metadata": {
# #                     "url": post.get("url", ""),
# #                     "author": post.get("author", ""),
# #                     "source": JSON_PATH.name,
# #                     "title": title
# #                 }
# #             })
            
# #             # Memory management: Batch processing
# #             if len(processed_chunks) % 1000 == 0:
# #                 yield processed_chunks
# #                 processed_chunks.clear()
    
# #     yield processed_chunks

# # # 3. Write in batches
# # if __name__ == "__main__":
# #     # Create directory if missing
# #     DATA_DIR.mkdir(parents=True, exist_ok=True)
    
# #     with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
# #         f.write('[\n')  # Start JSON array
        
# #         first_chunk = True
# #         for chunk in process_posts():
# #             for entry in chunk:
# #                 if not first_chunk:
# #                     f.write(',\n')
# #                 json.dump(entry, f, ensure_ascii=False)
# #                 first_chunk = False
                
# #         f.write('\n]')  # Close JSON array
    
# #     # print(f"Created {len(processed_chunks)} cleaned chunks")











import json
import os
import re

# --- Configuration ---
DATA_DIR = "TDS-Project1-Data"
INPUT_FILE = os.path.join(DATA_DIR, "discourse_posts.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "processed_chunks.json")

def clean_content(content):
    # Remove @mentions (including underscores and numbers)
    return re.sub(r"@[\w_]+", "", content).strip()

def process_posts(input_path, output_path):
    # Load the entire JSON array (standard format)
    with open(input_path, "r", encoding="utf-8") as f:
        raw_posts = json.load(f)

    processed_chunks = []
    for post in raw_posts:
        content = clean_content(post.get("content", ""))
        title = post.get("topic_title", "").strip() or "No Title"
        url = post.get("url", "")
        author = post.get("author", "")

        # Skip empty posts
        if not content:
            continue

        chunk = {
            "text": f"{title}\n\n{content}",
            "metadata": {
                "url": url,
                "author": author,
                "source": os.path.basename(input_path),
                "title": title
            }
        }
        processed_chunks.append(chunk)

    # Save processed data
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed_chunks, f, indent=2, ensure_ascii=False)

    print(f"Created {len(processed_chunks)} cleaned chunks.")
    print("Example chunk:")
    print(processed_chunks[0])

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    process_posts(INPUT_FILE, OUTPUT_FILE)
