import pandas as pd
import numpy as np
import joblib
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
import src.myproject.utils as utils
import src.myproject.logger as logger
from src.myproject.config.config_app import DataTransformationConfig
#------------------------------------------------------------------
# Data Transformation Class
#------------------------------------------------------------------
logger.app_logger.info("Data Transformation Module Loaded Successfully. Initiating Data Transformation Process...")
#------------------------------------------------------------------
class DataTransformation:
    def __init__(self):
        """
        Initializes the transformation component with immutable config.
        Standard: Use Dependency Injection for configuration.
        """
        self.transform_config = DataTransformationConfig()
    #----------------------------------------------------------------
    def get_data_transformer_object(self, df: pd.DataFrame) -> ColumnTransformer:
        """
        Creates a preprocessing pipeline for both numerical and categorical data.
        Standard: Encapsulate all transformations in a single ColumnTransformer.
        """
        num_cols, cat_cols = utils.list_dataframe_columns_by_type(df)
        preprocessor = utils.create_data_transformation_object(num_cols, cat_cols)

        return preprocessor
    #----------------------------------------------------------------
    def initiate_data_transformation(
        self, preprocessor_object: ColumnTransformer, 
        x_train: pd.DataFrame, x_val: pd.DataFrame, x_test: pd.DataFrame):
        """
        Applies transformations chronologically to prevent leakage.
        Step: Fit(Train) -> Transform(Train, Val, Test).
        """
        #----------------------------------------------------------------
        # Perform fit_transform on training data and transform on validation and test data
        # to prevent Data Leakage.
        #----------------------------------------------------------------
        logger.app_logger.info("Applying data transformations to training, validation, and testing sets...")
        x_train_transformed = preprocessor_object.fit_transform(x_train)
        x_val_transformed = preprocessor_object.transform(x_val)
        x_test_transformed = preprocessor_object.transform(x_test)
        #----------------------------------------------------------------
        logger.app_logger.info("Data transformations applied successfully.")
        #----------------------------------------------------------------
        # Save the preprocessor object
        #----------------------------------------------------------------
        logger.app_logger.info("Saving the preprocessor object...")
        utils.ensure_directory_exists(self.transform_config.pickled_object_file_path.parent)
        joblib.dump(preprocessor_object, self.transform_config.pickled_object_file_path)
        logger.app_logger.info("Preprocessor object saved at: %s", self.transform_config.pickled_object_file_path)
        #----------------------------------------------------------------
        # Save canonical processed CSVs
        #----------------------------------------------------------------
        logger.app_logger.info("Saving transformed datasets to CSV files...")
        x_train_transformed.to_csv(self.transform_config.x_transformed_data, index=False, header=True)
        x_val_transformed.to_csv(self.transform_config.x_val_transformed_data, index=False, header=True)
        x_test_transformed.to_csv(self.transform_config.x_test_transformed_data, index=False, header=True)
        logger.app_logger.info("Transformed datasets saved successfully.")
        
        return x_train_transformed, x_val_transformed, x_test_transformed