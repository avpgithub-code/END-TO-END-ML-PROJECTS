"""Data ingestion configuration module.
This module sets up the configuration for data ingestion,
including paths for raw, training, and testing data.
It uses environment variables to define these paths.
"""
from dataclasses import dataclass
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
import src.myproject.exception  as exception
import src.myproject.logger as logger
import src.myproject.utils as utils
import src.myproject.constants as constants
#------------------------------------------------------------------
# Load environment variables for data paths
#------------------------------------------------------------------
load_dotenv()
#--------------------------------------------------------------------
# Get data paths from environment variables
#--------------------------------------------------------------------
ROOT_DIR = constants.PROJECT_ROOT
RAW_DATA = constants.DATA_RAW_FILE_AND_PATH
DATA = constants.DATA_PROCESSED_FILE_AND_PATH
INPUT_FEATURE_DATA = constants.X_FILE_AND_PATH
TARGET_FEATURE_DATA = constants.Y_FILE_AND_PATH
print(f"ROOT_DIR: {ROOT_DIR}")
print(f"RAW_DATA: {RAW_DATA}")
print(f"PROCESSED DATA: {DATA}")
print(f"INPUT_FEATURE_DATA: {INPUT_FEATURE_DATA}")
print(f"TARGET_FEATURE_DATA: {TARGET_FEATURE_DATA}")
#--------------------------------------------------------------------
X_TRAIN_DATA = constants.X_TRAIN_FILE_AND_PATH
X_VAL_DATA = constants.X_VAL_FILE_AND_PATH
X_TEST_DATA = constants.X_TEST_FILE_AND_PATH
Y_TRAIN_DATA = constants.Y_TRAIN_FILE_AND_PATH
Y_VAL_DATA = constants.Y_VAL_FILE_AND_PATH
Y_TEST_DATA = constants.Y_TEST_FILE_AND_PATH
print(f"X_TRAIN_DATA: {X_TRAIN_DATA}")
print(f"X_VAL_DATA: {X_VAL_DATA}")
print(f"X_TEST_DATA: {X_TEST_DATA}")
print(f"Y_TRAIN_DATA: {Y_TRAIN_DATA}")
print(f"Y_VAL_DATA: {Y_VAL_DATA}")
print(f"Y_TEST_DATA: {Y_TEST_DATA}")
# #--------------------------------------------------------------------
# Get Constants for data splitting
#--------------------------------------------------------------------
TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
TEST_SIZE_VAL = float(os.getenv("TEST_SIZE_VAL", 0.25))
RANDOM_STATE = int(os.getenv("RANDOM_STATE", 42))
TARGET_COLUMN = constants.TARGET_COLUMN
#--------------------------------------------------------------------
# Data ingestion configuration using dataclass
#--------------------------------------------------------------------
@dataclass
class DataIngestionConfig:
    """Data Ingestion Configuration Class.
    Attributes:
        raw_data (str): Path to the raw data file.
        data (str): Path to the processed data file.
        input_feature_data (str): Path to the input feature data file.
        target_feature_data (str): Path to the target feature data file.
        x_train_data (str): Path to the training input features data file.
        x_val_data (str): Path to the validation input features data file.
        x_test_data (str): Path to the testing input features data file.
        y_train_data (str): Path to the training target feature data file.
        y_val_data (str): Path to the validation target feature data file.
        y_test_data (str): Path to the testing target feature data file.
    """
    raw_data: str = RAW_DATA
    data: str = DATA
    input_feature_data: str = INPUT_FEATURE_DATA
    target_feature_data: str = TARGET_FEATURE_DATA
    x_train_data: str = X_TRAIN_DATA
    x_val_data: str = X_VAL_DATA
    x_test_data: str = X_TEST_DATA
    y_train_data: str = Y_TRAIN_DATA
    y_val_data: str = Y_VAL_DATA
    y_test_data: str = Y_TEST_DATA
