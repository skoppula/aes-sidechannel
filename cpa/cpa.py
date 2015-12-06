r Python key recovery
# Modelled off Matlab code from 2014, Filip Stepanek and Jiri Bucek

import numpy as np
import matplotlib.pyplot as plt

import re
import wfm2read_fast

def read_wfm(infolder, num_traces=100):
    print 'Reading WFMs from', infolder
    # Can add a check to see that we are not reading a file that is not
    # availabled
    for file_count in xrange(1,num_traces+1):
        fname = 'W%d.wfm' % file_count
        print 'Reading %s [%d/%d]' % (fname, file_count, num_traces)
        trace_data = wfm2read_fast.wfm2read(infolder+'/'+fname)[0] 
        trace_trimmed = trace_data[:]
        try:
            traces
        except NameError:
            traces = np.zeros((num_traces, len(trace_trimmed)))
        traces[file_count-1, :] = trace_trimmed
    # np.save(outfile, traces)
    # print 'Finished processing all WFMs. Output in',outfile
    return traces

def read_pt(fname, num_traces):
    pt_file = open(fname, 'r')
    pt_list = np.zeros((num_traces, 16))
    line_num = 0
    for line in pt_file:
        pt = map(lambda x:int(x, 16), line.rstrip().split(' '))
        pt_list[line_num] = np.array(pt)
        line_num += 1
    pt_file.close()
    return pt_list

def corr(x, y):
    # C(x, y) = (x.y - N <x><y>)/sqrt((x.x - N<x><x>)(y.y-N<y><y>))
    assert x.shape[0] == y.shape[0], 'Matrix row count mismatch'

    x_std = np.std(x, axis=0)
    y_std = np.std(y, axis=0)
    assert x_std.any() != 0, 'x std is 0'
    assert y_std.any() != 0, 'y std is 0'
    x = x/x_std
    y = y/y_std

    xx = x - np.mean(x, axis=0)
    yy = y - np.mean(y, axis=0)

    # calculate standardized values for each x & y
    xt = np.transpose(xx)
    cc_scale = xt.dot(yy)

    #  divide by # of traces to account for division in 
    #   standard deviation
    cc = np.divide(cc_scale, x.shape[0])
    assert x.shape[0]!=0, 'x.shape[0] is 0'
    return cc

# Power Models
# A power model takes a plaintext and key byte and return a power guess

# Hamming weight
def hw(xx): return bin(xx).count('1')

# Hamming Distance function
def hd(p, k): return hw(p^k)

# SBOX based power model
def sbox_power(p, k): return hw(sbox_hex[(p^k) % 256])
def sbox_power_b(p, k): return hd((p^k) % 256, sbox_hex[(p^k) % 256])

# def zero_to_one(x, y):
#     return np.bitwise_and(np.invert(x), y)

