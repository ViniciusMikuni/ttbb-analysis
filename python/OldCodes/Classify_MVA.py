#!/usr/bin/env python
import sys
from os import environ, path
environ['KERAS_BACKEND'] = 'theano'
environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'
#environ['OMP_NUM_THREAD']=12
from MVA_cfg import *
import ROOT
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, SGD
from keras.regularizers import l2


# in order to start TMVA
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()

# if len(sys.argv) > 1:
#     bkg = sys.argv[1]
# else: bkg = 'ttbar'

#print 'Trainning ttbb against ',bkg
#currently multiclass does not work for unknown reasons
runSimpleGridSearch = False
add1 = False
# open input file, get trees, create output file

#file1 = ROOT.TFile('../../chi2Plots/Datasets/Correct_NoBtag_ttbar_full.root')
file1 = ROOT.TFile('../Datasets/ttbar_MVA_Full.root')
tree_s = file1.Get('tree')
    
fname = "MVA_ttbb"
if runSimpleGridSearch:
    if add1: fname+= "CV_1add_"
    else: fname+= "CV_2add_"
    
fout = ROOT.TFile(fname+".root","RECREATE")
 
# define factory with options
analysistype = 'AnalysisType=Classification'
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


        
usevar1add = ['deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','addJet_CSV[0]','ht','btagLR4b','btagLR3b','BDT_CWoLa','BDT_Comb','BDT_FullQCD','meanCSV','meanDeltaRbtag','addJet_QGL[0]']

#,'deltaEtaaddb1','deltaEtaaddb2','deltaEtaaddw1','deltaEtaaddw2','deltaEtaaddtop1','deltaEtaaddtop2','deltaPhiaddb1','deltaPhiaddb2','deltaPhiaddw1','deltaPhiaddw2','deltaPhiaddtop1','deltaPhiaddtop2',
usevar2add = usevar1add + ['addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_mass','addJet_QGL[1]']

variableList = usevar2add + ['n_jets']

for var in variableList:
    print var
    dataset.AddVariable(var,'F' if'n_' not in var else'I')
    
cat1add = ":".join(usevar1add)
cat2add = ":".join(usevar2add)

sigcut = ROOT.TCut("addJet_CSV[0] >= 0 && addJet_CSV[1] >= 0 ")

cutList = {
    'ttbbCut':ROOT.TCut("ttCls>52"),
    'tt2bCut':ROOT.TCut("ttCls==52"),
    'ttbCut':ROOT.TCut("ttCls==51"),
    'ttccCut':ROOT.TCut("ttCls<= 46 && ttCls > 0"),
    'ttbarCut':ROOT.TCut("ttCls==0"),
    'ttbbAllCut':ROOT.TCut("ttCls>=51"),
    'ttallCut':ROOT.TCut("ttCls>=0 && ttCls <= 46")}


tbkgCut = cutList['ttallCut']
tcorrCut = ROOT.TCut('isPerfect == 1 && isCorrect')


dataset.AddSignalTree(tree_s)
dataset.AddBackgroundTree(tree_s)
dataset.PrepareTrainingAndTestTree(sigcut + cutList['ttbbAllCut'],sigcut+cutList['ttallCut'],
                                   ":".join(["SplitMode=Random",
                                             "NormMode=EqualNumEvents",
                                             "TrainTestSplit_Signal=0.8",
                                             "TrainTestSplit_Background=0.8",
                                             "!V"
                                   ]))
    
dataset.SetWeightExpression('weight')



if runSimpleGridSearch:
    #currently only implemented for BDT
    bestroc = 0
    hyperparam = {'act':['relu','elu','selu'],'neurons':[32,64,256],'optmizers':[Adam(),RMSprop()],'batchs':[64,256,1024]}
    cv = ROOT.TMVA.CrossValidation(dataset)
    nmodes = 0
    for actfun in hyperparam['act']:
        for neuron in hyperparam['neurons']:
            for optmizer in hyperparam['optmizers']:
                for nbatch in hyperparam['batchs']:
                    PyDNN_Opt(fname+str(nmodes)+'_1add'+str(), len(variableList))
                    optstring = ":".join(["H","!V","NumEpochs=20","BatchSize="+str(nbatch)])      
                    cv.BookMethod(ROOT.TMVA.Types.kPyKeras,"DNN"+str(nmodes),
                                  optstring+':FilenameModel=models/model'+fname+str(nmodes)+'_1add.h5')
                    nmodes+=1
    cv.Evaluate()
    res = cv.GetResults()
    # for i,s in enumerate(res):
    #     s.Print()
    #     #res.Print()
    #     roc = s.GetROCAverage()
    #     if roc > bestroc:
    #         bestmode = i
    #         print i
    #         nCuts = i%len(hyperparam['nCuts'])
    #         nshrink = i/len(hyperparam['nCuts'])
    #         ndepth = nshrink/len(hyperparam['Shrinkage'])
    #         nshrink = nshrink % len(hyperparam['Shrinkage'])
    #         ntree = ndepth/len(hyperparam['MaxDepth'])
    #         ndepth = ndepth % len(hyperparam['MaxDepth'])
    #         bestroc = roc
    #         res_string = 'nTrees = ' + str(hyperparam['nTrees'][ntree]) + ", MaxDepth = " + str(hyperparam['MaxDepth'][ndepth]) + ", Schrinkage = " + str(hyperparam['Shrinkage'][nshrink]) + ", nCuts = " + str(hyperparam['nCuts'][nCuts]) + ", ROC = " + str(roc)
    # print res_string


else:

#if not path.isfile('models/model1add_'+bkg+'.h5'):
#if not path.isfile('models/model2add_'+bkg+'.h5'):
  
    UseMethod = ["PyDNN","BDT"]




    PyDNN_Opt(fname+'_1add', len(usevar1add))
    PyDNN_Opt(fname+'_2add', len(usevar2add))

    mcat = {}


    for key in UseMethod:
        mcat[key] = factory.BookMethod(dataset,ROOT.TMVA.Types.kCategory,key+'Cat','')
        mcat[key].AddMethod(ROOT.TCut('n_jets == 7'),cat1add,methodList[key][0],key +'1add',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+fname+'_1add.h5')
        mcat[key].AddMethod(ROOT.TCut('n_jets >= 8'),cat2add,methodList[key][0],key +'2add',methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+fname+'_2add.h5')

        # self-explaining
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
