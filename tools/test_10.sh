#!/usr/bin/env zsh
#!/usr/bin/env zsh
cd `dirname $0`/..
project_path=10

for d in `ls $project_path`; do
    echo "-- " $project_path/$d " --"
    ./JackAnalyzer $project_path/$d
    for f in `ls $project_path/$d/*.jack`; do
        cmd="diff -w ${f:r}.xml ${f:r}.org.xml"
        eval $cmd
    done
done
