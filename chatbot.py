from datetime import datetime
from fastapi import APIRouter,Form
import tempfile
import redis
from RAG_APP.RAG import get_redis_client
from RAG_APP.RAG import llm
from RAG_APP.RAG import prompt_template
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
import os
import tempfile
from RAG_APP.index import register_file,aceess_file,file_exists
start=datetime.now()
"""splitter=RecursiveCharacterTextSplitter(chunk_size=750,chunk_overlap=110)
embeddings=HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
"""
model=Ollama(model="phi3:mini",temperature=0.0,base_url="http://localhost:11434",num_predict=512)
pdf_path=r"C:\Users\madhugoud\Downloads\AI_Shopkeeper_Full_Documentation.pdf"
print(os.path.exists(pdf_path))
prompt_template = """You are a help assistant for a login screen.

Answer only about:
- Login
- Account creation
- App features
- Basic usage

Rules:
- Maximum 3 bullet points.
- No paragraphs.
- No technical terms.
- If unsure, say you don’t know.

Context:
{retrieved_documents}

Question:
{user_query}

Answer:
"""
with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_file:
    with open(pdf_path,"rb") as f:
        content=f.read()
    temp_file.write(content)
    temp_file_path=temp_file.name
file_id="chatbot_data_file"
if not file_exists(file_id):
    register_file(temp_file_path,file_id)
    print("File registered successfully.")
router=APIRouter()
@router.post("/chatbot/")
async def get_answer_from_pdf(query:str):
    cache_key=f"{file_id}:{query}"
    if get_redis_client().exists(cache_key):
        return {"message":get_redis_client().get(cache_key).decode()}
    if not file_exists(file_id):
        register_file(temp_file_path,file_id)
        print("File registered successfully.")
    hybrid_retriver=aceess_file(file_id)
    print("Retriever accessed successfully.")
    docs=hybrid_retriver.get_relevant_documents(query)
    print(f"Number of documents retrieved: {len(docs)}")
    #splitted_docs=splitter.split_documents(docs)
    #print(f"Number of splitted documents: {len(splitted_docs)}")
    context=" ".join([doc.page_content for doc in docs])
    prompt=prompt_template.format(retrieved_documents=context,user_query=query)
    print("Prompt prepared successfully.")
    answer=model.invoke(prompt)
    print("Model invoked successfully.")
    get_redis_client().set(cache_key,answer,ex=3600)
    end=datetime.now()
    print("time taken",end-start)
    return {"message":answer}



