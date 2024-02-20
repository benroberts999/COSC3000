#!/usr/bin/env python3
import numpy as np
import pickle as pkl

# requires: pip install pickle5

pkl_filename = "data.pkl"

# Generate x/y data as before
x = np.linspace(0.0, 2 * np.pi, 25)
y = np.cos(x)
xy_data = np.column_stack((x, y))

with open(pkl_filename, "wb") as file:
    pkl.dump(xy_data, file)

# The "pickle" file is slightly larger than the raw binary.
# But it knows about python data structures.
# If you're exclusively inside python, it's a great choice, but not portable.


# Extract the "pickle" simply
with open(pkl_filename, "rb") as file:
    xy_data_in = pkl.load(file)

print(xy_data_in - xy_data)
