import json
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

levels = ['low', 'medium']
names = ['aws-lambda', 'google-cloud-functions']
colors = ['r', 'b']

def cdf(data, level, name, color):
  data_size=len(data)

  data_set=sorted(set(data))
  bins=np.append(data_set, data_set[-1]+1)

  counts, bin_edges = np.histogram(data, bins=bins, density=False)

  counts=counts.astype(float) / data_size

  cdf = np.cumsum(counts)

  plt.title(name)
  plt.plot(bin_edges[0:-1], cdf, linestyle='-', color=color)
  plt.ylim((0,1))
  plt.xlabel('Latency (ms)')
  plt.ylabel('CDF')
  plt.grid(True)

  # plt.show()
  plt.savefig('./results/{0}.png'.format(level), transparent=True, dpi=300)


for level in levels:
  plt.cla()
  plt.clf()
  i = 0

  for name in names:
    with open('./results/{0}/{1}.json'.format(level, name)) as f:
      data = json.load(f)

      cdf(data['latencies'], level, name, colors[i])
      i += 1
