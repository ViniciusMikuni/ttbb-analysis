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
rt.gROOT.LoadMacro("triggerWeightRound.h+")
tdrstyle.setTDRStyle()


plot_tree = 1
saveplots = 1
processlist = ['data','ttbar','QCD']

#addCut = 'w1_m < 100 && w1_m > 60 && w2_m < 100 && w2_m > 60 && qgLR > 0.5'
addCut = 'w1_m>0'
#cut = ['prob_chi2 >= 0.0','prob_chi2 > 0.001','prob_chi2 > 0.01','prob_chi2 > 0.05','prob_chi2 > 0.1','prob_chi2 > 0.2']
cut = ['isCorrect == 1','chi2Correctall == 1','isCorrect == 1','chi2Correct == 1']
cuttext = ['All Combinations BDT','All Combinations #chi^{2}','b-jet Assignment BDT','b-jet Assignment #chi^{2}']
#cut = ['exp(-simple_chi2/4) > 0','exp(-simple_chi2/4) > 0.001','exp(-simple_chi2/4) > 0.01','exp(-simple_chi2/4) > 0.05','exp(-simple_chi2/4) > 0.1','exp(-simple_chi2/4) > 0.2']
#cuttext = ['Prob(#chi^{2}) >= 0.0','Prob(#chi^{2}) > 0.0001','Prob(#chi^{2}) > 0.01','Prob(#chi^{2}) > 0.05','Prob(#chi^{2}) > 0.1','Prob(#chi^{2}) > 0.2']
#cuttext = ['No cut','P_{gof} > 0.0001','P_{gof} > 0.01','P_{gof} > 0.05','P_{gof} > 0.1','P_{gof} > 0.2']
cats = ["1","n_bjets == 3 && n_jets == 7","n_bjets == 3 && n_jets == 8","n_bjets >= 4 && n_jets == 8","n_bjets == 3 && n_jets == 9","n_bjets >= 4 && n_jets == 9"]
shortcats = ["All","3b7j","3b8j","4b8j","3b9j","4b9j"]

# cats = ["1","n_jets == 7 ","n_jets >= 8 "]
# shortcats = ["All","7j","8j or more"]

#treeplots = ['chi2','prob_chi2','wkin','catplot']
npoints = 100
nostack = {'eff':[],'Signf':[rt.TH1F('Signf','Signf;BDT output;#frac{S}{#sqrt{S+B}}',npoints,-1,1)],'QCD':[rt.TH1F('QCD','QCD;BDT output;',npoints,-1,1),rt.TH1F('ttbar','ttbar;BDT output;',npoints,-1,1)],'Comb':[rt.TH1F('Wrongc',';BDT output;',npoints,-1,1),rt.TH1F('Corrc',';BDT output;',npoints,-1,1)],'ROC':[rt.TH1F('ROCBDT','ROC;1-Speficity;Sensitivity',npoints,0,1),rt.TH1F('ROCQGLR','ROCQGLR;1-Speficity;Sensitivity',npoints,0,1)]}
#legtext = ['Wrong combinations','Correct combinations']
legtext = ['BDT for QCD','QGLR']
for i in range(len(cut)):
    nostack['eff'].append(rt.TH1F('eff'+str(i),'eff;;Efficiency',len(cats),0,len(cats)))



def singlePlot(h,saveplots):
    rt.gStyle.SetLegendFont(42)
    c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
    SetupCanvas(c, 0)
    legend = rt.TLegend(x0_l,y0_l,x1_l, y1_l );
    # h[0].SetMarkerColor(8) 
    # h[0].SetMarkerStyle(1)
    # h[0].SetMarkerSize(1)
    h[0].SetLineColor(8) 
    h[0].SetLineWidth(1)

    h[0].SetMaximum(max(h[len(h)-1].GetMaximum()*2.0,1.5))
    h[0].SetMinimum(0.0)
    if len(h)>2:
        for i in range(len(shortcats)):
            h[0].GetXaxis().SetBinLabel(i+1,shortcats[i])
    # xAxis = h.GetXaxis()
    # xAxis.SetNdivisions(6,5,0)
    yAxis = h[0].GetYaxis()
    yAxis.SetNdivisions(6,5,0)
    yAxis.SetTitleOffset(1)
    yAxis.SetTitleSize(0.05)
    if len(h)>2:
        legend.AddEntry(h[0],cuttext[0],'p')

    if len(h)==2:
        legend.AddEntry(h[0],legtext[0],'l')

    h[0].Draw('histsamex0')
    CMS_lumi.CMS_lumi(c, iPeriod, iPos)
    print 'lumi'
    for i in range(len(h)-1):
        h[i+1].SetMarkerSize(1)
        #h[i+1].SetMarkerStyle(24+i)
        #h[i+1].SetMarkerStyle(1)
        #h[i+1].SetMarkerColor(i+2)
        # legend.AddEntry(h[i+1],cuttext[i+1],'p')
        #h[i+1].Draw("histsamex0")
           
        h[i+1].SetLineWidth(1)
        h[i+1].SetLineColor(i+2)
        if len(h) == 2:legend.AddEntry(h[i+1],legtext[i+1],'l')  
        h[i+1].Draw("histsamex0")

    c.cd()
    if len(h)>1:legend.Draw('same')
    else:
        h[0].SetMarkerSize(1)
        h[0].SetMarkerStyle(1)
        h[0].SetMarkerColor(1)

    c.Update()
    c.RedrawAxis()
    if saveplots:
        if not os.path.exists(destination+ "/"+addCut):
            os.makedirs(destination+ "/"+addCut)
        else:
            print "WARNING: directory already exists. Will overwrite existing files..."
        c.SaveAs(destination+ "/"+addCut+"/"+h[0].GetName()+".png")


    
