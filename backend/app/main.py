"""FastAPI application for the Chinese BookSage demo."""
from contextlib import asynccontextmanager
from typing import Any

import pandas as pd
from fastapi import FastAPI, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import Config
from app.core.logger import logger
from app.services.recommendation_engine import RecommendationEngine

# Global recommendation engine instance
engine: RecommendationEngine | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    global engine

    # Startup: Load models
    logger.info("Starting 书灵 BookSage application...")
    Config.ensure_directories()

    engine = RecommendationEngine()
    if not engine.load_trained_models():
        logger.warning(
            "No pre-trained models found. "
            "Please train models first using the training script."
        )

    yield

    # Shutdown
    logger.info("Shutting down 书灵 BookSage application...")


# Create FastAPI app
app = FastAPI(
    title="书灵 BookSage",
    description="基于协同过滤、内容相似度与混合策略的智能图书推荐系统",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration for development

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/popular", response_class=JSONResponse)
async def get_popular_books() -> list[dict[str, Any]]:
    """Return popular books for the homepage."""
    popular_books = []
    if engine and engine.is_trained:
        popular_books = engine.get_popular_books(limit=10)
    return popular_books


@app.post("/api/recommend", response_class=JSONResponse)
async def recommend(
    book_title: str = Form(...),
    method: str = Form(default="hybrid")
) -> dict[str, Any]:
    """Return book recommendations for a title and method."""
    recommendations: list[dict[str, Any]] = []
    selected_book: dict[str, Any] | None = None

    if engine and engine.is_trained:
        # Get selected book details
        selected_book = engine.get_book_info(book_title)

        # Get recommendations
        recommendations = engine.get_recommendations(
            book_title=book_title,
            method=method,
            top_n=10
        )
        logger.info(
            f"Generated {len(recommendations)} {method} recommendations "
            f"for '{book_title}'"
        )

    return {
        "recommendations": recommendations,
        "book_title": book_title,
        "method": method,
        "selected_book": selected_book
    }


@app.get("/api/search_books", response_class=JSONResponse)
async def search_books(
    query: str = Query(default="")
) -> list[dict[str, Any]]:
    """
    Search for books by title.
    """
    if not query:
        return []

    if not engine or not engine.is_trained:
        logger.warning("Engine not ready for search")
        return []

    query_lower = query.lower()

    # Search in books_content
    books_content = engine.processed_data["books_content"]
    matching_books = books_content[
        books_content["title"].str.lower().str.contains(
            query_lower, na=False
        )
    ]

    # If not enough results, search in books
    if len(matching_books) < 5:
        books = engine.processed_data["books"]
        additional = books[
            books["title"].str.lower().str.contains(query_lower, na=False)
        ]
        matching_books = pd.concat(
            [matching_books, additional]
        ).drop_duplicates("title")

    results = []
    for _, row in matching_books.head(9).iterrows():
        img_url = row["img_url"]
        if not isinstance(img_url, str) or not img_url.startswith("http"):
            img_url = Config.DEFAULT_IMAGE_URL

        results.append({
            "title": row["title"],
            "author": row["author"],
            "image_url": img_url
        })

    logger.debug(f"Search for '{query}' returned {len(results)} results")
    return results


@app.get("/api/health")
async def health_check() -> dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "app_name": "书灵 BookSage",
        "message": "服务运行正常",
        "models_loaded": engine.is_trained if engine else False,
        "version": "2.0.0"
    }


# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True
    )
