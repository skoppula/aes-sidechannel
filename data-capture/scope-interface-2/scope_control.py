import pyvisa
import time
import serial
import sys

def get_serial(ser, t=1):
    time.sleep(t)
    nbytes = ser.inWaiting()
    if nbytes > 0:
        print ">> "+ '\n>> '.join(ser.read(nbytes).rstrip().split('\n'))

port = sys.argv[1]
print 'Using port %s for Arduino' % port
ser = serial.Serial(port)

rm = pyvisa.ResourceManager()
print rm.list_resources()
ii = rm.open_resource(rm.list_resources()[1])

ser.setDTR(False)
time.sleep(0.022)
ser.setDTR(True)
get_serial(ser, 5)

# Hack to reset acquisition count on scope to zero
ii.write('ACQUIRE:MODE SAMPLE')
ii.write('ACQ:STATE RUN')
ii.write('ACQUIRE:MODE AVERAGE')

ii.write('ACQUIRE:NUMAVG 10')  

num_acqs = int(ii.query('ACQUIRE:NUMACQ?'))

prev_acqs = num_acqs
orig_acqs = num_acqs
curr_acqs = 0

dirname = 'C:\\858\\'+'-'.join(time.strftime("%x").split('/'))+'-'+'-'.join(time.strftime("%X").split(':'))
ii.write('FILESystem:MKDir "'+dirname+'"')

num_traces = 100
n = 0

while(n < num_traces):
    while(ii.query('TRIGGER:STATE?') != 'READY\n'):
        continue

    prev_acqs = int(ii.query('ACQUIRE:NUMACQ?'))
    time.sleep(0.2)
    ser.write('r')
    curr_acqs = int(ii.query('ACQUIRE:NUMACQ?'))
    while(curr_acqs == prev_acqs):
        curr_acqs = int(ii.query('ACQUIRE:NUMACQ?'))

    if(curr_acqs % 10 == 0):
        n += 1
        filename = '%s\W%d.wfm' % (dirname, n)
        ii.write('SAV:WAVE CH1, "'+filename+'"')
        get_serial(ser, 2)

ser.close()
ii.close()
