"""Main module to orchestrate data ingestion process.
This module initializes the data ingestion configuration,
executes the data ingestion process, and handles exceptions.
"""
import sys
import pandas as pd
import src.myproject.logger as logger
import src.myproject.exception as exception
from src.myproject.components.data_ingestion import DataIngestion
from src.myproject.components.data_transformation import DataTransformation
from src.myproject.components.model_trainer import ModelTrainer
#------------------------------------------------------------------
# Main function to orchestrate data ingestion
#------------------------------------------------------------------
def main():
    try:
        #----------------------------------------------------------------
        # Initialize data ingestion configuration and class
        #----------------------------------------------------------------
        data_ingestion = DataIngestion()
        data_transformation = DataTransformation()
        #----------------------------------------------------------------
        # Initite data ingestion from RAW file source and return as DataFrame
        #----------------------------------------------------------------
        raw_df,X,y = data_ingestion.initiate_data_ingestion_from_file()
        data_ingestion.save_ingested_data(raw_df, X, y)
        #----------------------------------------------------------------
        # Split the Dataframe into Training, Validation, and Testing sets
        # Also derive and return the respective feature and target datasets
        # #----------------------------------------------------------------
        (X_train, y_train), (X_val, y_val), (X_test, y_test) = data_ingestion.train_test_split_data(X,y)
        logger.app_logger.info("Data split into training, validation and testing sets successfully.")
        # #----------------------------------------------------------------
        # # Save the training and testing data to their respective paths
        # #----------------------------------------------------------------
        data_ingestion.save_data_splits(X_train, y_train, X_val, y_val, X_test, y_test)
        logger.app_logger.info("Data ingestion process completed successfully.")
        #----------------------------------------------------------------
        # Initialize Data Transformation Component
        #----------------------------------------------------------------
        data_transformation = DataTransformation()
        #----------------------------------------------------------------
        # Get Data Transformer Object
        #----------------------------------------------------------------
        logger.app_logger.info("Creating Data Transformation Preprocessor Object...")
        preprocessor = data_transformation.get_data_transformer_object(raw_df)
        logger.app_logger.info("Data Transformation Preprocessor Object created successfully.")
        #----------------------------------------------------------------
        # Initiate Data Transformation Process
        #----------------------------------------------------------------
        logger.app_logger.info("Starting Data Transformation process...")
        x_train_transformed, x_val_transformed, x_test_transformed = \
            data_transformation.initiate_data_transformation(
            preprocessor_object=preprocessor, 
            x_train=X_train, x_val=X_val, x_test=X_test)
        logger.app_logger.info("Data Transformation process completed successfully.")
        #----------------------------------------------------------------
        # Initialize Model Trainer Component
        #----------------------------------------------------------------
        model_trainer = ModelTrainer()
        #----------------------------------------------------------------
        # Initiate Model Training Process
        #----------------------------------------------------------------
        logger.app_logger.info("Starting Model Training process...")
        champion_name, champion_model, champion_score = model_trainer.initiate_model_trainer(
            x_train_transformed=x_train_transformed, y_train=y_train,
            x_val_transformed=x_val_transformed, y_val=y_val,
            x_test_transformed=x_test_transformed, y_test=y_test
        )
        logger.app_logger.info("Model Training process completed successfully.")
        logger.app_logger.info("Champion Model: %s with R2 Score: %.4f", champion_name, champion_score)
    except exception.CustomException as ce:
        logger.app_logger.error("An error occurred during data ingestion: %s", ce)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce

if __name__ == "__main__":
    main()