#!/bin/bash
export LD_LIBRARY_PATH=$HOME/simgrid-3.14.159/lib
cd ..
make clean all
cd examples/
make clean all
./hello_bighybrid.bin Experiment_0.xml d-Experiment_0.xml Experiment_0.conf
