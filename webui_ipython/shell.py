#!/usr/bin/env python3

from collections import OrderedDict

import webui


kwargs_txt2img = OrderedDict(
    prompt="",
    negative_prompt="",
    steps=20,
    sampler_index=0,
    use_GFPGAN=False,
    tiling=False,
    n_iter=9,
    batch_size=1,
    cfg_scale=10.0,
    seed=42,
    height=512,
    width=512,
)


def set(**kwargs):
    kwargs_txt2img.update(kwargs)


def queue():
    args = list(kwargs_txt2img.values())
    args.append(0)
    webui.modules.txt2img.txt2img(*args)
