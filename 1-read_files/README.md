# Read text files - examples

* Examples in:
  * python
  * Mathematica
  * C++
  * gnuplot

"data.dat" is a simple white-space delimetered text file, with no comments, and no header.
This is typically the simplest/easiest format to read in.

"data-csv-labels.dat" is a comma separated file, with column headers, and a data header at the top that we need to skip/ignore, and comments

The python, C++, and gnuplot examples with "extra" will read in the more complicated CSV data

[https://matplotlib.org/cheatsheets/](matplotlib cheatsheets)


## Real-world example:

The python file [gps-example.py](./gps-example.py) (also available as jupyter notebook: [gps-jupyter.ipynb](./gps-jupyter.ipynb)) downloads and plots data from the atomic clocks onboard the GPS satellites for a given day.