#!/usr/bin/env python
import sys
from os import environ, path
environ['KERAS_BACKEND'] = 'tensorflow'
#environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'
from MVA_cfg import *
import ROOT
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, SGD
from keras.regularizers import l2
ROOT.gROOT.SetBatch(True)

# in order to start TMVA
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()
ROOT.gROOT.LoadMacro("../src/triggerWeightRound.h+")
#Remember the best so far: MC + Data for ttbar region

#currently multiclass does not work for unknown reasons
runSimpleGridSearch = False
# open input file, get trees, create output file
useData = False
useCWoLa = False
useDeep = False
isCut = True
isTest = True
cwolaname = '_CWoLa'


#CWoLa_Test: CWoLa without BDT_Comb
#CWoLa: Currently best for CWoLa
#Data_Test: n_jets == 7 MC ttbar + data (currently the best) needs to be retrained with BDT
#Data: can be used for Testting (will change places with training)




qcd = "(qgLR<0.95&&jet_QGL[2]<0.82 && jet_QGL[4]<0.56 && n_jets==7)"
#qcd = "(qgLR<0.95&&jet_QGL[2]<0.82 && jet_QGL[4]<0.56 && jet_CSV[0]<0.9535&&jet_CSV[1]<0.9535 )"
#qcd = "(jet_QGL[2]<0.4&& jet_QGL[3]<0.5&& jet_QGL[4]<0.5&& jet_QGL[5]<0.4 && n_jets==7)"
#qcd = "(qgLR < 0.4 && jet_QGL[2]<0.52 && jet_QGL[4]<0.56 )"
#qcd = "(qgLR < 0.4 && jet_QGL[2]<0.5 && jet_QGL[4]<0.5 && jet_QGL[3]<0.99 && jet_QGL[5]<0.99)"

#
#ttbar = "(qgLR>0.9 && jet_QGL[2]>0.5&& jet_QGL[3]>0.5&& jet_QGL[4]>0.5&& jet_QGL[5]>0.5)"
ttbar = "(qgLR>0.95 && jet_QGL[2]>0.31 && jet_QGL[4]>0.4 && jet_QGL[3]>0.1 && jet_QGL[5]>0.2 && n_jets==7)"
#ttbar = "(qgLR>0.95 && jet_QGL[2]>0.31 && jet_QGL[4]>0.4 && jet_QGL[3]>0.1 && jet_QGL[5]>0.2 && jet_CSV[0]<0.9535&&jet_CSV[1]<0.9535 )"
#ttbar = "(qgLR<0.4 && jet_QGL[2]>0.4 && jet_QGL[4]>0.4 && jet_QGL[3]>0.001 && jet_QGL[5]>0.01 && jet_QGL[1]>0.001 && jet_QGL[0]>0.001)"
#ttbar = "(qgLR<0.4 && jet_QGL[3]>0.1 && jet_QGL[2]>0.52 && jet_QGL[4]>0.31)"
print 'qcd: ', qcd, ' ttbar: ',ttbar

UseMethod = ["BDTCW"]
#,"PyForest","PyDNN"
#qcd = "(BDTQGL< -0.2 && n_jets == 7)"
#ttbar = "(BDTQGL> 0.2 && n_jets == 7)"


# qcd = "(qgLR< 0.15 && n_jets == 7)"
# ttbar = "(qgLR> 0.95 && n_jets == 7)"



#qcd = "(jet_CSV[0] < 0.8484  || jet_CSV[1] < 0.8484 )"
#ttbar = "(jet_CSV[0] > 0.8484 && jet_CSV[1] > 0.8484)"
# qcd = "(qgLR<0.2)"
# ttbar = "(qgLR>0.9)"
# qcd = "(qgLR<0.4)"
# ttbar = "(qgLR>0.7)"

# qcd = '(meanDeltaRbtag < 1)'
# ttbar = '(meanDeltaRbtag > 2.0)'
# qcd = "(BDT_QCD<-0.5)"
# ttbar = "(BDT_QCD>0.35)"

qcdcut = ROOT.TCut(qcd)
restcut = ROOT.TCut(ttbar)

