import os
import glob
import pandas as pd
import numpy as np

class data_parcing:

    def __init__(self, DATA_PATH):
        self.path = DATA_PATH


    def get_all_content_list(self, input_path):
        """get all contents in the directory"""
        return glob.glob(os.path.join(input_path, "*"))

    def parsing_file_name(self, file_name):
        

        splited_file_name = file_name.split(" ")
        date = splited_file_name[0]

        return date

    def print_content_list(self, dir_list):
       
        cnt = 1
        for dir_name in dir_list:
            print("{}. {}".format(cnt, dir_name))
            cnt += 1
    def get_label(self, label):
      '''This method helps getting labels from decimal number to binary 
         if gas data is abnormal data, decimal number is 1 so converting to binary result is 001 
      '''
      if label == 0:
        transformed_label = [0,0,0]
      elif label == 1:
        transformed_label = [0,0,1]
      elif label == 2:
        transformed_label = [0,1,0]
      elif label == 3:
        transformed_label = [0,1,1]
      elif label == 4:
        transformed_label = [1,0,0]
      elif label == 5:
        transformed_label = [1,0,1]
      elif label == 6:
        transformed_label = [1,1,0]
      elif label == 7:
        transformed_label = [1,1,1]
      
      return transformed_label
      
    def test_data_convert_format(self):
        '''this method's role is converting sensor data to learning data'''
        file_list = self.get_all_content_list(self.path)
       
        self.print_content_list(file_list)
        content_num = int(input("select number you want:"))
       
        file_name = file_list[content_num - 1]
        
        temparature = list()
      
        humidity = list()
        
        gas = list()
        
        label = list()
       
        date = self.parsing_file_name(file_name)
      
        IOT_data = pd.read_csv(file_name)
        for i in range(len(IOT_data)):
            temp_data = IOT_data.iloc[i]
            label = self.get_label(temp_data['LABEL'])
            temparature.append( [temp_data['TEMP'], label[0]])
            humidity.append( [temp_data['HUM'], label[1]])
            gas.append([temp_data['LPG'], label[2]])
        
        return temparature, humidity, gas
 
if __name__ == "__main__":
  
  data_path = '/home/samlon09/socketTest/'
  dp = data_parcing(data_path)
  temp, hum, gas = dp.test_data_convert_format()
  