# declaration of the SBOX (might be useful to calculate the power hypothesis)
sbox_hex = [
   0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
   0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
   0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
   0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
   0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
   0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
   0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
   0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
   0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
   0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
   0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
   0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
   0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
   0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
   0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
   0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
   0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
   0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
   0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
   0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
   0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
   0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
   0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
   0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
   0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
   0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
   0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
   0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
   0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
   0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
   0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
   0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

def read_data(wfm_folder='12-03-15-17-49-12', pt_file='run_log', num_traces=100):
    traces = read_wfm(wfm_folder, num_traces)
    plaintext = read_pt(pt_file, num_traces)
    # ciphertext = myin.myin('../traces_unknown_key/ciphertext.txt', columns, rows)
    return traces, plaintext

def new_corr(state, power_hypothesis_trace, trace):
    '''
        args:
            state   dictionary of xd1, yd1, xdx, ydy, xdy, n. n starts from 10.
            power_hypothesis_trace  array of length 256
            trace   array of length len_trace
        returns:
            new_state   updated dictionary with new value
            cc_byte_num_traces  cc for a particular byte & number of traces
    '''
    xdy_new = state['x.y'] + np.dot(np.transpose(power_hypothesis_trace), trace)
    xdx_new = state['x.x'] + np.dot(np.transpose(power_hypothesis_trace), power_hypothesis_trace)
    ydy_new = state['y.y'] + np.dot(np.transpose(trace), trace)
    xd1_new = state['x.1'] + power_hypothesis_trace
    yd1_new = state['y.1'] + trace
    x_bar = xd1_new/(state['n']+1)
    y_bar = yd1_new/(state['n']+1)

    c = xdy_new -
    

def run_cpa_fast(traces, plaintext):
    '''
        args:
            traces: matrix of [num_traces x trace_len] 
            plaintext: matrix of [num_traces x size_of_plaintext]
    '''

    num_traces = len(traces)
    trace_len = len(traces[0])
    size_plaintext = len(plaintext)
    assert num_plaintext_bytes == 16
    pwr_model = np.vectorize(sbox_power)

    lines = np.zeros((size_plaintext, 256, num_traces))
    
    for byte in xrange(size_plaintext):
        CC_for_byte_and_trace_num = None # [256 x trace_len]
        power_hypothesis = np.zeros((num_traces, 256))  # for one byte [num_traces x 256]
        
        # Create the power model from plaintext
        for k in xrange(256):
            # XOR the plaintext byte with key byte and put the result through the S-BOX
            power_hypothesis[:, k] = pwr_model(plaintext[:, byte].astype(int), k)
        
        state = {'x.x':0, 'y.y':0, 'x.1':0, 'y.1':0, 'x.y':0, 'n':-1}
        # correlations for base case -- first ten traces
        first_ten_traces = traces[:10]
        first_ten_ph = power_hypothesis[:10]
        cc_for_byte_and_trace_first_ten = corr(first_ten_ph, first_ten_traces)
        # return CC, PH, x.1, y.1, x.x, y.y, x.y
        start_state['x.1'] = np.dot(power_hypothesis, np.ones((power_hypothesis.shape[1], power_hypothesis.shape[0])))
        start_state['y.1'] = np.dot(traces, np.ones((traces.shape[1], traces.shape[0])))
        start_state['x.x'] =  np.dot(np.transpose(power_hypothesis), power_hypothesis)
        start_state['y.y'] = np.dot(np.transpose(traces), traces)
        start_state['x.y'] = np.dot(np.transpose(power_hypothesis), traces)
        start_state['n'] = 9
             
        for trace_num in xrange(10, traces):
            state, CC_for_byte_and_trace_num = new_corr(state, power_hypothesis[trace_num], traces[trace_num])
            CC_for_byte_and_trace_num = np.abs(CC_for_byte_and_trace_num)
            lines[byte, :, trace_num] = np.max(CC_for_byte_and_trace_num, axis=1)

    return lines



# verbose_return returns aidditional information useful in calculating
#   cc for one more tracke
def run_cpa(traces, plaintext, num_traces=0, verbose_return=False, verbose=False):
    if num_traces != 0:
        traces = traces[:num_traces]
        plaintext = plaintext[:num_traces]
    else:
        num_traces = traces.shape[0]
    trace_length = traces.shape[1]
    # Correlation Matrix [16 x (256 x trace_length)]
    CC = [None]*16 
    PH = [None]*16
    for byte in xrange(16):
        if verbose:
            print 'Started analyzing key byte %d' % byte
    
        # Power hypothesis matrix [num_traces x 256]
        if verbose:
            print 'Creating power model'
        power_hypothesis = np.zeros((num_traces, 256))
        for k in xrange(256):
            # XOR the plaintext byte with key byte and put the result through the S-BOX
            pwr_model = np.vectorize(sbox_power)
            power_hypothesis[:, k] = pwr_model(plaintext[:, byte].astype(int), k)
        PH[byte] = power_hypothesis
    
        if verbose:
            print 'Calculating correlation'
        CC[byte] = np.abs(corr(power_hypothesis, traces))
        
        # --> do some operations here to find the correct byte of the key <--
        max_samples = np.max(CC[byte], axis=1)   # index of maximum point in sample for each key
        max_key = np.argmax(max_samples)  # index of maximum key among maximumms in samples
        max_10_keys = np.argsort(max_samples)[::-1][:10]
        if verbose:
            print 'max keys: ' + str(max_10_keys)
        # print '\t',sorted([(value, i) for i,value in enumerate(max_samples)])
    # return CC, PH, x.1, y.1, x.x, y.y, x.y
    x_ones = np.ones((power_hypothesis.shape[1], power_hypothesis.shape[0]))
    xd1 = np.dot(power_hypothesis, x_ones)
    print 'xd1: '
    print xd1.shape
    yd1 = np.dot(traces, np.ones((traces.shape[1], traces.shape[0])))
    xdx = np.dot(np.transpose(power_hypothesis), power_hypothesis)
    ydy = np.dot(np.transpose(traces), traces)
    xdy = np.dot(np.transpose(power_hypothesis), traces)
    if verbose_return:
        return CC, PH, xd1, yd1, xdx, ydy, xdy
    else:
        return CC, PH

def run_key_evolution(traces, plaintext, limits):
    lines = np.zeros((16, 256, limits[1]-limits[0]+1))
    for N in xrange(limits[0], limits[1]+1):
        print 'Waveforms %d/%d' % (N, limits[1])
        CC,_ = run_cpa(traces, plaintext, N, N==limits[1])
        for byte in xrange(16):
           lines[byte, :, N-limits[0]] = np.max(CC[byte], axis=1)
    return lines

def plot_key_evolution(lines, limits, key):
    for byte in xrange(16):
        plt.subplot(4, 4, byte+1)
        for line_num in xrange(256):
            if line_num != key[byte]:
                plt.plot(np.arange(limits[0], limits[1]+1), lines[byte, line_num], color='gray')
        plt.plot(np.arange(limits[0], limits[1]+1), lines[byte, key[byte]], color='red')
    plt.show()

def plot_cc_with_trace(CC, traces, byte, k2):
    plt.subplot(2, 1, 1)
    plt.plot(CC[byte][byte,:], 'g')
    plt.plot(CC[byte][k2,:], 'r--')
    # for line in range(0,16):
    #     x = 50+37+(389-37)*line/15.0
    #     plt.text(x-5, 4.15, '%d' % line)
    #     plt.axvline(x, color='k', linestyle='dotted')
    plt.subplot(2, 1, 2)
    #plt.plot(np.max(CC[byte-1], axis=1), 'r')
    for i in range(0,20):
        plt.plot(traces[i])
    # for line in range(0,16):
    #     x = 50+37+(389-37)*line/15.0
    #     plt.axvline(x, color='k', linestyle='dotted')
    plt.show()

# first bytes of plaintxt
# first_bytes = []
# for byte in range(0,100):
#     first_bytes.append(plaintext[0, byte])
# # Hamming weights each thing the array
# def hw_plaintxt(arr):
#     return map(num_ones, arr)
# print first_bytes
# print hw_plaintxt(first_bytes)
