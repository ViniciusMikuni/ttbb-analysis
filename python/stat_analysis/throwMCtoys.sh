#!/usr/bin/env bash

export folder=$1
export data=$2
BBB=$3
export BBB
nToys=1000
toyMu=1.

export shapes=my_inputs/190211_tt2b_fixVHbb/hCard_addJetCSV_cw_05_qg_08_plot_tt2b.root
export rateJSON=my_inputs/190211_tt2b_fixVHbb/hCard_addJetCSV_cw_05_qg_08_plot_tt2b.json
export jecJSON=my_inputs/190211_tt2b_fixVHbb/hCard_addJetCSV_cw_05_qg_08_plot_tt2b_JECrate.json

function throwAndFitAsimov() {
	FIT_OPT=( --freezeNuisanceGroups=extern --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=999999999 --X-rtd MINIMIZER_analytic --robustFit 1 --cminDefaultMinimizerPrecision 1E-12 )

    ./prepareShapesAndCards.py -i ${shapes} -o ${folder}/toy_$1 --fit-mode abcd --rate-systs ${rateJSON} --sub-folder fiducial --exp-rate ${jecJSON} --fact-theory all --randomise ${BBB}

    pushd ${folder}/toy_$1

    text2workspace.py datacard.dat -o workspace.root
    combine -M MultiDimFit -d workspace.root --toysFile=../higgsCombine_toyAsimov.GenerateOnly.mH120.123456.root --rMin 0 --rMax 5 --expectSignal=1 --algo singles "${FIT_OPT[@]}" -t -1

    popd
}
export -f throwAndFitAsimov

function throwAndFitData() {
	FIT_OPT=( --freezeNuisanceGroups=extern --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=999999999 --X-rtd MINIMIZER_analytic --robustFit 1 --cminDefaultMinimizerPrecision 1E-12 )

    ./prepareShapesAndCards.py -i ${shapes} -o ${folder}/toy_$1 --fit-mode abcd --rate-systs ${rateJSON} --sub-folder fiducial --exp-rate ${jecJSON} --fact-theory all --randomise ${BBB} -d

    pushd ${folder}/toy_$1

    text2workspace.py datacard.dat -o workspace.root
    combine -M MultiDimFit -d workspace.root --rMin 0 --rMax 5 --expectSignal=1 --algo singles "${FIT_OPT[@]}"

    popd
}
export -f throwAndFitData


if [[ $data = "asimov" ]]; then
    # Run blind, on toy Asimov
    
    echo "## Will run MC toys on Asimov pseudo-data"
    echo "## Preparing Asimov..."

    ./prepareShapesAndCards.py -i ${shapes} -o ${folder} --fit-mode abcd --rate-systs ${rateJSON} --sub-folder fiducial --exp-rate ${jecJSON} --fact-theory all
    pushd ${folder}
    text2workspace.py datacard.dat -o workspace.root
    combine -M GenerateOnly --saveToys --toysNoSystematics --expectSignal=${toyMu} -t -1 -n _toyAsimov -d workspace.root
    popd

    echo "## Running toys..."

    SHELL=/bin/bash parallel --gnu -j 4 throwAndFitAsimov ::: $(seq 1 $nToys)
fi

if [[ $data = "true" ]]; then

    echo "## Will run MC toys on real data!"

    mkdir ${folder}

    echo "## Running toys..."
    
    SHELL=/bin/bash parallel --gnu -j 4 throwAndFitData ::: $(seq 1 $nToys)
fi

pushd ${folder}

hadd -f toys.root toy_*/higgsCombineTest.MultiDimFit.mH120.root

popd
