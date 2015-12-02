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

def loadFromNPFile(fname='../../trace-data/11-30-2015/230_traces_averaged/230_trace_averaged.npy'):
    return np.load(fname)

def readWFMs(infolder='../../trace-data/11-23-2015/', outfile='trace_data'):
    print 'Reading WFMs from', infolder


    sys.path.append('../data-capture/process-wfms/')
    import wfm2read_fast

    num_traces = 100
    start_frac, end_frac = (0.1,0.8)

    # EVIL DO NO USE!
    # num_traces = 0
    # for fyle in os.listdir(infolder):
    #     if fyle.endswith('.wfm') and not (int(fyle.split('.')[0][1:]) == 0 or int(fyle.split('.')[0][1:]) > N):
    #         num_traces += 1

    # file_count = 0
    # EVIL DO NO USE!
    # for fyle in os.listdir(infolder):
    for file_count in xrange(num_traces):
        # if not fyle.endswith('.wfm'): continue
        # if int(fyle.split('.')[0][1:]) == 0 or int(fyle.split('.')[0][1:]) > N: continue
        fyle = 'W%d.wfm' % (file_count+1)
        print '\tReading ', infolder+fyle, ' ', file_count+1,'/', num_traces
        trace_values = wfm2read_fast.wfm2read(infolder+fyle)[0] 
        trimmed_values = trace_values[len(trace_values)*start_frac:len(trace_values)*end_frac]
        def avg_map(arr, numSamps):
            avged_arr = []
            for i in range(len(arr)/numSamps):
                nextClump = arr[i*numSamps:i*numSamps+numSamps]
                nextValue = sum(nextClump)/numSamps
                avged_arr.append(nextValue)
            return avged_arr

        averaged_values = avg_map(trimmed_values, 5)
        #average_values = []
        #for i in range(len(trace_values)/data_scale):
        #    average_values.append(sum(trace_values[data_scale*i:data_scale*i+data_scale]
        try:
            traces
        except NameError:
            traces = np.zeros((num_traces, len(averaged_values)))
        traces[file_count, :] = averaged_values
        # file_count += 1
        
    np.save(outfile, traces)
    print 'Finished processing all WFMs. Output in',outfile

if '__main__' == __name__:
    # readWFMs(infolder='../../trace-data/11-30-2015/500-plaintexts-attempt-1/',outfile='11-30-2015')
    readWFMs(infolder='/home/skoppula/11-30-2015-500-again/',outfile='11-30-2015-again')

