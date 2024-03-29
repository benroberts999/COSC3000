#include <array>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

/*
  This example is for a simple plain text file using C++
  That is white-space delimetered, and contains no comments/header.
  See "extra" example for more complicated case.

  compile: gcc readfile-cpp.cpp -o readfile-cpp
  run:     ./readfile-cpp

  On older compilers, may need: g++ -std=c++17 readfile-cpp.cpp
  On even older compilers, remove the C++17 feature as commented below
*/

int main() {

  std::string file_name{"data.dat"};

  // Open the file using "in-file-stream"
  std::ifstream input_file{file_name};

  if (!input_file.is_open()) {
    std::cout << "Error: File " << file_name << " could not be opened\n";
    return 1;
  }

  // Arrays to store x and y data separately
  std::vector<double> x{}, y{};

  // Alternatively, store as a 2D array
  // (There are many ways to do this, this is a common/simple way)
  std::vector<std::array<double, 2>> xy;

  // Loop through the file line-by-line (copy each line to string 'line')
  std::string line;
  while (std::getline(input_file, line)) {
    // Use stringstream to extract the data
    double tx, ty;
    std::stringstream(line) >> tx >> ty;

    // read into x/y arrays seperately
    x.push_back(tx);
    y.push_back(ty);

    // Or, into 2D array
    xy.push_back({tx, ty});
  }

  // Output the screen (just a test):

  // this requires c++-17:
  for (const auto &[x, y] : xy) {
    std::cout << x << " " << y << "\n";
  }

  // // otherwise, this works with c++11
  // for (const auto &entry : xy) {
  //   std::cout << entry[0] << " " << entry[1] << "\n";
  // }
}
