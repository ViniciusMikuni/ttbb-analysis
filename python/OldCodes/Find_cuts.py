import os
import sys
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *
from itertools import product
rt.gROOT.SetBatch(True)
rt.gROOT.LoadMacro("triggerWeightRound.h+")




watch = rt.TStopwatch()

npoints = 4
processlist = ['data','ttbar']

interestVar = {
    'BDT_CWoLa':np.arange(-0.85,-0.8,0.05/npoints),
    'BDT_Comb':np.arange(-0.05,0.05,0.1/npoints),
    #'prob_chi2':np.arange(0,0.006,0.006/npoints)
}
makelist = 0
if len(sys.argv) > 1:
    makelist = sys.argv[1]


if makelist:
    cutlist = []
    for var in interestVar:
        cut = []
        for val in interestVar[var]:
            cut.append(var+'[0]>='+str(val))
        cutlist.append(cut)
    with open('allcuts','w') as f:
        for c in list(product(*cutlist)):
            f.write("&&".join(c))
            f.write('\n')

else:
    files = []
    tree = []
    asi = 0
    bestcut = 0
    lines = [line.rstrip('\n') for line in open('allcuts')]

    # for i, fi in enumerate(processlist):
    #     files.append(rt.TFile(processfiles[fi],"READ"))    
    #     tree.append(files[i].Get('tree'))
    rt.ROOT.EnableImplicitMT()
    TDF = rt.ROOT.Experimental.TDataFrame
    dbkg = TDF('tree',processfiles['data'])
    dsig = TDF('tree',processfiles['ttbar'])
    
    # dsig_def = dsig.Define('weights','weight[0]*trigWeight(ht[0],jet5pt[0],n_bjets[0])') \
    #           .Define('var','BDT_Comb[0]') 
    # dbkg_def = dbkg.Define('weights','weight[0]*trigWeight(ht[0],jet5pt[0],n_bjets[0])') \
    #           .Define('var','BDT_Comb[0]') 


    
    for l, c in enumerate(lines):
        if l%100 == 0: print 'reading line: ', l, ' of', len(lines)
        sig = dsig.Filter(c).Count().GetValue()*dscale['ttbar']
        bkg = dbkg.Filter(c).Count().GetValue() - sig
        
        # sigfilter = dsig_def.Filter(c)
        # bkgfilter = dbkg_def.Filter(c)
    
        # hs = sigfilter.Histo1D('var','weights')
        # hb = bkgfilter.Histo1D('var','weights')
        # sig = hs.Integral()*dscale['ttbar']       
        # bkg = hb.Integral() - sig
        
        # tree[1].Draw('n_jets>>'+ 'h1'+str(l),"weight*trigWeight(ht,jet5pt,n_bjets)*("+c+")")
        # sig = rt.gDirectory.Get('h1'+str(l)).Integral()*dscale['ttbar']
        # tree[0].Draw('n_jets>>'+ 'h0'+str(l),"weight*trigWeight(ht,jet5pt,n_bjets)*("+c+")")
        # bkg = rt.gDirectory.Get('h0'+str(l)).Integral()
        # bkg -= sig
        if sig/sqrt(sig+bkg)>asi:
            asi = sig/sqrt(sig+bkg)
            bestcut = l
    print lines[bestcut], 'with significance: ',asi
            
                
    watch.Print()

