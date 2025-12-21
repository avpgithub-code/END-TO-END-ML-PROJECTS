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
from src.myproject.exception  import CustomException
from src.myproject.logger import app_logger
import src.myproject.utils as utils
import src.myproject.constants as constants
#------------------------------------------------------------------
# Load environment variables for data paths
#------------------------------------------------------------------
load_dotenv()
#--------------------------------------------------------------------
# Get data paths from environment variables
#--------------------------------------------------------------------
BASE_DIR = constants.PROJECT_ROOT
RAW_DATA = constants.DATA_RAW_DIR
DATA = constants.DATA_PROCESSED_FILE_PATH
INPUT_FEATURE_DATA = constants.X_FILE_PATH
TARGET_FEATURE_DATA = constants.Y_FILE_PATH
print(f"BASE_DIR: {BASE_DIR}")
print(f"DATA: {DATA}")
print(f"RAW_DATA: {RAW_DATA}")
print(f"INPUT_FEATURE_DATA: {INPUT_FEATURE_DATA}")
print(f"TARGET_FEATURE_DATA: {TARGET_FEATURE_DATA}")
#--------------------------------------------------------------------
# X_TRAIN_DATA = constants.DATA_PROCESSED_DIR / constants.X_TRAIN_FILE
# X_VAL_DATA = constants.DATA_PROCESSED_DIR / constants.X_VAL_FILE
# X_TEST_DATA = constants.DATA_PROCESSED_DIR / constants.X_TEST_FILE
# Y_TRAIN_DATA = constants.DATA_PROCESSED_DIR / constants.Y_TRAIN_FILE
# Y_VAL_DATA = constants.DATA_PROCESSED_DIR / constants.Y_VAL_FILE
# Y_TEST_DATA = constants.DATA_PROCESSED_DIR / constants.Y_TEST_FILE
#--------------------------------------------------------------------
# Ensure necessary directories exist; otherwise, create them
#--------------------------------------------------------------------
# utils.ensure_directory_exists(RAW_DATA.parent)
# utils.ensure_directory_exists(INPUT_FEATURE_DATA.parent)
# utils.ensure_directory_exists(TARGET_FEATURE_DATA.parent)
# utils.ensure_directory_exists(X_TRAIN_DATA.parent)
# utils.ensure_directory_exists(X_VAL_DATA.parent)
# utils.ensure_directory_exists(X_TEST_DATA.parent)
# utils.ensure_directory_exists(Y_TRAIN_DATA.parent)
# utils.ensure_directory_exists(Y_VAL_DATA.parent)
# utils.ensure_directory_exists(Y_TEST_DATA.parent)
#--------------------------------------------------------------------
# Log the data paths
#--------------------------------------------------------------------
# app_logger.info("Raw Data Path: %s", RAW_DATA)
# app_logger.info("Input Feature Data Path: %s", INPUT_FEATURE_DATA)
# app_logger.info("Target Feature Data Path: %s", TARGET_FEATURE_DATA)
# app_logger.info("X_Train Data Path: %s", X_TRAIN_DATA)
# app_logger.info("X_Val Data Path: %s", X_VAL_DATA)
# app_logger.info("X_Test Data Path: %s", X_TEST_DATA)
# app_logger.info("Y_Train Data Path: %s", Y_TRAIN_DATA)
# app_logger.info("Y_Val Data Path: %s", Y_VAL_DATA)
# app_logger.info("Y_Test Data Path: %s", Y_TEST_DATA)
# #--------------------------------------------------------------------
# Get Constants for data splitting
#--------------------------------------------------------------------
# TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
# TEST_SIZE_VAL = float(os.getenv("TEST_SIZE_VAL", 0.25))
# RANDOM_STATE = int(os.getenv("RANDOM_STATE", 42))
# TARGET_COLUMN = os.getenv("TARGET_COLUMN")
#--------------------------------------------------------------------
# Data ingestion configuration using dataclass
#--------------------------------------------------------------------
# @dataclass
# class DataIngestionConfig:
#     data: str = DATA
#     raw_data: str = RAW_DATA
#     input_feature_data: str = INPUT_FEATURE_DATA
#     target_feature_data: str = TARGET_FEATURE_DATA
#     x_train_data: str = X_TRAIN_DATA
#     x_val_data: str = X_VAL_DATA
#     x_test_data: str = X_TEST_DATA
#     y_train_data: str = Y_TRAIN_DATA
#     y_val_data: str = Y_VAL_DATA
#     y_test_data: str = Y_TEST_DATA
#     target_column: str = TARGET_COLUMN
# #------------------------------------------------------------------
# # Data Ingestion Class
# #------------------------------------------------------------------
# class DataIngestion:
#     def __init__(self, config: DataIngestionConfig):
#         self.ingestion_config = config
#     #------------------------------------------------------------------
#     # Initiate data ingestion from file
#     #------------------------------------------------------------------
#     def initiate_data_ingestion_from_file(self):
#         """Initiates the data ingestion process from file."""
#         try:
#             #--------------------------------------------------
#             # Ingest data from the Raw data file and return as DataFrame and X, y
#             #--------------------------------------------------
#             app_logger.info("Loading Ingestion Configuration. Starting data ingestion from file...")
#             df = utils.ingest_data_from_file(self.ingestion_config.raw_data)
#             app_logger.info("Data Ingestion from file completed successfully.")
#             #--------------------------------------------------
#             # Make 'X' Input Features and 'y' Target Feature
#             #--------------------------------------------------
#             X = df.drop(columns=[self.ingestion_config.target_column], axis=1)
#             y = df[self.ingestion_config.target_column]
#             #--------------------------------------------------
#             # Save the Ingested data to the specified path
#             #--------------------------------------------------
#             app_logger.info("Saving Raw data to the specified path...")
#             df.to_csv(self.ingestion_config.data, index=False, header=False)
#             X.to_csv(self.ingestion_config.input_feature_data, index=False, header=False)
#             y.to_csv(self.ingestion_config.target_feature_data, index=False, header=False)
#             #--------------------------------------------------
#             # Log the saved data paths
#             #--------------------------------------------------
#             app_logger.info("Original Data Dataframe saved to: %s", self.ingestion_config.data)
#             app_logger.info("Original Data Dataframe shape: %s", df.shape)
#             app_logger.info("X - Input feature data saved to: %s", self.ingestion_config.input_feature_data)
#             app_logger.info("X - Input Features shape: %s", X.shape)
#             app_logger.info("y - Target feature data saved to: %s", self.ingestion_config.target_feature_data)
#             app_logger.info("y - Target Feature shape: %s", y.shape)
#             app_logger.info("Done with Ingestion Configuration Module...")
#             #-------------------------------------------------
#             return df,X, y
#         except Exception as e:
#             exc_type, exc_value, exc_traceback = sys.exc_info()
#             raise CustomException(exc_type, exc_value, exc_traceback) from e
#     #------------------------------------------------------------------
#     # Initiate data ingestion from database
#     #------------------------------------------------------------------
#     def initiate_data_ingestion_from_db(self):
#         """Initiates the data ingestion process from database."""
#         try:
#             app_logger.info("Starting data ingestion from database...")
#             # Placeholder for database ingestion logic
#             # Implement database connection and data retrieval here
#             app_logger.info("Done with Ingestion Configuration Module...")
#         except Exception as e:
#             exc_type, exc_value, exc_traceback = sys.exc_info()
#             raise CustomException(exc_type, exc_value, exc_traceback) from e
#     #------------------------------------------------------------------
#     # Split data into training and testing sets
#     #------------------------------------------------------------------
#     def train_valid_test_split_data(self, X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE):
#         """Splits the data into training and testing sets."""
#         try:
#             #--------------------------------------------------
#             # 1. First Split: Isolate the final 'Test' set (e.g., 20% of total data)
#             # Use 'stratify' to ensure class proportions are kept across splits
#             #--------------------------------------------------
#             app_logger.info("Splitting X into X_train_full and X_test...")
#             X_train_full, X_test, y_train_full, y_test = train_test_split(
#                 X, y, test_size=test_size, random_state=random_state
#             )
#             #--------------------------------------------------
#             # 3. Second Split: Divide the 'Train-Full' set into 'Train' and 'Validation'
#             # To get a 60/20/20 overall split, we take 25% of the remaining 80% (0.25 * 0.80 = 0.20)
#             #--------------------------------------------------
#             app_logger.info("Splitting X_train_full into X_train and X_val...")
#             X_train, X_val, y_train, y_val = train_test_split(
#                 X_train_full, y_train_full, test_size=TEST_SIZE_VAL, random_state=random_state
#             )
#             app_logger.info("Data split completed.")
#             return (X_train, y_train), (X_val, y_val), (X_test, y_test)
#         except Exception as e:
#             exc_type, exc_value, exc_traceback = sys.exc_info()
#             raise CustomException(exc_type, exc_value, exc_traceback) from e
#     #------------------------------------------------------------------
#     # Save training and testing data to respective paths
#     #------------------------------------------------------------------
#     def save_data_splits(self, X_train, y_train, X_val, y_val, X_test, y_test):
#         """Saves the training and testing data to their respective paths."""
#         try:
#             app_logger.info("Initiating training, validating and testing data to respective paths...")
#             #--------------------------------------------------
#             # Save the data splits to their respective paths
#             #--------------------------------------------------
#             X_train.to_csv(self.ingestion_config.x_train_data, index=False, header=False)
#             y_train.to_csv(self.ingestion_config.y_train_data, index=False, header=False)
#             X_val.to_csv(self.ingestion_config.x_val_data, index=False, header=False)
#             y_val.to_csv(self.ingestion_config.y_val_data, index=False, header=False)
#             X_test.to_csv(self.ingestion_config.x_test_data, index=False, header=False)
#             y_test.to_csv(self.ingestion_config.y_test_data, index=False, header=False)
#             #--------------------------------------------------
#             app_logger.info("X_Train data saved to: %s", self.ingestion_config.x_train_data)
#             app_logger.info("Y_Train data saved to: %s", self.ingestion_config.y_train_data)
#             app_logger.info("X_Val data saved to: %s", self.ingestion_config.x_val_data)
#             app_logger.info("Y_Val data saved to: %s", self.ingestion_config.y_val_data)
#             app_logger.info("X_Test data saved to: %s", self.ingestion_config.x_test_data)
#             app_logger.info("Y_Test data saved to: %s", self.ingestion_config.y_test_data)
#             #--------------------------------------------------
#             app_logger.info("X_Train shape: %s", X_train.shape)
#             app_logger.info("Y_Train shape: %s", y_train.shape)
#             app_logger.info("X_Val shape: %s", X_val.shape)
#             app_logger.info("Y_Val shape: %s", y_val.shape)
#             app_logger.info("X_Test shape: %s", X_test.shape)
#             app_logger.info("Y_Test shape: %s", y_test.shape)
#             #--------------------------------------------------
#             app_logger.info("Data saving completed.")
#             return None
#         except Exception as e:
#             exc_type, exc_value, exc_traceback = sys.exc_info()
#             raise CustomException(exc_type, exc_value, exc_traceback) from e
