#include <stdio.h>
#include <stdlib.h>

/*
  Example to read simple white-space delimetered file using C

  compile: gcc readfile-c.c -o readfile-c
  run:     ./readfile-c
*/

int main() {

  const char *file_name = "data.dat";

  // Open the file:
  FILE *file = fopen(file_name, "r");
  if (file == NULL) {
    printf("Error: file not open.\n");
    return 1;
  }

  // Define array/buffer sizes:
  const int max_line_size = 128;    // maximum length of a line in the file
  const int max_data_length = 1024; // maximum number of lines in file
  const int data_dim = 2;           // dimensionality: 2 for 2D (x,y) data

  double data[max_data_length][data_dim];
  int lines_read = 0; // keep track of actual number of lines read

  // array to store each line:
  char line[max_line_size];

  // Loop through file, line-by-line:
  while (fgets(line, max_line_size, file)) {

    // Ensure we don't over-run array size
    if (lines_read >= max_data_length) {
      puts("Warning: file too long, increase buffer\n");
      break;
    }

    // split each line into doubles using strtod:
    char *pStart = line, *pEnd;
    for (int j = 0; j < data_dim; ++j) {
      data[lines_read][j] = strtod(pStart, &pEnd);
      pStart = pEnd;
    }

    // keep track of data lines actually read/stored
    lines_read++;
  }

  fclose(file);

  printf("Read %i lines into array\n", lines_read);

  // Print array to screen, to check it worked:
  printf("\nData:\n");
  for (int i = 0; i < lines_read; ++i) {
    for (int j = 0; j < data_dim; ++j) {
      printf("%.4f ", data[i][j]);
    }
    printf("\n");
  }
  printf("\n");

  return 0;
}