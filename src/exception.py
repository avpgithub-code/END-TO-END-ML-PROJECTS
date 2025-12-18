"""
Exception Handling Module for the Application
This module defines a custom exception class that captures detailed
information about exceptions, including the type, message, filename, and line number.
"""
import sys
from src.logger import app_logger
#------------------------------------------------------------------
# Function to generate detailed error messages
#------------------------------------------------------------------
def error_message_detail(exc_type, exc_value, exc_traceback):
    if exc_traceback is not None:
        filename = exc_traceback.tb_frame.f_code.co_filename
        line_number = exc_traceback.tb_lineno
        return f"Exception type: {exc_type.__name__}, Message: {exc_value}, File: {filename}, Line: {line_number}"
    else:
        return f"Exception type: {exc_type.__name__}, Message: {exc_value}"
#------------------------------------------------------------------
# Custom Exception Class
#------------------------------------------------------------------
class CustomException(Exception):
    def __init__(self, exc_type, exc_value, exc_traceback):
        super().__init__(exc_value)
        self.error_message = error_message_detail(exc_type, exc_value, exc_traceback)
        app_logger.error(self.error_message)

    def __str__(self):
        return self.error_message

# if __name__ == "__main__":
#     try:
#         # Example to raise an exception
#         1 / 0
#     except Exception:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         custom_exc = CustomException(exc_type, exc_value, exc_traceback)