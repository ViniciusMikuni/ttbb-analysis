#!/usr/bin/env python 
import sys
import ROOT
from itertools import permutations, combinations
import numpy as np
from os import environ
environ['KERAS_BACKEND'] = 'theano'
import re

sys.path.insert(0, '/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test')
#import Kinematic_Fit_FH_cfg
from Skim_cfg import *
ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.LoadMacro("CRcorrections/btagCorrections.h+")
# ROOT.gSystem.Load("libPhysicsToolsKinFitter.so")
# ROOT.gROOT.ProcessLine(".L /shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/Kinfit.C+")

from ROOT import TFile,TTree,TString, TMVA, TMath
TMVA.Tools.Instance()
#TMVA.PyMethodBase.PyInitialize()


def JetComb(njets, nbjets,jetpos_,bpos_=[]):
      '''return all the combinations for jet and b-jet  positioning'''
      if nbjets == 0:
            jetpermut_ = list(permutations(jetpos_,6))#permutations of all jets 
            completelist_ = []
            for i in range(len(jetpermut_)):
                  if (jetpermut_[i][0] > jetpermut_[i][1] or jetpermut_[i][2] > jetpermut_[i][3] or jetpermut_[i][4] > jetpermut_[i][5]): continue
                  completelist_.append(jetpermut_[i])
            return completelist_

      else:
            bpermut_ = list(combinations(bpos_,2))
#            print bpermut_, ' bpermut '
            jetpermut_ = list(permutations(jetpos_,4 if len(jetpos_) >= 4 else 3))#permutations of all jets - bjets
            completelist_ = []
            for i in range(len(bpermut_)):
                  for j in range(len(jetpermut_)):
                        if len(jetpos_) >= 4 and (jetpermut_[j][0] > jetpermut_[j][1] or jetpermut_[j][2] > jetpermut_[j][3]): continue
                        if len(jetpos_) == 3 and jetpermut_[j][0] > jetpermut_[j][1]: continue
                        completelist_.append(bpermut_[i] + jetpermut_[j])
#            print completelist_, ' complete list ', nbjets, ' nbjets ', njets, ' njets'
            return completelist_
      

