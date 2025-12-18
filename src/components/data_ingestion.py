"""
Module for data ingestion functionality.
This module provides functions to ingest data from various sources
and handles exceptions using the CustomException class.
"""
#------------------------------------------------------------------
# Import Modules: Custom Exception and Logger
#------------------------------------------------------------------
import sys
from src.exception import CustomException
from src.logger import app_logger
from src.components.data_ingestion_config import DataIngestionConfig,DataIngestion
#------------------------------------------------------------------
# Log module loading
#------------------------------------------------------------------
app_logger.info("Data Ingestion Module Loaded Successfully. Initiating Data Ingestion Process...")
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
        # Initite data ingestion from RAW file source and return as DataFrame
        #----------------------------------------------------------------
        df = data_ingestion.initiate_data_ingestion_from_file()
        app_logger.info("Raw Data Type: %s", type(df))
        app_logger.info("Dataframe shape: %s", df.shape)
        #----------------------------------------------------------------
        # Split the Dataframe into Training and Testing sets
        #----------------------------------------------------------------
        train_data, test_data = data_ingestion.train_test_split_data(df)
        app_logger.info("Training Data Shape: %s", train_data.shape)
        app_logger.info("Testing Data Shape: %s", test_data.shape)
        #----------------------------------------------------------------
        # Save the training and testing data to their respective paths
        #----------------------------------------------------------------
        app_logger.info("Saving training and testing data to respective paths...")
        train_data,test_data = data_ingestion.save_data_splits(train_data, test_data)
        app_logger.info("Data ingestion process completed successfully.")
    except CustomException as ce:
        app_logger.error("An error occurred during data ingestion: %s", ce)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise CustomException(exc_type, exc_value, exc_traceback) from ce
        
