import sys
from os import environ, path
import re
import numpy as np
environ['KERAS_BACKEND'] = 'theano'
#environ['THEANO_FLAGS'] = 'gcc.cxxflags=-march=corei7'
from Plotting_cfg import processfiles
import ROOT
from array import array
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, SGD
from keras.regularizers import l2
import json
nmax = 10000
# in order to start TMVA
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()
#ROOT.ROOT.EnableImplicitMT()


class ManageTTree:
    def __init__(self,tree,varlist,newvars,savename):
        self.vardict = {}
        self.newvars = {}
        self.branches = {}
        self.jetCSV = [array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.])]
        self.jetDeepCSV = [array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.])]
        self.addCSV = [array('f',[0.]),array('f',[0.])]
        self.addQGL = [array('f',[0.]),array('f',[0.])]
        self.addpt = [array('f',[0.]),array('f',[0.])]
        self.jetQGL = [array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.])]
        self.jetMOverPt = [array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.]),array('f',[0.])]

        for var in varlist:

            if 'jet_DeepCSV[' in var:

                self.vardict['jet_DeepCSV'] = array('f',6*[0])
                tree.SetBranchAddress('jet_DeepCSV',self.vardict['jet_DeepCSV'])

            elif 'addJet_CSV[' in var:

                self.vardict['addJet_CSV'] = array('f',2*[0])
                tree.SetBranchAddress('addJet_CSV',self.vardict['addJet_CSV'])
            elif 'addJet_pt[' in var:

                self.vardict['addJet_pt'] = array('f',2*[0])
                tree.SetBranchAddress('addJet_pt',self.vardict['addJet_pt'])

            elif 'addJet_QGL[' in var:

                self.vardict['addJet_QGL'] = array('f',2*[0])
                tree.SetBranchAddress('addJet_QGL',self.vardict['addJet_QGL'])


            elif 'jet_CSV[' in var:
                self.vardict['jet_CSV'] = array('f',6*[0])
                tree.SetBranchAddress('jet_CSV',self.vardict['jet_CSV'])

            elif 'MOverPt[' in var:

                self.vardict['jet_MOverPt'] = array('f',6*[0])
                tree.SetBranchAddress('jet_MOverPt',self.vardict['jet_MOverPt'])

            elif 'jet_QGL[' in var:

                self.vardict['jet_QGL'] = array('f',6*[0])
                tree.SetBranchAddress('jet_QGL',self.vardict['jet_QGL'])

            else:
                self.vardict[var] = array('f',[0.0])

                tree.SetBranchAddress(var,self.vardict[var])
        #self.vardict['n_jets'] = array('f',[0.0])

        #tree.SetBranchAddress(var,self.vardict['n_jets'])

        self.name = savename
        self.file = ROOT.TFile('../Datasets/'+self.name+'.root','RECREATE')
        self.tree = tree.CloneTree()
        #self.tree.CopyAddresses(tree)
        #self.tree = tree.CloneTree()

        for var in newvars:
            self.newvars[var] = array('f',[-100.])
            self.branches[var]=self.tree.Branch(var,self.newvars[var], var+'/F')

    def Fill(self):
        #self.tree.Fill()
        for var in self.branches:
            self.branches[var].Fill()

    def Save(self):

        self.file.Write('',ROOT.TFile.kOverwrite)
        self.file.Close()

    def Print(self):
        print '#######################################################'
        print 'Old TTree vars: '
        print '#######################################################'
        print self.addCSV, 'addCSV'
        print self.jetCSV, 'CSV'
        print self.jetQGL, 'QGL'
        for var in self.vardict:
            print var, self.vardict[var][0]
        print '#######################################################'
        print 'new TTree vars: '
        print '#######################################################'
        for var in self.newvars:
            print var,self.newvars[var][0]

    def __del__(self):
        del self.vardict
        del self.name
        del self.tree
        del self.branches
        del self.newvars
        del self.file

#'ttZ',


if len(sys.argv) > 2:
    mode = int(sys.argv[1])
    isTest = int(sys.argv[2])
else: print 'Missing arguments'

