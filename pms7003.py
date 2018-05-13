"""Read a Plantower PMS7003 serial sensor data.

A simple script to test the Plantower PMS7003 serial particulate sensor.

Mark Benson 2018

Licence

Outputs the various readings to the console.

Requires PySerial.

Edit the physical port variable to match the port you are using to connect to the sensor.

Run with 'python pms7003.py'

The sensor payload is 32 bytes long and consists of the following:

2 fixed start bytes (0x42 and 0x4d)
2 bytes for frame length
6 bytes for standard concentrations in ug/m3
6 bytes for atmospheric concentrations in ug/m3
12 bytes for counts per 0.1 litre
1 byte for version
1 byte for error codes
2 bytes for checksum

"""

import serial
import time
import os

physicalPort = '/dev/ttyUSB0'

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
			frameLength = ord(data[1]) + (ord(data[0])<<8)
			# Standard particulate values in ug/m3
			concPM1_0_CF1 = ord(data[3]) + (ord(data[2])<<8)
			concPM2_5_CF1 = ord(data[5]) + (ord(data[4])<<8)
			concPM10_0_CF1 = ord(data[7]) + (ord(data[6])<<8)
			# Atmospheric particulate values in ug/m3
			concPM1_0_ATM = ord(data[9]) + (ord(data[8])<<8)
			concPM2_5_ATM = ord(data[11]) + (ord(data[10])<<8)
			concPM10_0_ATM = ord(data[13]) + (ord(data[12])<<8)
			# Raw counts per 0.1l
			rawGt0_3um = ord(data[15]) + (ord(data[14])<<8)
			rawGt0_5um = ord(data[17]) + (ord(data[16])<<8)
			rawGt1_0um = ord(data[19]) + (ord(data[18])<<8)
			rawGt2_5um = ord(data[21]) + (ord(data[20])<<8)
			rawGt5_0um = ord(data[23]) + (ord(data[22])<<8)
			rawGt10_0um = ord(data[25]) + (ord(data[24])<<8)
			# Misc data
			version = ord(data[26])
			errorCode = ord(data[27])
			payloadChecksum = ord(data[29]) + (ord(data[28])<<8)

			# Calculate the payload checksum (not including the payload checksum bytes)
			inputChecksum = 0x42 + 0x4d
			for x in range(0,27):
				inputChecksum = inputChecksum + ord(data[x])

			os.system('clear') # Set to 'cls' on Windows
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
	time.sleep(0.7) # Maximum recommended delay (as per data sheet)
