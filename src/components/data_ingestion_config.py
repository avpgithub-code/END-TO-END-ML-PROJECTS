"""Data ingestion configuration module.
This module sets up the configuration for data ingestion,
including paths for raw, training, and testing data.
It uses environment variables to define these paths.
"""
from dataclasses import dataclass
import os,sys
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from sklearn.model_selection import train_test_split
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
from src.exception import CustomException
from src.logger import app_logger
from src.utils import ensure_directory_exists,ingest_data_from_file
#------------------------------------------------------------------
# Load environment variables for data paths
#------------------------------------------------------------------
load_dotenv()
#--------------------------------------------------------------------
# Get data paths from environment variables
#--------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA = (BASE_DIR / os.getenv("DATA_PATH")).resolve()
RAW_DATA = (BASE_DIR / os.getenv("RAW_DATA_PATH")).resolve()
TRAIN_DATA = (BASE_DIR / os.getenv("TRAIN_DATA_PATH")).resolve()
TEST_DATA = (BASE_DIR / os.getenv("TEST_DATA_PATH")).resolve()
#--------------------------------------------------------------------
# Ensure necessary directories exist; otherwise, create them
#--------------------------------------------------------------------
ensure_directory_exists(RAW_DATA.parent)
ensure_directory_exists(TRAIN_DATA.parent)
ensure_directory_exists(TEST_DATA.parent)
#--------------------------------------------------------------------
# Log the data paths
#--------------------------------------------------------------------
app_logger.info(f"Raw Data Path: {RAW_DATA}")
app_logger.info(f"Train Data Path: {TRAIN_DATA}")
app_logger.info(f"Test Data Path: {TEST_DATA}")
#--------------------------------------------------------------------
# Get Constants for data splitting
#--------------------------------------------------------------------
TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
RANDOM_STATE = int(os.getenv("RANDOM_STATE", 42))
#--------------------------------------------------------------------
# Data ingestion configuration using dataclass
#--------------------------------------------------------------------
@dataclass
class DataIngestionConfig:
    data: str = DATA
    raw_data: str = RAW_DATA
    train_data: str = TRAIN_DATA
    test_data: str = TEST_DATA
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
            # Ingest data from the raw data file and return as DataFrame
            #--------------------------------------------------
            app_logger.info("Loading Ingestion Configuration. Starting data ingestion from file...")
            df = ingest_data_from_file(self.ingestion_config.raw_data)
            #--------------------------------------------------
            # Save the raw data to the specified path
            #--------------------------------------------------
            app_logger.info("Saving Raw data to the specified path...")
            df.to_csv(self.ingestion_config.data, index=False, header=False)
            app_logger.info("Raw data saved to: %s", self.ingestion_config.data)
            app_logger.info("Done with Ingestion Configuration Module...")
            return df
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise CustomException(exc_type, exc_value, exc_traceback) from e
    #------------------------------------------------------------------
    # Initiate data ingestion from database
    #------------------------------------------------------------------
    def initiate_data_ingestion_from_db(self):
        """Initiates the data ingestion process from database."""
        try:
            app_logger.info("Loading Ingestion Configuration. Starting data ingestion from database...")
            # Placeholder for database ingestion logic
            # Implement database connection and data retrieval here
            app_logger.info("Done with Ingestion Configuration Module...")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise CustomException(exc_type, exc_value, exc_traceback) from e
    #------------------------------------------------------------------
    # Split data into training and testing sets
    #------------------------------------------------------------------
    def train_test_split_data(self, data, test_size=TEST_SIZE, random_state=RANDOM_STATE):
        """Splits the data into training and testing sets."""
        try:
            app_logger.info("Splitting data into training and testing sets...")
            train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
            app_logger.info("Data split completed.")
            return train_data, test_data
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise CustomException(exc_type, exc_value, exc_traceback) from e
    #------------------------------------------------------------------
    # Save training and testing data to respective paths
    #------------------------------------------------------------------
    def save_data_splits(self, train_data, test_data):
        """Saves the training and testing data to their respective paths."""
        try:
            app_logger.info("Initiating training and testing data to respective paths...")
            train_data.to_csv(self.ingestion_config.train_data, index=False, header=False)
            test_data.to_csv(self.ingestion_config.test_data, index=False, header=False)
            app_logger.info(f"Training data saved to: {self.ingestion_config.train_data}")
            app_logger.info(f"Testing data saved to: {self.ingestion_config.test_data}")
            return train_data, test_data  
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise CustomException(exc_type, exc_value, exc_traceback) from e