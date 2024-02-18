#!/usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt

filename = "data-csv-labels.dat"

xy_data = np.genfromtxt(
    filename, delimiter=",", names=True, skip_header=3, comments="#"
)

# nb: " comments='#' " is actually the default, but I put it explicitely for example

# We can get the column names if we set 'names=True':
column_names = xy_data.dtype.names
print(column_names)
xlabel = column_names[0]
ylabel = column_names[1]

# With "names", can address the columns by their name (string)
x_data = xy_data["xlabel"]
y_data = xy_data["ylabel"]

# Example: plot the data
plt.title("Example: plot of function")
plt.xlabel(column_names[0] + " (units)")
plt.ylabel("function (units)")
plt.plot(x_data, y_data, "r-", label=column_names[1])
plt.plot(x_data, y_data * (1.25), "k--", label="error")
plt.plot(x_data, y_data * (0.75), "k--")
plt.legend()

fig = plt.gcf()
fig.savefig("python-extra.png")
plt.show()
