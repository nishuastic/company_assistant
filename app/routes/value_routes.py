from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.utils.value_utils import process_value_app_logic, create_langchain_context, query_vectorstore

value_router = APIRouter()

# Request model for the chat endpoint
class ChatRequest(BaseModel):
    base_url: str
    query: str

# Store vectorstore in memory for reuse
vectorstore_cache = {}

@value_router.get("/analyze")
async def analyze_competitor(base_url: str):
    try:
        results = process_value_app_logic(base_url)
        # Create and cache vectorstore for querying
        vectorstore = create_langchain_context(results)
        vectorstore_cache[base_url] = vectorstore
        return {"base_url": base_url, "filtered_content": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@value_router.post("/chat")
async def chat_with_vectorstore(request: ChatRequest):
    try:
        if request.base_url not in vectorstore_cache:
            raise HTTPException(status_code=404, detail="No vectorstore available for the given base URL.")
        
        vectorstore = vectorstore_cache[request.base_url]
        response = query_vectorstore(vectorstore, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
