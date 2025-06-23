from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#from services.rag_pipeline import rag_chain, load_vector_store, load_documents
from services.rag_pipeline import rag_chain
from services.vector_store import load_documents
from services.pdf_processor import save_and_process_pdf
from models.schemas import ChatRequest
import os
import re

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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
def list_documents():
    files = os.listdir("data")
    return {"documents": files}

@app.post("/api/chat")
def ask_question(request: ChatRequest):
    result = rag_chain.invoke(request.question)
    raw_answer = result["result"]

    # Simple cleanup rule: remove party placeholders with no values
    cleaned_answer = []
    for line in raw_answer.splitlines():
        if "Party" in line and re.search(r"Party \d\s*$", line):
            continue  # skip lines like "Party 2" with no data
        cleaned_answer.append(line)

    answer_text = "\n".join(cleaned_answer)

    # Show unique sources only
    source_list = list({doc.metadata.get("source", "unknown") for doc in result["source_documents"]})

    return {
        "answer": answer_text.strip(),
        "sources": source_list
    }

