import ROOT
from ROOT import TFile,TTree,TString
from array import array

topjets = 6
maxb = 10
maxtop = 2
lumi = 35.920026
btagcsvm = 0.8484
btagcsvl = 0.5426
tsig =  TTree("tsig","tsig")



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


      

qgLR = array( 'f', [ 0. ] )
tsig.Branch('qgLR',qgLR,'qgLR/F')
tt = Particle('tt',tsig)
isCorrect = array( 'i', [ 0 ] )
tsig.Branch('isCorrect',isCorrect,'isCorrect/I')
b1 = Particle('b1',tsig)
b2 = Particle('b2',tsig)
b1pull_Et = array( 'f', [ 0. ] )
tsig.Branch('b1pull_Et',b1pull_Et,'b1pull_Et/F')
b1pull_Eta = array( 'f', [ 0. ] )
tsig.Branch('b1pull_Eta',b1pull_Eta,'b1pull_Eta/F')
b1pull_Phi = array( 'f', [ 0. ] )
tsig.Branch('b1pull_Phi',b1pull_Phi,'b1pull_Phi/F')
b2pull_Et = array( 'f', [ 0. ] )
tsig.Branch('b2pull_Et',b2pull_Et,'b2pull_Et/F')
b2pull_Eta = array( 'f', [ 0. ] )
tsig.Branch('b2pull_Eta',b2pull_Eta,'b2pull_Eta/F')
b2pull_Phi = array( 'f', [ 0. ] )
tsig.Branch('b2pull_Phi',b2pull_Phi,'b2pull_Phi/F')
lightq1 = Particle('lq1',tsig)
lightq2 = Particle('lq2',tsig)
lightp1 = Particle('lp1',tsig)
lightp2 = Particle('lp2',tsig)
deltaRl1l2 = array( 'f', [ 0. ] )
tsig.Branch('deltaRl1l2',deltaRl1l2,'deltaRl1l2/F')
deltaRq1q2 = array( 'f', [ 0. ] )
tsig.Branch('deltaRq1q2',deltaRq1q2,'deltaRq1q2/F')
deltaRb1b2 = array( 'f', [ 0. ] )
tsig.Branch('deltaRb1b2',deltaRb1b2,'deltaRb1b2/F')
deltaEtal1l2 = array( 'f', [ 0. ] )
tsig.Branch('deltaEtal1l2',deltaEtal1l2,'deltaEtal1l2/F')
deltaEtab1b2 = array( 'f', [ 0. ] )
tsig.Branch('deltaEtab1b2',deltaEtab1b2,'deltaEtab1b2/F')
deltaEtaq1q2 = array( 'f', [ 0. ] )
tsig.Branch('deltaEtaq1q2',deltaEtaq1q2,'deltaEtaq1q2/F')
deltaPhil1l2 = array( 'f', [ 0. ] )
tsig.Branch('deltaPhil1l2',deltaPhil1l2,'deltaPhil1l2/F')
deltaPhiq1q2 = array( 'f', [ 0. ] )
tsig.Branch('deltaPhiq1q2',deltaPhiq1q2,'deltaPhiq1q2/F')
deltaPhib1b2 = array( 'f', [ 0. ] )
tsig.Branch('deltaPhib1b2',deltaPhib1b2,'deltaPhib1b2/F')
deltaPhiw1w2 = array( 'f', [ 0. ] )
tsig.Branch('deltaPhiw1w2',deltaPhiw1w2,'deltaPhiw1w2/F')
deltaPhit1t2 = array( 'f', [ 0. ] )
tsig.Branch('deltaPhit1t2',deltaPhit1t2,'deltaPhit1t2/F')
btagLR4b = array( 'f', [ 0. ] )
tsig.Branch('btagLR4b',btagLR4b,'btagLR4b/F')
btagLR3b = array( 'f', [ 0. ] )
tsig.Branch('btagLR3b',btagLR3b,'btagLR3b/F')
centrality = array( 'f', [ 0. ] )
tsig.Branch('centrality',centrality,'centrality/F')
deltaRb1w1 = array( 'f', [ 0. ] )
tsig.Branch('deltaRb1w1',deltaRb1w1,'deltaRb1w1/F')
deltaRb2w2 = array( 'f', [ 0. ] )
tsig.Branch('deltaRb2w2',deltaRb2w2,'deltaRb2w2/F')
deltaRaddb1 = array( 'f', [ 0. ] )
tsig.Branch('deltaRaddb1',deltaRaddb1,'deltaRaddb1/F')
deltaRaddb2 = array( 'f', [ 0. ] )
tsig.Branch('deltaRaddb2',deltaRaddb2,'deltaRaddb2/F')
deltaRaddw1 = array( 'f', [ 0. ] )
tsig.Branch('deltaRaddw1',deltaRaddw1,'deltaRaddw1/F')
deltaRaddw2 = array( 'f', [ 0. ] )
tsig.Branch('deltaRaddw2',deltaRaddw2,'deltaRaddw2/F')
deltaRaddtop1 = array( 'f', [ 0. ] )
tsig.Branch('deltaRaddtop1',deltaRaddtop1,'deltaRaddtop1/F')
deltaRaddtop2 = array( 'f', [ 0. ] )
tsig.Branch('deltaRaddtop2',deltaRaddtop2,'deltaRaddtop2/F')



