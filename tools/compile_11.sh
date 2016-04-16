#!/usr/bin/env zsh
bin_path=`dirname $0`/..
project_path=$bin_path/11

for d in `ls $project_path`; do
    $bin_path/JackCompiler $project_path/$d
done
