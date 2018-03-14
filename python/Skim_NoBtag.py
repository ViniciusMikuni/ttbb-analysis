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
      var['simple_chi2'][0] = pow(((jet[comb[0]] + jet[comb[2]]+ jet[comb[3]]).M() - 173.4)/20.0,2) + pow(((jet[comb[1]] + jet[comb[4]]+ jet[comb[5]]).M() - 173.4)/20.0,2) + pow(((jet[comb[2]]+ jet[comb[3]]).M() - 83.1)/16.5,2) + pow(((jet[comb[5]]+ jet[comb[4]]).M() - 83.1)/16.5,2)
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
      #readerQCD = TMVA.Reader( "!Color:!Silent" )
      #readerQCDData = TMVA.Reader( "!Color:!Silent" )
      #readerQCDCWoLa = TMVA.Reader( "!Color:!Silent" )
      #readerQCDCWoLa2 = TMVA.Reader( "!Color:!Silent" )
      #reader_Class1ad = TMVA.Reader( "!Color:!Silent" )
      #reader_Class2ad = TMVA.Reader( "!Color:!Silent" )
      #reader_Class = TMVA.Reader( "!Color:!Silent" )
      mytree = ManageTTree(tvars,tkin)

      usevar = ['top1_m','top2_m','w1_m','w2_m','b1_pt','b2_pt','deltaRl1l2','deltaRq1q2','deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhil1l2','deltaPhiq1q2','deltaPhib1b2','deltaPhiw1w2','deltaPhit1t2','q1b1_mass','p1b2_mass','deltaRb1q1','deltaRb2p1','deltaRb1top2','deltaRb2top1','deltaRb1w2','deltaRb2w1','mindeltaRb1q','simple_chi2','mindeltaRb2p', 'deltaEtal1l2', 'deltaEtaq1q2', 'deltaEtab1b2', 'deltaEtaw1w2', 'deltaEtat1t2','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']

      # usevarQCD = ['jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','qgLR']

      # usevarQCDCWoLa = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']

      # usevarQCDCWoLa2 = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','BDT_Comb','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass']
      
      #usevarQCDData = ['top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jets_dRmax','jets_dRavg','all_mass','closest_mass','BDT_Comb']
      
      # usevar1add = ['deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','deltaPhiaddb1','deltaPhiaddb2','deltaPhiaddw1','deltaPhiaddw2','deltaPhiaddtop1','deltaPhiaddtop2','deltaEtaaddb1','deltaEtaaddb2','deltaEtaaddw1','deltaEtaaddw2','deltaEtaaddtop1','deltaEtaaddtop2','addJet_CSV[0]','addJet_pt[0]','ht','btagLR4b','btagLR3b','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','tt_pt']
      # usevar2add = usevar1add + ['addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass']

      # useall = usevar2add + ['n_jets']
      

      for var in usevar:
            if var in mytree.variables:reader.AddVariable(var,mytree.variables[var])
            else:reader.AddVariable(var,MVA_Only[var])
      # for var in usevarQCD:
      #       if var in mytree.variables:readerQCD.AddVariable(var,mytree.variables[var])
      #       else:readerQCD.AddVariable(var,MVA_Only[var])

      # for var in usevarQCDData:
      #       if var in mytree.variables:readerQCDData.AddVariable(var,mytree.variables[var])
      #       else:readerQCDData.AddVariable(var,MVA_Only[var])
      # for var in usevarQCDCWoLa:
      #       if var in mytree.variables:readerQCDCWoLa.AddVariable(var,mytree.variables[var])
      #       else:readerQCDCWoLa.AddVariable(var,MVA_Only[var])
      # for var in usevarQCDCWoLa2:
      #       if var in mytree.variables:readerQCDCWoLa2.AddVariable(var,mytree.variables[var])
      #       else:readerQCDCWoLa2.AddVariable(var,MVA_Only[var])
      # for var in usevar1add:
      #       if var in mytree.variables:reader_Class1ad.AddVariable(var,mytree.variables[var])
      #       else:reader_Class1ad.AddVariable(var,MVA_Only[var])
      # for var in usevar2add:
      #       if var in mytree.variables:reader_Class2ad.AddVariable(var,mytree.variables[var])
      #       else:reader_Class2ad.AddVariable(var,MVA_Only[var])
      # for var in useall:
      #       if var in mytree.variables:reader_Class.AddVariable(var,mytree.variables[var])
      #       else:reader_Class.AddVariable(var,MVA_Only[var])            



      weightFileBDT_Comb = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDT_comb.weights.xml'
      #weightFileBDT_QCD = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDT_QCD.weights.xml'
      #weightFileBDT_QCDData = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDT_Data.weights.xml'
      # weightFileBDT_Class1ad = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDTmulti_Cat1add.weights.xml'
      # weightFileBDT_Class2ad = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDTmulti_Cat2add.weights.xml'
      # weightFileBDT_Class = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDTttbarCat.weights.xml'
      # weightFileBDT_CWoLa = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDT_QCD_CWoLa.weights.xml'
      # weightFileBDT_CWoLa2 = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDT_QCD_CWoLa_Diff.weights.xml'
      # weightFileFish_CWoLa = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_Fish_QCD_CWoLa.weights.xml'
      
      reader.BookMVA('BDT_Comb',weightFileBDT_Comb)
      # readerQCDCWoLa.BookMVA('BDT_QCDCWoLa',weightFileBDT_CWoLa)
      # readerQCDCWoLa2.BookMVA('BDT_QCDCWoLa2',weightFileBDT_CWoLa2)
      # readerQCDCWoLa.BookMVA('Fish_QCDCWoLa',weightFileFish_CWoLa)
      # readerQCD.BookMVA('BDT_QCD',weightFileBDT_QCD)
      #readerQCDData.BookMVA('BDT_QCDData',weightFileBDT_QCDData)
      # reader_Class1ad.BookMVA('BDT_Class1ad',weightFileBDT_Class1ad)
      # reader_Class2ad.BookMVA('BDT_Class2ad',weightFileBDT_Class2ad)
      #reader_Class.BookMVA('BDT_Class',weightFileBDT_Class)
      

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
            tthcut = t.json and (t.HLT_ttH_FH or t.HLT_BIT_HLT_PFJet450_v) and t.ht>500 and t.jets_pt[5]>40
