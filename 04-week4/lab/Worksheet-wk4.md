# Visualisation worksheet [13/3/2024]

## Week 4: Timeseries data

### A. Annual cycles

Load the data in `data.csv`.
It has 5 data collumns (creatively labelled `data1`...`data5` as a function of `month`).

1. Create plots (e.g., tile/heat map, or any other relevant plot type) to see if there are annual cycles and/or longer-
term cycles or trends.

2. Calculate and autocorrelation function for the data; plot them on the same plot

### B. Fourier Transforms

1. Plot the data in f1, f2 and f3 vs t1. Can you see cycles in the data?

2. Use fft to calculate the Fourier transforms of the data. Note that the Fourier transform
is complex rather than real, so we plot the absolute value squared, and includes positive and negative frequencies, which we can deal with using fftshift or by using the
positive frequencies only (see lecture examples).

### C. C02 data

Get the data from: <https://gml.noaa.gov/ccgg/trends/gl_data.html>

* Globally averaged marine surface monthly mean data as (CSV)

```python
data3 = np.genfromtxt("co2_mm_gl.csv", delimiter=",", skip_header=38, names=True)
```

Figure out what the collumns mean, and plot the data

Visualise this data in a number of ways using the techniques from the lecture

1. Use linear fit to extract the overall trend, and a smoothing function to examine the shorter term oscaillations

2. Use heatmaps to visualse the trends

3. Plot a cycle graph, with the January CO2 concentrations over the years, the February concentrations, etc.
