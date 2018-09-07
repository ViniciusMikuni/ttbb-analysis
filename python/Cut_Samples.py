import sys
from os import environ, path
import re
import numpy as np
import random
from Plotting_cfg import processfiles
import ROOT
from array import array
nmax = 120000
#samples = {'ttbar':[(24e3,6e3),(36e3,18e3),(12e3,6e3),(24e3,18e3)],'QCD':[(54e3,36e3),(42e3,24e3),(54e3,48e3),(42e3,36e3)]}
samples = {'QCD':[(0e3,30e3),(18e3,27e3),(12e3,21e3),(24e3,27e3),(18e3,21e3),(3e3,12e3),(9e3,18e3),(3e3,6e3),(9e3,12e3),(3e3,18e3),(12e3,27e3),(6e3,27e3),(3e3,24e3)]}
#'ttbar':[(30e3,0e3),(12e3,3e3),(18e3,9e3),(6e3,3e3),(12e3,9e3),(27e3,18e3),(21e3,12e3),(27e3,24e3),(21e3,18e3),(27e3,12e3),(18e3,3e3),(24e3,3e3),(27e3,6e3)],
#samples = {'ttbar':[(27e3,18e3),(21e3,12e3),(27e3,24e3),(21e3,18e3)],'QCD':[(3e3,12e3),(9e3,18e3),(3e3,6e3),(9e3,12e3)]}
#samples = {'QCD':[(0e3,30e3)]}
ROOT.ROOT.EnableImplicitMT()



#samples = {'ttbar':[100],'QCD':[900]}
for sample in samples:
    fi = ROOT.TFile(processfiles[sample],"READ")
    t = fi.Get('tree')
    if sample == 'QCD':
        rg_ = random.sample(xrange(t.GetEntries()),t.GetEntries())
        print 'shuffled QCD'
    else:
        rg_ = np.arange(0,t.GetEntries())
    for nsamples in samples[sample]:
        ftext = sample+'_Nevts_'+str(nsamples[0])+'_'+str(nsamples[1])+'.root'
        print 'Saving file: ',ftext
        fo= ROOT.TFile(ftext,"RECREATE")
        t1 = t.CloneTree(0)
        t1.SetName("Reg1")
        t2 = t.CloneTree(0)
        t2.SetName("Reg2")
        nfills =0

        for event in rg_:
            t.GetEntry(event)
            if (t.jet_CSV[0]>=0 and t.jet_CSV[1]>=0 and t.jet_CSV[2]>=0 and t.jet_CSV[3]>=0 and t.jet_CSV[4]>=0 and t.jet_CSV[5]>=0 and t.meanCSVbtag>0 and t.deltaRb1b2>0 and t.n_jets==7):
                if nfills < nsamples[0]:t1.Fill()
                else:t2.Fill()
                nfills +=1
                
            if nfills >= sum(nsamples): break
        t1.AutoSave()
        t2.AutoSave()
        del fo
    del fi
