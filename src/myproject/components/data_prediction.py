import sys
import pandas as pd
import joblib

import src.myproject.exception as exception
import src.myproject.logger as logger
#------------------------------------------------------------------
# Import Prediction Pipeline Config
#------------------------------------------------------------------
from src.myproject.config.config_app import PredictionPipelineConfig
#------------------------------------------------------------------
# Prediction Pipeline Class
#------------------------------------------------------------------
logger.app_logger.info("Prediction Pipeline Module Loaded Successfully. Initiating Prediction Process...")
#------------------------------------------------------------------
class PredictionPipeline:
    def __init__(self):
        """
        Initializes the prediction pipeline component with immutable config.
        Standard: Use Dependency Injection for configuration.
        """
        self.prediction_pipeline_config = PredictionPipelineConfig()
    #----------------------------------------------------------------
    def initiate_prediction(self, input_data: pd.DataFrame) -> pd.Series:
        """
        Generates predictions using the pre-trained champion model.
        """
        try:
            logger.app_logger.info("Starting prediction process...")
            #----------------------------------------------------------------
            # Load Preprocessor Object
            #----------------------------------------------------------------
            preprocessor = joblib.load(self.prediction_pipeline_config.preprocessor_file_path)
            logger.app_logger.info("Preprocessor object loaded successfully.")
            #----------------------------------------------------------------
            # Transform Input Data
            #----------------------------------------------------------------
            input_data_transformed = preprocessor.transform(input_data)
            logger.app_logger.info("Input data transformed successfully.")
            #----------------------------------------------------------------
            # Load Champion Model
            #----------------------------------------------------------------
            champion_model = joblib.load(self.prediction_pipeline_config.champion_model_file_path)
            logger.app_logger.info("Champion model loaded successfully.")
            #----------------------------------------------------------------
            # Generate Predictions
            #----------------------------------------------------------------
            predictions = champion_model.predict(input_data_transformed)
            logger.app_logger.info("Predictions generated successfully.")
            return pd.Series(predictions)
        except exception.CustomException as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.app_logger.error("Error occurred in Prediction Pipeline: %s", str(ce))
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
#------------------------------------------------------------------
if __name__ == "__main__":
    try:
        #----------------------------------------------------------------
        # Example usage of PredictionPipeline
        #----------------------------------------------------------------
        prediction_pipeline = PredictionPipeline()
        # Example input data as a DataFrame (replace with actual data)
        example_input_data = pd.DataFrame({
            "gender": ["female"],
            "race_ethnicity": ["group B"],
            "parental_level_of_education": ["bachelor's degree"],
            "lunch": ["standard"],
            "test_preparation_course": ["none"],
            "reading_score": [72],
            "writing_score": [74]
        })
        predictions = prediction_pipeline.initiate_prediction(example_input_data)
        logger.app_logger.info("Predictions: %s", predictions.tolist())
    except exception.CustomException as ce:
        logger.app_logger.error("An error occurred during prediction: %s", ce)
        exc_type, exc_value, exc_traceback = sys.exc_info()
