#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
  This C example is for more general data file.
  It allows multiple collumns, comments, skipped header lines, arbitrary
  delimeters etc

  compile: gcc readfile-c-extra.c -o readfile-c-extra
  run:     ./readfile-c-extra
*/

int main() {

  const char *file_name = "data-csv-labels.dat";

  int skip_header = 4;
  char comment_character = '#';
  const char *delimeter = ",";

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
  int count_lines = 0;
  while (fgets(line, max_line_size, file)) {
    ++count_lines;

    // Ensure we don't over-run array size
    if (lines_read >= max_data_length) {
      puts("Warning: file too long, increase buffer\n");
      break;
    }

    // skip header
    if (count_lines <= skip_header)
      continue;

    // Skip any comment lines
    if (line[0] == comment_character)
      continue;

    // Parse the line by comma delimiter using strtok()
    // and convert the characters to double using strtod()
    char *pt = strtok(line, delimeter);
    while (pt != NULL) {
      for (int j = 0; j < data_dim && pt != NULL; ++j) {
        data[lines_read][j] = strtod(pt, NULL);
        pt = strtok(NULL, delimeter);
      }
    }

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