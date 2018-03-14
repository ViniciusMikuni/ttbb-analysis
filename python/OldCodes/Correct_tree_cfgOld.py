import ROOT
from ROOT import TFile,TTree,TString
from array import array

topjets = 6
maxb = 10
maxtop = 2
lumi = 35.920026
btagcsvm = 0.8484
btagcsvl = 0.5426
probcut = 1e-3
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
      else: print "No sample fits the current supported ones (QCD, ttbar, data)"


maxaddjet = 10      
tt = Particle('tt',tkin)
b1 = Particle('b1',tkin)
b2 = Particle('b2',tkin)
lightq1 = Particle('lq1',tkin)
lightq2 = Particle('lq2',tkin)
lightp1 = Particle('lp1',tkin)
lightp2 = Particle('lp2',tkin)
w1 = Particle('w1',tkin)
w2 = Particle('w2',tkin)
top1 = Particle('top1',tkin)
top2 = Particle('top2',tkin)

tvars = {
    'qgLR': [array('f', [ 0. ] ),1,'F'],
    'isCorrect': [array('i', [ 0 ] ),1,'I'],
    'hasCorrect': [array('i', [ 0 ] ),1,'I'],
    'isPerfect': [array('i', [ 0 ] ),1,'I'],
    'deltaRl1l2': [array('f', [ 0. ] ),1,'F'],
    'deltaRq1q2': [array('f', [ 0. ] ),1,'F'],
    'deltaRb1b2': [array('f', [ 0. ] ),1,'F'],
    'deltaRb1w1': [array('f', [ 0. ] ),1,'F'],
    'deltaRb2w2': [array('f', [ 0. ] ),1,'F'],
    'deltaEtal1l2': [array('f', [ 0. ] ),1,'F'],
    'deltaEtab1b2': [array('f', [ 0. ] ),1,'F'],
    'deltaEtaq1q2': [array('f', [ 0. ] ),1,'F'],
    'deltaEtaw1w2': [array('f', [ 0. ] ),1,'F'],
    'deltaEtat1t2': [array('f', [ 0. ] ),1,'F'],
    'deltaPhil1l2': [array('f', [ 0. ] ),1,'F'],
    'deltaPhiq1q2': [array('f', [ 0. ] ),1,'F'],
    'deltaPhib1b2': [array('f', [ 0. ] ),1,'F'],
    'deltaPhiw1w2': [array('f', [ 0. ] ),1,'F'],
    'deltaPhit1t2': [array('f', [ 0. ] ),1,'F'],
    'btagLR4b': [array('f', [ 0. ] ),1,'F'],
    'btagLR3b': [array('f', [ 0. ] ),1,'F'],
    'centrality': [array('f', [ 0. ] ),1,'F'],
    'aplanarity': [array('f', [ 0. ] ),1,'F'],
    'meanDeltaRbtag': [array('f', [ 0. ] ),1,'F'],
    'meanCSVbtag': [array('f', [ 0. ] ),1,'F'],
    'meanCSV': [array('f', [ 0. ] ),1,'F'],
    
    'b1_csv': [array('f', [ 0. ] ),1,'F'],
    'b2_csv': [array('f', [ 0. ] ),1,'F'],
    'ttCls': [array('f', [ 0. ] ),1,'F'],
    'n_bjets': [array('I', [ 0 ] ),1,'I'],
    'n_addbjets': [array('I', [ 0 ] ),1,'I'],
    'ht': [array('f', [ 0. ] ),1,'F'],
    'weight': [ array('f', [ 0. ] ) , 1 , 'F'],
    'n_jets': [array('f', [ 0 ] ),1,'F'],
    'simple_chi2': [array('f', [ 0. ] ),1,'F'],
    'prob_chi2': [array('f', [ 0. ] ),1,'F'],
    'n_addJets': [array('f', [ 0 ] ),1,'F'],
    'addJet_CSV': [array('f', maxb*[ 0. ] ),maxb,'F'],
    'addJet_QGL':[array('f', maxb*[ 0. ] ),maxb,'F'],
    'addJet_pt': [array('f', maxb*[ 0. ] ),maxb,'F'],
    'addJet_eta': [array('f', maxb*[ 0. ] ),maxb,'F'],
    'addJet_phi': [array('f', maxb*[ 0. ] ),maxb,'F'],
    'addJet_deltaR': [array('f', [ 0. ] ),1,'F'],
    'addJet_deltaPhi': [array('f', [ 0. ] ),1,'F'],
    'addJet_deltaEta': [array('f', [ 0. ] ),1,'F'],
    'addJet_mass': [array('f', [ 0. ] ),1,'F'],
    'memttbb': [array('d', [ 0. ] ),1,'F'],
    'q1b1_mass': [array('f', [ 0. ] ),1,'F'],
    'p1b2_mass': [array('f', [ 0. ] ),1,'F'],
    'deltaRb1q1': [array('f', [ 0. ] ),1,'F'],
    'deltaRb2p1': [array('f', [ 0. ] ),1,'F'],
    'deltaRb1top2': [array('f', [ 0. ] ),1,'F'],
    'deltaRb2top1': [array('f', [ 0. ] ),1,'F'],
    'deltaRb1w2': [array('f', [ 0. ] ),1,'F'],
    'deltaRb2w1': [array('f', [ 0. ] ),1,'F'],
    'mindeltaRb1q': [array('f', [ 0. ] ),1,'F'],
    'mindeltaRb2p': [array('f', [ 0. ] ),1,'F'],
    'deltaRaddb1': [array('f', [ 0. ] ),1,'F'],
    'deltaRaddb2': [array('f', [ 0. ] ),1,'F'],
    'deltaRaddw1': [array('f', [ 0. ] ),1,'F'],
    'deltaRaddw2': [array('f', [ 0. ] ),1,'F'],
    'deltaRaddtop1': [array('f', [ 0. ] ),1,'F'],
    'deltaRaddtop2': [array('f', [ 0. ] ),1,'F'],

    'deltaPhiaddb1': [array('f', [ 0. ] ),1,'F'],
    'deltaPhiaddb2': [array('f', [ 0. ] ),1,'F'],
    'deltaPhiaddw1': [array('f', [ 0. ] ),1,'F'],
    'deltaPhiaddw2': [array('f', [ 0. ] ),1,'F'],
    'deltaPhiaddtop1': [array('f', [ 0. ] ),1,'F'],
    'deltaPhiaddtop2': [array('f', [ 0. ] ),1,'F'],

    'deltaEtaaddb1': [array('f', [ 0. ] ),1,'F'],
    'deltaEtaaddb2': [array('f', [ 0. ] ),1,'F'],
    'deltaEtaaddw1': [array('f', [ 0. ] ),1,'F'],
    'deltaEtaaddw2': [array('f', [ 0. ] ),1,'F'],
    'deltaEtaaddtop1': [array('f', [ 0. ] ),1,'F'],
    'deltaEtaaddtop2': [array('f', [ 0. ] ),1,'F'],
    'deltaTopMgen': [array('f', [ 0. ] ),1,'F'],
    'deltaWMgen': [array('f', [ 0. ] ),1,'F'],
    'jet_CSV': [array('f', 6*[ 0. ] ),6,'F'],
    'jet_QGL': [array('f', 6*[ 0. ] ),6,'F'],
    'BDT_ttlf': [array('f', [ 0. ] ),1,'F'],
    'BDT_ttcc': [array('f', [ 0. ] ),1,'F'],
    'BDT_ttbb': [array('f', [ 0. ] ),1,'F'],

}
class ManageTTree:
    'Manage TTree branches from set of tvarlist_'
    def __init__(self,tvarlist_,tree):
        for var in tvarlist_:
            tree.Branch(var,tvarlist_[var][0],var+'['+str(tvarlist_[var][1])+']/'+tvarlist_[var][2])

    def ZeroArray(self,tvarlist_):
        for var in tvarlist_:
            if len(tvarlist_[var])>1:
                for dummy in range(tvarlist_[var][1]):
                    tvarlist_[var][0][dummy] = 0
            else:
                tvarlist_[var][0] = 0



addJet_CSV_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
addJet_QGL_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
addJet_pt_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
addJet_eta_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
addJet_phi_ =  [array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
Jet_QGL_ = [array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] ),array( 'f', [ 0. ] )]
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
      'jet_QGL[0]':Jet_QGL_[0],
      'jet_QGL[1]':Jet_QGL_[1],
      'jet_QGL[2]':Jet_QGL_[2],
      'jet_QGL[3]':Jet_QGL_[3],
      'jet_QGL[4]':Jet_QGL_[4],
      'jet_QGL[5]':Jet_QGL_[5],
      

}