fname = ''
addCWoLa = addMulti = addMisc = addToy = False
if mode == 0:
    addCWoLa = True
    fname += '_CWoLa'
    print 'mode: CWoLa'
    newvars = {
        # "PyDNN_CWoLa": {
	#     "weight":"MVA_weights/weights/TMVAClassification_PyDNN_QCD_CWoLa.weights.xml",
	#     "variables":['lq2_pt','lp1_pt','lp2_pt','b1_pt', 'w2_m', 'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1', 'p1b2_mass', 'deltaRb1b2','jet_CSV[0]','jet_CSV[1]', 'mindeltaRb2p','BDT_Comb','simple_chi2', 'deltaRb2top1','deltaRb2p1','b2_eta','deltaPhiq1q2']
        # },

        "BDT_CWoLa_Sec": {
	   "weight":"MVA_weights/weights/TMVAClassification_BDTCW_QCD_Test_CWoLa.weights.xml",

	   # "variables":['top1_m','top2_m', 'meanDeltaRbtag',   'deltaRp1p2',   'deltaRb2w1',
       # 'q1b2_mass', 'deltaRb1b2','jet_CSV[0]','jet_CSV[1]', 'mindeltaRb2q','simple_chi2',
       # 'meanCSVbtag','centrality','aplanarity','jets_dRmax','jets_dRavg',
       # 'deltaRb2top1','deltaRb2q1','meanCSV']
       "variables":[
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
       #'tt_m,
       'w1_pt',
       'w2_pt',
       #'jets_dRavg',
       # 'jet_CSV[2]',
       # 'jet_CSV[3]',
       # 'jet_CSV[4]',
       # 'jet_CSV[5]',
       ]
        },
        #"BDTFish_CWoLa": {
	#     "weight":"MVA_weights/weights/TMVAClassification_BDTFish_QCD_CWoLa.weights.xml",
	#     "variables":['lq2_pt','lp1_pt','lp2_pt','b1_pt', 'w2_m', 'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1', 'p1b2_mass', 'deltaRb1b2','jet_CSV[0]','jet_CSV[1]', 'mindeltaRb2p','BDT_Comb','simple_chi2', 'deltaRb2top1','deltaRb2p1','b2_eta','deltaPhiq1q2']
        # },
        # "PyForest_CWoLa": {
	#     "weight":"MVA_weights/weights/TMVAClassification_PyForest_QCD_Test_CWoLa.weights.xml",
	#     "variables":['lq2_pt','lp1_pt','lp2_pt','b1_pt', 'w2_m', 'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1', 'p1b2_mass', 'deltaRb1b2','jet_CSV[0]','jet_CSV[1]', 'mindeltaRb2p','BDT_Comb','simple_chi2', 'deltaRb2top1','deltaRb2p1','b2_eta','deltaPhiq1q2']
        # }
    }
