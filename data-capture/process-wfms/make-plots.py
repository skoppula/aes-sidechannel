import gen_plot as gp
import matplotlib.pyplot as plt

filenames = [
        'W-2-99.wfm',
        'W-1-3.wfm',
        'W0-3.wfm',
        'W97-3.wfm',
        ]

plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow', 'purple'])

for fyle in filenames:
    plt.plot(*gp.plot('/home/skoppula/mit/security/final-project/trace-data/12-02-2015-100/' + fyle))

plt.show()
