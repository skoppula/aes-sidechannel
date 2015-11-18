import numpy as np


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
