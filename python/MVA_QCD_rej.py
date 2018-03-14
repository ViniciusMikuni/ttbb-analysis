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
ROOT.gROOT.LoadMacro("../../chi2Plots/triggerWeightRound.h+")


#currently multiclass does not work for unknown reasons
runSimpleGridSearch = False
# open input file, get trees, create output file
useData = False
useCWoLa = True
useDeep = False
cwolaname = '_CWoLa'

qcd = "(qgLR<0.3)"
ttbar = "(qgLR>0.9)"

# qcd = '(meanDeltaRbtag < 1)'
# ttbar = '(meanDeltaRbtag > 2.0)'
# qcd = "(BDT_QCD<-0.5)"
# ttbar = "(BDT_QCD>0.35)"

qcdcut = ROOT.TCut(qcd)
restcut = ROOT.TCut(ttbar)

#file1 = ROOT.TFile('../../chi2Plots/ttbar_MVA.root')
#file2 = ROOT.TFile('../../chi2Plots/QCD_MVA.root')
file1 = ROOT.TFile('../../chi2Plots/Datasets/Skimmed_Ttbar.root')
file2 = ROOT.TFile('../../chi2Plots/Datasets/Skimmed_QCD.root')
if useData or useCWoLa: file2 = ROOT.TFile('../../chi2Plots/Datasets/Skimmed_Data.root')
tree_s = file1.Get("tree")
tree_b = file2.Get('tree')
    
fname = "MVA_QCD"
if useData:fname+='_Data'
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


dataset = ROOT.TMVA.DataLoader('../weights')


#vless = ['existCorrect','chi2Correct','addJet_DeepcMVA','isPerfect','addJet_deltaPhi','n_addbjets','weight','hasbCorrect','jet_MOverPt', 'jet_CSV', 'has4light', 'jet_DeepcMVA', 'BDT_ClassMajo','b2_csv','ttCls', 'deltaTopMgen', 'BDT_ttbarMax','addJet_cMVA','jet_cMVA', 'BDT_QCDCWoLa29', 'BDT_QCDCWoLa25','n_sumIDtop', 'BDT_QCDCWoLa19', 'addJet_DeepCSV','addJet_mass','addJet_QGL', 'n_topjets', 'addJet_phi','BDT_ttcc', 'addJet_CSV', 'n_addJets','isCorrect', 'b1_csv', 'addJet_deltaR','BDT_ttbarMajo', 'jet_QGL','addJet_eta', 'hasCorrect', 'BDT_ttlf', 'addJet_pt', 'jet_DeepCSV', 'BDT_ttbb', 'addJet_deltaEta','BDT_ttbar','BDT_Class','deltaWMgen','jets_dRmin','BDT_QCD','qgLR','BDT_QCDCWoLa2','BDT_QCDCWoLa','Fish_QCDCWoLa']
#vless+=['deltaPhit1t2','tt_eta', 'b1_eta','b2_eta', 'b1_pt', 'b2_pt','lq1_eta','lq2_eta','lp1_eta','lp2_eta','w1_eta','w2_eta','top1_eta','top2_eta', 'deltaEtaaddb1', 'deltaEtaaddb2','deltaPhiaddtop1', 'deltaPhiaddtop2','deltaEtaaddtop2', 'deltaPhiq1q2', 'deltaEtaaddtop1', 'n_bjets', 'deltaPhiaddb2', 'deltaPhiaddb1','deltaEtaw1w2', 'deltaRb1top2','deltaEtaaddw2', 'deltaEtaaddw1','deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2','memttbb', 'deltaRaddw2', 'deltaRaddw1', 'deltaPhib1b2','deltaEtab1b2','deltaPhiw1w2', 'girth','deltaRaddb1','jets_dRmax', 'deltaEtat1t2', 'deltaRaddtop2','centrality', 'deltaRaddb2','deltaRaddtop1','btagLR4b', 'meanCSV']

# vnames = [b.GetName() for b in tree_s.GetListOfBranches()]
# for v in vless:
#     if v in vnames:
#         vnames.remove(v)
#print vnames

########################################
# Deep + QGLR Cut
########################################
#vnames = ['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'deltaRb1w1', 'deltaRb1w2',  'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'deltaRb1q1', 'deltaRl1l2',  'deltaRb2w2', 'deltaRb2w1', 'simple_chi2', 'btagLR3b',  'mindeltaRb1q',  'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'deltaRb1b2', 'mindeltaRb2p', 'meanCSVbtag',  'deltaRq1q2', 'all_mass','jet_DeepCSV[0]','jet_DeepCSV[1]','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]']


########################################
# CSV + QGLR Cut
########################################
vnames = ['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'deltaRb1w1', 'deltaRb1w2',  'meanDeltaRbtag', 'prob_chi2', 'jet5pt',  'n_jets',  'deltaRb1q1', 'deltaRl1l2',  'deltaRb2w2', 'deltaRb2w1', 'btagLR3b',  'mindeltaRb1q',  'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'deltaRb1b2', 'mindeltaRb2p', 'meanCSVbtag',  'deltaRq1q2', 'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']
# 'BDT_Comb', 'prob_chi2','jets_dRmin'

########################################
# Deep + Mean b DeltaR Cut
########################################

#vnames = ['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'simple_chi2', 'btagLR3b',  'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'meanCSVbtag',  'all_mass','jet_DeepCSV[0]','jet_DeepCSV[1]','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']



