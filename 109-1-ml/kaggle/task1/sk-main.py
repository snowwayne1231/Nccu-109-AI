# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import os, csv

PATH_RESULT_CSV = './result.submission.csv'

dataset = pd.read_csv('task1.training.csv')
dataset_submission = pd.read_csv('task1.test.csv')

train_dataset = dataset.sample(frac=0.6, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

def get_xy_by_dataset(dataset):
      x = dataset.to_numpy()[:, 0:10]
      y = dataset.to_numpy()[:, 10]
      return x, y

xx, yy = get_xy_by_dataset(dataset)

regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(xx, yy)


y_pred = regr.predict(xx)
# y_pred_rounded = np.array([round(_, 4) for _ in y_pred])


rmse = mean_squared_error(yy, y_pred, squared=False)
print('rmse: ', rmse)


# def rmse(predictions, targets):
#     return np.sqrt(((predictions - targets) ** 2).mean())

subm_x = dataset_submission.to_numpy()[:, 0:10]
subm_y = regr.predict(subm_x)

with open(PATH_RESULT_CSV, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'Predicted'])
    _id = 1
    for r in subm_y:
        writer.writerow([_id, r])
        _id += 1

