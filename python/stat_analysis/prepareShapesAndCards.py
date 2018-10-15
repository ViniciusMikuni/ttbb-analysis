#!/usr/bin/env python

# Python imports
import os, sys, argparse, stat
from math import sqrt
from pdb import set_trace as bp # insert bp() to have a breakpoint anywhere
import itertools

import ROOT
ROOT.gROOT.SetBatch()
ROOT.PyConfig.IgnoreCommandLineOptions = True

import CombineHarvester.CombineTools.ch as ch

import definitions as defs
import utils

def main():

    parser = argparse.ArgumentParser(description='Create shape datacards ready for combine')

    parser.add_argument('-i', '--input', type=str, help='Input ROOT file containing templates')
    parser.add_argument('-d', '--data', action='store_true', help='Use real data in SIGNAL REGION (by default, will transfer QCD shape from the CR1) - for now Asimov datasets are always used.')
    parser.add_argument('--bbb', action='store_true', help='Add bin-by-bin uncertainties')
    parser.add_argument('--fit-mode', dest='fit_mode', choices=['shape_direct', 'shape_CR1', 'abcd'], help='Fit mode')
    parser.add_argument('---qcd-systs', dest='QCD_systs', action='store_true', help='If mode is "shape_CR1", add uncertainty on the QCD shape from the VR/CR2 ratio')
    parser.add_argument('-o', '--output', type=str, help='Output directory')

    options = parser.parse_args()

    prepareShapesAndCards(options)


