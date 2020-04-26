FROM nvidia/cuda:10.2-cudnn7-devel


# Dependencies
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
python3-dev python3-pip git g++ wget make libprotobuf-dev protobuf-compiler libopencv-dev \
libgoogle-glog-dev libboost-all-dev libcaffe-cuda-dev libhdf5-dev libatlas-base-dev

RUN pip3 install numpy opencv-python

RUN pip3 install flask flask-restful


# Cmake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.0/cmake-3.16.0-Linux-x86_64.tar.gz && \
	tar xzf cmake-3.16.0-Linux-x86_64.tar.gz -C /opt && \
	rm cmake-3.16.0-Linux-x86_64.tar.gz
ENV PATH="/opt/cmak/e-3.16.0-Linux-x86_64/bin:${PATH}"


# OpenPose
WORKDIR /app
COPY . /app


# Build
RUN cd ./algorithms_files/openpose && \
mkdir build && \
cd ./build && \
cmake ../ -DBUILD_PYTHON=ON && \
make -j`nproc` && \
make install


RUN cd /app


# expose the port used
EXPOSE 5001


# start the app
CMD ["python3", "main.py"]