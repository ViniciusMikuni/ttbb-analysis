import os
import sys
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *
#rt.gROOT.SetBatch(True)
import  tdrstyle
import CMS_lumi
import pandas as pd
tdrstyle.setTDRStyle()
#HEADS UP: CURRENTLY WE NEED AND OFFSET UNTIL THE NEXT SET OF MC IS DONE
offset = 0
sys_list=[
        '_btagweight_hf',
        '_btagweight_cferr1',
        '_btagweight_cferr2',
        '_btagweight_lf',
        '_btagweight_lfstats2',
        '_btagweight_lfstats1',
        '_btagweight_hfstats2',
        '_btagweight_hfstats1',
        '_btagweight_jes',
        '_puweight',
        '_trigweight',
        #'_qgweight',
        '_RelativeStatEC',
        '_RelativeStatHF',
        '_PileUpDataMC',
        '_PileUpPtRef',
        '_PileUpPtBB',
        '_PileUpPtEC1',
        '_PileUpPtEC2',
        '_PileUpPtHF',
        '_RelativeStatFSR',
        '_RelativeFSR',
        '_AbsoluteScale',
        '_AbsoluteFlavMap',
        '_AbsoluteMPFBias',
        '_Fragmentation',
        '_SinglePionECAL',
        '_SinglePionHCAL',
        '_FlavorQCD',
        '_TimePtEta',
        '_RelativeJEREC1',
        '_RelativeJEREC2',
        '_RelativeJERHF',
        '_RelativePtBB',
        '_RelativePtEC1',
        '_RelativePtEC2',
        '_RelativePtHF',
        '_SubTotalPileUp',
        '_JER',
        '_AbsoluteStat',
        '_Total'
]
direction = ["Up","Down"]
tree={}
files={}
variables = ['BDT_CWoLa'] #order kinda matters
processlist=['ttbar']
addCut='n_jets>7&&BDT_CWoLa>=-1&&prob_chi2>1e-6'
weight='weight*puweight*btagweight*qgweight*trigweight'
destination='../Plots/Sys_selector'
for iproc, process in enumerate(processlist): #ntuple files
    files[process]=rt.TFile(processfiles[process],"READ")
    tree[process] = files[process].Get('tree')
for var in variables:
    nbins=vartitle[var][1][0]-1
    std_={}
    tree[processlist[0]].Draw(var+ '>>'+ 'hnom'+var+ str(vartitle[var][1]),weight+'*('+addCut+')')
    hnominal= rt.gDirectory.Get('hnom'+var).Clone('nominal'+var)
    hnominal.Sumw2()
    th1={}
    for b in range(nbins):th1[str(b+1)]=rt.TH1D(var+str(b+1),var+str(b+1),100,-5,5)

    # for b in range(nbins):th1[str(b+1)]=rt.TH1D(var+str(b+1),var+str(b+1),100,8000,int(0.07*hnominal.Integral(b+1,hnominal.GetSize()-2)*dscale['ttbar']))
    is_weight=0
    for sys in sys_list:
        std_[sys]={}
        if 'weight' in sys:
            is_weight=1
        else:
            is_weight=0
        for direc in direction:
            if is_weight:
                addCutSys='n_jets>7&&BDT_CWoLa>=-1&&prob_chi2>1e-6'
                weight_name = sys[1:].partition('_')[0] #btagweight
                weight_sys = weight.replace(weight_name,sys[1:]+'_'+direc)

            else:
                addCutSys='n_jets{0}{1}>7&&BDT_CWoLa{0}{1}>=-1&&prob_chi2{0}{1}>1e-6'.format(sys,direc)
                weight_sys=weight

            if is_weight:
                tree[processlist[0]].Draw(var +'>>'+ 'h'+sys+direc+var+ str(vartitle[var][1]),weight_sys+'*('+addCutSys+'&&'+var+'>=-1)')
            else:
                tree[processlist[0]].Draw(var+sys+direc +'>>'+ 'h'+sys+direc+var+ str(vartitle[var][1]),weight_sys+'*('+addCutSys+'&&'+var+sys+direc+'>=-1)')
                #print var+sys+direc +'>>'+ 'h'+sys+direc+var+ str(vartitle[var][1]),weight_sys+'*('+addCutSys+'&&'+var+sys+direc+'>=-1)'
            hsys= rt.gDirectory.Get('h'+sys+direc+var).Clone('sys'+var+sys+direc)
            for bin in range(nbins):
                nominal=hnominal.Integral(bin+1,hnominal.GetSize()-2)*dscale[processlist[0]]
                nsys=hsys.Integral(bin+1,hsys.GetSize()-2)*dscale[processlist[0]]
                #print 'nom',nominal, ' nsys ',nsys
                #print 'nom',nominal,' nsys ',nsys
                #print nominal-nsys, is_weight

                if is_weight:
                    th1[str(bin+1)].Fill((nominal-nsys)/nominal if nominal>0 else 0)
                else:
                    th1[str(bin+1)].Fill((nominal-nsys-offset)/nominal if nominal>0 else 0)
                std_[sys][str(bin+1)] = (nominal-nsys-offset)/nominal if nominal>0 else 0


    th1['50'].GetXaxis().SetNdivisions(6,5,0)
    th1['50'].GetXaxis().SetTitle('#Delta(n_{nominal})')
    print 'std: ',th1['50'].GetStdDev(), ' err: ',th1['50'].GetStdDevError()
    th1['50'].Draw()
    raw_input('here we go again')
    df=pd.DataFrame.from_dict(std_)
    with open('std','w') as f:
        df.to_csv(f,sep=' ')
        #f.write(df)

    std = []
    stderr=[]
    #x = np.linspace(vartitle[var][1][1],vartitle[var][1][2],vartitle[var][1][0])
    print vartitle[var][1][0],vartitle[var][1][1],vartitle[var][1][2]

    h=rt.TH1D(var,var,nbins,vartitle[var][1][1],vartitle[var][1][2])
    for j in range(1,nbins+1):
        std.append(th1[str(j)].GetStdDev())
        stderr.append(th1[str(j)].GetStdDevError())
        h.SetBinContent(j,th1[str(j)].GetStdDev())
        h.SetBinError(j,th1[str(j)].GetStdDevError())

    c = rt.TCanvas(var,var,5,30,W_ref,H_ref)
    SetupCanvas(c, 0)
    h.GetYaxis().SetRangeUser(0.01,0.03)
    h.GetYaxis().SetNdivisions(6,5,0)
    h.Draw("samex0")
    h.GetXaxis().SetTitle(vartitle[var][0])
    CMS_lumi.CMS_lumi(c, iPeriod, iPos)
    c.Update()
    c.RedrawAxis()

    #h.SetTitle(vartitle[var][0])
    if not os.path.exists(destination):
        os.makedirs(destination)
    else:
        print "WARNING: directory already exists. Will overwrite existing files..."
    c.SaveAs(destination+ "/"+var+".pdf")
