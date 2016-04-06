#!/usr/bin/env zsh
project_path=`dirname $0`/../10/

for d in `ls $project_path`; do
    for f in `ls $project_path$d/*.jack`; do
        echo $f
        diff -w ${f:r}.xml ${f:r}.org.xml
    done
done
