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

useDeep=False
print 'Trainning for correct combinations'
#currently multiclass does not work for unknown reasons
runSimpleGridSearch = False
# open input file, get trees, create output file

file1 = ROOT.TFile('../Datasets/Combination_train30.root')

tree_s = file1.Get("tree")


fname = "MVA_Comb_Less"
if useDeep:
    fname+="Deep"
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

usevar = ['lp1_eta','lp2_eta','lq1_eta','lq2_eta','b1_eta','b2_eta',
'top1_m','top2_m','w1_m','w2_m','deltaRp1p2','deltaRq1q2',
'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]',
'deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhiw1w2','deltaPhit1t2','p1b1_mass','q1b2_mass','deltaRb1w2','deltaRb2w1',
'mindeltaRb1p','simple_chi2','mindeltaRb2q', 'deltaEtap1p2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]',
'jet_CSV[5]']
#'simple_chi2'

#, 'deltaEtab1b2', 'deltaEtat1t2','deltaRb2top1','deltaRb1top2','b1_pt','b2_pt','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]', 'deltaEtaw1w2','deltaRb2p1','deltaRb1q1','mindeltaRb1q','deltaPhiw1w2',
if useDeep:
    usevar = ['top1_m','top2_m','w1_m','w2_m','b1_pt','b2_pt','deltaRl1l2','deltaRq1q2','deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhil1l2','deltaPhiq1q2','deltaPhib1b2','deltaPhiw1w2','deltaPhit1t2','q1b1_mass','p1b2_mass','deltaRb1q1','deltaRb2p1','deltaRb1top2','deltaRb2top1','deltaRb1w2','deltaRb2w1','mindeltaRb1q','prob_chi2','mindeltaRb2p', 'deltaEtal1l2', 'deltaEtaq1q2', 'deltaEtab1b2', 'deltaEtaw1w2', 'deltaEtat1t2','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_DeepCSV[0]','jet_DeepCSV[1]','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]']
#,'jet_DeepcMVA[0]','jet_DeepcMVA[1]','jet_DeepcMVA[2]','jet_DeepcMVA[3]','jet_DeepcMVA[4]','jet_DeepcMVA[5]','deltaPhil1l2','deltaPhiq1q2','deltaPhib1b2'
if runSimpleGridSearch:
    for var in usevar:
        print var
        dataset.AddVariable(var,'F' if 'n_' not in var else 'I')

else:
    for var in usevar:
        print var
        dataset.AddVariable(var,'F' if 'n_' not in var else 'I')

dataset.AddSpectator('n_jets','F')
#dataset.AddVariable('prob_chi2','F')



csvandqgl =  'jet_CSV[0]>=0 && jet_CSV[1]>=0 && jet_CSV[2]>=0 && jet_CSV[3]>=0 && jet_CSV[4]>=0 && jet_CSV[5]>=0 && deltaRp1p2>0'
#'jet_QGL[0]>=0 && jet_QGL[1]>=0 && jet_QGL[2]>=0 && jet_QGL[3]>=0 && jet_QGL[4]>=0 && jet_QGL[5]>=0 &&
if useDeep: csvandqgl = 'jet_QGL[0]>=0 && jet_QGL[1]>=0 && jet_QGL[2]>=0 && jet_QGL[3]>=0 && jet_QGL[4]>=0 && jet_QGL[5]>=0 && jet_DeepCSV[0]>=0 && jet_DeepCSV[1]>=0 && jet_DeepCSV[2]>=0 && jet_DeepCSV[3]>=0 && jet_DeepCSV[4]>=0 && jet_DeepCSV[5]>=0'
sigcut = ROOT.TCut("hasCorrect==1&&"+csvandqgl)


if runSimpleGridSearch:
    dataset.AddSignalTree(tree_s)
    dataset.AddBackgroundTree(tree_s)
    dataset.PrepareTrainingAndTestTree(sigcut ,sigcut,
                                       ":".join(["SplitMode=Random",
                                                 "NormMode=EqualNumEvents",
                                                 "!V"
                                       ]))