#            if t.njets >= 6: hPass.SetBinContent(1,hPass.GetBinContent(1)+1)
            if not tthcut: continue
            if t.njets >= 7 and t.nBCSVM >=2:
                  if sample !='data':
                        mytree.variables['weight'][0] = t.puWeight * t.btagWeightCSV * np.sign(t.genWeight)
                        #mytree.variables['btagCorr'][0] = np.exp(sum(np.log(btagCorrMC(t.jets_pt,t.jets_eta,t.jets_dRmin,t.jets_btagCSV))*t.jets_btagFlag))
                  else:
                        mytree.variables['weight'][0] = 1
                        #mytree.variables['btagCorr'][0] = np.exp(sum(np.log(btagCorrData(t.jets_pt,t.jets_eta,t.jets_dRmin,t.jets_btagCSV))*t.jets_btagFlag))
                  mytree.variables['qgWeight'][0] = t.qgWeight if sample != 'data' else 1.0
#                  hPass.SetBinContent(2,hPass.GetBinContent(2)+1)
                  
                  ntopjets = ntoptaggedjets= 0
                  nbjets = 0
                  nljets = 0
                  
                  for i in range(0,t.njets):#find the b-tagged jets
                        ptR+=t.jets_pt[i]*(t.jets_phi[i]**2 + t.jets_eta[i]**2)**0.5
                        jet = ROOT.TLorentzVector()
                        jet.SetPtEtaPhiM(t.jets_pt[i],t.jets_eta[i],t.jets_phi[i],t.jets_mass[i])
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
                  mytree.variables['jets_dRavg'][0] = sum(t.jets_dRave)/t.njets
                  mytree.variables['jets_dRmin'][0] = min(x for x in t.jets_dRmin if x > 0)
                  mytree.variables['jets_dRmax'][0] = max(t.jets_dRmax)
                  if sample == 'QCD':mytree.variables['isQCD'][0] = 1
                  else: mytree.variables['isQCD'][0] = 0
                  
                  mytree.variables['girth'][0] = ptR/t.ht
                  if sample not in ['data','QCD']: mytree.variables['ttCls'][0] = t.ttCls
                  else: mytree.variables['ttCls'][0] = -1
                  mytree.variables['ht'][0] = t.ht
                  mytree.variables['all_mass'][0] = t.invmass
                  mytree.variables['closest_mass'][0] = t.mjjmin
                  mytree.variables['jet5pt'][0] = t.jets_pt[5]
                  mytree.variables['n_jets'][0] = nljets + nbjets
                  mytree.variables['n_bjets'][0] = nbjets
                  mytree.variables['n_addbjets'][0] = nbjets -2
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

                  qgLR3b = max(t.qg_LR_3b_flavour_4q_0q,t.qg_LR_3b_flavour_5q_0q)
                  qgLR4b = max(t.qg_LR_4b_flavour_4q_0q,t.qg_LR_4b_flavour_5q_0q)
                  

                  mytree.variables['qgLR'][0] = max(qgLR3b,qgLR4b)
