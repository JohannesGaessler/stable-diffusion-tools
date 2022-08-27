#!/usr/bin/env python3

import os
import numpy as np
import imageio as iio
from kafe2 import XYFit, Plot

SAMPLE_DIR = "data"
PROMPTS = [
    "Flowers, red, blue",
    "Flowers, [red], blue",
    "Flowers, [[red]], blue",
    "Flowers, [[[red]]], blue",
    "Flowers, [[[[red]]]], blue",
    "Flowers, [[[[[red]]]]], blue",
]

x_data = np.arange(len(PROMPTS))
y_data = []
y_error = []

for prompt in PROMPTS:
    prompt_dir = os.path.join(SAMPLE_DIR, prompt)
    means = []
    file_list = os.listdir(prompt_dir)
    num_samples = len(file_list)
    for filename in file_list:
        if not filename.endswith(".png"):
            continue
        image = iio.v3.imread(os.path.join(prompt_dir, filename))
        red = np.mean(image[:, :, 0])
        means.append(red)
    y_data.append(np.mean(means))
    y_error.append(np.std(means) / np.sqrt(num_samples))


fit = XYFit([x_data, y_data])
fit.add_error("y", y_error)
fit.do_fit()

plot = Plot(fit)
plot.x_label = "Number of square  brackets PRELIMINARY RESULT"
plot.y_label = "Mean red pixel value PRELIMINARY RESULT"
plot.plot()
plot.show()
