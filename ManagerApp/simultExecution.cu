#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include <iostream>
#include <cuda_runtime.h>
#include "structs.h"
#include "simultExecution.h"

using namespace std;
#include "/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/bfs/bfs.h"
#include "/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/lud/cuda/lud.h"

// Workloads Paths
char* bfsWorkloadPath = "/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/data/bfs/"; //graph65536.txt





int simultExecution(Configuration& config) {

// Print or use the configuration variables here

	     	cout << "Simult: " << config.simult << endl;
			cout << "Blocks: " << config.blocks << endl;
				cout << "Threads: " << config.threads << endl;
					cout << "Frequency: " << config.frequency << endl;

   char* concatenatedPath = new char[200];


   //Verify how many apps to execute
   int appsCount = 0;
  
   /* for (int i = 0; i < ; ++i) {
	   // Check if the app at index i is non-empty
	   if (config.apps[i][0] != '\0') {
		   appsCount++;
	   }
	   cout <<" app iteration"<< i <<endl;
   }*/


   // Allocate an array of cudaStream_t
    cudaStream_t* streams = new cudaStream_t[config.appsNum];
   

 // Initialize each stream
     for (int i = 0; i < config.appsNum ; i++){	  
	     cudaStreamCreate(&streams[i]); // Create a new stream and store its handle in the array
     }


  // Events for measuring time
   cudaEvent_t start, stop;
   cudaEventCreate(&start);
   cudaEventCreate(&stop);

   for( int i = 0 ; i < config.appsNum; i++){

	   cudaEventRecord(start);
           
	   if(strcmp(config.apps[i], "bfs") == 0 ){
		   strcpy(concatenatedPath, bfsWorkloadPath);
		   strcat(concatenatedPath, config.workloads[i]);
		   cout << "ConcatenatedPath: " << concatenatedPath << endl;
		   BFSGraph(concatenatedPath, config.blocks, config.threads, streams[i]);

	   } 

	   const char* input_file = NULL;  // Set your input file name
	   int matrix_dim = 768;  // Set your matrix dimension
	   int do_verify = 1;
	   char makeCommand[200]; // adjust the size according to your needs
	       
	   int rdWgSizeValue = 64; // The value you want to set for RD_WG_SIZE_0_0

	    int cleanResult = system("make -C /home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/lud/cuda/ clean");

	           
	       // Construct the make command with the specific variable value
	           snprintf(makeCommand, sizeof(makeCommand), "make -C /home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/lud/cuda/ BLOCK_SIZE=%d", rdWgSizeValue);

		       // Execute the make command with system()
		       int result = system(makeCommand);

	   	       
	   // Check the result of the system() call	   
       	   if (result == 0) {
		               
		   // The command executed successfully	  
       		   cout << "Make command executed successfully.\n";
	   } else {
					           
		   // There was an error executing the command
		   cerr << "Error executing make command.\n";

	   }


           lud_main(input_file, matrix_dim, do_verify, streams[i]);
	   cudaEventRecord(stop);
	   cudaEventSynchronize(stop);

   }

		
   float milliseconds = 0;

   cudaEventElapsedTime(&milliseconds, start, stop);

   std::cout << "Total execution time:  " << milliseconds << " ms\n";
   return 0;
}
