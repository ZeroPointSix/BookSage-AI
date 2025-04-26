# --- Imports ---
import streamlit as st
import pickle
import numpy as np
import os

# --- Set Base Directory ---
# Get the absolute path of the directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Model File Paths ---
cf_model_path = os.path.join(BASE_DIR, 'models', 'cf_model.pkl')
book_pivot_path = os.path.join(BASE_DIR, 'models', 'book_pivot.pkl')
tfidf_path = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.pkl')
content_sim_matrix_path = os.path.join(BASE_DIR, 'models', 'content_sim_matrix.pkl')
title_to_idx_path = os.path.join(BASE_DIR, 'models', 'title_to_idx.pkl')
books_content_path = os.path.join(BASE_DIR, 'models', 'books_content.pkl')
final_rating_path = os.path.join(BASE_DIR, 'models', 'final_rating.pkl')
books_data_path = os.path.join(BASE_DIR, 'models', 'books_data.pkl')

# --- Load Models and Data ---
cf_model = pickle.load(open(cf_model_path, 'rb'))
book_pivot = pickle.load(open(book_pivot_path, 'rb'))
tfidf = pickle.load(open(tfidf_path, 'rb'))
content_sim_matrix = pickle.load(open(content_sim_matrix_path, 'rb'))
title_to_idx = pickle.load(open(title_to_idx_path, 'rb'))
books_content = pickle.load(open(books_content_path, 'rb'))
final_rating = pickle.load(open(final_rating_path, 'rb'))
books = pickle.load(open(books_data_path, 'rb'))

# --- Recommendation Functions ---
def collaborative_recommendations(book_title, top_n=10):
    try:
        if book_title not in book_pivot.index:
            return []
        book_idx = np.where(book_pivot.index == book_title)[0][0]
        distances, indices = cf_model.kneighbors(
            book_pivot.iloc[book_idx, :].values.reshape(1, -1),
            n_neighbors=top_n+1)
        recs = book_pivot.index[indices.flatten()].tolist()
        scores = (1 - distances.flatten()).tolist()
        if book_title in recs:
            idx = recs.index(book_title)
            recs.pop(idx)
            scores.pop(idx)
        return list(zip(recs, scores))
    except Exception:
        return []

def content_recommendations(book_title, top_n=10):
    try:
        if book_title not in title_to_idx:
            return []
        idx = title_to_idx[book_title]
        sim_scores = list(enumerate(content_sim_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        recs = [(books_content['title'].iloc[i[0]], i[1]) for i in sim_scores]
        return recs
    except Exception:
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
        return sorted_recs
    except Exception:
        return []

def fetch_book_info(title, score):
    try:
        info = books_content[books_content['title'] == title]
        if info.empty:
            info = books[books['title'] == title]
            if info.empty:
                return None
        info = info.iloc[0]
        image = info['img_url'] if isinstance(info['img_url'], str) and info['img_url'].startswith("http") else "https://via.placeholder.com/150x220?text=No+Image"
        return {
            'title': info['title'],
            'author': info['author'],
            'year': info['year'],
            'publisher': info['publisher'],
            'image_url': image,
            'score': score
        }
    except Exception:
        return None

def get_popular_books(top_n=10):
    popular = final_rating.groupby('title').count()['rating'].sort_values(ascending=False).head(top_n)
    return popular.index.tolist()

# --- Streamlit UI ---
st.set_page_config(page_title="📚 BookSage AI", layout="wide")
st.title("📚 Welcome to BookSage AI!")
st.text("Multi-Method Book Recommendation System")
st.text("Made by Md Emon Hasan")

# Sidebar Settings
st.sidebar.header("🔧 Settings")
book_list = sorted(books_content['title'].unique())
selected_book = st.sidebar.selectbox("Choose a Book", book_list)

method = st.sidebar.radio("Recommendation Method", ["Hybrid", "Collaborative Filtering", "Content-Based Filtering"])
top_n = st.sidebar.slider("Number of Recommendations", 5, 20, 10)

cf_weight, cb_weight = 0.6, 0.4
if method == "Hybrid":
    cf_weight = st.sidebar.slider("Collaborative Weight", 0.0, 1.0, 0.6)
    cb_weight = st.sidebar.slider("Content-Based Weight", 0.0, 1.0, 0.4)

if st.sidebar.button("🎯 Get Recommendations"):
    with st.spinner("Crunching recommendations..."):
        recommendations = []
        if method == "Hybrid":
            recommendations = hybrid_recommendations(selected_book, cf_weight, cb_weight, top_n)
        elif method == "Collaborative Filtering":
            recommendations = collaborative_recommendations(selected_book, top_n)
        else:
            recommendations = content_recommendations(selected_book, top_n)

        if not recommendations:
            st.warning("No recommendations found! Showing popular books instead. 🎯")
            popular_titles = get_popular_books(top_n)
            recommendations = [(title, 0) for title in popular_titles]

        st.subheader(f"{method} Recommendation for: *{selected_book}*" if recommendations else "Popular Books 📚")
        cols = st.columns(2)
        for idx, (title, score) in enumerate(recommendations):
            info = fetch_book_info(title, score)
            if info:
                with cols[idx % 2]:
                    st.image(info['image_url'], width=120)
                    st.markdown(f"**{info['title']}**")
                    st.markdown(f"Author: {info['author']}")
                    st.markdown(f"Year: {info['year']}")
                    st.markdown(f"Publisher: {info['publisher']}")
                    if method != "Popular Books 📚":
                        st.markdown(f"Score: {info['score']:.2f}")
                    st.markdown("---")
