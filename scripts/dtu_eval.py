import os
import json
import time

if __name__ == '__main__':

    #dtu_scenes = ['scan24', 'scan37', 'scan40', 'scan55', 'scan63', 'scan65', 'scan69', 'scan83', 'scan97', 'scan105', 'scan106', 'scan110', 'scan114', 'scan118', 'scan122']
    dtu_scenes = ['scan63']

    all_scenes = []
    all_scenes.extend(dtu_scenes)  

    python_path = "C:/Users/YangYixin/.conda/envs/unbiased_2DGS/python"
    output_path = os.path.join(".", "eval", "dtu")
    GS2D_dtu_path = "D:/dataset/DTU_2DGS"
    DTU_Official = "D:/dataset/MVS_Official_Dataset/SampleSet/MVS_Data"

    skip_training = False
    skip_rendering = False
    skip_metrics = False

    densify_until_iter = 20000  # 20000 # 在这之前都要执行 densify
    iterations = 30000          # 30000

    lambda_normal = 0.05        # 
    lambda_dist = 0             # 2D_GS Depth Distortion Loss
    lambda_converge = 7.0       # Converge Loss
    seed = 1111 
    assert densify_until_iter < iterations

    for scene in dtu_scenes:
        # ---------------------- Train ----------------------
        if not skip_training:
            common_args = " ".join([
                "--quiet",
                f"--depth_ratio 1.0",
                f"-r 2",
                f"--test_iterations {iterations}",
                f"--save_iterations {iterations}",
                f"--lambda_normal {lambda_normal}",
                f"--lambda_dist {lambda_dist}",
                f"--lambda_converge {lambda_converge}",
                f"--iterations {iterations}",
                f"--densify_until_iter {densify_until_iter}",
                f"--seed {seed}",
                # f"--logger_enabled", # TODO 开启 logger
            ])

            source = GS2D_dtu_path + "/" + scene

            cmd = python_path + " train.py -s " + source + " -m " + output_path + "/" + scene + " " + common_args
            os.system(cmd)

        # ---------------------- Extract Mesh ----------------------
        if not skip_rendering:
            all_sources = []
            common_args = " ".join([
                "--quiet",
                "--skip_train",
                f"--depth_ratio 1.0",
                f"--num_cluster 1",
                f"--voxel_size 0.004",
                f"--sdf_trunc 0.016",
                f"--depth_trunc 3.0",
            ])
            source = GS2D_dtu_path + "/" + scene
            cmd = python_path + \
                f" render.py --iteration {iterations} -s " + \
                source + " -m" + output_path + "/" + scene + " " + common_args
            os.system(cmd)

        # ------------------------ Evaluate ------------------------
        if not skip_metrics:
            scan_id = scene[4:]

            # Make output directory
            output_eval_path = os.path.join(output_path, scene, 'eval')
            os.makedirs(output_eval_path, exist_ok=True)

            script_dir = os.path.dirname(os.path.abspath(__file__))  
            
            # Run evaluate_single_scene.py
            cmd = " ".join([
                python_path,
                f"{script_dir}/eval_dtu/evaluate_single_scene.py",
                f"--input_mesh {output_path}/{scene}/train/ours_{iterations}/fuse_post.ply",
                f"--scan_id {scan_id}",
                f"--output_dir {output_eval_path}",
                f"--mask_dir {GS2D_dtu_path}",
                f"--DTU {DTU_Official}",
            ])
            os.system(cmd)

