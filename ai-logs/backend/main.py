from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class MeetingRequest(BaseModel):
    transcript: str

@app.post("/generate-summary")
async def generate_summary(request: MeetingRequest):
    # Planner-Reasoner: Extracting insights using Claude 3.5 Sonnet
    prompt = f"Summarize this meeting transcript into TLDR, Action Items, and Key Decisions: {request.transcript}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": os.getenv("ANTHROPIC_API_KEY"), "anthropic-version": "2023-06-01"},
            json={
                "model": "claude-3-5-sonnet-20240620",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        return response.json()
      