w1 = Particle('w1',tsig)
w2 = Particle('w2',tsig)
top1 = Particle('top1',tsig)
top2 = Particle('top2',tsig)

fitted_top1 = Particle('fitted_top1',tsig)
fitted_top2 = Particle('fitted_top2',tsig)
fitted_tt = Particle('fitted_tt',tsig)
chi2 = array( 'f', [ 0. ] )
tsig.Branch('chi2',chi2,'chi2/F')
b1_csv = array( 'f', [ 0. ] )
tsig.Branch('b1_csv',b1_csv,'b1_csv/F')
b2_csv = array( 'f', [ 0. ] )
tsig.Branch('b2_csv',b2_csv,'b2_csv/F')
delta_w1M = array( 'f', [ 0. ] )
tsig.Branch('delta_w1M',delta_w1M,'delta_w1M/F')
delta_w2M = array( 'f', [ 0. ] )
tsig.Branch('delta_w2M',delta_w2M,'delta_w2M/F')
delta_t1M = array( 'f', [ 0. ] )
tsig.Branch('delta_t1M',delta_t1M,'delta_t1M/F')
delta_t2M = array( 'f', [ 0. ] )
tsig.Branch('delta_t2M',delta_t2M,'delta_t2M/F')
ttCls = array( 'f', [ 0. ] )
tsig.Branch('ttCls',ttCls,'ttCls/F')
n_bjets = array( 'I', [ 0 ] )
tsig.Branch('n_bjets',n_bjets,'n_bjets/I')
n_addbjets = array( 'I', [ 0 ] )
tsig.Branch('n_addbjets',n_addbjets,'n_addbjets/I')
ht = array( 'f', [ 0. ] )
tsig.Branch('ht',ht,'ht/F')
weight = array( 'f', [ 0. ] )
tsig.Branch('weight',weight,'weight/F')
wkin = array( 'f', [ 0. ] )
tsig.Branch('wkin',wkin,'wkin/F')
prob_chi2 = array( 'f', [ 0. ] )
tsig.Branch('prob_chi2',prob_chi2,'prob_chi2/F')
n_jets = array( 'i', [ 0 ] )
tsig.Branch('n_jets',n_jets,'n_jets/I')
maxaddjet = 10
simple_chi2 = array( 'f', [ 0. ] )
tsig.Branch('simple_chi2',simple_chi2,'simple_chi2/F')
n_addJets = array( 'I', [ 0 ] )
tsig.Branch('n_addJets',n_addJets,'n_addJets/I')
addJet_CSV = array( 'f', maxb*[ 0. ] )
tsig.Branch('addJet_CSV',addJet_CSV,'addJet_CSV[n_addJets]/F')
addJet_pt = array( 'f', maxb*[ 0. ] )
tsig.Branch('addJet_pt',addJet_pt,'addJet_pt[n_addJets]/F')
addJet_deltaR = array( 'f', [ 0. ] )
tsig.Branch('addJet_deltaR',addJet_deltaR,'addJet_deltaR/F')
addJet_deltaPhi = array( 'f', [ 0. ] )
tsig.Branch('addJet_deltaPhi',addJet_deltaPhi,'addJet_deltaPhi/F')
memttbb = array( 'd', [ 0. ] )
tsig.Branch('memttbb',memttbb,'memttbb/D')
jet_CSV = array( 'f', 6*[ 0. ] )
tsig.Branch('jet_CSV',jet_CSV,'jet_CSV[6]/F')
jet_QGL = array( 'f', 6*[ 0. ] )
tsig.Branch('jet_QGL',jet_QGL,'jet_QGL[6]/F')
