# ==========================================================
# DATA INGESTION COMPONENT
# Responsibility:
# 1. Read raw data from the source.
# 2. Store a backup copy in the artifacts folder.
# 3. Split the data into training and testing sets.
# 4. Save the split datasets for downstream components.
# ==========================================================


import os     #To Work with folders and file paths. (Create folders ,Join paths,Check files)
import sys    #sys -> Used while handling exceptions (error).
from src.exception import CustomException  # extracting or importing this func from another file whose source or path mentioned
from src.logger import logging
import pandas as pd  # as we need to work with dataframe

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig


# class to save all inputs where to save test ,raw ,train data 
#  All the inputs in data ingestion which is required we will give it to this class

# using DECORATOR - dataclass  -> instead of using __init__ we can directly define our class
@dataclass
class DataIngestionConfig:
  # defining class variable - >all the output will save in artifacts folder and we are giving the path 
  #  giving these inputs to data ingestion component  so that data ingestion knows where to save trainpath , test path
  train_data_path: str=os.path.join('artifacts' , "train.csv")  #train_csv - file name
  test_data_path: str=os.path.join('artifacts' , "test.csv")
  raw_data_path: str=os.path.join('artifacts' , "data.csv")


#  for defining variables only - > dataclass
#  if func are used in class - > use init
class DataIngestion:
    def __init__(self):
      #  ingestion_config will consist of above three values train,test,raw because we need input to intialize
      # when DataIngestion class called the above three path will be saved in this class
      self.ingestion_config = DataIngestionConfig()

    #  to read data from any source when it is saved we made below class
    def initiate_data_ingestion(self):
      logging.info("Entered the data ingestion method or component")
      #  if any error come we can write in partiular manner using try except
      # try and except blocks to handle errors (exceptions) gracefully so that your program does not crash when something goes wrong

      #  1. READ THE DATA FROM ANY SOURCE _ CSV , API , anywhere
      try:
        df = pd.read_csv(os.path.join("notebook", "data", "stud.csv"))
        logging.info('Read the dataset as dataframe')

        os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

        #  here we r doing for csv but same manner we can do it for mongo db or any else also
        df.to_csv(self.ingestion_config.raw_data_path,index = False,header=True)

        logging.info("Train Test split initiated")
        train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

        train_set.to_csv(self.ingestion_config.train_data_path,index = False,header=True)

        test_set.to_csv(self.ingestion_config.test_data_path,index = False,header=True)

        logging.info("Ingestion of the data is completed")

        return(
          self.ingestion_config.train_data_path,
          self.ingestion_config.test_data_path

        )
      except Exception as e:
        raise CustomException(e,sys)

#  combined data ingestion and data transformation
if __name__ =="__main__":
  obj=DataIngestion()
  train_data , test_data = obj.initiate_data_ingestion()


  data_transformation = DataTransformation()
  data_transformation.intiate_data_transformation(train_data,test_data)

