#include <iostream>
#include <cstring>
#include "parseLine.h"
#include "structs.h"

using namespace std;


int parseLine(const char* line, Configuration& config) {

	char key[32];
	char value[256];
	if (sscanf(line, "%31[^=] = %255[^\n]", key, value) == 2) {
                // Trim leading and trailing whitespace from the value
		char* trimmedValue = strdup(value);
		size_t len = strlen(trimmedValue);
		
		while (len > 0 && (trimmedValue[len - 1] == ' ' || trimmedValue[len - 1] == '\t')) {
		
			trimmedValue[len - 1] = '\0';

			--len;

		}
//appsNum
		
		if (strcmp(key, "Simult") == 0) {

			config.simult = (strcmp(value, "True") == 0);

		}
		else if (strcmp(key, "AppsNum") == 0) {		
			config.appsNum = atoi(value);
				
				                
		}else if (strcmp(key, "Blocks") == 0) {
			config.blocks = atoi(value);

		} else if (strcmp(key, "Threads") == 0) {
			config.threads = atoi(value);

		} else if (strcmp(key, "Frequency") == 0) {	
			config.frequency = atoi(value);

		} else if (strcmp(key, "Apps") == 0) {
			char* token = strtok(value, ", ");
			int i = 0;

			while (token != NULL && i < 8) {

				config.apps[i] = strdup(token);
	  			token = strtok(NULL, ", ");
				++i;

			}

		} else if (strcmp(key, "Workloads") == 0) {

			char* token = strtok(value, ", ");

			int i = 0;

			while (token != NULL && i < 8) {
				config.workloads[i] = strdup(token);
				token = strtok(NULL, ", ");
				++i;

			}

		} else {
			cerr << "Error: Unknown key in the configuration file." << endl;
			return 1;

		}

		return 0;

	}

	cerr << "Error: Invalid line in the configuration file." << endl;

	return 1;
}
