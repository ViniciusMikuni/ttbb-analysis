#!/usr/bin/env python
import sys
from os import environ, path

environ['KERAS_BACKEND'] = 'theano'
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'
from MVA_cfg import *
import ROOT
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, SGD
from keras.regularizers import l2

# in order to start TMVA
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()

#Currently Multiclass + categories does not work in TMVA, hence Multiclass will be handled for each category separately



# onlyPerfect = 0
# use1ad = 1

# if len(sys.argv) > 2:
#     onlyPerfect = int(sys.argv[1])
#     use1ad = int(sys.argv[2])

# print 'Using only correct combinations? ',onlyPerfect
# print 'Using only 7 jets? ',use1ad

# open input file, get trees, create output file
#file1 = ROOT.TFile('..//Datasets/Correct_NoBtag_ttbar_Full.root')
file1 = ROOT.TFile('../Datasets/ttbar_MVA_Full.root')
#file1 = ROOT.TFile('../Datasets/Correct_NoBtag_ttbar_full.root')
#file1 = ROOT.TFile('../Datasets/Skimmed_Ttbar.root')

tree_s = file1.Get('tree')
#file2 = ROOT.TFile('..//Datasets/Skimmed_QCD.root')
#tree_b = file1.Get('tree')
    
fname = "MVA_Multi"

mycats = ['3b','4b','5b']

filestr = '_Multi_'
#if use1ad == 1: filestr+='1ad'
#else:filestr+='2ad'
#if onlyPerfect:fname+='Deep'
#else: fname+='Full'
#fname+=catstr
    
fout = ROOT.TFile('MVA_root/'+filestr+".root","RECREATE")
 
# define factory with options
analysistype = 'AnalysisType=Multiclass'
factory = {}
for cat in mycats:
    factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=None",
                                          analysistype]
                                     ))
 
# add discriminating variables for training
#first 2 are going to be the b's


dataset = ROOT.TMVA.DataLoader('MVA_weights')

#dataset2add = ROOT.TMVA.DataLoader('MVA_weights_2ad')




usevar =['tt_m', 'tt_pt', 'tt_phi', 'tt_eta', 'b1_m', 'b1_pt', 'b1_phi', 'b1_eta', 'b2_m', 'b2_pt', 'b2_phi', 'b2_eta', 'lq1_m', 'lq1_pt', 'lq1_phi', 'lq1_eta', 'lq2_m', 'lq2_pt', 'lq2_phi', 'lq2_eta', 'lp1_m', 'lp1_pt', 'lp1_phi', 'lp1_eta', 'lp2_m', 'lp2_pt', 'lp2_phi', 'lp2_eta', 'w1_m', 'w1_pt', 'w1_phi', 'w1_eta', 'w2_m', 'w2_pt', 'w2_phi', 'w2_eta', 'top1_m', 'top1_pt', 'top1_phi', 'top1_eta', 'top2_m', 'top2_pt', 'top2_phi', 'top2_eta', 'deltaRb1w1', 'deltaRb1w2', 'deltaEtaaddb1', 'deltaEtaaddb2', 'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'jet5pt', 'deltaPhiaddtop1', 'deltaPhiaddtop2', 'n_jets', 'deltaEtaaddtop2', 'deltaPhiq1q2', 'deltaEtaaddtop1', 'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1', 'simple_chi2', 'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q', 'deltaEtaaddw2', 'deltaEtaaddw1', 'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2', 'memttbb', 'closest_mass', 'girth', 'deltaPhib1b2', 'jets_dRavg', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2', 'all_mass', 'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']




#['deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','deltaPhiaddb1','deltaPhiaddb2','deltaPhiaddw1','deltaPhiaddw2','deltaPhiaddtop1','deltaPhiaddtop2','deltaEtaaddb1','deltaEtaaddb2','deltaEtaaddw1','deltaEtaaddw2','deltaEtaaddtop1','deltaEtaaddtop2','addJet_CSV[0]','ht','btagLR4b','btagLR3b','BDT_CWoLa','BDT_Comb','BDT_FullQCD','meanCSV','meanDeltaRbtag']

#,'addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','tt_pt','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]',

if use1ad == 0:
    usevar += ['addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass','addJet_QGL[1]']

# if onlyPerfect == 0:
#     usevar1add = ['BDT_ttbb','BDT_ttcc','BDT_ttlf','meanCSVbtag','meanDeltaRbtag','centrality','meanCSV']
#     usevar2add = usevar1add


#usevar1add = ['deltaPhib1b2','deltaRb1b2','addJet_deltaR','addJet_deltaPhi','deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','addJet_CSV[0]','addJet_pt[0]','ht','btagLR4b','btagLR3b','addJet_deltaEta','meanDeltaRbtag','meanCSV','meanCSVbtag','BDT_Comb','addJet_QGL[0]','memttbb','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','BDT_QCD']
# usevar2add = ['deltaPhib1b2','deltaRb1b2','addJet_deltaR','addJet_deltaPhi','deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','addJet_CSV[0]','addJet_pt[0]','ht','btagLR4b','btagLR3b','addJet_deltaEta','meanDeltaRbtag','meanCSV','meanCSVbtag','BDT_Comb','addJet_QGL[0]','memttbb','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','n_jets','BDT_QCD','addJet_QGL[1]','addJet_CSV[1]','addJet_pt[1]']


