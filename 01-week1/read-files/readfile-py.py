#!/usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt

""" 
Example python script for reading simple white-spaced delimitered file
into a numpy array, and plotting it.
"""

filename = "data.dat"

# read the file into a "file" object
file1 = open(filename, "r")

# and extract the contents as a string (don't often actually need this)
contents = file1.read()

# -------------------

# We usually load the data from a text file directly into an array

# Read file as 2D (x,y) array - sometimes useful, sometimes not
xy_data = np.genfromtxt(filename)

# We can also extract the x and y parts of the xy array:
# If we have huge data files, we want to avoid needless copies,
# but this also works:
x_data_2 = xy_data[:, 0]
y_data_2 = xy_data[:, 1]

# We can also read each column one-by-one
x_data = np.genfromtxt(filename, usecols=0)
y_data = np.genfromtxt(filename, usecols=1)

# Full documentation:
# https://numpy.org/doc/stable/reference/generated/numpy.genfromtxt.html
# The 'loadtxt' function is similar, but is a little less advanced
# https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html

# Example: plot the data
plt.title("Example: plot of function")
plt.xlabel("variable (units)")
plt.ylabel("function (units)")
plt.plot(x_data, y_data, "r-", label="function")
plt.plot(x_data, y_data * (1.25), "k--", label="error")
plt.plot(x_data, y_data * (0.75), "k--")
plt.legend()

# This saves the current plot (Get Current Figure), so we can show, then save
fig = plt.gcf()
fig.savefig("python.png")

# This works too, but also 'resets' the plt figure
# plt.savefig("python.png")

plt.show()