elif mode == 1:
    addMulti = True
    fname += '_Multi'
    print 'mode: Multi'

    newvars = {
        "BDT_ttbb_All": {

            "weight":"MVA_weights/weights/TMVAClassification_BDT_Multi_n_jets>=7.weights.xml",
            "variables":[  "b2_phi",   "lq1_phi",    "lq2_phi",    "top1_m",  "top2_phi",  "deltaPhiaddtop2", "deltaRaddb1", "deltaRaddb2",  "btagLR4b",   "btagLR3b",    "deltaRb2p1",  "p1b2_mass",  "deltaPhil1l2",  "q1b1_mass",   "ht", "deltaPhib1b2", "jets_dRavg","jets_dRmin",  "meanCSV", "deltaRb1b2",  "mindeltaRb2p", "meanCSVbtag",  "addJet_CSV[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]"]
        },

        "BDT_ttbb3b": {

            "weight":"MVA_weights/weights/TMVAClassification_BDT_Multi_3b.weights.xml",
            "variables":[ "b2_phi",   "lq1_phi",    "lq2_phi",    "top1_m",  "top2_phi",  "deltaPhiaddtop2", "deltaRaddb1", "deltaRaddb2",  "btagLR4b",   "btagLR3b",    "deltaRb2p1",  "p1b2_mass",  "deltaPhil1l2",  "q1b1_mass",   "ht", "deltaPhib1b2", "jets_dRavg","jets_dRmin",  "meanCSV", "deltaRb1b2",  "mindeltaRb2p", "meanCSVbtag",  "addJet_CSV[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]","addJet_CSV[1]","addJet_pt[1]"]
        },
        "PyDNN_ttbb3b": {

            "weight":"MVA_weights/weights/TMVAClassification_PyDNN_Multi_3b.weights.xml",
            "variables":[ "b2_phi",   "lq1_phi",    "lq2_phi",    "top1_m",  "top2_phi",  "deltaPhiaddtop2", "deltaRaddb1", "deltaRaddb2",  "btagLR4b",   "btagLR3b",    "deltaRb2p1",  "p1b2_mass",  "deltaPhil1l2",  "q1b1_mass",   "ht", "deltaPhib1b2", "jets_dRavg","jets_dRmin",  "meanCSV", "deltaRb1b2",  "mindeltaRb2p", "meanCSVbtag",  "addJet_CSV[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]","addJet_CSV[1]","addJet_pt[1]"]
        },
        "BDT_ttbb7j": {

            "weight":"MVA_weights/weights/TMVAClassification_BDT_Multi_7j.weights.xml",
            "variables":[ "b2_phi",   "lq1_phi",    "lq2_phi",    "top1_m",  "top2_phi",  "deltaPhiaddtop2", "deltaRaddb1", "deltaRaddb2",  "btagLR4b",   "btagLR3b",    "deltaRb2p1",  "p1b2_mass",  "deltaPhil1l2",  "q1b1_mass",   "ht", "deltaPhib1b2", "jets_dRavg","jets_dRmin",  "meanCSV", "deltaRb1b2",  "mindeltaRb2p", "meanCSVbtag",  "addJet_CSV[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]","n_bjets","addJet_CSV[1]","addJet_pt[1]"]
        },
        "PyDNN_ttbb7j":{

            "weight": "MVA_weights/weights/TMVAClassification_PyDNN_Multi_7j.weights.xml",
            "variables": [ "b2_phi",   "lq1_phi",    "lq2_phi",    "top1_m",  "top2_phi",  "deltaPhiaddtop2", "deltaRaddb1", "deltaRaddb2",  "btagLR4b",   "btagLR3b",    "deltaRb2p1",  "p1b2_mass",  "deltaPhil1l2",  "q1b1_mass",   "ht", "deltaPhib1b2", "jets_dRavg","jets_dRmin",  "meanCSV", "deltaRb1b2",  "mindeltaRb2p", "meanCSVbtag",  "addJet_CSV[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]","n_bjets","addJet_CSV[1]","addJet_pt[1]"]
        },
        "BDT_ttbb8j": {

            "weight":"MVA_weights/weights/TMVAClassification_BDT_Multi_8j.weights.xml",
            "variables":[ "b2_phi",   "lq1_phi",    "lq2_phi",    "top1_m",  "top2_phi",  "deltaPhiaddtop2", "deltaRaddb1", "deltaRaddb2",  "btagLR4b",   "btagLR3b",    "deltaRb2p1",  "p1b2_mass",  "deltaPhil1l2",  "q1b1_mass",   "ht", "deltaPhib1b2", "jets_dRavg","jets_dRmin",  "meanCSV", "deltaRb1b2",  "mindeltaRb2p", "meanCSVbtag",  "addJet_CSV[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]","n_bjets","addJet_CSV[1]","addJet_pt[1]"]
        },
        "PyDNN_ttbb8j":{

            "weight": "MVA_weights/weights/TMVAClassification_PyDNN_Multi_8j.weights.xml",
            "variables": ["b2_phi",   "lq1_phi",    "lq2_phi",    "top1_m",  "top2_phi",  "deltaPhiaddtop2", "deltaRaddb1", "deltaRaddb2",  "btagLR4b",   "btagLR3b",    "deltaRb2p1",  "p1b2_mass",  "deltaPhil1l2",  "q1b1_mass",   "ht", "deltaPhib1b2", "jets_dRavg","jets_dRmin",  "meanCSV", "deltaRb1b2",  "mindeltaRb2p", "meanCSVbtag",  "addJet_CSV[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]","n_bjets","addJet_CSV[1]","addJet_pt[1]"]
        },


        "BDT_ttbb9j": {

            "weight":"MVA_weights/weights/TMVAClassification_BDT_Multi_n_jets>=9.weights.xml",
            "variables":[ "tt_pt", "tt_phi", "tt_eta",  "b1_phi", "b1_eta", "b2_phi", "b2_eta",   "lq1_phi",    "lq2_phi",    "lp1_phi",    "lp2_phi",  "w1_m",    "w2_m",    "top1_m", "top1_pt", "top1_phi",  "top2_m", "top2_pt", "top2_phi",  "deltaRb1w1", "deltaRb1w2",  "deltaPhiaddw1", "deltaPhiaddw2", "meanDeltaRbtag", "prob_chi2", "BDT_Comb", "deltaPhiaddtop1", "deltaPhiaddtop2",   "deltaPhiq1q2",  "deltaPhiaddb2", "deltaPhiaddb1", "deltaRaddb1", "deltaRaddb2", "deltaPhit1t2", "deltaRb1q1", "deltaRl1l2", "btagLR4b", "deltaRb2w2", "deltaRb2w1",  "btagLR3b", "deltaEtaw1w2", "deltaRb1top2", "mindeltaRb1q",   "deltaRb2p1", "deltaRb2top1", "aplanarity", "p1b2_mass", "centrality", "deltaEtaq1q2", "deltaPhil1l2", "deltaEtal1l2", "q1b1_mass", "deltaRaddtop2", "deltaRaddtop1", "ht", "deltaPhiw1w2",  "closest_mass",  "deltaPhib1b2", "jets_dRavg","jets_dRmin", "deltaEtab1b2", "meanCSV", "deltaRb1b2", "deltaRaddw2", "deltaRaddw1", "mindeltaRb2p", "meanCSVbtag", "jets_dRmax", "deltaEtat1t2", "deltaRq1q2",  "BDT_CWoLa","addJet_CSV[0]","addJet_pt[0]","jet_QGL[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[1]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]","jet_MOverPt[0]","jet_MOverPt[1]","jet_MOverPt[2]","jet_MOverPt[3]","jet_MOverPt[4]","jet_MOverPt[5]","addJet_QGL[0]","addJet_deltaR","addJet_deltaPhi","addJet_deltaEta","addJet_CSV[1]","addJet_pt[1]","addJet_mass","addJet_QGL[1]"]
        },
        "PyDNN_ttbb9j":{

            "weight": "MVA_weights/weights/TMVAClassification_PyDNN_Multi_n_jets>=9.weights.xml",
                "variables": [ "tt_pt", "tt_phi", "tt_eta",  "b1_phi", "b1_eta", "b2_phi", "b2_eta",   "lq1_phi",    "lq2_phi",    "lp1_phi",    "lp2_phi",  "w1_m",    "w2_m",    "top1_m", "top1_pt", "top1_phi",  "top2_m", "top2_pt", "top2_phi",  "deltaRb1w1", "deltaRb1w2",  "deltaPhiaddw1", "deltaPhiaddw2", "meanDeltaRbtag", "prob_chi2", "BDT_Comb", "deltaPhiaddtop1", "deltaPhiaddtop2",   "deltaPhiq1q2",  "deltaPhiaddb2", "deltaPhiaddb1", "deltaRaddb1", "deltaRaddb2", "deltaPhit1t2", "deltaRb1q1", "deltaRl1l2", "btagLR4b", "deltaRb2w2", "deltaRb2w1",  "btagLR3b", "deltaEtaw1w2", "deltaRb1top2", "mindeltaRb1q",   "deltaRb2p1", "deltaRb2top1", "aplanarity", "p1b2_mass", "centrality", "deltaEtaq1q2", "deltaPhil1l2", "deltaEtal1l2", "q1b1_mass", "deltaRaddtop2", "deltaRaddtop1", "ht", "deltaPhiw1w2",  "closest_mass",  "deltaPhib1b2", "jets_dRavg","jets_dRmin", "deltaEtab1b2", "meanCSV", "deltaRb1b2", "deltaRaddw2", "deltaRaddw1", "mindeltaRb2p", "meanCSVbtag", "jets_dRmax", "deltaEtat1t2", "deltaRq1q2",  "BDT_CWoLa","addJet_CSV[0]","addJet_pt[0]","jet_QGL[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_CSV[1]","jet_CSV[2]","jet_CSV[3]","jet_CSV[4]","jet_CSV[5]","jet_MOverPt[0]","jet_MOverPt[1]","jet_MOverPt[2]","jet_MOverPt[3]","jet_MOverPt[4]","jet_MOverPt[5]","addJet_QGL[0]","addJet_deltaR","addJet_deltaPhi","addJet_deltaEta","addJet_CSV[1]","addJet_pt[1]","addJet_mass","addJet_QGL[1]"]
        }


    }

