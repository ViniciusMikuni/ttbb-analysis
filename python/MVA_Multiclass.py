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



#file1 = ROOT.TFile('../Datasets/ttbar_MVA.root')
#file1 = ROOT.TFile('../Datasets/Correct_NoBtag_ttbar_full.root')
file1 = ROOT.TFile('../Datasets/Skimmed_Ttbar.root')

tree_s = file1.Get('tree')
    
fname = "MVA_Multi"
analysistype = 'AnalysisType=Multiclass'
filestr = '_Multi_'
usevar =[  'b2_phi',   'lq1_phi',    'lq2_phi',    'top1_m',  'top2_phi',  'deltaPhiaddtop2', 'deltaRaddb1', 'deltaRaddb2',  'btagLR4b',   'btagLR3b',    'deltaRb2p1',  'p1b2_mass',  'deltaPhil1l2',  'q1b1_mass',   'ht', 'deltaPhib1b2', 'jets_dRavg','jets_dRmin',  'meanCSV', 'deltaRb1b2',  'mindeltaRb2p', 'meanCSVbtag',  'addJet_CSV[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']

#'memttbb','n_jets','simple_chi2','deltaEtaaddb1', 'deltaEtaaddb2', 'jet5pt','b1_m','all_mass','top1_eta','top2_eta','w1_eta','w2_eta', 'b2_m', 'b1_pt', 'b2_pt','jet_CSV[0]','w1_pt','w2_pt','lq1_pt','lq2_pt','lp1_pt','lp2_pt','lp1_eta','lq2_eta','lp2_eta','lq1_eta','girth','lq1_m','lq2_m','lp1_m','lp2_m','tt_m','deltaEtaaddtop2','deltaEtaaddtop1','deltaEtaaddw2','deltaEtaaddw1','w1_phi','w2_phi',
# 'BDT_CWoLa,'addJet_QGL[0]','addJet_QGL[1]', ,'addJet_mass', 'deltaRaddw2', 'prob_chi2', 'BDT_Comb', 'deltaRl1l2', 'deltaEtaw1w2','tt_eta','top1_pt', 'deltaEtat1t2','deltaRaddtop2','deltaRaddw1','deltaRb1w1','jet_CSV[1]','deltaRb1top2','addJet_pt[0]','top2_pt','deltaRb2w1','tt_pt', 'deltaRq1q2', 'centrality','jet_MOverPt[1]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','deltaRb2top1', 'aplanarity','deltaEtab1b2','deltaRaddtop1', 'deltaRb1w2', 'deltaPhiaddtop1','deltaEtaq1q2', 'deltaRb2w2','addJet_deltaEta','deltaPhit1t2', 'deltaPhiaddw2','jets_dRmax','deltaPhiq1q2','deltaEtal1l2','lp1_phi', 'w2_m','addJet_deltaR','b1_eta','top1_phi','w1_m',  'mindeltaRb1q', 'tt_phi',   'deltaPhiaddw1', 'b2_eta', 'addJet_deltaPhi','lp2_phi', 'deltaPhiaddb2',  'deltaRb1q1',    'closest_mass', 'deltaPhiaddb1','deltaPhiw1w2', 'jet_MOverPt[2]',   'top2_m',  'meanDeltaRbtag','b1_phi', 'jet_QGL[0]','jet_MOverPt[0]',

useadd = ['addJet_CSV[1]','addJet_pt[1]']


sigcut = ROOT.TCut('jet_QGL[0]>=0 && jet_QGL[1]>=0 && jet_QGL[2]>=0 && jet_QGL[3]>=0 && jet_QGL[4]>=0 && jet_QGL[5]>=0 && jet_CSV[0]>=0 && jet_CSV[1]>=0 && jet_CSV[2]>=0 && jet_CSV[3]>=0 && jet_CSV[4]>=0 && jet_CSV[5]>=0')

cutList = {
    'ttbb':ROOT.TCut("ttCls>52"),
    'tt2b':ROOT.TCut("ttCls==52"),
    'ttb':ROOT.TCut("ttCls==51"),
    'ttcc':ROOT.TCut("ttCls<= 46 && ttCls > 0"),
    'ttlf':ROOT.TCut("ttCls==0"),
    'ttbbAll':ROOT.TCut("ttCls>=51"),
    'ttAll':ROOT.TCut("ttCls>=0 && ttCls <= 46")
}


