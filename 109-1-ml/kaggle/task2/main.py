import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import os, csv

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.__version__)

PATH_MODEL = './saved_model.h5'
PATH_RESULT_CSV = './result.submission.csv'

PATH_TRAINING_DATA = './task2.training.csv'
PATH_TEST_DATA = './task2.test.withOUT.answers.csv'



dataset = pd.read_csv(PATH_TRAINING_DATA)
dataset_submission = pd.read_csv(PATH_TEST_DATA)

train_dataset = dataset.sample(frac=0.6, random_state=0)
test_dataset = dataset.drop(train_dataset.index)



class TFModel():
    """
    """
    train = []
    test = []
    model = None
    NUM_FEATURE = 16
    NUM_RESULT_CLASS = 6

    class_index_map = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5
    }

    def __init__(self, train_dataset, test_dataset, debug=False):
        self.train = train_dataset.to_numpy()
        self.test = test_dataset.to_numpy()
        self.build_model(debug=debug)


    def build_model(self, debug=False):

        def logistic_regression(x):
    
            # Apply softmax to normalize the logits to a probability distribution.

            return tf.nn.softmax(tf.matmul(x, W) + b)
        
        if os.path.isfile(PATH_MODEL) and debug is False:
            _model = tf.keras.models.load_model(PATH_MODEL)
        else:
            _model = tf.keras.Sequential([
                layers.Dense(self.NUM_FEATURE, input_shape=(self.NUM_FEATURE,), activation="relu"),
                layers.Dense(self.NUM_FEATURE * self.NUM_RESULT_CLASS, activation="relu"),
                layers.Dense(self.NUM_RESULT_CLASS, activation='softmax'),
            ])
            
            _model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer=tf.optimizers.Adam(learning_rate=0.001), metrics=['accuracy'])
            # _model.compile(
            #     loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=yhat, labels=Y)),
            #     optimizer=tf.keras.optimizers.SGD(learning_rate=0.01, nesterov=False, name='SGD'),
            #     metrics=['accuracy'])

        _model.summary()
        
        self.model = _model

    
    def get_labels(self, nparray):
        _list = []
        _num_zero = self.NUM_RESULT_CLASS
        _class_index_map = self.class_index_map
        for _ in nparray:
            _new_array = np.zeros(_num_zero)
            _idx = _class_index_map.get(_)
            _new_array[_idx] = 1
            _list.append(_new_array)

        labels = np.array(_list, dtype=int)
        return labels



    def fit(self):
        x_train = self.train[:, 0:self.NUM_FEATURE].astype(np.float64)
        y_train = self.get_labels(self.train[:, self.NUM_FEATURE])

        x_test = self.test[:, 0:self.NUM_FEATURE].astype(np.float64)
        y_test = self.get_labels(self.test[:, self.NUM_FEATURE])

        # print('fit x_train length: ', len(x_train))
        # print(x_train.shape)
        # print(x_test.shape)
        # print('================================')
        # print(y_train.shape)
        # print(y_test.shape)
        # exit(2)

        history = self.model.fit(
            x_train,
            y_train,
            epochs=100,
            # suppress logging
            verbose=2,
            # Calculate validation results on 30% of the training data
            validation_split = 0.3,
            validation_data=(x_test, y_test),
        )

        self.model.save(PATH_MODEL)

        return history


    def predict(self, dataset):
        _model = self.model
        _array = dataset.to_numpy()
        features = _array[:, 0:self.NUM_FEATURE]
        res = _model.predict(features)
        map_list = ['A', 'B', 'C', 'D', 'E', 'F']
        res = [map_list[np.argmax(_)] for _ in res]
        return res



MODEL = TFModel(train_dataset=train_dataset, test_dataset=test_dataset, debug=False)
# MODEL = TFModel(train_dataset=dataset, test_dataset=dataset)
MODEL.fit()

result = MODEL.predict(dataset_submission)
# print(result[:10])

with open(PATH_RESULT_CSV, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'Predicted'])
    _id = 1
    for r in result:
        writer.writerow([_id, r])
        _id += 1