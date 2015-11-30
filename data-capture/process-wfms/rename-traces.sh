#!/bin/bash

traces_path="/home/skoppula/mit/security/final-project/trace-data/traces-23-11-2015/"

for filename in ${traces_path}*.wfm
do
    
    echo $filename
    new_filename=$(echo $filename | cut -c 83-90)
    new_path="${traces_path}${new_filename}"
    echo $new_path
    mv $filename $new_path
done
