#include <cstdio>
#include <fstream>
#include <iostream>

int main() {

  // This is the output from the python script "binary.py"
  // Make sure you run that first!
  std::string file_name{"data.binary"};
  std::ifstream input_file(file_name, std::ios::binary);

  if (!input_file.is_open()) {
    std::cout << "Error: File " << file_name << " could not be opened\n";
    std::cout << "Run the python code first to create it!\n";
    return 1;
  }

  int count_lines{0};
  while (input_file.good()) {
    double x, y;
    input_file.read(reinterpret_cast<char *>(&x), sizeof(x));
    input_file.read(reinterpret_cast<char *>(&y), sizeof(y));

    if (input_file.eof())
      break;

    ++count_lines;

    std::cout << x << " " << y << "\n";
  }

  std::cout << "Read " << count_lines << " {x,y} pairs from binary file\n";

  /*
  // Note:
  // This version seems to read the end line twice (it doesn't really!)
  // Can anyone guess why? Not really in the scope of this course!
  while (!input_file.eof()) {
    double x, y;
    input_file.read(reinterpret_cast<char *>(&x), sizeof(x));
    input_file.read(reinterpret_cast<char *>(&y), sizeof(y));
    std::cout << x << " " << y << "\n";
  }
  */

  /*
  // Note:
  // This version also fails!
  // Can anyone see why?
  while (input_file.good()) {
    float x, y;
    input_file.read(reinterpret_cast<char *>(&x), sizeof(x));
    input_file.read(reinterpret_cast<char *>(&y), sizeof(y));
    if (input_file.eof())
      break;
    std::cout << x << " " << y << "\n";
  }
  */
}