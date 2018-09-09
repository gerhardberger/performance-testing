import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import interp1d

levels = ['low', 'medium', 'high']
names = ['aws-lambda', 'google-cloud-functions', 'microsoft-azure-functions', 'fission']
colors = ['r', 'b', 'y', 'g']

def cdf(data, level, name, color):
  data_size = len(data)

  data_set = sorted(set(data))
  bins = np.append(data_set, data_set[-1]+1)

  counts, bin_edges = np.histogram(data, bins=bins, density=False)
  counts = counts.astype(float) / data_size
  cdf = np.cumsum(counts)

  plt.plot(bin_edges[0:-1], cdf, linestyle='-', color=color)

def draw_percentile(percentile):
  for level in levels:
    plt.cla()
    plt.clf()
    i = 0

    legend_patches = []
    for name in names:
      with open('./results/{0}/{1}.json'.format(level, name)) as f:
        data = json.load(f)

        sorted_latencies = np.sort(data['latencies'])
        percentile_length = int(len(sorted_latencies) * (percentile / 100.0))
        percentiled_latencies = sorted_latencies[:percentile_length]

        cdf(percentiled_latencies, level, name, colors[i])
        legend_patches.append(mpatches.Patch(color=colors[i], label=name))

        i += 1


    plt.title('{0} load, {1}th percentile latency'.format(level, percentile))
    plt.legend(handles=legend_patches)
    plt.ylim((0,1))
    plt.xlabel('Latency (ms)')
    plt.ylabel('CDF')
    plt.grid(True)

    # plt.show()
    plt.savefig('./results/{0}_{1}.png'.format(level, percentile), transparent=True, dpi=300)

draw_percentile(100)
draw_percentile(99)
draw_percentile(95)
