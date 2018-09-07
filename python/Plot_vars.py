#Plotting.py
import os
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *

rt.gROOT.SetBatch(True)
tdrstyle.setTDRStyle()

cut = '(n_jets>=8 && btagweight>=0)'
weight = 'weight*puweight*btagweight*qgweight*trigweight'

processlist = ['ttbar']

interestVar =['BDT_CWoLa','BDT_CWoLa_RelativeJEREC1Up','BDT_CWoLa_RelativeJEREC1Down']


plots = {processlist[0]:[]}
for var in interestVar:
    plots[processlist[0]].append(rt.TH1F())

def singlePlot(h,name,legtext=[]):
    rt.gStyle.SetLegendFont(42)

    c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
    SetupCanvas(c, 0)
    legend = rt.TLegend(x0_l-0.3,y0_l+0.1,x1_l-0.3, y1_l )

    for ihist in range(len(h)):
        #h[ihist].GetYaxis().SetRangeUser(0,0.3)
        yAxis = h[ihist].GetYaxis()
        yAxis.SetNdivisions(6,5,0)
        yAxis.SetTitleOffset(1)
        yAxis.SetTitleSize(0.05)


        c.cd()

        legend.AddEntry(h[ihist],vartitle[interestVar[ihist]][0] if len(legtext)==0 else legtext[ihist],'l')
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
    c.SaveAs(destination+ "/"+name+"/"+h[0].GetName()+".pdf")



files = []
tree = []
hvar = []

for i, f in enumerate(processlist):
    files.append(rt.TFile(processfiles[f],"READ"))
    tree.append(files[i].Get('tree'))
    hprocess = []
    for j, var in enumerate(interestVar):
        #puweight*btagweight*qgWeight*trigWeight(ht,jet5pt,n_bjets)
        tree[i].Draw(var + '>>'+ 'h1'+var+str(j)+ str(vartitle[interestVar[0]][1]),weight+"*("+cut+"&&"+var+">=-1)")
        print weight+"*("+cut+"&&"+var+">=-1)"

        plots[f][j] = rt.gDirectory.Get('h1'+var+str(j)).Clone(f+var)
        plots[f][j].SetLineColor(rt.TColor.GetColor(histFillColor[j]))
        plots[f][j].SetLineWidth(3)
        plots[f][j].Scale(1.0/(plots[f][j].Integral() if plots[f][j].Integral() > 0 else 1.0))
        #plots[var][i][0].Sumw2()
        #plots[var][i][0].Divide(plots[var][i][1])

singlePlot(plots[processlist[0]],'ttbar_sys',interestVar)

    #raw_input("Press Enter to end")