elif mode == 2:
    addMisc = True
    fname += '_Misc'
    print 'mode: Misc'
    newvars = {

        "BDT_Misc": {
            "weight":"MVA_weights/weights/TMVAClassification_BDTP_comb.weights.xml",
            "variables":['top1_m','top2_m','w1_m','w2_m','deltaRl1l2','deltaRq1q2','deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhiw1w2','deltaPhit1t2','q1b1_mass','p1b2_mass','deltaRb1w2','deltaRb2w1','mindeltaRb1q','simple_chi2','mindeltaRb2p', 'deltaEtal1l2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']
        },

        # "PyDNN_Misc": {
        #     "weight":"MVA_weights/weights/TMVAClassification_PyDNN_QCD.weights.xml",
        #     "variables":["qgLR","jet_QGL[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]","jet_MOverPt[0]","jet_MOverPt[1]","jet_MOverPt[2]","jet_MOverPt[3]","jet_MOverPt[4]","jet_MOverPt[5]"]
        # },

        # "BDT_QGL": {
        #     "weight":"MVA_weights/weights/TMVAClassification_BDT_QCD_Test.weights.xml",
        #     "variables":["qgLR","jet_QGL[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]"]
        # },

        # "PyDNN_QGL": {
        #     "weight":"MVA_weights/weights/TMVAClassification_PyDNN_QCD_Test.weights.xml",
        #     "variables":["qgLR","jet_QGL[0]","jet_QGL[1]","jet_QGL[2]","jet_QGL[3]","jet_QGL[4]","jet_QGL[5]"]
        # }

    }


