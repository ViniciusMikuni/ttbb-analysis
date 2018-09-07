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
rt.gROOT.LoadMacro("../src/triggerWeightRound.h+")
tdrstyle.setTDRStyle()


processlist = ['ttbar','data']
interestVar = ['BDT_CWoLa','qgLR']
#addCut = 'n_jets>=8&&n_bjets>=3'
#addCut = 'n_jets>7'
addCut = 'n_jets>7 && BDT_CWoLa>=-1&&BDT_Comb>=-1&&qgLR>0&&nBCSVM>=2'
npoints = 500
plots = {'Signf':[],
         'Var':[],
         'ROC':[]
}
for var in interestVar:
    #plots['Signf'].append(rt.TH1F('Signf'+var,'Signf;'+vartitle[var][0]+';#frac{S}{#sqrt{S+B}}',npoints,vartitle[var][1][1],vartitle[var][1][2]))
    #plots['Var'].append([rt.TH1F('QCD'+var,'QCD;'+vartitle[var][0]+';',vartitle[var][1][0],vartitle[var][1][1],vartitle[var][1][2]),rt.TH1F('ttbar'+var,'ttbar;'+vartitle[var][0]+';',vartitle[var][1][0],vartitle[var][1][1],vartitle[var][1][2])])
    plots['ROC'].append(rt.TH1F('ROC'+var,'ROC;Bkg. acceptance;Sig. acceptance',npoints,0,1))



def singlePlot(h,same,legtext=[]):
    rt.gStyle.SetLegendFont(42)
    if same:
        c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
        SetupCanvas(c, 0)
        legend = rt.TLegend(x0_l-0.2,y0_l-0.4,x1_l-0.2, y1_l-0.4)
        legend.SetTextSize(4)

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
            c.SaveAs(destination+ "/"+addCut+"/"+h[ihist].GetName()+".pdf")

        if same:
            c.cd()

            legend.AddEntry(h[ihist],vartitle[interestVar[ihist]][0] if len(legtext)==0 else legtext[ihist],'l')
            h[ihist].Draw("lsamex0")

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
        c.SaveAs(destination+ "/"+addCut+"/"+h[0].GetName()+".pdf")







def MakeROC(hROC,hsig,hbkg,icolor,var):
    hsig.Scale(dscale['ttbar'])
    hbkg.Add(hsig,-1)
    for bin in range(hbkg.GetSize()-2):
        if hbkg.GetBinContent(bin+1) < 0:
            hbkg.SetBinContent(bin+1,0) 
    nsig = hsig.Integral()
    nbkg = hbkg.Integral()
    print nbkg
    hROC.SetLineColor(rt.TColor.GetColor(histFillColor[icolor]))
    hROC.SetLineWidth(3)
    sumroc = 0
    for point in range(hsig.GetSize()-2):
        sig = hsig.Integral(point+1,hsig.GetSize()-2)
        bkg = hbkg.Integral(point+1,hsig.GetSize()-2)
        #print 'sig: ', sig, ' bkg: ', bkg
        xAxis = hROC.GetXaxis()
        x =  xAxis.FindBin(bkg/nbkg)
        w = hROC.GetBinWidth(point+1)
        if hROC.GetBinContent(x) < sig/nsig:
            hROC.SetBinContent(x,sig/nsig)
            sumroc+= w*sig/nsig
    print 'AUC for ', var ,': ' ,sumroc


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
        if 'ttbar' in f:
            tree[i].Draw(var + '>>'+ 'h'+var+str(j)+ str(vartitle[var][1]),"puweight*btagweight*qgweight*trigweight*("+addCut+")")
        else:
            tree[i].Draw(var + '>>'+ 'h'+var+str(j)+ str(vartitle[var][1]),"("+addCut+")")
        hprocess.append(rt.gDirectory.Get('h'+var+str(j)))
    hvar.append(hprocess)


hROC = []
for i, var in enumerate(interestVar):
    # plots['Var'][i][0] = hvar[1][i].Clone('QCD'+var)
    # plots['Var'][i][0].SetLineColor(2)
    # plots['Var'][i][0].SetLineWidth(2)
    # plots['Var'][i][1] = hvar[0][i].Clone('ttbar'+var)
    # plots['Var'][i][1].SetLineColor(4)
    #
    # plots['Var'][i][1].SetLineWidth(2)

    MakeROC(plots['ROC'][i],hvar[0][i],hvar[1][i],i,var)
    #MakeSignificance(plots['Signf'][i],hvar[1][i],hvar[0][i])



# singlePlot(plots['Signf'],0)
singlePlot(plots['ROC'],1)
# for ivar, var in enumerate(plots['Var']):
#    singlePlot(var,1,['QCD '+vartitle[interestVar[ivar]][0],'t#bar{t} '+vartitle[interestVar[ivar]][0]])

   #raw_input("Press Enter to end")
