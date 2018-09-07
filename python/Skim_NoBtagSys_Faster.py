#!/usr/bin/env python
import sys
import ROOT
from itertools import permutations, combinations
import numpy as np
from os import environ
environ['KERAS_BACKEND'] = 'theano'
import re
import ConfigParser
import ast
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
            #return ast.literal_eval(config.get('Permutations',str(njets)))
            jetpermut_ = list(permutations(jetpos_,6))#permutations of all jets
            completelist_ = []
            for i in range(len(jetpermut_)):
                  if (jetpermut_[i][0] > jetpermut_[i][1] or jetpermut_[i][2] > jetpermut_[i][3] or jetpermut_[i][4] > jetpermut_[i][5]): continue
                  completelist_.append(jetpermut_[i])
            #print completelist_, ' complete list ',
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
            #print completelist_, ' complete list ', nbjets, ' nbjets ', njets, ' njets'
            return completelist_

def MeasureNominal(t,mytree,pass_sys,isSys=0):
      bpos_ = []
      jetpos_ =[]
      jets_ = ROOT.vector('TLorentzVector')()
      ordered_jets_ = ROOT.vector('TLorentzVector')()
      bestcomb_ = []
      corrcomb_ = []
      corrb_ = []
      corrlight_ = []
      if (t.njets >= 7 and t.nBCSVM >=2) or pass_sys:
            if sample !='data':
                  mytree.variables['weight'][0] = np.sign(t.genWeight)
                  mytree.variables['puweight'][0] = t.puWeight
                  mytree.variables['puweight_Up'][0] = t.puWeightUp
                  mytree.variables['puweight_Down'][0] = t.puWeightDown

                  mytree.variables['trigweight'][0] = t.triggerWeight
                  mytree.variables['trigweight_Up'][0] = t.triggerWeightUp
                  mytree.variables['trigweight_Down'][0] = t.triggerWeightDown
                  mytree.variables['btagweight'][0] = t.btagWeightCSV
                  mytree.variables['qgweight'][0] = t.qgWeight
                  mytree.variables['qgweight_Up'][0] = 2*t.qgWeight -1
                  mytree.variables['qgweight_Down'][0] = 1.0
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
            else:
                  mytree.variables['weight'][0] = 1


            ntopjets = ntoptaggedjets= 0
            nbjets = 0
            nljets = 0


            bdtcomb  =  -999999999
            chi2comb    =  999999999

            mytree.variables['nPVs'][0] = t.nPVs
            mytree.variables['sphericity'][0] = t.sphericity
            mytree.variables['C'][0] = t.C
            mytree.variables['minjetpt'][0] = t.jets_pt[t.njets-1]

            mytree.variables['jets_dRavg'][0] = sum(t.jets_dRave)/t.njets
            drmin_list= [x for x in t.jets_dRmin if x > 0]
            if len(drmin_list)>0:mytree.variables['jets_dRmin'][0] = min([x for x in t.jets_dRmin if x > 0])
            else:   mytree.variables['jets_dRmin'][0] =0
            mytree.variables['jets_dRmax'][0] = max(t.jets_dRmax)
            if sample == 'QCD':mytree.variables['isQCD'][0] = 1
            else: mytree.variables['isQCD'][0] = 0

            #mytree.variables['girth'][0] = ptR/(t.ht)**2
            if 'ttbar' in sample or 'theory' in sample:mytree.variables['ttCls'][0] = t.ttCls
            else: mytree.variables['ttCls'][0] = -1
            mytree.variables['ht'][0] = t.ht
            #mytree.variables['all_mass'][0] = t.invmass
            #mytree.variables['closest_mass'][0] = t.mjjmin
            mytree.variables['jet5pt'][0] = t.jets_pt[5]
            mytree.variables['n_jets'][0] = t.njets
            mytree.variables['n_bjets'][0] = t.nBCSVM
            mytree.variables['n_addJets'][0] = t.njets - 6
            #mytree.variables['n_topjets'][0] = ntopjets
            mytree.variables['qgLR'][0] = -100
            mytree.variables['centrality'][0] = t.centrality
            mytree.variables['aplanarity'][0] = t.aplanarity
            mytree.variables['meanDeltaRbtag'][0] = t.mean_dr_btag
            mytree.variables['meanCSVbtag'][0]=t.mean_bdisc
            mytree.variables['meanCSV'][0]=t.mean_bdisc_btag
            mytree.variables['btagLR3b'][0] = t.btag_LR_3b_2b_btagCSV
            mytree.variables['btagLR4b'][0] = t.btag_LR_4b_2b_btagCSV
            mytree.variables['nBCSVM'][0] = t.nBCSVM

            qgLR3b = t.qg_LR_3b_flavour_4q_0q
            qgLR4b = t.qg_LR_4b_flavour_4q_0q



            if nbjets == 3:
                  mytree.variables['qgLR'][0] = qgLR3b
                  # if t.mem_ttbb_FH_4w2h1t_p  > 0: mytree.variables['memttbb'][0] = -TMath.Log10(t.mem_ttbb_FH_4w2h1t_p)
                  # else: mytree.variables['memttbb'][0] = -10
                  # #print mytree.variables['memttbb'][0]
                  # if nljets == 4:
                  #       mytree.variables['qgLR'][0] = t.qg_LR_3b_flavour_4q_0q
                  # elif nljets >= 5:
                  #       mytree.variables['qgLR'][0] = t.qg_LR_3b_flavour_5q_0q
            if nbjets >= 4:
                  mytree.variables['qgLR'][0] = qgLR4b
                  # if t.mem_ttbb_FH_4w2h2t_p  > 0: mytree.variables['memttbb'][0] = -TMath.Log10(t.mem_ttbb_FH_4w2h2t_p)
                  # else: mytree.variables['memttbb'][0] = -10
                  # #print mytree.variables['memttbb'][0]
                  # if nljets == 4: mytree.variables['qgLR'][0] = t.qg_LR_4b_flavour_4q_0q
                  # elif nljets >= 5: mytree.variables['qgLR'][0] = t.qg_LR_4b_flavour_5q_0q
            else:
                  # mytree.variables['memttbb'][0] = -TMath.Log10(t.mem_ttbb_FH_4w2h1t_p) if t.mem_ttbb_FH_4w2h1t_p >0 else -10
                  mytree.variables['qgLR'][0] = qgLR3b

            if not (t.njets >= 7 and t.nBCSVM >=2):return 0
            for i in range(0,t.njets):#find the b-tagged jets
                  jet = ROOT.TLorentzVector()
                  jet.SetPtEtaPhiM(t.jets_pt[i],t.jets_eta[i],t.jets_phi[i],t.jets_mass[i])

                  jets_.push_back(jet)
                  if sample !='data':
                        if abs(t.jets_mcMatchId[i]) == 6:
                              if abs(t.jets_mcFlavour[i]) == 5 and t.jets_matchFlag[i] == 1 : corrb_.append(i)
                              elif t.jets_matchFlag[i] == 0: corrlight_.append(i)


            alljets = range(min(t.njets,8))
            if len(corrb_) == 2 and len(corrlight_) == 4:
                  mytree.variables['existCorrect'][0] = 1
                  corrcomb_ = JetComb(4,2,corrlight_,corrb_)
                  for ii, c in enumerate(corrcomb_[0]):
                        mytree.variables['corr_comb'][ii]=c
            else:mytree.variables['existCorrect'][0] = 0
            mytree.variables['hasbCorrect'][0] = 0

            allcomb_ = JetComb(min(t.njets,8),0,alljets)

            mytree.variables['hasCorrect'][0] = 0
            BDT_classes = [0,0,0]
            printing = 0
            highest = 0
            bestcat = 0
            #print comb_, 'comb_'
            meanBDTttbar=sumprob = 0
            maxbdt = 0

            # print 'start comb'
            # watch.Print()

            for comb in allcomb_:

                  mytree.variables['simple_chi2'][0] = pow(((jets_[comb[0]] + jets_[comb[2]]+ jets_[comb[3]]).M() - 173.2)/20.5,2) + pow(((jets_[comb[1]] + jets_[comb[4]]+ jets_[comb[5]]).M() - 173.2)/17.8,2) + pow(((jets_[comb[2]]+ jets_[comb[3]]).M() - 82.3)/10.9,2) + pow(((jets_[comb[5]]+ jets_[comb[4]]).M() - 82.3)/10.9,2)
                  if mytree.variables['simple_chi2'][0] < chi2cut:continue
                  mytree.variables['prob_chi2'][0] = TMath.Prob(mytree.variables['simple_chi2'][0],4)
                  #if mytree.variables['prob_chi2'][0] < probcut:return


                  # MVA_Only['top1_m'][0] = (jets_[comb[0]]+jet[comb[3]]+jet[comb[2]]).M()
                  # MVA_Only['top2_m'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).M()
                  # MVA_Only['tt_m'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]+jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).M()
                  # MVA_Only['tt_pt'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]+jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Pt()

                  # MVA_Only['w1_m'][0] = (jet[comb[2]]+jet[comb[3]]).M()
                  # MVA_Only['w2_m'][0] = (jet[comb[5]]+jet[comb[4]]).M()
                  # MVA_Only['top1_pt'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Pt()
                  # MVA_Only['top2_pt'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).Pt()
                  # MVA_Only['w1_pt'][0] = (jet[comb[2]]+jet[comb[3]]).Pt()
                  # MVA_Only['w2_pt'][0] = (jet[comb[5]]+jet[comb[4]]).Pt()
                  # MVA_Only['b1_pt'][0] = (jet[comb[0]]).Pt()
                  # MVA_Only['b2_pt'][0] = (jet[comb[1]]).Pt()
                  mytree.variables['deltaRp1p2'][0] = jets_[comb[2]].DeltaR(jets_[comb[3]])
                  mytree.variables['deltaPhip1p2'][0] = jets_[comb[2]].DeltaPhi(jets_[comb[3]])
                  mytree.variables['deltaPhib1b2'][0] = jets_[comb[0]].DeltaPhi(jets_[comb[1]])

                  mytree.variables['deltaPhiw1w2'][0] = (jets_[comb[3]]+jets_[comb[2]]).DeltaPhi((jets_[comb[5]]+jets_[comb[4]]))
                  mytree.variables['deltaPhit1t2'][0] = (jets_[comb[0]]+jets_[comb[3]]+jets_[comb[2]]).DeltaPhi((jets_[comb[1]]+jets_[comb[5]]+jets_[comb[4]]))
                  mytree.variables['deltaRq1q2'][0] = jets_[comb[4]].DeltaR(jets_[comb[5]])
                  mytree.variables['deltaPhiq1q2'][0] = jets_[comb[4]].DeltaPhi(jets_[comb[5]])

                  mytree.variables['deltaRb1b2'][0] = jets_[comb[0]].DeltaR(jets_[comb[1]])
                  mytree.variables['deltaRb1w1'][0] = jets_[comb[0]].DeltaR(jets_[comb[3]]+jets_[comb[2]])
                  mytree.variables['deltaRb2w2'][0] = jets_[comb[1]].DeltaR(jets_[comb[4]]+jets_[comb[5]])

                  mytree.variables['deltaEtap1p2'][0] = jets_[comb[2]].Eta() - jets_[comb[3]].Eta()
                  mytree.variables['deltaEtaq1q2'][0] = jets_[comb[4]].Eta() - jets_[comb[5]].Eta()
                  mytree.variables['deltaEtab1b2'][0] = jets_[comb[0]].Eta() - jets_[comb[1]].Eta()
                  mytree.variables['deltaEtaw1w2'][0] = (jets_[comb[3]]+jets_[comb[2]]).Eta() - (jets_[comb[5]]+jets_[comb[4]]).Eta()
                  mytree.variables['deltaEtat1t2'][0] = (jets_[comb[0]]+jets_[comb[3]]+jets_[comb[2]]).Eta() - (jets_[comb[1]]+jets_[comb[5]]+jets_[comb[4]]).Eta()



                  mytree.variables['p1b1_mass'][0] = (jets_[comb[0]] + jets_[comb[2]]).M()
                  mytree.variables['q1b2_mass'][0] = (jets_[comb[1]] + jets_[comb[4]]).M()
                  mytree.variables['deltaRb1p1'][0] = jets_[comb[0]].DeltaR(jets_[comb[2]])
                  mytree.variables['deltaRb2q1'][0] = jets_[comb[1]].DeltaR(jets_[comb[4]])
                  mytree.variables['deltaRb1top2'][0] = jets_[comb[0]].DeltaR(jets_[comb[1]]+jets_[comb[4]]+jets_[comb[5]])
                  mytree.variables['deltaRb2top1'][0] = jets_[comb[1]].DeltaR(jets_[comb[0]]+jets_[comb[2]]+jets_[comb[3]])
                  mytree.variables['deltaRb1w2'][0] = jets_[comb[0]].DeltaR(jets_[comb[4]]+jets_[comb[5]])
                  mytree.variables['deltaRb2w1'][0] = jets_[comb[1]].DeltaR(jets_[comb[2]]+jets_[comb[3]])
                  minrb1p = mytree.variables['deltaRb1p1'][0]
                  minrb2q = mytree.variables['deltaRb2q1'][0]
                  if jets_[comb[0]].DeltaR(jets_[comb[3]]) < minrb1p:
                        minrb1p = jets_[comb[0]].DeltaR(jets_[comb[3]])
                  if jets_[comb[1]].DeltaR(jets_[comb[5]]) < minrb2q:
                        minrb2q = jets_[comb[1]].DeltaR(jets_[comb[5]])
                  mytree.variables['mindeltaRb1p'][0] = minrb1p
                  mytree.variables['mindeltaRb2q'][0] = minrb2q
                  for ipos, pos in enumerate(comb):
                        MVA_Only['jet_CSV['+str(ipos)+']'][0] = t.jets_btagCSV[pos]
                        MVA_Only['jet_MOverPt['+str(ipos)+']'][0] = t.jets_mass[pos]/jets_[pos].Pt()
                        mytree.variables['jet_MOverPt'][ipos] = t.jets_mass[pos]/jets_[pos].Pt()
                        mytree.variables['jet_CSV'][ipos] = t.jets_btagCSV[pos]
                        #mytree.variables['jet_DeepCSV'][ipos] = t.jets_btagDeepCSV[pos]
                        #mytree.variables['jet_cMVA'][ipos] = t.jets_btagCMVA[pos]
                        #mytree.variables['jet_DeepcMVA'][ipos] = t.jets_btagDeepCMVA[pos]
                        MVA_Only['jet_QGL['+str(ipos)+']'][0] = t.jets_qgl[pos]
                        mytree.variables['jet_QGL'][ipos] = t.jets_qgl[pos]


                  if comb in corrcomb_ :
                        mytree.variables['hasCorrect'][0] = 1
                  w1.UpdateParam(jets_[comb[2]]+jets_[comb[3]])
                  top1.UpdateParam(jets_[comb[0]]+jets_[comb[3]]+jets_[comb[2]])
                  w2.UpdateParam(jets_[comb[5]]+jets_[comb[4]])
                  top2.UpdateParam(jets_[comb[1]]+jets_[comb[4]]+jets_[comb[5]])
                  b1.UpdateParam(jets_[comb[0]])
                  b2.UpdateParam(jets_[comb[1]])
                  lp1.UpdateParam(jets_[comb[2]])
                  lp2.UpdateParam(jets_[comb[3]])
                  lq1.UpdateParam(jets_[comb[4]])
                  lq2.UpdateParam(jets_[comb[5]])

                  BDT_Value = reader.EvaluateMVA("BDT_Comb")

                  if BDT_Value > bdtcomb:
                        mytree.variables['BDT_Comb'][0] = BDT_Value
                        bdtcomb = BDT_Value
                        bestcomb_=comb
                        if  bestcomb_ in corrcomb_ : mytree.variables['isCorrect'][0] = 1
                        else: mytree.variables['isCorrect'][0] = 0
                              # if sample !='data':
                              #       mytree.variables['n_sumIDtop'][0] = t.jets_mcMatchId[comb[0]]
                              #       mytree.variables['n_sumIDtop'][1] = t.jets_mcMatchId[comb[2]]
                              #       mytree.variables['n_sumIDtop'][2] = t.jets_mcMatchId[comb[3]]
                              #       mytree.variables['n_sumIDtop'][3] = t.jets_mcMatchId[comb[1]]
                              #       mytree.variables['n_sumIDtop'][4] = t.jets_mcMatchId[comb[4]]
                              #       mytree.variables['n_sumIDtop'][5] = t.jets_mcMatchId[comb[5]]

            if len(bestcomb_) == 0: return 0
            # print 'finish comb'
            # watch.Print()

            for ii, c in enumerate(bestcomb_):
                  mytree.variables['best_comb'][ii]=c

            UpdateVariables(bestcomb_,jets_,mytree.variables,MVA_Only)

            b1.UpdateParam(jets_[bestcomb_[0]])
            b2.UpdateParam(jets_[bestcomb_[1]])
            lp1.UpdateParam(jets_[bestcomb_[2]])
            lp2.UpdateParam(jets_[bestcomb_[3]])
            lq1.UpdateParam(jets_[bestcomb_[4]])
            lq2.UpdateParam(jets_[bestcomb_[5]])
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
            #print 'nominal'
            #mytree.Print(useQCD)
            mytree.variables['BDT_CWoLa'][0] = readerQCD.EvaluateMVA("BDT_QCD")

            return 1
      else:return 0



