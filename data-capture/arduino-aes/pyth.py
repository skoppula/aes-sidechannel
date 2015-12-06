import serial
import time
import sys

num_traces = 500

for i in range(0, num_traces):
    ser.write(b"r")
    time.sleep(1)
port = sys.argv[1]
print 'Using port', port

with serial.Serial(port) as ser:
    numTraces = 500

    for i in range(0, numTraces):
        ser.write(b"r")
        print 'Sent run command!'
        time.sleep(60)
        numBytesToRead = ser.inWaiting()
        if numBytesToRead > 0:
            print ser.read(numBytesToRead)

