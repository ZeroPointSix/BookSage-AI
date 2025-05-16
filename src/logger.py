import logging
import os
from datetime import datetime

# Create logs directory if not exists
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Log filename with date
log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
log_filepath = os.path.join(LOG_DIR, log_filename)

# Logger Setup
logger = logging.getLogger("BookSageAI_Logger")
logger.setLevel(logging.DEBUG)

# Handlers
file_handler = logging.FileHandler(log_filepath)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add Handlers
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
