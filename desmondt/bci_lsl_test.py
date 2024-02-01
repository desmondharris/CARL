import matplotlib
import matplotlib.pyplot as plt
import random
import time
import pylsl
warmup_trials = 10
trials_per_class = 60
perform_time = 3.5
wait_time = 1
pause_every = 30
pause_duration = 10
fontsize = 40
labels = ['C', 'R']
markers = ['Activated', 'Relaxed']

matplotlib.rcParams.update({'font.size': fontsize})

hFigure, ax = plt.subplots()
ax.set_yticklabels([''])
ax.set_xticklabels([''])
t = plt.text(0.5, 0.5, '', horizontalalignment='center')
plt.xlim(xmin=0, xmax=1)
plt.ylim(ymin=0, ymax=1)
plt.ion()
plt.draw()
plt.show()
try:
    for trial in range(1, warmup_trials + trials_per_class * len(labels) + 1):
        # Check if the figure has been closed
        #if not plt.fignum_exists(hFigure.number):
            #break
        # TODO: better randomness
        choice = random.choice(range(len(labels)))
        t.set_text(labels[choice])
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
        time.sleep(perform_time)
        t.set_text('')
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()

        if trial % pause_every == 0:
            t.set_text('Pause')
            hFigure.canvas.draw()
            hFigure.canvas.flush_events()
            t.set_text('')
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
except Exception as e:
    print(e)