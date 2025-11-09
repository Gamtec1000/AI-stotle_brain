# backend/api/main.py
"""
AI-stotle FastAPI Backend
Serves AI-stotle to your website
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.aristotle_brain import AristotleBrain
from knowledge.embedding_engine import LocalEmbeddingEngine

# Initialize FastAPI
app = FastAPI(
    title="AI-stotle API",
    description="The wise AI science tutor for Carls Newton",
    version="1.0.0"
)

# CORS - Allow your website to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://carlsnewton.com",
        "https://www.carlsnewton.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI-stotle
aristotle = AristotleBrain()
knowledge_engine = LocalEmbeddingEngine()

# Request/Response Models
class QuestionRequest(BaseModel):
    question: str
    student_age: Optional[int] = 10
    context: Optional[dict] = None
    use_knowledge_base: Optional[bool] = True

class QuestionResponse(BaseModel):
    answer: str
    success: bool
    cost: Optional[float] = None
    tokens_used: Optional[int] = None
    sources: Optional[List[dict]] = None

# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "AI-stotle",
        "version": "1.0.0",
        "philosophy": "Wonder is the beginning of wisdom"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    stats = knowledge_engine.get_stats()

    return {
        "status": "healthy",
        "aristotle": "ready",
        "knowledge_base": stats,
        "model": "deepseek-chat",
        "embeddings": "local (free)"
    }

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask AI-stotle a question

    This is the main endpoint your website will call
    """

    try:
        # Search knowledge base if requested
        relevant_knowledge = None
        sources = None

        if request.use_knowledge_base:
            # Search experiments
            exp_results = knowledge_engine.search(
                request.question,
                collection="experiments",
                n_results=2
            )

            # Search Q&A
            qa_results = knowledge_engine.search(
                request.question,
                collection="qa",
                n_results=2
            )

            relevant_knowledge = (
                exp_results['documents'][0] +
                qa_results['documents'][0]
            )

            sources = (
                exp_results['metadatas'][0] +
                qa_results['metadatas'][0]
            )

        # Get answer from AI-stotle
        response = aristotle.ask_aristotle(
            question=request.question,
            student_age=request.student_age,
            context=request.context,
            knowledge=relevant_knowledge
        )

        if response['success']:
            return QuestionResponse(
                answer=response['answer'],
                success=True,
                cost=response.get('cost'),
                tokens_used=response.get('tokens_used'),
                sources=sources
            )
        else:
            raise HTTPException(status_code=500, detail=response.get('error'))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/experiments/search")
async def search_experiments(query: str, limit: int = 5):
    """Search experiments"""

    results = knowledge_engine.search(
        query,
        collection="experiments",
        n_results=limit
    )

    return {
        "results": [
            {
                "name": meta['name'],
                "category": meta['category'],
                "age_range": f"{meta['age_min']}-{meta['age_max']}",
                "wow_factor": meta['wow_factor']
            }
            for meta in results['metadatas'][0]
        ]
    }

@app.get("/stats")
async def get_stats():
    """Get usage statistics"""

    stats = knowledge_engine.get_stats()

    return {
        "knowledge_base": stats,
        "model": "deepseek-chat",
        "cost_per_1k_questions": "$0.50",
        "vs_gpt4": "$10 (95% savings!)"
    }

@app.get("/meta.json")
async def get_meta():
    """API metadata and capabilities"""

    stats = knowledge_engine.get_stats()

    return {
        "api": {
            "title": "AI-stotle API",
            "version": "1.0.0",
            "description": "The wise AI science tutor for Carls Newton",
            "philosophy": "Wonder is the beginning of wisdom"
        },
        "endpoints": [
            {
                "path": "/",
                "method": "GET",
                "description": "Health check"
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Detailed health check with system stats"
            },
            {
                "path": "/ask",
                "method": "POST",
                "description": "Ask AI-stotle a question",
                "parameters": {
                    "question": "string (required)",
                    "student_age": "int (optional, default: 10)",
                    "context": "dict (optional)",
                    "use_knowledge_base": "bool (optional, default: true)"
                }
            },
            {
                "path": "/experiments/search",
                "method": "GET",
                "description": "Search knowledge base experiments",
                "parameters": {
                    "query": "string (required)",
                    "limit": "int (optional, default: 5)"
                }
            },
            {
                "path": "/stats",
                "method": "GET",
                "description": "Get usage statistics and cost information"
            },
            {
                "path": "/meta.json",
                "method": "GET",
                "description": "API metadata and capabilities (this endpoint)"
            }
        ],
        "capabilities": {
            "ai_provider": aristotle.provider,
            "model": aristotle.model_name,
            "temperature": aristotle.temperature,
            "knowledge_base": {
                "enabled": True,
                "vector_db": stats.get("vector_db", "ChromaDB"),
                "total_experiments": stats.get("total_experiments", 0),
                "total_qa_pairs": stats.get("total_qa_pairs", 0),
                "total_concepts": stats.get("total_concepts", 0),
                "total_passages": stats.get("total_passages", 0),
                "collections": stats.get("collections", ["experiments", "qa_pairs", "concepts"]),
                "embedding_model": stats.get("embedding_model", "all-mpnet-base-v2"),
                "embedding_dimension": stats.get("embedding_dimension", 768),
                "total_cost": stats.get("total_cost", "$0 (all local!)")
            },
            "rag_enabled": True,
            "cors_enabled": True
        },
        "status": "online",
        "documentation": "/docs"
    }

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🏛️ AI-STOTLE API SERVER")
    print("="*60)
    print("\n🚀 Starting server...")
    print("📍 http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )