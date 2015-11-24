import numpy as np
import matplotlib.pyplot as plt
import wfm2read

filename = '11-23-2015W4.wfm'
yt = [None]*4
for i in [1]:
    curr_filename = '11-23-2015W4.wfm'
    yt[i-1],t,_,_,_,_ = wfm2read.wfm2read(curr_filename)
    print "Read file: ", curr_filename
y = np.array(yt)

plt.plot(t, y[0], 'r')
# plt.plot(t, y[2]/2, 'g')
# plt.plot(t, y[1]+2, 'c')
# plt.plot(t, y[3]+2, 'm')
plt.show()

# tmin = 0.012
# tmax = 0.023
# def print_errors(y, t, tmin, tmax):
#     tx_1  = 0
#     tx_0v5 = 0
#     last_tx = 0
#     rx_1v = 0
#     rx_2v = 0
#     last_rx = 1
#     
#     for n in xrange(np.where(t<tmin)[0][-1], np.where(t>=tmax)[0][0]):
#         # TX level detect
#         if y[0][n] > 1:
#             tx_1v = n
#         if y[0][n] <= 0.5:
#             if tx_0v5 < tx_1v:
#                 if last_rx <= last_tx:
#                     print 'Missed TX at time ', t[last_tx]
#                 last_tx = int(np.floor((tx_1v+n)/2));
#             tx_0v5 = n
#         # RX level detect
#         if y[2][n] < 1:
#             rx_1v = n
#         if y[2][n] >= 2:
#             if rx_2v < rx_1v:
#                 if last_tx <= last_rx:
#                     print 'Extra RX at time ', t[last_rx]
#                 last_rx = int(np.floor((rx_1v+n)/2))
#             rx_2v = n
# # figure(2)
# # set(gcf,'Units', 'inches')
# # set(gcf, 'Position', [2.1444    6.5444   200.0    3.5111])
# # clf
# # plot(t,y(1,:)+1.5,'b')
# # hold on
# # plot(t,y(4,:)/2,'r')
# # xlim([0.012,0.023])
# # %xlim([0.0025,0.015])
