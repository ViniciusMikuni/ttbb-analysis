#!/usr/bin/env python
from time import sleep
from scipy import stats
import os
import ROOT as rt
import  tdrstyle
rt.gStyle.SetOptStat(0)
rt.gStyle.SetErrorX(0) #turns of horizontal error bars (but also for bkg)
rt.gROOT.SetBatch(True)
import numpy as np
from collections import OrderedDict
from Plotting_cfg import *
import CMS_lumi
rt.gROOT.LoadMacro("../src/triggerWeightRound.h+")
tdrstyle.setTDRStyle()
saveplots = True
interestvar = ['n_bjets']
cut = '(BDT_Comb>0.657801)'
#cut = '(BDT_Comb>0.657801&&prob_chi2>0.125174 )'
fout =  rt.TFile("QCD_Estimate.root","RECREATE")
xdist = -0.35
r = {
    "CR1":{'cut':'(prob_chi2>0.125174 && BDT_CWoLa<0.170504 )','data':None,'bkg':None,'QCD':None},
    "CR2":{'cut':'(prob_chi2<0.125174 && BDT_CWoLa<0.170504 )','data':None,'bkg':None,'QCD':None},
    "VR":{'cut':'(prob_chi2<0.125174 && BDT_CWoLa>0.170504)','data':None,'bkg':None,'QCD':None},
    "SR":{'cut':'(prob_chi2>0.125174 && BDT_CWoLa>0.170504)','data':None,'bkg':None,'QCD':None}
}
# r = {
#     "CR1":{'cut':'(qgLR>0.5 && BDT_CWoLa<0.170504 )','data':None,'bkg':None,'QCD':None},
#     "CR2":{'cut':'(qgLR<0.5 && BDT_CWoLa<0.170504 )','data':None,'bkg':None,'QCD':None},
#     "VR":{'cut':'(qgLR<0.5 && BDT_CWoLa>0.170504)','data':None,'bkg':None,'QCD':None},
#     "SR":{'cut':'(qgLR>0.5 && BDT_CWoLa>0.170504)','data':None,'bkg':None,'QCD':None}
# }


ddata = {}
dbkg = {}
bkgs = ['dibosonCW','ttVCW','VJCW','s_topCW','ttbarCW']
f_data = rt.TFile(processfiles['dataCW'],"READ")
t_data = f_data.Get("tree")
files = {}
trees = {}
regions = OrderedDict(sorted(r.items(), key=lambda t: t[0]))
for process in bkgs:
    if process[:-2] in processgroup:
        for subprocess in processgroup[process[:-2]]:
            files[subprocess] = rt.TFile(processfiles[subprocess+'CW'],"READ")
            trees[subprocess] = files[subprocess].Get('tree')
    else:
        files[process] = rt.TFile(processfiles[process],"READ")
        trees[process] = files[process].Get('tree')

