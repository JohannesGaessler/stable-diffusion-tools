#!/usr/bin/env python3

import os
import numpy as np
import imageio as iio
from kafe2 import XYFit, Plot
import matplotlib.pyplot as plt

SAMPLE_DIR = "data_voldemort"
PROMPTS = [
    "Flowers",
    "Flowers - red",  # not the actual prompt
]

data = []

for i, prompt in enumerate(PROMPTS):
    prompt_dir = os.path.join(SAMPLE_DIR, prompt)
    means_i = []
    file_list = sorted(os.listdir(prompt_dir))

    for filename in file_list:
        if not filename.endswith(".png"):
            continue
        image = iio.v3.imread(os.path.join(prompt_dir, filename))
        red = np.mean(image[:, :, 0])
        means_i.append(red)

    means_i = np.array(means_i)
    data.append(means_i)

data = np.array(data)

diffs = data[1] - data[0]

plt.scatter(data[0], diffs, marker=".")
plt.xlabel("Red px value no neg. prompt")
plt.ylabel("Diff red px value from neg. prompt")
plt.savefig("negative_prompt_scatter_plot.png", dpi=240)

num_bins = 8
bin_size = 10
hist_low = 80
bin_edges = np.arange(hist_low, hist_low+bin_size*num_bins+1, bin_size)
x_data = 0.5 * (bin_edges[1:] + bin_edges[:-1])

y_data = []
y_err = []
for i in range(num_bins):
    diffs_i = diffs[np.logical_and(data[0] >= bin_edges[i], data[0] < bin_edges[i + 1])]
    y_data.append(np.mean(diffs_i))
    y_err.append(np.std(diffs_i) / np.sqrt(len(diffs_i)))
y_data = np.array(y_data)
y_err = np.array(y_err)


fit = XYFit([x_data, y_data])
fit.add_error("x", 0.25*bin_size)
fit.add_error("y", y_err)
fit.do_fit()
fit.report()

plot = Plot(fit)
plot.x_label = "Red px value no neg. prompt"
plot.y_label = "Diff red px value from neg. prompt"
plot.plot(asymmetric_parameter_errors=True)
plot.save("negative_prompt_fit.png", dpi=240)
plot.show()
