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

mipnerf360_outdoor_scenes = ["bicycle", "flowers", "garden", "stump", "treehill"]
mipnerf360_indoor_scenes = ["room", "counter", "kitchen", "bonsai"]
mipnerf360_outdoor_scenes = ["flowers", "garden", "stump", "treehill"]
mipnerf360_indoor_scenes = ["room", "counter", "kitchen", "bonsai"]

python_path = sys.executable
mipnerf360 = "D:/dataset/MipNerf360"

skip_training = True
skip_rendering = False
skip_metrics = False

lambda_converge = 7.0
seeds = [8888]

all_scenes = []
all_scenes.extend(mipnerf360_outdoor_scenes)
all_scenes.extend(mipnerf360_indoor_scenes)

for seed in seeds:

    output_path = f"./eval/mipnerf360/{seed}"

    if not skip_training:
        common_args = " ".join([
            "--quiet",
            "--test_iterations -1",
            "--depth_ratio 1.0",
            # "-r 2",
            "--lambda_dist 0",
            "--lambda_centrate 0",
            f"--lambda_converge {lambda_converge}",
            "--densify_until_iter 20000",
            f"--seed {seed}"
        ])
        for scene in mipnerf360_outdoor_scenes:
            source = mipnerf360 + "/" + scene
            os.system(python_path + " train.py -s " + source + " -i images_4 -m " + output_path + "/" + scene + " " + common_args)
        for scene in mipnerf360_indoor_scenes:
            source = mipnerf360 + "/" + scene
            os.system(python_path + " train.py -s " + source + " -i images_2 -m " + output_path + "/" + scene + " " + common_args)

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
                f"--depth_ratio 1.0",
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