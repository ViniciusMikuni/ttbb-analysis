import ROOT
from ROOT import TFile,TTree,TString
from array import array
import numpy as np

topjets = 6
maxb = 10
maxtop = 2
lumi = 35.920026
btagcsvm = 0.8484
btagcsvl = 0.5426
probcut = 1e-7
tkin =  TTree("tree","tree")
#twrong =  TTree("twrong","twrong")



class Particle:
    'Defines a particle with its properties and create a TTree branch associated'
    def __init__(self,name,tree,mc = 0):
        self.pt = array( 'f', [ 0. ] )
        self.mass = array( 'f', [ 0. ] )
        self.eta = array( 'f', [ 0. ] )
        self.phi = array( 'f', [ 0. ] )
        tree.Branch(name + '_m',self.mass,name + '_m/F')
        tree.Branch(name + '_pt',self.pt,name + '_pt/F')
        tree.Branch(name + '_phi',self.phi,name + '_phi/F')
        tree.Branch(name + '_eta',self.eta,name + '_eta/F')


    def UpdateParam(self,vec):
        self.pt[0] = vec.Pt()
        self.eta[0] = vec.Eta()
        self.phi[0] = vec.Phi()
        self.mass[0] = vec.M()

                  
def AddProcessChain(sample,t):
      if sample == 'ttbar':
            f2 = ROOT.TFile.Open('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root')
            f2.Close()
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root')
      elif sample == 'QCD':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
                    
      elif sample == 'data':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/JetHT.root')
      elif sample == 'ttW':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.root')
      elif sample == 'ttZ':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8.root')
      elif sample == 'WJ':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8.root')
      elif sample == 'ZJ':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ZJetsToQQ_HT600toInf_13TeV-madgraph.root')
      elif sample == 'tW':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root')
      elif sample == 'tbarW':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root')
      elif sample == 't':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin.root ')
      elif sample == 'tbar':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin.root')
      elif sample == 's':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8.root')
      elif sample == 'WW':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/WW_TuneCUETP8M1_13TeV-pythia8.root')
      elif sample == 'WZ':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/WZ_TuneCUETP8M1_13TeV-pythia8.root')
      elif sample == 'ZZ':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ZZ_TuneCUETP8M1_13TeV-pythia8.root')
      else: print "No sample fits the current supported ones (QCD, ttbar, data)"


maxaddjet = 10      
tt = Particle('tt',tkin)
b1 = Particle('b1',tkin)
b2 = Particle('b2',tkin)
lq1=Particle('lq1',tkin)
lq2=Particle('lq2',tkin)
lp1=Particle('lp1',tkin)
lp2=Particle('lp2',tkin)
w1 = Particle('w1',tkin)
w2 = Particle('w2',tkin)
top1 = Particle('top1',tkin)
top2 = Particle('top2',tkin)

tvars = {
    'qgLR': [1,'F'],
    'isCorrect': [1,'I'],
    'isQCD': [1,'I'],
    'hasCorrect': [1,'I'],
    'hasbCorrect': [1,'I'],
    'has4light': [1,'I'],
    'isPerfect': [1,'I'],
    'chi2Correct': [1,'I'],
    'deltaRl1l2': [1,'F'],
    'deltaRq1q2': [1,'F'],
    'deltaRb1b2': [1,'F'],
    'deltaRb1w1': [1,'F'],
    'deltaRb2w2': [1,'F'],
    'deltaEtal1l2': [1,'F'],
    'deltaEtab1b2': [1,'F'],
    'deltaEtaq1q2': [1,'F'],
    'deltaEtaw1w2': [1,'F'],
    'deltaEtat1t2': [1,'F'],
    'deltaPhil1l2': [1,'F'],
    'deltaPhiq1q2': [1,'F'],
    'deltaPhib1b2': [1,'F'],
    'deltaPhiw1w2': [1,'F'],
    'deltaPhit1t2': [1,'F'],
    'btagLR4b': [1,'F'],
    'btagLR3b': [1,'F'],
    'centrality': [1,'F'],
    'aplanarity': [1,'F'],
    'meanDeltaRbtag': [1,'F'],
    'meanCSVbtag': [1,'F'],
    'meanCSV': [1,'F'],
    'jet5pt': [1,'F'],
    'b1_csv': [1,'F'],
    'b2_csv': [1,'F'],
    'ttCls': [1,'F'],
    'n_bjets': [1,'F'],
    'n_sumIDtop':[topjets,'I'],
    'n_addbjets': [1,'I'],
    'ht': [1,'F'],
    'weight': [1 , 'F'],
    'qgWeight': [1 , 'F'],
    'btagCorr': [1 , 'F'],
    'n_jets': [1,'F'],
    'simple_chi2': [1,'F'],
    'prob_chi2': [1,'F'],
    'n_addJets': [1,'F'],
    'addJet_CSV': [maxb,'F'],
    'addJet_DeepCSV': [maxb,'F'],
    'addJet_cMVA': [maxb,'F'],
    'addJet_DeepcMVA': [maxb,'F'],
    'addJet_QGL':[maxb,'F'],
    'addJet_pt': [maxb,'F'],
    'addJet_eta': [maxb,'F'],
    'addJet_phi': [maxb,'F'],
    'addJet_deltaR': [1,'F'],
    'addJet_deltaPhi': [1,'F'],
    'addJet_deltaEta': [1,'F'],
    'addJet_mass': [1,'F'],
    'memttbb': [1,'F'],
    'q1b1_mass': [1,'F'],
    'p1b2_mass': [1,'F'],
    'deltaRb1q1': [1,'F'],
    'deltaRb2p1': [1,'F'],
    'deltaRb1top2': [1,'F'],
    'deltaRb2top1': [1,'F'],
    'deltaRb1w2': [1,'F'],
    'deltaRb2w1': [1,'F'],
    'mindeltaRb1q': [1,'F'],
    'mindeltaRb2p': [1,'F'],
    'deltaRaddb1': [1,'F'],
    'deltaRaddb2': [1,'F'],
    'deltaRaddw1': [1,'F'],
    'deltaRaddw2': [1,'F'],
    'deltaRaddtop1': [1,'F'],
    'deltaRaddtop2': [1,'F'],
    'n_topjets': [1,'I'],
    'existCorrect': [1,'I'],

    'deltaPhiaddb1': [1,'F'],
    'deltaPhiaddb2': [1,'F'],
    'deltaPhiaddw1': [1,'F'],
    'deltaPhiaddw2': [1,'F'],
    'deltaPhiaddtop1': [1,'F'],
    'deltaPhiaddtop2': [1,'F'],
    'girth': [1,'F'],
    'deltaEtaaddb1': [1,'F'],
    'deltaEtaaddb2': [1,'F'],
    'deltaEtaaddw1': [1,'F'],
    'deltaEtaaddw2': [1,'F'],
    'deltaEtaaddtop1': [1,'F'],
    'deltaEtaaddtop2': [1,'F'],
    'deltaTopMgen': [1,'F'],
    'deltaWMgen': [1,'F'],
    'jet_CSV': [6,'F'],
    'jet_MOverPt': [6,'F'],
    'jet_DeepCSV': [6,'F'],
    'jet_cMVA': [6,'F'],
    'jet_DeepcMVA': [6,'F'],
    'jet_QGL': [6,'F'],
    'all_mass':[1,'F'],
    'closest_mass':[1,'F'],
    'jets_dRavg':[1,'F'],
    'jets_dRmin':[1,'F'],
    'jets_dRmax':[1,'F'],
    'BDT_ttlf': [1,'F'],
    'BDT_ttcc': [1,'F'],
    'BDT_ttbb': [1,'F'],
    'BDT_Comb': [1,'F'],
    'BDT_Class': [3,'I'],
    'BDT_ClassMajo':[3,'I'],
    'BDT_ttbar':[1,'F'],
    'BDT_ttbarMax':[1,'F'],
    'BDT_ttbarMajo':[1,'F'],
    'BDT_QCD':[1,'F'],
    'BDT_Data':[1,'F'],
    'BDT_QCDCWoLa':[1,'F'],#qglr>0.9 && qglr<0.25
    'BDT_QCDCWoLa2':[1,'F'],#qglr>0.9 && qglr<0.25
    'Fish_QCDCWoLa':[1,'F']#qglr>0.9 && qglr<0.25
    

}