#file1 = ROOT.TFile('../Datasets/ttbar_MVA_CWoLa.root')
#file2 = ROOT.TFile('../Datasets/QCD_MVA_CWoLa.root')
# file1 = ROOT.TFile('../Datasets/ttbar_MVA_CWoLa_Test.root')
# file2 = ROOT.TFile('../Datasets/QCD_MVA_CWoLa_Test.root')
file1 = ROOT.TFile('../Datasets/Skimmed_Ttbar.root')
file2 = ROOT.TFile('../Datasets/Skimmed_QCD.root')
#if useData or useCWoLa: file2 = ROOT.TFile('../Datasets/Skimmed_Data.root')
if useData or useCWoLa:
    # file1 = ROOT.TFile('../Datasets/ttbar_MVA_Misc.root')
    # file2 = ROOT.TFile('../Datasets/data_MVA_Misc.root')
    file1 = ROOT.TFile('../Datasets/Skimmed_Ttbar.root')
    file2 = ROOT.TFile('../Datasets/Skimmed_Data.root')

tree_s = file1.Get("tree")
tree_b = file2.Get('tree')

fname = "MVA_QCD"
if isTest: fname += '_Test'
if useData:fname+='_Data'
if isCut: fname+='_Cut'
if useCWoLa:fname+=cwolaname
if runSimpleGridSearch:
    fname+= "GRID_"


fout = ROOT.TFile('MVA_root/'+fname+".root","RECREATE")

# define factory with options
analysistype = 'AnalysisType=Classification'
factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=I",
                                          analysistype]
                                     ))

# add discriminating variables for training
#first 2 are going to be the b's


dataset = ROOT.TMVA.DataLoader('MVA_weights')


# vless = ['existCorrect','chi2Correct','addJet_DeepcMVA','isPerfect','addJet_deltaPhi','n_addbjets','weight','hasbCorrect','jet_MOverPt', 'jet_CSV', 'has4light', 'jet_DeepcMVA', 'BDT_ClassMajo','b2_csv','ttCls', 'deltaTopMgen', 'BDT_ttbarMax','addJet_cMVA','jet_cMVA', 'BDT_QCDCWoLa29', 'BDT_QCDCWoLa25','n_sumIDtop', 'BDT_QCDCWoLa19', 'addJet_DeepCSV','addJet_mass','addJet_QGL', 'n_topjets', 'addJet_phi','BDT_ttcc', 'addJet_CSV', 'n_addJets','isCorrect', 'b1_csv', 'addJet_deltaR','BDT_ttbarMajo', 'jet_QGL','addJet_eta', 'hasCorrect', 'BDT_ttlf', 'addJet_pt', 'jet_DeepCSV', 'BDT_ttbb', 'addJet_deltaEta','BDT_ttbar','BDT_Class','deltaWMgen','jets_dRmin','BDT_QCD','qgLR','BDT_QCDCWoLa2','BDT_QCDCWoLa','Fish_QCDCWoLa']
# vless+=['deltaPhit1t2','tt_eta', 'b1_eta','b2_eta', 'b1_pt', 'b2_pt','lq1_eta','lq2_eta','lp1_eta','lp2_eta','w1_eta','w2_eta','top1_eta','top2_eta', 'deltaEtaaddb1', 'deltaEtaaddb2','deltaPhiaddtop1', 'deltaPhiaddtop2','deltaEtaaddtop2', 'deltaPhiq1q2', 'deltaEtaaddtop1', 'n_bjets', 'deltaPhiaddb2', 'deltaPhiaddb1','deltaEtaw1w2', 'deltaRb1top2','deltaEtaaddw2', 'deltaEtaaddw1','deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2','memttbb', 'deltaRaddw2', 'deltaRaddw1', 'deltaPhib1b2','deltaEtab1b2','deltaPhiw1w2', 'girth','deltaRaddb1','jets_dRmax', 'deltaEtat1t2', 'deltaRaddtop2','centrality', 'deltaRaddb2','deltaRaddtop1','btagLR4b', 'meanCSV']

# vnames = [b.GetName() for b in tree_s.GetListOfBranches()]
# for v in vless:
#     if v in vnames:
#         vnames.remove(v)
# print vnames

