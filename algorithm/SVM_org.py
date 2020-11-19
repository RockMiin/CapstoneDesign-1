
import numpy as np
from sklearn.svm import OneClassSVM
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from data_parcing import data_parcing
from SVM import *

dp = data_parcing('dataset')
temp, hum, gas = dp.test_data_convert_format()

temp= np.array(temp)
data_temp_x= temp[:, 1].reshape(-1, 1)
data_temp_y= temp[:, 2]

data_temp_x, data_temp_y = data_split(temp)

train_temp_x, test_temp_x, train_temp_y, test_temp_y= train_test_split(data_temp_x, data_temp_y, test_size=0.3,
                                                                       random_state=123, shuffle=True)

model_temp= OneClassSVM(gamma='auto', kernel="linear")
model_temp.fit(train_temp_x)
pred_temp_y=model_temp.predict(test_temp_x)

cnt=0
print("len:", len(pred_temp_y))
for i in range(len(pred_temp_y)):
    if pred_temp_y[i]==-1:
        pred_temp_y[i]=0
        cnt+=1
print("cnt:", cnt)

test_temp_y = np.array(list(map(int, test_temp_y)))
acc= accuracy_score(test_temp_y, pred_temp_y)

# test_temp_y=np.array(test_temp_y)
print(test_temp_y)
print(pred_temp_y)
print('accuracy is ', acc)

temp1, hum1, gas1= dp.test_data_convert_format()
temp1= np.array(temp1)
test_data_x= temp1[:, 1].reshape(-1, 1)
test_data_y= temp1[:, 2]
print(test_data_y)
pred_test_y1= model_temp.predict(test_data_x)
print(pred_test_y1)

cnt1 = 0
for i in range(len(pred_test_y1)):
    if pred_test_y1[i]==-1:
        pred_test_y1[i]=0;
        cnt1+=1
cnt2=0
# for i in range(len(test_data_y)):
#     if test_data_y[i] ==1:
#         cnt2+=1
print("percent {} / {} = {} ".format(cnt1, len(pred_test_y1), cnt1/len(pred_test_y1)) )
test_data_y = np.array(list(map(int, test_data_y)))
acc1 = accuracy_score(test_data_y, pred_test_y1)
print('test accuracy is ', acc1)