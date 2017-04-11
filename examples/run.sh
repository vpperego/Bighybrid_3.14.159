#!/bin/bash
export LD_LIBRARY_PATH=$HOME/simgrid-3.14.159/lib

clear
cd ..
make clean all
cd examples/
make clean all
python create-bighybrid-plat.py yh.xml 2000 2 5e9 1e-4 1.25e8
python create-bighybrid-plat.py fb.xml 3000 2 5e9 1e-4 1.25e8
python create-bighybrid-depoly.py yh.xml
python create-bighybrid-depoly.py fb.xml
./hello_bighybrid.bin --cfg=tracing:no  cc.xml d-cc.xml cc.conf 2>&1| $HOME/simgrid-3.14.159/bin/colorize  > cc.txt &
./hello_bighybrid.bin --cfg=tracing:no  yh.xml d-yh.xml yh_206.conf 2>&1| $HOME/simgrid-3.14.159/bin/colorize > yh_206.txt &
./hello_bighybrid.bin --cfg=tracing:no  yh.xml d-yh.xml yh_568.conf  2>&1| $HOME/simgrid-3.14.159/bin/colorize > yh_568.txt &
./hello_bighybrid.bin --cfg=tracing:no  fb.xml d-fb.xml fb.conf  2>&1| $HOME/simgrid-3.14.159/bin/colorize > fb.txt &
