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

nmax = 100
# in order to start TMVA
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()

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
                if '[0]' in var:
                    self.vardict['jet_DeepCSV'] = array('f',6*[0])
                    tree.SetBranchAddress('jet_DeepCSV',self.vardict['jet_DeepCSV'])

            elif 'addJet_CSV[' in var:
                if '[0]' in var:
                    self.vardict['addJet_CSV'] = array('f',2*[0])
                    tree.SetBranchAddress('addJet_CSV',self.vardict['addJet_CSV'])
            elif 'addJet_pt[' in var:
                if '[0]' in var:
                    self.vardict['addJet_pt'] = array('f',2*[0])
                    tree.SetBranchAddress('addJet_pt',self.vardict['addJet_pt'])
                    
            elif 'addJet_QGL[' in var:
                if '[0]' in var:
                    self.vardict['addJet_QGL'] = array('f',2*[0])
                    tree.SetBranchAddress('addJet_QGL',self.vardict['addJet_QGL'])

            
            elif 'jet_CSV[' in var:
                if '[1]' in var:
                    self.vardict['jet_CSV'] = array('f',6*[0])
                    tree.SetBranchAddress('jet_CSV',self.vardict['jet_CSV'])

            elif 'MOverPt[' in var:
                if '[0]' in var:
                    self.vardict['jet_MOverPt'] = array('f',6*[0])
                    tree.SetBranchAddress('jet_MOverPt',self.vardict['jet_MOverPt'])

            elif 'jet_QGL[' in var:
                if '[0]' in var:
                    self.vardict['jet_QGL'] = array('f',6*[0])
                    tree.SetBranchAddress('jet_QGL',self.vardict['jet_QGL'])

            else:
                self.vardict[var] = array('f',[0.0]) 
                
                tree.SetBranchAddress(var,self.vardict[var])

        
        self.name = savename
        self.file = ROOT.TFile('../Datasets/'+self.name+'.root','RECREATE')
        self.tree = tree.CloneTree()

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
        print self.addCSV, 'CSV'
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
processlist = ['ttbar']
#,'ttbar','QCD','ttW','ttZ','WJ','ZJ','tW','tbarW','t','tbar','s','WW','WZ','ZZ'
#,'data','QCD'

