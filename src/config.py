"""
Configuration Module for the Application
This module defines configuration parameters used throughout the application.
"""
import os

# Define the directory where logs should be stored
# os.getcwd() gets the current working directory
LOG_DIR = os.path.join(os.getcwd(), 'logs')

# Define the maximum size for a single log file (e.g., 5 MB)
LOG_FILE_MAX_BYTES = 5 * 1024 * 1024 

# Define how many backup log files to keep
LOG_FILE_BACKUP_COUNT = 3 