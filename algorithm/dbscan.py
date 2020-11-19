from SVM import *
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
dp = data_parcing('dataset')
temp, hum, gas = dp.test_data_convert_format()

temp= np.array(gas)
data_temp_x= temp[:, 1].reshape(-1, 1)
data_temp_y= temp[:, 2]
unique, counts = np.unique(data_temp_y, return_counts=True)

model_temp= DBSCAN(min_samples=10)
pred_temp_y=model_temp.fit_predict(data_temp_x)

print(dict(zip(unique, counts)))
unique, counts = np.unique(pred_temp_y, return_counts=True)
print(dict(zip(unique, counts)))

x= np.arange(len(pred_temp_y))
plt.scatter(x, pred_temp_y)
plt.show()

