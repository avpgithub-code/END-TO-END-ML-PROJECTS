""" Constants for ML-Project with Dynamic Path Resolution and Environment Variables
This module defines constants for directory paths and filenames used throughout the ML-Project.
It dynamically determines the project root and constructs paths based on environment variables,
ensuring flexibility and portability across different environments and setups.
"""
from pathlib import Path
import os
from dotenv import load_dotenv
import src.myproject.logger as logger
#----------------------------------------------------------------------------------------------------
def get_project_root() -> Path:
    #------------------------------------------------------------------------------------------------
    """Finds the project root by searching for a marker file.
    Start from the current file's location and move upwards until a marker file is found.
    Markers can be .env, .git, or pyproject.toml
    Returns: Path object representing the project root directory
    """
    for parent in Path(__file__).resolve().parents:
        # Markers commonly used in 2025: .env, .git, or pyproject.toml
        if (parent / ".env").exists() or \
            (parent / "pyproject.toml").exists() or \
            (parent / ".git").exists():
            return parent

    return Path(__file__).resolve().parent
#----------------------------------------------------------------------------------------------------
# 1. Establish the Anchor Paths for Root, Raw Data, and Processed Data
#----------------------------------------------------------------------------------------------------
PROJECT_ROOT = get_project_root()
#----------------------------------------------------------------------------------------------------
# 2. Directory Map (Centralized for easy updates)
#----------------------------------------------------------------------------------------------------
ARTIFACTS_DIR = (PROJECT_ROOT / "artifacts").resolve()
LOGS_DIR = (ARTIFACTS_DIR / "logs").resolve()
MODELS_DIR = (ARTIFACTS_DIR / "models").resolve()
PLOTS_DIR = (ARTIFACTS_DIR / "plots").resolve()
# print(f"PROJECT_ROOT: {PROJECT_ROOT}")
# print(f"ARTIFACTS_DIR: {ARTIFACTS_DIR}")
# print(f"LOGS_DIR: {LOGS_DIR}")
# print(f"MODELS_DIR: {MODELS_DIR}")
# print(f"PLOTS_DIR: {PLOTS_DIR}")
#----------------------------------------------------------------------------------------------------
DATA_DIR = (PROJECT_ROOT / "data").resolve()
PROCESSED_DIR = (DATA_DIR / "processed").resolve()
RAW_DIR = (DATA_DIR / "raw").resolve()
# print(f"DATA_DIR: {DATA_DIR}")
# print(f"PROCESSED_DIR: {PROCESSED_DIR}")
# print(f"RAW_DIR: {RAW_DIR}")
#----------------------------------------------------------------------------------------------------
NOTEBOOKS_DIR = (PROJECT_ROOT / "notebooks").resolve()
# print(f"NOTEBOOKS_DIR: {NOTEBOOKS_DIR}")
#----------------------------------------------------------------------------------------------------
SRC_DIR = (PROJECT_ROOT / "src").resolve()
SRC_LOGS_DIR = (SRC_DIR / "logs").resolve()
SRC_MYPROJECT_DIR = (SRC_DIR / "myproject").resolve()
SRC_COMPONENTS_DIR = (SRC_MYPROJECT_DIR / "components").resolve()
SRC_CONFIG_DIR = (SRC_MYPROJECT_DIR / "config").resolve()
SRC_PIPELINE_DIR = (SRC_MYPROJECT_DIR / "pipeline").resolve()
# print(f"SRC_DIR: {SRC_DIR}")
# print(f"SRC_LOGS_DIR: {SRC_LOGS_DIR}")
# print(f"SRC_MYPROJECT_DIR: {SRC_MYPROJECT_DIR}")
# print(f"SRC_COMPONENTS_DIR: {SRC_COMPONENTS_DIR}")
# print(f"SRC_CONFIG_DIR: {SRC_CONFIG_DIR}")
# print(f"SRC_PIPELINE_DIR: {SRC_PIPELINE_DIR}")
#----------------------------------------------------------------------------------------------------
# 2. Ensure Directories Exist
#----------------------------------------------------------------------------------------------------
for directory in [ARTIFACTS_DIR, LOGS_DIR, MODELS_DIR, PLOTS_DIR, DATA_DIR, PROCESSED_DIR, RAW_DIR, NOTEBOOKS_DIR,
                  SRC_DIR, SRC_LOGS_DIR, SRC_MYPROJECT_DIR, SRC_COMPONENTS_DIR, SRC_CONFIG_DIR, SRC_PIPELINE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
#----------------------------------------------------------------------------------------------------
# 3. Load Environment Variables from .env File
#----------------------------------------------------------------------------------------------------
load_dotenv(PROJECT_ROOT / ".env")
#----------------------------------------------------------------------------------------------------
# 4. Canonical filename Constants (Relative to their directories)
#----------------------------------------------------------------------------------------------------
DATA_RAW_FILE = os.getenv("RAW_DATA_SOURCE", "stud.csv") # Default to "stud.csv" if not set
#----------------------------------------------------------------------------------------------------
DATA_PROCESSED_FILE = "data.csv"
X_FILE = "X.csv"
Y_FILE = "y.csv"
X_TRAIN_FILE = "X_train.csv"
Y_TRAIN_FILE = "y_train.csv"
X_VAL_FILE = "X_val.csv"
Y_VAL_FILE = "y_val.csv"
X_TEST_FILE = "X_test.csv"
Y_TEST_FILE = "y_test.csv"
#----------------------------------------------------------------------------------------------------
# Other constants can be defined here as needed
#----------------------------------------------------------------------------------------------------
TARGET_COLUMN="math_score"
# #----------------------------------------------------------------------------------------------------
# 5. Final Absolute File Paths
#----------------------------------------------------------------------------------------------------
DATA_RAW_FILE_AND_PATH = (RAW_DIR / DATA_RAW_FILE).resolve()
DATA_PROCESSED_FILE_AND_PATH = (PROCESSED_DIR / DATA_PROCESSED_FILE).resolve()
X_FILE_AND_PATH = (PROCESSED_DIR / X_FILE).resolve()
Y_FILE_AND_PATH = (PROCESSED_DIR / Y_FILE).resolve()
X_TRAIN_FILE_AND_PATH = (PROCESSED_DIR / X_TRAIN_FILE).resolve()
Y_TRAIN_FILE_AND_PATH = (PROCESSED_DIR / Y_TRAIN_FILE).resolve()
X_VAL_FILE_AND_PATH = (PROCESSED_DIR / X_VAL_FILE).resolve()
Y_VAL_FILE_AND_PATH = (PROCESSED_DIR / Y_VAL_FILE).resolve()
X_TEST_FILE_AND_PATH = (PROCESSED_DIR / X_TEST_FILE).resolve()
Y_TEST_FILE_AND_PATH = (PROCESSED_DIR / Y_TEST_FILE).resolve()
# print(f"DATA_RAW_FILE_AND_PATH: {DATA_RAW_FILE_AND_PATH}")
# print(f"DATA_PROCESSED_FILE_AND_PATH: {DATA_PROCESSED_FILE_AND_PATH}")
# print(f"X_FILE_AND_PATH: {X_FILE_AND_PATH}")
# print(f"Y_FILE_AND_PATH: {Y_FILE_AND_PATH}")
# print(f"X_TRAIN_FILE_AND_PATH: {X_TRAIN_FILE_AND_PATH}")
# print(f"Y_TRAIN_FILE_AND_PATH: {Y_TRAIN_FILE_AND_PATH}")
# print(f"X_VAL_FILE_AND_PATH: {X_VAL_FILE_AND_PATH}")
# print(f"Y_VAL_FILE_AND_PATH: {Y_VAL_FILE_AND_PATH}")
# print(f"X_TEST_FILE_AND_PATH: {X_TEST_FILE_AND_PATH}")
# print(f"Y_TEST_FILE_AND_PATH: {Y_TEST_FILE_AND_PATH}")
#----------------------------------------------------------------------------------------------------
# 6. Example of Using Environment Variables for Configurable Constants (If Needed)
#----------------------------------------------------------------------------------------------------
# The logic: We define the constant here
# The config: We pull the actual value from .env
# DATABASE_URL = os.getenv("DATABASE_URL")

# # If the URL is missing, we can raise a clear error here
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL not found in .env file!")
#--------------------------------------------------
# Example usage:
# from src.constants import TRAIN_DATA_PATH
# import pandas as pd

# df = pd.read_csv(TRAIN_DATA_PATH)
#--------------------------------------------------
# Additional constants can be defined similarly
