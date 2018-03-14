# import ROOT in batch mode
import sys
import ROOT
from itertools import permutations, combinations
import numpy as np

import re
sys.path.insert(0, '/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test')
from BDTTree_cfg import *
ROOT.gROOT.SetBatch(True)
#ROOT.gSystem.Load("libPhysicsToolsKinFitter.so")
#ROOT.gROOT.ProcessLine(".L /shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/Kinfit.C+")
from ROOT import TMath,TFile,TTree,TString

def JetComb(njets, nbjets,jetpos_,bpos_=[]):
      '''return all the combinations for jet and b-jet  positioning'''
      if nbjets == 0: return list(combinations(range(njets),6))
      else:
            bpermut_ = list(combinations(bpos_,2))

#            print bpermut_, ' bpermut '
            jetpermut_ = list(permutations(jetpos_,4))#permutations of all jets - bjets
            completelist_ = []
            for i in range(len(bpermut_)):
                  for j in range(len(jetpermut_)):
                        if len(jetpos_) >= 4 and (jetpermut_[j][0] > jetpermut_[j][1] or jetpermut_[j][2] > jetpermut_[j][3]): continue
                        completelist_.append(bpermut_[i] + jetpermut_[j])
#            print completelist_, ' complete list ', nbjets, ' nbjets ', njets, ' njets'
            return completelist_

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

      foutname = 'BDT_train_tth'
      foutname += sample
      foutname += str(emax)+'.root'
      fout = TFile(foutname,'recreate')

      if emax == 0:
          print 'emax == 0'

      #ROOT.ROOT.EnableImplicitMT()      
      for e,event in enumerate(t) :
