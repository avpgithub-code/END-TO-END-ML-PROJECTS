"""
Module for data ingestion functionality.
This module provides functions to ingest data from various sources
and handles exceptions using the CustomException class.
"""
#------------------------------------------------------------------
# Import necessary Standard and 3rd party libraries
#------------------------------------------------------------------
import sys
import pandas as pd
#------------------------------------------------------------------
# Import Modules: Custom Exception and Logger
#------------------------------------------------------------------
import src.myproject.utils as utils
import src.myproject.logger as logger
import src.myproject.exception as exception
from src.myproject.config.config_app import DataIngestionConfig
#------------------------------------------------------------------
# Log module loading
#------------------------------------------------------------------
logger.app_logger.info("Data Ingestion Module Loaded Successfully. Initiating Data Ingestion Process...")
#------------------------------------------------------------------
# Main execution block for data ingestion
#------------------------------------------------------------------
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.ingestion_config = config

    def initiate_data_ingestion_from_file(self) -> pd.DataFrame:
        """Ingest data from the raw data file specified in the configuration."""
        try:
            logger.app_logger.info("Starting data ingestion from file: %s", str(self.ingestion_config.raw_file_and_path))
            #----------------------------------------------------------------
            # Ensure the raw data directory exists
            #----------------------------------------------------------------
            logger.app_logger.info("Ensuring raw data directory exists at: %s", str(self.ingestion_config.raw_path))
            utils.ensure_directory_exists(self.ingestion_config.raw_path)
            logger.app_logger.info("Raw data directory verified/created successfully.")
            #----------------------------------------------------------------
            # Ingest data using the utility function
            #----------------------------------------------------------------
            logger.app_logger.info("Ingesting data from file: %s", str(self.ingestion_config.raw_file_and_path))
            df = utils.ingest_data_from_file(str(self.ingestion_config.raw_file_and_path))
            logger.app_logger.info("Data ingestion from file completed successfully.")
            #----------------------------------------------------------------
            # Separate features and target variable
            #----------------------------------------------------------------
            logger.app_logger.info("Separating features and target variable: %s", str(self.ingestion_config.target_column))
            X = df.drop(columns=[self.ingestion_config.target_column], axis=1)
            y = df[self.ingestion_config.target_column]
            logger.app_logger.info("Feature and target variable separation completed successfully.")
            
            return df, X, y
        except exception.CustomException as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce

    def train_test_split_data(self, X: pd.DataFrame, y: pd.Series):
        """Split the data into training, validation, and testing sets."""
        try:
            # First split into training+validation and testing sets
            (X_train, y_train), (X_val, y_val), (X_test, y_test) = utils.train_valid_test_split_data(self, X, y)

            return (X_train, y_train), (X_val, y_val), (X_test, y_test)
        except exception.CustomException as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce

    def save_data_splits(self, X_train, y_train, X_val, y_val, X_test, y_test):
        """Save the training and testing data splits to their respective paths."""
        try:
            # Ensure directories exist
            utils.ensure_directory_exists(self.ingestion_config.processed_dir_path)
            # Save training data
            X_train.to_csv(self.ingestion_config.x_train_data, index=False)
            y_train.to_csv(self.ingestion_config.y_train_data, index=False)
            # Save validation data
            X_val.to_csv(self.ingestion_config.x_val_data, index=False)
            y_val.to_csv(self.ingestion_config.y_val_data, index=False)
            # Save testing data
            X_test.to_csv(self.ingestion_config.x_test_data, index=False)
            y_test.to_csv(self.ingestion_config.y_test_data, index=False)
            logger.app_logger.info("Training and testing data splits saved successfully.")
            logger.app_logger.info("X_Train shape: %s", X_train.shape)
            logger.app_logger.info("Y_Train shape: %s", y_train.shape)
            logger.app_logger.info("X_Val shape: %s", X_val.shape)
            logger.app_logger.info("Y_Val shape: %s", y_val.shape)
            logger.app_logger.info("X_Test shape: %s", X_test.shape)
            logger.app_logger.info("Y_Test shape: %s", y_test.shape)
        except exception.CustomException as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
        
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
        
