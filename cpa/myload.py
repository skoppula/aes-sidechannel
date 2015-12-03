import numpy as np
import os
import sys

sys.path.append('../data-capture/process-wfms/')
import wfm2read_fast

def loadFromNPFile(fname):
    return np.load(fname)

def filter_plaintexts(lst):
    with open('./hex_plaintexts.txt', 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if (i+1) not in lst:
            lines[i] = None
    new_lines = filter(lambda x: x != None, lines)
    with open('./hex_plaintexts_288_first159.txt', 'w') as f:
        lines = f.writelines(new_lines)
        

def readWFMs(infolder, outfile):
    print 'Reading WFMs from', infolder

    start_frac, end_frac = (0.1,0.8)

    all_files =  os.listdir(infolder)
    num_traces = 159
    files_included = []
    for file_count in xrange(1,num_traces):
        for fyle in all_files:
            if 'W' + str(file_count) + '-'  in fyle:
                break
        if fyle.split('-')[1].startswith('288'):
            files_included.append(file_count)
    filter_plaintexts(files_included)

    z = 0
    for file_count in xrange(1,num_traces):
        for fyle in all_files:
            if 'W' + str(file_count) + '-'  in fyle:
                break
        if not fyle.split('-')[1].startswith('288'): continue

        print '\tReading ', infolder+fyle, ' ', file_count,'/', num_traces
        trace_values = wfm2read_fast.wfm2read(infolder+fyle)[0] 
        trimmed_values = trace_values[len(trace_values)*start_frac:len(trace_values)*end_frac]
        def avg_map(arr, numSamps):
            avged_arr = []
            for i in range(len(arr)/numSamps):
                nextClump = arr[i*numSamps:i*numSamps+numSamps]
                nextValue = sum(nextClump)/numSamps
                avged_arr.append(nextValue)
            return avged_arr

        averaged_values = avg_map(trimmed_values, 1)
        try:
            traces
        except NameError:
            traces = np.zeros((len(files_included), len(averaged_values)))
        traces[z, :] = averaged_values
        z += 1
        
    np.save(outfile, traces)
    print 'Finished processing all WFMs. Output in',outfile

if '__main__' == __name__:
    readWFMs(infolder='/media/usb/11-30-2015-500-attempt5/',outfile='11-30-2015-attempt5-only288-first159')

