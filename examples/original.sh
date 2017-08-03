#!/bin/bash
export LD_LIBRARY_PATH=$HOME/simgrid-3.14.159/lib
cd ..
make clean all
cd examples/
make clean all
#./hello_bighybrid.bin test.xml d-test.xml test.conf parser-boinc-1500.txt
./hello_bighybrid.bin --cfg=contexts/stack-size:512 test.xml d-test.xml test.conf parser-boinc-1500.txt
