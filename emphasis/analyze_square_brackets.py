#!/usr/bin/env python3

import os
import numpy as np
import imageio as iio
from kafe2 import XYFit, Plot

SAMPLE_DIR = "data"
PROMPTS = [
#    "Flowers, red, blue",
#    "Flowers, (red), blue",
#    "Flowers, ((red)), blue",
#    "Flowers, (((red))), blue",
#    "Flowers, ((((red)))), blue",
#    "Flowers, (((((red))))), blue",
#    "Flowers, ((((((red)))))), blue",
#    "Flowers, [red], blue",
#    "Flowers, [[red]], blue",
#    "Flowers, [[[red]]], blue",
#    "Flowers, [[[[red]]]], blue",
#    "Flowers, [[[[[red]]]]], blue",
#    "Flowers, [[[[[[red]]]]]], blue",
#    "Flowers, [[[[[[[red]]]]]]], blue",
#    "Flowers, [[[[[[[[red]]]]]]]], blue",
    "Flowers, blue, red",
    "Flowers, blue, [red]",
    "Flowers, blue, [[red]]",
    "Flowers, blue, [[[red]]]",
    "Flowers, blue, [[[[red]]]]",
    "Flowers, blue, [[[[[red]]]]]",
    "Flowers, blue, [[[[[[red]]]]]]",
    "Flowers, blue, [[[[[[[red]]]]]]]",
    "Flowers, blue, [[[[[[[[red]]]]]]]]",
]

x_data = np.arange(1, len(PROMPTS))
diffs = []

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
    if i == 0:
        means_0 = means_i
    else:
        diffs_i = means_i - means_0
        diffs.append(diffs_i)

diffs = np.array(diffs)
y_data = np.mean(diffs, axis=1)
y_cov_mat = np.cov(diffs) / diffs.shape[1]

fit = XYFit([x_data, y_data])
fit.add_matrix_error("y", y_cov_mat, "cov")
#fit.fix_parameter("a", 0)
#fit.fix_parameter("b", 0)
fit.do_fit()
fit.report()

plot = Plot(fit)
plot.x_label = "Number of square brackets"
plot.y_label = "Mean red pixel value diff"
plot.plot()
plot.save("square_brackets.png", dpi=240)
plot.show()
