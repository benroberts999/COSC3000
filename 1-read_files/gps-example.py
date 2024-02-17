#!/usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt
from urllib import request
import gzip
import pandas as pd
from os import path

""" This file downloads and plots data from the atomic clocks
    onboard the GPS satellites for a given day.
    This dats is publicly available at: sideshow.jpl.nasa.gov/pub/jpligsac/
"""

# GPS data file location and format:
week = 2299
day_of_week = 0

url = "https://sideshow.jpl.nasa.gov/pub/jpligsac/" + str(week) + "/"
filename = "jpl" + str(week) + str(day_of_week) + ".clk.gz"


def get_file(url, filename):
    """Download file if it doesn't already exist"""
    if not path.isfile(filename):
        filename2, info = request.urlretrieve(
            url + filename,
            filename,
        )
        assert filename2 == filename


# Download the file, if it doesn't exist already
get_file(url, filename)

print("Have or downloaded file: ", filename)
print()

# This file has a large 'header'
# It's usually ~96 lines long, but not always.
# The header ends with "END OF HEADER"
# There is some useful info up there, but we don't need it
# We find the '"END OF HEADER"' string, and read the file from there


def find_line_containing(file, the_string) -> int:
    for num, line in enumerate(file, 1):
        if the_string in line:
            return num


unziped = gzip.open(filename, "rt")
header_line = find_line_containing(unziped, "END OF HEADER")
print("Found", header_line, "header lines")
print()

# Here, we use pandas, because of its ability to deal
# with complicated data containing multiple types.
# You can achieve the same results

data = pd.read_csv(
    filename,
    skiprows=header_line,
    delimiter=" ",
    skipinitialspace=True,  # Interpret multiple spaces as 1 delimiter
    names=(  # Give names to each column of data file:
        "Type",
        "Clock",
        "Year",
        "Month",
        "Day",
        "Hour",
        "Minute",
        "Second",
        "ncols",
        "Bias",
        "Error",
    ),
)

print("Read file into dataframe:")
print(data)
print()

# There are two types of "clocks" - satellite clocks (labelled "AS"), and ground recievers (AR)
sat_data = data[data.Type == "AS"]
rec_data = data[data.Type == "AR"]

# Get the date from the file (it is in the filename, but here we get it from the file)
date_string = (
    str(sat_data.iloc[0]["Year"])
    + "-"
    + str(sat_data.iloc[0]["Month"])
    + "-"
    + str(sat_data.iloc[0]["Day"])
)

print("Date of file:", date_string)
print()

# Generate the list of unique satellite clocks:
clock_list = sat_data["Clock"].unique()
print("List of satellite clocks:")
print(clock_list)
print()

# The time stamps are given in an annoying "yy dd mm hh mm ss" format
# We want to convert to a plottable float


# Define a function to convert "d/h/m/s" to "hours since start of day".
# We only plot 1 day, so we can ignore year/month.
# We need to include the day, because midnight appears twice in the file!
def convert_time(row):
    return (
        row["Day"] * 24.0 * 60.0 * 60.0
        + row["Hour"] * 60.0 * 60.0
        + row["Minute"] * 60.0
        + row["Second"]
        - sat_data.iloc[0]["Day"] * 24.0 * 60.0 * 60.0
    ) / (60.0 * 60.0)


# Apply this conversion to each row, store in new column "Time"
sat_data["Time"] = sat_data.apply(convert_time, axis=1)


print("Plot raw clock data:\n")

# When plotting, we change x-axis units to hours, and y-axis to nanoseconds,
# for improved legibility
plt.title("Raw bias data")
plt.xlabel("Hours since " + date_string)
plt.ylabel("Bias (ns)")

for clock in clock_list:
    t_data = sat_data[sat_data.Clock == clock]
    plt.plot(t_data["Time"], t_data["Bias"] * 1e9, label=clock)
plt.legend()
plt.show()


# The clocks all show a reasonably significant offset
# This is essentially an "initial calibration offset"
# And can be removed without any issue

print("Plot clock data with mean subtracted:\n")

plt.title("Subtract mean")
plt.xlabel("Hours since " + date_string)
plt.ylabel("Bias (ns)")

for clock in clock_list:
    t_data = sat_data[sat_data.Clock == clock]
    bias = t_data["Bias"]
    bias -= np.mean(bias)
    plt.plot(t_data["Time"], bias * 1e9, label=clock)
plt.legend()
plt.show()


# All the clocks show a significant drift.
# Depending on the reason for studying the data, the drift can be modelled and removed.
# The common method is to subtract a 2nd-order polynomal (fitted for each day).
# We also add a constant offset to each clock, so we can see them on the plot.
# Finally, we only plot every second clock, because there's so many

print("Plot clock data with Polynomial subtracted + offset:\n")

plt.title("Polynomial subtracted + offset + every second + errors")
plt.xlabel("Hours since " + date_string)
plt.ylabel("Bias (ns)")


def poly(c, x):
    return c[0] * x**2 + c[1] * x + c[2]


offset = 1e-9  # 1 ns
for count, clock in enumerate(clock_list):
    if count % 2 == 0:
        continue
    t_data = sat_data[sat_data.Clock == clock]
    bias = t_data["Bias"]
    time = t_data["Time"]
    c = np.polyfit(time, bias, 2)
    bias -= poly(c, time)
    bias += count * offset / 2  # (/2) because plot every second
    error1 = bias + t_data["Error"]
    error2 = bias - t_data["Error"]
    plt.plot(time, bias * 1e9, label=clock)
    plt.plot(time, error1 * 1e9, "k--", linewidth=0.5)
    plt.plot(time, error2 * 1e9, "k--", linewidth=0.5)
plt.legend()
plt.show()
