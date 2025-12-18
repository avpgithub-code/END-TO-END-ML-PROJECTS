"""Data ingestion configuration module.
This module sets up the configuration for data ingestion,
including paths for raw, training, and testing data.
It uses environment variables to define these paths.
"""
from dataclasses import dataclass
import os,sys
from pathlib import Path
from dotenv import load_dotenv
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
from src.exception import CustomException
from src.logger import logger
from src.utils import ensure_directory_exists,ingest_data_from_file
#------------------------------------------------------------------
# Load environment variables for data paths
#------------------------------------------------------------------
load_dotenv()
#--------------------------------------------------------------------
# Get data paths from environment variables
#--------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
RAW_DATA = (BASE_DIR / os.getenv("RAW_DATA_PATH")).resolve()
TRAIN_DATA = (BASE_DIR / os.getenv("TRAIN_DATA_PATH")).resolve()
TEST_DATA = (BASE_DIR / os.getenv("TEST_DATA_PATH")).resolve()
#--------------------------------------------------------------------
# Ensure necessary directories exist
#--------------------------------------------------------------------
ensure_directory_exists(RAW_DATA.parent)
ensure_directory_exists(TRAIN_DATA.parent)
ensure_directory_exists(TEST_DATA.parent)
#--------------------------------------------------------------------
# Log the data paths
#--------------------------------------------------------------------
logger.info(f"Raw Data Path: {RAW_DATA}")
logger.info(f"Train Data Path: {TRAIN_DATA}")
logger.info(f"Test Data Path: {TEST_DATA}")
#--------------------------------------------------------------------
# Data ingestion configuration using dataclass
#--------------------------------------------------------------------
@dataclass
class DataIngestionConfig:
    raw_data: str = RAW_DATA
    train_data: str = TRAIN_DATA
    test_data: str = TEST_DATA
#------------------------------------------------------------------
# Data Ingestion Class
#------------------------------------------------------------------
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.ingestion_config = config
        
    def initiate_data_ingestion_from_file(self):
        """Initiates the data ingestion process from file."""
        try:
            # Ingest data from the raw data file
            data = ingest_data_from_file(self.ingestion_config.raw_data)
            logger.info("Data ingestion completed successfully.")
            return data
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise CustomException(exc_type, exc_value, exc_traceback) from e    