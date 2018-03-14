
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

#reg1cut = '(qgLR>0.9)'
#reg2cut = '(qgLR < 0.3)'
# reg1cut = '(meanDeltaRbtag > 2.0)'
# reg2cut = '(meanDeltaRbtag < 1)'
reg1cut = 'BDT_Comb> 0.657801 && BDT_CWoLa>0.170504 && prob_chi2>0.125174 && BDT_ttbb3b == 4 '
reg2cut ='BDT_Comb> 0.657801 && BDT_CWoLa>0.170504 && prob_chi2>0.125174 && BDT_ttbb3b < 4'

#
processlist = ['ttbar','QCD']
# interestVar = ['jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','top1_m','top2_m','w1_m','w2_m','deltaRb1b2','deltaRb1w1','deltaRb2w2','jet_CSV[0]','jet_CSV[1]','BDT_Comb','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','ht','simple_chi2','meanDeltaRbtag','mindeltaRb1q','mindeltaRb2p','n_jets','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','all_mass','closest_mass','jets_dRavg','jets_dRmax','BDT_QCD','qgLR']
interestVar=['tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'deltaRb1w1', 'deltaRb1w2',  'meanDeltaRbtag', 'prob_chi2', 'BDT_Comb', 'jet5pt',  'n_bjets',  'deltaRaddb1', 'deltaRaddb2',  'deltaRb1q1', 'deltaRl1l2', 'btagLR4b', 'deltaRb2w2', 'deltaRb2w1', 'simple_chi2', 'btagLR3b',  'mindeltaRb1q',  'deltaRb2p1', 'deltaRb2top1', 'aplanarity', 'p1b2_mass', 'centrality',  'q1b1_mass', 'deltaRaddtop2', 'deltaRaddtop1', 'ht', 'deltaPhiw1w2',  'closest_mass', 'girth', 'jets_dRavg',  'meanCSV', 'deltaRb1b2', 'mindeltaRb2p', 'meanCSVbtag', 'jets_dRmax', 'deltaEtat1t2', 'deltaRq1q2', 'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']
addCut = 'jet_QGL[0]>=0 && jet_QGL[1]>=0 && jet_QGL[2]>=0 && jet_QGL[3]>=0 && jet_QGL[4]>=0 && jet_QGL[5]>=0 && jet_CSV[0]>=0 && jet_CSV[1]>=0 && jet_CSV[2]>=0 && jet_CSV[3]>=0 && jet_CSV[4]>=0 && jet_CSV[5]>=0'




plots = {}
for var in interestVar:
    plots[var] = [rt.TH1F(),rt.TH1F()],[rt.TH1F(),rt.TH1F()]




def singlePlot(h,same,legtext=[]):
    rt.gStyle.SetLegendFont(42)
    if same:
        c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
        SetupCanvas(c, 0)
        legend = rt.TLegend(x0_l-0.3,y0_l,x1_l-0.3, y1_l )

    for ihist in range(len(h)):
        h[ihist].Scale(1.0/h[ihist].Integral() if h[ihist].Integral() > 0 else 1.0)
        h[ihist].GetYaxis().SetRangeUser(0,0.3)
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
            h[ihist].Draw("histsamex0")
            
    if same:
        legend.SetTextSize(0.03)
        legend.Draw('same')

        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        
        c.Update()
        c.RedrawAxis()

        if not os.path.exists(destination+ "/"+addCut):
            os.makedirs(destination+ "/"+addCut)
        else:
            print "WARNING: directory already exists. Will overwrite existing files..."
        c.SaveAs(destination+ "/"+addCut+"/"+h[0].GetName()+".png")

    
    
files = []
tree = []
hvar = []

for i, f in enumerate(processlist):
    files.append(rt.TFile(processfiles[f],"READ"))    
    tree.append(files[i].Get('tree'))
    hprocess = []
    for j, var in enumerate(interestVar):
        tree[i].Draw(var + '>>'+ 'h1'+var+str(j)+ str(vartitle[var][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+")*"+reg1cut)
        
        tree[i].Draw(var + '>>'+ 'h2'+var+str(j)+ str(vartitle[var][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+")*"+reg2cut)
        plots[var][i][0] = rt.gDirectory.Get('h1'+var+str(j)).Clone(f+'Rg.1'+var)
        plots[var][i][0].SetLineColor(3)
        plots[var][i][0].SetLineWidth(2)    
        plots[var][i][1] = rt.gDirectory.Get('h2'+var+str(j)).Clone(f+'Rg.2'+var)
        plots[var][i][1].SetLineColor(2)
        plots[var][i][1].SetLineWidth(2)

    
for iproc, proc in enumerate(processlist):
    print 'processing: ',proc
    for ivar, var in enumerate(plots):
        print 'variable: ',var
        singlePlot(plots[var][iproc],1,['Rg.1 '+vartitle[var][0],'Rg.2 '+vartitle[var][0]])
    
    #raw_input("Press Enter to end")                            



