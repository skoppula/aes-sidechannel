import gen_plot as gp
import matplotlib.pyplot as plt

filenames = [
        'W1.wfm',
        'W2.wfm',
        'W3.wfm',
        'W4.wfm',
        'W5.wfm',
        ]

plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow', 'purple'])

for fyle in filenames:
    plt.plot(*gp.plot('../../../trace-data/11-30-2015/500-plaintexts-attempt-1/' + fyle))

plt.show()