files = rt.TFile(processfiles['ttbar'],"READ")
#fdata = rt.TFile(processfiles['Data'],"READ")
fQCD = rt.TFile(processfiles['QCD'],"READ")
fdata = rt.TFile(processfiles['data'],"READ")

tqcd = fQCD.Get('tree')
tdata = fdata.Get('tree')
tqcd.Draw("BDT_Comb>>QCDBDTComb"+ str(vartitle['BDT_Comb'][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+")")
nostack['QCD'][0] = rt.gDirectory.Get("QCDBDTComb")
tttbar = files.Get('tree')
tttbar.Draw("BDT_Comb>>ttbarBDTComb"+ str(vartitle['BDT_Comb'][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+")")
nostack['QCD'][1] = rt.gDirectory.Get("ttbarBDTComb")

tttbar = files.Get('tree')
tttbar.Draw("BDT_Comb>>ttbarBDTW"+ str(vartitle['BDT_Comb'][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&& hasCorrect == 1 && isCorrect == 0)")
nostack['Comb'][0] = rt.gDirectory.Get("ttbarBDTW")
tttbar.Draw("BDT_Comb>>ttbarBDTC"+ str(vartitle['BDT_Comb'][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&& isCorrect == 1)")
nostack['Comb'][1] = rt.gDirectory.Get("ttbarBDTC")
hist = 'BDT_Comb'
        
for  ncat, cat in enumerate(cats):
    nhascorr = nhasbcorr = niscorrBDT = niscorrchi2 = 0
    
    tvar = files.Get('tree')
    tvar.Draw(hist+">>hisBDT"+str(ncat)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cat+"&& isCorrect == 1)")
    tvar.Draw(hist+">>hisChi2"+str(ncat)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cat+"&& chi2Correctall == 1)")
    tvar.Draw(hist+">>hisBDTb"+str(ncat)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cat+"&& isCorrect == 1 && hasbCorrect == 1)")
    tvar.Draw(hist+">>hisChi2b"+str(ncat)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cat+"&& chi2Correct == 1 && hasbCorrect == 1)")
    tvar.Draw(hist+">>hhas"+str(ncat)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cat+"&& hasCorrect == 1)")
    tvar.Draw(hist+">>hhasb"+str(ncat)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cat+"&& hasbCorrect == 1)")
    nhascorr =rt.gDirectory.Get("hhas"+str(ncat)).Integral()
    nhasbcorr =rt.gDirectory.Get("hhasb"+str(ncat)).Integral()
    niscorrBDT =rt.gDirectory.Get("hisBDT"+str(ncat)).Integral()
    niscorrchi2 =rt.gDirectory.Get("hisChi2"+str(ncat)).Integral()
    niscorrBDTb =rt.gDirectory.Get("hisBDTb"+str(ncat)).Integral()
    niscorrchi2b =rt.gDirectory.Get("hisChi2b"+str(ncat)).Integral()
         

    nostack['eff'][0].SetBinContent(ncat+1,float(niscorrBDT)/nhascorr if nhascorr > 0 else 0.0 )
    nostack['eff'][0].SetBinError(ncat+1,sqrt(float(niscorrBDT))/nhascorr if nhascorr > 0 else 0.0 )
    nostack['eff'][1].SetBinContent(ncat+1,float(niscorrchi2)/nhascorr if nhascorr > 0 else 0.0 )
    nostack['eff'][1].SetBinError(ncat+1,sqrt(float(niscorrchi2))/nhascorr if nhascorr > 0 else 0.0 )
    nostack['eff'][2].SetBinContent(ncat+1,float(niscorrBDTb)/nhasbcorr if nhasbcorr > 0 else 0.0 )
    nostack['eff'][2].SetBinError(ncat+1,sqrt(float(niscorrBDTb))/nhasbcorr if nhasbcorr > 0 else 0.0 )
    nostack['eff'][3].SetBinContent(ncat+1,float(niscorrchi2b)/nhasbcorr if nhasbcorr > 0 else 0.0 )
    nostack['eff'][3].SetBinError(ncat+1,sqrt(float(niscorrchi2b))/nhasbcorr if nhasbcorr > 0 else 0.0 )

addCut = 'qgLR>=0'
tqcd.Draw(hist+">>hb"+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_QCD>=-1)")
ntotalqcd= rt.gDirectory.Get("hb").Integral()
tvar.Draw(hist+">>hs"+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_QCD>=-1)")
ntotalsig= rt.gDirectory.Get("hs").Integral()
for i in range(npoints*10):
    val = -1 + i*2.0/(npoints*10)
    # tvar.Draw(hist+">>hhas"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_Comb>"+str(val)+"&& hasCorrect == 1)")
    # nhascorr =rt.gDirectory.Get("hhas"+str(ncat)).Integral()
    # tvar.Draw(hist+">>his"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_Comb>"+str(val)+"&& isCorrect == 1)")
    # niscorr =rt.gDirectory.Get("his"+str(len(cats)+i)).Integral()
    # nostack['Signf'][0].SetBinContent(i+1,float(niscorr)/sqrt(nhascorr) if nhascorr > 0 else 1.0 )
    # nostack['Signf'][0].SetBinError(i+1,sqrt(float(niscorr))/sqrt(nhascorr) if nhascorr > 0 else 1.0 )

    #tqcd.Draw(hist+">>hhas"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_Comb>"+str(val)+")")
    #nqcd =rt.gDirectory.Get("hhas"+str(len(cats)+i)).Integral()
    # tdata.Draw(hist+">>hdata"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_Comb>"+str(val)+")")
    # ndata =rt.gDirectory.Get("hdata"+str(len(cats)+i)).Integral()
    # tvar.Draw(hist+">>his"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_Comb>"+str(val)+")")
    # nttbar =rt.gDirectory.Get("his"+str(len(cats)+i)).Integral()
    # nostack['Signf'][0].SetBinContent(i+1,float(dscale['ttbar']*nttbar)/(ndata) if ndata > 0 else 1.0 )
    # nostack['Signf'][0].SetBinError(i+1,sqrt(float(dscale['ttbar']*nttbar))/(ndata) if ndata > 0 else 1.0 )

    tqcd.Draw(hist+">>hhas"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_QCD>"+str(val)+")")
    nfalseposBDT =rt.gDirectory.Get("hhas"+str(len(cats)+i)).Integral()
    tvar.Draw(hist+">>hbhas"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"BDT_QCD>"+str(val)+")")
    ntrueposBDT =rt.gDirectory.Get("hbhas"+str(len(cats)+i)).Integral()

    tqcd.Draw(hist+">>hhasqgl"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"qgLR>"+str(abs(val))+")")
    nfalseposQGL =rt.gDirectory.Get("hhasqgl"+str(len(cats)+i)).Integral()
    tvar.Draw(hist+">>hshasqgl"+str(len(cats)+i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+"qgLR>"+str(abs(val))+")")
    ntrueposQGL =rt.gDirectory.Get("hshasqgl"+str(len(cats)+i)).Integral()

    xAxis = nostack['ROC'][0].GetXaxis()
    binBDT =  xAxis.FindBin(nfalseposBDT/ntotalqcd)
    binQGL =  xAxis.FindBin(nfalseposQGL/ntotalqcd)
    if val == 0.5:
        print nfalseposQGL/ntotalqcd
    
    nostack['ROC'][0].SetBinContent(binBDT,ntrueposBDT/ntotalsig)
    nostack['ROC'][1].SetBinContent(binQGL,ntrueposQGL/ntotalsig)


    

#imax = nostack['Signf'][0].GetMaximumBin()
#xAxis = nostack['Signf'][0].GetXaxis()
#print xAxis.GetBinCenter(imax)

    
for key in nostack:
    singlePlot(nostack[key],saveplots)
    #raw_input("Press Enter to end")                            



