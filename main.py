import streamlit as st
from app.recommender import hybrid_recommendations, collaborative_recommendations, content_recommendations, get_popular_books
from app.utils import fetch_book_info
from app.data_loader import books_content
from app.logger import logger

st.set_page_config(page_title="📚 BookSage AI", layout="wide")
st.title("📚 Welcome to BookSage AI!")
st.text("Multi-Method Book Recommendation System")
st.text("Made by Md Emon Hasan")

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
        try:
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

            st.subheader(f"{method} Recommendation for: *{selected_book}*")
            cols = st.columns(3)
            for idx, (title, score) in enumerate(recommendations):
                info = fetch_book_info(title, score)
                if info:
                    with cols[idx % 3]:
                        st.image(info['image_url'], width=120)
                        st.markdown(f"**{info['title']}**")
                        st.markdown(f"Author: {info['author']}")
                        st.markdown(f"Year: {info['year']}")
                        st.markdown(f"Publisher: {info['publisher']}")
                        if method != "Popular Books 📚":
                            st.markdown(f"Score: {info['score']:.2f}")
                        st.markdown("---")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"Streamlit error: {str(e)}")
