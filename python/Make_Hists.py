#Plotting.py
import os
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *
import pandas as pd

rt.gROOT.SetBatch(True)
rt.gROOT.LoadMacro("triggerWeightRound.h+")
tdrstyle.setTDRStyle()

addCut = 'BDT_Comb> 0.657801 && BDT_CWoLa>0.170504 && prob_chi2>0.125174 '
#addCut = 'prob_chi2 > 0'
#
processlist = ['data','ttbar','diboson','ttV','VJ','s_top','QCD']
hname = {'data':'data_obs','ttlf':'ttlf','diboson':'VV','ttV':'ttV','VJ':'VJ','s_top':'s_top','QCD':'QCD','ttcc':'ttcc','ttbb':'ttbb','tt2b':'tt2b','ttb':'ttb'}
interestVar = ['n_bjets']
files = {}
tree = {}
hvar = []
hlist = []

for iproc, process in enumerate(processlist): #ntuple files
    if process in processgroup:
        for subprocess in processgroup[process]:
            files[subprocess]=rt.TFile(processfiles[subprocess],"READ")
            tree[subprocess]= files[subprocess].Get('tree')
    elif process == 'ttbar':
        for tproc in ttplot:
            files[tproc]=rt.TFile(processfiles[process],"READ")
            tree[tproc]= files[tproc].Get('tree')
    else:
        files[process] =rt.TFile(processfiles[process],"READ") 
        tree[process] =files[process].Get('tree')


#print tree.keys()        
for j, var in enumerate(interestVar):
    for proc in hname:
        if proc == 'QCD':continue
        if proc in ttplot:
            tree[proc].Draw(var + '>>'+ 'h'+proc+ str(vartitle[var][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+ttCls[proc] + ")")
            h = rt.gDirectory.Get('h'+proc).Clone(hname[proc])
            h.Scale(dscale['ttbar'])
            hlist.append(h)
        elif proc in processgroup:
            for isub, subprocess in enumerate(processgroup[proc]):
                tree[subprocess].Draw(var + ">>" + "h"+subprocess+str(vartitle[var][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+")")
                if isub == 0:
                    h = rt.gDirectory.Get('h'+subprocess).Clone(hname[proc])
                    h.Scale(dscale[subprocess])
                else:
                    hsub = rt.gDirectory.Get('h'+subprocess).Clone(subprocess)
                    hsub.Scale(dscale[subprocess])
                    h.Add(hsub)
            hlist.append(h)
        else:
            tree[proc].Draw(var + '>>'+ 'h'+proc+str(vartitle[var][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+")")
            h = rt.gDirectory.Get('h'+proc).Clone(hname[proc])
            h.Scale(dscale[proc])
            hlist.append(h)
                
                
    nbkg = 0
    ndata = 0
    for h in hlist:
        if h.GetName() == 'data_obs':ndata = h.Integral()
        else: nbkg+=h.Integral()


    tree['QCD'].Draw(var + '>>'+ 'hQCD'+str(vartitle[var][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+")")
    hqcd = rt.gDirectory.Get('hQCD').Clone(hname['QCD'])
    nqcd = hqcd.Integral()
    print (ndata-nbkg)/nqcd
    hqcd.Scale((ndata-nbkg)/nqcd)
    hlist.append(hqcd)
fout = rt.TFile('hCard.root','RECREATE')
for h in hlist:h.Write()

    



    
