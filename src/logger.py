# log any kind of exceptions into a file  in order to track if any error comes
import logging
import os 
from datetime import datetime 

# log file (txt file ) will be created with this naming convention
# the file will be created in this source directory with naming convention
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)


LOG_FILE_Path = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
  filename = LOG_FILE_Path,
  format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
  level = logging.INFO,

)

