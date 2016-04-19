#!/usr/bin/env zsh
cd `dirname $0`/..
project_path=12

for d in `find $project_path -type d -depth 1 | xargs ls -d`; do
    echo "-- " $d " --"
    ./JackCompiler $d
done
