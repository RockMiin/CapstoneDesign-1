from data_parcing import data_parcing

import numpy as np
import pandas as pd

from sklearn.svm import OneClassSVM
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def data_split(data):
    data= np.array(data)
    data_x= data[:, 1].reshape(-1, 1)
    data_y= data[:, 2]

    return data_x, data_y

def model_ocsvm(train_x, test_x):
    model= OneClassSVM(gamma='auto', kernel='linear')
    model.fit(train_x)
    pred= model.predict(test_x)
    return model, pred


