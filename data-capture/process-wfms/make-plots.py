import gen_plot as gp

filenames = [
        '11-30-2015/W1.wfm',
        '11-30-2015/W2.wfm',
        '11-30-2015/W3.wfm'
        ]

for fyle in filenames:
    print fyle
    gp.plot(fyle)
