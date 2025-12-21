"""
Data Transformation Module
This module provides classes and functions to perform data transformation
on ingested data, including scaling and encoding.
"""
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import numpy as np
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
import src.myproject.exception as exception
import src.myproject.logger as logger
import src.myproject.utils as utils
import src.myproject.constants as constants
#------------------------------------------------------------------
# Load environment variables for data paths
#------------------------------------------------------------------
load_dotenv()
#--------------------------------------------------------------------
# Get data paths from Contants Module
#--------------------------------------------------------------------
ROOT_DIR = constants.PROJECT_ROOT
TARGET_COLUMN = constants.TARGET_COLUMN
#--------------------------------------------------------------------
RAW_DATA = constants.DATA_RAW_FILE_AND_PATH
PROCESSED_DATA = constants.DATA_PROCESSED_FILE_AND_PATH
X_DATA = constants.X_FILE_AND_PATH
Y_DATA = constants.Y_FILE_AND_PATH
X_TRAIN_DATA = constants.X_TRAIN_FILE_AND_PATH
Y_TRAIN_DATA = constants.Y_TRAIN_FILE_AND_PATH
X_TEST_DATA = constants.X_TEST_FILE_AND_PATH
Y_TEST_DATA = constants.Y_TEST_FILE_AND_PATH
X_VAL_DATA = constants.X_VAL_FILE_AND_PATH
Y_VAL_DATA = constants.Y_VAL_FILE_AND_PATH
print(f"RAW_DATA: {RAW_DATA}")
print(f"PROCESSED_DATA: {PROCESSED_DATA}")
print(f"X_DATA: {X_DATA}")
print(f"Y_DATA: {Y_DATA}")
print(f"X_TRAIN_DATA: {X_TRAIN_DATA}")
print(f"Y_TRAIN_DATA: {Y_TRAIN_DATA}")
print(f"X_TEST_DATA: {X_TEST_DATA}")
print(f"Y_TEST_DATA: {Y_TEST_DATA}")
print(f"X_VAL_DATA: {X_VAL_DATA}")
print(f"Y_VAL_DATA: {Y_VAL_DATA}")
#--------------------------------------------------------------------
# Data transformation configuration
#--------------------------------------------------------------------
@dataclass
class DataTransformationConfig:
    target_column: str = TARGET_COLUMN
    x_train_data: str = X_TRAIN_DATA
    x_valid_data: str = X_VAL_DATA
    x_test_data: str = X_TEST_DATA
    y_train: str = Y_TRAIN_DATA
    y_valid: str = Y_VAL_DATA
    y_test: str = Y_TEST_DATA
    x_data: str = X_DATA
    y_data: str = Y_DATA
#------------------------------------------------------------------
# Data Transformation Class
#------------------------------------------------------------------
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.transformation_config = config
    #--------------------------------------------------------------------
    # Initiate data transformation process
    
    def prepare_for_data_transformation(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Function to initiate data transformation on the given DataFrame.
        Applies scaling and encoding as necessary.
        Returns the transformed DataFrame.
        """
        try:
            logger.app_logger.info("Starting data transformation process...")
            #---------------------------------------------------------------------------------
            # Identify numerical and categorical columns, Create Pipelines, and fit-transform
            #---------------------------------------------------------------------------------
            target_col = self.transformation_config.target_column
            print(f"Target Column: {target_col}")
            numerical_features, categorical_features =  utils.list_dataframe_columns_by_type(df)
            preprocessor = utils.create_data_transformation_pipelines(numerical_features, categorical_features)
            # feature_names = preprocessor.get_feature_names_out()
            # app_logger.info("Feature names after transformation: %s", feature_names)
            # print(f"Feature names after transformation: {feature_names}")
            # transformed_data = preprocessor.fit_transform(df)
            logger.app_logger.info("Data transformation completed successfully.")
            #---------------------------------------------------------------------------------
            return pd.DataFrame(transformed_data)
        except Exception as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
    #------------------------------------------------------------------
    # Save transformed data to file
    def save_transformed_data(self, transformed_train_df,transformed_test_df):
        """Saves the transformed DataFrame to the specified path."""
        try:
            transformed_train_df.to_csv(self.transformation_config.transformed_train_data, index=False,header=False)
            logger.app_logger.info("Transformed Train data saved to: %s", self.transformation_config.transformed_train_data)
            transformed_test_df.to_csv(self.transformation_config.transformed_test_data, index=False,header=False)
            logger.app_logger.info("Transformed Test data saved to: %s", self.transformation_config.transformed_test_data)
        except Exception as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
    #------------------------------------------------------------------
    # First initiate data transformation process by reading test and train data from artifacts
    #------------------------------------------------------------------
    def initiate_data_transformation(self, train_data,test_data):
        #--------------------------------------------------
        # Ingest train and test data from Artifacts
        #--------------------------------------------------
        train_df = utils.ingest_data_from_file(train_data)
        test_df = utils.ingest_data_from_file(test_data)
        #--------------------------------------------------
        # Apply data transformation on train and test data
        #--------------------------------------------------
        transformed_train_df = self.get_data_transformation(train_df)
        transformed_test_df = self.get_data_transformation(test_df)
        return transformed_train_df, transformed_test_df
#------------------------------------------------------------------