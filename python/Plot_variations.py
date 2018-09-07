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


processlist = ['ttbb']
var = 'btagLR4b'

sys_list=[
    #'_bkg_extrap',
    '_CMS_LHE_renorm_Weight',
    '_CMS_LHE_fact_Weight',
    '_CMS_LHEPDF_Weight',
    '_lumi',
    '_pdf_gg',
    '_QCD_scale_tt',
    #'_bgnorm_ttbarPlusCCbar',
    # '_ttbb_FSR',
    # '_ttbb_ISR',
    # '_ttbb_tune',
    # '_ttbb_hdamp',
    # '_ttcc_FSR',
    # '_ttcc_ISR',
    # '_ttcc_tune',
    # '_ttcc_hdamp',
    #'_ttlf_FSR',
    #'_ttlf_ISR',
    #'_ttlf_tune',
    #'_ttlf_hdamp',
    # '_tt2b_FSR',
    # '_tt2b_ISR',
    # '_tt2b_tune',
    # '_tt2b_hdamp',
    # '_ttb_FSR',
    # '_ttb_ISR',
    # '_ttb_tune',
    # '_ttb_hdamp',
    '_CMS_btag_hf',
    '_CMS_btag_cferr1',
    '_CMS_btag_cferr2',
    '_CMS_btag_lf',
    '_CMS_btag_lfstats2',
    '_CMS_btag_lfstats1',
    '_CMS_btag_hfstats2',
    '_CMS_btag_hfstats1',
    '_CMS_btag_jes',
    '_CMS_pu_Weight',
    '_CMS_top_Weight',
    '_CMS_qg_Weight',
    '_CMS_trig_Weight',
    '_CMS_RelativeStatEC_j',
    '_CMS_RelativeStatHF_j',
    '_CMS_PileUpDataMC_j',
    '_CMS_PileUpPtRef_j',
    '_CMS_PileUpPtBB_j',
    '_CMS_PileUpPtEC1_j',
    '_CMS_PileUpPtHF_j',
    '_CMS_RelativeStatFSR_j',
    '_CMS_RelativeFSR_j',
    '_CMS_AbsoluteScale_j',
    '_CMS_AbsoluteMPFBias_j',
    '_CMS_Fragmentation_j',
    '_CMS_SinglePionECAL_j',
    '_CMS_SinglePionHCAL_j',
    '_CMS_FlavorQCD_j',
    '_CMS_TimePtEta_j',
    '_CMS_RelativeJEREC1_j',
    '_CMS_RelativeJEREC2_j',
    '_CMS_RelativeJERHF_j',
    '_CMS_RelativePtBB_j',
    '_CMS_RelativePtEC1_j',
    '_CMS_RelativePtEC2_j',
    '_CMS_RelativePtHF_j',
    '_CMS_JER_j',
    '_CMS_AbsoluteStat_j',
    # '_CMS_Total_j'
    #'_CMS_AbsoluteFlavMap_j'
]
direction=['Up','Down']
def singlePlot(h,name,legtext=[]):
    rt.gStyle.SetLegendFont(42)

    c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
    pad1 = rt.TPad("pad1", "pad1", 0.0, 0.15,1,1)
    pad1.Draw()
    pad1.cd()

    SetupCanvas(pad1, 1)
    hframe = h[0].Clone('hframe')
    hframe.Draw("ehist")
    c.Update()
    c.RedrawAxis()
    legend = rt.TLegend(x0_l-0.3,y0_l+0.1,x1_l-0.3, y1_l )
    legend.AddEntry(h[0],'nominal','l')
    for ihist in range(len(h)):
        if ihist==0: continue
        #h[ihist].GetYaxis().SetRangeUser(0.7,1.3)
        yAxis = h[ihist].GetYaxis()
        yAxis.SetNdivisions(6,5,0)
        yAxis.SetTitleOffset(1)
        yAxis.SetTitleSize(0.05)




        legend.AddEntry(h[ihist],vartitle[interestVar[ihist]][0] if len(legtext)==0 else legtext[ihist],'l')
        h[ihist].Draw("ehistsameaaxis")


        legend.SetTextSize(0.03)
        legend.Draw('same')

    CMS_lumi.CMS_lumi(c, iPeriod, iPos)


    pad1.cd()
    pad1.Update()
    pad1.RedrawAxis()
    c.cd()
    p1r = rt.TPad("p4","",0,0,1,0.26)

    p1r.SetRightMargin(0.04)
    p1r.SetLeftMargin(0.12)
    p1r.SetTopMargin(0.0)
    p1r.SetBottomMargin(0.42)
    p1r.SetTicks()
    p1r.Draw()
    p1r.cd()
    xmin = float(h[0].GetXaxis().GetXmin())
    xmax = float(h[0].GetXaxis().GetXmax())
    one = rt.TF1("one","1",xmin,xmax)
    one.SetLineColor(1)
    #one.SetLineStyle(2)
    one.SetLineWidth(3)

    hratio = h[0].Clone("hratio")
    hratio.Reset()
    hratio.GetYaxis().SetRangeUser(0.8,1.2)

    hratio.SetTitle("")

    hratio.GetXaxis().SetTitle(vartitle[var][0])
    hratio.GetXaxis().SetTitleSize(0.156)
    hratio.GetXaxis().SetLabelSize(0.171)
    hratio.GetXaxis().SetLabelOffset(0.02)

    hratio.GetYaxis().SetTitleSize(0.196)
    hratio.GetYaxis().SetLabelSize(0.171)
    hratio.GetYaxis().SetTitleOffset(0.30)
    hratio.GetYaxis().SetTitle("      Sys/Nom")
    hratio.GetYaxis().SetDecimals(1)
    hratio.GetYaxis().SetNdivisions(4,2,0,rt.kTRUE) #was 402
    hratio.GetXaxis().SetNdivisions(6,5,0)
    hratio.Draw("pe")
    hup=h[1].Clone("Up")
    hup.Divide(h[0])
    hdown=h[2].Clone("Down")
    hdown.Divide(h[0])
    hup.Draw("ehistsame")
    hdown.Draw("ehistsame")
    one.Draw("same")
    hratio.Draw("PEsame")
    hratio.Draw("PE0X0same")
    hratio.Draw("sameaxis") #redraws the axes
    p1r.Update()
    if not os.path.exists(destination+ "/"+name):
        os.makedirs(destination+ "/"+name)
    else:
        print "WARNING: directory already exists. Will overwrite existing files..."
    c.SaveAs(destination+ "/"+name+"/"+h[1].GetName()+".pdf")


f = rt.TFile('hCard_bLR_2b_theory30.root',"READ")

plot = {}
for i, proc in enumerate(processlist):
    plot[proc] = {}

    for j, sys in enumerate(sys_list):
        print sys
        plot[proc][sys]=[rt.TH1F(),rt.TH1F(),rt.TH1F()]
        plot[proc][sys][0]=f.Get('SR/'+proc)
        plot[proc][sys][0].SetLineColor(1)
        plot[proc][sys][0].SetLineWidth(3)
        for k, direc in enumerate(direction):

            plot[proc][sys][k+1]=f.Get('SR/'+proc+sys+direc)
            #plot[proc][sys][k+1].Divide(plot[proc][sys][0])
            #print proc+sys+direc
            #print type(plot[proc][sys][k+1]), type(plot[proc][sys][0])
            plot[proc][sys][k+1].SetLineColor(rt.TColor.GetColor(histFillColor[k]))
            plot[proc][sys][k+1].SetLineWidth(3)



for ivar, proc in enumerate(plot):
    print 'variable: ',proc
    for sys in sys_list:
        singlePlot(plot[proc][sys],'Sys_variations',[proc+' Nominal',proc + ' '+ sys.replace('_',' ')+' Up',proc+ ' ' +sys.replace('_',' ')+ ' Down'])

        #raw_input("Press Enter to end")
