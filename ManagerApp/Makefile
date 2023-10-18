CUDA_DIR := /usr/local/cuda-11.4
INCLUDE := -I/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/bfs
LIB_DIR := -L/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/bfs -L/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/lud/cuda
LIBS := -lbfs -llud

manager: managerApp.cu parseLine.cu simultExecution.cu
	    $(CUDA_DIR)/bin/nvcc -o managerApp managerApp.cu parseLine.cu simultExecution.cu $(INCLUDE) $(LIB_DIR) $(LIBS)



clean:
	    rm -f managerApp
