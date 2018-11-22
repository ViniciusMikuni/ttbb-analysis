#!/usr/bin/env bash

baseDir=vini_inputs/ROOT_files/20181120
outDir=181120_compareBinning

mkdir $outDir/shapes/

for path in $baseDir/*.root; do
    fileName=$(basename $path)
    if [[ $fileName =~ .*bin_10.root ]]; then
        #../flattenDiagonalTH2.py -i $path -o $outDir/shapes/$fileName
        #fitDir=$outDir/$(basename $fileName .root)
        #./prepareShapesAndCards.py -i $outDir/shapes/${fileName} --fit-mode shape_CR1 -o $fitDir --bbb --qcd-systs
        fitDir=$outDir/$(basename $fileName .root)_ABCD
        ./prepareShapesAndCards.py -i $outDir/shapes/${fileName} --fit-mode abcd -o $fitDir --bbb
        pushd $fitDir
        ./do_fit.sh > fit.log 2>&1
        popd
    fi
done

for dir in $outDir/*; do
    pushd $dir > /dev/null
    echo "Shapes: $dir"
    cat fit.log | grep " r :"
    popd > /dev/null
done
