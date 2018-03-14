#!/usr/bin/env python
 
from os import environ
environ['KERAS_BACKEND'] = 'theano'
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'
import ROOT
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam, SGD
from keras.regularizers import l2


# in order to start TMVA
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()

# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.

# open input file, get trees, create output file

file1 = ROOT.TFile('../../chi2Plots/Datasets/BDT_train.root')
#file2 = ROOT.TFile('/Users/viniciusmikuni/cernbox/CMS/ttbbAnalysis/KinFitter/test/chi2Plots/Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_Ttbar.root')
#file1 = ROOT.TFile('BDT_train.root')

tree_s = file1.Get("tsig")
#tree_k = file2.Get("tkin")
fout = ROOT.TFile("MVA_Multi_Multi.root","RECREATE")
 
# define factory with options
factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=I;D;P;G,D",
                                          "AnalysisType=Multiclass"]
                                     ))
 
# add discriminating variables for training
#first 2 are going to be the b's

dataset = ROOT.TMVA.DataLoader('DataMulti')

dataset.AddVariable('qgLR','F')
#dataset.AddVariable('b1_m','F')
#dataset.AddVariable('b1_pt','F')
#dataset.AddVariable('b1_eta','F')
#dataset.AddVariable('b1_phi','F')
#dataset.AddVariable('b2_m','F')
#dataset.AddVariable('b2_pt','F')
#dataset.AddVariable('b2_eta','F')
#dataset.AddVariable('b2_phi','F')
#dataset.AddVariable('lq1_m','F')
#dataset.AddVariable('lq1_pt','F')
#dataset.AddVariable('lq1_eta','F')
#dataset.AddVariable('lq1_phi','F')
#dataset.AddVariable('lq2_m','F')
#dataset.AddVariable('lq2_pt','F')
# dataset.AddVariable('lq2_eta','F')
# dataset.AddVariable('lq2_phi','F')
# dataset.AddVariable('lp1_m','F')
#dataset.AddVariable('lp1_pt','F')
# dataset.AddVariable('lp1_eta','F')
# dataset.AddVariable('lp1_phi','F')
# dataset.AddVariable('lp2_m','F')
#dataset.AddVariable('lp2_pt','F')
# dataset.AddVariable('lp2_eta','F')
# dataset.AddVariable('lp2_phi','F')
#dataset.AddVariable('w1_m','F')
#dataset.AddVariable('w1_pt','F')
# dataset.AddVariable('w1_eta','F')
# dataset.AddVariable('w1_phi','F')
dataset.AddVariable('w2_m - w1_m','F')
#dataset.AddVariable('w2_pt','F')
# dataset.AddVariable('w2_eta','F')
# dataset.AddVariable('w2_phi','F')
#dataset.AddVariable('top1_m','F')
dataset.AddVariable('top1_pt','F')
# dataset.AddVariable('top1_eta','F')
# dataset.AddVariable('top1_phi','F')
dataset.AddVariable('top2_m - top1_m','F')
dataset.AddVariable('top2_pt','F')
# dataset.AddVariable('top2_eta','F')
# dataset.AddVariable('top2_phi','F')
#dataset.AddVariable('b1pull_Et','F')
#dataset.AddVariable('b1pull_Eta','F')
dataset.AddVariable('b1pull_Phi','F')
#dataset.AddVariable('b2pull_Et','F')
#dataset.AddVariable('b2pull_Eta','F')
dataset.AddVariable('b2pull_Phi','F')
#dataset.AddVariable('deltaRl1l2','F')
#dataset.AddVariable('deltaRq1q2','F')
dataset.AddVariable('deltaRb1b2','F')
#dataset.AddVariable('deltaEtal1l2','F')
#dataset.AddVariable('deltaEtab1b2','F')
dataset.AddVariable('deltaPhiw1w2','F')
dataset.AddVariable('deltaPhit1t2','F')
dataset.AddVariable('deltaPhib1b2','F')
dataset.AddVariable('chi2','F')
dataset.AddVariable('b1_csv','F')
dataset.AddVariable('b2_csv','F')
#dataset.AddVariable('delta_w1M','F')
#dataset.AddVariable('delta_w2M','F')
#dataset.AddVariable('delta_t1M','F')
#dataset.AddVariable('delta_t2M','F')
#dataset.AddVariable('ht','F')
#dataset.AddVariable('simple_chi2','F')
dataset.AddVariable('wkin','F')
#dataset.AddVariable('prob_chi2','F')
#dataset.AddVariable('n_addJets','I')
dataset.AddVariable('n_addbjets','I')
dataset.AddVariable('addJet_CSV[0]','F')
dataset.AddVariable('addJet_pt[0]','F')
dataset.AddVariable('addJet_CSV[1]','F')
dataset.AddVariable('addJet_pt[1]','F')
#dataset.AddVariable('btagLR3b','F')
#dataset.AddVariable('btagLR4B','F')
dataset.AddVariable('addJet_deltaR','F')
dataset.AddVariable('addJet_deltaPhi','F')
dataset.AddVariable('memttbb','F')


#cat2b = 'w2_m-w1_m:top2_m-top1_m:b1pull_Phi:b2pull_Phi:deltaRb1b2:deltaPhiw1w2:deltaPhit1t2:deltaPhib1b2:chi2:b1_csv:b2_csv:wkin:btagLR3b'
cat1add = 'qgLR:w2_m-w1_m:top2_m-top1_m:b1pull_Phi:b2pull_Phi:deltaRb1b2:deltaPhiw1w2:deltaPhit1t2:deltaPhib1b2:chi2:b1_csv:b2_csv:wkin:addJet_CSV[0]:addJet_pt[0]:memttbb'
cat2add = 'qgLR:w2_m-w1_m:top2_m-top1_m:b1pull_Phi:b2pull_Phi:deltaRb1b2:deltaPhiw1w2:deltaPhit1t2:deltaPhib1b2:chi2:b1_csv:b2_csv:wkin:n_addbjets:addJet_CSV[0]:addJet_pt[0]:addJet_CSV[1]:addJet_pt[1]:addJet_deltaR:addJet_deltaPhi:memttbb'