########################################
# All
########################################
#vnames = ['lq1_pt','lq2_pt','lp1_pt','lp2_pt','b1_pt','b2_pt', 'w1_m', 'w2_m', 'top1_m','top2_m',   'deltaRb1w2', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1',   'deltaRb2p1','deltaRb2top1', 'p1b2_mass', 'q1b1_mass', 'deltaRb1b2','meanCSVbtag','deltaRq1q2','jet_CSV[0]','jet_CSV[1]','minjetpt','sphericity','centrality','aplanarity','b2_eta', 'lp1_phi','top1_phi','top2_eta','lq1_phi','lq1_eta','tt_eta','b2_phi','top1_eta','w1_eta','tt_phi','w1_phi','lp2_phi','top2_phi','deltaPhit1t2','deltaPhiq1q2','lp1_eta','w2_eta','lq2_phi', 'b1_phi','deltaPhib1b2','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','mass','tt_pt', 'b2_m', 'lq1_m', 'w1_pt', 'w2_pt', 'w2_phi', 'btagLR3b', 'mindeltaRb1q',  'ht', 'mindeltaRb2p', 'all_mass','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]', 'b1_eta','lp2_eta', 'deltaRb1top2', 'deltaPhil1l2', 'deltaEtal1l2', 'deltaEtab1b2','jets_dRmax', 'deltaEtat1t2','meanCSV','jets_dRmin','simple_chi2','BDT_Comb']
########################################
# BEst MC discrimination
########################################
#vnames=['lq2_pt','lp1_pt','lp2_pt','b1_pt','b2_pt', 'w1_m', 'w2_m', 'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1', 'p1b2_mass', 'q1b1_mass', 'deltaRb1b2','deltaRq1q2','jet_CSV[0]','jet_CSV[1]','minjetpt','aplanarity', 'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','tt_pt', 'lq1_m', 'mindeltaRb1q',  'ht', 'mindeltaRb2p', 'all_mass','meanCSV','jets_dRmin','BDT_Comb']
########################################
# CSV + QGLR Cut
########################################
#vnames = ['lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt', 'w1_m',  'w2_m',   'top1_m',  'top2_m',   'mindeltaRb1q' ,'mindeltaRb2p', 'deltaRb1w2','jet_CSV[0]','jet_CSV[1]', 'meanCSVbtag',  'deltaRb1b2','meanDeltaRbtag','q1b1_mass']
#vnames = ['qgLR','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]']

#vnames = ['lq1_pt','lp1_pt',  'w1_pt',  'w2_pt', 'w2_phi',   'deltaRb1w2', 'meanDeltaRbtag', 'p1b2_mass',  'ht', 'deltaRb1b2', 'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]', 'b1_eta','lq2_eta','lp2_eta', 'deltaPhil1l2', 'deltaEtal1l2', 'deltaEtab1b2','jets_dRmax', 'deltaEtat1t2','meanCSV']


#,'BDT_Comb'
#to try:
# ,'lq2_phi','w1_phi '


#vnames = ['lq1_pt', 'lq2_pt', 'lp1_pt', 'lp2_pt', 'b1_pt', 'b2_pt', 'w2_m', 'top1_m', 'top2_m', 'deltaRb1w2', 'meanDeltaRbtag', 'deltaRl1l2', 'deltaRb2w1', 'deltaRb2p1', 'deltaRb2top1', 'p1b2_mass', 'q1b1_mass', 'deltaRb1b2', 'meanCSVbtag', 'jet_CSV[0]','jet_CSV[1]', 'sphericity', 'centrality', 'aplanarity', 'b2_eta', 'lp1_phi', 'top1_phi', 'top2_eta', 'lq1_phi', 'lq1_eta', 'tt_eta', 'b2_phi', 'top1_eta', 'w1_eta', 'tt_phi', 'w1_phi', 'lp2_phi', 'top2_phi', 'deltaPhit1t2', 'deltaPhiq1q2', 'lp1_eta', 'w2_eta', 'lq2_phi', 'b1_phi', 'deltaPhib1b2', 'mass', 'tt_pt', 'b2_m', 'w1_pt', 'w2_pt', 'w2_phi', 'btagLR3b', 'ht', 'mindeltaRb2p', 'all_mass', 'jet_CSV[2]', 'jet_CSV[3]', 'jet_CSV[4]', 'jet_CSV[5]', 'b1_eta', 'lp2_eta', 'deltaRb1top2', 'deltaPhil1l2', 'deltaEtal1l2', 'deltaEtab1b2', 'jets_dRmax', 'deltaEtat1t2', 'meanCSV', 'simple_chi2', 'BDT_Comb']

