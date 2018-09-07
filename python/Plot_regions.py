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

reg1cut = '(n_jets>=8 && ttCls == 0)'
reg2cut = '(n_jets>=8 && ttCls >=51)'
reg3cut = '(n_jets>=8 && ttCls <= 46 && ttCls > 0)'
#reg1cut = '(n_jets>=8 &&qgLR>0 && qgLR < 0.5 && BDT_Comb>=-1)'
#reg2cut = '(n_jets>=8 &&qgLR >0.5 && qgLR<0.8 && BDT_Comb>=-1)'
#reg3cut = '(n_jets>=8 && BDT_Comb>=-1 && qgLR>0.8)'
#reg1cut = "(qgLR<0.95&&jet_QGL[2]<0.82 && jet_QGL[4]<0.56 && n_jets==7)"
#reg2cut = "(qgLR>0.95 && jet_QGL[2]>0.31 && jet_QGL[4]>0.4 && jet_QGL[3]>0.1 && jet_QGL[5]>0.2 && n_jets==7)"
weight = 'weight*puweight*btagweight*qgweight*topweight'

#reg1cut = '(jet_CSV[0]>=0.8484 && jet_CSV[1]>=0.8484)'
#reg2cut = '(jet_CSV[0]<0.2 || jet_CSV[1]<0.2)'

#reg1cut = '(simple_chi2<10)'
#reg2cut = '(simple_chi2>10)'

#reg1cut = "(n_jets==7)"
#reg2cut = "(n_jets>7)"

#reg1cut = "(qgLR< 0.3 && n_jets==7)"
#reg2cut = "(qgLR> 0.8 && n_jets==7)"


#reg1cut = '(meanDeltaRbtag > 2.0)'
#reg2cut = '(meanDeltaRbtag < 1)'
#reg1cut = 'BDT_Comb> 0.657801 && BDT_CWoLa>0.170504 && prob_chi2>0.125174 && BDT_ttbb3b == 4 '
#reg2cut ='BDT_Comb> 0.657801 && BDT_CWoLa>0.170504 && prob_chi2>0.125174 && BDT_ttbb3b < 4'

#
#processlist = ['ttbar','QCD']
processlist = ['ttbar']

#file1 = ROOT.TFile('../Datasets/Correct_NoBtag_ttbarRed.root')
#interestVar = ['top1_m','top2_m','w1_m','w2_m','deltaRl1l2','deltaRq1q2','deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhiw1w2','deltaPhit1t2','q1b1_mass','p1b2_mass','deltaRb1w2','deltaRb2w1','mindeltaRb1q','simple_chi2','mindeltaRb2p', 'deltaEtal1l2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]']

interestVar =[
    'lp2_pt',
    #'lq1_pt',
    'lq2_pt',
    'b1_pt',
    'b2_pt',
    'lp1_pt',
    'w2_m',
    'w1_m',
    #'top1_m',
    'top2_m',
    'meanDeltaRbtag',
    #'deltaRp1p2',
    #'deltaRq1q2',
    #'deltaRb2w1',
    #'q1b2_mass',
    'p1b1_mass',
    'deltaRb1b2',
    'jet_CSV[0]',
    'jet_CSV[1]',
    #'mindeltaRb2q',
    #'mindeltaRb1p',
    'deltaRb2top1',
    'BDT_Comb',
    #'tt_m'
    'w1_pt',
    'w2_pt',
    #'jets_dRavg',
    # 'jet_CSV[2]',
    # 'jet_CSV[3]',
    # 'jet_CSV[4]',
    # 'jet_CSV[5]'
    ]
interestVar =['btagLR4b']
#interestVar = ['lq2_pt','lp1_pt','lp2_pt','b1_pt','b2_pt', 'w1_m', 'w2_m', 'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1', 'p1b2_mass', 'q1b1_mass', 'deltaRb1b2','deltaRq1q2','jet_CSV[0]','jet_CSV[1]','minjetpt','aplanarity', 'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','tt_pt', 'lq1_m', 'mindeltaRb1q',  'ht', 'mindeltaRb2p', 'all_mass','meanCSV','jets_dRmin','BDT_Comb']

#'tt_pt', 'tt_phi', 'b1_phi', 'b2_m', 'b2_phi', 'lq1_m', 'lq1_pt', 'lq1_phi', 'lq2_phi',  'lp1_pt', 'lp1_phi', 'lp2_phi', 'w1_pt', 'w1_phi', 'w2_pt', 'w2_phi', 'top1_phi', 'top2_phi', 'deltaRb1w2', 'meanDeltaRbtag', 'deltaRl1l2', 'btagLR3b', 'mindeltaRb1q', 'p1b2_mass', 'q1b1_mass',  'ht', 'deltaRb1b2', 'mindeltaRb2p', 'deltaRq1q2', 'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','deltaPhit1t2','tt_eta', 'b1_eta','b2_eta', 'b1_pt','lq1_eta','lq2_eta','lp1_eta','lp2_eta','w1_eta','w2_eta','top1_eta','top2_eta', 'deltaPhiq1q2', 'deltaRb1top2', 'deltaPhil1l2', 'deltaEtal1l2', 'deltaPhib1b2','deltaEtab1b2','jets_dRmax', 'deltaEtat1t2','meanCSV'

#'deltaEtab1b2', 'deltaEtat1t2', 'deltaEtaw1w2','deltaPhil1l2','deltaPhiq1q2','deltaPhib1b2','deltaPhit1t2', 'deltaEtal1l2', 'deltaEtaq1q2','deltaEtaw1w2'

