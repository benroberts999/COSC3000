#!/usr/bin/env python3
import struct

# See: https://docs.python.org/3/library/struct.html
# For struct documentation

# Symbols:
# H = unsigned short (2 byte)
# I = unsigned int (4)
# Q = unsigned long long (8)
# f = float (4)
# d = double (8)

file_name = "waves_data0.bin"

################################################################################

# Parsers: for nicer output:


def parse_wf_type(type):
    types = {0: "Unknown", 1: "Normal", 2: "PeakDetection", 3: "Average", 6: "Logic"}
    return types.get(type, "error")


def parse_units(type):
    units = {
        0: "Unknown",
        1: "Volts (V)",
        2: "Seconds (s)",
        3: "Constant",
        4: "Amps (A)",
        5: "Decibel (dB)",
        6: "Hertz (Hz)",
    }
    return units.get(type, "error")


def parse_buffer_type(type):
    buffer_types = {
        0: "Unknown",
        1: "Normal 32 bit float data",
        2: "Maximum float data",
        3: "Minimum float data",
        5: "Digital unsigned 8-bit character data",
    }
    return buffer_types.get(type, "error")


################################################################################


with open(file_name, "rb") as input_file:
    cookie = input_file.read(2).decode()
    print("cookie:", cookie)
    assert cookie == "RG"

    version = struct.unpack("H", input_file.read(2))[0]
    print("version:", version)

    file_size = struct.unpack("Q", input_file.read(8))[0]
    print("file size:", file_size)

    num_waveforms = struct.unpack("I", input_file.read(4))[0]
    print("Number of Waveforms:", num_waveforms)

    print("\n-- Table 20.3 : Waveform Header --")

    for i_wf in range(num_waveforms):
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Waveform number:", i_wf + 1, "/", num_waveforms)

        header_size = struct.unpack("I", input_file.read(4))[0]
        print("Header size:", header_size)

        wf_type = struct.unpack("I", input_file.read(4))[0]
        print("Waveform type:", wf_type, "=", parse_wf_type(wf_type))

        num_wf_buffers = struct.unpack("I", input_file.read(4))[0]
        print("num_wf_buffers:", num_wf_buffers, "(must be 1)")

        num_points = struct.unpack("I", input_file.read(4))[0]
        print("Number of wf points:", num_points)

        count = struct.unpack("I", input_file.read(4))[0]
        print("Count:", count, "(must be zero)")

        Xd_range = struct.unpack("f", input_file.read(4))[0]
        print("X Display Range:", Xd_range)

        Xd_origin = struct.unpack("d", input_file.read(8))[0]
        print("X Display Origin:", Xd_origin)

        X_inc = struct.unpack("d", input_file.read(8))[0]
        print("X Increment:", X_inc)

        print(
            "Sanity check:",
            Xd_range / X_inc,
            "=",
            num_points,
            " ",
            ":)" if int(Xd_range / X_inc) == num_points else ":(",
        )

        X_origin = struct.unpack("d", input_file.read(8))[0]
        print("X Origin:", X_origin)

        x_units = struct.unpack("I", input_file.read(4))[0]
        print("X units:", x_units, "=", parse_units(x_units))

        y_units = struct.unpack("I", input_file.read(4))[0]
        print("Y units:", y_units, "=", parse_units(y_units))

        date = input_file.read(16).decode()
        print("Date:", date)

        time = input_file.read(16).decode()
        print("Time:", time)

        model = input_file.read(24).decode()
        print("Model:", model)

        channel = input_file.read(16).decode()
        print("Channel Name:", channel)

        ## The header doesn't take up the full 'header size':
        size_read = 128
        jump = header_size - size_read
        input_file.seek(jump, 1)

        ##############
        print("-- Table 20.4 : Waveform Data Header --")

        wf_header_size = struct.unpack("I", input_file.read(4))[0]
        print("wf Header Size:", wf_header_size)

        buffer_type = struct.unpack("H", input_file.read(2))[0]
        print("Buffer type:", buffer_type, "=", parse_buffer_type(buffer_type))

        bytes_per_point = struct.unpack("H", input_file.read(2))[0]
        print("Bytes for point:", bytes_per_point)

        buffer_size = struct.unpack("Q", input_file.read(8))[0]
        print("Buffer size:", buffer_size)

        points = buffer_size // bytes_per_point

        data = struct.unpack("" + "f" * points, input_file.read(buffer_size))
        out_name = "out_" + str(i_wf) + ".txt"
        print("Write at plain text to:", out_name)
        with open(out_name, "w") as out_file:
            for i in range(len(data)):
                x = X_origin + i * X_inc
                out_file.write(str(x) + " " + str(data[i]) + "\n")
