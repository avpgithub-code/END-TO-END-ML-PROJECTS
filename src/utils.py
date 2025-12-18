"""
Utility Functions Module for the Application
This module provides utility functions used across the application,
such as ensuring the existence of directories.
"""
import os
from pathlib import Path
import sys
import pandas as pd
import src.exception as exception #import CustomException
import src.logger as logger
#--------------------------------------------------------------------
# Ensure directory exists function
#--------------------------------------------------------------------
def ensure_directory_exists(directory_path):
    """Checks if a directory exists, and creates it if necessary."""
    path = Path(directory_path)
    if not path.exists():
        # Creates the directory and any necessary parent directories
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")
#--------------------------------------------------------------------
# Function to Read data from file
#--------------------------------------------------------------------
def ingest_data_from_file(raw_data: str):
    """
    Function to ingest data from a given file path.
    Raises CustomException on failure.
    """
    try:
        if not os.path.exists(raw_data):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from FileNotFoundError(f"The file {raw_data} does not exist.")
        with open(raw_data, 'r', encoding='utf-8') as file:
            df = pd.read_csv(file)
            logger.app_logger.info("Data ingested successfully from %s", raw_data)
            return df
    except exception.CustomException as ce:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
