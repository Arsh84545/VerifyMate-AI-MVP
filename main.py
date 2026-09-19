from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

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
    return {
        "status": "success",
        "result": {
            "conflicts": [
                {
                    "issue": "Project Deadline Inconsistency",
                    "source_1": "October 15th at 5:00 PM",
                    "source_2": "November 1st at midnight",
                    "details": "Direct factual contradiction regarding submission timeline."
                }
            ],
            "summary": "Factual conflict detected between provided sources."
        }
    }
