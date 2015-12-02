import numpy as np
import myin
import myload
import mycorr

import matplotlib.pyplot as plt
import scipy as sp

##########################################
# Python key recovery
#
# Modelled off Matlab code from
# 2014, Filip Stepanek and Jiri Bucek
##########################################

# Function to count the number of ones in a 
#   binary expression of a number
def num_ones(xx): return bin(xx).count('1')

# Element-wise Hamming Distance function
def hd(x, y):
    bitwise_xor_hd  = np.bitwise_xor(x, y) 
    return map(num_ones, bitwise_xor_hd)	

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


#####################
# LOADING the DATA
#####################


# modify following variables so they correspond to
# the measurement setup
# "Each sample is represented by 8 bit unsigned value (i.e., the length of the file is 370 000 bytes * 200 traces = 74 MB)"
numberOfTraces = 100
# traceSize = 1400000

# modify the following variables to speed-up the measurement
# (this can be done later after analysing the power trace)
# offset = 0
# segmentLength = 1400000  # for the beginning the segmentLength = traceSize

# columns and rows variables are used as inputs
# to the function loading the plaintext/ciphertext
columns = 16
rows = numberOfTraces

#########################
# Calling the functions #
#########################

# function myload processes the binary file containing the measured traces and
# stores the data in the output matrix so the traces (or their reduced parts)
# can be used for the key recovery process.
# Inputs:
#   'file' - name of the file containing the measured traces
#   traceSize - number of samples in each trace
#   offset - used to define different beginning of the power trace
#   segmentLength - used to define different/reduced length of the power trace
#   numberOfTraces - number of traces to be loaded
#
# To reduce the size of the trace (e.g., to speed-up the computation process)
# modify the offset and segmentLength inputs so the loaded parts of the
# traces correspond to the trace segment you are using for the recovery.
traces = myload.loadFromNPFile(fname='../cpa/11-30-2015-again.npy')

# function myin is used to load the plaintext and ciphertext
# to the corresponding matrices.
# Inputs:
#   'file' - name of the file containing the plaintext or ciphertext
#   columns - number of columns (e.g., size of the AES data block)
#   rows - number of rows (e.g., number of measurements)
plaintext = myin.myin('../../trace-data/11-30-2015/230_traces/hex_plaintexts_100.txt', columns, rows)
# ciphertext = myin.myin('../traces_unknown_key/ciphertext.txt', columns, rows)

##########################
# EXERCISE 1 -- Plotting the power trace(s): #
##############################################
# Plot one trace (or plot the mean value of traces)
#     and check that it is complete
#     and then select the appropriate part of the traces
# 	  (e.g., containing the first round).

# --> create the plots here <--
# print traces
# print traces[1]
plt.plot(traces[0])
# plt.show()

###############################
# EXERCISE 2 -- Key recovery: #
###############################
# Create the power hypothesis for each byte of the key and then correlate
# the hypothesis with the power traces to extract the key.
# Task consists of the following parts:
#   - create the power hypothesis
#   - extract the key using the results of the mycorr function

# variables declaration
byteStart = 1
byteEnd = 16
keyCandidateStart = 0
keyCandidateStop = 255
keyGuesses = keyCandidateStop - keyCandidateStart + 1


# for every byte in the key do:
for byte in range(byteStart, byteStart+1): #TODO change this back to byteEnd+1
    print 'Started analyzing key byte',byte

    # Create the power hypothesis matrix (dimensions:
    # rows = numberOfTraces, columns = 256).
    # The number 256 represents all possible bytes (e.g., 0x00..0xFF).
    powerHypothesis = np.zeros((numberOfTraces, keyGuesses))

    # Match every byte in the key with the corresponding byte of plaintext
	#	Take the nth byte of plaintext for every trace
	#	plaintext_nth_byte.shape = (200,)
    plaintext_nth_byte = plaintext[:, byte-1]
    
    print '\tCreating power model...'
    for k in range(keyCandidateStart, keyCandidateStop+1):
        # --> create the power hypothesis here <--
        	
        # XOR the plaintext byte with key byte and put the result through the S-BOX
        xored_plaintxt_key_bytes = np.bitwise_xor(plaintext_nth_byte.astype(int), k) 
        def sbox_func(b): return sbox_hex[b]
        sbox_result = map(sbox_func, xored_plaintxt_key_bytes)
        
        
        # Use the Hamming Distance model to calculate the hypothetical power consumption of
        #	the SBOX operation. 
        hd_arr = hd(0, sbox_result)
        
        hw_arr = num_ones(xored_plaintxt_key_bytes)

        # Use the Hamming Weight model to calculate the hypothetical power consumption
        #   of the Add Round Keys operation
        hw_arr = num_ones(xored_plaintxt_key_bytes)

		# Add this to the power hypothesis matrix
        powerHypothesis[:,k] = hw_arr

    # function mycorr returns the correlation coeficients matrix calculated
    # from the power consumption hypothesis matrix powerHypothesis and the
    # measured power traces. The resulting correlation coeficients stored in
    # the matrix CC are later used to extract the correct key.
    print '\tCalculating correlation...'
    CC = np.abs(mycorr.mycorr(powerHypothesis, traces))
    
    # --> do some operations here to find the correct byte of the key <--
    max_samples = np.max(CC, axis=1)   # index of maximum point in sample for each key
    max_key = np.argmax(max_samples)  # index of maximum key among maximumms in samples
    print '\t',sorted([(value, i) for i,value in enumerate(max_samples)])
    print 'key' + str(max_key)

    # plt.plot(CC[0])
    # plt.plot(CC[1])
    # plt.plot(CC[2])
    # plt.show()

   
