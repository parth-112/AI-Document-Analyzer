import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from document_processor import process_and_store_pdf
from chat_logic import ask_question

app = FastAPI(title="RAG Document Analyzer API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str


TEMP_DIR = "./temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(TEMP_DIR, file.filename)

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


        chunk_count = process_and_store_pdf(file_path)

        return {
            "message": "Document processed successfully.",
            "filename": file.filename,
            "chunks_created": chunk_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/chat")
async def chat_with_document(request: ChatRequest):

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:

        answer = ask_question(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"status": "API is running. Ready to accept PDFs!"}
