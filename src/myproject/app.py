import pandas as pd
import joblib
from flask import Flask, render_template, request
import os

# Get the directory of the current script (src/myproject)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to reach the PROJECT_ROOT
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
# Define the templates folder at the root
template_path = os.path.join(project_root, "templates")

applicaton = Flask(__name__, template_folder=template_path)
app = applicaton

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
@app.route('/')
def index():
    return render_template('index.html')
#----------------------------------------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from form matching stud.csv columns
    data = {
        'gender': [request.form.get('gender')],
        'race_ethnicity': [request.form.get('race_ethnicity')],
        'parental_level_of_education': [request.form.get('parental_level_of_education')],
        'lunch': [request.form.get('lunch')],
        'test_preparation_course': [request.form.get('test_preparation_course')],
        'reading_score': [float(request.form.get('reading_score'))],
        'writing_score': [float(request.form.get('writing_score'))]
    }
    #----------------------------------------------------------------
    # Convert to DataFrame
    df = pd.DataFrame(data)
    #----------------------------------------------------------------
    # Transform and Predict
    #----------------------------------------------------------------
    transformed_data = preprocessor.transform(df)
    prediction = model.predict(transformed_data)
    
    return render_template('index.html', results=round(prediction[0], 2))
#----------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
#----------------------------------------------------------------