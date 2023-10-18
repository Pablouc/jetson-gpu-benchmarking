/*
 * =====================================================================================
 *
 *       Filename:  lud.cu
 *
 *    Description:  The main wrapper for the suite
 *
 *        Version:  1.0
 *        Created:  10/22/2009 08:40:34 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Liang Wang (lw2aw), lw2aw@virginia.edu
 *        Company:  CS@UVa
 *
 * =====================================================================================
 */

#include <cuda.h>
#include <stdio.h>
#include <unistd.h>
#include <getopt.h>
#include <stdlib.h>
#include <assert.h>
#include "lud.h"
#include "common.h"
#include <cuda_runtime_api.h>
#include <cuda_runtime.h>


#ifdef TIMING
#include "timing.h"
#endif

#ifdef RD_WG_SIZE_0_0
        #define BLOCK_SIZE RD_WG_SIZE_0_0
#elif defined(RD_WG_SIZE_0)
        #define BLOCK_SIZE RD_WG_SIZE_0
#elif defined(RD_WG_SIZE)
        #define BLOCK_SIZE RD_WG_SIZE
#else
        #define BLOCK_SIZE 16
#endif



static int do_verify = 0;

static struct option long_options[] = {
  /* name, has_arg, flag, val */
  {"input", 1, NULL, 'i'},
  {"size", 1, NULL, 's'},
  {"verify", 0, NULL, 'v'},
  {0,0,0,0}
};

extern void
lud_cuda(float *d_m, int matrix_dim, cudaStream_t stream);

#ifdef TIMING
struct timeval tv;
struct timeval tv_total_start, tv_total_end;
struct timeval tv_h2d_start, tv_h2d_end;
struct timeval tv_d2h_start, tv_d2h_end;
struct timeval tv_kernel_start, tv_kernel_end;
struct timeval tv_mem_alloc_start, tv_mem_alloc_end;
struct timeval tv_close_start, tv_close_end;
float init_time = 0, mem_alloc_time = 0, h2d_time = 0, kernel_time = 0,
      d2h_time = 0, close_time = 0, total_time = 0;
#endif

void lud_main(const char* input_file, int matrix_dim, int do_verify,  cudaStream_t stream) {

	printf("WG size of kernel = %d X %d\n", BLOCK_SIZE, BLOCK_SIZE);
	func_ret_t ret;
	float *m, *d_m, *mm;
        stopwatch sw;

	if (input_file) {

		printf("Reading matrix from file %s\n", input_file);
		ret = create_matrix_from_file(&m, input_file, &matrix_dim);

		if (ret != RET_SUCCESS) {

			m = NULL;
			fprintf(stderr, "error create matrix from file %s\n", input_file);
			exit(EXIT_FAILURE);

		}

	} else if (matrix_dim) {

		printf("Creating matrix internally size=%d\n", matrix_dim);
		ret = create_matrix(&m, matrix_dim);
		
		if (ret != RET_SUCCESS) {

			m = NULL;
			fprintf(stderr, "error create matrix internally size=%d\n", matrix_dim);
			exit(EXIT_FAILURE);

		}

	} else {

		printf("Invalid input parameters!\n");
		exit(EXIT_FAILURE);
	
	}

	if (do_verify) {

		printf("Before LUD\n");
		// print_matrix(m, matrix_dim);
		matrix_duplicate(m, &mm, matrix_dim);

	}

	cudaMalloc((void**)&d_m, matrix_dim * matrix_dim * sizeof(float));
	cudaMemcpy(d_m, m, matrix_dim * matrix_dim * sizeof(float), cudaMemcpyHostToDevice);



       	stopwatch_start(&sw); // Start the stopwatch

#ifdef TIMING
	gettimeofday(&tv_kernel_start, NULL);
#endif


	lud_cuda(d_m, matrix_dim, stream);

#ifdef TIMING
	gettimeofday(&tv_kernel_end, NULL);
	tvsub(&tv_kernel_end, &tv_kernel_start, &tv);
	kernel_time += tv.tv_sec * 1000.0 + (float)tv.tv_usec / 1000.0;
#endif


	cudaMemcpy(m, d_m, matrix_dim * matrix_dim * sizeof(float), cudaMemcpyDeviceToHost);
	cudaFree(d_m);

	stopwatch_stop(&sw); // Stop the stopwatch

	if (do_verify) {

		printf("After LUD\n");
		// print_matrix(m, matrix_dim);
		printf(">>>Verify<<<<\n");
		lud_verify(mm, m, matrix_dim);
		free(mm);

	}


	free(m);

#ifdef TIMING
	printf("Exec: %f\n", kernel_time);
#endif

	printf("Time consumed(ms): %lf\n", 1000 * get_interval_by_sec(&sw));
}

