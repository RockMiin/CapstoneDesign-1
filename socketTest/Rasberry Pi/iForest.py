import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn.svm import OneClassSVM
from sklearn.metrics import accuracy_score
from sklearn.ensemble import IsolationForest
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split

def plot_scatter():

    fd_normal = open('result/sensorValue_normal.csv', 'r', encoding='utf-8-sig')
    fd_anomaly = open('result/sensorValue_anomaly.csv', 'r', encoding='utf-8-sig')

    normal_reader = csv.reader(fd_normal)
    anomaly_reader = csv.reader(fd_anomaly)

    X_normal = list(normal_reader)
    X_anomaly = list(anomaly_reader)
    X_normal = np.array(X_normal)[:, 1:].astype("float32")
    X_anomaly = np.array(X_anomaly)[:, 1:].astype("float32")

    fd_normal.close()
    fd_anomaly.close()

    plt.figure(figsize=(8, 6))
    plt.xlim(0, 1500)
    plt.ylim(0, 1500)
    plt.xlabel("Moisture sensor value")
    plt.ylabel("Light sensor value")
    plt.grid(axis='both', linestyle='--', linewidth=0.4)

    plt.scatter(X_normal[:, 0], X_normal[:, 1], color='0.75', edgecolors='b', label='Normal')
    plt.scatter(X_anomaly[:, 0], X_anomaly[:, 1], color='1', edgecolors='r',  marker='^', label='Anomaly')

    plt.legend(loc='upper right')

    plt.savefig("Raspberry Pi Sensor")

    plt.show()




def iFoest():

    fd_normal = open('result/sensorValue_normal.csv', 'r', encoding='utf-8-sig')
    fd_anomaly = open('result/sensorValue_anomaly.csv', 'r', encoding='utf-8-sig')

    normal_reader = csv.reader(fd_normal)
    anomaly_reader = csv.reader(fd_anomaly)

    X_normal = list(normal_reader)
    X_anomaly = list(anomaly_reader)
    X_normal = np.array(X_normal)
    X_anomaly = np.array(X_anomaly)

    Y_normal = X_normal[:, 0].astype("int32")
    X_normal = X_normal[:, 1:].astype("float32")

    Y_anomaly = X_anomaly[:, 0].astype("int32")
    X_anomaly = X_anomaly[:, 1:].astype("float32")

    fd_normal.close()
    fd_anomaly.close()

    X_train, X_test, y_train, y_test = train_test_split(X_normal, Y_normal, train_size=0.8)

    clf = IsolationForest(n_estimators=200, contamination=0.05, random_state=10)
    clf.fit(X_train)

    train_pred = clf.predict(X_train)
    test_pred = clf.predict(X_test)
    anomaly_pred = clf.predict(X_anomaly)

    print("Train acc : %.3f" % accuracy_score(y_train, train_pred))
    print("Test acc : %.3f" % accuracy_score(y_test, test_pred))
    print("----------------------------------------------------------------------------")
    print("Anomaly Detection Accuracy : %.3f" % accuracy_score(Y_anomaly, anomaly_pred))


def OCSVM():

    fd_normal = open('result/sensorValue_normal.csv', 'r', encoding='utf-8-sig')
    fd_anomaly = open('result/sensorValue_anomaly.csv', 'r', encoding='utf-8-sig')

    normal_reader = csv.reader(fd_normal)
    anomaly_reader = csv.reader(fd_anomaly)

    X_normal = list(normal_reader)
    X_anomaly = list(anomaly_reader)
    X_normal = np.array(X_normal)
    X_anomaly = np.array(X_anomaly)

    Y_normal = X_normal[:, 0].astype("int32")
    X_normal = X_normal[:, 1:].astype("float32")

    Y_anomaly = X_anomaly[:, 0].astype("int32")
    X_anomaly = X_anomaly[:, 1:].astype("float32")

    fd_normal.close()
    fd_anomaly.close()

    X_train, X_test, y_train, y_test = train_test_split(X_normal, Y_normal, train_size=0.8)


    clf = OneClassSVM(kernel='rbf', gamma=0.00001, nu=0.09)
    clf.fit(X_train)

    train_pred = clf.predict(X_train)
    test_pred = clf.predict(X_test)
    anomaly_pred = clf.predict(X_anomaly)

    print("Train acc : %.3f" % accuracy_score(y_train, train_pred))
    print("Test acc : %.3f" % accuracy_score(y_test, test_pred))
    print("----------------------------------------------------------------------------")
    print("Anomaly Detection Accuracy : %.3f" % accuracy_score(Y_anomaly, anomaly_pred))

    X = np.vstack([X_normal, X_anomaly])
    Y = np.hstack([Y_normal, Y_anomaly])
    # print(X_normal.shape, X_anomaly.shape)

    plot_decision_regions(X, Y, clf)

    plt.show()


def plot_decision_regions(X, y, classifier, test_idx=None, resolution=3):

    # setup marker generator and color map
    markers = ('^', 'o')
    colors = ('red', 'blue')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    # x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    # x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(0, 1500, resolution),
                           np.arange(0, 1500, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)

    plt.figure(figsize=(8, 6))
    plt.xlabel("Moisture sensor value")
    plt.ylabel("Light sensor value")
    plt.grid(axis='both', linestyle='--', linewidth=0.4)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(0, 1500)
    plt.ylim(0, 1500)

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], color='0.75', edgecolors=colors[idx], marker=markers[idx], label=cl)


    # highlight test samples
    if test_idx:
        # plot all samples
        if not versiontuple(np.__version__) >= versiontuple('1.9.0'):
            X_test, y_test = X[list(test_idx), :], y[list(test_idx)]
            warnings.warn('Please update to NumPy 1.9.0 or newer')
        else:
            X_test, y_test = X[test_idx, :], y[test_idx]

        plt.scatter(X_test[:, 0],
                    X_test[:, 1],
                    c='',
                    alpha=1.0,
                    linewidths=1,
                    marker='o',
                    s=55, label='test set')


def versiontuple(v):
    return tuple(map(int, (v.split("."))))

if __name__ == "__main__":
    OCSVM()
    # plot_scatter()
    # iFoest()