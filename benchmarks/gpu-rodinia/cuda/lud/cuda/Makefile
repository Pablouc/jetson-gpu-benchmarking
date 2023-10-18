CC = gcc
NVCC = nvcc

DEFS += \
			-DGPU_TIMER \
					$(SPACE)

NVCCFLAGS += -I../common \
	     			 -O3 \
				 			 -use_fast_math \
							 			 -arch=sm_72 \
										 			 -lm \
													 			 $(SPACE)

CFLAGS += -I../common \
	  					-I/usr/include/cuda \
								  -O3 \
								  		  -Wall \
										  		  $(SPACE)

# Add source files here
EXECUTABLE  := lud_cuda
# # Cuda source files (compiled with cudacc)
CUFILES     := lud_kernel.cu
# # C/C++ source files (compiled with gcc / c++)
CCFILES     := lud.c lud_cuda.c ../common/common.c

OBJS = lud.o lud_kernel.o ../common/common.o

LIBRARY = liblud.a

.PHONY: all clean

all: $(LIBRARY)

$(LIBRARY): $(OBJS)
	ar rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) $(DEFS) -o $@ -c $<

%.o: %.cu
	$(NVCC) $(NVCCFLAGS) $(DEFS) -o $@ -c $<

clean:
	rm -f $(LIBRARY) $(OBJS)

