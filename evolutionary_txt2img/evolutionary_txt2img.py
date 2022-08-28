#!/usr/bin/env python3

import os
import yaml
import random
from copy import deepcopy

import numpy as np

from scripts import webui

config_path = webui.opt.cli

with open(config_path, "r", encoding="utf8") as f:
    config = yaml.safe_load(f)

outdir = config.pop("outdir")
os.makedirs(outdir, exist_ok=True)
webui.opt.outdir = outdir
min_population_for_crossbreed = config.pop("min_population_for_crossbreed")


def mutate(sample_spec):
    for key in sample_spec.keys():
        if key == "ddim_steps":
            sample_spec[key] = int(sample_spec[key] * np.random.normal(loc=0.95, scale=0.1))
        elif key in ["ddim_eta", "cfg_scale"]:
            sample_spec[key] *= np.random.normal(loc=1.0, scale=0.1)
    keyword_list = sample_spec["keyword_list"]
    num_keywords = len(keyword_list)
    if num_keywords > 2:
        i1, i2 = random.sample(range(len(keyword_list)), 2)
        keyword_list[i1], keyword_list[i2] = keyword_list[i2], keyword_list[i1]

    random_extra_keyword = random.sample(config["prompt"]["maybe"], 1)[0]
    if random_extra_keyword not in keyword_list:
        keyword_list.append(random_extra_keyword)

    sample_spec["keyword_list"] = keyword_list
    return sample_spec


def crossbreed(sample_specs):
    if len(sample_specs) < min_population_for_crossbreed:
        sample_spec = deepcopy(config)
        sample_spec["rating"] = 0
        prompt = sample_spec.pop("prompt")
        keyword_list = prompt["always"]
        for keyword in prompt["maybe"]:
            if np.random.rand() < 0.5:
                keyword_list.append(keyword)
        random.shuffle(keyword_list)
    else:
        sample_spec = {}

        ratings = np.array([ss["rating"] for ss in sample_specs], dtype=float)
        random_indices = np.random.permutation(ratings.shape[0])[:4]
        ratings = ratings[random_indices]
        sample_specs = [sample_specs[ri] for ri in random_indices]
        ratings_argmax = np.argmax(ratings)
        sample_spec_1 = sample_specs[ratings_argmax]
        ratings[ratings_argmax] = -np.inf
        ratings_argmax = np.argmax(ratings)
        sample_spec_2 = sample_specs[ratings_argmax]

        keyword_list_1 = sample_spec_1["keyword_list"]
        keyword_list_2 = sample_spec_2["keyword_list"]
        keyword_list = []
        while(keyword_list_1 or keyword_list_2):
            if keyword_list_1 and keyword_list_2:
                if np.random.rand() < 0.5:
                    rand_kl_1 = keyword_list_1
                    rand_kl_2 = keyword_list_2
                else:
                    rand_kl_1 = keyword_list_2
                    rand_kl_2 = keyword_list_1

                keyword = rand_kl_1.pop(0)
                p_bonus = 0.5 if keyword in rand_kl_2 else 0.0
            elif keyword_list_1:
                keyword = keyword_list_1.pop(0)
                p_bonus = 0.0
            else:
                keyword = keyword_list_2.pop(0)
                p_bonus = 0.0
            if keyword in config["prompt"]["always"]:
                p_bonus += 1.0
            if keyword not in keyword_list and np.random.rand() < 0.45 + p_bonus:
                keyword_list.append(keyword)
        for key in sample_spec_1.keys():
            sample_spec[key] = random.choice([sample_spec_1, sample_spec_2])[key]

    sample_spec["keyword_list"] = keyword_list
    sample_spec["seed"] = webui.seed_to_int(config["seed"])
    return sample_spec


while True:
    sample_spec_file_names = [f for f in os.listdir(outdir) if f.endswith(".yaml")]
    sample_specs = []
    for fn in sample_spec_file_names:
        with open(os.path.join(outdir, fn), "r", encoding="utf8") as f:
            sample_specs.append(yaml.safe_load(f))
    crossbred_spec = crossbreed(sample_specs)
    mutated_spec = mutate(crossbred_spec)

    txt2img_kwargs = deepcopy(mutated_spec)
    txt2img_kwargs["prompt"] = config["prompt"]["start"] + ", " + ", ".join(txt2img_kwargs.pop("keyword_list"))
    txt2img_kwargs.pop("rating")

    sanitized_prompt = txt2img_kwargs["prompt"].replace(' ', '_').translate(
        {ord(x): '' for x in webui.invalid_filename_chars})[:128]
    filename = f"grid-{len(sample_specs):05}-{mutated_spec['seed']}_{sanitized_prompt}.yaml"
    print(f"===== {txt2img_kwargs['prompt']} =====")
    output_images, seed, info, stats = webui.txt2img(**txt2img_kwargs)
    print(f'Seed: {seed}')
    print(info)
    print(stats)
    print()
    with open(os.path.join(outdir, filename), "w", encoding="utf8") as f:
        f.write("# Human-readable prompt: ")
        f.write(txt2img_kwargs["prompt"])
        f.write("\n\n")
        yaml.dump(mutated_spec, f)
