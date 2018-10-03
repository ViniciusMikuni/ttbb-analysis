#!/usr/bin/env python

# Python imports
import os, sys, argparse, stat
from math import sqrt
from pdb import set_trace as bp # insert bp() to have a breakpoint anywhere

# ROOT imports
import ROOT
ROOT.gROOT.SetBatch()
ROOT.PyConfig.IgnoreCommandLineOptions = True

import CombineHarvester.CombineTools.ch as ch

import definitions as defs
import utils

def main():

    parser = argparse.ArgumentParser(description='Create shape datacards ready for combine')

    parser.add_argument('-i', '--input', type=str, help='Input ROOT file containing templates')
    parser.add_argument('-d', '--data', action='store_true', help='Use REAL DATA in SIGNAL REGION')
    parser.add_argument('--no-qcd-systs', dest='no_QCD_systs', action='store_true', help='Do not add any uncertainty on the QCD shape')
    parser.add_argument('-o', '--output', type=str, help='Output directory')

    options = parser.parse_args()

    prepareShapesAndCards(options)


def prepareShapesAndCards(options):

    cb = ch.CombineHarvester()

    cats = [
        (1, 'CR1'),
        (2, 'SR')
    ]
    
    processed_shapes = os.path.join(options.output, 'processed_shapes.root')
    QCD_VR_ratios, QCD_yield_CR1, QCD_yield_SR, QCD_shape_CR1 = utils.extractShapes(options.input, processed_shapes, defs.bkg_processes_mc, defs.sig_processes, options.data)
    Nbins = len(QCD_VR_ratios)

    cb.AddObservations(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], cats)
    
    cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], defs.sig_processes, cats, True)

    cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], defs.bkg_processes_mc, cats, False)

    ### QCD estimate: add all "delta" templates
    QCD_processes = [ 'QCD_bin_{}'.format(i+1) for i in range(Nbins) ]
    cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], QCD_processes, cats, False)

    ### Modeling systematics, not on QCD! ###
    cbWithoutQCD = cb.cp().process_rgx(['QCD.*'], False)

    cbWithoutQCD.AddSyst(cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')(['13TeV_2016'], defs.getLumiUncertainty('13TeV_2016')))

    # Experimental systematics, common for all processes and categories
    for s in defs.exp_systs:
        cbWithoutQCD.AddSyst(cb, s, 'shape', ch.SystMap()(1.))
        # cb.cp().process(bkg_processes_mc + sig_processes).AddSyst(cb, s, 'shape', ch.SystMap()(1.))

    ### QCD systematics: add a lnN for each bin using the ratio QCD_subtr/QCD_est in the VR
    if not options.no_QCD_systs:
        for i in range(1, Nbins+1):
            lnN = 1 + abs(1 - QCD_VR_ratios[i-1])
            cb.cp().bin(['SR']).process(['QCD_bin_{}'.format(i)]).AddSyst(cb, 'QCD_shape_bin_{}'.format(i), 'lnN', ch.SystMap()(lnN))

    ### QCD estimate: add the rate params for each bin and for the total normalisation in CR1 and SR
    extraStrForQCD = ''
    extraStrForQCD += 'scale_QCD_CR1 extArg {} [0.,200000.]\n'.format(QCD_yield_CR1)
    extraStrForQCD += 'scale_QCD_SR extArg {} [0.,50000.]\n'.format(QCD_yield_SR)
    
    for i in range(2, Nbins+1):
        extraStrForQCD += 'fraction_QCD_bin_{} extArg {} [0.,1.]\n'.format(i, QCD_shape_CR1[i-1])
        extraStrForQCD += 'yield_QCD_CR1_bin_{0} rateParam CR1 QCD_bin_{0} (@0*@1) scale_QCD_CR1,fraction_QCD_bin_{0}\n'.format(i)
        extraStrForQCD += 'yield_QCD_SR_bin_{0} rateParam SR QCD_bin_{0} (@0*@1) scale_QCD_SR,fraction_QCD_bin_{0}\n'.format(i)
    
    allBinSum = '+'.join([ '@{}'.format(i) for i in range(1, Nbins) ])
    allBinParams = ','.join([ 'fraction_QCD_bin_{}'.format(i) for i in range(2, Nbins+1) ])
    extraStrForQCD += 'yield_QCD_CR1_bin_1 rateParam CR1 QCD_bin_1 (@0*(1-({0}))) scale_QCD_CR1,{1}\n'.format(allBinSum, allBinParams)
    extraStrForQCD += 'yield_QCD_SR_bin_1 rateParam SR QCD_bin_1 (@0*(1-({0}))) scale_QCD_SR,{1}\n'.format(allBinSum, allBinParams)
    
    cb.AddDatacardLineAtEnd(extraStrForQCD)
   
    # Define theory systematic group

    syst_groups = {
            "theory": ['CMS_btag_hf']
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

    output_dir = options.output

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    datacard = os.path.join(output_dir, 'datacard.dat')
    output_shapes = os.path.join(output_dir, 'shapes.root')
        
    cb.WriteDatacard(datacard, output_shapes)


    def createScript(content, filename):
        script_path = os.path.join(output_dir, filename)
        with open(script_path, 'w') as f:
            f.write(script)
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | stat.S_IEXEC)

    # Script: simple fit
    script = """
#!/bin/bash

if [[ ! -f workspace.root ]]; then
    text2workspace.py datacard.dat -o workspace.root
fi

combine -M FitDiagnostics -d workspace.root --rMin -5 --rMax 5 -t -1 --expectSignal=1 | tee asimov_fit.log
    """
    createScript(script, 'do_fit.sh')


    # Script: plots of NLL vs. r for different uncertainties
    script = """
#!/bin/bash

if [[ ! -f workspace.root ]]; then
    text2workspace.py datacard.dat -o workspace.root
fi

combine -M MultiDimFit --algo grid --points 500 --rMin 0 --rMax 2 -t -1 --expectSignal=1 -n nominal workspace.root
combine -M MultiDimFit --algo grid --points 500 --rMin -1 --rMax 4 -t -1 --expectSignal=1 -n theory --freezeNuisanceGroups theory workspace.root
combine -M MultiDimFit --algo grid --points 500 --rMin 0 --rMax 2 -t -1 --expectSignal=1 -n stat -S 0 workspace.root
# combine -M MultiDimFit --algo grid --points 500 --rMin -1 --rMax 4 --expectSignal=1 -n stat --freezeParameters all --fastScan workspace.root
# plot1DScan.py higgsCombinenominal.MultiDimFit.mH120.root --others 'higgsCombinestat.MultiDimFit.mH120.root:Freeze all:2' --breakdown syst,stat
plot1DScan.py higgsCombinenominal.MultiDimFit.mH120.root --others 'higgsCombinetheory.MultiDimFit.mH120.root:Freeze theory:4' 'higgsCombinestat.MultiDimFit.mH120.root:Freeze all:2' --breakdown theory,syst,stat
    """
    createScript(script, 'do_DeltaNLL_plot.sh')




if __name__ == '__main__':
    main()
