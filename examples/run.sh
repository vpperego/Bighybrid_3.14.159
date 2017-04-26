#!/bin/bash
export LD_LIBRARY_PATH=$HOME/simgrid-3.14.159/lib

WORKLOAD=()
MRA_MACHINES=()
MRSG_MACHINES=()
MSRG_CHUNK_COUNT=()
MRA_CHUNK_COUNT=()
MRA_CHUNK_SIZE=()
MRSG_CHUNK_SIZE=()
MRSG_MAP_COST=()
MRSG_REDUCE_COST=()
MRA_MAP_COST=()
MRA_REDUCE_COST=()
INTERMED_PERC=()
PERC_VOLATILITE=()
while read p; do
	case $p in
		"MRA Machines"*) MRA_MACHINES+=($(echo $p | grep -o "[0-9]*"));;
		"MRSG Machines"*) MRSG_MACHINES+=($(echo $p | grep -o "[0-9]*"));;
		"Load Cloud"*) MSRG_CHUNK_COUNT+=($(echo $p | grep -o "[0-9]*"));;
		"Load DG"*) MRA_CHUNK_COUNT+=($(echo $p | grep -o "[0-9]*"));;
		"MRA Map Cost"*) MRA_MAP_COST+=($(echo $p | grep -o "[0-9]*.[0-9]*e+[0-9]*"));;
		"MRA Reduce Cost"*) MRA_REDUCE_COST+=($(echo $p | grep -o "[0-9]*.[0-9]*e+[0-9]*"));;
		"MRSG Map Cost"*) MRSG_MAP_COST+=($(echo $p | grep -o "[0-9]*.[0-9]*e+[0-9]*"));;
		"MRSG Reduce Cost"*)MRSG_REDUCE_COST+=($(echo $p | grep -o "[0-9]*.[0-9]*e+[0-9]*"));;
		"Vol"*)PERC_VOLATILITE+=($(echo $p | grep -o "[0-9]*"));;
		"MRA chunk"*)MRA_CHUNK_SIZE+=($(echo $p | grep -o "[0-9]*"));;
		"MRSG chunk"*)MRSG_CHUNK_SIZE+=($(echo $p | grep -o "[0-9]*"));;
	esac

done < teste.txt
echo ${MRA_MAP_COST[0]}


clear
cd ..
make clean all
cd examples/
make clean all
for MRSG_MACHINES in 1 2 3 4
do
	python create-bighybrid-plat.py $WORKLOAD.xml $MRA_MACHINES 2 5e9 1e-4 1.25e8 $MRSG_MACHINES 2 5e9 1e-4 1.25e8
	python create-bighybrid-depoly.py $WORKLOAD.xml

	"mrsg_reduces `expr $MRSG_MACHINES \* 2`
	mrsg_chunk_size 64
	mrsg_input_chunks $MSRG_CHUNK_COUNT
	mrsg_dfs_replicas 3
	mrsg_map_slots 2
	mrsg_reduce_slots 2
	mrsg_intermed_perc $INTERMED_PERC 0.68651656029929577400
	mrsg_map_task_cost $MRSG_MAP_COST
	mrsg_reduce_task_cost $MRSG_REDUCE_COST

	mra_reduces `expr $MRA_MACHINES \* 2`
	mra_chunk_size 64
	mra_input_chunks $MRA_CHUNK_COUNT
	mra_dfs_replicas 5
	mra_map_slots 2
	mra_reduce_slots 2
	mra_intermed_perc $INTERMED_PERC 0.68651656029929577400
	perc_num_volatile_node $PERC_VOLATILITE
	grain_factor 1
	failure_timeout 4.0
	mra_map_task_cost $MRA_MAP_COST
	mra_reduce_task_cost $MRA_REDUCE_COST" > $WORKLOAD.conf
	./hello_bighybrid.bin --cfg=tracing:no  $WORKLOAD.xml d-$WORKLOAD.xml $WORKLOAD.conf 2>&1| $HOME/simgrid-3.14.159/bin/colorize > $WORKLOAD.txt 
done
python create-bighybrid-plat.py fb.xml 3000 2 5e9 1e-4 1.25e8
python create-bighybrid-depoly.py yh.xml
python create-bighybrid-depoly.py fb.xml
./hello_bighybrid.bin --cfg=tracing:no  cc.xml d-cc.xml cc.conf 2>&1| $HOME/simgrid-3.14.159/bin/colorize  > cc.txt &
./hello_bighybrid.bin --cfg=tracing:no  yh.xml d-yh.xml yh_206.conf 2>&1| $HOME/simgrid-3.14.159/bin/colorize > yh_206.txt &
./hello_bighybrid.bin --cfg=tracing:no  yh.xml d-yh.xml yh_568.conf  2>&1| $HOME/simgrid-3.14.159/bin/colorize > yh_568.txt &
./hello_bighybrid.bin --cfg=tracing:no  fb.xml d-fb.xml fb.conf  2>&1| $HOME/simgrid-3.14.159/bin/colorize > fb.txt &
