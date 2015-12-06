import serial
import time
ser = serial.Serial('/dev/cu.usbmodem1411')
print('Port in use is ' + ser.name)

num_traces = 500

for i in range(0, num_traces):
    ser.write(b"r")
    time.sleep(1)

ser.close()
