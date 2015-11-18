import numpy as np
import numpy.matlib

# rows ... observations
# columns ... variables
# x,y are numpy ndarrays


def mycorr(x, y):

    (xr, xc) = x.shape
    (yr, yc) = y.shape
    assert xr == yr, 'Matrix row count mismatch'

    x = x/np.std(x, axis=0)
    y = y/np.std(y, axis=0)

    xx = x - np.mean(x, axis=0)
    yy = y - np.mean(y, axis=0)

	# calculate standardized values for each x & y
    xt = np.transpose(xx)
    cc_scale = xt.dot(yy)

    #  divide by # of traces to account for division in 
    #   standard deviation
    cc = np.divide(cc_scale, x.shape[0])
    return cc
