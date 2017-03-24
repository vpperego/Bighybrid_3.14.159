#!/bin/bash
clear
cd ..
make clean all
cd examples
make clean all
export LD_LIBRARY_PATH=$HOME/simgrid-3.14.159/lib

./hello_bighybrid.bin --cfg=surf/nthreads:-1 2>&1 | $HOME/simgrid-3.14.159/bin/simgrid-colorizer 
