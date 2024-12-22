from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.generate_note import generate_note

linkedin_router = APIRouter()

class ConnectNoteRequest(BaseModel):
    recipient_name: str
    recipient_headline: str
    recipient_about: str
    purpose: str
    sender_name: str

@linkedin_router.post("/generate_note")
async def generate_connect_note(request: ConnectNoteRequest):
    try:
        # Generate the personalized note
        note = generate_note(request)
        return {"note": note}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating note: {str(e)}")
