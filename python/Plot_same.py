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
save_root = False
cut = '(n_jets>=8 && BDT_Comb>=-1 && qgLR >0)'
weight = 'weight*puweight*btagweight*qgweight*trigweight'

processlist = ['ttbar']

interestVar =['btagLR3b']


plots = {}
for var in interestVar:
    plots[var] = [rt.TH1F(),rt.TH1F(),rt.TH1F(),rt.TH1F(),rt.TH1F()]

def singlePlot(h,var,name,legtext=[]):
    rt.gStyle.SetLegendFont(42)

    c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
    SetupCanvas(c, 0)
    legend = rt.TLegend(x0_l-0.2,y0_l+0.1,x1_l-0.2, y1_l )

    for ihist in range(len(h)):
        #h[ihist].GetYaxis().SetRangeUser(0,0.3)
        yAxis = h[ihist].GetYaxis()
        xAxis = h[ihist].GetXaxis()
        yAxis.SetNdivisions(6,5,0)
        yAxis.SetTitleOffset(1.3)
        yAxis.SetTitleSize(0.05)
        yAxis.SetLabelSize(0.05)
        yAxis.SetTitle("Normalized events")
        xAxis.SetTitle(vartitle[var][0])

        c.cd()

        legend.AddEntry(h[ihist],vartitle[var][0] if len(legtext)==0 else legtext[ihist],'l')
        h[ihist].Draw("histsamex0")


        legend.SetTextSize(0.05)
        legend.Draw('same')

        CMS_lumi.CMS_lumi(c, iPeriod, iPos)

        c.Update()
        c.RedrawAxis()

    if not os.path.exists(destination+ "/"+name):
        os.makedirs(destination+ "/"+name)
    else:
        print "WARNING: directory already exists. Will overwrite existing files..."
    c.SaveAs(destination+ "/"+name+"/"+h[0].GetName()+".pdf")
    if save_root:
        fout = rt.TFile(destination+ "/"+name+"/"+h[0].GetName()+".root","UPDATE")
        for ih in h:
            ih.Write()


files = []
tree = []
hvar = []

for i, f in enumerate(processlist):
    files.append(rt.TFile(processfiles[f],"READ"))
    tree.append(files[i].Get('tree'))
    hprocess = []
    for j, var in enumerate(interestVar):
        #puweight*btagweight*qgWeight*trigWeight(ht,jet5pt,n_bjets)
        if f == 'ttbar':
            for k,proc in enumerate(ttCls):
                print proc
                tree[i].Draw(var + '>>'+ 'h1'+var+str(j)+proc+ str(vartitle[var][1]),weight+"*("+cut+"&&"+ttCls[proc]+")")
                plots[var][k] = rt.gDirectory.Get('h1'+var+str(j)+proc).Clone(f+var+proc)
                plots[var][k].SetLineColor(rt.TColor.GetColor(histFillColor[k]))
                plots[var][k].SetLineWidth(3)
                plots[var][k].Scale(1.0/(plots[var][k].Integral() if plots[var][k].Integral() > 0 else 1.0))

        else:
            tree[i].Draw(var + '>>'+ 'h1'+var+str(j)+ str(vartitle[var][1]),weight+"*("+cut+")")
            plots[var][3] = rt.gDirectory.Get('h1'+var+str(j)).Clone(f+var)
            plots[var][3].SetLineColor(rt.TColor.GetColor(histFillColor[3]))
            plots[var][3].SetLineWidth(3)
            plots[var][3].Scale(1.0/(plots[var][3].Integral() if plots[var][3].Integral() > 0 else 1.0))

        #plots[var][i][0].Sumw2()
        #plots[var][i][0].Divide(plots[var][i][1])


for ivar, var in enumerate(plots):
    print 'variable: ',var
    #singlePlot(plots[var][iproc],1,['Rg.1 '+vartitle[var][0]])
    #singlePlot(plots[var][iproc],1,[proc + ' Rg.1 '+vartitle[var][0], proc + ' Rg.2 '+vartitle[var][0]])
    singlePlot(plots[var],var,'QCD_ttbar',['t#bar{t}bb','t#bar{t}2b','t#bar{t}lf','t#bar{t}cc','t#bar{t}b'])

    #raw_input("Press Enter to end")
