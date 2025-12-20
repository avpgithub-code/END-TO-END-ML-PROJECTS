from pathlib import Path
import os
from dotenv import load_dotenv

def get_project_root() -> Path:
    """Finds the project root by searching for a marker file."""
    # Start from the current file's location
    for parent in Path(__file__).resolve().parents:
        # Markers commonly used in 2025: .env, .git, or pyproject.toml
        if (parent / ".env").exists() or (parent / ".git").exists():
            return parent
    # Fallback to the immediate parent if no marker is found
    return Path(__file__).resolve().parent

# 1. Establish the Anchor
PROJECT_ROOT = get_project_root()

# 2. Load Environment Variables
load_dotenv(PROJECT_ROOT / ".env")

# 3. Build Paths Dynamically
# Now, even if you move constants.py, these remain correct
#----------------------------------------------------------------------------------------------------
# Constants for Artifacts directories and file paths
#----------------------------------------------------------------------------------------------------
ARTIFACTS_DIR = PROJECT_ROOT / os.getenv("ARTIFACTS", "artifacts")
ARTIFACTS_LOGS_DIR = PROJECT_ROOT / os.getenv("ARTIFACTS_LOGS", f"{os.getenv('ARTIFACTS', 'artifacts')}/logs")
ARTIFACTS_MODELS_DIR = PROJECT_ROOT / os.getenv("ARTIFACTS_MODELS", f"{os.getenv('ARTIFACTS', 'artifacts')}/models")
ARTIFACTS_PLOTS_DIR = PROJECT_ROOT / os.getenv("ARTIFACTS_PLOTS", f"{os.getenv('ARTIFACTS', 'artifacts')}/plots")
#----------------------------------------------------------------------------------------------------
# Constants for Data directories and file paths
#----------------------------------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / os.getenv("DATA", f"{os.getenv('PROJECT_ROOT', PROJECT_ROOT)}/data")
DATA_PROCESSED_DIR = PROJECT_ROOT / os.getenv("DATA_PROCESSED", f"{os.getenv('DATA', 'data')}/processed")
DATA_RAW_DIR = PROJECT_ROOT / os.getenv("DATA_RAW", f"{os.getenv('DATA', 'data')}/raw")
#----------------------------------------------------------------------------------------------------
NOTEBOOKS_DIR = PROJECT_ROOT / os.getenv("NOTEBOOKS", "notebooks")
#----------------------------------------------------------------------------------------------------
SRC_DIR = PROJECT_ROOT / os.getenv("SRC", f"{os.getenv('PROJECT_ROOT', PROJECT_ROOT)}/src")
SRC_MYPROJECT_DIR = PROJECT_ROOT / os.getenv("SRC_MYPROJECT", f"{os.getenv('SRC', 'src')}/myproject")
SRC_MYPROJECT_COMPONENTS_DIR = PROJECT_ROOT / os.getenv("SRC_MYPROJECT_COMPONENTS", f"{os.getenv('SRC_MYPROJECT', 'myproject')}/components")
SRC_MYPROJECT_CONFIG_DIR = PROJECT_ROOT / os.getenv("SRC_MYPROJECT_CONFIG", f"{os.getenv('SRC_MYPROJECT', 'myproject')}/config")
SRC_MYPROJECT_PIPELINES_DIR = PROJECT_ROOT / os.getenv("SRC_MYPROJECT_PIPELINES", f"{os.getenv('SRC_MYPROJECT', 'myproject')}/pipelines")
#----------------------------------------------------------------------------------------------------
# Example file paths
print("Project root set to:", PROJECT_ROOT)
print(f"Artifacts directory set to: {ARTIFACTS_DIR}")
print(f"Artifacts logs directory set to: {ARTIFACTS_LOGS_DIR}")
print(f"Artifacts models directory set to: {ARTIFACTS_MODELS_DIR}")
print(f"Artifacts plots directory set to: {ARTIFACTS_PLOTS_DIR}")
print(f"Data directory set to: {DATA_DIR}")
print(f"Processed data directory set to: {DATA_PROCESSED_DIR}")
print(f"Raw data directory set to: {DATA_RAW_DIR}")
print(f"Notebooks directory set to: {NOTEBOOKS_DIR}")
print(f"Source directory set to: {SRC_DIR}")
print(f"MyProject source directory set to: {SRC_MYPROJECT_DIR}")
print(f"MyProject components directory set to: {SRC_MYPROJECT_COMPONENTS_DIR}")
print(f"MyProject config directory set to: {SRC_MYPROJECT_CONFIG_DIR}")
print(f"MyProject pipelines directory set to: {SRC_MYPROJECT_PIPELINES_DIR}")




# The logic: We define the constant here
# The config: We pull the actual value from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# If the URL is missing, we can raise a clear error here
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file!")
#--------------------------------------------------
# Example usage:
# from src.constants import TRAIN_DATA_PATH
# import pandas as pd

# df = pd.read_csv(TRAIN_DATA_PATH)
#--------------------------------------------------
# Additional constants can be defined similarly