elif mode == 3:
    addCWoLa = True
    fname += '_CWoLa_Toy'
    print 'mode: CWoLa Toy'
    vnames = ['lq2_pt','lp1_pt','lp2_pt','b1_pt', 'w2_m', 'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1', 'p1b2_mass', 'deltaRb1b2','jet_CSV[0]','jet_CSV[1]','mindeltaRb2p','simple_chi2', 'deltaRb2top1','btagLR4b','deltaRb2p1','b2_eta','deltaPhiq1q2','BDT_Comb']
    newvars = {
        "PyDNN_CWoLa_100_0": {
	    "weight":"MVA_weights/weights/TMVAClassification_PyDNNCWoLa_ToyReg_100_0.weights.xml",
	    "variables":vnames
        },
        "BDT_CWoLa_100_0": {
	    "weight":"MVA_weights/weights/TMVAClassification_BDTCWoLa_ToyReg_100_0.weights.xml",
	    "variables":vnames
        },
        "PyDNN_CWoLa_10_20": {
	    "weight":"MVA_weights/weights/TMVAClassification_PyDNNCWoLa_ToyReg_10_20.weights.xml",
	    "variables":vnames
        },
        "BDT_CWoLa_10_20": {
	    "weight":"MVA_weights/weights/TMVAClassification_BDTCWoLa_ToyReg_10_20.weights.xml",
	    "variables":vnames
        },
        "PyDNN_CWoLa_10_40": {
	    "weight":"MVA_weights/weights/TMVAClassification_PyDNNCWoLa_ToyReg_10_40.weights.xml",
	    "variables":vnames
        },
        "BDT_CWoLa_10_40": {
	    "weight":"MVA_weights/weights/TMVAClassification_BDTCWoLa_ToyReg_10_40.weights.xml",
	    "variables":vnames
        },
        "PyDNN_CWoLa_30_40": {
	    "weight":"MVA_weights/weights/TMVAClassification_PyDNNCWoLa_ToyReg_30_40.weights.xml",
	    "variables":vnames
        },
        "BDT_CWoLa_30_40": {
	    "weight":"MVA_weights/weights/TMVAClassification_BDTCWoLa_ToyReg_30_40.weights.xml",
	    "variables":vnames
        },
        "PyDNN_CWoLa_30_60": {
	    "weight":"MVA_weights/weights/TMVAClassification_PyDNNCWoLa_ToyReg_30_60.weights.xml",
	    "variables":vnames
        },
        "BDT_CWoLa_30_60": {
	    "weight":"MVA_weights/weights/TMVAClassification_BDTCWoLa_ToyReg_30_60.weights.xml",
	    "variables":vnames
        },

    }


