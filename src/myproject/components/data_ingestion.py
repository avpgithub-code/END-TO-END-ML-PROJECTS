"""
Module for data ingestion functionality.
This module provides functions to ingest data from various sources
and handles exceptions using the CustomException class.
"""
#------------------------------------------------------------------
# Import Modules: Custom Exception and Logger
#------------------------------------------------------------------
import sys
import src.myproject.exception as exception
import src.myproject.logger as logger
from src.myproject.components.data_ingestion_config import DataIngestionConfig,DataIngestion
#------------------------------------------------------------------
# Log module loading
#------------------------------------------------------------------
logger.app_logger.info("Data Ingestion Module Loaded Successfully. Initiating Data Ingestion Process...")
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
        raw_df,X,y = data_ingestion.initiate_data_ingestion_from_file()
        #----------------------------------------------------------------
        # Split the Dataframe into Training and Testing sets
        #----------------------------------------------------------------
        (X_train, y_train), (X_val, y_val), (X_test, y_test) = data_ingestion.train_valid_test_split_data(X,y)
        logger.app_logger.info("Data split into training, validation and testing sets successfully.")
        #----------------------------------------------------------------
        # Save the training and testing data to their respective paths
        #----------------------------------------------------------------
        data_ingestion.save_data_splits(X_train, y_train, X_val, y_val, X_test, y_test)
        logger.app_logger.info("Data ingestion process completed successfully.")
    except exception.CustomException as ce:
        logger.app_logger.error("An error occurred during data ingestion: %s", ce)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
        
