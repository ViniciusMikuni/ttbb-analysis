# import ROOT in batch mode
import sys
import ROOT
from itertools import permutations, combinations
import numpy as np

import re
sys.path.insert(0, '/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test')
from Skim_cfg import *
ROOT.gROOT.SetBatch(True)
#ROOT.gSystem.Load("libPhysicsToolsKinFitter.so")
#ROOT.gROOT.ProcessLine(".L /shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/Kinfit.C+")
from ROOT import TFile,TTree,TString, TMVA, TMath
TMVA.Tools.Instance()


def JetComb(njets,jetpos_):
    '''return all the combinations for jet and b-jet  positioning'''
    jetpermut_ = list(permutations(jetpos_,6))#permutations of all jets - bjets
    completelist_ = []
    for i in range(len(jetpermut_)):
        if (jetpermut_[i][0] > jetpermut_[i][1] or jetpermut_[i][2] > jetpermut_[i][3] or jetpermut_[i][4] > jetpermut_[i][5]): continue
        completelist_.append(jetpermut_[i])
#    print completelist_, ' complete list ', njets, ' njets'
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



                  for ind, rev in enumerate(csvrank):
                        var['addJet_CSV'][ind] = t.jets_btagCSV[addjets[csvrank[rev]]]
                        var['addJet_cMVA'][ind] = t.jets_btagCMVA[addjets[csvrank[rev]]]
                        var['addJet_DeepCSV'][ind] = t.jets_btagDeepCSV[addjets[csvrank[rev]]]
                        var['addJet_DeepcMVA'][ind] = t.jets_btagDeepCMVA[addjets[csvrank[rev]]]
                        var['addJet_pt'][ind] = t.jets_pt[addjets[csvrank[rev]]]
                        var['addJet_eta'][ind] = t.jets_eta[addjets[csvrank[rev]]]
                        var['addJet_phi'][ind] = t.jets_phi[addjets[csvrank[rev]]]
                        var['addJet_QGL'][ind] = t.jets_qgl[addjets[csvrank[rev]]]
                        
                        
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
                        var['jet_MOverPt'][ipos] = t.jets_mass[pos]/t.jets_pt[pos]
                        var['jet_CSV'][ipos] = t.jets_btagCSV[pos]
                        var['jet_cMVA'][ipos] = t.jets_btagCMVA[pos]
                        var['jet_DeepCSV'][ipos] = t.jets_btagDeepCSV[pos]
                        var['jet_DeepcMVA'][ipos] = t.jets_btagDeepCMVA[pos]
                        MVA_Only['jet_QGL['+str(ipos)+']'][0] = t.jets_qgl[pos]
                        var['jet_QGL'][ipos] = t.jets_qgl[pos]

                  # for var in tvars:
                  #      print var, tvars[var][0]

        
#def KinAnalysis(tagged,filename,nmaxentries = -1):
if __name__ == "__main__":
 
      if len(sys.argv) > 2:
            filename = sys.argv[1]
            sample = str(sys.argv[2])
      else: print 'Missing arguments'
      
      t = ROOT.TChain('tree')
      AddProcessChain(sample,t)
      samples = ['ttbar','QCD','data']
      if sample not in samples: print 'We dont have this sample!'
      emin = emax = 0
      print 'start stopwatch'
      watch = ROOT.TStopwatch()
      with open(filename) as f:
            lines = f.read().splitlines()
            emin = map(int, re.findall(r'\d+', lines[0]))[0]
            emax = map(int, re.findall(r'\d+', lines[0]))[1]           

      foutname = 'Correct_NoBtag_'
      foutname += sample
      foutname += str(emax)+'.root'
      fout = TFile(foutname,'recreate')


      mytree = ManageTTree(tvars,tkin)
      #mytree.variables.update(MVA_Only)

      reader_Class1ad = TMVA.Reader( "!Color:!Silent" )
      reader_Class2ad = TMVA.Reader( "!Color:!Silent" )
      usevar1add = ['deltaRaddb1','deltaRaddb2','deltaRaddw1','deltaRaddw2','deltaRaddtop1','deltaRaddtop2','deltaPhiaddb1','deltaPhiaddb2','deltaPhiaddw1','deltaPhiaddw2','deltaPhiaddtop1','deltaPhiaddtop2','deltaEtaaddb1','deltaEtaaddb2','deltaEtaaddw1','deltaEtaaddw2','deltaEtaaddtop1','deltaEtaaddtop2','addJet_CSV[0]','addJet_pt[0]','ht','btagLR4b','btagLR3b','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','tt_pt']
      usevar2add = usevar1add + ['addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[1]','addJet_pt[1]','addJet_mass']
      
      for var in usevar1add:
          if var in mytree.variables:
              reader_Class1ad.AddVariable(var,mytree.variables[var])
          else:
              reader_Class1ad.AddVariable(var,MVA_Only[var])
      for var in usevar2add:
          if var in mytree.variables:
              reader_Class2ad.AddVariable(var,mytree.variables[var])
          else:
              reader_Class2ad.AddVariable(var,MVA_Only[var])

      weightFileBDT_Class1ad = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDTmulti_Cat1add.weights.xml'
      weightFileBDT_Class2ad = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDTmulti_Cat2add.weights.xml'

      reader_Class1ad.BookMVA('BDT_Class1ad',weightFileBDT_Class1ad)
      reader_Class2ad.BookMVA('BDT_Class2ad',weightFileBDT_Class2ad)
      



      
      if emax == 0:
          print 'emax == 0'