if isTest: fname += '_Test'

processlist = ['ttbar','data']
#'data','ttbar','QCD','ttW','ttZ','ttH','WJ','ZJ','tW','tbarW','t','tbar','s','WW','WZ','ZZ'
#,'data','QCD'
#,'data','ttW','ttZ','ttH','WJ','ZJ','tW','tbarW','t','tbar','s','WW','WZ','ZZ'


# with open(filename,'r') as jfile:
#     newvars = json.load(jfile)

#newvars ={
    #############################################################################################
    # CWoLa + Comb + prob_chi2
    #############################################################################################
    # 'BDT_FullQCD': {
    #
    #     'weight':'MVA_weights/weights/TMVAClassification_BDT_QCD.weights.xml',
    #     'variables':['BDT_Comb','BDT_CWoLa','qgLR','prob_chi2']
    # },
    # 'PyDNN_FullQCD':{
    #
    #     'weight': 'MVA_weights/weights/TMVAClassification_PyDNN_QCD.weights.xml',
    #     'variables': ['BDT_Comb','BDT_CWoLa','qgLR','prob_chi2']
    # }

    #############################################################################################
    # ttbb caretogiries
    # 0: ttbb
    # 1: tt2b
    # 2: ttb
    # 3: ttcc
    # 4: ttlf
    #############################################################################################

    #############################################################################################
    # CWoLa
    #############################################################################################

    # 'PyDNN_CWoLa3b': {
    #
    #     'weight': 'MVA_weights/weights/TMVAClassification_PyDNN_QCD_CWoLa3b.weights.xml',
    #     'variables': ['lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m',  'w2_m',   'top1_m',  'top2_m',   'mindeltaRb1q' ,'q1b1_mass','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]', 'deltaRb1w2','jet_CSV[0]','jet_CSV[1]', 'meanCSVbtag',  'deltaRb1b2']
    # },

    # 'BDT_CWoLa3b': {
    #
    #     'weight':'MVA_weights/weights/TMVAClassification_BDT_QCD_CWoLa3b.weights.xml',
    #     'variables':['lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m',  'w2_m',   'top1_m',  'top2_m',   'mindeltaRb1q' ,'q1b1_mass','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]', 'deltaRb1w2','jet_CSV[0]','jet_CSV[1]', 'meanCSVbtag',  'deltaRb1b2']
    # }

    # 'PyDNN_CWoLa_DeltaR': {
    #
    #     'weight':'MVA_weights/weights/TMVAClassification_PyDNN_QCD_CWoLa_DeltaR.weights.xml',
    #     'variables':['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'simple_chi2', 'btagLR3b',  'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'meanCSVbtag',  'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']
    # },
    # 'BDT_CWoLa_DeltaR': {
    #
    #     'weight':'MVA_weights/weights/TMVAClassification_BDT_QCD_CWoLa_DeltaR.weights.xml',
    #     'variables':['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'simple_chi2', 'btagLR3b',  'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'meanCSVbtag',  'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']
    # }
    # 'PyDNN_CWoLa_Deep': {
    #
    #     'weight':'MVA_weights/weights/TMVAClassification_PyDNN_QCD_CWoLa_Deep.weights.xml',
    #     'variables':['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_DeepCSV[0]','jet_DeepCSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']
    # },
    # 'BDT_CWoLa_Deep': {
    #
    #     'weight':'MVA_weights/weights/TMVAClassification_BDT_QCD_CWoLa_Deep.weights.xml',
    #     'variables':['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_DeepCSV[0]','jet_DeepCSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']
    #}

    #############################################################################################
    # Miscelanous
    #############################################################################################


    #}

