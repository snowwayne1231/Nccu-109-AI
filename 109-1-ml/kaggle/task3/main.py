import numpy as np
import tensorflow as tf
import pandas as pd
import os, csv

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.__version__)

PATH_MODEL = './saved_model.h5'
PATH_RESULT_CSV = './result.submission.csv'

PATH_TRAINING_DATA = './task3.training.csv'
PATH_TEST_DATA = './task3.test.withOUT.answers.csv'



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
    NUM_FEATURE = 23
    NUM_RESULT_CLASS = 10

    class_index_map = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7,
        'I': 8,
        'J': 9,
    }

    def __init__(self, train_dataset, test_dataset, debug=False):
        self.train = train_dataset.to_numpy()
        self.test = test_dataset.to_numpy()
        self.build_model(debug=debug)


    def build_model(self, debug=False):
        
        if os.path.isfile(PATH_MODEL) and debug is False:
            _model = tf.keras.models.load_model(PATH_MODEL)
        else:
            _model = tf.keras.Sequential([
                layers.Dense(self.NUM_FEATURE, input_shape=(self.NUM_FEATURE,)),
                # layers.Dense(self.NUM_FEATURE * self.NUM_RESULT_CLASS, activation='relu'),
                layers.Dense(self.NUM_RESULT_CLASS, activation='softmax'),
            ])
            
            _model.compile(
                loss='categorical_crossentropy',
                optimizer=tf.optimizers.Adam(learning_rate=0.001),  # 0.9764
                # optimizer=tf.optimizers.SGD(learning_rate=0.001, name="SGD"),  # 0.917
                # optimizer= tf.optimizers.lbfgs_minimize(tolerance=0.000001, max_iterations=5000, name='lbfgs'),
                metrics=['accuracy']
            )
            

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

        print('fit x_train length: ', len(x_train))
        print(x_train.shape)
        print(x_test.shape)
        print('================================')
        print(y_train.shape)
        print(y_test.shape)
        # exit(2)

        while (True):
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
            if max(history.history['accuracy']) > 0.99:
                break

        return history


    def predict(self, dataset):
        _model = self.model
        _array = dataset.to_numpy()
        features = _array[:, 0:self.NUM_FEATURE]
        res = _model.predict(features)
        map_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
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