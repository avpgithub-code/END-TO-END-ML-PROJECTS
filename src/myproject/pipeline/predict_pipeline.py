import sys
import pandas as pd
import os
import joblib

import src.myproject.constants as constants
from src.myproject.exception import CustomException
from src.myproject.logger import app_logger

class PredictPipeline:
    def __init__(self):
        """
        Initializes the prediction pipeline with a trained model and preprocessor.
        """
        pass
    def predict(self, features: pd.DataFrame) -> pd.Series:
        """
        Transforms the input features and makes predictions using the trained model.
        """
        try:
            # Get the directory of the current script (src/myproject)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up two levels to reach the PROJECT_ROOT
            project_root = constants.PROJECT_ROOT
            # Define the templates folder at the root
            template_path = os.path.join(project_root, "templates")

            # applicaton = Flask(__name__, template_folder=template_path)
            # app = applicaton

            # Define paths for artifacts relative to project root
            PREPROCESSOR_PATH = os.path.join(project_root, "artifacts", "models", "preprocessor.joblib")
            MODEL_PATH = os.path.join(project_root, "artifacts", "models", "champion_model.joblib")
            #----------------------------------------------------------------
            # Load artifacts once when app starts
            preprocessor = joblib.load(PREPROCESSOR_PATH)
            model = joblib.load(MODEL_PATH)
            #----------------------------------------------------------------
            # Critical: Ensure the preprocessor always outputs a DataFrame
            preprocessor.set_output(transform="pandas")
            #----------------------------------------------------------------
            app_logger.info("Starting prediction process...")
            # Ensure the preprocessor outputs a DataFrame
            preprocessor.set_output(transform="pandas")
            # Transform the input features
            transformed_features = preprocessor.transform(features)
            app_logger.info("Feature transformation completed successfully.")
            # Make predictions
            predictions = model.predict(transformed_features)
            app_logger.info("Prediction process completed successfully.")
            
            return pd.Series(predictions)
        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:
    # def __init__(self, **kwargs):
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: float,
        writing_score: float
    ):
        """
        Initializes the custom data instance with input features.
        """
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score
    #----------------------------------------------------------------
    def get_data_as_data_frame(self) -> pd.DataFrame:
        """
        Converts the input features into a pandas DataFrame.
        """
        try:
            data_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score]
            }
            return pd.DataFrame(data_dict)
        except Exception as e:
            raise CustomException(e, sys)
#------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage
    custom_data = CustomData(
        gender="female",
        race_ethnicity="group B",
        parental_level_of_education="bachelor's degree",
        lunch="standard",
        test_preparation_course="none",
        reading_score=72.0,
        writing_score=74.0
    )
    input_df = custom_data.get_data_as_data_frame()
    # Load model and preprocessor
    project_root = constants.PROJECT_ROOT
    PREPROCESSOR_PATH = os.path.join(project_root, "artifacts", "models", "preprocessor.joblib")
    MODEL_PATH = os.path.join(project_root, "artifacts", "models", "champion_model.joblib")
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)
    # Initialize prediction pipeline
    predict_pipeline = PredictPipeline(model=model, preprocessor=preprocessor)
    # Make prediction
    prediction = predict_pipeline.predict(input_df)
    print(f"Prediction: {prediction.iloc[0]}")
#------------------------------------------------------------------