#            print "processing event number: ", e
            if e < emin: continue
            bpos_ = []
            jetpos_ =[]
            corrb_ = []
            corrlight_ = []
            jets_ = ROOT.vector('TLorentzVector')()
            bestcomb_ = []

            #
            tthcut = t.json and (t.HLT_ttH_FH or t.HLT_BIT_HLT_PFJet450_v) and t.ht>500 and t.jets_pt[5]>40

            if not tthcut: continue
            if t.njets >= 6 and t.nBCSVM >=3 and (t.njets - t.nBCSVM >=4) :
                weight[0] = t.puWeight * t.btagWeightCSV  * t.qgWeight * np.sign(t.genWeight)
                centrality[0] = t.centrality
                ttCls[0] = t.ttCls if sample != 'QCD' else -1 
                njets = 0
                nbjets = 0
                nljets = 0
                for i in range(0,t.njets):#find the b-tagged jets
                    jet = ROOT.TLorentzVector()
                    jet.SetPtEtaPhiM(t.jets_pt[i],t.jets_eta[i],t.jets_phi[i],t.jets_mass[i])
                    jets_.push_back(jet)
                    if abs(t.jets_mcFlavour[i]) == 5 and abs(t.jets_mcMatchId[i]) != 6 :ncorrb+=1
                    if abs(t.jets_mcMatchId[i]) == 6:
                          if abs(t.jets_mcFlavour[i]) == 5 : corrb_.append(i)
                          else: corrlight_.append(i)
                          
                    if t.jets_btagCSV[i] >= btagcsvm:
                        bpos_.append(i)
                        nbjets +=1
                    else: 
                        nljets+=1
                        jetpos_.append(i)
                        
                qgLR[0] = -100
                btagLR4b[0] = -100
                btagLR3b[0] = -100
                memttbb[0] = -1e-19

                btagLR3b[0] = t.btag_LR_3b_2b_btagCSV
                btagLR4b[0] = t.btag_LR_4b_2b_btagCSV
                if nbjets == 3:
                      if (t.mem_ttbb_FH_4w2h1t_p + 0.5* t.mem_tth_FH_4w2h1t_p) > 0: memttbb[0] = t.mem_ttbb_FH_4w2h1t_p/(t.mem_ttbb_FH_4w2h1t_p + 0.5* t.mem_tth_FH_4w2h1t_p)
                      else: memttbb[0] = -10
                      if nljets == 4:
                            qgLR[0] = t.qg_LR_3b_flavour_4q_0q
                      elif nljets >= 5:
                            qgLR[0] = t.qg_LR_3b_flavour_5q_0q
                if nbjets >= 4:
                      if (t.mem_ttbb_FH_4w2h2t_p + 0.5* t.mem_tth_FH_4w2h2t_p) > 0: memttbb[0] = t.mem_ttbb_FH_4w2h2t_p/(t.mem_ttbb_FH_4w2h2t_p + 0.5* t.mem_tth_FH_4w2h2t_p)
                      else: memttbb[0] = -10
                      if nljets == 4: qgLR[0] = t.qg_LR_4b_flavour_4q_0q
                      elif nljets >= 5: qgLR[0] = t.qg_LR_4b_flavour_5q_0q
                if len(corrb_) == 2 and len(corrlight_) == 4:
                      isCorrect[0] = 1
                else:
                      if sample != 'QCD': isCorrect[0] = 0
                      else: isCorrect[0] = -1

                
                bestchi2  =  999999999
                probchi2  = probkin  = -10
                simplechi2 = -10
                ht[0] = t.ht
                n_jets[0] = t.njets
                n_bjets[0] = nbjets
                n_addbjets[0] = nbjets -2
                n_addJets[0] = nljets + nbjets - 6
                n_jets[0] = nljets + nbjets

                comb_ = JetComb(nljets,nbjets,jetpos_,bpos_)
                corrcomb_ = JetComb(4,2,corrlight_,corrb_)
                print corrcomb_, 'corrcomb_'
                print comb_, 'comb_'
                
                for i in range(len(comb_)):
                      simple_chi2[0] = pow(((jets_[bestcomb_[0]] + jets_[bestcomb_[2]]+ jets_[bestcomb_[3]]).M() - 173.4)/20.0,2) + pow(((jets_[bestcomb_[1]] + jets_[bestcomb_[4]]+ jets_[bestcomb_[5]]).M() - 173.4)/20.0,2) + pow(((jets_[bestcomb_[2]]+ jets_[bestcomb_[3]]).M() - 83.1)/16.5,2) + pow(((jets_[bestcomb_[5]]+ jets_[bestcomb_[4]]).M() - 83.1)/16.5,2)
                        
                    if bestchi2 > simplechi2:
                        simple_chi2[0] = simplechi2
                        prob_chi2[0] = TMath.Prob(float(simple_chi2[0]),4)
                        bestcomb_=comb_[i]
                        bestchi2 = simplechi2
                if len(bestcomb_) == 0: continue        
                alljets = range(t.njets)
                addjets = [x for x in alljets if x not in bestcomb_]
                addjetscsv = []
                addjetspt = []
                if len(addjets) < 10:
                      for najet,ajet in enumerate(addjets):
                            addjetscsv.append(t.jets_btagCSV[ajet])
                            addjetspt.append(t.jets_pt[ajet])
                csvrank = np.flip(np.argsort(addjetscsv),0)
                if len(csvrank)>=1:
                        deltaRaddb1[0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[bestcomb_[0]])
                        deltaRaddb2[0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[bestcomb_[1]])
                        deltaRaddw1[0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[bestcomb_[3]]+jets_[bestcomb_[2]])
                        deltaRaddw2[0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[bestcomb_[4]]+jets_[bestcomb_[5]])
                        deltaRaddtop1[0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[bestcomb_[0]]+jets_[bestcomb_[2]]+jets_[bestcomb_[3]])
                        deltaRaddtop2[0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[bestcomb_[1]]+jets_[bestcomb_[4]]+jets_[bestcomb_[5]])
                        
                if len(csvrank)>=2:
                      addJet_deltaR[0] = jets_[addjets[csvrank[0]]].DeltaR(jets_[addjets[csvrank[1]]])
                      addJet_deltaPhi[0] = jets_[addjets[csvrank[0]]].DeltaPhi(jets_[addjets[csvrank[1]]])

                for ind, rev in enumerate(csvrank):
                      addJet_CSV[ind] = addjetscsv[rev]
                      addJet_pt[ind] = addjetspt[rev]
                lightq1.UpdateParam(jets_[bestcomb_[2]])
                lightq2.UpdateParam(jets_[bestcomb_[3]])
                lightp1.UpdateParam(jets_[bestcomb_[4]])
                lightp2.UpdateParam(jets_[bestcomb_[5]])
                deltaRl1l2[0] = jets_[bestcomb_[2]].DeltaR(jets_[bestcomb_[3]])
                deltaEtal1l2[0] = abs(jets_[bestcomb_[2]].Eta() - jets_[bestcomb_[3]].Eta())
                deltaPhil1l2[0] = abs(jets_[bestcomb_[2]].Phi() - jets_[bestcomb_[3]].Phi())

                deltaPhiw1w2[0] = (jets_[bestcomb_[3]]+jets_[bestcomb_[2]]).DeltaPhi((jets_[bestcomb_[5]]+jets_[bestcomb_[4]]))
                deltaPhit1t2[0] = (jets_[bestcomb_[0]]+jets_[bestcomb_[3]]+jets_[bestcomb_[2]]).DeltaPhi((jets_[bestcomb_[1]]+jets_[bestcomb_[5]]+jets_[bestcomb_[4]]))
                deltaRq1q2[0] = jets_[bestcomb_[4]].DeltaR(jets_[bestcomb_[5]])
                deltaEtaq1q2[0] = abs(jets_[bestcomb_[4]].Eta() - jets_[bestcomb_[5]].Eta())
                deltaPhiq1q2[0] = abs(jets_[bestcomb_[4]].Phi() - jets_[bestcomb_[5]].Phi())
                
                deltaRb1b2[0] = jets_[bestcomb_[0]].DeltaR(jets_[bestcomb_[1]])
                deltaRb1w1[0] = jets_[bestcomb_[0]].DeltaR(jets_[bestcomb_[3]]+jets_[bestcomb_[2]])
                deltaRb2w2[0] = jets_[bestcomb_[1]].DeltaR(jets_[bestcomb_[4]]+jets_[bestcomb_[5]])
                deltaEtab1b2[0] = abs(jets_[bestcomb_[0]].Eta() - jets_[bestcomb_[1]].Eta())
                deltaPhib1b2[0] = abs(jets_[bestcomb_[0]].Phi() - jets_[bestcomb_[1]].Phi())
                
                b1.UpdateParam(jets_[bestcomb_[0]])
                b2.UpdateParam(jets_[bestcomb_[1]])
                b1_csv[0] = t.jets_btagCSV[bestcomb_[0]]
                b2_csv[0] = t.jets_btagCSV[bestcomb_[1]]
                w1.UpdateParam(jets_[bestcomb_[2]]+jets_[bestcomb_[3]])
                top1.UpdateParam(jets_[bestcomb_[0]]+jets_[bestcomb_[3]]+jets_[bestcomb_[2]])
                w2.UpdateParam(jets_[bestcomb_[5]]+jets_[bestcomb_[4]])
                top2.UpdateParam(jets_[bestcomb_[1]]+jets_[bestcomb_[4]]+jets_[bestcomb_[5]])
                tt.UpdateParam(jets_[bestcomb_[0]]+jets_[bestcomb_[1]]+jets_[bestcomb_[2]]+jets_[bestcomb_[3]]+jets_[bestcomb_[4]]+jets_[bestcomb_[5]])
                for icomb, comb in enumerate(bestcomb_):
                      jet_CSV[icomb] = t.jets_btagCSV[comb]
                      jet_QGL[icomb] = t.jets_qgl[comb]


                tsig.Fill()
            
                

            
            
            if e > emax: break


#      hCount.Write()
#      hPass.Write()
      tsig.Write()
      watch.Print()
      fout.Write()
      fout.Close()
#      f.Close()
