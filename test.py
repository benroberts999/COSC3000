#!/usr/bin/env python3

filename = "data.dat"

file1 = open(filename,"r")

# print(file1)

contents = file1.read()

# print(file1.read())

# Normally, imports go at the top of the file
# But I want to deonstrate what import is required for each step
import numpy as np

# Read file as 2D (x,y) array - sometimes useful, sometimes not
xy_data = np.loadtxt(filename)

# We can read each column one-by-one
x_data = np.loadtxt(filename, usecols=0)
y_data = np.loadtxt(filename, usecols=1)

# note: for *very* large input files, this might be too slow
# since it reads through the file twice.

# print(xy_data)
# print(x_data)
# print(y_data)

# We can also extract the x and y parts of the xy array:
# If we have huge data files, we want to avoid needless copies,
# but this also works:
x_data_2 = xy_data[:,0]
y_data_2 = xy_data[:,1]


from matplotlib import pyplot as plt

plt.title('Example: plot of function')
plt.xlabel('variable (units)')
plt.ylabel('function (units)')


plt.plot(x_data, y_data, 'r-', label = "function")
plt.plot(x_data, y_data*(1.25), 'k--', label = "error")
plt.plot(x_data, y_data*(0.75), 'k--')
plt.legend()

plt.show()