"""
Utility Functions Module for the Application
This module provides utility functions used across the application,
such as ensuring the existence of directories.
"""
import os
from pathlib import Path
import sys
#--------------------------------------------------------------------
# Ensure directory exists function
#--------------------------------------------------------------------
def ensure_directory_exists(directory_path):
    """Checks if a directory exists, and creates it if necessary."""
    if not os.path.exists(directory_path):
        # Creates the directory and any necessary parent directories
        os.makedirs(directory_path, exist_ok=True)
        print(f"Created directory: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")
#--------------------------------------------------------------------
# Function to Read data from file
#--------------------------------------------------------------------
def ingest_data_from_file(file_path: str):
    """
    Function to ingest data from a given file path.
    Raises CustomException on failure.
    """
    from src.exception import CustomException
    from src.logger import logger
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r') as file:
            data = file.read()
            logger.info(f"Data ingested successfully from {file_path}")
            return data
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise CustomException(exc_type, exc_value, exc_traceback) from e