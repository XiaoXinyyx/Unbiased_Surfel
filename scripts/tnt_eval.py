import os
import sys
from argparse import ArgumentParser

tnt_360_scenes = ['Barn', 'Caterpillar', 'Ignatius', 'Truck']
tnt_large_scenes = ['Meetingroom', 'Courthouse']
tnt_360_scenes = ['Caterpillar', 'Ignatius', 'Truck']
tnt_large_scenes = []

python_path = sys.executable
TNT_data = "D:\\dataset\\TNT_GOF\\TrainingSet"

lambda_converge = 7.0
iteration = 30000
seed = 8887

skip_training = False
skip_rendering = False
skip_metrics = True

parser = ArgumentParser(description="Full evaluation script parameters")
parser.add_argument("--output_path", default="./eval/tnt")
args, _ = parser.parse_known_args()

if not skip_metrics:
    parser.add_argument('--TNT_GT', required=True, type=str)
    args = parser.parse_args()


if not skip_training:
    common_args = " ".join([
        " --quiet",
        "--test_iterations -1",
        "--depth_ratio 1.0",
        "-r 2",
        "--lambda_dist 0",
        "--lambda_centrate 0",
        f"--lambda_converge {lambda_converge}",
        "--densify_until_iter 20000",
        f"--seed {seed}"
    ])
    
    for scene in tnt_360_scenes:
        source = TNT_data + "/" + scene
        cmd = python_path + " train.py -s " + source + " -m " + args.output_path + "/" + scene + common_args
        print(cmd)
        os.system(cmd)

    for scene in tnt_large_scenes:
        source = TNT_data + "/" + scene
        cmd = python_path + " train.py -s " + source + " -m " + args.output_path + "/" + scene + common_args
        print(cmd)
        os.system(cmd)


if not skip_rendering:
    all_sources = []
    common_args = " ".join([
        " --quiet",
        "--skip_train",      # Skip rendering training images
        "--depth_ratio 1.0",
    ])

    for scene in tnt_360_scenes:
        source = TNT_data + "/" + scene
        cmd = python_path + " render.py --iteration 30000 -s " + source + " -m " + args.output_path + "/" + scene + common_args + ' --num_cluster 1 --voxel_size 0.004 --sdf_trunc 0.016 --depth_trunc 3.0'
        print(cmd)
        os.system(cmd)

    for scene in tnt_large_scenes:
        source = TNT_data + "/" + scene
        cmd = python_path + " render.py --iteration 30000 -s " + source + " -m " + args.output_path + "/" + scene + common_args + ' --num_cluster 1 --voxel_size 0.006 --sdf_trunc 0.024 --depth_trunc 4.5'
        print(cmd)
        os.system(cmd)

if not skip_metrics:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    all_scenes = tnt_360_scenes + tnt_large_scenes

    for scene in all_scenes:
        ply_file = f"{args.output_path}/{scene}/train/ours_{iteration}/fuse_post.ply"
        string = f"OMP_NUM_THREADS=4 {python_path} {script_dir}/eval_tnt/run.py " + \
            f"--dataset-dir {args.TNT_GT}/{scene} " + \
            f"--traj-path {TNT_data}/{scene}/{scene}_COLMAP_SfM.log " + \
            f"--ply-path {ply_file}"
        print(string)
        os.system(string)