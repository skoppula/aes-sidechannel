import numpy as np
import os
import sys

sys.path.append('../data-capture/process-wfms/')
import wfm2read_fast

def loadFromNPFile(fname):
    return np.load(fname)

def readWFMs(infolder, outfile):
    print 'Reading WFMs from', infolder

    all_files =  os.listdir(infolder)
    num_traces = 900
    for file_count in xrange(1,num_traces+1):
        fyle = 'W' + str(file_count) + '.wfm'
        print '\tReading ', infolder+fyle, ' ', file_count,'/', num_traces
        trace_values = wfm2read_fast.wfm2read(infolder+fyle)[0] 
        traces_trimmed = trace_values
        try:
            traces
        except NameError:
            traces = np.zeros((num_traces, len(traces_trimmed)))
        traces[file_count-1, :] = traces_trimmed
        
    np.save(outfile, traces)
    print 'Finished processing all WFMs. Output in',outfile

if '__main__' == __name__:
    readWFMs(infolder='/Users/hol/Desktop/2015-12-3-0-19/',outfile='12-03-0-19')

