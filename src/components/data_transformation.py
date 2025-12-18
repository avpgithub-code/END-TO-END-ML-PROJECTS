"""
Data Transformation Module
This module provides classes and functions to perform data transformation
on ingested data, including scaling and encoding.
"""
import os,sys
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from dataclasses import dataclass
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
DATA = (BASE_DIR / os.getenv("DATA_PATH")).resolve()
PROCESSED_DATA = (BASE_DIR / os.getenv("PROCESSED_DATA_PATH")).resolve
TRANSFORMED_DATA = (BASE_DIR / os.getenv("TRANSFORMED_DATA_PATH")).resolve()
#--------------------------------------------------------------------
# Ensure necessary directories exist; otherwise, create them
#--------------------------------------------------------------------
ensure_directory_exists(PROCESSED_DATA.parent)
ensure_directory_exists(TRANSFORMED_DATA.parent)
#--------------------------------------------------------------------
# Log the data paths
#--------------------------------------------------------------------
logger.info(f"Processed Data Path: {PROCESSED_DATA}")
logger.info(f"Transformed Data Path: {TRANSFORMED_DATA}")
#--------------------------------------------------------------------
# Data transformation configuration using dataclass
#--------------------------------------------------------------------
@dataclass
class DataTransformationConfig:
    data: str = DATA
    processed_data: str = PROCESSED_DATA
    transformed_data: str = TRANSFORMED_DATA
#------------------------------------------------------------------
# Data Transformation Class
#------------------------------------------------------------------
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.transformation_config = config
    #------------------------------------------------------------------
    # Initiate data transformation process
    def initiate_data_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Function to initiate data transformation on the given DataFrame.
        Applies scaling and encoding as necessary.
        Returns the transformed DataFrame.
        """
        try:
            logger.info("Starting data transformation process...")
            # Example transformation: Scaling numerical features
            numerical_features = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_features = df.select_dtypes(include=[object]).columns.tolist()
            
            # Define transformers
            numerical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])
            
            # Combine transformers into a ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numerical_transformer, numerical_features),
                    ('cat', categorical_transformer, categorical_features)
                ])
            
            # Fit and transform the data
            transformed_data = preprocessor.fit_transform(df)
            logger.info("Data transformation completed successfully.")
            return pd.DataFrame(transformed_data)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise CustomException(exc_type, exc_value, exc_traceback) from e
    #------------------------------------------------------------------
    # Save transformed data to file
    def save_transformed_data(self, transformed_df: pd.DataFrame):
        """Saves the transformed DataFrame to the specified path."""
        try:
            transformed_df.to_csv(self.transformation_config.transformed_data, index=False)
            logger.info(f"Transformed data saved to: {self.transformation_config.transformed_data}")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise CustomException(exc_type, exc_value, exc_traceback) from e

#------------------------------------------------------------------
# Log module loading
logger.info("Data Transformation Module Loaded Successfully.")
#------------------------------------------------------------------
if __name__ == "__main__":
    try:
        #----------------------------------------------------------------
        # Initialize data transformation configuration and class
        #----------------------------------------------------------------
        transformation_config = DataTransformationConfig()
        data_transformation = DataTransformation(config=transformation_config)
        #----------------------------------------------------------------
        # Ingest data from file
        #----------------------------------------------------------------
        raw_data = ingest_data_from_file(transformation_config.data)
        df = pd.read_csv(transformation_config.data)
        #----------------------------------------------------------------
        # Initiate data transformation
        transformed_df = data_transformation.initiate_data_transformation(df)
        #----------------------------------------------------------------
        # Save transformed data
        data_transformation.save_transformed_data(transformed_df)
        logger.info("Data transformation process completed successfully.")
    except CustomException as ce:
        logger.error(f"An error occurred during data transformation: {ce}")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise CustomException(exc_type, exc_value, exc_traceback) from ce