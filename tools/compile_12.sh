#!/usr/bin/env zsh
cd `dirname $0`/..
project_path=12

for d in `ls $project_path`; do
    echo "-- " $project_path/$d " --"
    ./JackCompiler $project_path/$d
done
