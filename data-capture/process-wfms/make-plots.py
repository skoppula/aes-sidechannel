import gen_plot as gp
import matplotlib.pyplot as plt

filenames = [
        'W375-601.wfm',
        #'W371-288.wfm',
        'W377-641.wfm',
        #'W331-288.wfm',
        ]

plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow', 'purple'])

for fyle in filenames:
    plt.plot(*gp.plot('/media/usb/11-30-2015-500-attempt5/' + fyle))

plt.show()
