#!/usr/bin/env python

# Python imports
import os, sys, argparse, stat
from math import sqrt
from pdb import set_trace as bp # insert bp() to have a breakpoint anywhere
import json

import ROOT
ROOT.gROOT.SetBatch()
ROOT.PyConfig.IgnoreCommandLineOptions = True

import CombineHarvester.CombineTools.ch as ch

import definitions as defs
import utils

def main():

    parser = argparse.ArgumentParser(description='Create shape datacards ready for combine')

    parser.add_argument('-i', '--input', required=True, help='Input ROOT file containing templates')
    parser.add_argument('-d', '--data', action='store_true', help='Use real data in SIGNAL REGION (by default, will build fake data using estimated QCD). Also, use real data in the fit (by default use Asimov)')
    parser.add_argument('--bbb', action='store_true', help='Add bin-by-bin uncertainties')
    parser.add_argument('--fit-mode', required=True, choices=['shape_CR1', 'abcd'], help='Fit mode')
    parser.add_argument('--qcd-systs', dest='QCD_systs', action='store_true', help='If mode is "shape_CR1", add uncertainty on the QCD shape from the VR/CR2 ratio')
    parser.add_argument('--equal-bins', dest='equal_bins', action='store_true', help='Modify templates to have equal-width bins numbered 1 through nBins, without changing the bin contents. Makes plotting easier if some bins are very fine.')
    parser.add_argument('--rate-systs', nargs='*', help='Input any JSON files with theory rate systematics in the four regions')
    parser.add_argument('--exp-rate', nargs='*', help='Input any JSON files with experimental rate systematics in the four regions')
    parser.add_argument('--sub-folder', help='Select sub-folder inside the input ROOT file')
    parser.add_argument('--fact-theory', nargs='?', choices=['some', 'all', 'OOA'], help='Factorise some theory uncertainties among ttXX components. Either keep all ttbb common ("some"), factorise everything ("all"), or separate in-acceptance ttbb from the other ttbs ("OOA").')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    options = parser.parse_args()

    prepareShapesAndCards(options)