#                  mytree.variables['memttbb'][0]  = max(t.mem_ttbb_FH_4w2h1t_p/(t.mem_tth_FH_4w2h1t_p) if t.mem_tth_FH_4w2h1t_p > 0 else -10,t.mem_ttbb_FH_4w2h2t_p/(t.mem_tth_FH_4w2h2t_p) if t.mem_tth_FH_4w2h2t_p > 0 else -10)

                  if nbjets == 3:
                        if (t.mem_ttbb_FH_4w2h1t_p + 0.5* t.mem_tth_FH_4w2h1t_p) > 0: mytree.variables['memttbb'][0] = t.mem_ttbb_FH_4w2h1t_p/(t.mem_ttbb_FH_4w2h1t_p + 0.5* t.mem_tth_FH_4w2h1t_p)
                        else: mytree.variables['memttbb'][0] = -10
                        #print mytree.variables['memttbb'][0]
                        # if nljets == 4:
                        #       mytree.variables['qgLR'][0] = t.qg_LR_3b_flavour_4q_0q
                        # elif nljets >= 5:
                        #       mytree.variables['qgLR'][0] = t.qg_LR_3b_flavour_5q_0q
                  if nbjets >= 4:
                        if (t.mem_ttbb_FH_4w2h2t_p + 0.5* t.mem_tth_FH_4w2h2t_p) > 0: mytree.variables['memttbb'][0] = t.mem_ttbb_FH_4w2h2t_p/(t.mem_ttbb_FH_4w2h2t_p + 0.5* t.mem_tth_FH_4w2h2t_p)
                        else: mytree.variables['memttbb'][0] = -10
                        #print mytree.variables['memttbb'][0]
                        # if nljets == 4: mytree.variables['qgLR'][0] = t.qg_LR_4b_flavour_4q_0q
                        # elif nljets >= 5: mytree.variables['qgLR'][0] = t.qg_LR_4b_flavour_5q_0q
                  else:
                        mytree.variables['memttbb'][0] = max(t.mem_ttbb_FH_4w2h2t_p/(t.mem_ttbb_FH_4w2h2t_p + 0.5*t.mem_tth_FH_4w2h2t_p)if (t.mem_ttbb_FH_4w2h2t_p + 0.5* t.mem_tth_FH_4w2h2t_p) >0 else -10 ,t.mem_ttbb_FH_4w2h1t_p/(t.mem_ttbb_FH_4w2h1t_p + 0.5* t.mem_tth_FH_4w2h1t_p) if (t.mem_ttbb_FH_4w2h1t_p + 0.5*t.mem_tth_FH_4w2h1t_p)>0 else -10) 
                        
                            


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
                  allcomb_ = JetComb(nljets+nbjets,0,alljets)
                  mytree.variables['hasCorrect'][0] = 0
                  BDT_classes = [0,0,0]
                  printing = 0
                  highest = 0
                  bestcat = 0
                  #print comb_, 'comb_'
                  meanBDTttbar=sumprob = 0
                  maxbdt = 0
                  for i in range(len(allcomb_)):
                        #if i > 2521: continue
                        #UpdateVariables(allcomb_[i],jets_,mytree.variables,MVA_Only)
                        mytree.variables['simple_chi2'][0] = pow(((jets_[allcomb_[i][0]] + jets_[allcomb_[i][2]]+ jets_[allcomb_[i][3]]).M() - 173.4)/20.0,2) + pow(((jets_[allcomb_[i][1]] + jets_[allcomb_[i][4]]+ jets_[allcomb_[i][5]]).M() - 173.4)/20.0,2) + pow(((jets_[allcomb_[i][2]]+ jets_[allcomb_[i][3]]).M() - 83.1)/16.5,2) + pow(((jets_[allcomb_[i][5]]+ jets_[allcomb_[i][4]]).M() - 83.1)/16.5,2)
                        mytree.variables['prob_chi2'][0] = TMath.Prob(mytree.variables['simple_chi2'][0],4)
                        if mytree.variables['prob_chi2'][0] < probcut: continue
                        addjets = [x for x in alljets if x not in allcomb_[i]]
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
                              mytree.variables['deltaRaddb1'][0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[allcomb_[i][0]])
                              mytree.variables['deltaRaddb2'][0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[allcomb_[i][1]])
                              mytree.variables['deltaRaddw1'][0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]])
                              mytree.variables['deltaRaddw2'][0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]])
                              mytree.variables['deltaRaddtop1'][0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[allcomb_[i][0]]+jets_[allcomb_[i][2]]+jets_[allcomb_[i][3]])
                              mytree.variables['deltaRaddtop2'][0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[allcomb_[i][1]]+jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]])
                  
                              mytree.variables['deltaPhiaddb1'][0] = jets_[addjets[csvrank[0]]].DeltaPhi(jets_[allcomb_[i][0]])
                              mytree.variables['deltaPhiaddb2'][0] = jets_[addjets[csvrank[0]]].DeltaPhi(jets_[allcomb_[i][1]])
                              mytree.variables['deltaPhiaddw1'][0] = jets_[addjets[csvrank[0]]].DeltaPhi(jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]])
                              mytree.variables['deltaPhiaddw2'][0] = jets_[addjets[csvrank[0]]].DeltaPhi(jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]])
                              mytree.variables['deltaPhiaddtop1'][0] = jets_[addjets[csvrank[0]]].DeltaPhi(jets_[allcomb_[i][0]]+jets_[allcomb_[i][2]]+jets_[allcomb_[i][3]])
                              mytree.variables['deltaPhiaddtop2'][0] = jets_[addjets[csvrank[0]]].DeltaPhi(jets_[allcomb_[i][1]]+jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]])
                              
                              mytree.variables['deltaEtaaddb1'][0] = jets_[addjets[csvrank[0]]].Eta() - jets_[allcomb_[i][0]].Eta()
                              mytree.variables['deltaEtaaddb2'][0] = jets_[addjets[csvrank[0]]].Eta() - jets_[allcomb_[i][1]].Eta()
                              mytree.variables['deltaEtaaddw1'][0] = jets_[addjets[csvrank[0]]].Eta() - (jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).Eta()
                              mytree.variables['deltaEtaaddw2'][0] = jets_[addjets[csvrank[0]]].Eta() - (jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]]).Eta()
                              mytree.variables['deltaEtaaddtop1'][0] = jets_[addjets[csvrank[0]]].Eta() - (jets_[allcomb_[i][0]]+jets_[allcomb_[i][2]]+jets_[allcomb_[i][3]]).Eta()
                              mytree.variables['deltaEtaaddtop2'][0] = jets_[addjets[csvrank[0]]].Eta() - (jets_[allcomb_[i][1]]+jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]]).Eta()
                  
                              if len(csvrank)>=2:
                                    mytree.variables['addJet_deltaR'][0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[addjets[csvrank[1]]])
                                    mytree.variables['addJet_deltaPhi'][0] = jets_[addjets[csvrank[0]]].DeltaPhi(jets_[addjets[csvrank[1]]])
                                    mytree.variables['addJet_deltaEta'][0] = jets_[addjets[csvrank[0]]].Eta() -jets_[addjets[csvrank[1]]].Eta()
                                    mytree.variables['addJet_mass'][0] = (jets_[addjets[csvrank[0]]]+jets_[addjets[csvrank[1]]]).M()
                                    MVA_Only['addJet_CSV[1]'][0] = t.jets_btagCSV[addjets[csvrank[1]]]
                                    MVA_Only['addJet_QGL[1]'][0] = t.jets_qgl[addjets[csvrank[1]]]
                                    MVA_Only['addJet_pt[1]'][0] = t.jets_pt[addjets[csvrank[1]]]
                                    MVA_Only['addJet_eta[1]'][0] = t.jets_eta[addjets[csvrank[1]]]
                                    MVA_Only['addJet_phi[1]'][0] = t.jets_phi[addjets[csvrank[1]]]



                              for ind, rev in enumerate(csvrank):
                                    mytree.variables['addJet_CSV'][ind] = t.jets_btagCSV[addjets[csvrank[rev]]]
                                    mytree.variables['addJet_pt'][ind] = t.jets_pt[addjets[csvrank[rev]]]
                                    mytree.variables['addJet_eta'][ind] = t.jets_eta[addjets[csvrank[rev]]]
                                    mytree.variables['addJet_phi'][ind] = t.jets_phi[addjets[csvrank[rev]]]
                                    mytree.variables['addJet_QGL'][ind] = t.jets_qgl[addjets[csvrank[rev]]]
                        
                        
                              MVA_Only['top1_m'][0] = (jets_[allcomb_[i][0]]+jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).M()
                              MVA_Only['top2_m'][0] = (jets_[allcomb_[i][1]]+jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]]).M()
                              MVA_Only['tt_m'][0] = (jets_[allcomb_[i][1]]+jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]]+jets_[allcomb_[i][0]]+jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).M()
                              MVA_Only['tt_pt'][0] = (jets_[allcomb_[i][1]]+jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]]+jets_[allcomb_[i][0]]+jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).Pt()
                  
                              MVA_Only['w1_m'][0] = (jets_[allcomb_[i][2]]+jets_[allcomb_[i][3]]).M()
                              MVA_Only['w2_m'][0] = (jets_[allcomb_[i][5]]+jets_[allcomb_[i][4]]).M()
                              MVA_Only['top1_pt'][0] = (jets_[allcomb_[i][0]]+jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).Pt()
                              MVA_Only['top2_pt'][0] = (jets_[allcomb_[i][1]]+jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]]).Pt()
                              MVA_Only['w1_pt'][0] = (jets_[allcomb_[i][2]]+jets_[allcomb_[i][3]]).Pt()
                              MVA_Only['w2_pt'][0] = (jets_[allcomb_[i][5]]+jets_[allcomb_[i][4]]).Pt()
                              MVA_Only['b1_pt'][0] = (jets_[allcomb_[i][0]]).Pt()
                              MVA_Only['b2_pt'][0] = (jets_[allcomb_[i][1]]).Pt()
                              mytree.variables['deltaRl1l2'][0] = jets_[allcomb_[i][2]].DeltaR(jets_[allcomb_[i][3]])
                              mytree.variables['deltaPhil1l2'][0] = jets_[allcomb_[i][2]].DeltaPhi(jets_[allcomb_[i][3]])
                              mytree.variables['deltaPhib1b2'][0] = jets_[allcomb_[i][0]].DeltaPhi(jets_[allcomb_[i][1]])

                              mytree.variables['deltaPhiw1w2'][0] = (jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).DeltaPhi((jets_[allcomb_[i][5]]+jets_[allcomb_[i][4]]))
                              mytree.variables['deltaPhit1t2'][0] = (jets_[allcomb_[i][0]]+jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).DeltaPhi((jets_[allcomb_[i][1]]+jets_[allcomb_[i][5]]+jets_[allcomb_[i][4]]))
                              mytree.variables['deltaRq1q2'][0] = jets_[allcomb_[i][4]].DeltaR(jets_[allcomb_[i][5]])
                              mytree.variables['deltaPhiq1q2'][0] = jets_[allcomb_[i][4]].DeltaPhi(jets_[allcomb_[i][5]])
                    
                              mytree.variables['deltaRb1b2'][0] = jets_[allcomb_[i][0]].DeltaR(jets_[allcomb_[i][1]])
                              mytree.variables['deltaRb1w1'][0] = jets_[allcomb_[i][0]].DeltaR(jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]])
                              mytree.variables['deltaRb2w2'][0] = jets_[allcomb_[i][1]].DeltaR(jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]])

                              mytree.variables['deltaEtal1l2'][0] = jets_[allcomb_[i][2]].Eta() - jets_[allcomb_[i][3]].Eta()
                              mytree.variables['deltaEtaq1q2'][0] = jets_[allcomb_[i][4]].Eta() - jets_[allcomb_[i][5]].Eta()
                              mytree.variables['deltaEtab1b2'][0] = jets_[allcomb_[i][0]].Eta() - jets_[allcomb_[i][1]].Eta()
                              mytree.variables['deltaEtaw1w2'][0] = (jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).Eta() - (jets_[allcomb_[i][5]]+jets_[allcomb_[i][4]]).Eta()
                              mytree.variables['deltaEtat1t2'][0] = (jets_[allcomb_[i][0]]+jets_[allcomb_[i][3]]+jets_[allcomb_[i][2]]).Eta() - (jets_[allcomb_[i][1]]+jets_[allcomb_[i][5]]+jets_[allcomb_[i][4]]).Eta()



                              mytree.variables['q1b1_mass'][0] = (jets_[allcomb_[i][0]] + jets_[allcomb_[i][2]]).M()
                              mytree.variables['p1b2_mass'][0] = (jets_[allcomb_[i][1]] + jets_[allcomb_[i][4]]).M()
                              mytree.variables['deltaRb1q1'][0] = jets_[allcomb_[i][0]].DeltaR(jets_[allcomb_[i][2]])
                              mytree.variables['deltaRb2p1'][0] = jets_[allcomb_[i][1]].DeltaR(jets_[allcomb_[i][4]])
                              mytree.variables['deltaRb1top2'][0] = jets_[allcomb_[i][0]].DeltaR(jets_[allcomb_[i][1]]+jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]])
                              mytree.variables['deltaRb2top1'][0] = jets_[allcomb_[i][1]].DeltaR(jets_[allcomb_[i][0]]+jets_[allcomb_[i][2]]+jets_[allcomb_[i][3]])
                              mytree.variables['deltaRb1w2'][0] = jets_[allcomb_[i][0]].DeltaR(jets_[allcomb_[i][4]]+jets_[allcomb_[i][5]])
                              mytree.variables['deltaRb2w1'][0] = jets_[allcomb_[i][1]].DeltaR(jets_[allcomb_[i][2]]+jets_[allcomb_[i][3]])
                              minrb1q = mytree.variables['deltaRb1q1'][0]
                              minrb2p = mytree.variables['deltaRb2p1'][0]
                              if jets_[allcomb_[i][0]].DeltaR(jets_[allcomb_[i][3]]) < minrb1q:
                                    minrb1q = jets_[allcomb_[i][0]].DeltaR(jets_[allcomb_[i][3]])
                              if jets_[allcomb_[i][1]].DeltaR(jets_[allcomb_[i][5]]) < minrb2p:
                                    minrb2p = jets_[allcomb_[i][1]].DeltaR(jets_[allcomb_[i][5]])
                              mytree.variables['mindeltaRb1q'][0] = minrb1q
                              mytree.variables['mindeltaRb2p'][0] = minrb2p
                              for ipos, pos in enumerate(allcomb_[i]):
                                    MVA_Only['jet_CSV['+str(ipos)+']'][0] = t.jets_btagCSV[pos]
                                    mytree.variables['jet_CSV'][ipos] = t.jets_btagCSV[pos]
                                    MVA_Only['jet_QGL['+str(ipos)+']'][0] = t.jets_qgl[pos]
                                    mytree.variables['jet_QGL'][ipos] = t.jets_qgl[pos]


                        
                        #if mytree.variables['prob_chi2'][0] < probcut and sample != 'data': continue
                        
                        BDT_Value = reader.EvaluateMVA("BDT_Comb")
                        #BDT_ClassValue = reader_Class.EvaluateMVA("BDT_Class")
                        #meanBDTttbar+=BDT_ClassValue*mytree.variables['prob_chi2'][0]
                        # if BDT_ClassValue*mytree.variables['prob_chi2'][0]>maxbdt:
                        #       maxbdt = BDT_ClassValue
                        # sumprob+=mytree.variables['prob_chi2'][0]
                        if allcomb_[i] in corrcomb_ :
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
                              if  allcomb_[i] in corrcomb_ :mytree.variables['chi2Correct'][0] = 1
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
                              bestcomb_=allcomb_[i]
                              
                              #if printing:
                                    #print e, BDT_Value,'highest', bestcomb_, mytree.variables['prob_chi2'][0]
                              if  bestcomb_ in corrcomb_ : mytree.variables['isCorrect'][0] = 1
                              else: mytree.variables['isCorrect'][0] = 0
                              if sample !='data': 
                                    mytree.variables['n_sumIDtop'][0] = t.jets_mcMatchId[allcomb_[i][0]]
                                    mytree.variables['n_sumIDtop'][1] = t.jets_mcMatchId[allcomb_[i][2]]
                                    mytree.variables['n_sumIDtop'][2] = t.jets_mcMatchId[allcomb_[i][3]]
                                    mytree.variables['n_sumIDtop'][3] = t.jets_mcMatchId[allcomb_[i][1]]
                                    mytree.variables['n_sumIDtop'][4] = t.jets_mcMatchId[allcomb_[i][4]]
                                    mytree.variables['n_sumIDtop'][5] = t.jets_mcMatchId[allcomb_[i][5]]

                  if len(bestcomb_) == 0: continue
                  
                  # mytree.variables['BDT_ClassMajo'][BDT_classes.index(max(BDT_classes))] = 1
                  mytree.variables['BDT_ttbarMajo'][0] = meanBDTttbar/sumprob if sumprob>0 else meanBDTttbar/len(allcomb_)
                  UpdateVariables(bestcomb_,jets_,mytree.variables,MVA_Only)
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

                  # t1 = ROOT.TLorentzVector()
                  # t2 = ROOT.TLorentzVector()
                  # if sample !='data':
                  #       mytree.variables['n_genTopHad'][0] = t.ngenTopHad
                  #       for itophad in range(t.ngenTopHad):
                  #             mytree.variables['genTopHad_pt'][itophad] = t.genTopHad_pt[itophad]
                  #       if t.ngenTopHad == 2:
                  #             t1.SetPtEtaPhiM(t.genTopHad_pt[0],t.genTopHad_eta[0],t.genTopHad_phi[0],t.genTopHad_mass[0])
                  #             t2.SetPtEtaPhiM(t.genTopHad_pt[1],t.genTopHad_eta[1],t.genTopHad_phi[1],t.genTopHad_mass[1])
                  #       else:
                  #             t1.SetPtEtaPhiM(-10,-10,-10,-10)
                  #             t2.SetPtEtaPhiM(-10,-10,-10,-10)                  


                  # if corrbestchi2 > 0 and corrbestchi2 < bestchi2:


                  
                  if sample == 'ttbar':
                        mytree.variables['weight'][0] *= np.exp(0.5*(t.ngenTopLep*0.0843616-0.000743051*np.sum(t.genTopLep_pt)+t.ngenTopHad*0.0843616-0.000743051*np.sum(t.genTopHad_pt)))*(t.jets_pt[0]/t.jets_pt[0])
                        
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
                  
                  tkin.Fill()
                  
                  mytree.ZeroArray()
                  
            if e > emax: break

      watch.Print()
      tkin.Write()
      fout.Write()
      fout.Close()

