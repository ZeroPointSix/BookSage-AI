from app.data_loader import books_content, books
from app.logger import logger

def fetch_book_info(title, score):
    try:
        info = books_content[books_content['title'] == title]
        if info.empty:
            info = books[books['title'] == title]
            if info.empty:
                logger.warning(f"No info found for book: {title}")
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
    except Exception as e:
        logger.error(f"Error fetching book info: {str(e)}")
        return None
