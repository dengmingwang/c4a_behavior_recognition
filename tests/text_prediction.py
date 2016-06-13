# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 11:24:51 2016

@author: aitor
"""

from keras.models import Sequential
from keras.layers.recurrent import LSTM, GRU
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
import numpy as np

WINDOW_SIZE = 1
TRAIN_PER = 0.8

# Create the X and Y secuence vectors based on a window size
# E.G:
# training = [1,2,3,4,5], WINDOW_SIZE = 2 
# X --> [[1, 2], [2, 3], [3, 4]] 
# Y --> [3, 4, 5]
def create_X_Y(samples):
    X = []
    Y = []
    i = 0
    for i in range(len(samples)):
        if i + WINDOW_SIZE >= len(samples):
            break
#        X_sample = samples[i:i+WINDOW_SIZE]
        X_sample = samples[i]
        Y_sample = samples[i+WINDOW_SIZE]
        X.append(X_sample)
        Y.append(Y_sample)
    return X, Y



# *********Create the training and test data
print 'Creating test data...'
lines = []
for l in open('shakespear.txt', 'r'):
    lines.append(l)
text = ''.join(lines)
text = text.lower()
# Get the features (alphabet + other char)
chars = set()
for char in text:
    chars.add(char)
feature_list = list(chars)
# Transform the chars to feature_list vectors. shape = [len(feature_list)] with
# a 1 on the pos of the char in feature_list
vectorized_text = []
for char in text:
    char_repr = [0] * len(feature_list)
    pos = feature_list.index(char)
    char_repr[pos] = 1
    vectorized_text.append(char_repr)
# create the training and text X and Y groups. 
limit = int(TRAIN_PER * len(vectorized_text))
training = vectorized_text[:limit]
evaluation = vectorized_text[limit:]
X_train, Y_train = create_X_Y(training)
print 'Total samples training:', len(training)
print 'Total samples evaluation:', len(evaluation)
print 'Training sets lenght:', len(X_train), len(Y_train)
print 'Sample lenghts train:', set([len(x) for x in X_train]),set([len(x) for x in Y_train])
X_eval, Y_eval = create_X_Y(evaluation)
print 'Evaluation sets lenght:', len(X_eval), len(Y_eval)
print 'Sample lenghts train:', set([len(x) for x in X_eval]),set([len(x) for x in Y_eval])
X_train = np.array(X_train)
Y_train = np.array(Y_train)
X_eval = np.array(X_eval)
Y_eval = np.array(Y_eval)
print 'X_train shape:', X_train.shape
print 'Y_train shape:', Y_train.shape



# Create the model (WINDOW_SIZE, len(feature_list))
print 'Creating model...'
model = Sequential()
model.add(Embedding(X_train.shape[0], len(feature_list), input_length=len(feature_list)))
model.add(LSTM(len(feature_list))) 
model.add(Activation('softmax'))
print 'Training model...'
batch_size = 10
model.compile(optimizer='adam', loss='categorical_crossentropy')
print X_train.shape, Y_train.shape
model.fit(X_train, Y_train, nb_epoch=2, batch_size=batch_size)
print 'Evaluating model...'
score, acc = model.evaluate(X_eval, Y_eval, batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)