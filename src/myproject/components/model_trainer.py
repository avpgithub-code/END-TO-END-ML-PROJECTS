"""
Module for training machine learning models.
Implements model training, hyperparameter tuning, and model selection.
"""
import sys
import pandas as pd
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import root_mean_squared_error, r2_score

#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
import src.myproject.utils as utils
import src.myproject.exception as exception
import src.myproject.logger as logger

from src.myproject.config.config_app import ModelTrainerConfig
#------------------------------------------------------------------
# Model Trainer Class
#------------------------------------------------------------------
logger.app_logger.info("Model Trainer Module Loaded Successfully. Initiating Model Training Process...")
#------------------------------------------------------------------
class ModelTrainer:
    def __init__(self):
        """
        Initializes the model trainer component with immutable config.
        Standard: Use Dependency Injection for configuration.
        """
        self.model_trainer_config = ModelTrainerConfig()
    #----------------------------------------------------------------
    def initiate_model_trainer(self, 
        x_train_transformed: pd.DataFrame, y_train: pd.Series,
        x_val_transformed: pd.DataFrame, y_val: pd.Series,
        x_test_transformed: pd.DataFrame, y_test: pd.Series
    ):
        """
        Trains multiple models and evaluates them on validation data.
        Selects the best model based on R2 Score.
        """
        try:
            logger.app_logger.info("Starting model training process...")
            #----------------------------------------------------------------
            # 1. Train and evaluate each model
            #----------------------------------------------------------------
            best_models_report = {}
            fitted_models = {}
            for model_name, config in self.model_trainer_config.model_hyperparameters.items():
                logger.app_logger.info("Training model: %s",model_name)
                #----------------------------------------------------------------
                # Hyperparameter Tuning using GridSearchCV
                #----------------------------------------------------------------
                grid = GridSearchCV(config["model"], config["params"], cv=3, scoring='r2')
                grid.fit(x_train_transformed, y_train)
                #----------------------------------------------------------------
                # 2. Evaluate the best tuned version on Validation Data
                #----------------------------------------------------------------
                best_version = grid.best_estimator_
                y_val_pred = best_version.predict(x_val_transformed)
                val_score = r2_score(y_val, y_val_pred)
                #----------------------------------------------------------------
                best_models_report[model_name] = val_score
                fitted_models[model_name] = best_version
                logger.app_logger.info("%s Best Val R2: %.4f", model_name, val_score)
                print("%s Best Val R2: %.4f", model_name, val_score)
            #----------------------------------------------------------------
            # 3. Prepare best models report and fitted models dictionary
            #    Champion Selection (Based on Validation Set)
            #----------------------------------------------------------------
            champion_name = max(best_models_report, key=best_models_report.get)
            champion_model = fitted_models[champion_name]
            logger.app_logger.info("The Best Fitted Model: %s", champion_name)
            #----------------------------------------------------------------
            # 4. Final Verification on UNSEEN Test Data
            # This is the single unbiased estimate of real-world performance
            #----------------------------------------------------------------
            unseen_test_pred = champion_model.predict(x_test_transformed)
            final_test_score = r2_score(y_test, unseen_test_pred)
            logger.app_logger.info("Final Performance on Unseen Test Data: %.4f", final_test_score)
            #----------------------------------------------------------------
            # 5. Persist Champion Model
            #----------------------------------------------------------------
            saved_file = joblib.dump(champion_model, self.model_trainer_config.champion_model_and_path)
            logger.app_logger.info("Champion Model saved at: %s", saved_file)
            #----------------------------------------------------------------
            
            return champion_name, champion_model, final_test_score

        except exception.CustomException as ce:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
#------------------------------------------------------------------
logger.app_logger.info("Model Trainer Module Execution Completed.")
#------------------------------------------------------------------  