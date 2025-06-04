#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import os
import sys
from argparse import ArgumentParser

# Path to the MipNerf dataset
mipnerf360 = "/dataset/MipNerf360"

mipnerf360_outdoor_scenes = ["bicycle", "flowers", "garden", "stump", "treehill"]
mipnerf360_indoor_scenes = ["room", "counter", "kitchen", "bonsai"]

python_path = sys.executable

skip_training = False
skip_rendering = False
skip_metrics = False

lambda_converge = 7.0
seed = 1111

all_scenes = []
all_scenes.extend(mipnerf360_outdoor_scenes)
all_scenes.extend(mipnerf360_indoor_scenes)

output_path = f"./eval/mipnerf360/{seed}"

if not skip_training:
    common_args = " ".join([
        "--quiet",
        "--test_iterations -1",
        "--eval", # Only required when NVS
        "--lambda_dist 0",
        f"--lambda_converge {lambda_converge}",
        "--densify_until_iter 20000",
        f"--seed {seed}"
    ])
    for scene in mipnerf360_outdoor_scenes:
        source = mipnerf360 + "/" + scene
        os.system(python_path + " train.py -s " + source + " -m " + output_path + "/" + scene + " " + common_args + " -r 4 ")
    for scene in mipnerf360_indoor_scenes:
        source = mipnerf360 + "/" + scene
        os.system(python_path + " train.py -s " + source + " -m " + output_path + "/" + scene + " " + common_args + " -r 2 ")

if not skip_rendering:
    all_sources = []
    for scene in mipnerf360_outdoor_scenes:
        all_sources.append(mipnerf360 + "/" + scene)
    for scene in mipnerf360_indoor_scenes:
        all_sources.append(mipnerf360 + "/" + scene)

    common_args = " ".join([
            "--quiet",
            "--skip_train",  # Skip rendering training images
            # "--skip_mesh", # Skip mesh extraction
            f"--eval",
            f"--voxel_size 0.004",
            f"--sdf_trunc 0.04",
            f"--depth_trunc 6.0"
        ])
    for scene, source in zip(all_scenes, all_sources):
        os.system(python_path + " render.py --iteration 30000 -s " + source + " -m " + output_path + "/" + scene + " " + common_args)

if not skip_metrics:
    scenes_string = ""
    for scene in all_scenes:
        scenes_string += "\"" + output_path + "/" + scene + "\" "
    
    os.system(python_path + " metrics.py -m " + scenes_string)