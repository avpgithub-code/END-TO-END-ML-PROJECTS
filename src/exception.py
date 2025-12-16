#------------------------------------------------------------------
# Exception Handling Module for the Application
#------------------------------------------------------------------
import sys
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

    def __str__(self):
        return self.error_message