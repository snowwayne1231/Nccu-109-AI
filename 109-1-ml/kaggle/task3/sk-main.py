
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.neural_network import MLPClassifier

import pandas as pd
import numpy as np
import os, csv


PATH_RESULT_CSV = './result.submission.csv'

PATH_TRAINING_DATA = './task3.training.csv'
PATH_TEST_DATA = './task3.test.withOUT.answers.csv'


dataset = pd.read_csv(PATH_TRAINING_DATA)
dataset_submission = pd.read_csv(PATH_TEST_DATA)

train_dataset = dataset
test_dataset = dataset.sample(frac=0.5, random_state=0)

features_train = train_dataset.iloc[:, 0:23]
classes_train = train_dataset.iloc[:, 23]

features_test = test_dataset.iloc[:, 0:23]
classes_test = test_dataset.iloc[:, 23]

print(features_train[:5])
print(classes_train[:5])


# clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(16, 6), random_state=1, max_iter=5000)
# clf.fit(features_train, ont_hoted_classes)



clf = linear_model.LogisticRegression(
    tol=0.000000001,
    random_state=0,
    solver='lbfgs',
    max_iter=15000,
    multi_class='multinomial',
)


# clf = MLPClassifier(
#     solver='lbfgs',
#     activation='relu',
#     alpha=1e-6,
#     hidden_layer_sizes=(23,),
#     random_state=0,
#     max_iter=500000,
#     tol＝0.000001,
# )



clf.fit(features_train, classes_train)


predicted = clf.predict(features_test)
predicted_trained = clf.predict(features_train)

print(predicted)
print(predicted_trained)
# 0.9836

accuracy = accuracy_score(classes_test, predicted)
print(accuracy)

accuracy_trained = accuracy_score(classes_train, predicted_trained)
print(accuracy_trained)

# exit(2)




result = clf.predict(dataset_submission.iloc[:, 0:23])

with open(PATH_RESULT_CSV, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'Predicted'])
    _id = 1
    for r in result:
        writer.writerow([_id, r])
        _id += 1