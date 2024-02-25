#!/usr/bin/env python3
import numpy as np

txt_filename = "data.text"
bin_filename = "data.binary"
bin_filename2 = "data.binary2"

# Generate x data: linearly spaced list, from 0 to 2Pi in 100 points
x = np.linspace(0.0, 2 * np.pi, 25)

# Generate y data: cosine of the x-data
y = np.cos(x)

# For illustrative purpose, zip this data into a 2D array:
xy_data = np.column_stack((x, y))

# (You could of course do this all in one go, but I want to illistrate
# the methods clearly at first)


# Write out to text file, keeping full precission:
np.savetxt(txt_filename, xy_data)

# # The above is equivilant to:
# with open(txt_filename, "wt") as out_file:
#     for x, y in xy_data:
#         print("{:.18e} {:.18e}".format(x, y), file=out_file)


# Now, write to file in raw binary format:
xy_data.tofile(bin_filename)

# The above is equivilant to:
with open(bin_filename2, "wb") as file:
    for x, y in xy_data:
        file.write(x)
        file.write(y)

# Look at the file sizes of the text vs. binary file:
# The binary file should be ~3x smaller.
# This is because we only wrote the exact required bytes to the file.

data_in = np.fromfile(bin_filename)
data_in2 = np.fromfile(bin_filename2)

# We can check these are the same:
print(data_in - data_in2)

# Note: this returned us 1D data, when we wrote a 2D array
# None of the shape information was written to the file

num_cols = 2
num_rows = int(len(data_in) / num_cols)

xy_data_in = data_in.reshape(num_rows, num_cols)

# Now, we can check that this has the right size/shape, and is the same as the
# original data:
print(xy_data - xy_data_in)