newvars ={
    #############################################################################################
    # CWoLa + Comb + prob_chi2
    #############################################################################################
    # 'BDT_FullQCD': { 
    #     'reader': ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_BDT_QCD.weights.xml',
    #     'variables':['BDT_Comb','BDT_CWoLa','qgLR','prob_chi2']
    # },
    # 'PyDNN_FullQCD':{
    #     'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight': '../weights/weights/TMVAClassification_PyDNN_QCD.weights.xml',
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
    # 'BDT_ttbb_All': { 
    #     'reader': ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_BDT_Multi_n_jets>=7.weights.xml',
    #     'variables':[ 'tt_pt', 'tt_phi', 'tt_eta',  'b1_phi', 'b1_eta', 'b2_phi', 'b2_eta',   'lq1_phi',    'lq2_phi',    'lp1_phi',    'lp2_phi',  'w1_m',    'w2_m',    'top1_m', 'top1_pt', 'top1_phi',  'top2_m', 'top2_pt', 'top2_phi',  'deltaRb1w1', 'deltaRb1w2',  'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'deltaPhiaddtop1', 'deltaPhiaddtop2',   'deltaPhiq1q2',  'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1',  'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q',   'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass',  'deltaPhib1b2', 'jets_dRavg','jets_dRmin', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2',  'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','addJet_QGL[0]','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass','addJet_QGL[1]']
    # },
    # 'BDT_ttbb3b': { 
    #     'reader': ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_BDT_Multi_n_bjets>=3.weights.xml',
    #     'variables':[ 'tt_pt', 'tt_phi', 'tt_eta',  'b1_phi', 'b1_eta', 'b2_phi', 'b2_eta',   'lq1_phi',    'lq2_phi',    'lp1_phi',    'lp2_phi',  'w1_m',    'w2_m',    'top1_m', 'top1_pt', 'top1_phi',  'top2_m', 'top2_pt', 'top2_phi',  'deltaRb1w1', 'deltaRb1w2',  'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'deltaPhiaddtop1', 'deltaPhiaddtop2',   'deltaPhiq1q2',  'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1',  'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q',   'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass',  'deltaPhib1b2', 'jets_dRavg','jets_dRmin', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2',  'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','addJet_QGL[0]','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass','addJet_QGL[1]']
    # },
    # 'BDT_ttbb7j': { 
    #     'reader': ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_BDT_Multi_n_jets==7.weights.xml',
    #     'variables':[ 'tt_pt', 'tt_phi', 'tt_eta',  'b1_phi', 'b1_eta', 'b2_phi', 'b2_eta',   'lq1_phi',    'lq2_phi',    'lp1_phi',    'lp2_phi',  'w1_m',    'w2_m',    'top1_m', 'top1_pt', 'top1_phi',  'top2_m', 'top2_pt', 'top2_phi',  'deltaRb1w1', 'deltaRb1w2',  'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'deltaPhiaddtop1', 'deltaPhiaddtop2',   'deltaPhiq1q2',  'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1',  'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q',   'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass',  'deltaPhib1b2', 'jets_dRavg','jets_dRmin', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2',  'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','addJet_QGL[0]']
    # },
    # 'PyDNN_ttbb7j':{
    #     'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight': '../weights/weights/TMVAClassification_PyDNN_Multi_n_jets==7.weights.xml',
    #     'variables': [ 'tt_pt', 'tt_phi', 'tt_eta',  'b1_phi', 'b1_eta', 'b2_phi', 'b2_eta',   'lq1_phi',    'lq2_phi',    'lp1_phi',    'lp2_phi',  'w1_m',    'w2_m',    'top1_m', 'top1_pt', 'top1_phi',  'top2_m', 'top2_pt', 'top2_phi',  'deltaRb1w1', 'deltaRb1w2',  'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'deltaPhiaddtop1', 'deltaPhiaddtop2',   'deltaPhiq1q2',  'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1',  'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q',   'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass',  'deltaPhib1b2', 'jets_dRavg','jets_dRmin', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2',  'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','addJet_QGL[0]']
    # },
    # 'BDT_ttbb8j': { 
    #     'reader': ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_BDT_Multi_n_jets==8.weights.xml',
    #     'variables':[ 'tt_pt', 'tt_phi', 'tt_eta',  'b1_phi', 'b1_eta', 'b2_phi', 'b2_eta',   'lq1_phi',    'lq2_phi',    'lp1_phi',    'lp2_phi',  'w1_m',    'w2_m',    'top1_m', 'top1_pt', 'top1_phi',  'top2_m', 'top2_pt', 'top2_phi',  'deltaRb1w1', 'deltaRb1w2',  'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'deltaPhiaddtop1', 'deltaPhiaddtop2',   'deltaPhiq1q2',  'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1',  'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q',   'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass',  'deltaPhib1b2', 'jets_dRavg','jets_dRmin', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2',  'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','addJet_QGL[0]','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass','addJet_QGL[1]']
    # },
    # 'PyDNN_ttbb8j':{
    #     'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight': '../weights/weights/TMVAClassification_PyDNN_Multi_n_jets==8.weights.xml',
    #     'variables': [ 'tt_pt', 'tt_phi', 'tt_eta',  'b1_phi', 'b1_eta', 'b2_phi', 'b2_eta',   'lq1_phi',    'lq2_phi',    'lp1_phi',    'lp2_phi',  'w1_m',    'w2_m',    'top1_m', 'top1_pt', 'top1_phi',  'top2_m', 'top2_pt', 'top2_phi',  'deltaRb1w1', 'deltaRb1w2',  'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'deltaPhiaddtop1', 'deltaPhiaddtop2',   'deltaPhiq1q2',  'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1',  'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q',   'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass',  'deltaPhib1b2', 'jets_dRavg','jets_dRmin', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2',  'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','addJet_QGL[0]','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass','addJet_QGL[1]']
    # },
    # 'BDT_ttbb9j': { 
    #     'reader': ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_BDT_Multi_n_jets>=9.weights.xml',
    #     'variables':[ 'tt_pt', 'tt_phi', 'tt_eta',  'b1_phi', 'b1_eta', 'b2_phi', 'b2_eta',   'lq1_phi',    'lq2_phi',    'lp1_phi',    'lp2_phi',  'w1_m',    'w2_m',    'top1_m', 'top1_pt', 'top1_phi',  'top2_m', 'top2_pt', 'top2_phi',  'deltaRb1w1', 'deltaRb1w2',  'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'deltaPhiaddtop1', 'deltaPhiaddtop2',   'deltaPhiq1q2',  'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1',  'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q',   'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass',  'deltaPhib1b2', 'jets_dRavg','jets_dRmin', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2',  'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','addJet_QGL[0]','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass','addJet_QGL[1]']
    # },
    # 'PyDNN_ttbb9j':{
    #     'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight': '../weights/weights/TMVAClassification_PyDNN_Multi_n_jets>=9.weights.xml',
    #     'variables': [ 'tt_pt', 'tt_phi', 'tt_eta',  'b1_phi', 'b1_eta', 'b2_phi', 'b2_eta',   'lq1_phi',    'lq2_phi',    'lp1_phi',    'lp2_phi',  'w1_m',    'w2_m',    'top1_m', 'top1_pt', 'top1_phi',  'top2_m', 'top2_pt', 'top2_phi',  'deltaRb1w1', 'deltaRb1w2',  'deltaPhiaddw1', 'deltaPhiaddw2', 'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'deltaPhiaddtop1', 'deltaPhiaddtop2',   'deltaPhiq1q2',  'deltaPhiaddb2', 'deltaPhiaddb1', 'deltaRaddb1', 'deltaRaddb2', 'deltaPhit1t2', 'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1',  'btagLR3b', 'deltaEtaw1w2', 'deltaRb1top2', 'mindeltaRb1q',   'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality', 'deltaEtaq1q2', 'deltaPhil1l2', 'deltaEtal1l2', 'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass',  'deltaPhib1b2', 'jets_dRavg','jets_dRmin', 'deltaEtab1b2', 'meanCSV', 'deltaRb1b2', 'deltaRaddw2', 'deltaRaddw1', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2',  'BDT_CWoLa','addJet_CSV[0]','addJet_pt[0]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','addJet_QGL[0]','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass','addJet_QGL[1]']
    # }

    #############################################################################################
    # CWoLa
    #############################################################################################
    'PyDNN_CWoLa': {
        'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
        'weight': '../weights/weights/TMVAClassification_PyDNN_QCD_CWoLa.weights.xml',
        'variables': ['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'deltaRb1w1', 'deltaRb1w2',  'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'deltaRb1q1', 'deltaRl1l2',  'deltaRb2w2', 'deltaRb2w1', 'simple_chi2', 'btagLR3b',  'mindeltaRb1q',  'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg','jets_dRmin',  'deltaRb1b2', 'mindeltaRb2p', 'meanCSVbtag',  'deltaRq1q2', 'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']
    },
    
    'BDT_CWoLa': {
        'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
        'weight':'../weights/weights/TMVAClassification_BDT_QCD_CWoLa.weights.xml',
        'variables':['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'deltaRb1w1', 'deltaRb1w2',  'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'deltaRb1q1', 'deltaRl1l2',  'deltaRb2w2', 'deltaRb2w1', 'simple_chi2', 'btagLR3b',  'mindeltaRb1q',  'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg','jets_dRmin',  'deltaRb1b2', 'mindeltaRb2p', 'meanCSVbtag',  'deltaRq1q2', 'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']
    }
    
    # 'PyDNN_CWoLa_DeltaR': {
    #     'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_PyDNN_QCD_CWoLa_DeltaR.weights.xml',
    #     'variables':['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'simple_chi2', 'btagLR3b',  'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'meanCSVbtag',  'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']
    # },
    # 'BDT_CWoLa_DeltaR': {
    #     'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_BDT_QCD_CWoLa_DeltaR.weights.xml',
    #     'variables':['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_jets',  'simple_chi2', 'btagLR3b',  'aplanarity', 'p1b2_mass',   'q1b1_mass', 'ht',   'closest_mass', 'jets_dRavg',  'meanCSVbtag',  'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']
    # }
    # 'PyDNN_CWoLa_Deep': {
    #     'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_PyDNN_QCD_CWoLa_Deep.weights.xml',
    #     'variables':['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_DeepCSV[0]','jet_DeepCSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']
    # },
    # 'BDT_CWoLa_Deep': {
    #     'reader':ROOT.TMVA.Reader( "!Color:!Silent" ),
    #     'weight':'../weights/weights/TMVAClassification_BDT_QCD_CWoLa_Deep.weights.xml',
    #     'variables':['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_DeepCSV[0]','jet_DeepCSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_DeepCSV[2]','jet_DeepCSV[3]','jet_DeepCSV[4]','jet_DeepCSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']
    #}
}