def MeasureSystematics(t,mytree,sys,direc,isSys=1):
      jets_ = ROOT.vector('TLorentzVector')()
      sysvars = ['nBCSVM','qgLR','btagLR4b','BDT_CWoLa','BDT_Comb','prob_chi2','top1_m','n_jets']


      for var in sysvars:
            sysvar = var+sys+direc
            if not mytree.HaveBranch(sysvar):
                  mytree.variables[sysvar]=array('f',[-10])
                  mytree.tree.Branch(sysvar,mytree.variables[sysvar],sysvar+'/F')

      bestcomb_ = []
      bpos_ = []
      jetpos_ =[]
      njets = eval("t.numJets{0}{1}".format(sys,direc))

      mytree.variables['n_jets'][0]=njets
      #mytree.variables['n_jets{0}{1}'.format(sys,direc)][0] = njets
      nbjets = eval("t.nBCSVM{0}{1}".format(sys,direc))
      #print nbjets
      if njets >= 7 and nbjets >=2:

            ntopjets = ntoptaggedjets= 0

            nljets = 0

            for i in range(0,t.njets):#find the b-tagged jets
                  jet = ROOT.TLorentzVector()
                  jet_pt = 0
                  if syst == 'JER':
                        jet_pt = eval("t.jets_pt[i]*t.jets_corr{0}{1}[i]/t.jets_corr_JER[i]".format(syst,direc))
                  else:
                        jet_pt = eval("t.jets_pt[i]*t.jets_corr{0}{1}[i]/t.jets_corr[i]".format(syst,direc))
                  jet.SetPtEtaPhiM(jet_pt,t.jets_eta[i],t.jets_phi[i],t.jets_mass[i])

                  jets_.push_back(jet)


            bdtcomb  =  -999999999
            chi2comb    =  999999999



            mytree.variables['nBCSVM{0}{1}'.format(sys,direc)][0] = nbjets
            mytree.variables['n_jets{0}{1}'.format(sys,direc)][0] = njets
            mytree.variables['qgLR{0}{1}'.format(sys,direc)][0] = -100
            mytree.variables['meanDeltaRbtag'][0] = t.mean_dr_btag
            mytree.variables['btagLR4b{0}{1}'.format(sys,direc)][0] = eval("t.btag_LR_4b_2b_btagCSV{0}{1}".format(sys,direc))

            if nbjets <= 3:
                  mytree.variables['qgLR{0}{1}'.format(sys,direc)][0] = eval('t.qg_LR_3b_flavour_4q_0q{0}{1}'.format(sys,direc))

            if nbjets >= 4:
                  mytree.variables['qgLR{0}{1}'.format(sys,direc)][0] = eval('t.qg_LR_4b_flavour_4q_0q{0}{1}'.format(sys,direc))

            alljets = range(min(t.njets,8))
            allcomb_ = JetComb(min(t.njets,8),0,alljets)

            printing = 0
            highest = 0
            bestcat = 0
            #print comb_, 'comb_'

            # print 'starting comb sys'
            # watch.Print()

            for comb in allcomb_:


                  mytree.variables['simple_chi2'][0] = pow(((jets_[comb[0]] + jets_[comb[2]]+ jets_[comb[3]]).M() - 173.2)/20.5,2) + pow(((jets_[comb[1]] + jets_[comb[4]]+ jets_[comb[5]]).M() - 173.2)/17.8,2) + pow(((jets_[comb[2]]+ jets_[comb[3]]).M() - 82.3)/10.9,2) + pow(((jets_[comb[5]]+ jets_[comb[4]]).M() - 82.3)/10.9,2)
                  if mytree.variables['simple_chi2'][0] < chi2cut:continue
                  mytree.variables['prob_chi2'][0] = TMath.Prob(mytree.variables['simple_chi2'][0],4)
                  #if mytree.variables['prob_chi2'][0] < probcut:return



                  # MVA_Only['top1_m'][0] = (jets_[comb[0]]+jets_[comb[3]]+jet[comb[2]]).M()
                  # MVA_Only['top2_m'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).M()
                  # MVA_Only['tt_m'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]+jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).M()
                  # MVA_Only['tt_pt'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]+jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Pt()

                  # MVA_Only['w1_m'][0] = (jet[comb[2]]+jet[comb[3]]).M()
                  # MVA_Only['w2_m'][0] = (jet[comb[5]]+jet[comb[4]]).M()
                  # MVA_Only['top1_pt'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Pt()
                  # MVA_Only['top2_pt'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).Pt()
                  # MVA_Only['w1_pt'][0] = (jet[comb[2]]+jet[comb[3]]).Pt()
                  # MVA_Only['w2_pt'][0] = (jet[comb[5]]+jet[comb[4]]).Pt()
                  # MVA_Only['b1_pt'][0] = (jet[comb[0]]).Pt()
                  # MVA_Only['b2_pt'][0] = (jet[comb[1]]).Pt()
                  mytree.variables['deltaRp1p2'][0] = jets_[comb[2]].DeltaR(jets_[comb[3]])
                  mytree.variables['deltaPhip1p2'][0] = jets_[comb[2]].DeltaPhi(jets_[comb[3]])
                  mytree.variables['deltaPhib1b2'][0] = jets_[comb[0]].DeltaPhi(jets_[comb[1]])

                  mytree.variables['deltaPhiw1w2'][0] = (jets_[comb[3]]+jets_[comb[2]]).DeltaPhi((jets_[comb[5]]+jets_[comb[4]]))
                  mytree.variables['deltaPhit1t2'][0] = (jets_[comb[0]]+jets_[comb[3]]+jets_[comb[2]]).DeltaPhi((jets_[comb[1]]+jets_[comb[5]]+jets_[comb[4]]))
                  mytree.variables['deltaRq1q2'][0] = jets_[comb[4]].DeltaR(jets_[comb[5]])
                  mytree.variables['deltaPhiq1q2'][0] = jets_[comb[4]].DeltaPhi(jets_[comb[5]])

                  mytree.variables['deltaRb1b2'][0] = jets_[comb[0]].DeltaR(jets_[comb[1]])
                  mytree.variables['deltaRb1w1'][0] = jets_[comb[0]].DeltaR(jets_[comb[3]]+jets_[comb[2]])
                  mytree.variables['deltaRb2w2'][0] = jets_[comb[1]].DeltaR(jets_[comb[4]]+jets_[comb[5]])

                  mytree.variables['deltaEtap1p2'][0] = jets_[comb[2]].Eta() - jets_[comb[3]].Eta()
                  mytree.variables['deltaEtaq1q2'][0] = jets_[comb[4]].Eta() - jets_[comb[5]].Eta()
                  mytree.variables['deltaEtab1b2'][0] = jets_[comb[0]].Eta() - jets_[comb[1]].Eta()
                  mytree.variables['deltaEtaw1w2'][0] = (jets_[comb[3]]+jets_[comb[2]]).Eta() - (jets_[comb[5]]+jets_[comb[4]]).Eta()
                  mytree.variables['deltaEtat1t2'][0] = (jets_[comb[0]]+jets_[comb[3]]+jets_[comb[2]]).Eta() - (jets_[comb[1]]+jets_[comb[5]]+jets_[comb[4]]).Eta()



                  mytree.variables['p1b1_mass'][0] = (jets_[comb[0]] + jets_[comb[2]]).M()
                  mytree.variables['q1b2_mass'][0] = (jets_[comb[1]] + jets_[comb[4]]).M()
                  mytree.variables['deltaRb1p1'][0] = jets_[comb[0]].DeltaR(jets_[comb[2]])
                  mytree.variables['deltaRb2q1'][0] = jets_[comb[1]].DeltaR(jets_[comb[4]])
                  mytree.variables['deltaRb1top2'][0] = jets_[comb[0]].DeltaR(jets_[comb[1]]+jets_[comb[4]]+jets_[comb[5]])
                  mytree.variables['deltaRb2top1'][0] = jets_[comb[1]].DeltaR(jets_[comb[0]]+jets_[comb[2]]+jets_[comb[3]])
                  mytree.variables['deltaRb1w2'][0] = jets_[comb[0]].DeltaR(jets_[comb[4]]+jets_[comb[5]])
                  mytree.variables['deltaRb2w1'][0] = jets_[comb[1]].DeltaR(jets_[comb[2]]+jets_[comb[3]])
                  minrb1p = mytree.variables['deltaRb1p1'][0]
                  minrb2q = mytree.variables['deltaRb2q1'][0]
                  if jets_[comb[0]].DeltaR(jets_[comb[3]]) < minrb1p:
                        minrb1p = jets_[comb[0]].DeltaR(jets_[comb[3]])
                  if jets_[comb[1]].DeltaR(jets_[comb[5]]) < minrb2q:
                        minrb2q = jets_[comb[1]].DeltaR(jets_[comb[5]])
                  mytree.variables['mindeltaRb1p'][0] = minrb1p
                  mytree.variables['mindeltaRb2q'][0] = minrb2q
                  for ipos, pos in enumerate(comb):
                        MVA_Only['jet_CSV['+str(ipos)+']'][0] = t.jets_btagCSV[pos]
                        MVA_Only['jet_MOverPt['+str(ipos)+']'][0] = t.jets_mass[pos]/jets_[pos].Pt()
                        mytree.variables['jet_MOverPt'][ipos] = t.jets_mass[pos]/jets_[pos].Pt()
                        mytree.variables['jet_CSV'][ipos] = t.jets_btagCSV[pos]
                        #mytree.variables['jet_DeepCSV'][ipos] = t.jets_btagDeepCSV[pos]
                        #mytree.variables['jet_cMVA'][ipos] = t.jets_btagCMVA[pos]
                        #mytree.variables['jet_DeepcMVA'][ipos] = t.jets_btagDeepCMVA[pos]
                        MVA_Only['jet_QGL['+str(ipos)+']'][0] = t.jets_qgl[pos]
                        mytree.variables['jet_QGL'][ipos] = t.jets_qgl[pos]
                  w1.UpdateParam(jets_[comb[2]]+jets_[comb[3]])
                  top1.UpdateParam(jets_[comb[0]]+jets_[comb[3]]+jets_[comb[2]])
                  w2.UpdateParam(jets_[comb[5]]+jets_[comb[4]])
                  top2.UpdateParam(jets_[comb[1]]+jets_[comb[4]]+jets_[comb[5]])
                  b1.UpdateParam(jets_[comb[0]])
                  b2.UpdateParam(jets_[comb[1]])
                  lp1.UpdateParam(jets_[comb[2]])
                  lp2.UpdateParam(jets_[comb[3]])
                  lq1.UpdateParam(jets_[comb[4]])
                  lq2.UpdateParam(jets_[comb[5]])


                  BDT_Value = reader.EvaluateMVA("BDT_Comb")

                  if BDT_Value > bdtcomb:
                        mytree.variables['BDT_Comb{0}{1}'.format(sys,direc)][0] = BDT_Value
                        bdtcomb = BDT_Value
                        bestcomb_=comb

            if len(bestcomb_) == 0: return 0
            # print 'finish comb sys'
            # watch.Print()

            UpdateVariables(bestcomb_,jets_,mytree.variables,MVA_Only,True)
            mytree.variables['prob_chi2{0}{1}'.format(sys,direc)][0]= mytree.variables['prob_chi2'][0]
            mytree.variables['BDT_Comb'][0] =mytree.variables['BDT_Comb{0}{1}'.format(sys,direc)][0]
            b1.UpdateParam(jets_[bestcomb_[0]])
            b2.UpdateParam(jets_[bestcomb_[1]])
            lp1.UpdateParam(jets_[bestcomb_[2]])
            lp2.UpdateParam(jets_[bestcomb_[3]])
            lq2.UpdateParam(jets_[bestcomb_[5]])
            w1.UpdateParam(jets_[bestcomb_[2]]+jets_[bestcomb_[3]])
            w2.UpdateParam(jets_[bestcomb_[5]]+jets_[bestcomb_[4]])
            top2.UpdateParam(jets_[bestcomb_[1]]+jets_[bestcomb_[4]]+jets_[bestcomb_[5]])
            top1.UpdateParam(jets_[bestcomb_[0]]+jets_[bestcomb_[2]]+jets_[bestcomb_[3]])
            mytree.variables['top1_m{0}{1}'.format(sys,direc)][0]= top1.mass[0]

            #print 'sys'
            #mytree.Print(useQCD)
            mytree.variables['BDT_CWoLa{0}{1}'.format(sys,direc)][0] = readerQCD.EvaluateMVA("BDT_QCD")

            return 1
      else:return 0



