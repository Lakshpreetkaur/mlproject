#  Data cleaning  ,  Feature Enginnering  
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd 

# Column Transformer -> use to create pipeline (OHE , Standard scaling ....)
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

#  exception why ? -> To handle Exceptions in data transformation file also 
from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object 

# Config ? -> any input we require in Data Transformation pipeline  it will provide us so we made this class
@dataclass
class DataTransformationConfig:
  # why ? -> to save any model in pickle file so we require a path in which we want to save 
  preprocessor_obj_file_path = os.path.join('artifacts' , "preprocessor.pkl")

class DataTransformation:
  # proving input path 
  def __init__(self):
    self.data_transformation_config = DataTransformationConfig()


  # to make all pickle filewhich are responsible to perform task - numerical -> categorical 
  def get_data_transformer_object(self):
    '''
    This Function is responsible fro data transformation 

    '''

    try:
      numerical_columns = ["writing_score" , "reading_score"]
      categorical_columns = ["gender" , "race_ethnicity" , "parental_level_of_education" , "lunch" , "test_preparation_course"]

      #   2 task to perform -> create pipeline , handle missing values
      
      # 1. Creating Numerical Pipeline  for Training data
      num_pipeline = Pipeline(
        #  steps to follow in this pipeline 
        #  Task :- handle missing values , scaling 
        steps =[
          ("imputer" , SimpleImputer(strategy="median")),   # imputer -> To Handle Missing Values  , median -> To Handle Outliers
          ("scaler" , StandardScaler())      # for scaling  - StandardScaling
        ]
      )

      # 2. Creating Categorical Pipeline
      cat_pipeline = Pipeline(
        # Task -: missing values , categorical- numerical 
        steps = [
          ("imputer" , SimpleImputer(strategy = "most_frequent")),  # Handle missing value  and replacing missing values with mode(most_frequent) 
          ("one_hot_encoder" , OneHotEncoder()),
          ("scaler" , StandardScaler(with_mean=False)),
        ]
      )

      logging.info(f"Numerical columns: {numerical_columns}")

      logging.info(f"Categorical columns: {categorical_columns}")


      #  Combining numerical and categorical pipeline together

      preprocessor = ColumnTransformer(
        [
          # pipeline_name , what pipeline used , where to use(columns) 
          ("num_pipeline" , num_pipeline , numerical_columns),  # num_pipeline using for numerical_columns 
          ("cat_pipeline" , cat_pipeline , categorical_columns),
        ]
      )

      return preprocessor

      
    except Exception as e:
      raise CustomException(e,sys)



  def initiate_data_transformation(self,train_path,test_path):  # getting these train , test path from data ingestion 

    try:
      # reading training ,testing dataset
      train_df = pd.read_csv(train_path)
      test_df = pd.read_csv(test_path)

      logging.info("Read train and test data completed")

      logging.info("Obtaining preprocessing object")

      preprocessing_obj = self.get_data_transformer_object()

      target_column_name="math_score"
      numerical_columns = ["writing_score", "reading_score"]

      input_feature_train_df = train_df.drop(columns = [target_column_name] , axis = 1)
      target_feature_train_df = train_df[target_column_name]

      input_feature_test_df = test_df.drop(columns = [target_column_name] , axis = 1)
      target_feature_test_df = test_df[target_column_name]

      logging.info(
        f"Applyinng preprocessing object on training dataframe and testing dataframe."
      )

      input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
      input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

      train_arr = np.c_[
        input_feature_train_arr , np.array(target_feature_train_df)
      ]

      test_arr = np.c_[
              input_feature_test_arr , np.array(target_feature_test_df)
      ]

      logging.info(f"Saved Preprocessing object.")

      # saving pickle file in hard disk 
      save_object(

        file_path  =self.data_transformation_config.preprocessor_obj_file_path,
        obj = preprocessing_obj

      )


      return (
        train_arr,
        test_arr,
        self.data_transformation_config.preprocessor_obj_file_path,
      )

    except Exception as e:
      raise CustomException(e,sys)