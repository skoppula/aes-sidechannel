import numpy as np
import numpy.matlib

# rows ... observations
# columns ... variables
# x,y are numpy ndarrays


def mycorr(x, y):

    (xr, xc) = x.shape
    (yr, yc) = y.shape
    assert xr == yr, 'Matrix row count mismatch'

    x_std = np.std(x, axis=0)
    y_std = np.std(y, axis=0)
    assert x_std.any() != 0, 'x std is 0'
    assert y_std.any() !=0, 'y std is 0'
    print 'x_std: ' + str(x_std)
    print 'y_std: ' + str(y_std)
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
