#!/usr/bin/env bash

# Clone the openpose repo
mkdir ./algorithms_files
cd ./algorithms_files
git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
cd ./openpose
git submodule update --init --recursive

# Clone the caffe repo
cd ./3rdparty
git clone https://github.com/CMU-Perceptual-Computing-Lab/caffe.git

# Clone pybind
git clone https://github.com/pybind/pybind11.git