factory = ROOT.TMVA.Factory("TMVAClassification", ROOT.TFile('MVA_root/'+fname+".root","RECREATE"),
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=None",
                                          analysistype]
                                     ))

mycats = {'3b':'n_bjets>=3'}

#          ,'n_bjets==4','n_bjets>=5']
#mycats = ['n_jets==7','n_jets==8','n_jets>=9']

UseMethod = ['PyDNN','BDT']

MVA_cats = {}
for cat in mycats:
    MVA_cats[cat] = { 
        'Dataset': ROOT.TMVA.DataLoader('MVA_weights'),
        #'Variables': usevar if cat == 'n_jets==7' else usevar + useadd,
        'Variables': usevar + useadd,
        'cut':ROOT.TCut(mycats[cat])
    }

    for var in MVA_cats[cat]['Variables']:
        MVA_cats[cat]['Dataset'].AddVariable(var,'F')
        
    MVA_cats[cat]['Dataset'].AddTree(tree_s,'ttbb',1.0e4/38862.0,cutList['ttbb'])
    MVA_cats[cat]['Dataset'].AddTree(tree_s,'tt2b',1.0e4/26293.0,cutList['tt2b'])
    MVA_cats[cat]['Dataset'].AddTree(tree_s,'ttb',1.0e4/45790.0,cutList['ttb'])
    MVA_cats[cat]['Dataset'].AddTree(tree_s,'ttcc',1.0e4/211503.0,cutList['ttcc'])
    MVA_cats[cat]['Dataset'].AddTree(tree_s,'ttlf',1.0e4/499928.0,cutList['ttlf'])
    # MVA_cats[cat]['Dataset'].AddTree(tree_s,'ttbb',1.0,cutList['ttbb'])
    # MVA_cats[cat]['Dataset'].AddTree(tree_s,'tt2b',1.0,cutList['tt2b'])
    # MVA_cats[cat]['Dataset'].AddTree(tree_s,'ttb',1.0,cutList['ttb'])
    # MVA_cats[cat]['Dataset'].AddTree(tree_s,'ttcc',1.0,cutList['ttcc'])
    # MVA_cats[cat]['Dataset'].AddTree(tree_s,'ttlf',1.0,cutList['ttlf'])

    MVA_cats[cat]['Dataset'].SetWeightExpression('weight','ttbb')
    MVA_cats[cat]['Dataset'].SetWeightExpression('weight','tt2b')
    MVA_cats[cat]['Dataset'].SetWeightExpression('weight','ttb')
    MVA_cats[cat]['Dataset'].SetWeightExpression('weight','ttcc')
    MVA_cats[cat]['Dataset'].SetWeightExpression('weight','ttlf')
    MVA_cats[cat]['Dataset'].PrepareTrainingAndTestTree(sigcut+MVA_cats[cat]['cut'],
                                                        ":".join(["SplitMode=Random",
                                                                  "NormMode=EqualNumEvents",
                                                                  "TrainTestSplit_ttbb=0.8",
                                                                  "TrainTestSplit_ttb=0.8",
                                                                  "TrainTestSplit_tt2b=0.8",
                                                                  "TrainTestSplit_ttcc=0.8",
                                                                  "TrainTestSplit_ttlf=0.8",
                                                                  # "nTrain_ttbb=1000",
                                                                  # "nTrain_ttcc=1000",
                                                                  # "nTrain_ttlf=1000",
                                                                  # "nTest_ttbb=1000",
                                                                  # "nTest_ttcc=1000",
                                                                  # "nTest_ttlf=1000",
                                                                  "V"
                                                        ]))

    PyDNN_Opt(filestr+cat, len(usevar + useadd),5)
    for key in UseMethod:
        factory.BookMethod(MVA_cats[cat]['Dataset'],methodList[key][0],key +filestr+cat,methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+filestr+cat+'.h5')


# self-explaining
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
