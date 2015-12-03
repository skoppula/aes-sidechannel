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

    z = 0
    for file_count in xrange(-2,len(all_files)-2):
        for fyle in all_files:
            if 'W' + str(file_count) + '-'  in fyle:
                break
        if not fyle.split('-')[1].startswith('288'): continue

        print '\tReading ', infolder+fyle, ' ', file_count,'/', num_traces
        trace_values = wfm2read_fast.wfm2read(infolder+fyle)[0] 
        trimmed_values = trace_values[len(trace_values)*start_frac:len(trace_values)*end_frac]
#         def avg_map(arr, numSamps):
#             avged_arr = []
#             for i in range(len(arr)/numSamps):
#                 nextClump = arr[i*numSamps:i*numSamps+numSamps]
#                 nextValue = sum(nextClump)/numSamps
#                 avged_arr.append(nextValue)
#             return avged_arr
# 
        # averaged_values = avg_map(trimmed_values, 1)
        try:
            traces
        except NameError:
            traces = np.zeros((len(files_included), len(averaged_values)))
        traces[z, :] = averaged_values
        z += 1
        
    np.save(outfile, traces)
    print 'Finished processing all WFMs. Output in',outfile

if '__main__' == __name__:
    readWFMs(infolder='../../trace-data/12-02-2015-100/',outfile='12-02-2015-100plaintexts-XOR')

