#!/usr/bin/env python3
import numpy as np
import pickle as pkl

# requires: pip install pickle5

filename = "data.dat"

pkl_filename = "data.pkl"

# As a start, read in the same example data from from before
xy_data = np.genfromtxt(filename)

# Just to make the numbers not round, multiply by pi:
xy_data *= np.pi

with open(pkl_filename, "wb") as file:
    pkl.dump(xy_data, file)

# The "pickle" file is slightly larger than the raw binary.
# But it knows about python data structures.
# If you're exclusively inside python, it's a great choice, but not portable.


# Extract the "pickle" simply
with open(pkl_filename, "rb") as file:
    xy_data_in = pkl.load(file)

print(xy_data_in - xy_data)
