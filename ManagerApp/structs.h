#ifndef STRUCTS_H
#define STRUCTS_H

#include <cstring>


const int MAX_APPS = 8;
const int MAX_APP_LENGHT = 50;

struct Configuration {
	       
       	bool simult;

	int executions;

	int appsNum;

	int blocks;

	int threads;

	int frequency;

	char* apps[MAX_APPS];//[MAX_APP_LENGHT];

	char* workloads[MAX_APPS];//[MAX_APP_LENGHT];
};


#endif // STRUCT_H