#------------------------------------------------------------------
# Data Ingestion Class
#------------------------------------------------------------------
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.ingestion_config = config
    #------------------------------------------------------------------
    # Initiate data ingestion from file
    #------------------------------------------------------------------
    def initiate_data_ingestion_from_file(self):
        """Initiates the data ingestion process from file."""
        try:
            #--------------------------------------------------
            # Ingest data from the Raw data file and return as DataFrame and X, y
            #--------------------------------------------------
            logger.app_logger.info("Loading Ingestion Configuration. Starting data ingestion from file...")
            df = utils.ingest_data_from_file(self.ingestion_config.raw_data)
            logger.app_logger.info("Data Ingestion from file completed successfully.")
            #--------------------------------------------------
            # Make 'X' Input Features and 'y' Target Feature
            #--------------------------------------------------
            X = df.drop(columns=TARGET_COLUMN, axis=1)
            y = df[TARGET_COLUMN]
            #--------------------------------------------------
            # Save the Ingested data to the specified path
            #--------------------------------------------------
            logger.app_logger.info("Saving Raw data to the specified path...")
            df.to_csv(self.ingestion_config.data, index=False, header=False)
            X.to_csv(self.ingestion_config.input_feature_data, index=False, header=False)
            y.to_csv(self.ingestion_config.target_feature_data, index=False, header=False)
            #--------------------------------------------------
            # Log the saved data paths
            #--------------------------------------------------
            logger.app_logger.info("Original Data Dataframe saved to: %s", self.ingestion_config.data)
            logger.app_logger.info("Original Data Dataframe shape: %s", df.shape)
            logger.app_logger.info("X - Input feature data saved to: %s", self.ingestion_config.input_feature_data)
            logger.app_logger.info("X - Input Features shape: %s", X.shape)
            logger.app_logger.info("y - Target feature data saved to: %s", self.ingestion_config.target_feature_data)
            logger.app_logger.info("y - Target Feature shape: %s", y.shape)
            logger.app_logger.info("Done with Ingestion Configuration Module...")
            #-------------------------------------------------
            return df,X, y
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from e
    #------------------------------------------------------------------
    # Initiate data ingestion from database
    #------------------------------------------------------------------
    def initiate_data_ingestion_from_db(self):
        """Initiates the data ingestion process from database."""
        try:
            logger.app_logger.info("Starting data ingestion from database...")
            # Placeholder for database ingestion logic
            # Implement database connection and data retrieval here
            logger.app_logger.info("Done with Ingestion Configuration Module...")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from e
    #------------------------------------------------------------------
    # Split data into training and testing sets
    #------------------------------------------------------------------
    def train_valid_test_split_data(self, X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE):
        """Splits the data into training and testing sets."""
        try:
            #--------------------------------------------------
            # 1. First Split: Isolate the final 'Test' set (e.g., 20% of total data)
            # Use 'stratify' to ensure class proportions are kept across splits
            #--------------------------------------------------
            logger.app_logger.info("Splitting X into X_train_full and X_test...")
            X_train_full, X_test, y_train_full, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            #--------------------------------------------------
            # 3. Second Split: Divide the 'Train-Full' set into 'Train' and 'Validation'
            # To get a 60/20/20 overall split, we take 25% of the remaining 80% (0.25 * 0.80 = 0.20)
            #--------------------------------------------------
            logger.app_logger.info("Splitting X_train_full into X_train and X_val...")
            X_train, X_val, y_train, y_val = train_test_split(
                X_train_full, y_train_full, test_size=TEST_SIZE_VAL, random_state=random_state
            )
            logger.app_logger.info("Data split completed.")
            return (X_train, y_train), (X_val, y_val), (X_test, y_test)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from e
    #------------------------------------------------------------------
    # Save training and testing data to respective paths
    #------------------------------------------------------------------
    def save_data_splits(self, X_train, y_train, X_val, y_val, X_test, y_test):
        """Saves the training and testing data to their respective paths."""
        try:
            logger.app_logger.info("Initiating training, validating and testing data to respective paths...")
            #--------------------------------------------------
            # Save the data splits to their respective paths
            #--------------------------------------------------
            X_train.to_csv(self.ingestion_config.x_train_data, index=False, header=False)
            y_train.to_csv(self.ingestion_config.y_train_data, index=False, header=False)
            X_val.to_csv(self.ingestion_config.x_val_data, index=False, header=False)
            y_val.to_csv(self.ingestion_config.y_val_data, index=False, header=False)
            X_test.to_csv(self.ingestion_config.x_test_data, index=False, header=False)
            y_test.to_csv(self.ingestion_config.y_test_data, index=False, header=False)
            #--------------------------------------------------
            logger.app_logger.info("X_Train data saved to: %s", self.ingestion_config.x_train_data)
            logger.app_logger.info("Y_Train data saved to: %s", self.ingestion_config.y_train_data)
            logger.app_logger.info("X_Val data saved to: %s", self.ingestion_config.x_val_data)
            logger.app_logger.info("Y_Val data saved to: %s", self.ingestion_config.y_val_data)
            logger.app_logger.info("X_Test data saved to: %s", self.ingestion_config.x_test_data)
            logger.app_logger.info("Y_Test data saved to: %s", self.ingestion_config.y_test_data)
            #--------------------------------------------------
            logger.app_logger.info("X_Train shape: %s", X_train.shape)
            logger.app_logger.info("Y_Train shape: %s", y_train.shape)
            logger.app_logger.info("X_Val shape: %s", X_val.shape)
            logger.app_logger.info("Y_Val shape: %s", y_val.shape)
            logger.app_logger.info("X_Test shape: %s", X_test.shape)
            logger.app_logger.info("Y_Test shape: %s", y_test.shape)
            #--------------------------------------------------
            logger.app_logger.info("Data saving completed.")
            return None
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from e
