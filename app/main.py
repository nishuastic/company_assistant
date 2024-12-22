from fastapi import FastAPI
from app.routes.linkedin_routes import linkedin_router
from app.routes.value_routes import value_router

app = FastAPI(title="Madkudu AI Assistant")

# Include routes
app.include_router(linkedin_router, prefix="/linkedin", tags=["LinkedIn Generator"])
app.include_router(value_router, prefix="/value", tags=["Value App"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Assistant"}
