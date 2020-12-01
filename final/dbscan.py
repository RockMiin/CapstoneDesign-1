
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import numpy as np

def get_label(label):
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


def dbscan(temp_list, hum_list, gas_list, label_list):

        
    temp= np.array(temp_list)
    label = []
    hum= np.array(hum_list)
    gas= np.array(gas_list)
    data_temp_y = []
    data_hum_y = []
    data_gas_y = []
    for i in label_list:
        data_label=get_label(i)
        data_temp_y.append(data_label[0])
        data_hum_y.append(data_label[1])
        data_gas_y.append(data_label[2])
    # split data
    # 이때 label을 temp, hum, gas의 label 형태로 변환해줘야함 
    
    data_temp_x= temp.astype(np.float64).reshape(-1, 1)
    data_hum_x= hum.astype(np.float64).reshape(-1, 1)
    data_gas_x= gas.astype(np.float64).reshape(-1, 1)
    

    # create model
    model_temp= DBSCAN(min_samples=10)
    model_hum= DBSCAN(min_samples=10)
    model_gas= DBSCAN(min_samples=10)

    # predict y
    pred_temp_y= model_temp.fit_predict(data_temp_x)
    pred_hum_y= model_temp.fit_predict(data_hum_x)
    pred_gas_y= model_temp.fit_predict(data_gas_x)
    
    pred_temp_y = np.where(pred_temp_y != -1, 0, pred_temp_y)
    pred_temp_y = np.where(pred_temp_y == -1, 1, pred_temp_y)
    
    pred_hum_y = np.where(pred_hum_y != -1, 0, pred_hum_y)
    pred_hum_y = np.where(pred_hum_y == -1, 1, pred_hum_y)
    
    pred_gas_y = np.where(pred_gas_y != -1, 0, pred_gas_y)
    pred_gas_y = np.where(pred_gas_y == -1, 1, pred_gas_y)
    
    unique_temp, counts_temp= np.unique(data_temp_y, return_counts=True)
    unique_hum, counts_hum= np.unique(data_hum_y, return_counts=True)
    unique_gas, counts_gas= np.unique(data_gas_y, return_counts=True)

    unique_temp_pred, counts_temp_pred = np.unique(pred_temp_y, return_counts=True)
    unique_hum_pred, counts_hum_pred = np.unique(pred_hum_y, return_counts=True)
    unique_gas_pred, counts_gas_pred = np.unique(pred_gas_y, return_counts=True)
    
    
    
    print("temp:",dict(zip(unique_temp, counts_temp)), dict(zip(unique_temp_pred, counts_temp_pred)))
    print("hum:",dict(zip(unique_hum, counts_hum)), dict(zip(unique_hum_pred, counts_hum_pred)))
    print("gas:",dict(zip(unique_gas, counts_gas)), dict(zip(unique_gas_pred, counts_gas_pred)))
    
    print('temparature\'s accuracy is:', accuracy_score(data_temp_y, pred_temp_y))
    print('humidity\'s accuracy is:', accuracy_score(data_hum_y, pred_hum_y))
    print('gas\'s accuracy is:', accuracy_score(data_gas_y, pred_gas_y))
    for i in range(40, len(pred_temp_y)):
        temp_label = 0
        if pred_temp_y[i] == 1:
            temp_label += 4 * pred_temp_y[i] 
        if pred_hum_y[i] == 1:
            temp_label += 2 * pred_hum_y[i]
        if pred_gas_y[i] == 1:
            temp_label += 1 * pred_gas_y[i]
        label.append(temp_label)
    
    return label