# 'lq1_pt', 'lq2_pt', 'lp1_pt', 'lp2_pt','b1_pt','b2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m',  'top2_m', 'deltaRb1w2',  'meanDeltaRbtag', 'deltaRl1l2', 'deltaRb2w1',   'deltaRb2p1', 'deltaRb2top1', 'p1b2_mass',   'q1b1_mass',   'deltaRb1b2', 'meanCSVbtag','deltaRq1q2','btagLR4b','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]',

#interestVar=['qgLR','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]']
#, 'w1_m',  'w2_m','meanDeltaRbtag','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]', 'btagLR4b',  'deltaRl1l2'
#'n_bjets','lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt', 'w1_m',  'w2_m',   'top1_m',  'top2_m',   'mindeltaRb1q' ,'mindeltaRb2p', 'deltaRb1w2','jet_CSV[0]','jet_CSV[1]', 'meanCSVbtag',  'deltaRb1b2','meanDeltaRbtag','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]','jet_QGL[0]','jet_QGL[1]','jet_QGL[2]','jet_QGL[3]','jet_QGL[4]','jet_QGL[5]','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]'

#'tt_m', 'tt_pt', 'lq1_m', 'lq1_pt',  'lq2_m', 'lq2_pt',  'lp1_m', 'lp1_pt',  'lp2_m', 'lp2_pt',  'w1_m', 'w1_pt',  'w2_m', 'w2_pt',  'top1_m', 'top1_pt',  'top2_m', 'top2_pt',  'deltaRb1w1', 'deltaRb1w2',  'meanDeltaRbtag', 'jet5pt',  'deltaRb1q1', 'deltaRl1l2',  'deltaRb2w2', 'deltaRb2w1', 'btagLR3b',  'mindeltaRb1q',  'deltaRb2p1', 'deltaRb2top1' , 'p1b2_mass',   'q1b1_mass', 'ht','closest_mass', 'jets_dRavg',  'deltaRb1b2', 'mindeltaRb2p', 'meanCSVbtag',  'deltaRq1q2', 'all_mass','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]'
addCut = 'BDT_Comb >= -1'




plots = {}
for var in interestVar:
    plots[var] = [[rt.TH1F(),rt.TH1F(),rt.TH1F()],[rt.TH1F(),rt.TH1F(),rt.TH1F()]]

def singlePlot(h,same,legtext=[]):
    rt.gStyle.SetLegendFont(42)
    if same:
        c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
        SetupCanvas(c, 0)
        legend = rt.TLegend(x0_l,y0_l,x1_l, y1_l )

    for ihist in range(len(h)):
    #for ihist in range(1):
        #h[ihist].Scale(1.0/h[ihist].Integral() if h[ihist].Integral() > 0 else 1.0)
        h[ihist].GetYaxis().SetRangeUser(0,1.25)
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
        c.SaveAs(destination+ "/"+addCut+"/"+h[0].GetName()+".pdf")



files = []
tree = []
hvar = []

for i, f in enumerate(processlist):
    files.append(rt.TFile(processfiles[f],"READ"))
    tree.append(files[i].Get('tree'))
    hprocess = []
    for j, var in enumerate(interestVar):
        #puweight*btagweight*qgWeight*trigWeight(ht,jet5pt,n_bjets)
        tree[i].Draw(var + '>>'+ 'h1'+var+str(j)+ str(vartitle[var][1]),weight+"*("+addCut+")*"+reg1cut)
        print var + '>>'+ 'h1'+var+str(j)+ str(vartitle[var][1]),weight+"*("+addCut+")*"+reg1cut
        tree[i].Draw(var + '>>'+ 'h2'+var+str(j)+ str(vartitle[var][1]),weight+"*("+addCut+")*"+reg2cut)
        tree[i].Draw(var + '>>'+ 'h3'+var+str(j)+ str(vartitle[var][1]),weight+"*("+addCut+")*"+reg3cut)
        plots[var][i][0] = rt.gDirectory.Get('h1'+var+str(j)).Clone(f+'Rg1'+var)
        plots[var][i][0].SetLineColor(3)
        plots[var][i][0].SetLineWidth(2)
        plots[var][i][1] = rt.gDirectory.Get('h2'+var+str(j)).Clone(f+'Rg2'+var)
        plots[var][i][1].SetLineColor(2)
        plots[var][i][1].SetLineWidth(2)
        plots[var][i][2] = rt.gDirectory.Get('h3'+var+str(j)).Clone(f+'Rg3'+var)
        plots[var][i][2].SetLineColor(4)
        plots[var][i][2].SetLineWidth(2)

        plots[var][i][0].Scale(1.0/(plots[var][i][0].Integral() if plots[var][i][0].Integral() > 0 else 1.0))
        #plots[var][i][0].Draw()
        #raw_input()
        plots[var][i][1].Scale(1.0/(plots[var][i][1].Integral() if plots[var][i][1].Integral() > 0 else 1.0))
        plots[var][i][2].Scale(1.0/(plots[var][i][2].Integral() if plots[var][i][2].Integral() > 0 else 1.0))
        #plots[var][i][0].Sumw2()
        #plots[var][i][0].Divide(plots[var][i][1])


for iproc, proc in enumerate(processlist):
    print 'processing: ',proc
    for ivar, var in enumerate(plots):
        print 'variable: ',var
        #singlePlot(plots[var][iproc],1,['Rg.1 '+vartitle[var][0]])
        #singlePlot(plots[var][iproc],1,[proc + ' Rg.1 '+vartitle[var][0], proc + ' Rg.2 '+vartitle[var][0]])
        #singlePlot(plots[var][iproc],1,['0 < QGLR < 0.5','0.5 < QGLR < 0.8','0.8 < QGLR < 1.0'])
        singlePlot(plots[var][iproc],1,['ttlf','ttbb','ttcc'])

    #raw_input("Press Enter to end")
