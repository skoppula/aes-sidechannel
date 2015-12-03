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
    num_traces = len(all_files) 
    for file_count in xrange(1,num_traces+1):
        fyle = 'W' + str(file_count) + '.wfm'
        print '\tReading ', infolder+fyle, ' ', file_count,'/', num_traces
        trace_values = wfm2read_fast.wfm2read(infolder+fyle)[0] 
        try:
            traces
        except NameError:
            traces = np.zeros((num_traces, len(trace_values)))
        traces[file_count-1, :] = trace_values
        
    np.save(outfile, traces)
    print 'Finished processing all WFMs. Output in',outfile

if '__main__' == __name__:
    readWFMs(infolder='/Users/hol/Desktop/2015-12-2-21-28/',outfile='12-02-21-28')

