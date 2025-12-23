"""
Configuration Module for the Application
This module defines configuration parameters used throughout the application.
"""
#------------------------------------------------------------------
# Import necessary Standard and 3rd party libraries
#------------------------------------------------------------------
import os
from pathlib import Path
from dataclasses import dataclass
#------------------------------------------------------------------
# Import constants module
#------------------------------------------------------------------
from src.myproject import constants
#------------------------------------------------------------------

# Load variables at the earliest possible stage in a dedicated module
# load_dotenv()

@dataclass(frozen=True)
class AppConfig:
    """Centralized, immutable configuration object."""
    #-----------------------------------------------------------------
    # Mapping directly to pre-resolved constants
    #-----------------------------------------------------------------
    raw_path: Path = constants.RAW_DIR
    raw_file: str = constants.DATA_RAW_FILE
    raw_file_and_path: Path = constants.DATA_RAW_FILE_AND_PATH
    print("Raw Data File and Path:", raw_file_and_path)
    print("Raw Data Directory Path:", raw_path)
    print("Raw Data File Name:", raw_file)
    #-----------------------------------------------------------------
    # Environment-specific variables with safe casting
    #-----------------------------------------------------------------
    target_column: str = constants.TARGET_COLUMN
    test_size: float = constants.TEST_SIZE
    test_size_val: float = constants.TEST_SIZE_VAL
    random_state: int = constants.RANDOM_STATE
    log_file_max_bytes: int = constants.LOG_FILE_MAX_BYTES # 10 MB
    log_file_backup_count: int = constants.LOG_FILE_BACKUP_COUNT    
    print("target_column:", target_column)
    print("test_size:", test_size)
    print("test_size_val:", test_size_val)
    print("random_state:", random_state)
    print("log_file_max_bytes:", log_file_max_bytes)
    print("log_file_backup_count:", log_file_backup_count)
#------------------------------------------------------------------
@dataclass(frozen=True)
class DataIngestionConfig(AppConfig):
    """Data Ingestion Configuration Class using 2025 standards."""
    #----------------------------------------------------------------
    # Use Path instead of str to maintain object-oriented functionality
    #----------------------------------------------------------------
    # Directory Paths
    #----------------------------------------------------------------
    processed_dir_path: Path = constants.PROCESSED_DIR
    logs_dir_path: Path = constants.LOGS_DIR
    models_dir_path: Path = constants.MODELS_DIR
    plots_dir_path: Path = constants.PLOTS_DIR
    #----------------------------------------------------------------
    # Caononical File Paths
    #----------------------------------------------------------------
    data: Path = constants.DATA_PROCESSED_FILE_AND_PATH
    input_feature_data: Path = constants.X_FILE_AND_PATH
    target_feature_data: Path = constants.Y_FILE_AND_PATH
    pickled_object_file_path: Path = constants.PICKLE_FILE_AND_PATH
    #---------------------------------------------------------------s-
    # Data Split Paths: Train, Validation, Test
    #----------------------------------------------------------------
    x_train_data: Path = constants.X_TRAIN_FILE_AND_PATH
    x_val_data: Path = constants.X_VAL_FILE_AND_PATH
    x_test_data: Path = constants.X_TEST_FILE_AND_PATH
    y_train_data: Path = constants.Y_TRAIN_FILE_AND_PATH
    y_val_data: Path = constants.Y_VAL_FILE_AND_PATH
    y_test_data: Path = constants.Y_TEST_FILE_AND_PATH
    #----------------------------------------------------------------
