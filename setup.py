#-----------------------------------------------------
# setup.py
#-----------------------------------------------------
from setuptools import setup, find_packages
from typing import List
#-----------------------------------------------------
# Constant for editable install marker
#-----------------------------------------------------
HYPENATE = '-e .'
#-----------------------------------------------------
# Function to read requirements from a file and return requirements as a list
#-----------------------------------------------------
def get_requirements(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        requirements = file.readlines()
    return [req.strip() for req in requirements if req.strip() \
            and not req.startswith('#') and req.strip() != HYPENATE]
#-----------------------------------------------------
# Package configuration
#-----------------------------------------------------
setup(
    name="ml_project",
    version="0.1",
    author="Archit Pandya",
    author_email="architpandya@yahoo.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)