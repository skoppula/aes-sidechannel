import numpy as np
# import scanf  # from Danny Yoo's scanf package (Berkeley)
import re


def myin(fname, ilen, n):
    myfile = open(fname, 'r')
    inputs = np.zeros((n, ilen))
    for i in range(0, n):
        s = myfile.readline()
        s_split = re.split(" ", s)
        count = 0
        for j in range(0, ilen):
            float_input = float.fromhex(s_split[count])
            inputs[i][j] = float_input
            count += 1
    return inputs
    myfile.close()