def TypeTranslate(stype):
    if stype == 'F':
        return 'f'
    if stype == 'I':
        return 'i'
    



class ManageTTree:
    'Manage TTree branches from set of tvarlist_'
    def __init__(self,tvarlist_,tree):
        self.variables={}
        for var in tvarlist_:
            self.variables[var]=array(tvarlist_[var][1].lower(),tvarlist_[var][0]*[0])
            tree.Branch(var,self.variables[var],var+'['+str(tvarlist_[var][0])+']/'+tvarlist_[var][1])

    def ZeroArray(self):
        for var in self.variables:
            for dummy in range(len(self.variables[var])):
                self.variables[var][dummy] = 0



addJet_CSV_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
addJet_QGL_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
addJet_pt_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
addJet_eta_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
addJet_phi_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
Jet_QGL_ = [array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
Jet_MOverPt_ = [array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
Jet_CSV_ = [array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]


MVA_Only = {
      'w1_m': w1.mass,
      'top2_pt': top2.pt,
      'b1_pt': b1.pt,
      'w2_pt': w2.pt,
      'tt_m': tt.mass,
      'b2_pt': b2.pt,
      'w2_m': w2.mass,
      'top1_m': top1.mass,
      'w1_pt': w1.pt,
      'tt_pt': tt.pt,
      'top1_pt':top1.pt ,
      'top2_m': top2.mass,

      'addJet_CSV[0]': addJet_CSV_[0],
      'addJet_CSV[1]':addJet_CSV_[1] ,


      'addJet_pt[1]': addJet_pt_[1],
      'addJet_pt[0]': addJet_pt_[0],
      'addJet_eta[1]': addJet_eta_[1],
      'addJet_eta[0]': addJet_eta_[0],
      'addJet_phi[1]': addJet_phi_[1],
      'addJet_phi[0]': addJet_phi_[0],

      'addJet_QGL[0]': addJet_QGL_[0],
      'addJet_QGL[1]': addJet_QGL_[1],
      'jet_CSV[0]':Jet_CSV_[0],
      'jet_CSV[1]':Jet_CSV_[1],
      'jet_CSV[2]':Jet_CSV_[2],
      'jet_CSV[3]':Jet_CSV_[3],
      'jet_CSV[4]':Jet_CSV_[4],
      'jet_CSV[5]':Jet_CSV_[5],

      'jet_MOverPt[0]':Jet_MOverPt_[0],
      'jet_MOverPt[1]':Jet_MOverPt_[1],
      'jet_MOverPt[2]':Jet_MOverPt_[2],
      'jet_MOverPt[3]':Jet_MOverPt_[3],
      'jet_MOverPt[4]':Jet_MOverPt_[4],
      'jet_MOverPt[5]':Jet_MOverPt_[5],
    
      'jet_QGL[0]':Jet_QGL_[0],
      'jet_QGL[1]':Jet_QGL_[1],
      'jet_QGL[2]':Jet_QGL_[2],
      'jet_QGL[3]':Jet_QGL_[3],
      'jet_QGL[4]':Jet_QGL_[4],
      'jet_QGL[5]':Jet_QGL_[5],
      

}
