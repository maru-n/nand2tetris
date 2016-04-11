#!/usr/bin/env zsh
bin_path=`dirname $0`/..
project_path=$bin_path/10

for d in `ls $project_path`; do
    $bin_path/JackAnalyzer $project_path/$d
    for f in `ls $project_path/$d/*.jack`; do
        cmd="diff -w ${f:r}.xml ${f:r}.org.xml"
        #echo $cmd
        eval $cmd
    done
done
