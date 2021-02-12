#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import sys
import string



if (len(sys.argv) != 2):
    print("usage python3 analysis.py <datafile>")
    exit()
else:
    filename = sys.argv[1]


plot_title = ""
plot_x_label = ""
plot_y_label = ""
data = []
with open(filename) as f:
    for l in f.readlines():
        if l == "\n":
            continue
        if (l.startswith("x_axis:")):
            plot_x_label = l.split()[1].rstrip()
        elif (l.startswith("y_axis:")):
            plot_y_label = l.split(":")[1].rstrip()
        elif (l.startswith("title:")):
            plot_title = l.split(":")[1].rstrip()
        elif ("data:" in l):
            continue
        else:
            if (l != ""):
                data.append(float(l.strip()))



# In[3]:
def perform_analysis(data, d_name):
    #Calculate Sample Standard Deviation
    N = len(data)
    x_bar = np.average(data)
    S = np.std(data, ddof=1) #Sets divisor to N-ddof or N-1
    S_xbar = S/ np.sqrt(N)

    X = 0
    for i in range(N):
        X += ((data[i] - x_bar)/(S))**2

    print("N", N , d_name)
    print("x_bar ", x_bar, d_name)
    print("S ", S, d_name)
    print("S_xbar", S_xbar, d_name)
    print("X", X, d_name)

    return(N, x_bar, S, S_xbar)

data_tuple = perform_analysis(data, plot_y_label)


fig, ax = plt.subplots(1,2)

def plot_sample(ax, data, dtuple):

    global plot_x_label
    global plot_y_label
    global plot_title

    N, x_bar, S, S_xbar = dtuple
    x = np.arange(N)
    ax.scatter(x, data, s=35, marker="x", color="red")
    ax.set_xlabel(plot_x_label)
    ax.set_ylabel(plot_y_label)
    ax.set_title(plot_title)



    # ax.set_ylim(0.75, 1.5)
    av_line = ax.hlines(x_bar, 0, N-1, color="red", label="mean")

    std_above = ax.hlines(x_bar+S, 0, N-1, color="blue", linestyle="--", label="mean + std")
    std_below = ax.hlines(x_bar-S, 0, N-1, color="blue", linestyle="--", label="mean - std")
    ax.legend()

def plot_difference_plot(ax, data, dtuple):
    global plot_x_label
    global plot_y_label
    global plot_title

    plot_title = "Deviation Plot"
    plot_y_label = "Sigma"

    N, x_bar, S, S_xbar = dtuple
    x = np.arange(N)

    diffav = lambda p: (p-x_bar)/S
    data = np.array([diffav(xi) for xi in data])

    S -= x_bar
    ax.scatter(x, data, s=35, marker="o", color="red")
    ax.set_xlabel(plot_x_label)
    ax.set_ylabel(plot_y_label)
    ax.set_title(plot_title)



    # ax.set_ylim(0.75, 1.5)
    av_line = ax.hlines(0, 0, N-1, color="red", label="mean")

    for i in range(1,4):
        std_above = ax.hlines(0+i, 0, N-1, color=(0, 0.1, 1, 1/(i)), linestyle="--", label="mean + std")
        std_below = ax.hlines(0-i, 0, N-1, color=(0, 0.1, 1, 1/(i)), linestyle="--", label="mean - std")
        if (i > 1):
            std_above.set_label(None)
            std_below.set_label(None)

    ax.legend()   
#Sample Plots

plot_sample(ax[0], data, data_tuple)
plot_difference_plot(ax[1], data, data_tuple)
# plot_sample(ax, y_vals, h_tuple)

# # N is the count in each bin, bins is the lower-limit of the bin
# N, bins, patches = ax.hist(y_vals, bins=25)

# # We'll color code by height, but you could use any scalar
# fracs = N / N.max()

# # we need to normalize the data to 0..1 for the full range of the colormap
# norm = colors.Normalize(fracs.min(), fracs.max())

# # Now, we'll loop through our objects and set the color of each accordingly
# for thisfrac, thispatch in zip(fracs, patches):
#     color = plt.cm.viridis(norm(thisfrac))
#     thispatch.set_facecolor(color)

# #Histogram
# ax.set_title("Height Value Histogram")
# ax.set_ylabel("Occurrences")
# ax.set_xlabel("Height")

# plt.savefig('hist.png', dpi=300, bbox_inches='tight')

plt.show()