else:
    dataset.AddSignalTree(tree_s)
    dataset.AddBackgroundTree(tree_s)
    iscorr = ROOT.TCut('isPerfect==1')
    iswrong = ROOT.TCut('isPerfect != 1')
    dataset.PrepareTrainingAndTestTree(sigcut+ iscorr,sigcut+iswrong ,
                                       ":".join(["SplitMode=Random",
                                                 "TrainTestSplit_Signal=0.7",
                                                 "TrainTestSplit_Background=0.7",
                                                  #"nTrain_Signal=20000",
                                                  #"nTrain_Background=3e6",
                                                  #"nTest_Signal=40000",
                                                  #"nTest_Background=50000",
                                                 "NormMode=EqualNumEvents",
                                                 "V"
                                       ]))
dataset.SetWeightExpression('weight')
if runSimpleGridSearch:
    #currently only implemented for BDT
    bestroc = 0
    hyperparam = {'nTrees':[500,1000,5000],'MaxDepth':[4,6,10],'Shrinkage':[0.001,0.01,0.1],'nCuts':[50,100,1000]}
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
    layoutString = "Layout=RELU|256,RELU|256,RELU|256,RELU|256,SIGMOID"
    training0 =  "LearningRate=1e-1,Momentum=0.5,Repetitions=1,ConvergenceSteps=10,BatchSize=256,TestRepetitions=10,Regularization=L2,Multithreading=True,WeightDecay=0.001,DropConfig=0.2,DropRepetitions=1"
    training1 = "LearningRate=1e-2,Momentum=0.0,Repetitions=1,ConvergenceSteps=10,BatchSize=256,TestRepetitions=7,Regularization=L2,Multithreading=True"

    trainingStrategyString  = "TrainingStrategy="
    trainingStrategyString += training0
    trainingStrategyString += training0 + "|" + training1

    nnOptions = "!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=G:WeightInitialization=XAVIERUNIFORM"
    nnOptions += ":" + layoutString + ":" +  trainingStrategyString + ":Architecture=CPU"


    #if not path.isfile('models/model1add_'+bkg+'.h5'):
    modelname="_comb"
    if useDeep:modelname+='Deep'
    PyDNN_Opt(modelname,len(usevar))



    #"BDT","BDTA,"PyDNN""
    UseMethod = ["BDTP"]
    mcat = {}


    for key in UseMethod:
        mcat[key] = factory.BookMethod(dataset,ROOT.TMVA.Types.kCategory,key + modelname,'')
        #factory.BookMethod(dataset,methodList[key][0], key+modelname, methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+modelname+'.h5')
        # mcat[key].AddMethod(ROOT.TCut('prob_chi2 <0.01'),":".join(usevar),methodList[key][0],key+modelname+'p001',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+modelname+'.h5')
        # mcat[key].AddMethod(ROOT.TCut('prob_chi2>0.01&&prob_chi2<0.1'),":".join(usevar),methodList[key][0],key+modelname+'p01',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+modelname+'.h5')
        # mcat[key].AddMethod(ROOT.TCut('prob_chi2>0.1&&prob_chi2<0.5'),":".join(usevar),methodList[key][0],key+modelname+'p1',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+modelname+'.h5')
        # mcat[key].AddMethod(ROOT.TCut('prob_chi2>0.5'),":".join(usevar),methodList[key][0],key+modelname+'p5',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+modelname+'.h5')
        mcat[key].AddMethod(ROOT.TCut('n_jets == 7'),":".join(usevar),methodList[key][0],key+modelname+'7j',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model_'+modelname+'.h5')
        mcat[key].AddMethod(ROOT.TCut('n_jets == 8'),":".join(usevar),methodList[key][0],key+modelname+'8j',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model_'+modelname+'.h5')
        mcat[key].AddMethod(ROOT.TCut('n_jets >= 9'),":".join(usevar),methodList[key][0],key+modelname+'9j',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model_'+modelname+'.h5')

    # self-explaining
    #factory.OptimizeAllMethods("ROCIntegral","FitGA")
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
