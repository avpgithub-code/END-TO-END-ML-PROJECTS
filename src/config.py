"""
Configuration Module for the Application
This module defines configuration parameters used throughout the application.
"""
import os
#-----------------------------------------------------------------------------------------
# Define the directory where logs should be stored, maxium size, how many backup log files
LOG_DIR = os.path.join(os.getcwd(), 'logs')
LOG_FILE_MAX_BYTES = 5 * 1024 * 1024 
LOG_FILE_BACKUP_COUNT = 3 
#------------------------------------------------------------------------------------------
