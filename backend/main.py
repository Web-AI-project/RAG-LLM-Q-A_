from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.rag_pipeline import rag_chain, load_vector_store, load_documents
from services.pdf_processor import save_and_process_pdf
from models.schemas import ChatRequest
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        filepath = await save_and_process_pdf(file)
        load_documents()
        return {"filename": file.filename, "status": "processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
def list_documents():
    files = os.listdir("data")
    return {"documents": files}

@app.post("/api/chat")
def ask_question(request: ChatRequest):
    result = rag_chain.invoke(request.question)
    return {
        "answer": result["result"],
        "sources": [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
    }
