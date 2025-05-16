import pickle
from src.config import *
from src.logger import logger

def load_pickle(path):
    try:
        with open(path, 'rb') as f:
            data = pickle.load(f)
        logger.info(f"Loaded model/data from {path}")
        return data
    except Exception as e:
        logger.error(f"Error loading {path}: {str(e)}")
        return None

cf_model = load_pickle(CF_MODEL_PATH)
book_pivot = load_pickle(BOOK_PIVOT_PATH)
tfidf = load_pickle(TFIDF_PATH)
content_sim_matrix = load_pickle(CONTENT_SIM_MATRIX_PATH)
title_to_idx = load_pickle(TITLE_TO_IDX_PATH)
books_content = load_pickle(BOOKS_CONTENT_PATH)
final_rating = load_pickle(FINAL_RATING_PATH)
books = load_pickle(BOOKS_DATA_PATH)
