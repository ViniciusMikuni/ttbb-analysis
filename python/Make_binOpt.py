import os
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *

#rt.gROOT.SetBatch(True)
tdrstyle.setTDRStyle()


def Compare_Significance(hsig,hbkg,bin):
    s1 = hsig.GetBinContent(bin)
    b1= hbkg.GetBinContent(bin)
    #if (s1+b1)>0: sig1=s1/sqrt(s1+b1)
    if (b1)>0: sig1=s1/b1
    # if (b1)>0:
    #     Z = 2*((s1+b1)*log((s1+b1)/b1)-s1)
    #     absZ = abs(Z)
    #     if absZ != 0:
    #         sig1 = Z*sqrt(absZ)/absZ
    #     else:
    #         sig1 = 0.0

    else:   sig1=0
    s2 = hsig.GetBinContent(bin+1)
    b2= hbkg.GetBinContent(bin+1)
    #if (s2+b2): sig2=s2/sqrt(s2+b2)
    if (b2)>0: sig2=s2/b2
    # if (b2)>0:
    #     Z = 2*((s2+b2)*log((s2+b2)/b2)-s2)
    #     absZ = abs(Z)
    #     if absZ != 0:
    #         sig2 = Z*sqrt(absZ)/absZ
    #     else:
    #         sig2 = 0.0
    else:sig2=0
    #if (s1+s2+b1+b2)>0:sig12=(s1+s2)/sqrt(s1+s2+b1+b2)
    if (b1+b2)>0:sig12=(s1+s2)/(b1+b2)
    # if (b1+b2)>0:
    #     Z = 2*((s1+b1+s2+b2)*log((s1+b1+s2+b2)/(b1+b2))-s1-s2)
    #     absZ = abs(Z)
    #     if absZ != 0:
    #         sig12 = Z*sqrt(absZ)/absZ
    #     else:
    #         sig12 = 0.0
    else: sig12=0
    if sig12> sig1 and sig12>sig2:
        return True
    else:
        return False



processlist = ['ttbar','data']
interestVar = ['btagLR4b']
npoints = 10000
minevts=500
files = {}
tree = {}
weight='weight*puweight*btagweight*trigweight*qgweight*'
add_cut='(BDT_CWoLa>0.36&&qgLR>0.87&&n_jets>=8&&prob_chi2>1e-6&&nBCSVM>=2)'
add_cut_sig='(BDT_CWoLa>0.36&&qgLR>0.87&&ttCls>=51&&n_jets>=8&&prob_chi2>1e-6&&nBCSVM>=2)'
add_cut_bkg='(BDT_CWoLa>0.36&&qgLR>0.87&&ttCls<51&&n_jets>=8&&prob_chi2>1e-6&&nBCSVM>=2)'
binning=np.linspace(0,1,npoints)
for i, f in enumerate(processlist):
    files[f]=rt.TFile(processfiles[f],"READ")
    tree[f]=files[f].Get('tree')
#First step: all bins must have minevts for each bin
for j, var in enumerate(interestVar):
    h0=rt.TH1D("h_opt","h_opt",npoints-1,binning)#change if variable changes
    tree['data'].Draw(var+">>h_opt",add_cut)

    pass_minevts=False
    ntries=0
    while not pass_minevts:
        ntries+=1
        pass_minevts=True
        to_remove=[]
        for bin in range(len(binning)-1):
            if h0.GetBinContent(bin+1) < minevts:
                #print bin+1
                #print  h0.GetBinContent(bin+1)
                #print h0.GetBinLowEdge(bin+2)
                pass_minevts=False
                #to_remove=binning[bin+1]
                #print to_remove
                #print 'before',binning
                #index = np.argwhere(binning==to_remove)
                new_bin=np.delete(binning,bin+1)
                #print 'after', new_bin
                new_binning=array.array('d',new_bin)
                break
        hnew=h0.Rebin(len(new_binning)-1,'h_opt_{0}'.format(ntries),new_binning)
        binning=new_binning
        h0=hnew
    print len(binning)
    print binning
    hsig=h0.Clone('hopt_sig')
    hbkg=h0.Clone('hopt_bkg')
    hsig.Reset()
    hbkg.Reset()
    tree['ttbar'].Draw(var+">>hopt_sig",weight+add_cut_sig)
    tree['ttbar'].Draw(var+">>hopt_bkg",weight+add_cut_bkg)
    pass_minsig=False
    ntries=0
    while not pass_minsig:
        ntries+=1
        pass_minsig=True
        for bin in range(len(binning)-1):
            pass_significance=Compare_Significance(hsig,hbkg,bin+1)
            if pass_significance:
                #print bin+1
                #print  h0.GetBinContent(bin+1)
                #print h0.GetBinLowEdge(bin+2)
                pass_minsig=False
                #to_remove=binning[bin+1]
                #print to_remove
                #print 'before',binning
                #index = np.argwhere(binning==to_remove)
                new_bin=np.delete(binning,bin+1)
                #print 'after', new_bin
                new_binning=array.array('d',new_bin)
                break
        hnew_s=hsig.Rebin(len(new_binning)-1,'hsig_{0}'.format(ntries),new_binning)
        hnew_b=hbkg.Rebin(len(new_binning)-1,'hbkg{0}'.format(ntries),new_binning)
        binning=new_binning
        hsig=hnew_s
        hbkg=hnew_b
    print len(binning)
    print binning

    hsig.Draw("hist")
    #hbkg.Draw("histsame")
    raw_input("hist")