useall = []
for var in newvars:
    for usevar in newvars[var]['variables']:
        if str(usevar) not in useall:
            useall.append(str(usevar))

print useall
watch = ROOT.TStopwatch()
for i, f in enumerate(processlist):
    print 'in process: ',f
    for var in newvars:
        newvars[var]['reader'] = ROOT.TMVA.Reader( "!Color:!Silent" )
    fi = ROOT.TFile(processfiles[f],"READ")
    fout = f+'_MVA' + fname

    print 'Saving new file', fout

    t = fi.Get('tree')
    mfiles=ManageTTree(t,useall,newvars,fout)
    isDeep = isAdCSV = isAdPt = isAdQG = isCSV = isQGL = isMov = False
    for var in newvars:
        for usevar in newvars[var]['variables']:
            if 'jet_DeepCSV[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.jetDeepCSV[int(re.search(r'\d+', usevar).group())])
                isDeep = True
            elif 'addJet_CSV[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.addCSV[int(re.search(r'\d+', usevar).group())])
                isAdCSV = True
            elif 'addJet_pt[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.addpt[int(re.search(r'\d+', usevar).group())])
                isAdPt = True
            elif 'addJet_QGL[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.addQGL[int(re.search(r'\d+', usevar).group())])
                isAdQG = True
            elif 'jet_CSV[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.jetCSV[int(re.search(r'\d+', usevar).group())])
                isCSV = True
            elif 'jet_QGL[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.jetQGL[int(re.search(r'\d+', usevar).group())])
                isQGL = True
            elif 'MOverPt[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.jetMOverPt[int(re.search(r'\d+', usevar).group())])
                isMov = True

            else:
                newvars[var]['reader'].AddVariable(usevar,mfiles.vardict[usevar])

        #newvars[var]['reader'].AddSpectator('n_jets',mfiles.vardict['n_jets'])
        newvars[var]['reader'].BookMVA(var+str(i),newvars[var]['weight'])


    for e in xrange(mfiles.tree.GetEntries()):
        if e%10000==0:print 'Entry ',e, ' all of ',mfiles.tree.GetEntries()
        mfiles.tree.GetEntry(e)
        #if t.n_bjets<3:continue
        #print 'category: ',t.ttCls
        if isAdQG or isAdPt or isAdCSV:
            for ijet in range(2):
                if isAdCSV: mfiles.addCSV[ijet][0]= mfiles.vardict['addJet_CSV'][ijet]
                if isAdPt: mfiles.addpt[ijet][0]= mfiles.vardict['addJet_pt'][ijet]
                if isAdQGL: mfiles.addQGL[ijet][0]= mfiles.vardict['addJet_QGL'][ijet]

        for ijet in range(6):

            if isCSV:mfiles.jetCSV[ijet][0]= mfiles.vardict['jet_CSV'][ijet]
            if isDeep:mfiles.jetDeepCSV[ijet][0]= mfiles.vardict['jet_DeepCSV'][ijet]
            if isQGL: mfiles.jetQGL[ijet][0]= mfiles.vardict['jet_QGL'][ijet]
            if isMov: mfiles.jetMOverPt[ijet][0]= mfiles.vardict['jet_MOverPt'][ijet]


        for var in newvars:

            if addMulti: mfiles.newvars[var][0] = np.argmax(newvars[var]['reader'].EvaluateMulticlass(var+str(i)))

            else:
                mfiles.newvars[var][0] = newvars[var]['reader'].EvaluateMVA(var+str(i))
                #print mfiles.newvars[var][0], t.BDT_Comb

        #mfiles.Print()
        mfiles.Fill()
        #if e > nmax:break

    mfiles.Save()
    watch.Print()
    del mfiles
