#ifndef DATASTRUC_H
#define DATASTRUC_H

#include <stdlib.h>

struct csv_data{
char task_id[30];
char phase[15];
int worker_id;
double time;
char action[6];
double shuffle;
};


#endif /* !DATASTRUC_H */
