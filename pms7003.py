"""Read a Plantower PMS7003 serial sensor data.

A simple script to test the Plantower PMS7003 serial particulate sensor.

Outputs the various readings to the console.

Requires PySerial.

Edit the physical port variable to match the port you are using to connect to the sensor.

Updated to work on Python 3 (ord() is redundant)

Run with 'python pms7003.py'

The sensor payload is 32 bytes:

2 fixed start bytes (0x42 and 0x4d)
2 bytes for frame length
6 bytes for standard concentrations in ug/m3 (3 measurements of 2 bytes each)
6 bytes for atmospheric concentrations in ug/m3 (3 measurements of 2 bytes each)
12 bytes for counts per 0.1 litre (6 measurements of 2 bytes each)
1 byte for version
1 byte for error codes
2 bytes for checksum

MIT License

Copyright (c) 2018 Mark Benson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import os
import time

import serial

physicalPort = 'COM3'

serialPort = serial.Serial(physicalPort)  # open serial port

while True:
    # Check if we have enough data to read a payload
    if serialPort.in_waiting >= 32:
        # Check that we are reading the payload from the correct place (i.e. the start bits)
        if ord(serialPort.read()) == 0x42 and ord(serialPort.read()) == 0x4d:

            # Read the remaining payload data
            data = serialPort.read(30)

            # Extract the byte data by summing the bit shifted high byte with the low byte
            # Use ordinals in python to get the byte value rather than the char value
            frameLength = data[1] + (data[0] << 8)
            # Standard particulate values in ug/m3
            concPM1_0_CF1 = data[3] + (data[2] << 8)
            concPM2_5_CF1 = data[5] + (data[4] << 8)
            concPM10_0_CF1 = data[7] + (data[6] << 8)
            # Atmospheric particulate values in ug/m3
            concPM1_0_ATM = data[9] + (data[8] << 8)
            concPM2_5_ATM = data[11] + (data[10] << 8)
            concPM10_0_ATM = data[13] + (data[12] << 8)
            # Raw counts per 0.1l
            rawGt0_3um = data[15] + (data[14] << 8)
            rawGt0_5um = data[17] + (data[16] << 8)
            rawGt1_0um = data[19] + (data[18] << 8)
            rawGt2_5um = data[21] + (data[20] << 8)
            rawGt5_0um = data[23] + (data[22] << 8)
            rawGt10_0um = data[25] + (data[24] << 8)
            # Misc data
            version = data[26]
            errorCode = data[27]
            payloadChecksum = data[29] + (data[28] << 8)

            # Calculate the payload checksum (not including the payload checksum bytes)
            inputChecksum = 0x42 + 0x4d
            for x in range(0, 27):
                inputChecksum = inputChecksum + data[x]

            # Clear the screen before displaying the next set of data
            os.system('cls')  # Set to 'cls' on Windows, 'clear' on linux
            print("PMS7003 Sensor Data:")
            print("PM1.0 = " + str(concPM1_0_CF1) + " ug/m3")
            print("PM2.5 = " + str(concPM2_5_CF1) + " ug/m3")
            print("PM10 = " + str(concPM10_0_CF1) + " ug/m3")
            print("PM1 Atmospheric concentration = " + str(concPM1_0_ATM) + " ug/m3")
            print("PM2.5 Atmospheric concentration = " + str(concPM2_5_ATM) + " ug/m3")
            print("PM10 Atmospheric concentration = " + str(concPM10_0_ATM) + " ug/m3")
            print("Count: 0.3um = " + str(rawGt0_3um) + " per 0.1l")
            print("Count: 0.5um = " + str(rawGt0_5um) + " per 0.1l")
            print("Count: 1.0um = " + str(rawGt1_0um) + " per 0.1l")
            print("Count: 2.5um = " + str(rawGt2_5um) + " per 0.1l")
            print("Count: 5.0um = " + str(rawGt5_0um) + " per 0.1l")
            print("Count: 10um = " + str(rawGt10_0um) + " per 0.1l")
            print("Version = " + str(version))
            print("Error Code = " + str(errorCode))
            print("Frame length = " + str(frameLength))
            if inputChecksum != payloadChecksum:
                print("Warning! Checksums don't match!")
                print("Calculated Checksum = " + str(inputChecksum))
                print("Payload checksum = " + str(payloadChecksum))
    time.sleep(0.7)  # Maximum recommended delay (as per data sheet)