def UpdateVariables(comb,jet,var,MVA_Only,isSys=False):
      var['simple_chi2'][0] = pow(((jet[comb[0]] + jet[comb[2]]+ jet[comb[3]]).M() - 173.2)/20.5,2) + pow(((jet[comb[1]] + jet[comb[4]]+ jet[comb[5]]).M() - 173.2)/17.8,2) + pow(((jet[comb[2]]+ jet[comb[3]]).M() - 82.3)/10.9,2) + pow(((jet[comb[5]]+ jet[comb[4]]).M() - 82.3)/10.9,2)
      if var['simple_chi2'][0] < chi2cut:return
      var['prob_chi2'][0] = TMath.Prob(var['simple_chi2'][0],4)
      #if var['prob_chi2'][0] < probcut:return

      if not isSys:
            addjets = [x for x in range(len(jet)) if x not in comb]
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





      # MVA_Only['top1_m'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).M()
      # MVA_Only['top2_m'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).M()
      # MVA_Only['tt_m'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]+jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).M()
      # MVA_Only['tt_pt'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]+jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Pt()

      # MVA_Only['w1_m'][0] = (jet[comb[2]]+jet[comb[3]]).M()
      # MVA_Only['w2_m'][0] = (jet[comb[5]]+jet[comb[4]]).M()
      # MVA_Only['top1_pt'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Pt()
      # MVA_Only['top2_pt'][0] = (jet[comb[1]]+jet[comb[4]]+jet[comb[5]]).Pt()
      # MVA_Only['w1_pt'][0] = (jet[comb[2]]+jet[comb[3]]).Pt()
      # MVA_Only['w2_pt'][0] = (jet[comb[5]]+jet[comb[4]]).Pt()
      # MVA_Only['b1_pt'][0] = (jet[comb[0]]).Pt()
      # MVA_Only['b2_pt'][0] = (jet[comb[1]]).Pt()
      var['deltaRp1p2'][0] = jet[comb[2]].DeltaR(jet[comb[3]])
      var['deltaPhip1p2'][0] = jet[comb[2]].DeltaPhi(jet[comb[3]])
      var['deltaPhib1b2'][0] = jet[comb[0]].DeltaPhi(jet[comb[1]])

      var['deltaPhiw1w2'][0] = (jet[comb[3]]+jet[comb[2]]).DeltaPhi((jet[comb[5]]+jet[comb[4]]))
      var['deltaPhit1t2'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).DeltaPhi((jet[comb[1]]+jet[comb[5]]+jet[comb[4]]))
      var['deltaRq1q2'][0] = jet[comb[4]].DeltaR(jet[comb[5]])
      var['deltaPhiq1q2'][0] = jet[comb[4]].DeltaPhi(jet[comb[5]])

      var['deltaRb1b2'][0] = jet[comb[0]].DeltaR(jet[comb[1]])
      var['deltaRb1w1'][0] = jet[comb[0]].DeltaR(jet[comb[3]]+jet[comb[2]])
      var['deltaRb2w2'][0] = jet[comb[1]].DeltaR(jet[comb[4]]+jet[comb[5]])

      var['deltaEtap1p2'][0] = jet[comb[2]].Eta() - jet[comb[3]].Eta()
      var['deltaEtaq1q2'][0] = jet[comb[4]].Eta() - jet[comb[5]].Eta()
      var['deltaEtab1b2'][0] = jet[comb[0]].Eta() - jet[comb[1]].Eta()
      var['deltaEtaw1w2'][0] = (jet[comb[3]]+jet[comb[2]]).Eta() - (jet[comb[5]]+jet[comb[4]]).Eta()
      var['deltaEtat1t2'][0] = (jet[comb[0]]+jet[comb[3]]+jet[comb[2]]).Eta() - (jet[comb[1]]+jet[comb[5]]+jet[comb[4]]).Eta()



      var['p1b1_mass'][0] = (jet[comb[0]] + jet[comb[2]]).M()
      var['q1b2_mass'][0] = (jet[comb[1]] + jet[comb[4]]).M()
      var['deltaRb1p1'][0] = jet[comb[0]].DeltaR(jet[comb[2]])
      var['deltaRb2q1'][0] = jet[comb[1]].DeltaR(jet[comb[4]])
      var['deltaRb1top2'][0] = jet[comb[0]].DeltaR(jet[comb[1]]+jet[comb[4]]+jet[comb[5]])
      var['deltaRb2top1'][0] = jet[comb[1]].DeltaR(jet[comb[0]]+jet[comb[2]]+jet[comb[3]])
      var['deltaRb1w2'][0] = jet[comb[0]].DeltaR(jet[comb[4]]+jet[comb[5]])
      var['deltaRb2w1'][0] = jet[comb[1]].DeltaR(jet[comb[2]]+jet[comb[3]])
      minrb1p = var['deltaRb1p1'][0]
      minrb2q = var['deltaRb2q1'][0]
      if jet[comb[0]].DeltaR(jet[comb[3]]) < minrb1p:
            minrb1p = jet[comb[0]].DeltaR(jet[comb[3]])
      if jet[comb[1]].DeltaR(jet[comb[5]]) < minrb2q:
            minrb2q = jet[comb[1]].DeltaR(jet[comb[5]])
      var['mindeltaRb1p'][0] = minrb1p
      var['mindeltaRb2q'][0] = minrb2q
      for ipos, pos in enumerate(comb):
            MVA_Only['jet_CSV['+str(ipos)+']'][0] = t.jets_btagCSV[pos]
            MVA_Only['jet_MOverPt['+str(ipos)+']'][0] = t.jets_mass[pos]/jet[pos].Pt()
            var['jet_MOverPt'][ipos] = t.jets_mass[pos]/jet[pos].Pt()
            var['jet_CSV'][ipos] = t.jets_btagCSV[pos]
            #var['jet_DeepCSV'][ipos] = t.jets_btagDeepCSV[pos]
            #var['jet_cMVA'][ipos] = t.jets_btagCMVA[pos]
            #var['jet_DeepcMVA'][ipos] = t.jets_btagDeepCMVA[pos]
            MVA_Only['jet_QGL['+str(ipos)+']'][0] = t.jets_qgl[pos]
            var['jet_QGL'][ipos] = t.jets_qgl[pos]




