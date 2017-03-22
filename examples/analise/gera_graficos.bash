#!/bin/bash

gcc estatisticas.c -o gera_estatisticas
var=1
#mkdir maps
#mkdir reduces
mkdir graph
#mkdir gantt

while [ $var -lt 11 ]; do
	if [ $var -lt 10 ]; then
		python gantt.py jobtracker.log job_201101201158_00$var; #GANTT
	else
		python gantt.py jobtracker.log job_201101201158_00$var; #GANTT
	fi
	./gera_estatisticas; #Gerador de estatísticas
	gnuplot graficos.gp; #Plota gráficos
#	mv map.out maps/map$var.out
#	mv reduces.out reduces/reduce$var.out
#	mv tasks.dat gantt/tasks$var.dat
	mv imagem.png graph/imagem0$var.png; #Arruma nome do arquivo
	var=`expr $var + 1`
done


