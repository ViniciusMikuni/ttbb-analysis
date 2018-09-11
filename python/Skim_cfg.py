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
chi2cut=28.4732
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
            #f2 = ROOT.TFile.Open('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root')
            #f2.Close()
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_PDF.root')
      elif sample == 'ttbar_fast':
            #f2 = ROOT.TFile.Open('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root')
            #f2.Close()
            #t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root')
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_v2.root')
      elif sample == 'QCD300':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
      elif sample == 'QCD500':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
      elif sample == 'QCD700':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
      elif sample == 'QCD1000':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
      elif sample == 'QCD1500':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
      elif sample == 'QCD200':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
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
      elif sample == 'ttH':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root')
            
      elif sample == 'ttW_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_v2.root')
      elif sample == 'ttZ_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v2.root')
      elif sample == 'WJ_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8_v2.root')
      elif sample == 'ZJ_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ZJetsToQQ_HT600toInf_13TeV-madgraph_v2.root')
      elif sample == 'tW_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4_v2.root')
      elif sample == 'tbarW_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4_v2.root')
      elif sample == 't_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin_v2.root ')
      elif sample == 'tbar_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin_v2.root')
      elif sample == 's_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8_v2.root')
      elif sample == 'WW_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/WW_TuneCUETP8M1_13TeV-pythia8_v2.root')
      elif sample == 'WZ_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/WZ_TuneCUETP8M1_13TeV-pythia8_v2.root')
      elif sample == 'ZZ_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ZZ_TuneCUETP8M1_13TeV-pythia8_v2.root')
      elif sample == 'ttH_fast':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8_v2.root')
      elif sample == 'theory_fsr_down':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-fsrdown-pythia8.root')
      elif sample == 'theory_pdf':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_PDF.root')
      elif sample == 'theory_fsr_up':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-fsrup-pythia8.root')
      elif sample == 'theory_isr_down':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8.root')
      elif sample == 'theory_isr_up':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8.root')
      elif sample == 'theory_hdamp_up':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-hdampup-pythia8.root')
      elif sample == 'theory_hdamp_down':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-hdampdown-pythia8.root')
      elif sample == 'theory_tune_up':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-tuneup-pythia8.root')
      elif sample == 'theory_tune_down':
            t.Add('/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/tth/TT_TuneCUETP8M2T4_13TeV-powheg-tunedown-pythia8.root')

      else: print "No sample fits the current supported ones"


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
    'C': [1,'F'],
    'qgLR': [1,'F'],
    'btagLR4b': [1,'F'],
    'btagLR3b': [1,'F'],
    'n_jets': [1,'F'],
    'simple_chi2': [1,'F'],
    'chi2': [1,'F'],
    'BDT_Comb': [1,'F'],
    'BDT_CWoLa': [1,'F'],
    'nBCSVM':[1,'F'],
    'prob_chi2': [1,'F'],
    #'qgLR': [1,'F'],
    'isCorrect': [1,'I'],
    'isQCD': [1,'I'],
    'hasCorrect': [1,'I'],
    'hasbCorrect': [1,'I'],
    'has4light': [1,'I'],
    'isPerfect': [1,'I'],
    'chi2Correct': [1,'I'],
    'deltaRp1p2': [1,'F'],
    'deltaRq1q2': [1,'F'],
    'deltaRb1b2': [1,'F'],
    'deltaRb1w1': [1,'F'],
    'deltaRb2w2': [1,'F'],
    'deltaEtap1p2': [1,'F'],
    'deltaEtab1b2': [1,'F'],
    'deltaEtaq1q2': [1,'F'],
    'deltaEtaw1w2': [1,'F'],
    'deltaEtat1t2': [1,'F'],
    'deltaPhip1p2': [1,'F'],
    'deltaPhiq1q2': [1,'F'],
    'deltaPhib1b2': [1,'F'],
    'deltaPhiw1w2': [1,'F'],
    'deltaPhit1t2': [1,'F'],
    #'btagLR4b': [1,'F'],
    #'btagLR3b': [1,'F'],
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
    'qgweight': [1 , 'F'],
    'qgweight_Up': [1 , 'F'],
    'qgweight_Down': [1 , 'F'],
    'btagweight': [1 , 'F'],
    'trigweight': [1 , 'F'],
    'trigweight_Up': [1 , 'F'],
    'trigweight_Down': [1 , 'F'],
    'LHE_renormweight':[1,'F'],
    'LHE_renormweight_Up':[1,'F'],
    'LHE_renormweight_Down':[1,'F'],
    'LHE_factweight':[1,'F'],
    'LHE_factweight_Up':[1,'F'],
    'LHE_factweight_Down':[1,'F'],
    'LHEPDFweight':[1,'F'],
    'LHEPDFweight_Down':[1,'F'],
    'LHEPDFweight_Up':[1,'F'],

    #'n_jets': [1,'F'],
    #'simple_chi2': [1,'F'],
    #'prob_chi2': [1,'F'],
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
    'addJet_mass': [maxb,'F'],
    #'memttbb': [1,'F'],
    'p1b1_mass': [1,'F'],
    'q1b2_mass': [1,'F'],
    'deltaRb1p1': [1,'F'],
    'deltaRb2q1': [1,'F'],
    'deltaRb1top2': [1,'F'],
    'deltaRb2top1': [1,'F'],
    'deltaRb1w2': [1,'F'],
    'deltaRb2w1': [1,'F'],
    'mindeltaRb1p': [1,'F'],
    'mindeltaRb2q': [1,'F'],
    'deltaRaddb1': [1,'F'],
    'deltaRaddb2': [1,'F'],
    'deltaRaddw1': [1,'F'],
    'deltaRaddw2': [1,'F'],
    'deltaRaddtop1': [1,'F'],
    'deltaRaddtop2': [1,'F'],
    'n_topjets': [1,'I'],
    'existCorrect': [1,'I'],
    'corr_comb':[6,'I'],
    'best_comb':[6,'I'],
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
    'best_permut': [6,'F'],
    'jet_QGL': [6,'F'],
    'all_mass':[1,'F'],
    'closest_mass':[1,'F'],
    'jets_dRavg':[1,'F'],
    'jets_dRmin':[1,'F'],
    'jets_dRmax':[1,'F'],
    'BDT_ttlf': [1,'F'],
    'BDT_ttcc': [1,'F'],
    'BDT_ttbb': [1,'F'],
    #'BDT_Comb': [1,'F'],
    'BDT_Class': [3,'I'],
    'pass_sys': [1,'I'],
    'pass_nom': [1,'I'],
    'BDT_ClassMajo':[3,'I'],
    'BDT_ttbar':[1,'F'],
    'BDT_ttbarMax':[1,'F'],
    'BDT_ttbarMajo':[1,'F'],
    'BDTMisc':[1,'F'],
    #'BDT_CWoLa':[1,'F'],
    'ptD':[1,'F'],
    'LHA':[1,'F'],
    'width':[1,'F'],
    'mass':[1,'F'],
    'nPVs':[1,'F'],
    'sphericity':[1,'F'],
    'soft_eta1':[1,'F'],
    'soft_eta2':[1,'F'],
    'minjetpt':[1,'F'],
    'topweight':[1,'F'],
    'topweight_Up':[1,'F'],
    'topweight_Down':[1,'F'],
    'puweight': [1 , 'F'],
    'puweight_Up': [1 , 'F'],
    'puweight_Down': [1 , 'F'],
    'gen_top_pt': [2 , 'F'],

    'btagweight_jesPileUpPtBB_Down':[1,'F'],
    'btagweight_jesFlavorQCD_Down':[1,'F'],
    'btagweight_jesAbsoluteScale_Down':[1,'F'],
    'btagweight_jesPileUpPtRef_Down':[1,'F'],
    'btagweight_jesRelativeFSR_Down':[1,'F'],
    'btagweight_jesTimePtEta_Down':[1,'F'],
    'btagweight_hf_Down':[1,'F'],
    'btagweight_cferr1_Down':[1,'F'],
    'btagweight_cferr2_Down':[1,'F'],
    'btagweight_jes_Down':[1,'F'],
    'btagweight_jesAbsoluteMPFBias_Down':[1,'F'],
    'btagweight_lf_Down':[1,'F'],
    'btagweight_jesPileUpPtEC1_Down':[1,'F'],
    'btagweight_lfstats2_Down':[1,'F'],
    'btagweight_lfstats1_Down':[1,'F'],
    'btagweight_hfstats2_Down':[1,'F'],
    'btagweight_hfstats1_Down':[1,'F'],
    'btagweight_jesPileUpDataMC_Down':[1,'F'],

    'btagweight_jesPileUpPtBB_Up':[1,'F'],
    'btagweight_jesFlavorQCD_Up':[1,'F'],
    'btagweight_jesAbsoluteScale_Up':[1,'F'],
    'btagweight_jesPileUpPtRef_Up':[1,'F'],
    'btagweight_jesRelativeFSR_Up':[1,'F'],
    'btagweight_jesTimePtEta_Up':[1,'F'],
    'btagweight_hf_Up':[1,'F'],
    'btagweight_cferr1_Up':[1,'F'],
    'btagweight_cferr2_Up':[1,'F'],
    'btagweight_jes_Up':[1,'F'],
    'btagweight_jesAbsoluteMPFBias_Up':[1,'F'],
    'btagweight_lf_Up':[1,'F'],
    'btagweight_jesPileUpPtEC1_Up':[1,'F'],
    'btagweight_lfstats2_Up':[1,'F'],
    'btagweight_lfstats1_Up':[1,'F'],
    'btagweight_hfstats2_Up':[1,'F'],
    'btagweight_hfstats1_Up':[1,'F'],
    'btagweight_jesPileUpDataMC_Up':[1,'F'],


    #'nBCSVM':[1,'F'],
    # 'nBCSVM_AbsoluteStat_Up':[1,'F'],
    # 'nBCSVM_AbsoluteStat_Up':[1,'F'],
    # 'nBCSVM_AbsoluteScale_Up':[1,'F'],
    # 'nBCSVM_AbsoluteFlavMap_Up':[1,'F'],
    # 'nBCSVM_AbsoluteMPFBias_Up':[1,'F'],
    # 'nBCSVM_Fragmentation_Up':[1,'F'],
    # 'nBCSVM_SinglePionECAL_Up':[1,'F'],
    # 'nBCSVM_SinglePionHCAL_Up':[1,'F'],
    # 'nBCSVM_FlavorQCD_Up':[1,'F'],
    # 'nBCSVM_TimePtEta_Up':[1,'F'],
    # 'nBCSVM_RelativeJEREC1_Up':[1,'F'],
    # 'nBCSVM_RelativeJEREC2_Up':[1,'F'],
    # 'nBCSVM_RelativeJERHF_Up':[1,'F'],
    # 'nBCSVM_RelativePtBB_Up':[1,'F'],
    # 'nBCSVM_RelativePtEC1_Up':[1,'F'],
    # 'nBCSVM_RelativePtEC2_Up':[1,'F'],
    # 'nBCSVM_RelativePtHF_Up':[1,'F'],
    # 'nBCSVM_RelativeBal_Up':[1,'F'],
    # 'nBCSVM_RelativeFSR_Up':[1,'F'],
    # 'nBCSVM_RelativeStatFSR_Up':[1,'F'],
    # 'nBCSVM_RelativeStatEC_Up':[1,'F'],
    # 'nBCSVM_RelativeStatHF_Up':[1,'F'],
    # 'nBCSVM_PileUpDataMC_Up':[1,'F'],
    # 'nBCSVM_PileUpPtRef_Up':[1,'F'],
    # 'nBCSVM_PileUpPtBB_Up':[1,'F'],
    # 'nBCSVM_PileUpPtEC1_Up':[1,'F'],
    # 'nBCSVM_PileUpPtEC2_Up':[1,'F'],
    # 'nBCSVM_PileUpPtHF_Up':[1,'F'],
    # 'nBCSVM_PileUpMuZero_Up':[1,'F'],
    # 'nBCSVM_PileUpEnvelope_Up':[1,'F'],
    # 'nBCSVM_SubTotalPileUp_Up':[1,'F'],
    # 'nBCSVM_SubTotalRelative_Up':[1,'F'],
    # 'nBCSVM_SubTotalPt_Up':[1,'F'],
    # 'nBCSVM_SubTotalScale_Up':[1,'F'],
    # 'nBCSVM_SubTotalAbsolute_Up':[1,'F'],
    # 'nBCSVM_SubTotalMC_Up':[1,'F'],
    # 'nBCSVM_Total_Up':[1,'F'],
    # 'nBCSVM_TotalNoFlavor_Up':[1,'F'],
    # 'nBCSVM_TotalNoTime_Up':[1,'F'],
    # 'nBCSVM_TotalNoFlavorNoTime_Up':[1,'F'],
    # 'nBCSVM_FlavorZJet_Up':[1,'F'],
    # 'nBCSVM_FlavorPhotonJet_Up':[1,'F'],
    # 'nBCSVM_FlavorPureGluon_Up':[1,'F'],
    # 'nBCSVM_FlavorPureQuark_Up':[1,'F'],
    # 'nBCSVM_FlavorPureCharm_Up':[1,'F'],
    # 'nBCSVM_FlavorPureBottom_Up':[1,'F'],
    # 'nBCSVM_TimeRunBCD_Up':[1,'F'],
    # 'nBCSVM_TimeRunEF_Up':[1,'F'],
    # 'nBCSVM_TimeRunG_Up':[1,'F'],
    # 'nBCSVM_TimeRunH_Up':[1,'F'],
    # 'nBCSVM_CorrelationGroupMPFInSitu_Up':[1,'F'],
    # 'nBCSVM_CorrelationGroupIntercalibration_Up':[1,'F'],
    # 'nBCSVM_CorrelationGroupbJES_Up':[1,'F'],
    # 'nBCSVM_CorrelationGroupFlavor_Up':[1,'F'],
    # 'nBCSVM_CorrelationGroupUncorrelated_Up':[1,'F'],
    # 'nBCSVM_JER_Up':[1,'F'],
    'genTopHad_pt':[2,'F'],

    # 'nBCSVM_AbsoluteStat_Down':[1,'F'],
    # 'nBCSVM_AbsoluteScale_Down':[1,'F'],
    # 'nBCSVM_AbsoluteFlavMap_Down':[1,'F'],
    # 'nBCSVM_AbsoluteMPFBias_Down':[1,'F'],
    # 'nBCSVM_Fragmentation_Down':[1,'F'],
    # 'nBCSVM_SinglePionECAL_Down':[1,'F'],
    # 'nBCSVM_SinglePionHCAL_Down':[1,'F'],
    # 'nBCSVM_FlavorQCD_Down':[1,'F'],
    # 'nBCSVM_TimePtEta_Down':[1,'F'],
    # 'nBCSVM_RelativeJEREC1_Down':[1,'F'],
    # 'nBCSVM_RelativeJEREC2_Down':[1,'F'],
    # 'nBCSVM_RelativeJERHF_Down':[1,'F'],
    # 'nBCSVM_RelativePtBB_Down':[1,'F'],
    # 'nBCSVM_RelativePtEC1_Down':[1,'F'],
    # 'nBCSVM_RelativePtEC2_Down':[1,'F'],
    # 'nBCSVM_RelativePtHF_Down':[1,'F'],
    # 'nBCSVM_RelativeBal_Down':[1,'F'],
    # 'nBCSVM_RelativeFSR_Down':[1,'F'],
    # 'nBCSVM_RelativeStatFSR_Down':[1,'F'],
    # 'nBCSVM_RelativeStatEC_Down':[1,'F'],
    # 'nBCSVM_RelativeStatHF_Down':[1,'F'],
    # 'nBCSVM_PileUpDataMC_Down':[1,'F'],
    # 'nBCSVM_PileUpPtRef_Down':[1,'F'],
    # 'nBCSVM_PileUpPtBB_Down':[1,'F'],
    # 'nBCSVM_PileUpPtEC1_Down':[1,'F'],
    # 'nBCSVM_PileUpPtEC2_Down':[1,'F'],
    # 'nBCSVM_PileUpPtHF_Down':[1,'F'],
    # 'nBCSVM_PileUpMuZero_Down':[1,'F'],
    # 'nBCSVM_PileUpEnvelope_Down':[1,'F'],
    # 'nBCSVM_SubTotalPileUp_Down':[1,'F'],
    # 'nBCSVM_SubTotalRelative_Down':[1,'F'],
    # 'nBCSVM_SubTotalPt_Down':[1,'F'],
    # 'nBCSVM_SubTotalScale_Down':[1,'F'],
    # 'nBCSVM_SubTotalAbsolute_Down':[1,'F'],
    # 'nBCSVM_SubTotalMC_Down':[1,'F'],
    # 'nBCSVM_Total_Down':[1,'F'],
    # 'nBCSVM_TotalNoFlavor_Down':[1,'F'],
    # 'nBCSVM_TotalNoTime_Down':[1,'F'],
    # 'nBCSVM_TotalNoFlavorNoTime_Down':[1,'F'],
    # 'nBCSVM_FlavorZJet_Down':[1,'F'],
    # 'nBCSVM_FlavorPhotonJet_Down':[1,'F'],
    # 'nBCSVM_FlavorPureGluon_Down':[1,'F'],
    # 'nBCSVM_FlavorPureQuark_Down':[1,'F'],
    # 'nBCSVM_FlavorPureCharm_Down':[1,'F'],
    # 'nBCSVM_FlavorPureBottom_Down':[1,'F'],
    # 'nBCSVM_TimeRunBCD_Down':[1,'F'],
    # 'nBCSVM_TimeRunEF_Down':[1,'F'],
    # 'nBCSVM_TimeRunG_Down':[1,'F'],
    # 'nBCSVM_TimeRunH_Down':[1,'F'],
    # 'nBCSVM_CorrelationGroupMPFInSitu_Down':[1,'F'],
    # 'nBCSVM_CorrelationGroupIntercalibration_Down':[1,'F'],
    # 'nBCSVM_CorrelationGroupbJES_Down':[1,'F'],
    # 'nBCSVM_CorrelationGroupFlavor_Down':[1,'F'],
    # 'nBCSVM_CorrelationGroupUncorrelated_Down':[1,'F'],
    # 'nBCSVM_JER_Down':[1,'F'],
    #
    #
    # 'btagLR4b_AbsoluteStat_Down':[1,'F'],
    # 'btagLR4b_AbsoluteScale_Down':[1,'F'],
    # 'btagLR4b_AbsoluteFlavMap_Down':[1,'F'],
    # 'btagLR4b_AbsoluteMPFBias_Down':[1,'F'],
    # 'btagLR4b_Fragmentation_Down':[1,'F'],
    # 'btagLR4b_SinglePionECAL_Down':[1,'F'],
    # 'btagLR4b_SinglePionHCAL_Down':[1,'F'],
    # 'btagLR4b_FlavorQCD_Down':[1,'F'],
    # 'btagLR4b_TimePtEta_Down':[1,'F'],
    # 'btagLR4b_RelativeJEREC1_Down':[1,'F'],
    # 'btagLR4b_RelativeJEREC2_Down':[1,'F'],
    # 'btagLR4b_RelativeJERHF_Down':[1,'F'],
    # 'btagLR4b_RelativePtBB_Down':[1,'F'],
    # 'btagLR4b_RelativePtEC1_Down':[1,'F'],
    # 'btagLR4b_RelativePtEC2_Down':[1,'F'],
    # 'btagLR4b_RelativePtHF_Down':[1,'F'],
    # 'btagLR4b_RelativeBal_Down':[1,'F'],
    # 'btagLR4b_RelativeFSR_Down':[1,'F'],
    # 'btagLR4b_RelativeStatFSR_Down':[1,'F'],
    # 'btagLR4b_RelativeStatEC_Down':[1,'F'],
    # 'btagLR4b_RelativeStatHF_Down':[1,'F'],
    # 'btagLR4b_PileUpDataMC_Down':[1,'F'],
    # 'btagLR4b_PileUpPtRef_Down':[1,'F'],
    # 'btagLR4b_PileUpPtBB_Down':[1,'F'],
    # 'btagLR4b_PileUpPtEC1_Down':[1,'F'],
    # 'btagLR4b_PileUpPtEC2_Down':[1,'F'],
    # 'btagLR4b_PileUpPtHF_Down':[1,'F'],
    # 'btagLR4b_PileUpMuZero_Down':[1,'F'],
    # 'btagLR4b_PileUpEnvelope_Down':[1,'F'],
    # 'btagLR4b_SubTotalPileUp_Down':[1,'F'],
    # 'btagLR4b_SubTotalRelative_Down':[1,'F'],
    # 'btagLR4b_SubTotalPt_Down':[1,'F'],
    # 'btagLR4b_SubTotalScale_Down':[1,'F'],
    # 'btagLR4b_SubTotalAbsolute_Down':[1,'F'],
    # 'btagLR4b_SubTotalMC_Down':[1,'F'],
    # 'btagLR4b_Total_Down':[1,'F'],
    # 'btagLR4b_TotalNoFlavor_Down':[1,'F'],
    # 'btagLR4b_TotalNoTime_Down':[1,'F'],
    # 'btagLR4b_TotalNoFlavorNoTime_Down':[1,'F'],
    # 'btagLR4b_FlavorZJet_Down':[1,'F'],
    # 'btagLR4b_FlavorPhotonJet_Down':[1,'F'],
    # 'btagLR4b_FlavorPureGluon_Down':[1,'F'],
    # 'btagLR4b_FlavorPureQuark_Down':[1,'F'],
    # 'btagLR4b_FlavorPureCharm_Down':[1,'F'],
    # 'btagLR4b_FlavorPureBottom_Down':[1,'F'],
    # 'btagLR4b_TimeRunBCD_Down':[1,'F'],
    # 'btagLR4b_TimeRunEF_Down':[1,'F'],
    # 'btagLR4b_TimeRunG_Down':[1,'F'],
    # 'btagLR4b_TimeRunH_Down':[1,'F'],
    # 'btagLR4b_CorrelationGroupMPFInSitu_Down':[1,'F'],
    # 'btagLR4b_CorrelationGroupIntercalibration_Down':[1,'F'],
    # 'btagLR4b_CorrelationGroupbJES_Down':[1,'F'],
    # 'btagLR4b_CorrelationGroupFlavor_Down':[1,'F'],
    # 'btagLR4b_CorrelationGroupUncorrelated_Down':[1,'F'],
    # 'btagLR4b_JER_Down':[1,'F'],
    #
    # 'btagLR4b_AbsoluteStat_Up':[1,'F'],
    # 'btagLR4b_AbsoluteScale_Up':[1,'F'],
    # 'btagLR4b_AbsoluteFlavMap_Up':[1,'F'],
    # 'btagLR4b_AbsoluteMPFBias_Up':[1,'F'],
    # 'btagLR4b_Fragmentation_Up':[1,'F'],
    # 'btagLR4b_SinglePionECAL_Up':[1,'F'],
    # 'btagLR4b_SinglePionHCAL_Up':[1,'F'],
    # 'btagLR4b_FlavorQCD_Up':[1,'F'],
    # 'btagLR4b_TimePtEta_Up':[1,'F'],
    # 'btagLR4b_RelativeJEREC1_Up':[1,'F'],
    # 'btagLR4b_RelativeJEREC2_Up':[1,'F'],
    # 'btagLR4b_RelativeJERHF_Up':[1,'F'],
    # 'btagLR4b_RelativePtBB_Up':[1,'F'],
    # 'btagLR4b_RelativePtEC1_Up':[1,'F'],
    # 'btagLR4b_RelativePtEC2_Up':[1,'F'],
    # 'btagLR4b_RelativePtHF_Up':[1,'F'],
    # 'btagLR4b_RelativeBal_Up':[1,'F'],
    # 'btagLR4b_RelativeFSR_Up':[1,'F'],
    # 'btagLR4b_RelativeStatFSR_Up':[1,'F'],
    # 'btagLR4b_RelativeStatEC_Up':[1,'F'],
    # 'btagLR4b_RelativeStatHF_Up':[1,'F'],
    # 'btagLR4b_PileUpDataMC_Up':[1,'F'],
    # 'btagLR4b_PileUpPtRef_Up':[1,'F'],
    # 'btagLR4b_PileUpPtBB_Up':[1,'F'],
    # 'btagLR4b_PileUpPtEC1_Up':[1,'F'],
    # 'btagLR4b_PileUpPtEC2_Up':[1,'F'],
    # 'btagLR4b_PileUpPtHF_Up':[1,'F'],
    # 'btagLR4b_PileUpMuZero_Up':[1,'F'],
    # 'btagLR4b_PileUpEnvelope_Up':[1,'F'],
    # 'btagLR4b_SubTotalPileUp_Up':[1,'F'],
    # 'btagLR4b_SubTotalRelative_Up':[1,'F'],
    # 'btagLR4b_SubTotalPt_Up':[1,'F'],
    # 'btagLR4b_SubTotalScale_Up':[1,'F'],
    # 'btagLR4b_SubTotalAbsolute_Up':[1,'F'],
    # 'btagLR4b_SubTotalMC_Up':[1,'F'],
    # 'btagLR4b_Total_Up':[1,'F'],
    # 'btagLR4b_TotalNoFlavor_Up':[1,'F'],
    # 'btagLR4b_TotalNoTime_Up':[1,'F'],
    # 'btagLR4b_TotalNoFlavorNoTime_Up':[1,'F'],
    # 'btagLR4b_FlavorZJet_Up':[1,'F'],
    # 'btagLR4b_FlavorPhotonJet_Up':[1,'F'],
    # 'btagLR4b_FlavorPureGluon_Up':[1,'F'],
    # 'btagLR4b_FlavorPureQuark_Up':[1,'F'],
    # 'btagLR4b_FlavorPureCharm_Up':[1,'F'],
    # 'btagLR4b_FlavorPureBottom_Up':[1,'F'],
    # 'btagLR4b_TimeRunBCD_Up':[1,'F'],
    # 'btagLR4b_TimeRunEF_Up':[1,'F'],
    # 'btagLR4b_TimeRunG_Up':[1,'F'],
    # 'btagLR4b_TimeRunH_Up':[1,'F'],
    # 'btagLR4b_CorrelationGroupMPFInSitu_Up':[1,'F'],
    # 'btagLR4b_CorrelationGroupIntercalibration_Up':[1,'F'],
    # 'btagLR4b_CorrelationGroupbJES_Up':[1,'F'],
    # 'btagLR4b_CorrelationGroupFlavor_Up':[1,'F'],
    # 'btagLR4b_CorrelationGroupUncorrelated_Up':[1,'F'],
    # 'btagLR4b_JER_Up':[1,'F']
    #


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
        self.tree = tree
        for var in tvarlist_:
            self.variables[var]=array(tvarlist_[var][1].lower(),tvarlist_[var][0]*[-10])
            self.tree.Branch(var,self.variables[var],var+'['+str(tvarlist_[var][0])+']/'+tvarlist_[var][1])

    def ZeroArray(self):
        for var in self.variables:
            for dummy in range(len(self.variables[var])):
                self.variables[var][dummy] = -10
    def Print(self,varlist=[]):
        for var in self.variables:
            if len(varlist)>0:
                if var not in varlist:continue
            else:
                for dummy in range(len(self.variables[var])):
                    print var, self.variables[var][dummy]
        print '################################################################'
    def HaveBranch(self,bname):
        return hasattr(self.tree,bname)




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
    'b1_pt': b1.pt,
    'b2_eta': b2.eta,
    'b1_eta': b1.eta,
    'b2_phi': b2.phi,
    'b1_phi': b1.phi,
    'lq1_phi': lq1.phi,
    'lq2_phi': lq2.phi,
    'lp2_pt': lp2.pt,
    'lq2_pt': lq2.pt,
    'lp1_pt': lp1.pt,
    'lq1_pt': lq1.pt,
    'lp2_eta': lp2.eta,
    'lq2_eta': lq2.eta,
    'lp1_eta': lp1.eta,
    'lq1_eta': lq1.eta,

    'w2_m': w2.mass,
    'top1_m': top1.mass,
    'top1_phi': top1.phi,
    'top2_phi': top2.phi,
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

sys_list=[

'_RelativeStatEC',
'_RelativeStatHF',
'_PileUpDataMC',
'_PileUpPtRef',
'_PileUpPtBB',
'_PileUpPtEC1',
'_PileUpPtEC2',
'_PileUpPtHF',
'_RelativeStatFSR',
'_RelativeFSR',
'_AbsoluteScale',
'_AbsoluteFlavMap',
'_AbsoluteMPFBias',
'_Fragmentation',
'_SinglePionECAL',
'_SinglePionHCAL',
'_FlavorQCD',
'_TimePtEta',
'_RelativeJEREC1',
'_RelativeJEREC2',
'_RelativeJERHF',
'_RelativePtBB',
'_RelativePtEC1',
'_RelativePtEC2',
'_RelativePtHF',
'_SubTotalPileUp',
'_JER',
'_AbsoluteStat',
'_Total',
]




