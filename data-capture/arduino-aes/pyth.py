import serial
import time
import sys

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

