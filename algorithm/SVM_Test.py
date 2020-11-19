
import numpy as np
from sklearn.svm import OneClassSVM
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from data_parcing import data_parcing
from SVM import *

dp = data_parcing('dataset')
temp, hum, gas = dp.test_data_convert_format()

data_temp_x, data_temp_y= data_split(temp)

train_temp_x, test_temp_x, train_temp_y, test_temp_y= train_test_split(data_temp_x, data_temp_y, test_size=0.2,
                                                                       random_state=1234, shuffle=False)


model_temp, pred_temp_y= model_ocsvm(train_temp_x, test_temp_x)
test_temp_y = np.array(list(map(int, test_temp_y)))
cnt=0
print("len:", len(pred_temp_y))
for i in range(len(pred_temp_y)):
    if pred_temp_y[i]==-1:
        pred_temp_y[i]=0
        cnt+=1
print("cnt:", cnt)
print(test_temp_y)
print(pred_temp_y)
acc= accuracy_score(test_temp_y, pred_temp_y)

print(acc)
temp1, hum1, gas1= dp.test_data_convert_format()

test_temp_x, test_temp_y= data_split(temp1)

# temp1= np.array(temp1)
# test_data_x= temp1[:, 1].reshape(-1, 1)
# test_data_y= temp1[:, 2]

model_temp, pred_temp= model_ocsvm(train_temp_x, test_temp_x)

print(pred_temp)

cnt1=0
for i in range(len(pred_temp)):
    if pred_temp[i]==1:
        cnt1+=1

print("percent : ", cnt1, len(pred_temp))
test_data_y = np.array(list(map(int, test_temp_y)))
acc1= accuracy_score(test_data_y, pred_temp)
print(acc1)
