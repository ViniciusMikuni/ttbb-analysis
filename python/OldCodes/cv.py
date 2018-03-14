#!/usr/bin/env pythonA
 
# 
# This example is basically the same as $ROOTSYS/tmva/test/TMVAClassification.C
# 
 
import ROOT
 
# in order to start TMVA
ROOT.TMVA.Tools.Instance()
 
# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.
 
# open input file, get trees, create output file
file1 = ROOT.TFile('/Users/viniciusmikuni/Dropbox/CMS/ttbbAnalysis/KinFitter/test/chi2Plots/Datasets/BDT_train.root')
tree_s = file1.Get("tsig")
tree_b = file1.Get("tbkg")
fout = ROOT.TFile("testBDT.root","RECREATE")
 
# define factory with options
# add discriminating variables for training
#first 2 are going to be the b's

dataset = ROOT.TMVA.DataLoader('Dataset')

dataset.AddVariable('qgLR3b5q','F')
dataset.AddVariable('b1_m','F')
dataset.AddVariable('b1_pt','F')
dataset.AddVariable('b1_eta','F')
dataset.AddVariable('b1_phi','F')
dataset.AddVariable('b2_m','F')
dataset.AddVariable('b2_pt','F')
dataset.AddVariable('b2_eta','F')
dataset.AddVariable('b2_phi','F')
#dataset.AddVariable('lq1_m','F')
dataset.AddVariable('lq1_pt','F')
#dataset.AddVariable('lq1_eta','F')
#dataset.AddVariable('lq1_phi','F')
#dataset.AddVariable('lq2_m','F')
dataset.AddVariable('lq2_pt','F')
# dataset.AddVariable('lq2_eta','F')
# dataset.AddVariable('lq2_phi','F')
# dataset.AddVariable('lp1_m','F')
dataset.AddVariable('lp1_pt','F')
# dataset.AddVariable('lp1_eta','F')
# dataset.AddVariable('lp1_phi','F')
# dataset.AddVariable('lp2_m','F')
dataset.AddVariable('lp2_pt','F')
# dataset.AddVariable('lp2_eta','F')
# dataset.AddVariable('lp2_phi','F')
dataset.AddVariable('w1_m','F')
dataset.AddVariable('w1_pt','F')
# dataset.AddVariable('w1_eta','F')
# dataset.AddVariable('w1_phi','F')
dataset.AddVariable('w2_m','F')
dataset.AddVariable('w2_pt','F')
# dataset.AddVariable('w2_eta','F')

# dataset.AddVariable('w2_phi','F')
dataset.AddVariable('top1_m','F')
dataset.AddVariable('top1_pt','F')
# dataset.AddVariable('top1_eta','F')
# dataset.AddVariable('top1_phi','F')
dataset.AddVariable('top2_m','F')
dataset.AddVariable('top2_pt','F')
# dataset.AddVariable('top2_eta','F')
# dataset.AddVariable('top2_phi','F')
dataset.AddVariable('b1pull[0]','F')
dataset.AddVariable('b1pull[1]','F')
dataset.AddVariable('b1pull[2]','F')
dataset.AddVariable('b2pull[0]','F')
dataset.AddVariable('b2pull[1]','F')
dataset.AddVariable('b2pull[2]','F')
dataset.AddVariable('deltaRl1l2','F')
dataset.AddVariable('deltaRq1q2','F')
dataset.AddVariable('deltaRb1b2','F')
#dataset.AddVariable('deltaEtal1l2','F')
#dataset.AddVariable('deltaEtab1b2','F')
dataset.AddVariable('deltaPhil1l2','F')
dataset.AddVariable('deltaPhiq1q2','F')
dataset.AddVariable('deltaPhib1b2','F')
dataset.AddVariable('chi2','F')
dataset.AddVariable('b_csv[0]','F')
dataset.AddVariable('b_csv[1]','F')
dataset.AddVariable('delta_w1M','F')
dataset.AddVariable('delta_w2M','F')
dataset.AddVariable('delta_t1M','F')
dataset.AddVariable('delta_t2M','F')
#dataset.AddVariable('ht','F')
#dataset.AddVariable('weight','F')
dataset.AddVariable('wkin','F')
dataset.AddVariable('prob_chi2','F')



 
# define signal and background trees
dataset.AddSignalTree(tree_s)
dataset.AddBackgroundTree(tree_b)
 
# define additional cuts 
sigCut = ROOT.TCut("isCorrect == 1 && abs(b1pull[2]) <= 1000 && abs(b2pull[2]) <= 1000")
bgCut = ROOT.TCut("abs( b1pull[2]) <= 1e7 && abs( b2pull[2]) <= 1e7")
 
# set options for trainings
dataset.PrepareTrainingAndTestTree(sigCut, 
                                   bgCut, 
                                   ":".join(["SplitMode=Random",
                                             "NormMode=NumEvents",
                                             "!V"
                                             ]))
optionsString = ""
secoptionsString = ""
hyper = ROOT.TMVA.HyperParameterOptimisation(dataset)
hyper.BookMethod(ROOT.TMVA.Types.kBDT, "BDT")
hyper.SetNumFolds(3)
hyper.Evaluate()
hresult = hyper.GetResults()

for opt in  hresult.fFoldParameters.at(0):
    optionsString += ":";
    optionsString += str(opt.first);
    optionsString += "=";
    optionsString += str(opt.second);
print optionsString


for opt in  hresult.fFoldParameters.at(0):
    secoptionsString += ":";
    secoptionsString += str(opt[0]);
    secoptionsString += "=";
    secoptionsString += str(opt[1]);
print optionsString