#      ROOT.ROOT.EnableImplicitMT()      
      for e,event in enumerate(t) :
#            print "processing event number: ", e
            if e < emin: continue
            bpos_ = []
            
            
            #corrb_ = []
            #corrlight_ = []
            jets_ = ROOT.vector('TLorentzVector')()
            ordered_jets_ = ROOT.vector('TLorentzVector')()
            bestcomb_ = []

            
            

            #if not tthcut: continue
            if t.nBCSVM >=2 and t.njets >=7:
                tth = t.json and (t.HLT_ttH_FH or t.HLT_BIT_HLT_PFJet450_v) and t.ht>500 and t.jets_pt[5]>40
                if not tth: continue
                mytree.variables['weight'][0] = t.puWeight * t.btagWeightCSV  * t.qgWeight * np.sign(t.genWeight)
                corrb_ = array( 'i', 2*[ -10 ] )
                corrlight_ = array( 'i', 4*[ -10 ] )
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
                mytree.variables['memttbb'][0]  = max(t.mem_ttbb_FH_4w2h1t_p/(t.mem_tth_FH_4w2h1t_p) if t.mem_tth_FH_4w2h1t_p > 0 else -10,t.mem_ttbb_FH_4w2h2t_p/(t.mem_tth_FH_4w2h2t_p) if t.mem_tth_FH_4w2h2t_p > 0 else -10)
                mytree.variables['ttCls'][0] = t.ttCls if sample != 'QCD' else -1 
                njets = 0
                nljets = 0
                ncorrb = 0
                jetpos_ =[]
                ptR = 0
                for i in range(0,t.njets):#find the b-tagged jets
                    jet = ROOT.TLorentzVector()
                    jet.SetPtEtaPhiM(t.jets_pt[i],t.jets_eta[i],t.jets_phi[i],t.jets_mass[i])
                    jets_.push_back(jet)
                    if abs(t.jets_mcFlavour[i]) == 5 and abs(t.jets_mcMatchId[i]) != 6 :ncorrb+=1
                    if abs(t.jets_mcMatchId[i]) == 6 and (t.jets_matchFlag[i]>=0):
                        if t.jets_mcMatchId[i] == 6:   
                            if t.jets_mcFlavour[i] == 5 and t.jets_matchFlag[i] == 1 : corrb_[0] = i
                            elif t.jets_matchFlag[i] == 0:
                                if corrlight_[0] == -10: corrlight_[0] = i
                                else: corrlight_[1] = i
                        else:
                            if t.jets_mcFlavour[i] == -5 and t.jets_matchFlag[i] == 1: corrb_[1] = i
                            elif t.jets_matchFlag[i] == 0:
                                if corrlight_[2] == -10: corrlight_[2] = i
                                else: corrlight_[3] = i
                        
                    njets+=1
                    jetpos_.append(i)
                    ptR+=t.jets_pt[i]*(t.jets_phi[i]**2 + t.jets_eta[i]**2)**0.5
                        
                            
                mytree.variables['girth'][0] = ptR/t.ht
                mytree.variables['hasCorrect'][0] = 0
                if -10 not in corrlight_ and -10 not in corrb_:
                    mytree.variables['hasCorrect'][0] = 1
                    if t.jets_pt[corrlight_[0]] < t.jets_pt[corrlight_[1]]:corrlight_ = [corrlight_[1],corrlight_[0]]
                    if t.jets_pt[corrlight_[2]] < t.jets_pt[corrlight_[3]]:corrlight_ = [corrlight_[3],corrlight_[2]]
                    if t.jets_pt[corrb_[0]] < t.jets_pt[corrb_[1]]:corrb_ = [corrb_[1],corrb_[0]]



