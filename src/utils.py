"""
Utility Functions Module for the Application
This module provides utility functions used across the application,
such as ensuring the existence of directories.
"""
import os
from pathlib import Path
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
import src.exception as exception
import src.logger as logger
#--------------------------------------------------------------------
# Ensure directory exists function
#--------------------------------------------------------------------
def ensure_directory_exists(directory_path):
    """Checks if a directory exists, and creates it if necessary."""
    path = Path(directory_path)
    if not path.exists():
        # Creates the directory and any necessary parent directories
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")
#--------------------------------------------------------------------
# Function to Read data from file
#--------------------------------------------------------------------
def ingest_data_from_file(raw_data: str):
    """
    Function to ingest data from a given file path.
    Raises CustomException on failure.
    """
    try:
        if not os.path.exists(raw_data):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from FileNotFoundError(f"The file {raw_data} does not exist.")
        with open(raw_data, 'r', encoding='utf-8') as file:
            df = pd.read_csv(file)
            logger.app_logger.info("Data ingested successfully from %s", raw_data)
            return df
    except exception.CustomException as ce:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
#--------------------------------------------------------------------
# List Dataframe Columns by Type
#--------------------------------------------------------------------
def list_dataframe_columns_by_type(df: pd.DataFrame):
    """
    Returns lists of numerical and character (object/string) column names.
    """
    #----------------------------------------------------
    # 'number' includes both integers and floats
    #----------------------------------------------------
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    #----------------------------------------------------
    # 'object' is standard for characters/strings in 2025
    # 'category' is also included for categorical types
    #----------------------------------------------------
    character_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    return numerical_cols, character_cols
#--------------------------------------------------------------------
# Perform Data Transformation Pipelines
#--------------------------------------------------------------------
def create_data_transformation_pipelines(numerical_features, categorical_features):
    """
    Creates and returns data transformation pipelines for numerical and categorical features.
    """
    try:
        logger.app_logger.info("Creating Numerical and Categorical data transformation pipelines...")
        #----------------------------------------------------------------
        # Define transformers for numerical and categorical features
        #----------------------------------------------------------------
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        #----------------------------------------------------------------
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        #----------------------------------------------------------------
        # Combine transformers into a ColumnTransformer
        #----------------------------------------------------------------
        logger.app_logger.info("Combining transformers into a ColumnTransformer...")
        #----------------------------------------------------------------
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        #----------------------------------------------------------------
        logger.app_logger.info("Data transformation pipelines created successfully.")
        #----------------------------------------------------------------
        return preprocessor
    except Exception as ce:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce