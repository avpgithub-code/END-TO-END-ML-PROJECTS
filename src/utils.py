import os

def ensure_directory_exists(directory_path):
    """Checks if a directory exists, and creates it if necessary."""
    if not os.path.exists(directory_path):
        # Creates the directory and any necessary parent directories
        os.makedirs(directory_path, exist_ok=True)
        print(f"Created directory: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")