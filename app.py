from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import requests
import os
from langchain_huggingface import HuggingFaceEmbeddings  

# import os, zipfile

# DB_ZIP = "data/chroma_db.zip"
# DB_DIR = "data/chroma_db"

# if not os.path.exists(DB_DIR):
#     print("Unzipping chroma DB...")
#     with zipfile.ZipFile(DB_ZIP, 'r') as zip_ref:
#         zip_ref.extractall("data")
#     print("✅ Unzipped chroma DB.")





# Load environment variables
load_dotenv()
API_KEY = os.getenv("AIPROXY_TOKEN")

if not API_KEY:
    raise ValueError("API key not found! Set AI_PROXY_API_KEY in .env")

# Initialize FastAPI app
app = FastAPI()

# Load Chroma DB
DB_DIR = "data/chroma_db"
# embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")

# embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")

vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embedding_function)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2 })


# Input model for the /ask endpoint
class QuestionRequest(BaseModel):
    question: str




@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question

    # Retrieve relevant documents
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Build messages for the chat model
    messages = [
        {"role": "system", "content": "You are a helpful virtual TA. Answer based only on the provided context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
    ]

    # Call AI Proxy
    response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.5,
            "max_tokens": 500
        }
    )

    if not response.ok:
        return {"error": response.text}

    res_json = response.json()
    answer = res_json["choices"][0]["message"]["content"]
    # return {"answer": answer}
    answer = res_json["choices"][0]["message"]["content"].strip()

    # Step 4: Extract links from document metadata
    links = []
    for doc in docs:
        url = doc.metadata.get("url", "")
        snippet = doc.page_content.strip().split("\n")[0]  # First line as preview
        if url:
            links.append({
                "url": url,
                "text": snippet
            })

    return {"answer": answer, "links": links}
    # return answer

# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 10000))  # Render sets $PORT
#     uvicorn.run("app:app", host="0.0.0.0", port=port)


# if __name__ == "__main__":
#     import os
#     import uvicorn

#     port = int(os.environ.get("PORT", 10000))  # Default for local dev
#     uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)


# @app.get("/")
# def home():
#     return {"message": "TDS Virtual TA is running!"}




# @app.post("/ask")
# def ask_question(request: QuestionRequest):
#     return {"answer": "Project 1 is due on Saturday", "links": []}




















# @app.post("/ask")
# def ask_question(request: QuestionRequest):
#     question = request.question

#     # Retrieve relevant documents
#     docs = retriever.get_relevant_documents(question)
#     context = "\n\n".join(doc.page_content for doc in docs)

#     # Build messages for the chat model
#     messages = [
#         {"role": "system", "content": "You are a helpful virtual TA. Answer based only on the provided context."},
#         {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
#     ]

#     # Call AI Proxy
#     response = requests.post(
#         "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {API_KEY}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "gpt-4o-mini",
#             "messages": messages,
#             "temperature": 0.5,
#             "max_tokens": 500
#         }
#     )

#     if not response.ok:
#         return {"error": response.text}

#     res_json = response.json()
#     answer = res_json["choices"][0]["message"]["content"]
#     # return {"answer": answer}
#     answer = res_json["choices"][0]["message"]["content"].strip()

#     # Step 4: Extract links from document metadata
#     links = []
#     for doc in docs:
#         url = doc.metadata.get("url", "")
#         snippet = doc.page_content.strip().split("\n")[0]  # First line as preview
#         if url:
#             links.append({
#                 "url": url,
#                 "text": snippet
#             })

#     return {"answer": answer , "links": links} 



# @app.post("/ask")
# def ask_question(request: QuestionRequest):
#     question = request.question

#     # Retrieve relevant documents
#     docs = retriever.get_relevant_documents(question)
#     context = "\n\n".join(doc.page_content for doc in docs)

#     # Build messages
#     messages = [
#         {"role": "system", "content": "You are a helpful virtual TA. Answer based only on the provided context."},
#         {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
#     ]

#     # Call AI proxy
#     response = requests.post(
#         "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {API_KEY}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "gpt-4o-mini",
#             "messages": messages,
#             "temperature": 0.5,
#             "max_tokens": 500
#         }
#     )

#     if not response.ok:
#         return response.text

#     res_json = response.json()
#     answer = res_json["choices"][0]["message"]["content"].strip()

#     # ✅ Only return plain answer as string
#     return answer
