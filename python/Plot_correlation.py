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
save_root = True
cut = '(n_jets>=8 && BDT_Comb>=-1 && qgLR>0 && ttCls<46)'
weight = 'weight*puweight*btagweight*qgweight*trigweight'

processlist = ['ttbar']

#var =['qgLR','nBCSVM']
#var =['qgLR','BDT_CWoLa']
#var =['qgLR','prob_chi2']
#var =['BDT_CWoLa','nBCSVM']
#var =['BDT_CWoLa','prob_chi2']
var =['btagLR4b','trigweight']


plots= {}


def singlePlot(h,name,axistext=[]):

    rt.gStyle.SetPalette(55)
    c = rt.TCanvas('mycv'+h.GetName(),'mycv'+h.GetName(),5,30,W_ref,H_ref)
    SetupCanvas(c, 0)



        #h[ihist].GetYaxis().SetRangeUser(0,0.3)
    yAxis = h.GetYaxis()
    xAxis = h.GetXaxis()
    xAxis.SetTitle(axistext[0])
    yAxis.SetNdivisions(6,5,0)
    yAxis.SetTitle(axistext[1])
    xAxis.SetNdivisions(6,5,0)

    yAxis.SetTitleOffset(1)
    yAxis.SetTitleSize(0.05)



    c.cd()
    pt = rt.TLatex(0.4,0.2,' Correlation: '+str(round(h.GetCorrelationFactor(),2)));
    h.SetMarkerColor(rt.TColor.GetColor(histFillColor[1]))
    h.Draw("histsamex0colz")
    pt.Draw("same")
    c.SetLogz()
    #c.SetLogy()



    CMS_lumi.CMS_lumi(c, iPeriod, iPos)

    c.Update()
    c.RedrawAxis()
    if not os.path.exists(destination+ "/"+name):
        os.makedirs(destination+ "/"+name)
    else:
        print "WARNING: directory already exists. Will overwrite existing files..."
    c.SaveAs(destination+ "/"+name+"/"+h.GetName()+".pdf")
    if save_root:
        fout = rt.TFile(destination+ "/"+name+"/"+h.GetName()+".root","UPDATE")
        h.SetName(var[0]+'_'+var[1])
        h.Write()




files = []
tree = []
hvar = []

for i, f in enumerate(processlist):
    files.append(rt.TFile(processfiles[f],"READ"))
    tree.append(files[i].Get('tree'))
    hprocess = []
    w = weight
    c = cut
    # if f == 'data':
    #     w="(1==1)"
    #     c="n_jets>=8"
    #puweight*btagweight*qgWeight*trigWeight(ht,jet5pt,n_bjets)
    tree[i].Draw(var[1]+':'+var[0] + '>>'+ 'h1'+f+ str(vartitle[var[0]][1]+vartitle[var[1]][1]),weight+"*("+c+")","colz")
    #print var[0]+':'+var[1] + '>>'+ 'h1'+f+ str(vartitle[var[0]][1]+vartitle[var[1]][1]),w+"*("+c+")","colz"

    plots[f] = rt.gDirectory.Get('h1'+f).Clone(f)
    print f, ': ', plots[f].GetCorrelationFactor()
    #plots[var][i][0].Sumw2()
    #plots[var][i][0].Divide(plots[var][i][1])


for ivar, proc in enumerate(plots):
    #singlePlot(plots[var][iproc],1,['Rg.1 '+vartitle[var][0]])
    #singlePlot(plots[var][iproc],1,[proc + ' Rg.1 '+vartitle[var][0], proc + ' Rg.2 '+vartitle[var][0]])
    singlePlot(plots[proc],'Correlation_vars',[vartitle[var[0]][0],vartitle[var[1]][0]])

    #raw_input("Press Enter to end")
