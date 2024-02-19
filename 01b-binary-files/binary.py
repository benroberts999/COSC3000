#!/usr/bin/env python3
import numpy as np

filename = "data.dat"

txt_filename = "data.text"
bin_filename = "data.binary"
bin_filename2 = "data.binary2"

# As a start, read in the same example data from from before
xy_data = np.genfromtxt(filename)

# Write out to text file, keeping full precission:
np.savetxt(txt_filename, xy_data)

# The above is equivilant to:
# with open(txt_filename, "wt") as file:
#     for x, y in xy_data:
#         print("{:.18e} {:.18e}".format(x, y), file=file)


# Now, write to file in binar format:
xy_data.tofile(bin_filename)

# The above is equivilant to:
with open(bin_filename2, "wb") as file:
    for x, y in xy_data:
        file.write(x)
        file.write(y)

# Look at the file sizes of the text vs. binary file:
# The binary file should be ~3x smaller.
# This is because we only wrote the exact required bytes to the file.

xy_data_in = np.fromfile(bin_filename)
xy_data_in2 = np.fromfile(bin_filename2)

# We can check these are the same:
print(xy_data_in - xy_data_in2)

# Note: this returned us 1D data, when we wrote a 2D array
# None of the shape information was written to the file

num_cols = 2
num_rows = int(len(xy_data_in) / num_cols)

xy_data_in = xy_data_in.reshape(num_rows, num_cols)

# Now, we can check that this has the right size/shape, and is the same as the
# original data:
print(xy_data - xy_data_in)
