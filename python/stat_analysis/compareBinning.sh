#!/usr/bin/env bash

baseDir=vini_inputs/ROOT_files/20181119
outDir=181119_compareBinning

mkdir $outDir/shapes/

for path in $baseDir/*.root; do
    fileName=$(basename $path)
    if [[ $fileName =~ .*bin_10.root ]]; then
        ../flattenDiagonalTH2.py -i $path -o $outDir/shapes/$fileName
        #fitDir=$outDir/$(basename $fileName .root)
        #./prepareShapesAndCards.py -i $outDir/shapes/${fileName} --fit-mode shape_CR1 -o $fitDir --bbb --qcd-systs
        fitDir=$outDir/$(basename $fileName .root)_ABCD
        ./prepareShapesAndCards.py -i $outDir/shapes/${fileName} --fit-mode abcd -o $fitDir --bbb
        pushd $fitDir
        ./do_fit.sh > fit.log 2>&1
        popd
    fi
done

function retrieve_results() {
    for dir in *; do
        pushd $dir > /dev/null
        echo "Shapes: $dir"
        cat fit.log | grep " r :"
        popd > /dev/null
    done
}

pushd $outDir
retrieve_results | tee cuts.log
echo "results = [" >> plot.py
cat cuts.log | grep " r " | sed 's|r :    +1.000   \(.*\) (68%)|\1|g' | tr -d ' ' | sed 's|-|    (abs(-|g' | sed 's|/|)|g' | sed 's|$|)/2,|g' >> plot.py
echo "]\ncuts = [" >> plot.py
cat cuts.log | grep "Shapes" | sed 's|.*cw_\(.*\)_qgl_\(.*\)_bin.*|    [\1,\2],|g' >> plot.py
echo "]" >> plot.py
popd
