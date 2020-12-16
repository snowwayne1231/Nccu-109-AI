import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.__version__)

dataset = pd.read_csv('task1.training.csv')

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
        self.train = train_dataset
        self.test = test_dataset


    def build_model(self):
        pass
