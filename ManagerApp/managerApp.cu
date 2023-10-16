#include <stdlib.h>
#include <stdio.h>
#include <cuda_runtime.h>
#include <iostream>
#include <fstream>
#include <cstring>
#include "parseLine.h"
using namespace std;

  

int managerApp(const char* configFile) {

	ifstream file(configFile);
	if (!file.is_open()) {
	    cerr << "Error: Cannot open file." << endl;
	    return 1;
	}


	Configuration config;
	memset(&config, 0, sizeof(Configuration)); // Initialize the struct

	char line[256];
    	int lineCount = 0;
	while (file.getline(line, sizeof(line))) {
		++lineCount;
		if (parseLine(line, config)) {
			cerr << "Error at line " << lineCount << endl;
			file.close();
			return 1;

		}

	}
	
	// Print or use the configuration variables here

     	cout << "Simult: " << config.simult << endl;
	cout << "Blocks: " << config.blocks << endl;
	cout << "Threads: " << config.threads << endl;
	cout << "Frequency: " << config.frequency << endl;
	cout << "Apps: ";

	for (int i = 0; i < 8 && config.apps[i] != nullptr; ++i) {
		cout << config.apps[i] << " ";

	}

	cout << endl;

	cout << "Workloads: ";

	for (int i = 0; i < 8 && config.workloads[i] != nullptr; ++i) {

		cout << config.workloads[i] << " ";

	}

	cout << endl;


	
	// Free allocated memory for strings

	for (int i = 0; i < 8; ++i) {

		if (config.apps[i] != nullptr) {

			free(config.apps[i]);

		}

		if (config.workloads[i] != nullptr) {

			free(config.workloads[i]);

		}

	}


	
	file.close();

	return 0;
}
	


int main() {
    const char* inputFileName = "exec_config.txt";
    managerApp(inputFileName);
    return 0;
}

