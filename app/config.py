import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model Paths
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')
CF_MODEL_PATH = os.path.join(MODELS_DIR, 'cf_model.pkl')
BOOK_PIVOT_PATH = os.path.join(MODELS_DIR, 'book_pivot.pkl')
TFIDF_PATH = os.path.join(MODELS_DIR, 'tfidf_vectorizer.pkl')
CONTENT_SIM_MATRIX_PATH = os.path.join(MODELS_DIR, 'content_sim_matrix.pkl')
TITLE_TO_IDX_PATH = os.path.join(MODELS_DIR, 'title_to_idx.pkl')
BOOKS_CONTENT_PATH = os.path.join(MODELS_DIR, 'books_content.pkl')
FINAL_RATING_PATH = os.path.join(MODELS_DIR, 'final_rating.pkl')
BOOKS_DATA_PATH = os.path.join(MODELS_DIR, 'books_data.pkl')