useall = []
for var in newvars:
    for usevar in newvars[var]['variables']:
        if usevar not in useall:
            useall.append(usevar)

print useall
for i, f in enumerate(processlist):
    print 'in process: ',f
    for var in newvars:
        newvars[var]['reader'] = ROOT.TMVA.Reader( "!Color:!Silent" )
    fi = ROOT.TFile(processfiles[f],"READ")    
    t = fi.Get('tree')
    mfiles=ManageTTree(t,useall,newvars,f+'_MVA')
    print 'Saving new file', f+'_MVA'
    for var in newvars:
        for usevar in newvars[var]['variables']:
            if 'jet_DeepCSV[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.jetDeepCSV[int(re.search(r'\d+', usevar).group())])
            elif 'addJet_CSV[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.addCSV[int(re.search(r'\d+', usevar).group())])
            elif 'addJet_pt[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.addpt[int(re.search(r'\d+', usevar).group())])
            elif 'addJet_QGL[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.addQGL[int(re.search(r'\d+', usevar).group())])
            elif 'jet_CSV[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.jetCSV[int(re.search(r'\d+', usevar).group())])
            elif 'jet_QGL[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.jetQGL[int(re.search(r'\d+', usevar).group())])
            elif 'MOverPt[' in usevar:
                newvars[var]['reader'].AddVariable(usevar,mfiles.jetMOverPt[int(re.search(r'\d+', usevar).group())])

            else:
                newvars[var]['reader'].AddVariable(usevar,mfiles.vardict[usevar])

        
        newvars[var]['reader'].BookMVA(var+str(i),newvars[var]['weight'])

        
    for e in xrange(t.GetEntries()):
        if e%10000==0:print 'Entry ',e, ' all of ',t.GetEntries()
        t.GetEntry(e)
        #if t.n_bjets<3:continue
        #print 'category: ',t.ttCls
        # for ijet in range(2):
        #      mfiles.addCSV[ijet][0]= mfiles.vardict['addJet_CSV'][ijet]
        #      mfiles.addpt[ijet][0]= mfiles.vardict['addJet_pt'][ijet]
        #      mfiles.addQGL[ijet][0]= mfiles.vardict['addJet_QGL'][ijet]
        
        for ijet in range(6):
            mfiles.jetCSV[ijet][0]= mfiles.vardict['jet_CSV'][ijet]
            #mfiles.jetDeepCSV[ijet][0]= mfiles.vardict['jet_DeepCSV'][ijet]
            #mfiles.jetQGL[ijet][0]= mfiles.vardict['jet_QGL'][ijet]
            #mfiles.jetMOverPt[ijet][0]= mfiles.vardict['jet_MOverPt'][ijet]

        for var in newvars:
            
            #mfiles.newvars[var][0] = np.argmax(newvars[var]['reader'].EvaluateMulticlass(var+str(i)))

            mfiles.newvars[var][0] = newvars[var]['reader'].EvaluateMVA(var+str(i))
        #mfiles.Print()
        mfiles.Fill()
        #if e > nmax:break
            
    mfiles.Save()
    #del mfiles
        
        
        
    


    
