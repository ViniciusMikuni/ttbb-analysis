#import os
import ROOT as rt
#import  tdrstyle
#import CMS_lumi
import array
from Plotting_cfg import *
#import numpy as np
#from math import *
from Make_Hists import Make_Hists

rt.gROOT.SetBatch(True)
#rt.gROOT.LoadMacro("../src/triggerWeightRound.h+")
#tdrstyle.setTDRStyle()

#add_cut = '(n_jets >=8 && simple_chi2<23.41 && BDT_CWoLa > 0.27 && BDT_Comb > 0.83 && qgLR > 0.39)'
#add_cut = '(n_jets >=8 && simple_chi2<9.4301 && BDT_CWoLa > 0.3234 && BDT_Comb > -0.971857 && qgLR > 0.636581)'
#add_cut = '(n_jets >=8 && BDT_CWoLa > 0.180626 && BDT_Comb >0.857525 && qgLR > 0.378745 )'
#add_cut = '(n_jets >=8 && BDT_CWoLa > 0.276738 && qgLR > 0.445648 )'


#add_cut = '(n_jets>=8 && simple_chi2<38.8797 && BDT_CWoLa > 0.335974 && BDT_Comb > -0.661968 && qgLR > 0.35119)'
#add_cut = '(n_jets>=8 && BDT_CWoLa > 0.479077  && qgLR > 0.62846)' #10% tmva



#add_cut = '(n_jets>=8 && simple_chi2<19.7491 && BDT_CWoLa > 0.206721 && BDT_Comb > 0.664107 && qgLR > 0.444917)' #TMVA 30% without btagLR info
fname = 'hCard_CR.root'
interest_var_ = ['nBCSVM']
#interest_var_ = ['btagLR4b']
files = {}
tree = {}
sys_ =[
    '_btagweight_hf',
    '_btagweight_cferr1',
    '_btagweight_cferr2',
    '_btagweight_lf',
    '_btagweight_lfstats2',
    '_btagweight_lfstats1',
    '_btagweight_jes',
    '_puweight',
    #'_topweight',
    '_qgweight',

    '_RelativeStatEC',
    '_RelativeStatHF',
    '_PileUpDataMC',
    '_PileUpPtRef',
    '_PileUpPtBB',
    '_PileUpPtEC1',
    '_PileUpPtEC2',
    '_PileUpPtHF',
    '_RelativeStatFSR',
    '_RelativeFSR',
    '_AbsoluteScale',
    '_AbsoluteFlavMap',
    '_AbsoluteMPFBias',
    '_Fragmentation',
    '_SinglePionECAL',
    '_SinglePionHCAL',
    '_FlavorQCD',
    '_TimePtEta',
    '_RelativeJEREC1',
    '_RelativeJEREC2',
    '_RelativeJERHF',
    '_RelativePtBB',
    '_RelativePtEC1',
    '_RelativePtEC2',
    '_RelativePtHF',
    '_SubTotalPileUp',
    '_JER',
    '_AbsoluteStat',
    '_Total',


]

directions_ = ['Up','Down']
processlist = ['data','ttbar','diboson','ttV','VJ','stop','QCD']
for iproc, process in enumerate(processlist): #ntuple files
        if process in processgroup:
            for subprocess in processgroup[process]:
                files[subprocess]=rt.TFile(processfiles[subprocess],"READ")
                tree[subprocess]= files[subprocess].Get('tree')
        elif process == 'ttbar':
            for tproc in ttplot:
                files[tproc]=rt.TFile(processfiles[process],"READ")
                tree[tproc]= files[tproc].Get('tree')
        else:

            files[process] =rt.TFile(processfiles[process],"READ")
            tree[process] =files[process].Get('tree')

add_cut = '(n_jets>=8 && prob_chi2>6e-2 && BDT_CWoLa > 0.5 && qgLR < 0.6 )' #RGS
Make_Hists(interest_var_,'','',False,processlist,tree,add_cut,fname = fname) #remember that if qgLR cut changes so do qwfactor
# Make_Hists(interest_var_,'_JER','Up',False,processlist,tree,add_cut) #remember that if qgLR cut changes so do qwfactor
# Make_Hists(interest_var_,'_JER','Down',False,processlist,tree,add_cut) #remember that if qgLR cut
# Make_Hists(interest_var_,'_btagweight_hf','Down',True,processlist,tree,add_cut)
#changes so do qwfactor

for sys in sys_:
        for dire in directions_:
                if 'weight' in sys:
                    is_weight = True
                    add_cut = '(n_jets>=8 && prob_chi2>6e-2 && BDT_CWoLa > 0.5 && qgLR < 0.6)' #RGS
                else:
                    is_weight = False
                    add_cut = '(n_jets>=8 && prob_chi2{0}{1}>6e-2 && BDT_CWoLa{0}{1} > 0.5 && qgLR{0}{1} < 0.6)'.format(sys,dire) #RGS
                print add_cut
                Make_Hists(interest_var_,sys,dire,is_weight,processlist,tree,add_cut,fname=fname)
