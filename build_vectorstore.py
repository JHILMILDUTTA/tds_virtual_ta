# from langchain.schema import Document
# from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# import json
# import os

# # Load your chunks
# with open("processed_chunks.json", "r", encoding="utf-8") as f:
#     processed_chunks = json.load(f)

# # Prepare embeddings
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# # Wrap chunks into Document objects
# documents = [
#     Document(page_content=chunk["text"], metadata=chunk["metadata"])
#     for chunk in processed_chunks
# ]

# # Build vectorstore
# vectorstore = Chroma.from_documents(
#     documents=documents,
#     embedding=embedding_model,  # Use `embedding`, not `embedding_function`
#     persist_directory="./data/chroma_db"
# )
# vectorstore.persist()

# print("Vectorstore created and persisted successfully!")


from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import json
import os
from tqdm import tqdm

def build_vectorstore():
    # 1. Configure Paths
    DATA_DIR = os.path.abspath("TDS-Project1-Data")
    CHUNKS_PATH = os.path.join(DATA_DIR, "processed_chunks.json")  # Updated path
    PERSIST_DIR = os.path.join(DATA_DIR, "chroma_db")
    
    # 2. Initialize Embeddings
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    # 3. Load entire JSON array
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        all_chunks = json.load(f)

    # 4. Process in batches
    batch_size = 100
    documents = []
    
    print("Building vectorstore...")
    for chunk in tqdm(all_chunks):
        documents.append(
            Document(
                page_content=chunk["text"],
                metadata=chunk["metadata"]
            )
        )
        
        if len(documents) >= batch_size:
            Chroma.from_documents(
                documents=documents,
                embedding=embedding_model,
                persist_directory=PERSIST_DIR
            )
            documents.clear()

    # Process remaining documents
    if documents:
        Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=PERSIST_DIR
        )

    print(f"Vectorstore persisted to {PERSIST_DIR}")

if __name__ == "__main__":
    build_vectorstore()
