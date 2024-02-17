#include <array>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

/*
  This example is for more general data file
  It allows multiple collumns, comments, skipped header lines, arbitrary
  delimeters etc
*/

int main() {

  std::string file_name{"data-csv-labels.dat"};

  // Open the file using "in-file-stream"
  std::ifstream input_file{file_name};

  // (Since we use std::array for inner array, this needs to be 'static' or
  // 'constexpr' for static-sized array. If we don't know the number of rows,
  // use std::vector or similar for inner array)
  constexpr std::size_t number_columns = 2;

  // Array to store x-y data
  // Could easily be updated to store x and y seperately
  std::vector<std::array<double, number_columns>> xy;

  // Numbr of initial rows to discard (i.e., discard header)
  const int skip_rows = 4;

  // Character to signify line is a comment:
  const char comment_charecter = '#';

  // Character to signify a new column
  const char collumn_delimeter = ',';

  // loop through lines of file, read each line into string 'line'
  std::string line;
  int count_lines{0};
  while (std::getline(input_file, line)) {
    ++count_lines;

    // skip the first few header lines
    if (count_lines <= skip_rows)
      continue;

    // skip any lines that start with a comment
    if (line.front() == comment_charecter)
      continue;

    // add an empty entry (will be {0,0}), we then set its values below
    xy.push_back({}); // this requires c++-17 (I think):

    // c++-11 version:
    // xy.push_back(std::array<double, number_columns>{});

    // Loop through all entries in the given line, count column position
    // Then, use stringstream to extract data.
    // There are many ways to do this, this way is fairly simple
    auto ssline = std::stringstream(line);
    std::string t_entry;
    std::size_t col_count{0};
    while (std::getline(ssline, t_entry, collumn_delimeter) &&
           col_count < number_columns) {
      std::stringstream(t_entry) >> xy.back().at(col_count);
      ++col_count;
    }
  }

  // Output the screen (just a test):

  // this requires c++-17:
  for (const auto &[x, y] : xy) {
    std::cout << x << " " << y << "\n";
  }
}
