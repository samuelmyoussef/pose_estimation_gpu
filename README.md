# Pose Estimation Using Openpose on a Flask Server

## Overview

This repository is based on the [Openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) multi-person detection library. It uses the body model to perform body pose estimation. The flask server implementation is based on the [flask-openpose](https://github.com/haris-o/flask-openpose) repo.


## NVIDIA Dependencies
You need to install the NVIDIA drivers for your GPU with the compatible CUDA and cudnn. Follow this [guide](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html)

You also need to install the [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)

## Installation
You can setup the repository using a docker image by running the following commands:
```bash
git clone https://github.com/samuelmyoussef/pose_estimation_gpu.git
cd pose_estimation_gpu
bash ./setup.sh
docker build . -t <image_name:tag>
```

## Running the Server
To run the server, run the docker container:
`docker run --gpus all --rm -it --network host <image_name:tag>`

It will run the server on localhost and expose port 5001.
To use the server, navigate to `localhost:5001`.

## APIs
* `/analyse_image` for image inference

## Model Details
For more information about the underlying models, check the OpenPose repository.

## License

This software is licensed for academic or non-profit organization non-commercial research use only according to the OpenPose repository licensing.

## Contact

For any inquires, please contact [Samuel Youssef](samuelm.youssef@gmail.com)