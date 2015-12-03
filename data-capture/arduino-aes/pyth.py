import serial
import time
ser = serial.Serial('/dev/cu.usbmodem1411')
print('Port in use is ' + ser.name)

numTraces = 500

for i in range(0, numTraces):
    ser.write(b"R")
    time.sleep(1)

ser.close()
