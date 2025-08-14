# ==========================================
# FILE: __init__.py
# ==========================================

"""
Book Recommendation System

A modular recommendation system that provides:
- Collaborative Filtering recommendations
- Content-based recommendations  
- Hybrid recommendations

Usage:
    from recommendation_engine import RecommendationEngine
    
    engine = RecommendationEngine()
    engine.train_models()  # or engine.load_trained_models()
    
    recommendations = engine.get_recommendations("Book Title", method='hybrid')
"""

from .recommendation_engine import RecommendationEngine
from .config import Config

__version__ = "2.0.0"
__all__ = ['RecommendationEngine', 'Config']