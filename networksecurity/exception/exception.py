import sys
from networksecurity.logging.logger import logging

class NetworkSecurityException(Exception):

    def __init__(self, error_message, error_detail: sys):
        self.error_message = error_message
        _,_,exc_tb = error_detail.exc_info()

        self.line_no = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python script name {self.file_name} --> line number {self.line_no} --> error message {self.error_message}"

'''
if __name__ == '__main__':
    try:
        a = 1/0
    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(e, sys)'''