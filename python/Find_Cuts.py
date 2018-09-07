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

npoints = 2
ntrials = 2
processlist = ['data','ttbar']

interestVar = {
    'BDT_CWoLa':np.arange(-1,1,2.0/npoints),
    'BDT_Comb':np.arange(-1,1,2/npoints),
    #'prob_chi2':np.arange(0,0.006,0.006/npoints)
}


def MakeCuts(rangelist):
    cutlist = []
    allcuts = []
    for var in interestVar:
        cut = []
        for val in rangelist[var]:
            cut.append(var+'[0]>='+str(val))
        cutlist.append(cut)

    for c in list(product(*cutlist)):
        allcuts.append("&&".join(c))
    return allcuts

else:
    files = []
    tree = []
    asi = 0
    bestcut = 0


    rt.ROOT.EnableImplicitMT()
    TDF = rt.ROOT.Experimental.TDataFrame
    dbkg = TDF('tree',processfiles['data'])
    dsig = TDF('tree',processfiles['ttbar'])
    allcuts = MakeCuts(interestVar)
    for i in range(ntrials):
        for l, c in enumerate(allcuts):
            sig = dsig.Filter(c).Count().GetValue()*dscale['ttbar']
            bkg = dbkg.Filter(c).Count().GetValue() - sig

            if sig/sqrt(sig+bkg)>asi:
                asi = sig/sqrt(sig+bkg)
                bestcut = l

        print allcuts[bestcut], 'with significance: ',asi


    watch.Print()