def prepareShapesAndCards(options):

    cb = ch.CombineHarvester()

    if options.fit_mode == 'shape_CR1':
        cats = [
            (1, 'SR'),
            (2, 'CR1')
        ]
        print('-- QCD estimation: fit bin-by-bin by assuming shape in CR1 and SR is the same --')

    elif options.fit_mode == 'abcd':
        cats = [
            (1, 'SR'),
            (2, 'CR1'),
            (3, 'VR'),
            (4, 'CR2'),
        ]
        print('-- QCD etimation: bin-by-bin ABCD using the four regions --')

    # object to handle the factorisation of uncertainties among ttbar components
    factTheory = defs.FactorisedTheory(options.fact_theory)
    
    # factorise shape uncertainties for ttbar components
    theory_shape_systs = []
    for procs, syst in defs.theory_shape_systs:
        for newProcs,newSyst in factTheory.getGrouping(procs, syst):
            theory_shape_systs.append((newProcs, newSyst))
    
    # Process shapes
    processed_shapes = os.path.join(options.output, 'processed_shapes.root')
    QCD_VR_ratios, est_QCD_yields, QCD_shape_CR1, QCD_shape_CR2 = utils.extractShapes(options.input, processed_shapes, defs.tt_bkg + defs.other_bkg, defs.sig_processes, options.data, fact_theory=factTheory, equal_bins=options.equal_bins, sub_folder=options.sub_folder)
    Nbins = len(QCD_VR_ratios)

    cb.AddObservations(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], cats)
    
    cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], defs.sig_processes, cats, True)

    cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], defs.tt_bkg + defs.other_bkg, cats, False)

    ### QCD estimate: add all "delta" templates
    QCD_processes = [ 'QCD_bin_{}'.format(i+1) for i in range(Nbins) ]
    cb.AddProcesses(['*'], ['ttbb'], ['13TeV_2016'], ['FH'], QCD_processes, cats, False)


    ### Systematics
    added_theory_systs = []
    added_exp_systs = []

    # Modeling systematics, not on QCD! ###
    cbWithoutQCD = cb.cp().process_rgx(['QCD.*'], False)
    
    # Theory rate uncertainties from the JSON file
    if options.rate_systs is not None:
        for json_file in options.rate_systs:
            added_theory_systs += addRateSystematics(cb, json_file, options.sub_folder, factTheory)
    
    # Experimental rate uncertainties from the JSON file
    if options.exp_rate is not None:
        for json_file in options.exp_rate:
            added_exp_systs += addRateSystematics(cb, json_file, options.sub_folder)

    # Luminosity
    cbWithoutQCD.AddSyst(cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')(['13TeV_2016'], defs.getLumiUncertainty('13TeV_2016')))
    added_exp_systs.append('lumi_13TeV_2016')

    # Experimental systematics, common for all processes and categories
    for s in defs.exp_systs:
        # If we have added it already as a rate systematics, skip it!
        if s not in added_exp_systs:
            added_exp_systs.append(s)
            cbWithoutQCD.AddSyst(cb, s, 'shape', ch.SystMap()(1.))

    # Theory shape systematics
    for syst in theory_shape_systs:
        if syst[1] not in added_theory_systs:
            added_theory_systs.append(syst[1])
            cbWithoutQCD.cp().process(syst[0]).AddSyst(cb, syst[1], 'shape', ch.SystMap()(1.))
    
    # Theory rate systematics (not taken from JSON)
    for name,syst in defs.theory_rate_systs.items():
        if not name in added_theory_systs:
            added_theory_systs.append(name)
            cbWithoutQCD.AddSyst(cb, name, syst[0], syst[1])

        
    ### QCD systematics: add a lnN for each bin using the ratio QCD_subtr/QCD_est in the VR
    if options.QCD_systs:
        print('-- Will apply bin-by-bin uncertainties on QCD estimate from ratio in VR --')
        if options.fit_mode == 'shape_CR1':
            for i in range(1, Nbins+1):
                # lnN = 1 + abs(1 - QCD_VR_ratios[i-1])
                ratio = QCD_VR_ratios[i-1]
                lnN = ratio if ratio > 1 else 1./ratio
                cb.cp().bin(['SR']).process(['QCD_bin_{}'.format(i)]).AddSyst(cb, 'QCD_shape_bin_{}'.format(i), 'lnN', ch.SystMap()(lnN))
        elif options.fit_mode == 'abcd':
            # using max
            # QCD_VR_ratios = [1.1047956681135658, 1.104982852935791, 1.0103355569221637, 1.0365746040205628, 1.027778957040471, 1.1635257239763037, 1.0604289770126343, 1.0326651334762573, 1.0882024148481384, 1.0879310369491577, 1.2372238755691953, 1.1039656400680542, 1.1208300590515137, 1.1252394914627075, 1.0652162084238805, 1.1746360299507677, 1.1441897907967598, 1.032749056816101, 1.1105864995541361, 1.264707088470459, 1.1289979219436646, 1.1032386479572462, 1.3740112781524658, 1.0779788494110107, 1.0679041983173836, 1.1521316766738892, 1.0189466861549783, 1.1371627554677426, 1.180934637513623, 1.0807719230651855, 1.1220710277557373, 1.2163840919860773, 1.1803903579711914, 1.1331188470149183, 1.2841500043869019, 1.124382576013972, 1.2853591442108154, 1.1161022064238948, 1.0491153764429137, 1.3020191192626953, 1.6365387568006153, 1.3135310411453247, 1.183979775003691, 1.3237843031833378, 1.105936050415039, 1.4582525497144114, 1.2740960121154785, 1.1744883060455322, 1.2689180716203021, 1.5666807889938354, 1.1884409189224243, 1.6787212785213594, 1.1295689911887752, 1.2143068313598633, 1.144478440284729]
            # using geometric average
            QCD_VR_ratios = [1.0556093647141687, 1.0658984862062695, 1.0057472468756388, 1.0208612636340562, 1.0185833946498413, 1.1211169739938442, 1.0353973123690785, 1.0258664065695766, 1.0586147959018684, 1.0522305760086619, 1.1354690006073973, 1.072695547895069, 1.0799492240063984, 1.0621373200388462, 1.0593700756267987, 1.1529412209016232, 1.122536304991689, 1.0187320772559685, 1.0972767308832914, 1.175709681780302, 1.0832093989858067, 1.0823283151259013, 1.1831016555993352, 1.054608634579664, 1.0599488955753065, 1.0752925245754967, 1.017269399510584, 1.122209514629158, 1.1702168450787551, 1.0695165830450506, 1.0857979999559528, 1.2041393773004465, 1.1151294041413826, 1.1230274391829085, 1.2502545040629076, 1.1070056845911258, 1.139110776895264, 1.082765772887927, 1.0487710649869804, 1.2332536614187524, 1.4655095128617284, 1.19038044691305, 1.1104215756611893, 1.1838495100927606, 1.0880046566588846, 1.4004062409319984, 1.248629899444753, 1.1411489734003788, 1.1805956668619682, 1.4378115712379096, 1.129952938278906, 1.3437817991926544, 1.0912141233598036, 1.1453139866153634, 1.1135893789689448]
            for i in range(1, Nbins+1):
                # lnN = 1.05
                lnN = QCD_VR_ratios[i-1]
                cb.cp().bin(['SR']).process(['QCD_bin_{}'.format(i)]).AddSyst(cb, 'QCD_shape_bin_{}'.format(i), 'lnN', ch.SystMap()(lnN))


    extraStrForQCD = ''
    # To define nuisance group with all QCD parameters
    paramListQCD = []
    
    if options.fit_mode == 'shape_CR1':
        ### QCD estimate: fit shape from CR1, normalisation floating
        extraStrForQCD += 'scale_ratio_QCD_CR1_SR extArg 1. [0.,2.]\n'
        paramListQCD.append('scale_ratio_QCD_CR1_SR')
        
        for i in range(1, Nbins+1):
            extraStrForQCD += 'yield_QCD_SR_bin_{0} rateParam SR QCD_bin_{0} 1. [0.,2.]\n'.format(i)
            paramListQCD.append('yield_QCD_SR_bin_{}'.format(i))
    
        for i in range(1, Nbins+1):
            extraStrForQCD += 'yield_QCD_CR1_bin_{0} rateParam CR1 QCD_bin_{0} (@0*@1) scale_ratio_QCD_CR1_SR,yield_QCD_SR_bin_{0}\n'.format(i)
        
        if options.QCD_systs:
            for i in range(1, Nbins+1):
                paramListQCD.append('QCD_shape_bin_{}'.format(i))
    
    elif options.fit_mode == 'abcd':
        ### QCD estimate: add the rate params for each bin in the CR1, CR2 and VR
        ### The yield in the SR is then expressed as CR1*VR/CR2
        for i in range(1, Nbins+1):
            # yield_CR2 = est_QCD_yields['CR2'] * QCD_shape_CR2[i-1]
            # yield_CR1 = est_QCD_yields['CR1'] * QCD_shape_CR1[i-1]
            # yield_VR = est_QCD_yields['VR'] * QCD_shape_CR2[i-1]
            # extraStrForQCD += 'yield_QCD_CR2_bin_{0} rateParam CR2 QCD_bin_{0} {1} [0,25000]\n'.format(i, yield_CR2)
            # extraStrForQCD += 'ratio1_QCD_bin_{0} extArg {1} [0.,5.]\n'.format(i, yield_CR1 / yield_CR2)
            # extraStrForQCD += 'ratio2_QCD_bin_{0} extArg {1} [0.,5.]\n'.format(i, yield_VR / yield_CR2)
            # extraStrForQCD += 'yield_QCD_CR2_bin_{0} rateParam CR2 QCD_bin_{0} 1. [0.,5.]\n'.format(i)
            # extraStrForQCD += 'ratio1_QCD_bin_{0} extArg 1. [0.,5.]\n'.format(i)
            # extraStrForQCD += 'ratio2_QCD_bin_{0} extArg 1. [0.,5.]\n'.format(i)
            # extraStrForQCD += 'yield_QCD_CR1_bin_{0} rateParam CR1 QCD_bin_{0} @0*@1 yield_QCD_CR2_bin_{0},ratio1_QCD_bin_{0}\n'.format(i)
            # extraStrForQCD += 'yield_QCD_VR_bin_{0} rateParam VR QCD_bin_{0} @0*@1 yield_QCD_CR2_bin_{0},ratio2_QCD_bin_{0}\n'.format(i)
        
            # extraStrForQCD += 'yield_QCD_SR_bin_{0} rateParam SR QCD_bin_{0} @0*@1*@2 yield_QCD_CR2_bin_{0},ratio1_QCD_bin_{0},ratio2_QCD_bin_{0}\n'.format(i)
            
            # paramListQCD.append('yield_QCD_CR2_bin_{}'.format(i))
            # paramListQCD.append('ratio1_QCD_bin_{}'.format(i))
            # paramListQCD.append('ratio2_QCD_bin_{}'.format(i))
    
            extraStrForQCD += 'yield_QCD_CR1_bin_{0} rateParam CR1 QCD_bin_{0} 1. [0.,5.]\n'.format(i)
            extraStrForQCD += 'yield_QCD_CR2_bin_{0} rateParam CR2 QCD_bin_{0} 1. [0.,5.]\n'.format(i)
            extraStrForQCD += 'yield_QCD_VR_bin_{0} rateParam VR QCD_bin_{0} 1. [0.,5.]\n'.format(i)
        
            extraStrForQCD += 'yield_QCD_SR_bin_{0} rateParam SR QCD_bin_{0} (@0*@1/@2) yield_QCD_VR_bin_{0},yield_QCD_CR1_bin_{0},yield_QCD_CR2_bin_{0}\n'.format(i)
            
            paramListQCD.append('yield_QCD_CR1_bin_{}'.format(i))
            paramListQCD.append('yield_QCD_CR2_bin_{}'.format(i))
            paramListQCD.append('yield_QCD_VR_bin_{}'.format(i))
    
    cb.AddDatacardLineAtEnd(extraStrForQCD)

    # Define systematic groups
    syst_groups = {
            "theory": added_theory_systs,
            "exp": added_exp_systs,
            "QCD": paramListQCD,
            "extern": defs.externalised_nuisances,
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
        print('-- Will add bin-by-bin uncertainties for MC statistics --')
        # MC statistics - has to be done after the shapes have been extracted!
        # bbb_bkg = ch.BinByBinFactory().SetVerbosity(5)
        # bbb_bkg.SetAddThreshold(0.05).SetMergeThreshold(0.5).SetFixNorm(False)
        # bbb_bkg.MergeBinErrors(cb.cp().backgrounds())
        # bbb_bkg.AddBinByBin(cb.cp().backgrounds(), cb)

        # bbb_sig = ch.BinByBinFactory().SetVerbosity(5).SetAddThreshold(0.2).SetFixNorm(False)
        # bbb_sig.AddBinByBin(cbWithoutQCD.cp().signals(), cb)

        # Use combine internal BBB (default: BB lite, merging everything for sig & bkg separately?)
        cb.AddDatacardLineAtEnd("* autoMCStats 0 0 1\n")
    
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

RMIN=0.
RMAX=5.0
NPOINTS=50
FIT_OPT=( --freezeNuisanceGroups=extern --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=999999999 --X-rtd MINIMIZER_analytic --robustFit 1 --cminDefaultMinimizerPrecision 1E-12 )
"""
    if options.data:
        print("WILL USE REAL DATA IN SR")
        initWorkSpace += 'TOY=""\n'
    else:
        print("Will use Asimov toy")
        initWorkSpace += 'TOY="-t -1\n"'

    def createScript(content, filename):
        script_path = os.path.join(output_dir, filename)
        with open(script_path, 'w') as f:
            f.write(initWorkSpace)
            f.write(content)
        # make script executable
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | stat.S_IEXEC)

    # Script: simple fits
    script = """
combine -M MultiDimFit -d workspace.root --rMin $RMIN --rMax $RMAX --expectSignal=1 ${TOY} --algo singles --setCrossingTolerance 1E-7 "${FIT_OPT[@]}"
#combine -M FitDiagnostics -d workspace.root --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1 --skipBOnlyFit --saveShapes --saveNormalizations --saveWithUncertainties --plots "${FIT_OPT[@]}"
#combine -M MultiDimFit -d workspace.root --rMin $RMIN --rMax $RMAX --expectSignal $1 -t 1000 -n _freq_$1 --toysFrequentist "${FIT_OPT[@]}" > freq_$1.log

# Goodness of fit
#combine -M GoodnessOfFit workspace.root --algo=saturated "${FIT_OPT[@]}" 
#parallel --gnu -j 5 combine -M GoodnessOfFit workspace.root --algo=saturated "${FIT_OPT[@]}" -t 100 -s 12345{} --toysFreq ::: {1..10}
"""
    createScript(script, 'do_fit.sh')


    # Script: plots of NLL vs. r for different uncertainties
    script = """
RMIN=0.5
RMAX=3.
combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1 -n _nominal workspace.root "${FIT_OPT[@]}"
combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1 -n _stat -S 0 workspace.root "${FIT_OPT[@]}"

# for post-fit: save best-fit parameters to workspace
#combine -M MultiDimFit --rMin $RMIN --rMax $RMAX -n _snap --saveWorkspace workspace.root "${FIT_OPT[@]}"
#combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX -n _stat -S 0 --snapshotName "MultiDimFit" -d higgsCombine_snap.MultiDimFit.mH120.root "${FIT_OPT[@]}"

plot1DScan.py higgsCombine_nominal.MultiDimFit.mH120.root --others 'higgsCombine_stat.MultiDimFit.mH120.root:Freeze all:2' --breakdown syst,stat

# also do frozen theory (not used anymore)
#combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1 -n _theory --freezeNuisanceGroups theory workspace.root "${FIT_OPT[@]}"
#plot1DScan.py higgsCombine_nominal.MultiDimFit.mH120.root --others 'higgsCombine_theory.MultiDimFit.mH120.root:Freeze theory:4' 'higgsCombine_stat.MultiDimFit.mH120.root:Freeze all:2' --breakdown theory,syst,stat

#combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1  "${FIT_OPT[@]}" -n _freeze_jet workspace.root --freezeParameters 'rgx{CMS_.*_j$}'
#plot1DScan.py higgsCombine_freeze_jet.MultiDimFit.mH120.root --output scan_freeze_jet

#combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1  "${FIT_OPT[@]}" -n _freeze_qg workspace.root --freezeParameters CMS_qg_Weight
#plot1DScan.py higgsCombine_freeze_qg.MultiDimFit.mH120.root --output scan_freeze_qg

#combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1  "${FIT_OPT[@]}" -n _freeze_btag workspace.root --freezeParameters 'rgx{.*btag.*}'
#plot1DScan.py higgsCombine_freeze_btag.MultiDimFit.mH120.root --output scan_freeze_btag

#combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1  "${FIT_OPT[@]}" -n _freeze_theory workspace.root --freezeNuisanceGroups theory
#plot1DScan.py higgsCombine_freeze_theory.MultiDimFit.mH120.root --output scan_freeze_theory

#combine -M MultiDimFit --algo grid --points $NPOINTS --rMin $RMIN --rMax $RMAX ${TOY} --expectSignal=1  "${FIT_OPT[@]}" -n _freeze_exp workspace.root --freezeNuisanceGroups exp
#plot1DScan.py higgsCombine_freeze_exp.MultiDimFit.mH120.root --output scan_freeze_exp
    """
    createScript(script, 'do_DeltaNLL_plot.sh')


    # Script: impacts signal injected
    script = """
mkdir impacts
pushd impacts

combineTool.py -M Impacts -d ../workspace.root ${TOY} -m 120 --rMin $RMIN --rMax $RMAX --expectSignal=1 --doInitialFit "${FIT_OPT[@]}"
combineTool.py -M Impacts -d ../workspace.root ${TOY} -m 120 --rMin $RMIN --rMax $RMAX --expectSignal=1 --doFits --parallel 6 "${FIT_OPT[@]}" --setParameterRanges CMS_qg_Weight=-2,2 --cminPreScan
combineTool.py -M Impacts -d ../workspace.root -m 120 -o impacts_signal_injected.json
plotImpacts.py -i impacts_signal_injected.json -o impacts_signal_injected
plotImpacts.py -i impacts_signal_injected.json -o impacts_qcd --groups QCD
plotImpacts.py -i impacts_signal_injected.json -o impacts_no_qcd --veto-groups QCD extern

popd
    """
    createScript(script, 'do_impacts_signal_injected.sh')


    # Script: plots of NLL vs. nuisance parameters
    script = """
function scan_param() {{
    combine -M MultiDimFit --algo grid --points 20 -n _$1 ../workspace.root --setParameters r=1 ${{TOY}} --setParameterRanges r=0,2:$1={scan} -P $1 "${{FIT_OPT[@]}}" --floatOtherPOIs 1
    plot1DScan.py higgsCombine_$1.MultiDimFit.mH120.root --output scan_$1 --POI $1
 
    combine -M MultiDimFit --algo grid --points 20 -n _freeze_$1 ../workspace.root --setParameters r=1 ${{TOY}} --setParameterRanges r=0,2:$1={scan} -P $1 "${{FIT_OPT[@]}}" -S 0 --floatOtherPOIs 1
    plot1DScan.py higgsCombine_freeze_$1.MultiDimFit.mH120.root --output scan_freeze_$1 --POI $1
    
    combine -M MultiDimFit --algo grid --points 20 -n _freezeQCD_$1 ../workspace.root --setParameters r=1 ${{TOY}} --setParameterRanges r=0,2:$1={scan} -P $1 --freezeNuisanceGroups extern,QCD --floatOtherPOIs 1
    plot1DScan.py higgsCombine_freezeQCD_$1.MultiDimFit.mH120.root --output scan_freezeQCD_$1 --POI $1
}}
export -f scan_param # needed for parallel

mkdir scans
pushd scans
SHELL=/bin/bash parallel --gnu -j 6 scan_param ::: {params}
popd
"""
    createScript(script.format(scan="0.5,1.5", params=" ".join(syst_groups['QCD'])), 'do_QCD_scans.sh')
    createScript(script.format(scan="-2,2", params=" ".join(syst_groups['exp'])), 'do_exp_scans.sh')
    createScript(script.format(scan="-2,2", params=" ".join(syst_groups['theory'])), 'do_theory_scans.sh')
    
    script = """
function scan_param() {{
    combine -M MultiDimFit --algo grid --points 20 -n _$1 ../workspace.root --setParameters r=1 ${{TOY}} --setParameterRanges r=0,2 -P $1 --autoRange 3 "${{FIT_OPT[@]}}" --floatOtherPOIs 1
    plot1DScan.py higgsCombine_$1.MultiDimFit.mH120.root --output scan_$1 --POI $1
    
    combine -M MultiDimFit --algo grid --points 20 -n _freeze_$1 ../workspace.root --setParameters r=1 ${{TOY}} --setParameterRanges r=0,2 -P $1 --autoRange 3 "${{FIT_OPT[@]}}" -S 0 --floatOtherPOIs 1
    plot1DScan.py higgsCombine_freeze_$1.MultiDimFit.mH120.root --output scan_freeze_$1 --POI $1
}}
export -f scan_param # needed for parallel

mkdir scans
pushd scans
SHELL=/bin/bash parallel --gnu -j 6 scan_param ::: {params}
popd
"""
    createScript(script.format(params=" ".join(syst_groups['QCD'])), 'do_QCD_scans.sh')


def addRateSystematics(cb, json_path, sub_folder=None, factTheory=None):
    # JSON is encoded as UTF8 by default, and that messes with the combineHarvester bindings
    def ascii_encode_dict(data):
        def ascii_encode(x):
            if isinstance(x, unicode): return x.encode('ascii')
            else: return x
        return dict(map(ascii_encode, pair) for pair in data.items())

    with open(json_path) as _f:
        systs = json.load(_f, object_hook=ascii_encode_dict)

    if sub_folder is not None:
        systs = systs[sub_folder]

    # Load all systematics in easier order
    # newSysts[systematic] = [ (cat, proc, (down, up)), ... ]
    newSysts = {}
    for cat in systs.keys():
        for sys in systs[cat].keys():
            sys_dict = newSysts.setdefault(sys, [])
            proc_up = set(systs[cat][sys]["Up"].keys())
            proc_down = set(systs[cat][sys]["Down"].keys())
            assert(proc_up == proc_down)
            for proc in proc_up:
                value_up = systs[cat][sys]["Up"][proc]
                value_down = systs[cat][sys]["Down"][proc]
                sys_dict.append( (cat, proc, (value_down, value_up)) )

    # Re-create systematics for those we want factorised among ttbar components
    # expects definitions.FactorisedTheory object
    if factTheory is not None:
        for name, syst in newSysts.items():
            if name in factTheory.factorised_uncertainties:
                newSysts[name] = []
                for entry in syst:
                    newSysts.setdefault(factTheory.getNewNuisance(name, entry[1]), []).append(entry)
                # So that the returned list of systematics makes sense:
                if len(newSysts[name]) == 0:
                    newSysts.pop(name)

    # print(newSysts)

    for name, syst in newSysts.items():
        cm = ch.SystMap('bin', 'process')
        for entry in syst:
            cm = cm([entry[0]], [entry[1]], entry[2])
        cb.cp().AddSyst(cb, name, 'lnN', cm)

    return newSysts.keys()
                
    

if __name__ == '__main__':
    main()
