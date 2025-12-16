import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from src.config import LOG_DIR, LOG_FILE_MAX_BYTES, LOG_FILE_BACKUP_COUNT
from src.utils import ensure_directory_exists
#------------------------------------------------------------------------------
# Create log directory if it doesn't exist and define log filename
#------------------------------------------------------------------------------
ensure_directory_exists(LOG_DIR)
log_filename = os.path.join(LOG_DIR, f"app_log_{datetime.now().strftime('%Y%m%d')}.log")
#------------------------------------------------------------------------------
# Create a logger and a rotating file handler and a formatter
#------------------------------------------------------------------------------
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    log_filename, 
    maxBytes=LOG_FILE_MAX_BYTES, 
    backupCount=LOG_FILE_BACKUP_COUNT
)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#------------------------------------------------------------------------------
# Add the handler to the logger and log an initialization message
#------------------------------------------------------------------------------
logger.addHandler(handler)
logger.debug("Logger initialized and ready to log messages.")

if __name__ == "__main__":
    logger.info("This is an info message for testing purposes.")
    logger.warning("This is a warning message for testing purposes.")
    logger.error("This is an error message for testing purposes.")
