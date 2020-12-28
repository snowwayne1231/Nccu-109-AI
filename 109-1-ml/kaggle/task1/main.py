import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, csv

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.__version__)

PATH_MODEL = './saved_model.h5'
PATH_RESULT_CSV = './result.submission.csv'

dataset = pd.read_csv('task1.training.csv')
dataset_submission = pd.read_csv('task1.test.csv')

train_dataset = dataset.sample(frac=0.6, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# sns.pairplot(train_dataset[['f0', 'f1', 'f2', 'target']], diag_kind='kde')

print('train_dataset: ', train_dataset)
print('train_dataset.index: ', train_dataset.index)



class LinearRegresionModel():
    """
    """
    train = []
    test = []
    model = None

    def __init__(self, train_dataset, test_dataset):
        self.train = train_dataset.to_numpy()
        self.test = test_dataset.to_numpy()
        self.build_model()


    def build_model(self):
        
        if os.path.isfile(PATH_MODEL):
            _model = tf.keras.models.load_model(PATH_MODEL)
        else:
            _model = tf.keras.Sequential([
                layers.Dense(16, input_shape=(10,), activation="relu"),
                layers.Dense(32, activation="relu"),
                layers.Dense(1),
            ])
            # mse  mean_absolute_error
            _model.compile(loss="mse", optimizer=tf.optimizers.Adam(learning_rate=0.00001), metrics=[keras.metrics.RootMeanSquaredError(name='rmse')])

        _model.summary()
        
        self.model = _model


    def fit(self):
        x_train = self.train[:, 0:10]
        y_train = self.train[:, 10]

        x_test = self.test[:, 0:10]
        y_test = self.test[:, 10]

        print('fit x_train length: ', len(x_train))

        history = self.model.fit(
            x_train,
            y_train,
            epochs=200,
            # suppress logging
            verbose=2,
            # Calculate validation results on 20% of the training data
            validation_split = 0.2,
            validation_data=(x_test, y_test),
        )

        self.model.save(PATH_MODEL)

        return history


    def predict(self, dataset):
        _model = self.model
        _array = dataset.to_numpy()
        features = _array[:, 0:10]
        res = _model.predict(features).flatten()
        
        return res



LRM = LinearRegresionModel(train_dataset=train_dataset, test_dataset=test_dataset)
# LRM = LinearRegresionModel(train_dataset=dataset, test_dataset=dataset)
LRM.fit()

result = LRM.predict(dataset_submission)
print(result[:10])

with open(PATH_RESULT_CSV, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'Predicted'])
    _id = 1
    for r in result:
        writer.writerow([_id, r])
        _id += 1