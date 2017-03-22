#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <ctype.h>
#define N 800

char *headings[N][6] ; 

struct data { 
char task_id[10];
char phase[15];
int worker_id;
double time;
char action[6];
double shuffle;
} ;        

struct data mydata[N]; 


int main() { 

int i ;  

FILE *fp = fopen("tasks-mra.csv", "r") ; 

 if ( fp != NULL ) 
 { 
    for(i=1; i<N; i++)  
    {           
         
                     
             fscanf(fp, "%s, %s, %s, %s, %s, %s \n", 
             headings[N][1], headings[N][2], headings[N][3], 
             headings[N][4], headings[N][5], headings[N][6]) ;   
             i++;      
              
                  
 //  mydata-> data = i ;  
        
   fscanf(fp, "%s, %s, %d, %lf, %s, %lf \n", 
      mydata->task_id, mydata->phase, &mydata->worker_id, &mydata->time, mydata->action, &mydata->shuffle);             
   i++;       
   }  /* EOF */  
   
}  /* File exists */    
   

/*  Print the file */ 

printf("%s, %s, %s, %s, %s, %s \n", 
   headings[N][0], headings[N][1], headings[N][2], headings[N][3], headings[N][4], headings[N][5], headings[N][6]);  
  
int j; 
  
for (j=0; j<N; j++)    
  { 
    printf("%s, %s, %d, %lf, %s, %lf \n", 
         mydata[j].task_id, mydata[j].phase,mydata[j].worker_id, mydata[j].time, mydata[j].action, mydata[j].shuffle);   
  }  
          
return 0;   
  
}