def prepareShapesAndCards(options):

    cb = ch.CombineHarvester()

    if options.fit_mode == 'shape_direct':
        cats = [(1,'SR')]
    elif options.fit_mode == 'shape_CR1':
        cats = [
            (1, 'SR'),
            (2, 'CR1')
        ]
    elif options.fit_mode == 'abcd':
        cats = [
            (1, 'SR'),
            (2, 'CR1'),
            (3, 'VR'),
            (4, 'CR2'),
        ]
    
    processed_shapes = os.path.join(options.output, 'processed_shapes.root')
    QCD_VR_ratios, est_QCD_yields, QCD_shape_CR1, QCD_shape_CR2 = utils.extractShapes(options.input, processed_shapes, defs.bkg_processes_mc, defs.sig_processes, options.data)
    Nbins = len(QCD_VR_ratios)

    cb.AddObservations(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], cats)
    
    cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], defs.sig_processes, cats, True)

    cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], defs.bkg_processes_mc, cats, False)

    if options.fit_mode == 'shape_direct':
        cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], ['QCD'], cats, False)
    
    elif options.fit_mode in ['shape_CR1', 'abcd']:
        ### QCD estimate: add all "delta" templates
        QCD_processes = [ 'QCD_bin_{}'.format(i+1) for i in range(Nbins) ]
        cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], QCD_processes, cats, False)

    ### Modeling systematics, not on QCD! ###
    cbWithoutQCD = cb.cp().process_rgx(['QCD.*'], False)

    # Luminosity
    cbWithoutQCD.AddSyst(cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')(['13TeV_2016'], defs.getLumiUncertainty('13TeV_2016')))

    # Experimental systematics, common for all processes and categories
    for s in defs.exp_systs:
        cbWithoutQCD.AddSyst(cb, s, 'shape', ch.SystMap()(1.))
    
    # Theory shape systematics
    for syst in defs.theory_shape_systs:
        cbWithoutQCD.cp().process(syst[0]).AddSyst(cb, syst[1], 'shape', ch.SystMap()(1.))
    
    # Theory rate systematics
    for name,syst in defs.theory_rate_systs.items():
        cbWithoutQCD.cp().AddSyst(cb, name, syst[0], syst[1])
        
    ### QCD systematics: add a lnN for each bin using the ratio QCD_subtr/QCD_est in the VR
    if options.fit_mode == 'shape_CR1' and options.QCD_systs:
        for i in range(1, Nbins+1):
            lnN = 1 + abs(1 - QCD_VR_ratios[i-1])
            cb.cp().bin(['SR']).process(['QCD_bin_{}'.format(i)]).AddSyst(cb, 'QCD_shape_bin_{}'.format(i), 'lnN', ch.SystMap()(lnN))

    extraStrForQCD = ''
    
    if options.fit_mode == 'shape_direct':
        ### QCD estimate: freely floating
        extraStrForQCD += 'rate_QCD rateParam SR QCD 1. [0.,10.]\n'
    
    elif options.fit_mode == 'shape_CR1':
        ### QCD estimate: fit shape from CR1, normalisation floating
        extraStrForQCD += 'scale_ratio_QCD_CR1_SR extArg 1. [0.,10.]\n'
        
        for i in range(1, Nbins+1):
            extraStrForQCD += 'yield_QCD_SR_bin_{0} rateParam SR QCD_bin_{0} 1. [0.,10.]\n'.format(i)
    
        for i in range(1, Nbins+1):
            extraStrForQCD += 'yield_QCD_CR1_bin_{0} rateParam CR1 QCD_bin_{0} (@0*@1) scale_ratio_QCD_CR1_SR,yield_QCD_SR_bin_{0}\n'.format(i)
    
    elif options.fit_mode == 'abcd':
        ### QCD estimate: add the rate params for each bin in the SR and for the SR->CR1 transfer ratio
        for i in range(1, Nbins+1):
            extraStrForQCD += 'scale_ratio_QCD_bin_{0} extArg 1.\n'.format(i)
            extraStrForQCD += 'yield_QCD_VR_bin_{0} rateParam VR QCD_bin_{0} 1.\n'.format(i)
            extraStrForQCD += 'yield_QCD_SR_bin_{0} rateParam SR QCD_bin_{0} 1.\n'.format(i)
        
            extraStrForQCD += 'yield_QCD_CR2_bin_{0} rateParam CR2 QCD_bin_{0} (@0*@1) scale_ratio_QCD_bin_{0},yield_QCD_VR_bin_{0}\n'.format(i)
            extraStrForQCD += 'yield_QCD_CR1_bin_{0} rateParam CR1 QCD_bin_{0} (@0*@1) scale_ratio_QCD_bin_{0},yield_QCD_SR_bin_{0}\n'.format(i)
    
    cb.AddDatacardLineAtEnd(extraStrForQCD)

    # Define theory systematic group
    syst_groups = {
            "theory": [ s[1] for s in defs.theory_shape_systs ] + 
                        list(itertools.chain.from_iterable(
                            map(defs.getNuisanceFromTemplate, defs.theory_rate_systs.keys(), defs.theory_rate_systs.values())
                        )),
            "exp": defs.exp_systs,
        }

    def getNuisanceGroupString(groups):
        m_str = ""
        for g in groups:
            m_str += g + ' group = '
            for sys in groups[g]:
                m_str += sys + ' '
            m_str += '\n'
        return m_str

    cb.AddDatacardLineAtEnd(getNuisanceGroupString(syst_groups))

    cb.cp().ExtractShapes(processed_shapes, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')

    if options.bbb:
        # MC statistics - has to be done after the shapes have been extracted!
        bbb_bkg = ch.BinByBinFactory().SetVerbosity(5)
        bbb_bkg.SetAddThreshold(0.05).SetMergeThreshold(0.5).SetFixNorm(False)
        bbb_bkg.MergeBinErrors(cb.cp().backgrounds())
        bbb_bkg.AddBinByBin(cb.cp().backgrounds(), cb)

        bbb_sig = ch.BinByBinFactory().SetVerbosity(5).SetAddThreshold(0.2).SetFixNorm(False)
        bbb_sig.AddBinByBin(cbWithoutQCD.cp().signals(), cb)
    
    output_dir = options.output

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    datacard = os.path.join(output_dir, 'datacard.dat')
    output_shapes = os.path.join(output_dir, 'shapes.root')
        
    cb.WriteDatacard(datacard, output_shapes)

    initWorkSpace = """
#!/bin/bash

if [[ ! -f workspace.root ]]; then
    text2workspace.py datacard.dat -o workspace.root
fi
"""

    def createScript(content, filename):
        script_path = os.path.join(output_dir, filename)
        with open(script_path, 'w') as f:
            f.write(initWorkSpace)
            f.write(script)
        # make script executable
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | stat.S_IEXEC)

    # Script: simple fits
    script = """
RMIN=0.
RMAX=2.0

combine -M MultiDimFit -d workspace.root --rMin $RMIN --rMax $RMAX --expectSignal=1 -t -1 --algo singles --autoBoundsPOIs "*" --robustFit=1 --setRobustFitAlgo Minuit2,Minos --setRobustFitStrategy 2
# combine -M FitDiagnostics -d workspace.root --rMin $RMIN --rMax $RMAX -t -1 --expectSignal=1 --robustFit=1 --cminDefaultMinimizerStrategy 2 --saveShapes --plots
#combine -M MultiDimFit -d workspace.root --rMin $RMIN --rMax $RMAX --expectSignal=1 -t 1000 --toysFrequentist > /dev/null
"""

    createScript(script, 'do_fit.sh')


    # Script: plots of NLL vs. r for different uncertainties
    script = """
NPOINTS=50
RMIN=0.
RMAX=2.0

combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX -t -1 --expectSignal=1 -n nominal workspace.root
combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX -t -1 --expectSignal=1 -n theory --freezeNuisanceGroups theory workspace.root
combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX -t -1 --expectSignal=1 -n stat -S 0 workspace.root
# combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX --expectSignal=1 -n stat --freezeParameters all --fastScan workspace.root
# plot1DScan.py higgsCombinenominal.MultiDimFit.mH120.root --others 'higgsCombinestat.MultiDimFit.mH120.root:Freeze all:2' --breakdown syst,stat
plot1DScan.py higgsCombinenominal.MultiDimFit.mH120.root --others 'higgsCombinetheory.MultiDimFit.mH120.root:Freeze theory:4' 'higgsCombinestat.MultiDimFit.mH120.root:Freeze all:2' --breakdown theory,syst,stat
    """
    createScript(script, 'do_DeltaNLL_plot.sh')


    # Script: impacts signal injected
    script = """
RMIN=-1
RMAX=3

combineTool.py -M Impacts -d workspace.root -m 120 -t -1 --rMin $RMIN --rMax $RMAX --expectSignal=1 --doInitialFit --robustFit 1 --setRobustFitAlgo Minuit2,Minos --setRobustFitStrategy 2
combineTool.py -M Impacts -d workspace.root -m 120 -t -1 --rMin $RMIN --rMax $RMAX --expectSignal=1 --robustFit 1  --setRobustFitAlgo Minuit2,Minos --setRobustFitStrategy 2 --doFits --parallel 6
combineTool.py -M Impacts -d workspace.root -m 120 -o impacts_signal_injected.json
plotImpacts.py -i impacts_signal_injected.json -o impacts_signal_injected
    """
    createScript(script, 'do_impacts_signal_injected.sh')

if __name__ == '__main__':
    main()