#, 'jet_MOverPt[0]'



##########################################################################################
#vnames=['lq1_pt','lq2_pt','lp1_pt','lp2_pt','b1_pt','b2_pt', 'w1_m', 'w2_m', 'top1_m','top2_m',   'deltaRb1w2', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1',   'deltaRb2p1','deltaRb2top1', 'p1b2_mass', 'q1b1_mass', 'deltaRb1b2','meanCSVbtag','deltaRq1q2','btagLR4b','jet_CSV[0]','jet_CSV[1]','minjetpt']
##########################################################################################

#vnames = ['lq1_pt','lp1_pt',  'w1_pt',  'w2_pt', 'w2_phi',   'deltaRb1w2', 'meanDeltaRbtag', 'p1b2_mass',  'ht', 'deltaRb1b2', 'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]', 'b1_eta','lq2_eta','lp2_eta', 'deltaPhil1l2', 'deltaEtal1l2', 'deltaEtab1b2','jets_dRmax', 'deltaEtat1t2','meanCSV']



#,'ptD','sphericity','centrality','aplanarity'
#,'b2_eta', 'lp1_phi','top1_phi','top2_eta','lq1_phi','lq1_eta','tt_eta','b2_phi','top1_eta','w1_eta','tt_phi','w1_phi','lp2_phi','top2_phi','deltaPhit1t2','deltaPhiq1q2','lp1_eta','w2_eta','lq2_phi', 'b1_phi','deltaPhib1b2',






#vnames=['lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt', 'w1_m',  'w2_m',   'top1_m',  'top2_m',   'mindeltaRb1q' ,'mindeltaRb2p', 'deltaRb1w2','jet_CSV[0]','jet_CSV[1]', 'meanCSVbtag',  'deltaRb1b2','meanDeltaRbtag','q1b1_mass','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']
#,'deltaEtab1b2', 'deltaEtat1t2', 'deltaPhil1l2','deltaPhiq1q2','deltaPhib1b2','deltaPhit1t2', 'deltaEtal1l2', 'deltaEtaq1q2','deltaEtaw1w2'
# 'w1_m', 'w2_m', 'top1_m',  'top2_m', 'meanDeltaRbtag','lq2_pt','lp2_pt',  'deltaRb2p1',
#, 'jet5pt', 'ht', 'all_mass','tt_pt','jets_dRavg'
#,'lq1_m', 'lq2_m', 'lp1_m', 'lp2_m','b1_m','b2_m'
#, 'jet5pt', 'ht', 'all_mass','tt_pt','btagLR3b','jets_dRavg',

###############################################################
#'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt', 'w1_m',  'w2_m',   'top1_m',  'top2_m',   'mindeltaRb1q' ,'mindeltaRb2p', 'deltaRb1w2','jet_CSV[0]','jet_CSV[1]', 'meanCSVbtag',  'deltaRb1b2','meanDeltaRbtag','q1b1_mass','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]'
###############################################################
# 'BDT_Comb', 'prob_chi2','jets_dRmin'

# vnames=[
#     'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRp1p2',   'deltaRb2w1',
#     'q1b2_mass', 'deltaRb1b2','jet_CSV[0]','jet_CSV[1]', 'mindeltaRb2q','simple_chi2',
#     'meanCSVbtag','centrality','jets_dRmax','jets_dRavg',
#     'deltaRb2top1','deltaRb2q1','meanCSV']
vnames=[
    'lp2_pt',
    #'lq1_pt',
    'lq2_pt',
    'b1_pt',
    'b2_pt',
    'lp1_pt',
    'w2_m',
    'w1_m',
    #'top1_m',
    'top2_m',
    'meanDeltaRbtag',
    #'deltaRp1p2',
    #'deltaRq1q2',
    #'deltaRb2w1',
    #'q1b2_mass',
    'p1b1_mass',
    'deltaRb1b2',
    'jet_CSV[0]',
    'jet_CSV[1]',
    #'mindeltaRb2q',
    #'mindeltaRb1p',
    'deltaRb2top1',
    'BDT_Comb',
    #'tt_m'
    'w1_pt',
    'w2_pt',
    #'jets_dRavg',
    # 'jet_CSV[2]',
    # 'jet_CSV[3]',
    # 'jet_CSV[4]',
    # 'jet_CSV[5]'
    ]
    # ,'deltaRb2q1', 'simple_chi2'



