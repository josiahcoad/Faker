# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 18:34:02 2017

@author: Sheel
"""
# Self Organization map
# For fraud detection
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Credit_Card_Applications.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values # We are ding this just to see if the customer was approved or not
                               # This is not for supervised learning

# Feature scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
X = sc.fit_transform(X)

# Training the SOM
# We will use MiniSom 1.0
from minisom import MiniSom
som = MiniSom(x = 10, y = 10, input_len = 15, sigma = 1.0, learning_rate = 0.5)
som.random_weights_init(X)
som.train_random(data = X, num_iteration = 100)

# Visualizing the results
from pylab import bone, pcolor, colorbar, plot, show
bone() # creates a white window
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']

for i,x in enumerate(X):
    # i - index f the customers, x - vector of each customer
    w = som.winner(x)
    plot(w[0] + 0.5,
         w[1] + 0.5,
         markers[y[i]],
         markeredgecolor = colors[y[i]],
         markerfacecolor = 'None',
         markersize = 10,
         markeredgewidth = 2)
show()

# Finding the frauds
# to find the inverse mapping rom the coordiantes to the customer
# we use a dictionary for this purpose
mappings = som.win_map(X)   # this gives the scaled value of the features of each customer
frauds = np.concatenate((mappings[(4,3)], mappings[(2,2)]), axis = 0)
frauds = sc.inverse_transform(frauds)