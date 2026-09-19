from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pipeline import run_pipeline

app = FastAPI(title="VerifyMate AI API")

class SourceItem(BaseModel):
    name: str
    text: str

class VerificationRequest(BaseModel):
    sources: List[SourceItem]

@app.get("/")
def home():
    return {"message": "VerifyMate AI API is running!"}

@app.post("/verify")
def verify_sources(request: VerificationRequest):
    try:
        sources_list = [{"name": item.name, "text": item.text} for item in request.sources]
        result = run_pipeline(sources_list)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