#              if mytree.variables['isCorrect'][0] == 1: print 'after', corrjets_

                mytree.variables['ht'][0] = t.ht
                mytree.variables['n_jets'][0] = t.njets
                mytree.variables['n_bjets'][0] = t.nBCSVM
                mytree.variables['n_addJets'][0] = njets - 6

                alljets = range(t.njets)


#                  print t.njets, ' njets ',nbjets, ' nbjets ', ' bpos ', bpos_ 
                comb_ = JetComb(njets,jetpos_)
                

                corr_ = []
                for b in corrb_:
                    corr_.append(b)
                for l in corrlight_:
                    corr_.append(l)
                
                corrcomb_ = JetComb(4+2,corr_)


                for icomb, bestcomb_ in enumerate(comb_) :
                    if icomb > 2521 and bestcomb_ not in corrcomb_: continue
                    UpdateVariables(bestcomb_,jets_,mytree.variables,MVA_Only)
                    if mytree.variables['prob_chi2'][0] < probcut: continue
                    lq1.UpdateParam(jets_[bestcomb_[2]])
                    lq2.UpdateParam(jets_[bestcomb_[3]])
                    lp1.UpdateParam(jets_[bestcomb_[4]])
                    lp2.UpdateParam(jets_[bestcomb_[5]])
                    b1.UpdateParam(jets_[bestcomb_[0]])
                    b2.UpdateParam(jets_[bestcomb_[1]])
                    w1.UpdateParam(jets_[bestcomb_[2]]+jets_[bestcomb_[3]])
                    top1.UpdateParam(jets_[bestcomb_[0]]+jets_[bestcomb_[3]]+jets_[bestcomb_[2]])
                    w2.UpdateParam(jets_[bestcomb_[5]]+jets_[bestcomb_[4]])
                    top2.UpdateParam(jets_[bestcomb_[1]]+jets_[bestcomb_[4]]+jets_[bestcomb_[5]])
                    tt.UpdateParam(jets_[bestcomb_[0]]+jets_[bestcomb_[1]]+jets_[bestcomb_[2]]+jets_[bestcomb_[3]]+jets_[bestcomb_[4]]+jets_[bestcomb_[5]])

                    if njets == 7:
                        mytree.variables['BDT_ttbb'][0] = reader_Class1ad.EvaluateMulticlass("BDT_Class1ad")[0]
                        mytree.variables['BDT_ttcc'][0] = reader_Class1ad.EvaluateMulticlass("BDT_Class1ad")[1]
                        mytree.variables['BDT_ttlf'][0] = reader_Class1ad.EvaluateMulticlass("BDT_Class1ad")[2]
                    else:
                        mytree.variables['BDT_ttbb'][0] = reader_Class2ad.EvaluateMulticlass("BDT_Class2ad")[0]
                        mytree.variables['BDT_ttcc'][0] = reader_Class2ad.EvaluateMulticlass("BDT_Class2ad")[1]
                        mytree.variables['BDT_ttlf'][0] = reader_Class2ad.EvaluateMulticlass("BDT_Class2ad")[2]
                        

                    
                      
                    mytree.variables['isPerfect'][0] =0
                    if bestcomb_ in corrcomb_:
                        mytree.variables['isCorrect'][0] = 1
                        if bestcomb_ == corrcomb_[0]:mytree.variables['isPerfect'][0] =1
                    else: mytree.variables['isCorrect'][0] = 0
                    tkin.Fill()
                    
                mytree.ZeroArray()
                    #else: twrong.Fill()
            


            
            
            if e > emax: break

      tkin.Write()
      #twrong.Write()
      watch.Print()

      fout.Write()
      fout.Close()