for var in interestvar:
    for reg in regions:
        t_data.Draw(var + '>>'+ 'hdata'+reg+ str(vartitle[var][1]),"weight*qgWeight*trigWeight(ht,jet5pt,n_bjets)*"+cut+"*"+regions[reg]['cut'])
        hdata = rt.gDirectory.Get('hdata'+reg).Clone('data'+reg)
        hdata.Sumw2()
        
        hbkg = hdata.Clone('bkg'+reg)
        hbkg.Reset()
        hbkg.Sumw2()
        for process in bkgs:
            if process[:-2] in processgroup:
                for subprocess in processgroup[process[:-2]]:
                    trees[subprocess].Draw(var + '>>'+ 'h'+reg+subprocess+ str(vartitle[var][1]),"weight*qgWeight*trigWeight(ht,jet5pt,n_bjets)*"+cut+"*"+regions[reg]['cut'])
                    h = rt.gDirectory.Get('h'+reg+subprocess).Clone('h'+reg)
                    h.Scale(dscale[subprocess])
                    #print type(hbkg),type(h)
                    hbkg.Add(h)

            else:
                trees[process].Draw(var + '>>'+ 'h'+reg+process+ str(vartitle[var][1]),"weight*qgWeight*trigWeight(ht,jet5pt,n_bjets)*"+cut+"*"+regions[reg]['cut'])
                h = rt.gDirectory.Get('h'+reg+process).Clone('h'+reg)
                h.Scale(dscale[process[:-2]])
                hbkg.Add(h)
                

        hres = hdata.Clone("hbkgsub"+reg)
        hres.Add(hbkg,-1)
        regions[reg]['QCD'] = hres
        regions[reg]['bkg'] = hbkg
        regions[reg]['data']= hdata

        if "CR" not in reg:
            if reg == 'SR':
                if regions['CR1']['QCD'] == None:
                    print 'Do CRs first!'
                    continue
                else:
                    nqcd = regions['CR1']['QCD'].Integral()
                    scale = hres.Integral()/nqcd
                    print 'scale SR: ',scale
                    hSR = regions['CR1']['QCD'].Clone('QCD'+reg)
                    hSR.Scale(scale)
                    regions[reg]['QCD'] = hSR
            if reg == 'VR':
                if regions['CR2']['QCD'] == None:
                    print 'Do CRs first!'
                    continue
                else:
                    nqcd = regions['CR2']['QCD'].Integral()
                    scale = hres.Integral()/nqcd
                    print 'scale VR: ',scale
                    hSR = regions['CR2']['QCD'].Clone('QCD'+reg)
                    hSR.Scale(scale)
                    regions[reg]['QCD'] = hSR



    for reg in regions:
        colors = {'ttbar':['#2c7fb8','t#bar{t} + Minor Bkgs.'],'Multijet':['#31a354','Multijet']}
        regions[reg]['data'].SetMarkerColor(1) 
        regions[reg]['data'].SetMarkerStyle(20)
        regions[reg]['data'].SetMarkerSize(1.0)
        regions[reg]['bkg'].SetFillColor(rt.TColor.GetColor(colors['ttbar'][0]))
        regions[reg]['QCD'].SetFillColor(rt.TColor.GetColor(colors['Multijet'][0]))
        hstack =  rt.THStack(vartitle[var][0],vartitle[var][0])
        hstack.Add(regions[reg]['QCD'])
        hstack.Add(regions[reg]['bkg'])
        c = rt.TCanvas(var+reg,var+reg,5,30,W_ref,H_ref)
        pad1 = rt.TPad("pad1", "pad1", 0, 0.15, 1, 1.0)
        pad1.Draw()
        pad1.cd()
        SetupCanvas(pad1, vartitle[var][2])            
        
        hframe = rt.TH1F(var,"h; {0}; Events ".format(vartitle[var][0]),vartitle[var][1][0],vartitle[var][1][1],vartitle[var][1][2])
        hframe.SetAxisRange(0.1, regions[reg]['data'].GetMaximum()*1e4 if vartitle[var][2] == 1 else regions[reg]['data'].GetMaximum()*1.8,"Y")
        xAxis = hframe.GetXaxis()
        xAxis.SetNdivisions(6,5,0)
        yAxis = hframe.GetYaxis()
        yAxis.SetNdivisions(6,5,0)
        yAxis.SetTitleOffset(1)
        hframe.Draw()
        c.Update()
        c.Modified()
        hstack.Draw("sameaxis")
        hstack.Draw('histsame')
        herr = regions[reg]['QCD'].Clone('stat.err')
        herr.Add(regions[reg]['bkg'])
        herr.SetFillColor( rt.kBlack )
        herr.SetMarkerStyle(0)
        herr.SetFillStyle(3354)
        rt.gStyle.SetHatchesLineWidth(1)
        rt.gStyle.SetHatchesSpacing(2)
        regions[reg]['data'].Draw("esamex0") 
        herr.Draw('e2same')
        CMS_lumi.CMS_lumi(c, iPeriod, iPos)
        
        pad1.cd()
        pad1.Update()
        pad1.RedrawAxis()
        frame = c.GetFrame()
        
        latex = rt.TLatex()
        
        legend =  rt.TPad("legend_0","legend_0",x0_l - 0.15,y0_l,x1_l, y1_l )
        
        legend.Draw()
        legend.cd()
        
        gr_l =  rt.TGraphErrors(1, x_l, y_l, ex_l, ey_l)            
        rt.gStyle.SetEndErrorSize(0)
        gr_l.SetMarkerSize(0.9)
        gr_l.Draw("0P")
        
        latex.SetTextFont(42)
        latex.SetTextAngle(0)
        latex.SetTextColor(rt.kBlack)    
        latex.SetTextSize(0.12)    
        latex.SetTextAlign(12) 
        yy_ = y_l[0]
        latex.DrawLatex(xx_+1.*bwx_,yy_,"Data")
        latex.DrawLatex(xx_+1.*bwx_,yy_-gap_,reg)
        for hist in colors:
            box_ = rt.TBox()
            SetupBox(box_,yy_,rt.TColor.GetColor(colors[hist][0]))
            box_.DrawBox( xx_-bwx_/2 - xdist, yy_-bwy_/2, xx_+bwx_/2 - xdist, yy_+bwy_/2 )
            box_.SetFillStyle(0)
            box_.DrawBox( xx_-bwx_/2 -xdist, yy_-bwy_/2, xx_+bwx_/2-xdist, yy_+bwy_/2 )
            latex.DrawLatex(xx_+1.*bwx_-xdist,yy_,colors[hist][1])
            yy_ -= gap_
            
        box_ = rt.TBox()
        SetupBox(box_,yy_)
        box_.SetFillStyle(3354)
        box_.DrawBox( xx_-bwx_/2 - xdist, yy_-bwy_/2, xx_+bwx_/2- xdist, yy_+bwy_/2 )
        latex.DrawLatex(xx_+1.*bwx_- xdist,yy_,'Stat. Uncert.')
        yy_ -= gap_
        c.Update()
        c.cd()
        p1r = rt.TPad("p4","",0,0,1,0.26)
            
        p1r.SetRightMargin(0.04)
        p1r.SetLeftMargin(0.12)
        p1r.SetTopMargin(0.0)
        p1r.SetBottomMargin(0.42)
        p1r.SetTicks()
        p1r.Draw()
        p1r.cd()
        
        xmin = float(herr.GetXaxis().GetXmin())
        xmax = float(herr.GetXaxis().GetXmax())
        one = rt.TF1("one","1",xmin,xmax)
        one.SetLineColor(1)
        one.SetLineStyle(2)
        one.SetLineWidth(1)
            
        nxbins = herr.GetNbinsX()
        hratio = regions[reg]['data'].Clone()
            
        he = herr.Clone()
        he.SetFillColor( 16 )
        he.SetFillStyle( 1001 )
            
        for b in range(nxbins):
            nbkg = herr.GetBinContent(b+1)
            ebkg = herr.GetBinError(b+1)
                
            ndata = regions[reg]['data'].GetBinContent(b+1)
            edata = regions[reg]['data'].GetBinError(b+1)
            r = ndata / nbkg if nbkg>0 else 0
            rerr = edata / nbkg if nbkg>0 else 0
                
            hratio.SetBinContent(b+1, r)
            hratio.SetBinError(b+1,rerr)
            
            he.SetBinContent(b+1, 1)
            he.SetBinError(b+1, ebkg/nbkg if nbkg>0 else 0 )

        hratio.GetYaxis().SetRangeUser(0.7,1.5)

        hratio.SetTitle("")
        
        hratio.GetXaxis().SetTitle(vartitle[var][0])
        hratio.GetXaxis().SetTitleSize(0.156)
        hratio.GetXaxis().SetLabelSize(0.171)
        #hratio.GetXaxis().SetTickLength(0.09)
            

        #for b in range(hratio.GetNbinsX()):
        #    hratio.GetXaxis().SetBinLabel(b+1, str(int(hratio.GetBinLowEdge(b+1))) )
            
        hratio.GetXaxis().SetLabelOffset(0.02)
            
        hratio.GetYaxis().SetTitleSize(0.196)
        hratio.GetYaxis().SetLabelSize(0.171)
        hratio.GetYaxis().SetTitleOffset(0.30)
        hratio.GetYaxis().SetTitle("      Data/Bkg")
        hratio.GetYaxis().SetDecimals(1)
        hratio.GetYaxis().SetNdivisions(4,2,0,rt.kTRUE) #was 402
        if  hist == 'catplot':
            for i in range(len(shortcats)): hratio.GetXaxis().SetBinLabel(i+1,shortcats[i])

        else: hratio.GetXaxis().SetNdivisions(6,5,0) 
            
        hratio.Draw("pe")
        #    setex2.Draw()
        he.Draw("e2same")
        one.Draw("SAME")
        #turn off horizontal error bars
        #    setex1.Draw()
        hratio.Draw("PEsame")
        hratio.Draw("PE0X0same")
        hratio.Draw("sameaxis") #redraws the axes                                                                                                                                                               
        p1r.Update()
        if saveplots:
            if not os.path.exists(destination+"/QCD Estimation"):
                os.makedirs(destination+"/QCD Estimation")
            else:
                print "WARNING: directory already exists. Will overwrite existing files..."
                c.SaveAs(destination+"/QCD Estimation/"+reg+".png")
    


        
        
fout.cd()
for reg in regions:
    regions[reg]['data'].Write()
    regions[reg]['bkg'].Write()
    regions[reg]['QCD'].Write()
        
            
                
        

            
            





