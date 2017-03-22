#!/bin/bash
echo "INICIANDO TESTES..."
export LD_LIBRARY_PATH=$HOME/simgrid-3.14.159/lib
echo "local maps,non-local maps,speculative maps (local),speculative maps (remote),recovery maps,total non-local maps,total speculative maps,normal reduces,speculative reduces,recovery reduces,Map Time,Reduce Time" >> stats_mra.csv

echo "local maps,non-local maps,speculative maps (local),speculative maps (remote),total non-local maps,total speculative maps,normal reduces,speculative reduces,Map Time,Reduce Time">> stats_mrsg.csv
cd ..
make clean all
cd examples
make clean all
for volatil_perc in 0 25
do
    for grain_factor in 1 2 4 6 8
    do
        for chunk_input in 512 1024 1536
        do
            for chunk_size in 16 32 64
            do
            rm -f bighyb-plat32-32.conf
            echo "mra_reduces 64
mra_chunk_size $chunk_size
mra_input_chunks $chunk_input
mra_dfs_replicas 3
mra_map_slots 2
mra_reduce_slots 2
grain_factor $grain_factor
mra_intermed_perc 100
perc_num_volatile_node $volatil_perc
failure_timeout 4

mrsg_reduces 64
mrsg_chunk_size $chunk_size
mrsg_input_chunks $chunk_input
mrsg_dfs_replicas 3
mrsg_map_slots 2
mrsg_reduce_slots 2
mrsg_intermed_perc 100" >> bighyb-plat32-32.conf
            ./hello_bighybrid.bin 2>&1 | $HOME/simgrid-3.14.159/bin/simgrid-colorizer > saida.txt
            done
        done
    done
done
echo "TESTES CONCLUIDOS"
