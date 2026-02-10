"""FastAPI application for BookSage-AI."""
from contextlib import asynccontextmanager
from typing import Any

import pandas as pd
from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
    logger.info("Starting BookSage-AI application...")
    Config.ensure_directories()

    engine = RecommendationEngine()
    if not engine.load_trained_models():
        logger.warning(
            "No pre-trained models found. "
            "Please train models first using the training script."
        )

    yield

    # Shutdown
    logger.info("Shutting down BookSage-AI application...")


# Create FastAPI app
app = FastAPI(
    title="BookSage-AI",
    description="AI-powered book recommendation system",
    version="2.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=str(Config.STATIC_DIR)),
    name="static"
)

# Setup Jinja2 templates
templates = Jinja2Templates(directory=str(Config.TEMPLATES_DIR))


def url_for_static(path: str) -> str:
    """Generate URL for static files."""
    return f"/static/{path}"


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    search_term: str = Query(default="")
) -> HTMLResponse:
    """
    Render homepage with popular books.

    Args:
        request: FastAPI request object
        search_term: Optional search term to preserve

    Returns:
        HTML response with rendered template
    """
    popular_books = []
    if engine and engine.is_trained:
        popular_books = engine.get_popular_books(limit=10)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "popular_books": popular_books,
            "search_term": search_term,
            "url_for": lambda name, **kwargs: (
                url_for_static(kwargs.get("filename", ""))
                if name == "static" else ""
            )
        }
    )


@app.post("/recommend", response_class=HTMLResponse)
async def recommend(
    request: Request,
    book_title: str = Form(...),
    method: str = Form(default="hybrid")
) -> HTMLResponse:
    """
    Get book recommendations and render results page.

    Args:
        request: FastAPI request object
        book_title: Title of the book to get recommendations for
        method: Recommendation method ('hybrid', 'collaborative', 'content')

    Returns:
        HTML response with recommendations
    """
    recommendations: list[dict[str, Any]] = []
    selected_book: dict[str, Any] | None = None

    if engine and engine.is_trained:
        # Get selected book details
        selected_book = engine.get_book_info(book_title)

        # Get recommendations
        recommendations = engine.get_recommendations(
            book_title=book_title,
            method=method,
            top_n=9
        )
        logger.info(
            f"Generated {len(recommendations)} {method} recommendations "
            f"for '{book_title}'"
        )

    return templates.TemplateResponse(
        "recommendations.html",
        {
            "request": request,
            "recommendations": recommendations,
            "book_title": book_title,
            "method": method,
            "selected_book": selected_book,
            "url_for": lambda name, **kwargs: (
                url_for_static(kwargs.get("filename", ""))
                if name == "static" else ""
            )
        }
    )


@app.get("/search_books", response_class=JSONResponse)
async def search_books(
    query: str = Query(default="")
) -> list[dict[str, Any]]:
    """
    Search for books by title.

    Args:
        query: Search query string

    Returns:
        JSON response with matching books
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
