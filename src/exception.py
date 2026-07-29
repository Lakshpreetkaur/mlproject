''' Python already provides many toolboxes called MODULES.'''
# sys - build-in python system module and all the functionalities present inside it we can use it so python interperter gets to know that we are using this thing from sys module 
# by default sys will be there in requirements.txt
import sys
from src.logger import logging

# if any error come i want to drop by custom message of exception handling (more details go check this documentation )
# this func will call when ever error comes
def error_message_detail(error,error_detail:sys):
  # exc_info() -> gives three info last one is imp exc_tb
  '''exc_tb ->this will give info about which error occured in which line , file and will be stored in this variable '''

  _,_,exc_tb = error_detail.exc_info()
  file_name = exc_tb.tb_frame.f.code.co_filename
  error_message = "Error occured in python script name[{0}] line number [{1}] error message[{2}]".format(
    file_name.exc_tb.tb_line.no,str(error)) # script name[{0}] line number [{1}] error message[{2}]

  return error_message


class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):  # [ error_detail is of sys type ]
      super().__init__(error_message)
      self.error_message = error_message_detail(error_message,error_detail = error_detail)

    # printing error message
    def __str__(self):
      return self.error_message





  

 


  


  




  