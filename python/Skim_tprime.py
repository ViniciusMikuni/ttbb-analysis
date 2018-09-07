import os
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from itertools import permutations, combinations
from Plotting_cfg import *
from Skim_cfg import ManageTTree
import numpy as np
from math import *
import numpy as np
import pandas as pd
rt.gROOT.SetBatch(True)
tdrstyle.setTDRStyle()





def JetComb(njets):
    '''return all the combinations for jet  positioning'''
    jetpos_=range(njets)
    jetpermut_ = list(permutations(jetpos_,4))#permutations of all jets
    completelist_ = []
    for i in range(len(jetpermut_)):
        if (jetpermut_[i][0] > jetpermut_[i][1] or jetpermut_[i][2] > jetpermut_[i][3]): continue
        completelist_.append(jetpermut_[i])
    #print completelist_, ' complete list ',
    return completelist_
        
    
    
files = ['ttbar']
f = {}
t = {}
fout={}
for fi in files:
    
    f[fi]=rt.TFile(processfiles[fi],"READ")
    t[fi]=f[fi].Get('tree')
    
    fout[fi] = rt.TFile('../Datasets/'+fi+'_tprime.root','recreate')

vlist={
    'chi2':[1,'F'],
    'top1_m':[1,'F'],
    'top2_m':[1,'F'],
    'h1_m':[1,'F'],
    'h2_m':[1,'F'],
    'tprime1_m':[1,'F'],
    'tprime2_m':[1,'F'],
    'BDT_CWoLa':[1,'F'],
    'qgLR':[1,'F'],
    'nBCSVM':[1,'F'],
    'weight':[1,'F'],
    'puweight':[1,'F'],
    'btagweight':[1,'F'],
    'qgweight':[1,'F'],
    'trigweight':[1,'F'],
    'topweight':[1,'F'],
    'ttCls':[1,'F'],
    }


for fi in files:
    tkin =  rt.TTree("tree","tree")
    mytree = ManageTTree(vlist,tkin)
    emax = t[fi].GetEntries()
    for e, event in enumerate(t[fi]):
        if e% 10000 == 0:
            print 'reading event: ',e, ' out of ', emax
        if t[fi].n_jets<10 or t[fi].BDT_Comb < -1 or t[fi].prob_chi2<1e-6:continue
        jets_ = rt.vector('TLorentzVector')()
        for i in range(int(t[fi].n_addJets)):
            jet = rt.TLorentzVector()
            jet.SetPtEtaPhiM(t[fi].addJet_pt[i],t[fi].addJet_eta[i],t[fi].addJet_phi[i],t[fi].addJet_mass[i])
            jets_.push_back(jet)

        all_comb_ = JetComb(int(t[fi].n_addJets))
        minchi2=1e9
        best_comb=[]
        for comb in all_comb_:
            h1 = jets_[comb[0]] + jets_[comb[1]]
            h2 = jets_[comb[2]] + jets_[comb[3]]
            chi2 = (h1.M()-125)**2/(13.5)**2 + (h2.M()-125)**2/(13.5)**2
            
            if chi2<minchi2:
                best_comb=comb
                minchi2=chi2
        mytree.variables['chi2'][0]=chi2
        mytree.variables['top1_m'][0]=t[fi].top1_m
        mytree.variables['top2_m'][0]=t[fi].top2_m
        mytree.variables['h1_m'][0]=(jets_[best_comb[0]] + jets_[best_comb[1]]).M()
        mytree.variables['h2_m'][0]=(jets_[best_comb[2]] + jets_[best_comb[3]]).M()
        top1=rt.TLorentzVector()
        top1.SetPtEtaPhiM(t[fi].top1_pt,t[fi].top1_eta,t[fi].top1_phi,t[fi].top1_m)
        top2=rt.TLorentzVector()
        top2.SetPtEtaPhiM(t[fi].top2_pt,t[fi].top2_eta,t[fi].top2_phi,t[fi].top2_m)
        h1=jets_[best_comb[0]] + jets_[best_comb[1]]
        h2=jets_[best_comb[2]] + jets_[best_comb[3]]
        if top1.DeltaR(h1) < top2.DeltaR(h1):
            tprime1=top1+h1
            tprime2=top2+h2
        else:
            tprime1=top1+h2
            tprime2=top2+h1
        mytree.variables['tprime1_m'][0]=tprime1.M()
        mytree.variables['tprime2_m'][0]=tprime2.M()
        mytree.variables['BDT_CWoLa'][0]=t[fi].BDT_CWoLa
        mytree.variables['qgLR'][0]=t[fi].qgLR
        mytree.variables['nBCSVM'][0]=t[fi].nBCSVM
        mytree.variables['weight'][0]=t[fi].weight
        mytree.variables['puweight'][0]=t[fi].puweight
        mytree.variables['btagweight'][0]=t[fi].btagweight
        mytree.variables['qgweight'][0]=t[fi].qgweight
        mytree.variables['trigweight'][0]=t[fi].trigweight
        mytree.variables['topweight'][0]=t[fi].topweight
        mytree.variables['ttCls'][0]=t[fi].ttCls
        tkin.Fill()

    
    fout[fi].cd()
    tkin.Write()
    fout[fi].Write()
    fout[fi].Close()
    
