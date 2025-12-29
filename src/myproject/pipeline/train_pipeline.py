import sys
import src.myproject.exception as exception
import src.myproject.logger as logger
from src.myproject.config.config_app import AppConfig
from src.myproject.components.data_ingestion import DataIngestion
from src.myproject.components.data_transformation import DataTransformation
from src.myproject.components.model_trainer import ModelTrainer
#------------------------------------------------------------------
# Training Pipeline Class
#------------------------------------------------------------------
logger.app_logger.info("Training Pipeline Module Loaded Successfully. Initiating Training Process...")
#------------------------------------------------------------------
class TrainPipeline:
    def __init__(self):
        """
        Initializes the training pipeline component with immutable config.
        Standard: Use Dependency Injection for configuration.
        """
        self.app_config = AppConfig()
        self.data_ingestion_config = DataIngestion()
        self.data_transformation_config = DataTransformation()
        self.model_trainer_config = ModelTrainer()
    #----------------------------------------------------------------
    def run_pipeline(self):
        """Runs the complete training pipeline: Ingestion, Transformation, Training."""
        try:
            logger.app_logger.info("Starting the training pipeline...")
            #----------------------------------------------------------------
            # Step 1: Data Ingestion
            #----------------------------------------------------------------
            df, X, y = self.data_ingestion_config.initiate_data_ingestion_from_file()
            self.data_ingestion_config.save_ingested_data(df, X, y)
            logger.app_logger.info("Data ingestion completed successfully.")
            #----------------------------------------------------------------
            # Split the Dataframe into Training, Validation, and Testing sets
            # Also derive and return the respective feature and target datasets
            # #----------------------------------------------------------------
            (X_train, y_train), (X_val, y_val), (X_test, y_test) = self.data_ingestion_config.train_test_split_data(X,y)
            logger.app_logger.info("Data split into training, validation and testing sets successfully.")
            # #----------------------------------------------------------------
            # # Save the training and testing data to their respective paths
            # #----------------------------------------------------------------
            self.data_ingestion_config.save_data_splits(X_train, y_train, X_val, y_val, X_test, y_test)
            logger.app_logger.info("Data ingestion process completed successfully.")            
            #----------------------------------------------------------------
            # Step 2: Data Transformation
            #----------------------------------------------------------------
            preprocessor    = self.data_transformation_config.get_data_transformer_object(df)
            #----------------------------------------------------------------
            # Initiate Data Transformation Process
            #----------------------------------------------------------------
            logger.app_logger.info("Starting Data Transformation process...")
            x_train_transformed, x_val_transformed, x_test_transformed = \
                self.data_transformation_config.initiate_data_transformation(
                preprocessor_object=preprocessor, 
                x_train=X_train, x_val=X_val, x_test=X_test)
            logger.app_logger.info("Data Transformation process completed successfully.")
            #----------------------------------------------------------------
            # Step 3: Model Training
            #----------------------------------------------------------------
            logger.app_logger.info("Starting Model Training process...")
            champion_name, champion_model, champion_score = self.model_trainer_config.initiate_model_trainer(
                x_train_transformed=x_train_transformed, y_train=y_train,
                x_val_transformed=x_val_transformed, y_val=y_val,
                x_test_transformed=x_test_transformed, y_test=y_test
            )
            logger.app_logger.info("Model Training process completed successfully.")
            logger.app_logger.info("Champion Model: %s with R2 Score: %.4f", champion_name, champion_score)
        except exception.CustomException as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
#------------------------------------------------------------------
if __name__ == "__main__":
    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()
#------------------------------------------------------------------