#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define N 800

int main(){

	FILE *arq1, *map, *shuf, *red;
	char task[36], c[1], h1[2], h2[2], m1[2], m2[2], s1[2], s2[2], time1[12], time2[12];
	int maps[N], shuffle[N], reduces[N],r, H0, H1, H2, M0, M1, M2, S0, S1, S2,x,t,tr,i,tipo;

	arq1=fopen("tasks.dat", "r");
	
	x=0;

	for(i=0;i<N;i++){
		maps[i]=0;
		shuffle[i]=0;
		reduces[i]=0;
	}

	while(!feof(arq1)){
		fscanf(arq1, "%s", task);
		fscanf(arq1, "%d", &tipo);
		fscanf(arq1, "%s", task);
		fscanf(arq1, "%s", time1);
		fscanf(arq1, "%s", task);
		fscanf(arq1, "%s", time2);

		h1[0]=time1[0];
		h1[1]=time1[1];
		m1[0]=time1[3];
		m1[1]=time1[4];
		s1[0]=time1[6];
		s1[1]=time1[7];

		h2[0]=time2[0];
		h2[1]=time2[1];
		m2[0]=time2[3];
		m2[1]=time2[4];
		s2[0]=time2[6];
		s2[1]=time2[7];

		H1=atoi(h1);
		H2=atoi(h2);
		M1=atoi(m1);
		M2=atoi(m2);
		S1=atoi(s1);
		S2=atoi(s2);

		if(x==0){
			H0=H1;
			M0=M1;
			S0=S1;	
			x=1;
		}

		printf("%d:%d:%d %d:%d:%d ", H1,M1,S1,H2,M2,S2);
		printf("Diferença=%d\n", (H1-H2)*3600-(M1-M2)*60-(S1-S2));
		printf("%d:%d:%d %d:%d:%d ", H0,M0,S0,H1,M1,S1);		
		printf("Diferença=%d\n", (H0-H1)*3600-(M0-M1)*60-(S0-S1));		
		
				
				t=(H1-H2)*3600-(M1-M2)*60-(S1-S2);
		tr=(H0-H1)*3600-(M0-M1)*60-(S0-S1);

		if(tipo==1){
			for(i=tr;i<tr+t;i++){
				maps[i]=maps[i]+1;
			}
		}
		if(tipo==2){
			for(i=tr;i<tr+t;i++){
				reduces[i]=reduces[i]+1;
			}
		}

	}

	map=fopen("map.out", "w");
	for(i=0;i<N;i++){
		fprintf(map, "%d %d\n", i, maps[i]);
	}
	red=fopen("reduces.out", "w");
	for(i=0;i<N;i++){
		fprintf(red, "%d %d\n", i, reduces[i]);
	}
	red=fopen("suffle.out", "w");
	for(i=0;i<N;i++){
		fprintf(shuf, "%d %d\n", i, shuffle[i]);
	}
	fclose(map);
	fclose(red);
	fclose(shuf);
	fclose(arq1);
	return 0;

}
