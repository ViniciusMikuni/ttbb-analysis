#Plotting.py
import os
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *

rt.gROOT.SetBatch(False)
rt.gROOT.LoadMacro("triggerWeightRound.h+")
tdrstyle.setTDRStyle()


processlist = ['ttbar','QCD']
interestVar = ['BDT_CWoLa','BDT_Comb','prob_chi2','qgLR']
addCut = 'qgLR>=0'
npoints = 100
plots = {'Signf':[],
         'Var':[],
         'ROC':[]
}
for var in interestVar:
    plots['Signf'].append(rt.TH1F('Signf'+var,'Signf;'+vartitle[var][0]+';#frac{S}{#sqrt{S+B}}',npoints,vartitle[var][1][1],vartitle[var][1][2]))
    plots['Var'].append([rt.TH1F('QCD'+var,'QCD;'+vartitle[var][0]+';',vartitle[var][1][0],vartitle[var][1][1],vartitle[var][1][2]),rt.TH1F('ttbar'+var,'ttbar;'+vartitle[var][0]+';',vartitle[var][1][0],vartitle[var][1][1],vartitle[var][1][2])])
    plots['ROC'].append(rt.TH1F('ROC'+var,'ROC;Bkg. acceptance;Sig. acceptance',npoints,0,1))



def singlePlot(h,same,legtext=[]):
    rt.gStyle.SetLegendFont(42)
    if same:
        c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
        SetupCanvas(c, 0)
        legend = rt.TLegend(x0_l-0.3,y0_l,x1_l-0.3, y1_l)

    for ihist in range(len(h)):
        #h[ihist].Scale(1.0/h[ihist].Integral())
        #h[ihist].SetMaximum(max(h[len(h)-1].GetMaximum()*0.5,0))
        #h[ihist].GetYaxis().SetRangeUser(0,0.4e5)
        h[ihist].SetMinimum(0.0)
        yAxis = h[ihist].GetYaxis()
        yAxis.SetNdivisions(6,5,0)
        yAxis.SetTitleOffset(1)
        yAxis.SetTitleSize(0.05)

        if not same:
            c = rt.TCanvas('mycv'+h[ihist].GetName(),'mycv'+h[ihist].GetName(),5,30,W_ref,H_ref)
            SetupCanvas(c, 0)
            h[ihist].Draw('histx0')
            CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        
            c.Update()
            c.RedrawAxis()

            if not os.path.exists(destination+ "/"+addCut):
                os.makedirs(destination+ "/"+addCut)
            else:
                print "WARNING: directory already exists. Will overwrite existing files..."
            c.SaveAs(destination+ "/"+addCut+"/"+h[ihist].GetName()+".png")
            
        if same:
            c.cd()

            legend.AddEntry(h[ihist],vartitle[interestVar[ihist]][0] if len(legtext)==0 else legtext[ihist],'l')
            h[ihist].DrawNormalized("histsamex0")
            
    if same:
        legend.SetTextSize(0.03)
        legend.Draw('samex0')

        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        
        c.Update()
        c.Modified()
        c.RedrawAxis()

        if not os.path.exists(destination+ "/"+addCut):
            os.makedirs(destination+ "/"+addCut)
        else:
            print "WARNING: directory already exists. Will overwrite existing files..."
        c.SaveAs(destination+ "/"+addCut+"/"+h[0].GetName()+".png")






        
def MakeROC(hROC,hsig,hbkg,icolor):
    nsig = hsig.Integral()
    nbkg = hbkg.Integral()
    hROC.SetLineColor(rt.TColor.GetColor(histFillColor[icolor])) 
    hROC.SetLineWidth(2)

    for point in range(hsig.GetSize()-2):
        sig = hsig.Integral(point+1,hsig.GetSize()-2)
        bkg = hbkg.Integral(point+1,hsig.GetSize()-2)
        
        xAxis = hROC.GetXaxis()
        x =  xAxis.FindBin(bkg/nbkg)
        hROC.SetBinContent(x,sig/nsig)
    
    print 'AUC: ',hROC.Integral()


def MakeSignificance(hAsi,hsig,hbkg):
    hAsi.SetLineColor(8) 
    hAsi.SetLineWidth(2)
    for point in range(hAsi.GetSize()-2):
        x = hAsi.GetBinCenter(point+1)
        binx = hsig.FindBin(x)
        sig = hsig.Integral(binx,hsig.GetSize()-2)*float(dscale['ttbar'])
        total = hbkg.Integral(binx,hsig.GetSize()-2) 
        
        hAsi.SetBinContent(point+1,sig/sqrt(total) if total > 0 else 0.0)
    maxbin = hAsi.GetMaximumBin()
    #print maxbin
    print 'max significance at: ',hAsi.GetBinCenter(maxbin)

    
    
files = []
tree = []
hvar = []
for i, f in enumerate(processlist):
    files.append(rt.TFile(processfiles[f],"READ"))    
    tree.append(files[i].Get('tree'))
    hprocess = []
    for j, var in enumerate(interestVar):
        tree[i].Draw(var + '>>'+ 'h'+var+str(j)+ str(vartitle[var][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+")")
        hprocess.append(rt.gDirectory.Get('h'+var+str(j)))
    hvar.append(hprocess)
    

hROC = []
for i, var in enumerate(interestVar):
    plots['Var'][i][0] = hvar[1][i].Clone('QCD'+var)
    plots['Var'][i][0].SetLineColor(2)
    plots['Var'][i][0].SetLineWidth(2)
    plots['Var'][i][1] = hvar[0][i].Clone('ttbar'+var)
    plots['Var'][i][1].SetLineColor(4)

    plots['Var'][i][1].SetLineWidth(2)

    MakeROC(plots['ROC'][i],hvar[0][i],hvar[1][i],i)
    #MakeSignificance(plots['Signf'][i],hvar[1][i],hvar[0][i])



# singlePlot(plots['Signf'],0)
singlePlot(plots['ROC'],1)
for ivar, var in enumerate(plots['Var']):
   singlePlot(var,1,['QCD '+vartitle[interestVar[ivar]][0],'t#bar{t} '+vartitle[interestVar[ivar]][0]])
    
   raw_input("Press Enter to end")                            



