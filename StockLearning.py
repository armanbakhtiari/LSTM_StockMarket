from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import csv
import numpy as np

for file_name in ('A_ticker.csv', 'B_ticker.csv', 'C_ticker.csv'):
    temp = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for i in range(0, 9):
                row[i] = float(row[i])
                # Eliminating -1s
                if row[i] == -1:
                    row[i] = row_temp[i]
            row_temp = row
            temp.append(row)

    d = np.array(temp)
    # Normalization
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = scaler.fit_transform(d)

    labels = data[:, 5]
    for p in range(10499):
        labels[p] = labels[p+1]
    # Splitting Train and Test data and labels
    train_data = data[0:8000, 0:9]
    train_labels = labels[0:8000]

    test_data = data[8000:10500, 0:9]
    test_labels = labels[8000:10500]

    # Test labels for 10, 15,...,50 minutes after test time

    temp_labels = test_labels

    test_labels10 = np.zeros(2500)
    for p in range(2499):
        test_labels10[p] = temp_labels[p+1]
    test_labels10[2499] = test_labels10[2498]
    test_labels15 = np.zeros(2500)
    for p in range(2499):
        test_labels15[p] = test_labels10[p+1]
    test_labels15[2499] = test_labels15[2498]
    test_labels20 = np.zeros(2500)
    for p in range(2499):
        test_labels20[p] = test_labels15[p+1]
    test_labels20[2499] = test_labels20[2498]
    test_labels25 = np.zeros(2500)
    for p in range(2499):
        test_labels25[p] = test_labels20[p+1]
    test_labels25[2499] = test_labels25[2498]
    test_labels30 = np.zeros(2500)
    for p in range(2499):
        test_labels30[p] = test_labels25[p+1]
    test_labels30[2499] = test_labels30[2498]
    test_labels35 = np.zeros(2500)
    for p in range(2499):
        test_labels35[p] = test_labels30[p+1]
    test_labels35[2499] = test_labels35[2498]
    test_labels40 = np.zeros(2500)
    for p in range(2499):
        test_labels40[p] = test_labels35[p + 1]
    test_labels40[2499] = test_labels40[2498]
    test_labels45 = np.zeros(2500)
    for p in range(2499):
        test_labels45[p] = test_labels40[p+1]
    test_labels45[2499] = test_labels45[2498]
    test_labels50 = np.zeros(2500)
    for p in range(2499):
        test_labels50[p] = test_labels45[p+1]
    test_labels50[2499] = test_labels50[2498]

    # Reshaping data to suitable format (3d) for learning
    train_data = train_data.reshape((train_data.shape[0], 1, train_data.shape[1]))
    test_data = test_data.reshape((test_data.shape[0], 1, test_data.shape[1]))
    print(train_data.shape, train_labels.shape, test_data.shape, test_labels.shape)
    # defining learning model
    model = Sequential()
    model.add(LSTM(50, input_shape=(train_data.shape[1], train_data.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')
    # fit network
    history = model.fit(train_data, train_labels, epochs=100, batch_size=72, validation_data=(test_data, test_labels), verbose=2, shuffle=False)
    # plot history
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')
    pyplot.legend()
    pyplot.show()

    # Predicting test data
    yhat5 = model.predict(test_data)
    t = d[8000:10500, 0]

    yhat5 = yhat5.reshape(2500)

    # Evaluating and Comparing predicted labels and original lables for test data
    pyplot.plot(t, yhat5*80)
    pyplot.plot(t, test_labels*80)
    pyplot.title('5 minutes later')

    pyplot.show()

    # Predicting prices for other times (10, 15, ...,50 mins from now)

    test_data[0:2500, 0, 5] = yhat5

    yhat10 = model.predict(test_data)
    yhat10 = yhat10.reshape(2500)
    test_data[0:2500, 0, 5] = yhat10

    rmse10 = sqrt(mean_squared_error(yhat10, test_labels10))
    print('Test RMSE: %.3f' % rmse10)
    pyplot.plot(t, yhat10*80)
    pyplot.plot(t, test_labels10*80)
    pyplot.title('10 minutes later')

    pyplot.show()

    yhat15 = model.predict(test_data)
    yhat15 = yhat15.reshape(2500)
    test_data[0:2500, 0, 5] = yhat15

    pyplot.plot(t, yhat15*80)
    pyplot.plot(t, test_labels15*80)
    pyplot.title('15 minutes later')

    pyplot.show()

    yhat20 = model.predict(test_data)
    yhat20 = yhat20.reshape(2500)
    test_data[0:2500, 0, 5] = yhat20

    pyplot.plot(t, yhat20*80)
    pyplot.plot(t, test_labels20*80)
    pyplot.title('20 minutes later')

    pyplot.show()

    yhat25 = model.predict(test_data)
    yhat25 = yhat25.reshape(2500)
    test_data[0:2500, 0, 5] = yhat25

    pyplot.plot(t, yhat25*80)
    pyplot.plot(t, test_labels25*80)
    pyplot.title('25 minutes later')

    pyplot.show()

    yhat30 = model.predict(test_data)
    yhat30 = yhat30.reshape(2500)
    test_data[0:2500, 0, 5] = yhat30

    pyplot.plot(t, yhat30*80)
    pyplot.plot(t, test_labels30*80)
    pyplot.title('30 minutes later')

    pyplot.show()

    yhat35 = model.predict(test_data)
    yhat35 = yhat35.reshape(2500)
    test_data[0:2500, 0, 5] = yhat35

    pyplot.plot(t, yhat35*80)
    pyplot.plot(t, test_labels35*80)
    pyplot.title('35 minutes later')

    pyplot.show()

    yhat40 = model.predict(test_data)
    yhat40 = yhat40.reshape(2500)
    test_data[0:2500, 0, 5] = yhat40

    pyplot.plot(t, yhat40*80)
    pyplot.plot(t, test_labels40*80)
    pyplot.title('40 minutes later')

    pyplot.show()

    yhat45 = model.predict(test_data)
    yhat45 = yhat45.reshape(2500)
    test_data[0:2500, 0, 5] = yhat45

    pyplot.plot(t, yhat45*80)
    pyplot.plot(t, test_labels45*80)
    pyplot.title('45 minutes later')

    pyplot.show()

    yhat50 = model.predict(test_data)
    yhat50 = yhat50.reshape(2500)

    pyplot.plot(t, yhat50*80)
    pyplot.plot(t, test_labels50*80)
    pyplot.title('50 minutes later')
    pyplot.show()

    rmse5 = sqrt(mean_squared_error(yhat5, test_labels))
    print('5 mins later==> Test RMSE: %.7f' % rmse5)

    rmse10 = sqrt(mean_squared_error(yhat10, test_labels10))
    print('10 mins later==> Test RMSE: %.7f' % rmse10)

    rmse15 = sqrt(mean_squared_error(yhat15, test_labels15))
    print('15 mins later==> Test RMSE: %.7f' % rmse15)

    rmse20 = sqrt(mean_squared_error(yhat20, test_labels20))
    print('20 mins later==> Test RMSE: %.7f' % rmse20)

    rmse25 = sqrt(mean_squared_error(yhat25, test_labels25))
    print('25 mins later==> Test RMSE: %.7f' % rmse25)

    rmse30 = sqrt(mean_squared_error(yhat30, test_labels30))
    print('30 mins later==> Test RMSE: %.7f' % rmse30)

    rmse35 = sqrt(mean_squared_error(yhat35, test_labels35))
    print('35 mins later==> Test RMSE: %.7f' % rmse35)

    rmse40 = sqrt(mean_squared_error(yhat40, test_labels40))
    print('40 mins later==> Test RMSE: %.7f' % rmse40)

    rmse45 = sqrt(mean_squared_error(yhat45, test_labels45))
    print('45 mins later==> Test RMSE: %.7f' % rmse45)

    rmse50 = sqrt(mean_squared_error(yhat50, test_labels50))
    print('50 mins later==> Test RMSE: %.7f' % rmse50)

    RMSs = [rmse5, rmse10, rmse15, rmse20, rmse25, rmse30, rmse35, rmse40, rmse45, rmse50]
    pyplot.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], RMSs)
    pyplot.title('RMS rises!')
    pyplot.show()

    print('************** Lets Learn next product!*****************')

