#include <cassert>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>

int main() {

  // You could of course take this in as input!
  std::string file_name{"waves_data0.bin"};

  std::ifstream input_file(file_name, std::ios::binary);

  if (!input_file.is_open()) {
    std::cout << "Error: File " << file_name << " could not be opened\n";
    return 1;
  }

  //----------------------------------------------------------------------------
  std::cout << "\n-- Table 20.2 : File Header --\n\n";

  char cookie[2];
  input_file.read(reinterpret_cast<char *>(&cookie), sizeof(cookie));
  std::cout << "cookie: " << cookie[0] << " " << cookie[1] << "\n";

  u_int16_t version;
  input_file.read(reinterpret_cast<char *>(&version), sizeof(version));
  std::cout << "version: " << version << "\n";

  u_int64_t file_size;
  input_file.read(reinterpret_cast<char *>(&file_size), sizeof(file_size));
  std::cout << "version: " << version << "\n";

  u_int32_t num_waveforms;
  input_file.read(reinterpret_cast<char *>(&num_waveforms),
                  sizeof(num_waveforms));
  std::cout << "Number of Waveforms: " << num_waveforms << "\n";

  //----------------------------------------------------------------------------
  std::cout << "\n-- Table 20.3 : Waveform Header --\n\n";

  const auto parse_wf_type = [](u_int32_t type) {
    switch (type) {
    case (0):
      return "Unkown";
    case (1):
      return "Normal";
    case (2):
      return "PeakDetection";
    case (3):
      return "Average";
    case (6):
      return "Logic";
    default:
      return "error";
    }
  };

  const auto parse_units = [](u_int32_t type) {
    switch (type) {
    case (0):
      return "Unkown";
    case (1):
      return "Volts (V)";
    case (2):
      return "Seconds (s)";
    case (3):
      return "Constant";
    case (4):
      return "Amps (A)";
    case (5):
      return "Decibel (dB)";
    case (6):
      return "Hertz (Hz)";
    default:
      return "error";
    }
  };

  // Loop throuh each of the waveforms:
  for (u_int32_t i_wf = 0; i_wf < num_waveforms; ++i_wf) {
    std::cout << "Waveform number: " << i_wf + 1 << "/" << num_waveforms
              << "\n";

    u_int32_t header_size;
    input_file.read(reinterpret_cast<char *>(&header_size),
                    sizeof(header_size));
    std::cout << "Header size " << header_size << "\n";

    u_int32_t wf_type;
    input_file.read(reinterpret_cast<char *>(&wf_type), sizeof(wf_type));
    std::cout << "Waveform type: " << wf_type << " = " << parse_wf_type(wf_type)
              << "\n";

    u_int32_t num_wf_buffers;
    input_file.read(reinterpret_cast<char *>(&num_wf_buffers),
                    sizeof(num_wf_buffers));
    assert(num_wf_buffers == 1 && "number of waveform buffers must be 1");

    u_int32_t num_points;
    input_file.read(reinterpret_cast<char *>(&num_points), sizeof(num_points));
    std::cout << "Number of wf points: " << num_points << "\n";

    u_int32_t count;
    input_file.read(reinterpret_cast<char *>(&count), sizeof(count));
    std::cout << "Count: " << count << "\n";
    assert(count == 0);

    static_assert(sizeof(float) == 4);

    float Xd_range;
    input_file.read(reinterpret_cast<char *>(&Xd_range), sizeof(Xd_range));
    std::cout << "X Display Range: " << Xd_range << "\n";

    static_assert(sizeof(double) == 8);

    double Xd_origin;
    input_file.read(reinterpret_cast<char *>(&Xd_origin), sizeof(Xd_origin));
    std::cout << "X Display Origin: " << Xd_origin << "\n";

    double X_inc;
    input_file.read(reinterpret_cast<char *>(&X_inc), sizeof(X_inc));
    std::cout << "X Increment: " << X_inc << "\n";

    std::cout << "Sanity check: " << Xd_range / X_inc << " = " << num_points
              << "  "
              << (u_int32_t(Xd_range / X_inc) == num_points ? " :)\n"
                                                            : " :(\n");

    double X_origin;
    input_file.read(reinterpret_cast<char *>(&X_origin), sizeof(X_origin));
    std::cout << "X Origin: " << X_origin << "\n";

    u_int32_t x_units;
    input_file.read(reinterpret_cast<char *>(&x_units), sizeof(x_units));
    std::cout << "X units: " << x_units << " = " << parse_units(x_units)
              << "\n";

    u_int32_t y_units;
    input_file.read(reinterpret_cast<char *>(&y_units), sizeof(y_units));
    std::cout << "Y units: " << y_units << " = " << parse_units(y_units)
              << "\n";

    char date[16];
    input_file.read(reinterpret_cast<char *>(&date), sizeof(date));
    std::cout << "Date: " << std::string{date} << "\n";

    char time[16];
    input_file.read(reinterpret_cast<char *>(&time), sizeof(time));
    std::cout << "Time: " << std::string{time} << "\n";

    char model[24];
    input_file.read(reinterpret_cast<char *>(&model), sizeof(model));
    std::cout << "Model: " << std::string{model} << "\n";

    char channel[16];
    input_file.read(reinterpret_cast<char *>(&channel), sizeof(channel));
    std::cout << "Channel Name: " << std::string{channel} << "\n";

    //----------------------------------------------------------------------------
    std::cout << "\n-- Table 20.4 : Waveform Data Header --\n\n";

    u_int32_t wf_header_size;
    input_file.read(reinterpret_cast<char *>(&wf_header_size),
                    sizeof(wf_header_size));
    std::cout << "wf Header Size: " << wf_header_size << "\n";

    u_int16_t buffer_type;
    input_file.read(reinterpret_cast<char *>(&buffer_type),
                    sizeof(buffer_type));
    std::cout << "Buffer type: " << buffer_type << "\n";

    break;
  }
}