#'tt_m', 'deltaRb2top1', 'w1_pt','w2_pt','deltaRl1l2','jets_dRavg',  'meanDeltaRbtag',  'deltaRb2w1','p1b2_mass',
#'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',
#'q1b1_mass','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]',
########################################
# Deep + Mean b DeltaR Cut
########################################

#vnames = ['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'simple_chi2', 'btagLR3b',  'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'meanCSVbtag',  'all_mass','jet_DeepCSV[0]','jet_DeepCSV[1]','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']



########################################
# CSV + Mean b DeltaR Cut
########################################

#vnames = ['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'simple_chi2', 'btagLR3b',  'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'meanCSVbtag',  'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']







usevar = ['BDT_CWoLa','prob_chi2']
#,'simple_chi2'
#usevar = vnames
#usevar = ['qgLR','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]']
#,'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]'




#usevar = ['qgLR','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]']
#,'qgLR','prob_chi2'
#usevar = vnames
#usevar += ['jet_CSV[0]','jet_CSV[1]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','jet_DeepCSV[0]','jet_DeepCSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]']
if useData:
    #usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']
    usevar=vnames
if useCWoLa:
    #usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','closest_mass']
    usevar = vnames


#usevar = ['qgLR','top1_m','top2_m','deltaRb1b2','deltaPhiw1w2','deltaPhib1b2','simple_chi2','n_addJets','addJet_CSV[0]','addJet_pt[0]','btagLR4b','btagLR3b','prob_chi2','meanDeltaRbtag','meanCSV','meanCSVbtag','BDT_Comb','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]']







for var in usevar:
    print var
    dataset.AddVariable(var,'F' if 'n_' not in var else 'I')





addcut = 'qgLR>=0 && BDT_Comb>=-1'
if isCut: addcut += '&& n_jets>=8'
sigcut = ROOT.TCut(addcut)
ttbbcut = ROOT.TCut('ttCls>=51')
ttbarweight = 35.920026e3*831.76/76972928.0


if useData or useCWoLa:
    tree_s.Draw('n_jets>>hsigQCD',qcd+'*puweight*btagweight*topweight*trigWeight(ht,jet5pt,n_bjets)*('+addcut+')')
    tree_b.Draw('n_jets>>hbkgQCD',qcd+'*('+addcut+')')
    tree_s.Draw('n_jets>>hsigTtbar',ttbar+'*puweight*btagweight*topweight*trigWeight(ht,jet5pt,n_bjets)*('+addcut+')')
    tree_b.Draw('n_jets>>hbkgTtbar',ttbar+'*('+addcut+')')
    contQCD = ROOT.gDirectory.Get("hsigQCD").Integral()*ttbarweight
    contTtbar = ROOT.gDirectory.Get("hsigTtbar").Integral()*ttbarweight
    print 'data raw events for QCD region: ',ROOT.gDirectory.Get("hbkgQCD").Integral()
    print 'data raw events for ttbar region: ',ROOT.gDirectory.Get("hbkgTtbar").Integral()
    print 'expected contaminaton of QCD enriched region of: ',contQCD, ' events, representing: ', contQCD/ROOT.gDirectory.Get("hbkgQCD").Integral()*100, '%'

    print 'expected signal of Ttbar enriched region of: ',contTtbar, ' events, representing: ', contTtbar/ROOT.gDirectory.Get("hbkgTtbar").Integral()*100, '%'

    #a = input('hello dear human')


if runSimpleGridSearch:
    dataset.AddSignalTree(tree_b)
    dataset.AddBackgroundTree(tree_b)
    dataset.PrepareTrainingAndTestTree(sigcut +restcut,sigcut+qcdcut,
                                       ":".join(["SplitMode=Random",
                                                 "TrainTestSplit_Signal=0.8",
                                                 "TrainTestSplit_Background=0.8",
                                                 "!V"
                                       ]))


