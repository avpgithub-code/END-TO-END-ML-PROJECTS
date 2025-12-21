"""
Data Transformation Module
This module provides classes and functions to perform data transformation
on ingested data, including scaling and encoding.
"""
import os
import sys
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
import src.myproject.exception as exception
from src.myproject.logger import app_logger
import src.myproject.utils as utils
from src.myproject.components.data_transformation_config import DataTransformationConfig,DataTransformation
#------------------------------------------------------------------
# Log module loading
app_logger.info("Data Transformation Module Loaded Successfully.")
#------------------------------------------------------------------
if __name__ == "__main__":
    try:
        #----------------------------------------------------------------
        # Initialize data transformation configuration and class
        #----------------------------------------------------------------
        transformation_config = DataTransformationConfig()
        data_transformation = DataTransformation(config=transformation_config)
        transformed_train_df, transformed_test_df = \
            data_transformation.initiate_data_transformation(
                transformation_config.train_data,transformation_config.test_data)
        #----------------------------------------------------------------
        # Save transformed data
        #----------------------------------------------------------------
        data_transformation.save_transformed_data(transformed_train_df,transformed_test_df)
        app_logger.info("Transformed Training Data Type: %s", type(transformed_train_df))
        app_logger.info("Transformed Training Data Shape: %s", transformed_train_df.shape)
        app_logger.info("Transformed Testing Data Type: %s", type(transformed_test_df))
        app_logger.info("Transformed Testing Data Shape: %s", transformed_test_df.shape)
    except exception.CustomException as ce:
        app_logger.error("An error occurred during data transformation: %s", ce)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce