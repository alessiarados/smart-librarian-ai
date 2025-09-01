from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from .chat_bot import SmartLibrarian

app = FastAPI(title="Smart Librarian API", description="AI-powered book recommendation system")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8501"],
    # React and Streamlit ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the chatbot
librarian = SmartLibrarian()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    inappropriate_content: bool
    recommended_books: Optional[List[str]] = None


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(status="healthy", message="Smart Librarian API is running!")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", message="API is operational")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for book recommendations
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        result = librarian.get_book_recommendation(request.message)

        return ChatResponse(
            response=result["response"],
            inappropriate_content=result["inappropriate_content"],
            recommended_books=result.get("recommended_books")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/books")
async def get_all_books():
    """
    Get list of all available books
    """
    try:
        books = librarian.vector_store.get_all_titles()
        return {"books": books}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching books: {str(e)}")


@app.get("/search")
async def search_books(query: str, limit: int = 5):
    """
    Search books by query
    """
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        results = librarian.vector_store.search_books(query, n_results=limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.api:app",
        host=os.getenv("API_HOST", "localhost"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )
