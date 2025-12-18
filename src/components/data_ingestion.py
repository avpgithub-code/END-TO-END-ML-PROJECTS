"""
Module for data ingestion functionality.
This module provides functions to ingest data from various sources
and handles exceptions using the CustomException class.
"""
#------------------------------------------------------------------
# Import necessary modules
#------------------------------------------------------------------
import os, sys
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
from src.exception import CustomException
from src.logger import logger
from src.utils import ensure_directory_exists,ingest_data_from_file
from src.components.data_ingestion_config \
    import DataIngestionConfig,DataIngestion,RAW_DATA,TRAIN_DATA,TEST_DATA


#------------------------------------------------------------------
# Example usage
if __name__ == "__main__":
    try:
        ingestion_config = DataIngestionConfig()
        data_ingestion = DataIngestion(config=ingestion_config)
        data = data_ingestion.initiate_data_ingestion_from_file()
        logger.info(f"Data Read Sucessfully") 
    except CustomException as ce:
        logger.error(f"An error occurred during data ingestion: {ce}")
        