sigcut = ROOT.TCut(" abs(b1pull_Phi) <= 1000 && n_addbjets > 0 &&  qgLR >= 0 && addJet_CSV > 0 &&  memttbb >= 0")
ttbbCut = ROOT.TCut("ttCls>52")
tt2bCut = ROOT.TCut("ttCls==52")
ttbCut = ROOT.TCut("ttCls==51")
ttccCut = ROOT.TCut("ttCls< 46 && ttCls > 0")
ttCut = ROOT.TCut("ttCls==0")
QCDCut = ROOT.TCut("ttCls<0")
allCut = ROOT.TCut("ttCls>=51")
tbkgCut = ROOT.TCut("ttCls<51 && ttCls >= 0")
tsigCut = ROOT.TCut("ttCls>=0")
 
#define signal and background trees
#dataset.AddSignalTree(tree_s)
#dataset.AddBackgroundTree(tree_s)
dataset.AddTree(tree_s,'ttbb',1.0,ttbbCut)
dataset.AddTree(tree_s,'tt2b',1.0,tt2bCut)
dataset.AddTree(tree_s,'ttb',1.0,ttbCut)
dataset.AddTree(tree_s,'ttcc',1.0,ttccCut)
dataset.AddTree(tree_s,'tt',1.0,ttCut)



# set options for trainings
dataset.PrepareTrainingAndTestTree(sigcut,
                                   ":".join(["SplitMode=Random",
                                             "NormMode=NumEvents",
                                             "!V"
                                             ]))



layoutString = "Layout=RELU|256,RELU|256,RELU|256,RELU|256,SIGMOID"
training0 =  "LearningRate=1e-1,Momentum=0.5,Repetitions=1,ConvergenceSteps=10,BatchSize=256,TestRepetitions=10,Regularization=L2,Multithreading=True,WeightDecay=0.001,DropConfig=0.2,DropRepetitions=1"
training1 = "LearningRate=1e-2,Momentum=0.0,Repetitions=1,ConvergenceSteps=10,BatchSize=256,TestRepetitions=7,Regularization=L2,Multithreading=True"

trainingStrategyString  = "TrainingStrategy=" 
trainingStrategyString += training0 
trainingStrategyString += training0 + "|" + training1  

nnOptions = "!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=G:WeightInitialization=XAVIERUNIFORM"
nnOptions += ":" + layoutString + ":" +  trainingStrategyString + ":Architecture=CPU"

model1ad = Sequential()
model1ad.add(Dense(256, init='glorot_uniform', activation='relu', input_dim=16))
model1ad.add(Dense(256, init='glorot_uniform', activation='relu', input_dim=16))
model1ad.add(Dense(256, init='glorot_uniform', activation='relu', input_dim=16))
model1ad.add(Dense(5, init='glorot_uniform', activation='softmax'))
model1ad.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy',])
model1ad.save('model1add.h5')
model1ad.summary()

model2ad = Sequential()
model2ad.add(Dense(256, init='glorot_uniform', activation='relu', input_dim=21))
model2ad.add(Dense(256, init='glorot_uniform', activation='relu', input_dim=21))
model2ad.add(Dense(256, init='glorot_uniform', activation='relu', input_dim=21))
model2ad.add(Dense(5, init='glorot_uniform', activation='softmax'))
model2ad.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy',])
model2ad.save('model2add.h5')
model2ad.summary()



#UseMethod = ["DNN","MLP"]
UseMethod = ["PyDNN","DNN","MLP","BDT","BDTA"]
methodList = {"BDT":[ROOT.TMVA.Types.kBDT,":".join(["!H","!V","NTrees=850","MaxDepth=4","BoostType=Grad","Shrinkage=0.10","UseBaggedBoost","BaggedSampleFraction=0.50","SeparationType=GiniIndex","nCuts=20",])], "LH":[ROOT.TMVA.Types.kLikelihood,"H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50"], "MLP": [ROOT.TMVA.Types.kMLP, "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator"], "SVM": [ROOT.TMVA.Types.kSVM,"Gamma=0.25:Tol=0.001:VarTransform=Norm"], "BDTA": [ROOT.TMVA.Types.kBDT, "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20"], "DNN": [ROOT.TMVA.Types.kDNN, nnOptions], "PyDNN":[ROOT.TMVA.Types.kPyKeras, "H:!V:VarTransform=G:NumEpochs=15:BatchSize=64"] }
mcat = {}

for key in UseMethod:
    #factory.BookMethod(dataset,methodList[key][0], key, methodList[key][1] )
    mcat[key] = factory.BookMethod(dataset,ROOT.TMVA.Types.kCategory,key + 'ttbbCat','')
#    mcat[key].AddMethod(ROOT.TCut('n_bjets == 2 && btagLR3b > 0 && btagLR4b>0'),cat2b,methodList[key][0],key + '2b',methodList[key][1])
    mcat[key].AddMethod(ROOT.TCut('n_addJets == 1'),cat1add,methodList[key][0],key + '1add',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=model1add.h5')
    mcat[key].AddMethod(ROOT.TCut('n_addJets >= 2'),cat2add,methodList[key][0],key + '2add',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=model2add.h5')


  

#factory.OptimizeAllMethods("ROCIntegral","FitGA")



# self-explaining
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
