"""
Logger Module for the Application
This module sets up a logger with rotating file handlers to log messages
to a file with a maximum size and backup count.
"""
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from src.myproject.utils  import ensure_directory_exists
import src.myproject.constants as constants
#-----------------------------------------------------------------------------
# Load environment variables for logger configuration
#-----------------------------------------------------------------------------
BASE_DIR = constants.PROJECT_ROOT
LOG_DIR = constants.LOGS_DIR
#-----------------------------------------------------------------------------
LOG_FILE_MAX_BYTES = constants.LOG_FILE_MAX_BYTES
LOG_FILE_BACKUP_COUNT = constants.LOG_FILE_BACKUP_COUNT
#-----------------------------------------------------------------------------
# Print configuration for verification
#-----------------------------------------------------------------------------
print(f"Root Directory: {BASE_DIR}")
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
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.DEBUG)
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
app_logger.addHandler(handler)
app_logger.debug("Logger initialized and ready to log messages.")