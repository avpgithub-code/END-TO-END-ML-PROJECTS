"""Main module to orchestrate data ingestion process.
This module initializes the data ingestion configuration,
executes the data ingestion process, and handles exceptions.
"""
import sys
import pandas as pd
from src.myproject.config.config_app import DataIngestionConfig
from src.myproject.components.data_ingestion import DataIngestion
# from src.myproject.components.data_transformation import DataTransformation
import src.myproject.logger as logger
import src.myproject.exception as exception
#------------------------------------------------------------------
# Main function to orchestrate data ingestion
#------------------------------------------------------------------

def main():
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
        data_ingestion.save_ingested_data(raw_df, X, y)
        #----------------------------------------------------------------
        # Split the Dataframe into Training and Testing sets
        # #----------------------------------------------------------------
        (X_train, y_train), (X_val, y_val), (X_test, y_test) = data_ingestion.train_test_split_data(X,y)
        logger.app_logger.info("Data split into training, validation and testing sets successfully.")
        # #----------------------------------------------------------------
        # # Save the training and testing data to their respective paths
        # #----------------------------------------------------------------
        data_ingestion.save_data_splits(X_train, y_train, X_val, y_val, X_test, y_test)
        logger.app_logger.info("Data ingestion process completed successfully.")
    except exception.CustomException as ce:
        logger.app_logger.error("An error occurred during data ingestion: %s", ce)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce

if __name__ == "__main__":
    main()