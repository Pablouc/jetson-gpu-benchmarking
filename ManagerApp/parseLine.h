#ifndef PARSELINE_H
#define PARSELINE_H

#include <cstring>

struct Configuration {
	bool simult;
	int executions;
	int blocks;
	int threads;
	int frequency;
	char* apps[8];
	char* workloads[8];
};

int parseLine(const char* line, Configuration& config);

#endif // PARSELINE_H
