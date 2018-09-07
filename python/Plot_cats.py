#Plotting.py
import os
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *
from collections import OrderedDict
#rt.gROOT.SetBatch(True)
tdrstyle.setTDRStyle()


def singlePlot(h,name,legtext=[]):
    rt.gStyle.SetLegendFont(42)

    c = rt.TCanvas('mycv','mycv',5,30,W_ref,H_ref)
    SetupCanvas(c, 0)
    legend = rt.TLegend(x0_l,y0_l+0.1,x1_l, y1_l )

    for ihist in h:
        h[ihist].GetYaxis().SetRangeUser(0,30000)
        yAxis = h[ihist].GetYaxis()
        yAxis.SetNdivisions(6,5,0)
        yAxis.SetTitleOffset(1)
        yAxis.SetTitleSize(0.05)


        c.cd()

        legend.AddEntry(h[ihist],ihist,'l')
        h[ihist].Draw("histsamex0")


        legend.SetTextSize(0.03)
        legend.Draw('same')

        CMS_lumi.CMS_lumi(c, iPeriod, iPos)

        c.Update()
        c.RedrawAxis()

    if not os.path.exists(destination+ "/"+name):
        os.makedirs(destination+ "/"+name)
    else:
        print "WARNING: directory already exists. Will overwrite existing files..."
    c.SaveAs(destination+ "/"+name+"/cat.pdf")


cut = '(n_jets>=8 && BDT_CWoLa>0.36 && qgLR>0.87)'
weight = 'weight*puweight*btagweight*qgweight*trigweight'

processlist = ['ttbar_fast']

cats=['ttlf','ttcc','ttb','ttbb','tt2b']
nominal=[1,1,1,1,1]
up=[1.11,1.06,1.11,1.036,1.08]
down=[0.99,0.99,0.97,0.97,0.98]
dcats=OrderedDict()
dhist = {
    'nominal':rt.TH1F('nominal','nominal',len(cats),1,len(cats)+1),
    'up':rt.TH1F('up','up',len(cats),1,len(cats)+1),
    'down':rt.TH1F('down','down',len(cats),1,len(cats)+1),
}

for icat, cat in enumerate(cats):
    dcats[cat]= {'nominal':nominal[icat],'up':up[icat],'down':down[icat]}

files = []
tree = []
hvar = []

for i, f in enumerate(processlist):
    files.append(rt.TFile(processfiles[f],"READ"))
    tree.append(files[i].Get('tree'))
    hprocess = []
    for j, cat in enumerate(dcats):
        for k, hist in enumerate(dhist):
            tree[i].Draw("BDT_Comb>>"+'h'+hist+cat,weight+"*("+cut+"&&"+ttCls[cat]+"&&BDT_CWoLa>=-1)")
            h=rt.gDirectory.Get('h'+hist+cat).Integral()*dscale[f]*dcats[cat][hist]
            dhist[hist].SetBinContent(j+1,h)
            dhist[hist].GetXaxis().SetBinLabel(j+1,cat)
            dhist[hist].GetYaxis().SetMaxDigits(5)
            dhist[hist].SetLineColor(rt.TColor.GetColor(histFillColor[k]))
            dhist[hist].SetLineWidth(3)


#raw_input("Press Enter to end")            
singlePlot(dhist,'ttbar_cat')

    #raw_input("Press Enter to end")
