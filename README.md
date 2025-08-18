<p align="center">

  <h1 align="center">Introducing Unbiased Depth into 2D Gaussian Splatting for
  High-accuracy Surface Reconstruction</h1>
  <p align="center">
    <a>Yixin Yang</a>
    ·
    <a href="https://zhouyangvcc.github.io/">Yang Zhou</a>
    ·
    <a href="https://vcc.tech/~huihuang">Hui Huang</a>
  </p>


  <div align="center">
 <a href='https://arxiv.org/abs/2503.06587'><img src='https://img.shields.io/badge/arXiv-2503.06587-b31b1b.svg'></a> &nbsp;&nbsp;
 <a href='https://xiaoxinyyx.github.io/unbiased-gs/'><img src='https://img.shields.io/badge/Project-Page-Green'></a>
</div>

</p>


<p align="center">
  <a href="">
    <img src="./assets/teaser.png" alt="Logo" width="95%">
  </a>
</p>

<p align="center">
We introduce unbiased depth into 2DGS, effectively solving the holes in specular highlight regions and significantly improving the geometry quality of surface reconstruction.
</p>
<br>

# Installation
Clone the repository and create an anaconda environment using
```
git clone git@github.com:XiaoXinyyx/Unbiased_Surfel.git --recursive

# if you have an environment used for 2dgs/3dgs, use it
# if not, create a new environment
conda env create --file environment.yml
conda activate unbiased_surfel

# We modified the cuda rasterizer
cd Unbiased_Surfel
pip install ./submodules/diff-surfel-rasterization
```

# Training

To train a scene, simply use

```
python train.py -s <path to COLMAP or NeRF Synthetic dataset>
```

Commandline arguments for regularizations
```
--lambda_normal   # hyperparameter for normal consistency
--lambda_converge # hyperparameter for depth converge (Ours)
--lambda_dist     # hyperparameter for depth converge (2DGS)
```

# Testing
## Bounded Mesh Extraction
To export a mesh within a bounded volume, simply use
```
python render.py -m <path to pre-trained model> -s <path to COLMAP dataset> 
```
Commandline arguments you should adjust accordingly for meshing for bounded TSDF fusion, use
```
--voxel_size # voxel size
--depth_trunc # depth truncation
```
If these arguments are not specified, the script will automatically estimate them using the camera information.

## Unbounded Mesh Extraction
To export a mesh with an arbitrary size, we devised an unbounded TSDF fusion with space contraction and adaptive truncation.
```
python render.py -m <path to pre-trained model> -s <path to COLMAP dataset> --mesh_res 1024
```

# Full evaluation

We provide scripts to evaluate our method on [Mip-NeRF 360](https://jonbarron.info/mipnerf360/), [Tanks and Template](https://www.tanksandtemples.org/download/) and [DTU](https://drive.google.com/drive/folders/1SJFgt8qhQomHX55Q4xSvYE2C6-8tFll9) dataset.
```
# DTU dataset
python scripts/dtu_eval.py

# Mip-NeRF 360 dataset
python scripts/m360_eval.py

# Tanks and Template dataset
python scripts/tnt_eval.py
```

# Acknowledgements
This project is built upon [2DGS](https://github.com/hbb1/2d-gaussian-splatting) and [3DGS](https://github.com/graphdeco-inria/gaussian-splatting). The TSDF fusion for extracting mesh is based on [Open3D](https://github.com/isl-org/Open3D). The rendering script for MipNeRF360 is adopted from [Multinerf](https://github.com/google-research/multinerf/), while the evaluation scripts for DTU and Tanks and Temples dataset are built apon [DTUeval-python](https://github.com/jzhangbs/DTUeval-python) and [TanksAndTemples](https://github.com/isl-org/TanksAndTemples/tree/master/python_toolbox/evaluation), respectively. The fusing operation for accelerating the renderer is inspired by [Han's repodcue](https://github.com/Han230104/2D-Gaussian-Splatting-Reproduce). We thank all the authors for their great work and repos. 

# Citation
If you find our code or paper useful, please cite



```bibtex
@misc{peng2025introducing,
    title={Introducing Unbiased Depth into 2D Gaussian Splatting for High-accuracy Surface Reconstruction},
    author={Yixin Yang and Yang Zhou and Hui Huang},
    year={2025},
    eprint={2503.06587},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```
