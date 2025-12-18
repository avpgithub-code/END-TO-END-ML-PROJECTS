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
from dataclasses import dataclass
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
from src.exception import CustomException
from src.logger import logger
from src.components.data_ingestion_config import DataIngestionConfig,DataIngestion
#------------------------------------------------------------------
# Log module loading
#------------------------------------------------------------------
logger.info("Data Ingestion Module Loaded Successfully. Initiating Data Ingestion Process...")
#------------------------------------------------------------------
# Main execution block for data ingestion
#------------------------------------------------------------------
if __name__ == "__main__":
    try:
        #----------------------------------------------------------------
        # Initialize data ingestion configuration and class
        #----------------------------------------------------------------
        ingestion_config = DataIngestionConfig()
        data_ingestion = DataIngestion(config=ingestion_config)
        #----------------------------------------------------------------
        # Ingest data from file source and load into DataFrame
        #----------------------------------------------------------------
        df = data_ingestion.initiate_data_ingestion_from_file()
        logger.info(f"Raw Data Type: {type(df)}")
        logger.info(f"Dataframe shape: {df.shape}")
        #----------------------------------------------------------------
        # Split the data into Training and Testing sets
        #----------------------------------------------------------------
        train_data, test_data = data_ingestion.train_test_split_data(df)
        logger.info(f"Training Data Shape: {train_data.shape}")
        logger.info(f"Testing Data Shape: {test_data.shape}")
        #----------------------------------------------------------------
        # Save the training and testing data to their respective paths
        #----------------------------------------------------------------
        logger.info("Saving training and testing data to respective paths...")
        train_data,test_data = data_ingestion.save_data_splits(train_data, test_data)
        logger.info("Data ingestion process completed successfully.")
    except CustomException as ce:
        logger.error(f"An error occurred during data ingestion: {ce}")
        
