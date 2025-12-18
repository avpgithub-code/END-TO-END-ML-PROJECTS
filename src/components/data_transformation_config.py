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
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
# from src.exception import CustomException
import src.exception as exception
from src.logger import app_logger
import src.utils as utils
#------------------------------------------------------------------
# Load environment variables for data paths
#------------------------------------------------------------------ 
load_dotenv()
#--------------------------------------------------------------------
# Get data paths from environment variables
#--------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
TRAIN_DATA = (BASE_DIR / os.getenv("TRAIN_DATA_FILE")).resolve()
TEST_DATA = (BASE_DIR / os.getenv("TEST_DATA_FILE")).resolve()
TRANSFORMED_TRAIN_DATA = (BASE_DIR / os.getenv("TRANSFORMED_TRAIN_FILE")).resolve()
TRANSFORMED_TEST_DATA = (BASE_DIR / os.getenv("TRANSFORMED_TEST_FILE")).resolve()
#--------------------------------------------------------------------
# Data transformation configuration using dataclass
#--------------------------------------------------------------------
@dataclass
class DataTransformationConfig:
    train_data: str = TRAIN_DATA
    test_data: str = TEST_DATA
    transformed_train_data: str = TRANSFORMED_TRAIN_DATA
    transformed_test_data: str = TRANSFORMED_TEST_DATA
#------------------------------------------------------------------
# Data Transformation Class
#------------------------------------------------------------------
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.transformation_config = config
    #--------------------------------------------------------------------
    # Initiate data transformation process
    def get_data_transformation(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Function to initiate data transformation on the given DataFrame.
        Applies scaling and encoding as necessary.
        Returns the transformed DataFrame.
        """
        try:
            app_logger.info("Starting data transformation process...")
            #---------------------------------------------------------------------------------
            # Identify numerical and categorical columns, Create Pipelines, and fit-transform
            #---------------------------------------------------------------------------------
            numerical_features, categorical_features =  utils.list_dataframe_columns_by_type(df)
            preprocessor = utils.create_data_transformation_pipelines(numerical_features, categorical_features)
            transformed_data = preprocessor.fit_transform(df)
            app_logger.info("Data transformation completed successfully.")
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
            app_logger.info("Transformed Train data saved to: %s", self.transformation_config.transformed_train_data)
            transformed_test_df.to_csv(self.transformation_config.transformed_test_data, index=False,header=False)
            app_logger.info("Transformed Test data saved to: %s", self.transformation_config.transformed_test_data)
        except Exception as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
    #------------------------------------------------------------------
    # First initiate data transformation process by reading test and train data from artifacts
    #------------------------------------------------------------------
    def initiate_data_transformation(self, train_data,test_data):
        train_df = utils.ingest_data_from_file(train_data)
        test_df = utils.ingest_data_from_file(test_data)
        #--------------------------------------------------
        # Apply data transformation on train and test data
        #--------------------------------------------------
        transformed_train_df = self.get_data_transformation(train_df)
        transformed_test_df = self.get_data_transformation(test_df)
        return transformed_train_df, transformed_test_df
#------------------------------------------------------------------