if __name__ == "__main__":
      if len(sys.argv) > 2:
            filename = sys.argv[1]
            sample = str(sys.argv[2])
      else: print 'Missing arguments'
      config = ConfigParser.ConfigParser()
      config.optionxform = str
      config.read('all_perm.cfg')


      watch = ROOT.TStopwatch()
      print 'start watch'

      t = ROOT.TChain('tree')
      AddProcessChain(sample,t)
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
      if emax == 0:
            print 'emax == 0'

      reader = TMVA.Reader( "!Color:!Silent" )
      readerQCD = TMVA.Reader( "!Color:!Silent" )

      mytree = ManageTTree(tvars,tkin)

      usevar=[
            'lp1_eta','lp2_eta','lq1_eta','lq2_eta','b1_eta','b2_eta',
            'top1_m','top2_m','w1_m','w2_m','deltaRp1p2','deltaRq1q2',
            'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]',
            'jet_MOverPt[4]','jet_MOverPt[5]','deltaRb1b2','deltaRb1w1',
            'deltaRb2w2','deltaPhiw1w2','deltaPhit1t2','p1b1_mass','q1b2_mass',
            'deltaRb1w2','deltaRb2w1','mindeltaRb1p','simple_chi2','mindeltaRb2q',
            'deltaEtap1p2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]',
            'jet_CSV[3]','jet_CSV[4]','jet_CSV[5]'
      ]
      useQCD = [
            'lp2_pt',
            'lq2_pt',
            'b1_pt',
            'b2_pt',
            'lp1_pt',
            'w2_m',
            'w1_m',
            'top2_m',
            'meanDeltaRbtag',
            'p1b1_mass',
            'deltaRb1b2',
            'jet_CSV[0]',
            'jet_CSV[1]',
            'deltaRb2top1',
            'BDT_Comb',
            'w1_pt',
            'w2_pt'
      ]


      for var in usevar:
            if var in mytree.variables:reader.AddVariable(var,mytree.variables[var])
            else:reader.AddVariable(var,MVA_Only[var])
      reader.AddSpectator('n_jets',mytree.variables['n_jets'])


      for var in useQCD:
            if var in mytree.variables:readerQCD.AddVariable(var,mytree.variables[var])
            else:readerQCD.AddVariable(var,MVA_Only[var])

      weightFileBDT_Comb = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDTP_comb.weights.xml' #30% of sample
      weightFileBDT_QCD = '/mnt/t3nfs01/data01/shome/vmikuni/CMSSW_9_3_0/src/ttbbAnalysis/KinFitter/test/weights/TMVAClassification_BDTCW_QCD_Test_CWoLa.weights.xml'

      reader.BookMVA('BDT_Comb',weightFileBDT_Comb)
      readerQCD.BookMVA('BDT_QCD',weightFileBDT_QCD)
      # print 'starting'
      # watch.Print()

      for e,event in enumerate(t) :
            if e < emin: continue
            if e%100==0: print 'Running entry: ',e, ' of ',emax, ' entries'
            passchi2=0
            pass_nominal = pass_sys = 0
            if sample != 'ttH':
                tthcut_nom = t.json and (t.HLT_ttH_FH or t.HLT_BIT_HLT_PFJet450_v) and t.ht>500 and t.jets_pt[5]>40
            else:tthcut_nom = t.json and (t.HLT_ttH_FH) and t.ht>500 and t.jets_pt[5]>40

            if 'data' not in sample and 'theory' not in sample:
                  for syst in sys_list:

                        for direc in ['Up','Down']:
                              ht = eval("t.ht{0}{1}".format(syst,direc))
                              jetpt5 = 0
                              if syst == 'JER': jetpt5 = eval("t.jets_pt[5]*t.jets_corr{0}{1}[5]/t.jets_corr_JER[5]".format(syst,direc))
                              else: jetpt5 = eval("t.jets_pt[5]*t.jets_corr{0}{1}[5]/t.jets_corr[5]".format(syst,direc))

                              if sample != 'ttH':
                                  tthcut = (t.HLT_ttH_FH or t.HLT_BIT_HLT_PFJet450_v) and ht>500 and jetpt5>40
                              else:tthcut = t.json and (t.HLT_ttH_FH) and ht>500 and jetpt5>40
                              if tthcut:
                                    pass_sys += MeasureSystematics(t,mytree,syst,direc)


            # if pass_sys:
            #      print mytree.variables['BDT_CWoLa'][0]
            #      print ' BDT_Comb'
            #      print '#'*80
            #      for var in usevar:
            #             if var in mytree.variables:print var, mytree.variables[var][0]
            #             else:print var, MVA_Only[var]
            #      print '#'*80
            #      print ' BDT_CWoLa'
            #      print '#'*80
            #      for var in useQCD:
            #             if var in mytree.variables:print var, mytree.variables[var][0]
            #             else:print var, MVA_Only[var]
            #      print '#'*80
            #      print "End of sys"

            # print 'finished sys'
            # watch.Print()

            if tthcut_nom or pass_sys:
                pass_nominal =  MeasureNominal(t,mytree,pass_sys)

            #       print "Look at the previous output!!!!"
            #       print '#'*200
            #       print 'nominal values'
            #       print ' BDT_Comb'
            #       print '#'*80
            #       for var in usevar:
            #              if var in mytree.variables:print var, mytree.variables[var][0]
            #              else:print var, MVA_Only[var]
            #       print '#'*80
            #       print ' BDT_CWoLa'
            #       print '#'*80
            #       for var in useQCD:
            #              if var in mytree.variables:print var, mytree.variables[var][0]
            #              else:print var, MVA_Only[var]
            #       print '#'*80
            #       print "End of nominal"
            if pass_nominal > 0 or pass_sys > 0:

                  tkin.Fill()
                  mytree.ZeroArray()

            # if pass_nominal > 0 or pass_sys > 0:
            #     print 'should all be reset'
            #     mytree.Print()
            if e > emax: break
      watch.Print()
      tkin.Write()
      fout.Write()
      fout.Close()
