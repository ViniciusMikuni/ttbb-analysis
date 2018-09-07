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
rt.gROOT.LoadMacro("../src/triggerWeightRound.h+")
tdrstyle.setTDRStyle()

#addCut = 'BDT_Comb> 0.657801 && BDT_CWoLa>0.170504 && prob_chi2>0.125174 ' #old iteration

#addCut = 'BDT_Comb>0.969692 && BDT_CWoLa>0.377061 && prob_chi2>0.402731 ' #0.1 eff
#addCut = 'BDT_Comb>0.905339 && BDT_CWoLa>0.409367 && prob_chi2>0.165256' #0.2 eff
#addCut = 'BDT_Comb>0.845594 && BDT_CWoLa>0.130812 && prob_chi2>0.0310777' #0.3 eff
#addCut = 'BDT_Comb>0.742602 && BDT_CWoLa>-0.37912 && prob_chi2>0.0318791 ' #0.4 eff
#addCut = 'BDT_Comb> 0.655242 && BDT_CWoLa>-0.79402 && prob_chi2>0.0121563 ' #0.5 eff
addCut = 'BDT_Comb>0.671697 && BDT_CWoLa>-0.698427 && prob_chi2> -0.00671869 ' #0.6 eff
#addCut = 'BDT_Comb>0.4723 && BDT_CWoLa>-0.828431 && prob_chi2>-0.00229578 ' #0.7 eff
#addCut = 'BDT_Comb>0.185833  && BDT_CWoLa>-0.948532 && prob_chi2>0 ' #0.8 eff
#addCut = 'BDT_Comb>-0.42434 && BDT_CWoLa>-0.986866 && prob_chi2>0 ' #0.9 eff

#addCut = 'prob_chi2 > 0'
#
processlist = ['ttbar','data']
interestVar = ['BDT_ttbb3b','BDT_ttbb7j','BDT_ttbb8j','n_bjets']

table = {}
table['s/b']=['bin 1','bin 2','bin 3','bin 4','bin 5']


files = []
tree = []
hvar = []

for i, f in enumerate(processlist):
    files.append(rt.TFile(processfiles[f],"READ"))    
    tree.append(files[i].Get('tree'))
    hprocess = []
    for j, var in enumerate(interestVar):
        ttbbcut = ' && ttCls >=51'
        if f == 'data':ttbbcut = '&& 1==1'
        tree[i].Draw(var + '>>'+ 'h1'+var+str(j)+ str(vartitle[var][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+ttbbcut + ")")
        hprocess.append(rt.gDirectory.Get('h1'+var+str(j)).Clone(f+var))
    hvar.append(hprocess)



for i, var in enumerate(interestVar):
    #print var
    table[var] = []
    for j in range(hvar[0][i].GetSize()-2):
        s = hvar[0][i].GetBinContent(j+1)*dscale['ttbar']
        #print 'bin: ',j+1, ' s: ',s, ' var ', var
        b = hvar[1][i].GetBinContent(j+1) - s
        table[var].append(float(s)/sqrt(s+b) if (b) > 0 else 0)
        #print 's/b: ',float(s)/b if b > 0 else 0, ' s/sqrt(s + b)', float(s)/sqrt(s+b) if (s+b) > 0 else 0


rows = table.keys()
rows.remove('s/b')
col = table['s/b']
newlist = []
mc = []
for key in rows:
    newlist.append(table[key])

pframe= pd.DataFrame(data=newlist,
                 index=rows,
                 columns=col)

print pframe.to_latex()
    
        

    



    