def UpdateVariables(comb,jet,var,MVA_Only):
      var['simple_chi2'][0] = pow(((jet[comb[0]] + jet[comb[2]]+ jet[comb[3]]).M() - 169.1)/20.5,2) + pow(((jet[comb[1]] + jet[comb[4]]+ jet[comb[5]]).M() - 174.5)/17.8,2) + pow(((jet[comb[2]]+ jet[comb[3]]).M() - 82.3)/10.9,2) + pow(((jet[comb[5]]+ jet[comb[4]]).M() - 82.3)/10.9,2)
      var['prob_chi2'][0] = TMath.Prob(var['simple_chi2'][0],4)
      if var['prob_chi2'][0] < probcut: return
      addjets = [x for x in alljets if x not in comb]
      addjetscsv = []
      if len(addjets) < 10:
            for najet,ajet in enumerate(addjets):
                  addjetscsv.append(t.jets_btagCSV[ajet])
            csvrank = np.flip(np.argsort(addjetscsv),0)
            if len(csvrank)>=1:
                  MVA_Only['addJet_CSV[0]'][0] = t.jets_btagCSV[addjets[csvrank[0]]]
                  MVA_Only['addJet_QGL[0]'][0] = t.jets_qgl[addjets[csvrank[0]]]
                  MVA_Only['addJet_pt[0]'][0] = t.jets_pt[addjets[csvrank[0]]]
                  MVA_Only['addJet_eta[0]'][0] = t.jets_eta[addjets[csvrank[0]]]
                  MVA_Only['addJet_phi[0]'][0] = t.jets_phi[addjets[csvrank[0]]]
                  var['deltaRaddb1'][0] = jet[addjets[csvrank[0]]].DeltaR(jet[comb[0]])
                  var['deltaRaddb2'][0] = jet[addjets[csvrank[0]]].DeltaR(jet[comb[1]])
                  var['deltaRaddw1'][0] = jet[addjets[csvrank[0]]].DeltaR(jet[comb[3]]+jet[comb[2]])
                  var['deltaRaddw2'][0] = jet[addjets[csvrank[0]]].DeltaR(jet[comb[4]]+jet[comb[5]])
                  var['deltaRaddtop1'][0] = jet[addjets[csvrank[0]]].DeltaR(jet[comb[0]]+jet[comb[2]]+jet[comb[3]])
                  var['deltaRaddtop2'][0] = jet[addjets[csvrank[0]]].DeltaR(jet[comb[1]]+jet[comb[4]]+jet[comb[5]])
                  
                  var['deltaPhiaddb1'][0] = jet[addjets[csvrank[0]]].DeltaPhi(jet[comb[0]])
                  var['deltaPhiaddb2'][0] = jet[addjets[csvrank[0]]].DeltaPhi(jet[comb[1]])
                  var['deltaPhiaddw1'][0] = jet[addjets[csvrank[0]]].DeltaPhi(jet[comb[3]]+jet[comb[2]])
                  var['deltaPhiaddw2'][0] = jet[addjets[csvrank[0]]].DeltaPhi(jet[comb[4]]+jet[comb[5]])
                  var['deltaPhiaddtop1'][0] = jet[addjets[csvrank[0]]].DeltaPhi(jet[comb[0]]+jet[comb[2]]+jet[comb[3]])
                  var['deltaPhiaddtop2'][0] = jet[addjets[csvrank[0]]].DeltaPhi(jet[comb[1]]+jet[comb[4]]+jet[comb[5]])

                  var['deltaEtaaddb1'][0] = jet[addjets[csvrank[0]]].Eta() - jet[comb[0]].Eta()
                  var['deltaEtaaddb2'][0] = jet[addjets[csvrank[0]]].Eta() - jet[comb[1]].Eta()
                  var['deltaEtaaddw1'][0] = jet[addjets[csvrank[0]]].Eta() - (jet[comb[3]]+jet[comb[2]]).Eta()
                  var['deltaEtaaddw2'][0] = jet[addjets[csvrank[0]]].Eta() - (jet[comb[4]]+jet[comb[5]]).Eta()
                  var['deltaEtaaddtop1'][0] = jet[addjets[csvrank[0]]].Eta() - (jet[comb[0]]+jet[comb[2]]+jet[comb[3]]).Eta()
                  var['deltaEtaaddtop2'][0] = jet[addjets[csvrank[0]]].Eta() - (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).Eta()
                  
                  for ind, rev in enumerate(csvrank):
                        var['addJet_CSV'][ind] = t.jets_btagCSV[addjets[csvrank[rev]]]
                        var['addJet_pt'][ind] = t.jets_pt[addjets[csvrank[rev]]]
                        var['addJet_eta'][ind] = t.jets_eta[addjets[csvrank[rev]]]
                        var['addJet_phi'][ind] = t.jets_phi[addjets[csvrank[rev]]]
                        var['addJet_QGL'][ind] = t.jets_qgl[addjets[csvrank[rev]]]
                  
            if len(csvrank)>=2:
                  var['addJet_deltaR'][0] = jet[addjets[csvrank[0]]].DeltaR(jet[addjets[csvrank[1]]])
                  var['addJet_deltaPhi'][0] = jet[addjets[csvrank[0]]].DeltaPhi(jet[addjets[csvrank[1]]])
                  var['addJet_deltaEta'][0] = jet[addjets[csvrank[0]]].Eta() -jet[addjets[csvrank[1]]].Eta()
                  var['addJet_mass'][0] = (jet[addjets[csvrank[0]]]+jet[addjets[csvrank[1]]]).M()
                  MVA_Only['addJet_CSV[1]'][0] = t.jets_btagCSV[addjets[csvrank[1]]]
                  MVA_Only['addJet_QGL[1]'][0] = t.jets_qgl[addjets[csvrank[1]]]
                  MVA_Only['addJet_pt[1]'][0] = t.jets_pt[addjets[csvrank[1]]]
                  MVA_Only['addJet_eta[1]'][0] = t.jets_eta[addjets[csvrank[1]]]
                  MVA_Only['addJet_phi[1]'][0] = t.jets_phi[addjets[csvrank[1]]]



                        
                        
            MVA_Only['top1_m'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).M()
            MVA_Only['top2_m'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).M()
            MVA_Only['tt_m'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]+jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).M()
            MVA_Only['tt_pt'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]+jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Pt()
                  
            MVA_Only['w1_m'][0] = (jet[comb[2]]+jet[comb[3]]).M()
            MVA_Only['w2_m'][0] = (jet[comb[5]]+jet[comb[4]]).M()
            MVA_Only['top1_pt'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Pt()
            MVA_Only['top2_pt'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).Pt()
            MVA_Only['w1_pt'][0] = (jet[comb[2]]+jet[comb[3]]).Pt()
            MVA_Only['w2_pt'][0] = (jet[comb[5]]+jet[comb[4]]).Pt()
            MVA_Only['b1_pt'][0] = (jet[comb[0]]).Pt()
            MVA_Only['b2_pt'][0] = (jet[comb[1]]).Pt()
            var['deltaRl1l2'][0] = jet[comb[2]].DeltaR(jet[comb[3]])
            var['deltaPhil1l2'][0] = jet[comb[2]].DeltaPhi(jet[comb[3]])
            var['deltaPhib1b2'][0] = jet[comb[0]].DeltaPhi(jet[comb[1]])
            
            var['deltaPhiw1w2'][0] = (jet[comb[3]]+jet[comb[2]]).DeltaPhi((jet[comb[5]]+jet[comb[4]]))
            var['deltaPhit1t2'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).DeltaPhi((jet[comb[1]]+jet[comb[5]]+jet[comb[4]]))
            var['deltaRq1q2'][0] = jet[comb[4]].DeltaR(jet[comb[5]])
            var['deltaPhiq1q2'][0] = jet[comb[4]].DeltaPhi(jet[comb[5]])
            
            var['deltaRb1b2'][0] = jet[comb[0]].DeltaR(jet[comb[1]])
            var['deltaRb1w1'][0] = jet[comb[0]].DeltaR(jet[comb[3]]+jet[comb[2]])
            var['deltaRb2w2'][0] = jet[comb[1]].DeltaR(jet[comb[4]]+jet[comb[5]])
            
            var['deltaEtal1l2'][0] = jet[comb[2]].Eta() - jet[comb[3]].Eta()
            var['deltaEtaq1q2'][0] = jet[comb[4]].Eta() - jet[comb[5]].Eta()
            var['deltaEtab1b2'][0] = jet[comb[0]].Eta() - jet[comb[1]].Eta()
            var['deltaEtaw1w2'][0] = (jet[comb[3]]+jet[comb[2]]).Eta() - (jet[comb[5]]+jet[comb[4]]).Eta()
            var['deltaEtat1t2'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Eta() - (jet[comb[1]]+jet[comb[5]]+jet[comb[4]]).Eta()
            
            
            
            var['q1b1_mass'][0] = (jet[comb[0]] + jet[comb[2]]).M()
            var['p1b2_mass'][0] = (jet[comb[1]] + jet[comb[4]]).M()
            var['deltaRb1q1'][0] = jet[comb[0]].DeltaR(jet[comb[2]])
            var['deltaRb2p1'][0] = jet[comb[1]].DeltaR(jet[comb[4]])
            var['deltaRb1top2'][0] = jet[comb[0]].DeltaR(jet[comb[1]]+jet[comb[4]]+jet[comb[5]])
            var['deltaRb2top1'][0] = jet[comb[1]].DeltaR(jet[comb[0]]+jet[comb[2]]+jet[comb[3]])
            var['deltaRb1w2'][0] = jet[comb[0]].DeltaR(jet[comb[4]]+jet[comb[5]])
            var['deltaRb2w1'][0] = jet[comb[1]].DeltaR(jet[comb[2]]+jet[comb[3]])
            minrb1q = var['deltaRb1q1'][0]
            minrb2p = var['deltaRb2p1'][0]
            if jet[comb[0]].DeltaR(jet[comb[3]]) < minrb1q:
                  minrb1q = jet[comb[0]].DeltaR(jet[comb[3]])
            if jet[comb[1]].DeltaR(jet[comb[5]]) < minrb2p:
                  minrb2p = jet[comb[1]].DeltaR(jet[comb[5]])
            var['mindeltaRb1q'][0] = minrb1q
            var['mindeltaRb2p'][0] = minrb2p
            for ipos, pos in enumerate(comb):
                  MVA_Only['jet_CSV['+str(ipos)+']'][0] = t.jets_btagCSV[pos]
                  MVA_Only['jet_MOverPt['+str(ipos)+']'][0] = t.jets_mass[pos]/t.jets_pt[pos]
                  var['jet_MOverPt'][ipos] = t.jets_mass[pos]/t.jets_pt[pos]
                  var['jet_CSV'][ipos] = t.jets_btagCSV[pos]
                  var['jet_DeepCSV'][ipos] = t.jets_btagDeepCSV[pos]
                  var['jet_cMVA'][ipos] = t.jets_btagCMVA[pos]
                  var['jet_DeepcMVA'][ipos] = t.jets_btagDeepCMVA[pos]
                  MVA_Only['jet_QGL['+str(ipos)+']'][0] = t.jets_qgl[pos]
                  var['jet_QGL'][ipos] = t.jets_qgl[pos]

            
      


#def KinAnalysis(tagged,filename,nmaxentries = -1):
if __name__ == "__main__":
 
      if len(sys.argv) > 2:
            filename = sys.argv[1]
            sample = str(sys.argv[2])
      else: print 'Missing arguments'
      print 'start stopwatch'
      watch = ROOT.TStopwatch()
      t = ROOT.TChain('tree')
      AddProcessChain(sample,t)
      usebdt = 1
      emin = emax = 0
      
      with open(filename) as f:
            lines = f.read().splitlines()
            emin = map(int, re.findall(r'\d+', lines[0]))[0]
            emax = map(int, re.findall(r'\d+', lines[0]))[1]           

      foutname = 'Skim_'
      foutname += sample + '_'
      foutname += str(emax)+'.root'
      fout = TFile(foutname,'recreate')

      if sample == 'ttbar':is_ttbar = 1
      else: is_ttbar = 0

      
#      print 'emin and max', emin, emax
      if emax == 0:
          print 'emax == 0'
      print "Using top mass constraint"
      # if sample != 'data': b1 = Particle('b1',tkin,1)
      # else: b1 = Particle('b1',tkin)
      # if sample != 'data': b2 = Particle('b2',tkin,1)
      # else: b2 = Particle('b2',tkin)

      
      reader = TMVA.Reader( "!Color:!Silent" )
      readerMisc = TMVA.Reader( "!Color:!Silent" )
      readerQGL = TMVA.Reader( "!Color:!Silent" )
     
      mytree = ManageTTree(tvars,tkin)

      #usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRl1l2','deltaRq1q2','deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhiw1w2','deltaPhit1t2','q1b1_mass','p1b2_mass','deltaRb1w2','deltaRb2w1','mindeltaRb1q','simple_chi2','mindeltaRb2p', 'deltaEtal1l2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']

      #usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRl1l2','deltaRq1q2','deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhit1t2','q1b1_mass','p1b2_mass','deltaRb1w2','deltaRb2w1','simple_chi2','mindeltaRb2p', 'deltaEtal1l2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']
      
      usevar = ['top1_m','top2_m','w1_m','w2_m','deltaRl1l2','deltaRq1q2','deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhiw1w2','deltaPhit1t2','q1b1_mass','p1b2_mass','deltaRb1w2','deltaRb2w1','mindeltaRb1q','mindeltaRb2p', 'deltaEtal1l2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','prob_chi2']

      useMisc = ['qgLR','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]']
      useQGL = ['qgLR','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]']
      

      

      for var in usevar:
            if var in mytree.variables:reader.AddVariable(var,mytree.variables[var])
            else:reader.AddVariable(var,MVA_Only[var])


      for var in useMisc:
            if var in mytree.variables:readerMisc.AddVariable(var,mytree.variables[var])
            else:readerMisc.AddVariable(var,MVA_Only[var])


      for var in useQGL:
            if var in mytree.variables:readerQGL.AddVariable(var,mytree.variables[var])
            else:readerQGL.AddVariable(var,MVA_Only[var])

     


      weightFileBDT_Comb = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDT_comb_chi2.weights.xml'
      weightFileBDT_Misc = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDT_QCD.weights.xml'
      weightFileBDT_QGL = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDT_QCD_Test.weights.xml'
           
      reader.BookMVA('BDT_Comb',weightFileBDT_Comb)
      readerMisc.BookMVA('BDT_Misc',weightFileBDT_Misc)
      readerQGL.BookMVA('BDT_QGL',weightFileBDT_QGL)
      allcomb_ = {}

      for e,event in enumerate(t) :
#            print "processing event number: ", e
            if e < emin: continue
            if e%100==0: print 'Running entry: ',e, ' of ',emax, ' entries'
            bpos_ = []
            jetpos_ =[]
            jets_ = ROOT.vector('TLorentzVector')()
            ordered_jets_ = ROOT.vector('TLorentzVector')()
            bestcomb_ = []
            corrcomb_ = []
            corrb_ = []
            corrlight_ = []
            ptR=0
            tthcut = t.json and (t.HLT_ttH_FH ) and t.ht>500 and t.jets_pt[5]>40
#            if t.njets >= 6: hPass.SetBinContent(1,hPass.GetBinContent(1)+1)
            if not tthcut: continue
            
            if t.njets >= 7 and t.nBCSVM >=2:
                  if sample !='data':
                        mytree.variables['weight'][0] = np.sign(t.genWeight)
                        mytree.variables['puweight'][0] = t.puWeight
                        mytree.variables['puweight_Up'][0] = t.puWeightUp
                        mytree.variables['puweight_Down'][0] = t.puWeightDown
                        mytree.variables['btagweight'][0] = t.btagWeightCSV 
                        mytree.variables['qgWeight'][0] = t.qgWeight
                        mytree.variables['btagweight_jesPileUpPtBB_Down'][0] = t.btagWeightCSV_down_jesPileUpPtBB
                        mytree.variables['btagweight_jesFlavorQCD_Down'][0] = t.btagWeightCSV_down_jesFlavorQCD
                        mytree.variables['btagweight_jesAbsoluteScale_Down'][0] = t.btagWeightCSV_down_jesAbsoluteScale
                        mytree.variables['btagweight_jesPileUpPtRef_Down'][0] = t.btagWeightCSV_down_jesPileUpPtRef
                        mytree.variables['btagweight_jesRelativeFSR_Down'][0] = t.btagWeightCSV_down_jesRelativeFSR
                        mytree.variables['btagweight_jesTimePtEta_Down'][0] = t.btagWeightCSV_down_jesTimePtEta
                        mytree.variables['btagweight_hf_Down'][0] = t.btagWeightCSV_down_hf
                        mytree.variables['btagweight_cferr1_Down'][0] =t.btagWeightCSV_down_cferr1
                        mytree.variables['btagweight_cferr2_Down'][0] =t.btagWeightCSV_down_cferr2
                        mytree.variables['btagweight_jes_Down'][0] =t.btagWeightCSV_down_jes
                        mytree.variables['btagweight_jesAbsoluteMPFBias_Down'][0] =t.btagWeightCSV_down_jesAbsoluteMPFBias
                        mytree.variables['btagweight_lf_Down'][0] =t.btagWeightCSV_down_lf
                        mytree.variables['btagweight_jesPileUpPtEC1_Down'][0] =t.btagWeightCSV_down_jesPileUpPtEC1
                        mytree.variables['btagweight_lfstats2_Down'][0] =t.btagWeightCSV_down_lfstats2
                        mytree.variables['btagweight_lfstats1_Down'][0] =t.btagWeightCSV_down_lfstats1
                        mytree.variables['btagweight_hfstats2_Down'][0] =t.btagWeightCSV_down_lfstats2
                        mytree.variables['btagweight_hfstats1_Down'][0] =t.btagWeightCSV_down_lfstats1
                        mytree.variables['btagweight_jesPileUpDataMC_Down'][0] =t.btagWeightCSV_down_jesPileUpDataMC

                        mytree.variables['btagweight_jesPileUpPtBB_Up'][0] = t.btagWeightCSV_up_jesPileUpPtBB
                        mytree.variables['btagweight_jesFlavorQCD_Up'][0] = t.btagWeightCSV_up_jesFlavorQCD
                        mytree.variables['btagweight_jesAbsoluteScale_Up'][0] = t.btagWeightCSV_up_jesAbsoluteScale
                        mytree.variables['btagweight_jesPileUpPtRef_Up'][0] = t.btagWeightCSV_up_jesPileUpPtRef
                        mytree.variables['btagweight_jesRelativeFSR_Up'][0] = t.btagWeightCSV_up_jesRelativeFSR
                        mytree.variables['btagweight_jesTimePtEta_Up'][0] = t.btagWeightCSV_up_jesTimePtEta
                        mytree.variables['btagweight_hf_Up'][0] = t.btagWeightCSV_up_hf
                        mytree.variables['btagweight_cferr1_Up'][0] =t.btagWeightCSV_up_cferr1
                        mytree.variables['btagweight_cferr2_Up'][0] =t.btagWeightCSV_up_cferr2
                        mytree.variables['btagweight_jes_Up'][0] =t.btagWeightCSV_up_jes
                        mytree.variables['btagweight_jesAbsoluteMPFBias_Up'][0] =t.btagWeightCSV_up_jesAbsoluteMPFBias
                        mytree.variables['btagweight_lf_Up'][0] =t.btagWeightCSV_up_lf
                        mytree.variables['btagweight_jesPileUpPtEC1_Up'][0] =t.btagWeightCSV_up_jesPileUpPtEC1
                        mytree.variables['btagweight_lfstats2_Up'][0] =t.btagWeightCSV_up_lfstats2
                        mytree.variables['btagweight_lfstats1_Up'][0] =t.btagWeightCSV_up_lfstats1
                        mytree.variables['btagweight_jesPileUpDataMC_Up'][0] =t.btagWeightCSV_up_jesPileUpDataMC
                        mytree.variables['nBCSVM_AbsoluteStat_Up'][0] = t.nBCSVM_AbsoluteStatUp
                        mytree.variables['nBCSVM_AbsoluteScale_Up'][0] = t.nBCSVM_AbsoluteScaleUp
                        mytree.variables['nBCSVM_AbsoluteFlavMap_Up'][0] = t.nBCSVM_AbsoluteFlavMapUp
                        mytree.variables['nBCSVM_AbsoluteMPFBias_Up'][0] = t.nBCSVM_AbsoluteMPFBiasUp
                        mytree.variables['nBCSVM_Fragmentation_Up'][0] = t.nBCSVM_FragmentationUp
                        mytree.variables['nBCSVM_SinglePionECAL_Up'][0] = t.nBCSVM_SinglePionECALUp
                        mytree.variables['nBCSVM_SinglePionHCAL_Up'][0] = t.nBCSVM_SinglePionHCALUp
                        mytree.variables['nBCSVM_FlavorQCD_Up'][0] = t.nBCSVM_FlavorQCDUp
                        mytree.variables['nBCSVM_TimePtEta_Up'][0] = t.nBCSVM_TimePtEtaUp
                        mytree.variables['nBCSVM_RelativeJEREC1_Up'][0] = t.nBCSVM_RelativeJEREC1Up
                        mytree.variables['nBCSVM_RelativeJEREC2_Up'][0] = t.nBCSVM_RelativeJEREC2Up
                        mytree.variables['nBCSVM_RelativeJERHF_Up'][0] = t.nBCSVM_RelativeJERHFUp
                        mytree.variables['nBCSVM_RelativePtBB_Up'][0] = t.nBCSVM_RelativePtBBUp
                        mytree.variables['nBCSVM_RelativePtEC1_Up'][0] = t.nBCSVM_RelativePtEC1Up
                        mytree.variables['nBCSVM_RelativePtEC2_Up'][0] = t.nBCSVM_RelativePtEC2Up
                        mytree.variables['nBCSVM_RelativePtHF_Up'][0] = t.nBCSVM_RelativePtHFUp
                        mytree.variables['nBCSVM_RelativeBal_Up'][0] = t.nBCSVM_RelativeBalUp
                        mytree.variables['nBCSVM_RelativeFSR_Up'][0] = t.nBCSVM_RelativeFSRUp
                        mytree.variables['nBCSVM_RelativeStatFSR_Up'][0] = t.nBCSVM_RelativeStatFSRUp
                        mytree.variables['nBCSVM_RelativeStatEC_Up'][0] = t.nBCSVM_RelativeStatECUp
                        mytree.variables['nBCSVM_RelativeStatHF_Up'][0] = t.nBCSVM_RelativeStatHFUp
                        mytree.variables['nBCSVM_PileUpDataMC_Up'][0] = t.nBCSVM_PileUpDataMCUp
                        mytree.variables['nBCSVM_PileUpPtRef_Up'][0] = t.nBCSVM_PileUpPtRefUp
                        mytree.variables['nBCSVM_PileUpPtBB_Up'][0] = t.nBCSVM_PileUpPtBBUp
                        mytree.variables['nBCSVM_PileUpPtEC1_Up'][0] = t.nBCSVM_PileUpPtEC1Up
                        mytree.variables['nBCSVM_PileUpPtEC2_Up'][0] = t.nBCSVM_PileUpPtEC2Up
                        mytree.variables['nBCSVM_PileUpPtHF_Up'][0] = t.nBCSVM_PileUpPtHFUp
                        mytree.variables['nBCSVM_PileUpMuZero_Up'][0] = t.nBCSVM_PileUpMuZeroUp
                        mytree.variables['nBCSVM_PileUpEnvelope_Up'][0] = t.nBCSVM_PileUpEnvelopeUp
                        mytree.variables['nBCSVM_SubTotalPileUp_Up'][0] = t.nBCSVM_SubTotalPileUpUp
                        mytree.variables['nBCSVM_SubTotalRelative_Up'][0] = t.nBCSVM_SubTotalRelativeUp
                        mytree.variables['nBCSVM_SubTotalPt_Up'][0] = t.nBCSVM_SubTotalPtUp
                        mytree.variables['nBCSVM_SubTotalScale_Up'][0] = t.nBCSVM_SubTotalScaleUp
                        mytree.variables['nBCSVM_SubTotalAbsolute_Up'][0] = t.nBCSVM_SubTotalAbsoluteUp
                        mytree.variables['nBCSVM_SubTotalMC_Up'][0] = t.nBCSVM_SubTotalMCUp
                        mytree.variables['nBCSVM_Total_Up'][0] = t.nBCSVM_TotalUp
                        mytree.variables['nBCSVM_TotalNoFlavor_Up'][0] = t.nBCSVM_TotalNoFlavorUp
                        mytree.variables['nBCSVM_TotalNoTime_Up'][0] = t.nBCSVM_TotalNoTimeUp
                        mytree.variables['nBCSVM_TotalNoFlavorNoTime_Up'][0] = t.nBCSVM_TotalNoFlavorNoTimeUp
                        mytree.variables['nBCSVM_FlavorZJet_Up'][0] = t.nBCSVM_FlavorZJetUp
                        mytree.variables['nBCSVM_FlavorPhotonJet_Up'][0] = t.nBCSVM_FlavorPhotonJetUp
                        mytree.variables['nBCSVM_FlavorPureGluon_Up'][0] = t.nBCSVM_FlavorPureGluonUp
                        mytree.variables['nBCSVM_FlavorPureQuark_Up'][0] = t.nBCSVM_FlavorPureQuarkUp
                        mytree.variables['nBCSVM_FlavorPureCharm_Up'][0] = t.nBCSVM_FlavorPureCharmUp
                        mytree.variables['nBCSVM_FlavorPureBottom_Up'][0] = t.nBCSVM_FlavorPureBottomUp
                        mytree.variables['nBCSVM_TimeRunBCD_Up'][0] = t.nBCSVM_TimeRunBCDUp
                        mytree.variables['nBCSVM_TimeRunEF_Up'][0] = t.nBCSVM_TimeRunEFUp
                        mytree.variables['nBCSVM_TimeRunG_Up'][0] = t.nBCSVM_TimeRunGUp
                        mytree.variables['nBCSVM_TimeRunH_Up'][0] = t.nBCSVM_TimeRunHUp
                        mytree.variables['nBCSVM_CorrelationGroupMPFInSitu_Up'][0] = t.nBCSVM_CorrelationGroupMPFInSituUp
                        mytree.variables['nBCSVM_CorrelationGroupIntercalibration_Up'][0] = t.nBCSVM_CorrelationGroupIntercalibrationUp
                        mytree.variables['nBCSVM_CorrelationGroupbJES_Up'][0] = t.nBCSVM_CorrelationGroupbJESUp
                        mytree.variables['nBCSVM_CorrelationGroupFlavor_Up'][0] = t.nBCSVM_CorrelationGroupFlavorUp
                        mytree.variables['nBCSVM_CorrelationGroupUncorrelated_Up'][0] = t.nBCSVM_CorrelationGroupUncorrelatedUp
                        mytree.variables['nBCSVM_JER_Up'][0] = t.nBCSVM_JERUp

                  
                        mytree.variables['nBCSVM_AbsoluteStat_Down'][0] = t.nBCSVM_AbsoluteStatUp
                        mytree.variables['nBCSVM_AbsoluteScale_Down'][0] = t.nBCSVM_AbsoluteScaleUp
                        mytree.variables['nBCSVM_AbsoluteFlavMap_Down'][0] = t.nBCSVM_AbsoluteFlavMapUp
                        mytree.variables['nBCSVM_AbsoluteMPFBias_Down'][0] = t.nBCSVM_AbsoluteMPFBiasUp
                        mytree.variables['nBCSVM_Fragmentation_Down'][0] = t.nBCSVM_FragmentationUp
                        mytree.variables['nBCSVM_SinglePionECAL_Down'][0] = t.nBCSVM_SinglePionECALUp
                        mytree.variables['nBCSVM_SinglePionHCAL_Down'][0] = t.nBCSVM_SinglePionHCALUp
                        mytree.variables['nBCSVM_FlavorQCD_Down'][0] = t.nBCSVM_FlavorQCDUp
                        mytree.variables['nBCSVM_TimePtEta_Down'][0] = t.nBCSVM_TimePtEtaUp
                        mytree.variables['nBCSVM_RelativeJEREC1_Down'][0] = t.nBCSVM_RelativeJEREC1Up
                        mytree.variables['nBCSVM_RelativeJEREC2_Down'][0] = t.nBCSVM_RelativeJEREC2Up
                        mytree.variables['nBCSVM_RelativeJERHF_Down'][0] = t.nBCSVM_RelativeJERHFUp
                        mytree.variables['nBCSVM_RelativePtBB_Down'][0] = t.nBCSVM_RelativePtBBUp
                        mytree.variables['nBCSVM_RelativePtEC1_Down'][0] = t.nBCSVM_RelativePtEC1Up
                        mytree.variables['nBCSVM_RelativePtEC2_Down'][0] = t.nBCSVM_RelativePtEC2Up
                        mytree.variables['nBCSVM_RelativePtHF_Down'][0] = t.nBCSVM_RelativePtHFUp
                        mytree.variables['nBCSVM_RelativeBal_Down'][0] = t.nBCSVM_RelativeBalUp
                        mytree.variables['nBCSVM_RelativeFSR_Down'][0] = t.nBCSVM_RelativeFSRUp
                        mytree.variables['nBCSVM_RelativeStatFSR_Down'][0] = t.nBCSVM_RelativeStatFSRUp
                        mytree.variables['nBCSVM_RelativeStatEC_Down'][0] = t.nBCSVM_RelativeStatECUp
                        mytree.variables['nBCSVM_RelativeStatHF_Down'][0] = t.nBCSVM_RelativeStatHFUp
                        mytree.variables['nBCSVM_PileUpDataMC_Down'][0] = t.nBCSVM_PileUpDataMCUp
                        mytree.variables['nBCSVM_PileUpPtRef_Down'][0] = t.nBCSVM_PileUpPtRefUp
                        mytree.variables['nBCSVM_PileUpPtBB_Down'][0] = t.nBCSVM_PileUpPtBBUp
                        mytree.variables['nBCSVM_PileUpPtEC1_Down'][0] = t.nBCSVM_PileUpPtEC1Up
                        mytree.variables['nBCSVM_PileUpPtEC2_Down'][0] = t.nBCSVM_PileUpPtEC2Up
                        mytree.variables['nBCSVM_PileUpPtHF_Down'][0] = t.nBCSVM_PileUpPtHFUp
                        mytree.variables['nBCSVM_PileUpMuZero_Down'][0] = t.nBCSVM_PileUpMuZeroUp
                        mytree.variables['nBCSVM_PileUpEnvelope_Down'][0] = t.nBCSVM_PileUpEnvelopeUp
                        mytree.variables['nBCSVM_SubTotalPileUp_Down'][0] = t.nBCSVM_SubTotalPileUpUp
                        mytree.variables['nBCSVM_SubTotalRelative_Down'][0] = t.nBCSVM_SubTotalRelativeUp
                        mytree.variables['nBCSVM_SubTotalPt_Down'][0] = t.nBCSVM_SubTotalPtUp
                        mytree.variables['nBCSVM_SubTotalScale_Down'][0] = t.nBCSVM_SubTotalScaleUp
                        mytree.variables['nBCSVM_SubTotalAbsolute_Down'][0] = t.nBCSVM_SubTotalAbsoluteUp
                        mytree.variables['nBCSVM_SubTotalMC_Down'][0] = t.nBCSVM_SubTotalMCUp
                        mytree.variables['nBCSVM_Total_Down'][0] = t.nBCSVM_TotalUp
                        mytree.variables['nBCSVM_TotalNoFlavor_Down'][0] = t.nBCSVM_TotalNoFlavorUp
                        mytree.variables['nBCSVM_TotalNoTime_Down'][0] = t.nBCSVM_TotalNoTimeUp
                        mytree.variables['nBCSVM_TotalNoFlavorNoTime_Down'][0] = t.nBCSVM_TotalNoFlavorNoTimeUp
                        mytree.variables['nBCSVM_FlavorZJet_Down'][0] = t.nBCSVM_FlavorZJetUp
                        mytree.variables['nBCSVM_FlavorPhotonJet_Down'][0] = t.nBCSVM_FlavorPhotonJetUp
                        mytree.variables['nBCSVM_FlavorPureGluon_Down'][0] = t.nBCSVM_FlavorPureGluonUp
                        mytree.variables['nBCSVM_FlavorPureQuark_Down'][0] = t.nBCSVM_FlavorPureQuarkUp
                        mytree.variables['nBCSVM_FlavorPureCharm_Down'][0] = t.nBCSVM_FlavorPureCharmUp
                        mytree.variables['nBCSVM_FlavorPureBottom_Down'][0] = t.nBCSVM_FlavorPureBottomUp
                        mytree.variables['nBCSVM_TimeRunBCD_Down'][0] = t.nBCSVM_TimeRunBCDUp
                        mytree.variables['nBCSVM_TimeRunEF_Down'][0] = t.nBCSVM_TimeRunEFUp
                        mytree.variables['nBCSVM_TimeRunG_Down'][0] = t.nBCSVM_TimeRunGUp
                        mytree.variables['nBCSVM_TimeRunH_Down'][0] = t.nBCSVM_TimeRunHUp
                        mytree.variables['nBCSVM_CorrelationGroupMPFInSitu_Down'][0] = t.nBCSVM_CorrelationGroupMPFInSituUp
                        mytree.variables['nBCSVM_CorrelationGroupIntercalibration_Down'][0] = t.nBCSVM_CorrelationGroupIntercalibrationUp
                        mytree.variables['nBCSVM_CorrelationGroupbJES_Down'][0] = t.nBCSVM_CorrelationGroupbJESUp
                        mytree.variables['nBCSVM_CorrelationGroupFlavor_Down'][0] = t.nBCSVM_CorrelationGroupFlavorUp
                        mytree.variables['nBCSVM_CorrelationGroupUncorrelated_Down'][0] = t.nBCSVM_CorrelationGroupUncorrelatedUp
                        mytree.variables['nBCSVM_JER_Down'][0] = t.nBCSVM_JERUp


                        #mytree.variables['btagCorr'][0] = np.exp(sum(np.log(btagCorrMC(t.jets_pt,t.jets_eta,t.jets_dRmin,t.jets_btagCSV))*t.jets_btagFlag))
                  else:
                        mytree.variables['weight'][0] = 1
                        #mytree.variables['btagCorr'][0] = np.exp(sum(np.log(btagCorrData(t.jets_pt,t.jets_eta,t.jets_dRmin,t.jets_btagCSV))*t.jets_btagFlag))

#                  hPass.SetBinContent(2,hPass.GetBinContent(2)+1)
                  
                  ntopjets = ntoptaggedjets= 0
                  nbjets = 0
                  nljets = 0
                  allp = ROOT.TLorentzVector()
                  ptD = LHA=width=mass=0
                  for i in range(0,t.njets):
                        je = ROOT.TLorentzVector()
                        je.SetPtEtaPhiM(t.jets_pt[i],t.jets_eta[i],t.jets_phi[i],t.jets_mass[i])
                        allp+=je
                  #       for ii in range(i,t.njets):
                  #             if ii == i: continue
                  #             je2 = ROOT.TLorentzVector()
                  #             je2.SetPtEtaPhiM(t.jets_pt[ii],t.jets_eta[ii],t.jets_phi[ii],t.jets_mass[ii])
                                    
                  #             ptR+=je.Pt()*je2.Pt()*(je.DeltaR(je2))**0.2
                  for i in range(0,t.njets):#find the b-tagged jets
                        #ptD+=(t.jets_pt[i]/t.ht)**2
                        jet = ROOT.TLorentzVector()
                        jet.SetPtEtaPhiM(t.jets_pt[i],t.jets_eta[i],t.jets_phi[i],t.jets_mass[i])

                        # LHA+=(t.jets_pt[i]/t.ht)*(jet.DeltaR(allp)/max(t.jets_dRmax))**0.5
                        # width+=(t.jets_pt[i]/t.ht)*(jet.DeltaR(allp)/max(t.jets_dRmax))
                        mass+=(t.jets_pt[i]/t.ht)*(jet.DeltaR(allp)/max(t.jets_dRmax))**2
                        jets_.push_back(jet)
                        if sample !='data':
                              if abs(t.jets_mcMatchId[i]) == 6:
                                    if abs(t.jets_mcFlavour[i]) == 5 and t.jets_matchFlag[i] == 1 : corrb_.append(i)
                                    elif t.jets_matchFlag[i] == 0: corrlight_.append(i)
                        if t.jets_btagCSV[i] >= btagcsvm:
                            bpos_.append(i)
                            nbjets +=1
                            if sample !='data' and  abs(t.jets_mcMatchId[i]) == 6: ntopjets += 1

                        else: 
                            nljets+=1
                            jetpos_.append(i)
                            if sample !='data' and abs(t.jets_mcMatchId[i]) == 6:ntopjets += 1

                  # if sample !='data' and t.ngenTopLep >0:
                  #       for toplep in range(t.ngenTopLep):
                  #             mytree.variables['genTopLep_pt'][toplep] = t.genTopLep_pt[toplep]
                  #             mytree.variables['n_genTopLep'][0] = t.ngenTopLep
                  #             mytree.variables['has_Lep'][0] =1
                  # else: mytree.variables['has_Lep'][0] =0
                  
                  
                        
                  bdtcomb  =  -999999999
                  chi2comb    =  999999999
                  mytree.variables['ptD'][0] = ptD
                  mytree.variables['LHA'][0] = LHA
                  mytree.variables['width'][0] = width
                  mytree.variables['mass'][0] = mass
                  mytree.variables['nPVs'][0] = t.nPVs
                  mytree.variables['sphericity'][0] = t.sphericity
                  mytree.variables['minjetpt'][0] = t.jets_pt[t.njets-1]
                  
                  mytree.variables['jets_dRavg'][0] = sum(t.jets_dRave)/t.njets
                  mytree.variables['jets_dRmin'][0] = min(x for x in t.jets_dRmin if x > 0)
                  mytree.variables['jets_dRmax'][0] = max(t.jets_dRmax)
                  if sample == 'QCD':mytree.variables['isQCD'][0] = 1
                  else: mytree.variables['isQCD'][0] = 0
                  
                  mytree.variables['girth'][0] = ptR/(t.ht)**2
                  if sample not in ['data','QCD']: mytree.variables['ttCls'][0] = t.ttCls
                  else: mytree.variables['ttCls'][0] = -1
                  mytree.variables['ht'][0] = t.ht
                  mytree.variables['all_mass'][0] = t.invmass
                  mytree.variables['closest_mass'][0] = t.mjjmin
                  mytree.variables['jet5pt'][0] = t.jets_pt[5]
                  mytree.variables['n_jets'][0] = nljets + nbjets
                  mytree.variables['n_bjets'][0] = nbjets
                  mytree.variables['n_addJets'][0] = nljets + nbjets - 6
                  mytree.variables['n_topjets'][0] = ntopjets
                  mytree.variables['qgLR'][0] = -100
                  mytree.variables['centrality'][0] = t.centrality
                  mytree.variables['aplanarity'][0] = t.aplanarity
                  mytree.variables['meanDeltaRbtag'][0] = t.mean_dr_btag
                  mytree.variables['meanCSVbtag'][0]=t.mean_bdisc
                  mytree.variables['meanCSV'][0]=t.mean_bdisc_btag
                  mytree.variables['btagLR3b'][0] = t.btag_LR_3b_2b_btagCSV
                  mytree.variables['btagLR4b'][0] = t.btag_LR_4b_2b_btagCSV
                  mytree.variables['nBCSVM'][0] = t.nBCSVM
                  

                       

                  qgLR3b = t.qg_LR_3b_flavour_5q_0q
                  qgLR4b = t.qg_LR_4b_flavour_5q_0q
                        
#                  mytree.variables['memttbb'][0]  = max(t.mem_ttbb_FH_4w2h1t_p/(t.mem_tth_FH_4w2h1t_p) if t.mem_tth_FH_4w2h1t_p > 0 else -10,t.mem_ttbb_FH_4w2h2t_p/(t.mem_tth_FH_4w2h2t_p) if t.mem_tth_FH_4w2h2t_p > 0 else -10)

                  if nbjets == 3:
                        mytree.variables['qgLR'][0] = qgLR3b
                        if t.mem_ttbb_FH_4w2h1t_p  > 0: mytree.variables['memttbb'][0] = -TMath.Log10(t.mem_ttbb_FH_4w2h1t_p)
                        else: mytree.variables['memttbb'][0] = -10
                        #print mytree.variables['memttbb'][0]
                        # if nljets == 4:
                        #       mytree.variables['qgLR'][0] = t.qg_LR_3b_flavour_4q_0q
                        # elif nljets >= 5:
                        #       mytree.variables['qgLR'][0] = t.qg_LR_3b_flavour_5q_0q
                  if nbjets >= 4:
                        mytree.variables['qgLR'][0] = qgLR4b
                        if t.mem_ttbb_FH_4w2h2t_p  > 0: mytree.variables['memttbb'][0] = -TMath.Log10(t.mem_ttbb_FH_4w2h2t_p)
                        else: mytree.variables['memttbb'][0] = -10
                        #print mytree.variables['memttbb'][0]
                        # if nljets == 4: mytree.variables['qgLR'][0] = t.qg_LR_4b_flavour_4q_0q
                        # elif nljets >= 5: mytree.variables['qgLR'][0] = t.qg_LR_4b_flavour_5q_0q
                  else:
                        mytree.variables['memttbb'][0] = -TMath.Log10(t.mem_ttbb_FH_4w2h1t_p) if t.mem_ttbb_FH_4w2h1t_p >0 else -10
                        mytree.variables['qgLR'][0] = qgLR3b
                        
                            


#                  print t.njets, ' njets ',nbjets, ' nbjets ', ' bpos ', bpos_
                  alljets = range(t.njets)
                  if len(corrb_) == 2 and len(corrlight_) == 4:
                        mytree.variables['existCorrect'][0] = 1
                        corrcomb_ = JetComb(4,2,corrlight_,corrb_)
                  else:mytree.variables['existCorrect'][0] = 0
                  mytree.variables['hasbCorrect'][0] = 0
                  if (nljets >=4 ):
                        comb_ = JetComb(nljets,nbjets,jetpos_,bpos_)
                        mytree.variables['has4light'][0] = 1
                        for comb in comb_:
                              if comb in corrcomb_:mytree.variables['hasbCorrect'][0] = 1
                  else:
                        comb_ = []
                        mytree.variables['has4light'][0] = 0

                  if str(t.njets) not in allcomb_:
                        allcomb_[str(t.njets)] = JetComb(nljets+nbjets,0,alljets)

                  mytree.variables['hasCorrect'][0] = 0
                  BDT_classes = [0,0,0]
                  printing = 0
                  highest = 0
                  bestcat = 0
                  #print comb_, 'comb_'
                  meanBDTttbar=sumprob = 0
                  maxbdt = 0
                  for i in range(len(allcomb_[str(t.njets)])):
                        #if i > 2521: continue
                        UpdateVariables(allcomb_[str(t.njets)][i],jets_,mytree.variables,MVA_Only)
                        
                        if mytree.variables['prob_chi2'][0] < probcut: continue
                                                
                        BDT_Value = reader.EvaluateMVA("BDT_Comb")
                        if allcomb_[str(t.njets)][i] in corrcomb_ :
                              mytree.variables['hasCorrect'][0] = 1
                        
                              #print e,BDT_Value,'correct', comb_[i], prob_chi2'][0]
                              #printing = 1

                              
                        # for cl in range(3):
                        #       if mytree.variables['n_jets'][0] == 7:
                        #             mycat = reader_Class1ad.EvaluateMulticlass("BDT_Class1ad")[cl]
                        #             if mycat > highest:
                        #                   highest = mycat
                        #                   bestcat = cl
                              
                        #       else:
                        #             mycat = reader_Class2ad.EvaluateMulticlass("BDT_Class2ad")[cl]
                        #             if mycat > highest:
                        #                   highest = mycat
                        #                   bestcat = cl
                                    
                        #BDT_classes[bestcat] += 1


                        if mytree.variables['simple_chi2'][0] < chi2comb:
                              chi2comb = mytree.variables['simple_chi2'][0]
                              if  allcomb_[str(t.njets)][i] in corrcomb_ :mytree.variables['chi2Correct'][0] = 1
                              else: mytree.variables['chi2Correct'][0] = 0
                        # print '###################################################'
                        # for var in usevar:
                        #       if var in mytree.variables:
                        #             print var, mytree.variables[var]
                        #       else:
                        #             print var,MVA_Only[var]
                        # print BDT_Value
                        # print '###################################################'
                        if BDT_Value > bdtcomb:
                              mytree.variables['BDT_Comb'][0] = BDT_Value
                              bdtcomb = BDT_Value
                              bestcomb_=allcomb_[str(t.njets)][i]
                              #if printing:
                                    #print e, BDT_Value,'highest', bestcomb_, mytree.variables['prob_chi2'][0]
                              if  bestcomb_ in corrcomb_ : mytree.variables['isCorrect'][0] = 1
                              else: mytree.variables['isCorrect'][0] = 0
                              if sample !='data': 
                                    mytree.variables['n_sumIDtop'][0] = t.jets_mcMatchId[allcomb_[str(t.njets)][i][0]]
                                    mytree.variables['n_sumIDtop'][1] = t.jets_mcMatchId[allcomb_[str(t.njets)][i][2]]
                                    mytree.variables['n_sumIDtop'][2] = t.jets_mcMatchId[allcomb_[str(t.njets)][i][3]]
                                    mytree.variables['n_sumIDtop'][3] = t.jets_mcMatchId[allcomb_[str(t.njets)][i][1]]
                                    mytree.variables['n_sumIDtop'][4] = t.jets_mcMatchId[allcomb_[str(t.njets)][i][4]]
                                    mytree.variables['n_sumIDtop'][5] = t.jets_mcMatchId[allcomb_[str(t.njets)][i][5]]

                  if len(bestcomb_) == 0: continue
                  ninternb = 0
                  for ii in bestcomb_:
                        if t.jets_btagCSV[ii]>=btagcsvm:ninternb+=1
                  # mytree.variables['BDT_ClassMajo'][BDT_classes.index(max(BDT_classes))] = 1
                  mytree.variables['BDT_ttbarMajo'][0] = meanBDTttbar/sumprob if sumprob>0 else meanBDTttbar/len(allcomb_[str(t.njets)])
                  UpdateVariables(bestcomb_,jets_,mytree.variables,MVA_Only)
                  mytree.variables['n_addbjets'][0] = nbjets - ninternb
                  # print '###################################################'
                  # for var in usevar:
                  #       if var in mytree.variables:
                  #             print var, mytree.variables[var]
                  #       else:
                  #             print var,MVA_Only[var]
                  # print mytree.variables['BDT_Comb'][0], reader.EvaluateMVA("BDT_Comb")
                  # print '###################################################'
                  
                  #mytree.variables['BDT_QCD'][0] = readerQCD.EvaluateMVA("BDT_QCD")
                  #mytree.variables['BDT_QCDData'][0] = readerQCDData.EvaluateMVA("BDT_QCDData")
                  # mytree.variables['BDT_QCDCWoLa'][0] = readerQCDCWoLa.EvaluateMVA("BDT_QCDCWoLa")
                  # mytree.variables['BDT_QCDCWoLa2'][0] = readerQCDCWoLa2.EvaluateMVA("BDT_QCDCWoLa2")
                  # mytree.variables['Fish_QCDCWoLa'][0] = readerQCDCWoLa.EvaluateMVA("Fish_QCDCWoLa")
                  # mytree.variables['BDT_ttbar'][0] = reader_Class.EvaluateMVA("BDT_Class")
                  # mytree.variables['BDT_ttbarMax'][0] = maxbdt
                  # if sample !='data': 
                  #       for b in range(nbjets -2):
                  #             mytree.variables['addB_MCid'][b] = t.jets_mcFlavour[bpos_[b+2]]
                  #             mytree.variables['addB_TopMCmatch'][b] = t.jets_mcMatchId[bpos_[b+2]]
                  #             mytree.variables['addB_TopMCmatch'][b] = t.jets_mcMatchId[bpos_[b+2]]

                  lq1.UpdateParam(jets_[bestcomb_[2]])
                  lq2.UpdateParam(jets_[bestcomb_[3]])
                  lp1.UpdateParam(jets_[bestcomb_[4]])
                  lp2.UpdateParam(jets_[bestcomb_[5]])
                  b1.UpdateParam(jets_[bestcomb_[0]])
                  b2.UpdateParam(jets_[bestcomb_[1]])
                  if b1.pt[0] < lq2.pt[0]:
                        mytree.variables['soft_eta1'][0] = abs(b1.eta[0]) - abs(lq1.eta[0]-lq2.eta[0])
                  else:
                        mytree.variables['soft_eta1'][0] = abs(lq2.eta[0]) - abs(lq1.eta[0]-b1.eta[0])
                  if b2.pt[0] < lp2.pt[0]:
                        mytree.variables['soft_eta2'][0] = abs(b2.eta[0]) - abs(lp1.eta[0]-lp2.eta[0])
                  else:
                        mytree.variables['soft_eta2'][0] = abs(lp2.eta[0]) - abs(lp1.eta[0]-b2.eta[0])

                  # if sample !='data':
                  #       #print 'bestcomb',bestcomb_, 'jets', jets_ 
                  #       b1.UpdateParam(jets_[bestcomb_[0]],t.jets_mcFlavour[bestcomb_[0]],t.jets_mcMatchId[bestcomb_[0]])
                  # else : 
                  #print 'flavours: ', t.jets_mcFlavour[bestcomb_[0]],t.jets_mcMatchId[bestcomb_[0]]
                  # if sample !='data': b2.UpdateParam(jets_[bestcomb_[1]],t.jets_mcFlavour[bestcomb_[1]],t.jets_mcMatchId[bestcomb_[1]])
                  # else : b2.UpdateParam(jets_[bestcomb_[1]])
                  w1.UpdateParam(jets_[bestcomb_[2]]+jets_[bestcomb_[3]])
                  top1.UpdateParam(jets_[bestcomb_[0]]+jets_[bestcomb_[3]]+jets_[bestcomb_[2]])
                  w2.UpdateParam(jets_[bestcomb_[5]]+jets_[bestcomb_[4]])
                  top2.UpdateParam(jets_[bestcomb_[1]]+jets_[bestcomb_[4]]+jets_[bestcomb_[5]])
                  tt.UpdateParam(jets_[bestcomb_[0]]+jets_[bestcomb_[1]]+jets_[bestcomb_[2]]+jets_[bestcomb_[3]]+jets_[bestcomb_[4]]+jets_[bestcomb_[5]])


                  
                  if sample == 'ttbar':
                        for itophad in range(t.ngenTopHad):
                              mytree.variables['genTopHad_pt'][itophad] = t.genTopHad_pt[itophad]
                        mytree.variables['topweight'][0] = np.exp(0.5*(t.ngenTopLep*0.0843616-0.000743051*np.sum(t.genTopLep_pt)+t.ngenTopHad*0.0843616-0.000743051*np.sum(t.genTopHad_pt)))*(t.jets_pt[0]/t.jets_pt[0])
                        mytree.variables['topweight_Up'][0] = np.exp(0.5*(t.ngenTopLep*0.00160296-0.000411375*sum(t.genTopLep_pt)+t.ngenTopHad*0.00160296- 0.000411375*sum(t.genTopHad_pt)))
                        mytree.variables['topweight_Down'][0] = np.exp(0.5*(t.ngenTopLep*0.16712-0.00107473*sum(t.genTopLep_pt)+t.ngenTopHad*0.16712-0.00107473*sum(t.genTopHad_pt)))

                        
                  highest = 0
                  bestcat = 0
                  # print '###################################################'
                  # for var in usevarQCDCWoLa:
                  #       if var in mytree.variables:
                  #             print var, mytree.variables[var][0]
                  #       else:
                  #             print var, MVA_Only[var][0]
                  # print 'BDT_CWoLa2', mytree.variables['BDT_QCDCWoLa2'][0]
                  # print 'BDT_CWoLa',mytree.variables['BDT_QCDCWoLa'][0]
                  # print '###################################################'
                  # for i in range(3):
                  #       if mytree.variables['n_jets'][0] == 7:
                  #             mycat = reader_Class1ad.EvaluateMulticlass("BDT_Class1ad")[i]
                  #             if mycat > highest:
                  #                   highest = mycat
                  #                   bestcat = i
                              
                  #       else:
                  #             mycat = reader_Class2ad.EvaluateMulticlass("BDT_Class2ad")[i]
                  #             if mycat > highest:
                  #                   highest = mycat
                  #                   bestcat = i
                  # mytree.variables['BDT_Class'][bestcat] = 1
                  #print 'ttcls: ',mytree.variables['ttCls'][0], ' bdt_class: ',BDT_Class, ' bdtmajor: ',BDT_ClassMajo, ' bdtmax: ',mytree.variables['BDT_ttbarMax'][0]
                  mytree.variables['BDTQGL'][0] = readerQGL.EvaluateMVA("BDT_QGL")
                  mytree.variables['BDTMisc'][0] = readerMisc.EvaluateMVA("BDT_Misc")
                  tkin.Fill()
                  
                  mytree.ZeroArray()
                  
            if e > emax: break

      watch.Print()
      tkin.Write()
      fout.Write()
      fout.Close()

