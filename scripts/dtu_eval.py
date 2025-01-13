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
    skip_metrics = True

    densify_until_iter = 20000  # 20000 # 在这之前都要执行 densify
    iterations = 30000          # 30000

    lambda_normal = 0.05        # 7000 轮后开始
    lambda_dist = 0             # 2D_GS Depth Distortion Loss 1000
    lambda_converge = [7.0]     # 7.0 
    seeds = [8888] # [x for x in range(8880, 8888)]
    assert densify_until_iter < iterations

    # Start timer
    start_time = time.time()

    for lconverge in lambda_converge:
        for seed in seeds:
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
                        f"--lambda_converge {lconverge}",
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

                    script_dir = os.path.dirname(os.path.abspath(__file__))  
                    eval_output_dir = os.path.join(script_dir, "tmp",
                        f"scan{scan_id}_s{seed}_iter{iterations}_conv{lconverge:.1f}")
                    
                    cmd = " ".join([
                        python_path,
                        f"{script_dir}/eval_dtu/evaluate_single_scene.py",
                        f"--input_mesh {output_path}/{scene}/train/ours_{iterations}/fuse_post.ply",
                        f"--scan_id {scan_id}",
                        f"--output_dir", eval_output_dir,
                        f"--mask_dir {GS2D_dtu_path}",
                        f"--DTU {DTU_Official}",
                    ])

                    os.system(cmd)

                    # 将 PSNR 和 l1 写入 results.json
                    output_json_path = os.path.join(output_path, scene, "output.json")
                    result_json_path = os.path.join(eval_output_dir, 'results.json')
                    if os.path.exists(output_json_path) and os.path.exists(result_json_path):
                        with open(output_json_path, 'r') as file:
                            data = json.load(file)
                        # 获取 score 参数
                        psnr = data['train'].get(f'{iterations}_psnr', 0.0)
                        l1_loss = data['train'].get(f'{iterations}_l1', 0.0)

                        with open(result_json_path, 'r') as file:
                            result_data = json.load(file)
                        result_data['psnr'] = psnr
                        result_data['l1'] = l1_loss
                        with open(result_json_path, 'w') as file:
                            json.dump(result_data, file)

                    # 读取 Chamfer Distance
                    score = result_data.get('overall', 0.0)

                    # 拷贝渲染图片
                    os.makedirs(os.path.join(eval_output_dir, "render"))
                    render_img_src = os.path.join(output_path, scene, "train", f"ours_{iterations}", "renders")
                    render_img_dst = os.path.join(eval_output_dir, "render")
                    os.system(f"xcopy {render_img_src} {render_img_dst} /E")

                    # 重命名 output_dir
                    if os.path.exists(eval_output_dir) and score >= 0:
                        new_output_dir = eval_output_dir + f"_{score:.2f}_PSNR_{psnr:.2f}"
                        os.rename(eval_output_dir, new_output_dir)

    # end timer
    end_time = time.time()
    print("Time elapsed: ", end_time - start_time)
