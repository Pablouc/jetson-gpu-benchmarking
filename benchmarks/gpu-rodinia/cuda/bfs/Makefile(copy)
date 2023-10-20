include /home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/common/make.config

CUDA_LIB_DIR = /usr/local/cuda-11.4/targets/aarch64-linux/lib/
CC := $(CUDA_DIR)/bin/nvcc
INCLUDE := $(CUDA_DIR)/include
UTIL := /home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/util
SRC = /home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/bfs/bfs.cu
OBJ = bfs.o  # Object file name
LIB = libbfs.a  # Static library name

all: $(LIB)

$(OBJ): $(SRC)
		$(CC) -c $(SRC) -o $(OBJ) -I$(INCLUDE) -I$(UTIL) -DTIMING

$(LIB): $(OBJ)
		ar rcs $(LIB) $(OBJ)
			rm -f $(OBJ)

release: $(LIB)

clean:
		rm -f $(LIB) $(OBJ) $(EXE) $(EXE).linkinfo result.txt