# usevar1add = ['deltaPhib1b2','prob_chi2','mindeltaRb1q','mindeltaRb2p','deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','addJet_CSV[0]','addJet_pt[0]','ht','top1_m-top2_m','w1_m-w2_m','btagLR4b','btagLR3b','centrality','tt_m','tt_pt','meanDeltaRbtag','meanCSV','BDT_Comb','BDT_ttcc','BDT_ttbar','BDT_ttall','BDT_ttbar_avg','BDT_ttcc_avg','BDT_ttall_avg']
# usevar2add = ['deltaPhib1b2','prob_chi2','addJet_deltaR','addJet_deltaPhi','mindeltaRb1q','mindeltaRb2p','deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','addJet_CSV[0]','addJet_CSV[1]','addJet_pt[0]','addJet_pt[1]','ht','n_addJets','top1_m-top2_m','w1_m-w2_m','btagLR4b','btagLR3b','centrality','tt_m','tt_pt','addJet_deltaEta','meanDeltaRbtag','meanCSV','BDT_Comb','BDT_ttcc','BDT_ttbar','BDT_ttall','BDT_ttbar_avg','BDT_ttcc_avg','BDT_ttall_avg']

for var in usevar:
    print var
    dataset.AddVariable(var,'F' if'n_' not in var else'I')


sigcut = ROOT.TCut("addJet_CSV[0] > 0")
if onlyPerfect == 0:
    sigcut = ROOT.TCut("addJet_CSV[0] > 0 ")
#sigcut = ROOT.TCut()

cutList = {
    'ttbbCut':ROOT.TCut("ttCls>52"),
    'tt2bCut':ROOT.TCut("ttCls==52"),
    'ttbCut':ROOT.TCut("ttCls==51"),
    'ttccCut':ROOT.TCut("ttCls<= 46 && ttCls > 0"),
    'ttbarCut':ROOT.TCut("ttCls==0"),
    'ttbbAllCut':ROOT.TCut("ttCls>=51"),
    'ttallCut':ROOT.TCut("ttCls>=0 && ttCls <= 46")
}
addCut = ROOT.TCut('n_bjets >= 4')
if use1ad:
    addCut = ROOT.TCut('n_bjets == 3')



if use1ad:
    dataset.AddTree(tree_s,'ttbb',1.0,cutList['ttbbAllCut'])
    dataset.AddTree(tree_s,'ttcc',1.0,cutList['ttccCut'])
    dataset.AddTree(tree_s,'ttbar',1.0,cutList['ttbarCut'])
    dataset.SetWeightExpression('weight','ttbb')
    dataset.SetWeightExpression('weight','ttcc')
    dataset.SetWeightExpression('weight','ttbar')
    #dataset.AddTree(tree_b,'QCD',1.0)
else:
    dataset.AddTree(tree_s,'ttbb',1.0,cutList['ttbbAllCut'])
    dataset.AddTree(tree_s,'ttcc',1.0,cutList['ttccCut'])
    dataset.AddTree(tree_s,'ttbar',1.0,cutList['ttbarCut'])
    #dataset.AddTree(tree_b,'QCD',1.0)
    dataset.SetWeightExpression('weight','ttbb')
    dataset.SetWeightExpression('weight','ttcc')
    dataset.SetWeightExpression('weight','ttbar')
    
dataset.PrepareTrainingAndTestTree(sigcut+addCut,
                                   ":".join(["SplitMode=Random",
                                             "NormMode=NumEvents",
                                             "TrainTestSplit_ttbb=0.8",
                                             "TrainTestSplit_ttcc=0.8",
                                             "TrainTestSplit_ttbar=0.8",
                                             # "nTrain_ttbb=1000",
                                             # "nTrain_ttcc=1000",
                                             # "nTrain_ttbar=1000",
                                             # "nTest_ttbb=1000",
                                             # "nTest_ttcc=1000",
                                             # "nTest_ttbar=1000",
                                             "V"
                                   ]))




if onlyPerfect:filestr='_multi_Deep'
#if not path.isfile('models/model1add_'+bkg+'.h5'):
PyDNN_Opt(filestr, len(usevar),3)
#if not path.isfile('models/model2add_'+bkg+'.h5'):
#PyDNN_Opt(filestr+'_2ad', len(usevar2add),3)

#"BDT","BDTA,"PyDNN""
UseMethod = ['BDT']
mcat = {}


for key in UseMethod:
    mcat[key] = factory.BookMethod(dataset,methodList[key][0],key +filestr,methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+filestr+'.h5')


# self-explaining
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
