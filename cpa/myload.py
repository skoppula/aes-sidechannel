import numpy as np
import os
import sys

def myload(fname, trlen, start, len, n):
    myfile = open(fname, 'r')
    traces = np.zeros((n, len))
    for i in range(n):
        myfile.seek(start, 1)
        if len + start > trlen:
            t = np.fromfile(myfile, dtype=np.uint8, count=len-start)
        else:
            t = np.fromfile(myfile, dtype=np.uint8, count=len)
        myfile.seek((trlen-len-start), 1)
        traces[i, :] = t
    myfile.close()
    return traces

def loadFromNPFile(fname='../../trace-data/11-23-2015/trace_data.npy'):
    return np.load(fname)

def readWFMs(infolder='../../trace-data/11-23-2015/', outfile='trace_data'):
    print 'Reading WFMs from', infolder


    sys.path.append('../data-capture/process-wfms/')
    import wfm2read_fast

    data_scale = 1
    num_traces = sum([1 if fyle.endswith('.wfm') else 0 for fyle in os.listdir(infolder)])

    file_count = 0
    for fyle in os.listdir(infolder):
        print '\tReading',fyle, file_count,'/',num_traces
        if not fyle.endswith('.wfm'): continue
        trace_values = wfm2read_fast.wfm2read(infolder+fyle)[0]
        trimmed_values = trace_values[len(trace_values)*0.4:len(trace_values)*0.75]
        #average_values = []
        #for i in range(len(trace_values)/data_scale):
        #    average_values.append(sum(trace_values[data_scale*i:data_scale*i+data_scale]
        try:
            traces
        except NameError:
            traces = np.zeros((num_traces, len(trimmed_values)/data_scale))
        traces[file_count, :] = trimmed_values
        file_count += 1
        
    np.save(outfile, traces)
    print 'Finished processing all WFMs. Output in',outfile

if '__main__' == __name__:
    readWFMs()

