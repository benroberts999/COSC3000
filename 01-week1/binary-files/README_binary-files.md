# Binary files

## Unstructured (raw) binary

The simplest method to store binary data is to simply dump the 1's and 0's from memory into a file.
This is the fastest and most storage-efficient method to read/write data, and is great in certain circumstances. But it also has important downsides:

### Some issues

* Big Endian vs. Little Endian (layout of bytes)
  * [wikipedia.org/wiki/Endianness](https://en.wikipedia.org/wiki/Endianness)
* The sizes of some data types can be system dependent
  * common example: `long double`

* Great for short-term data storage (run-to-run)
* Generally not ideal for long-term storage, or portability

### Examples

* The python script [binary.py](./binary.py):
  * Generates some x/y data
  * It then writes this array to file in (a) text format, and (b) raw binary format.
  * It's instructive to compare the file sizes of these files.
  * It then reads the binary file back in

* The C++ program [cpp-binary.cpp](./cpp-binary.cpp):
  * Reads in the raw binary file that was created by python, and prints the contents to the screen

## Structured binary formats

* A python example: pickle
* Very common (~industry standard): hdf5
  * [h5py: hdf5 for python](https://docs.h5py.org/en/stable/)
    * A nice tutorial: [HDF5 files in Python](https://pythonforthelab.com/blog/how-to-use-hdf5-files-in-python/)
  * [hdf5 in MatLab](https://au.mathworks.com/help/matlab/hdf5-files.html)
  * [hdf5 in C++](https://docs.hdfgroup.org/archive/support/HDF5/doc1.8/cpplus_RM/index.html)
    * There are also some nicer wrapper libraries for hdf5 in C++

### Example

* The python script [pickle-example.py](./pickle-example.py):
  * Reads the text file in to an array
  * Writes this to file in the "pickle" structured binary format
  * Reads this back in
  * You'll need the `pickle` package: `pip install pickle5`