else:
    if useCWoLa:
        dataset.AddSignalTree(tree_b) #REMEMBER ME
        dataset.AddBackgroundTree(tree_b)
        dataset.PrepareTrainingAndTestTree(sigcut+restcut,sigcut +qcdcut, #REMEMBER ME
                                           ":".join(["SplitMode=Random",
                                                     "TrainTestSplit_Signal=0.8",
                                                     "TrainTestSplit_Background=0.8",
                                                     "!V"
                                           ]))


    else:
        dataset.AddSignalTree(tree_s)
        dataset.AddBackgroundTree(tree_b)
        dataset.PrepareTrainingAndTestTree(sigcut + ttbbcut if not useData else sigcut+restcut,sigcut if not useData else sigcut+restcut,
                                           ":".join(["SplitMode=Random",
                                                     #"nTrain_Signal=50000",
                                                     #"nTrain_Background=50000"
                                                     #"TrainTestSplit_Signal=0.8",
                                                     #"TrainTestSplit_Background=0.8",
                                                     "NormMode=None",
                                                     "!V"
                                           ]))

if not useCWoLa:
    dataset.SetWeightExpression('qgweight*puweight*btagweight')

if runSimpleGridSearch:
    #currently only implemented for BDT
    bestroc = 0
    hyperparam = {'nTrees':[100,850,1500],'MaxDepth':[1,6,8],'Shrinkage':[0.001,0.01,0.1],'nCuts':[20,50,100]}
    cv = ROOT.TMVA.CrossValidation(dataset)
    nmodes = 0
    for ntree in hyperparam['nTrees']:
        for ndepth in hyperparam['MaxDepth']:
            for nshrink in hyperparam['Shrinkage']:
                for nCuts in hyperparam['nCuts']:
                    optstring = ":".join(["!H","!V","nTrees="+str(ntree),"MaxDepth="+str(ndepth),"BoostType=Grad","Shrinkage="+str(nshrink),"UseBaggedBoost","BaggedSampleFraction=0.50","SeparationType=GiniIndex","nCuts="+str(nCuts),])
                    cv.BookMethod(ROOT.TMVA.Types.kBDT,"BDT"+str(nmodes),optstring)
                    nmodes+=1
    cv.Evaluate()
    res = cv.GetResults()
    for i,s in enumerate(res):
        s.Print()
        #res.Print()
        roc = s.GetROCAverage()
        if roc > bestroc:
            bestmode = i
            print i
            nCuts = i%len(hyperparam['nCuts'])
            nshrink = i/len(hyperparam['nCuts'])
            ndepth = nshrink/len(hyperparam['Shrinkage'])
            nshrink = nshrink % len(hyperparam['Shrinkage'])
            ntree = ndepth/len(hyperparam['MaxDepth'])
            ndepth = ndepth % len(hyperparam['MaxDepth'])
            bestroc = roc
            res_string = 'nTrees = ' + str(hyperparam['nTrees'][ntree]) + ", MaxDepth = " + str(hyperparam['MaxDepth'][ndepth]) + ", Schrinkage = " + str(hyperparam['Shrinkage'][nshrink]) + ", nCuts = " + str(hyperparam['nCuts'][nCuts]) + ", ROC = " + str(roc)
    print res_string


else:

    modelname = '_QCD'
    if isCut: modelname+='_Cut'
    if isTest: modelname+='_Test'
    if useData:
            modelname += '_Data'
    if useCWoLa:
            modelname += cwolaname
    print 'saving xml with sufix: ',modelname

    #if not path.isfile('models/model1add_'+bkg+'.h5'):
    PyDNN_Opt(modelname, len(usevar))

    #"BDT","PyForest,"PyDNN""

    if isCut:
        UseMethod = ["Cuts"]
    mcat = {}


    for key in UseMethod:
        factory.BookMethod(dataset,methodList[key][0], key+modelname, methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+modelname+'.h5')


    #ROOT.ROOT.EnableImplicitMT()
    # self-explaining
    #factory.OptimizeAllMethods("ROCIntegral","FitGA")
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