########################################
# CSV + Mean b DeltaR Cut
########################################

#vnames = ['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'simple_chi2', 'btagLR3b',  'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'meanCSVbtag',  'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']


usevar = ['BDT_Comb','BDT_CWoLa','prob_chi2','qgLR']
#,'qgLR','prob_chi2'
#usevar = vnames
#usevar += ['jet_CSV[0]','jet_CSV[1]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','jet_DeepCSV[0]','jet_DeepCSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]']
if useData:
    usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass','BDT_Comb']
if useCWoLa:
    #usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','closest_mass']
    usevar = vnames

    
#usevar = ['qgLR','top1_m','top2_m','deltaRb1b2','deltaPhiw1w2','deltaPhib1b2','simple_chi2','n_addJets','addJet_CSV[0]','addJet_pt[0]','btagLR4b','btagLR3b','prob_chi2','meanDeltaRbtag','meanCSV','meanCSVbtag','BDT_Comb','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]']





if runSimpleGridSearch:
    for var in usevar:
        print var
        dataset.AddVariable(var,'F' if 'n_' not in var else 'I')

else:
    for var in usevar:
        print var
        dataset.AddVariable(var,'F' if 'n_' not in var else 'I')






sigcut = ROOT.TCut('jet_QGL[0]>=0 && jet_QGL[1]>=0 && jet_QGL[2]>=0 && jet_QGL[3]>=0 && jet_QGL[4]>=0 && jet_QGL[5]>=0 && jet_CSV[0]>=0 && jet_CSV[1]>=0 && jet_CSV[2]>=0 && jet_CSV[3]>=0 && jet_CSV[4]>=0 && jet_CSV[5]>=0')
ttbarweight = 35.920026e3*831.76/76972928.0


if useData or useCWoLa:
    tree_s.Draw('n_jets>>hsigQCD',qcd+'*weight*trigWeight(ht,jet5pt,n_bjets)')
    tree_b.Draw('n_jets>>hbkgQCD',qcd+'*weight*trigWeight(ht,jet5pt,n_bjets)')
    tree_s.Draw('n_jets>>hsigTtbar',ttbar+'*weight*trigWeight(ht,jet5pt,n_bjets)')
    tree_b.Draw('n_jets>>hbkgTtbar',ttbar+'*weight*trigWeight(ht,jet5pt,n_bjets)')
    contQCD = ROOT.gDirectory.Get("hsigQCD").Integral()*ttbarweight
    contTtbar = ROOT.gDirectory.Get("hsigTtbar").Integral()*ttbarweight
    print 'expected contaminaton of QCD enriched region of: ',contQCD, ' events, representing: ', contQCD/ROOT.gDirectory.Get("hbkgQCD").Integral()*100, '%'

    print 'expected signal of Ttbar enriched region of: ',contTtbar, ' events, representing: ', contTtbar/ROOT.gDirectory.Get("hbkgTtbar").Integral()*100, '%'

    


if runSimpleGridSearch:
    dataset.AddSignalTree(tree_s)
    dataset.AddBackgroundTree(tree_b)
    dataset.PrepareTrainingAndTestTree(sigcut +restcut,sigcut+qcdcut,
                                       ":".join(["SplitMode=Random",
                                                 "TrainTestSplit_Signal=0.8",
                                                 "TrainTestSplit_Background=0.8",
                                                 "!V"
                                       ]))


else:
    if useCWoLa:
        dataset.AddSignalTree(tree_s)
        dataset.AddBackgroundTree(tree_b)
        dataset.PrepareTrainingAndTestTree(sigcut+ restcut,sigcut +qcdcut,
                                           ":".join(["SplitMode=Random",
                                                     "TrainTestSplit_Signal=0.8",
                                                     "TrainTestSplit_Background=0.8",
                                                     "NormMode=None",
                                                     "!V"
                                           ]))


    else:        
        dataset.AddSignalTree(tree_s)
        dataset.AddBackgroundTree(tree_b)
        dataset.PrepareTrainingAndTestTree(sigcut,sigcut if useData != 1 else qcdcut,
                                           ":".join(["SplitMode=Random",
                                                     "TrainTestSplit_Signal=0.8",
                                                     "TrainTestSplit_Background=0.8",
                                                     "NormMode=None",
                                                     "!V"
                                           ]))
        
dataset.SetWeightExpression('weight')
if runSimpleGridSearch:
    #currently only implemented for BDT
    bestroc = 0
    hyperparam = {'nTrees':[100,500,850],'MaxDepth':[1,4,6],'Shrinkage':[0.05,0.1,0.5],'nCuts':[20,50,100]}
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
    if useData:
            modelname += '_Data'
    if useCWoLa:
            modelname += cwolaname

    #if not path.isfile('models/model1add_'+bkg+'.h5'):
    PyDNN_Opt(modelname, len(usevar))

    #"BDT","PyForest,"PyDNN""
    UseMethod = ["PyDNN","BDT"]
    mcat = {}


    for key in UseMethod:
        factory.BookMethod(dataset,methodList[key][0], key+modelname, methodList[key][1] if key != 'PyDNN' else methodList[key][1] + ':FilenameModel=models/model'+modelname+'.h5')


    #ROOT.ROOT.EnableImplicitMT()
    # self-explaining
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
