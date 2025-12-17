"""
Logger Module for the Application
This module sets up a logger with rotating file handlers to log messages
to a file with a maximum size and backup count.
"""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from datetime import datetime
# from src.config import LOG_DIR, LOG_FILE_MAX_BYTES, LOG_FILE_BACKUP_COUNT
from src.utils import ensure_directory_exists
#-----------------------------------------------------------------------------
load_dotenv()
# If .env has LOG_FILE_PATH="./logs/app.log"
# Resolve it based on the directory of the current Python file
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = (BASE_DIR / os.getenv("LOG_DIR")).resolve()
LOG_FILE_MAX_BYTES = int(os.getenv("LOG_FILE_MAX_BYTES", 5242880))
LOG_FILE_BACKUP_COUNT = int(os.getenv("LOG_FILE_BACKUP_COUNT", 3))
print(f"Log Directory: {LOG_DIR}")
print(f"LOG_FILE_MAX_BYTES: {LOG_FILE_MAX_BYTES}")
print(f"LOG_FILE_BACKUP_COUNT: {LOG_FILE_BACKUP_COUNT}")
#------------------------------------------------------------------------------
# Create log directory if it doesn't exist and define log filename
#------------------------------------------------------------------------------
ensure_directory_exists(LOG_DIR)
log_filename = os.path.join(LOG_DIR, f"app_log_{datetime.now().strftime('%Y%m%d')}.log")
print(f"Log filename: {log_filename}")
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
    logger.info("This is a test log message from logger.py")
    logger.error("This is a test error message from logger.py")
    logger.debug("This is a test debug message from logger.py")
    logger.warning("This is a test warning message from logger.py")
    