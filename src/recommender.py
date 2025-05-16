import numpy as np
from src.data_loader import cf_model, book_pivot, title_to_idx, content_sim_matrix, books_content, final_rating, books
from src.logger import logger

def collaborative_recommendations(book_title, top_n=10):
    try:
        if book_title not in book_pivot.index:
            logger.warning(f"{book_title} not found in pivot table.")
            return []
        book_idx = np.where(book_pivot.index == book_title)[0][0]
        distances, indices = cf_model.kneighbors(book_pivot.iloc[book_idx, :].values.reshape(1, -1), n_neighbors=top_n+1)
        recs = book_pivot.index[indices.flatten()].tolist()
        scores = (1 - distances.flatten()).tolist()
        if book_title in recs:
            idx = recs.index(book_title)
            recs.pop(idx)
            scores.pop(idx)
        logger.info(f"Collaborative recommendations generated for: {book_title}")
        return list(zip(recs, scores))
    except Exception as e:
        logger.error(f"Error in collaborative recommendations: {str(e)}")
        return []

def content_recommendations(book_title, top_n=10):
    try:
        if book_title not in title_to_idx:
            logger.warning(f"{book_title} not found in title_to_idx.")
            return []
        idx = title_to_idx[book_title]
        sim_scores = list(enumerate(content_sim_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        recs = [(books_content['title'].iloc[i[0]], i[1]) for i in sim_scores]
        logger.info(f"Content-based recommendations generated for: {book_title}")
        return recs
    except Exception as e:
        logger.error(f"Error in content recommendations: {str(e)}")
        return []

def hybrid_recommendations(book_title, cf_weight=0.6, cb_weight=0.4, top_n=10):
    try:
        cf_recs = collaborative_recommendations(book_title, top_n)
        cb_recs = content_recommendations(book_title, top_n)

        combined_scores = {}
        for rec, score in cf_recs:
            combined_scores[rec] = score * cf_weight
        for rec, score in cb_recs:
            if rec in combined_scores:
                combined_scores[rec] += score * cb_weight
            else:
                combined_scores[rec] = score * cb_weight

        sorted_recs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        logger.info(f"Hybrid recommendations generated for: {book_title}")
        return sorted_recs
    except Exception as e:
        logger.error(f"Error in hybrid recommendations: {str(e)}")
        return []

def get_popular_books(top_n=10):
    try:
        popular = final_rating.groupby('title').count()['rating'].sort_values(ascending=False).head(top_n)
        logger.info("Popular books fetched.")
        return popular.index.tolist()
    except Exception as e:
        logger.error(f"Error fetching popular books: {str(e)}")
        return []
