#Plotting.py
import os
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *
import numpy as np
rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)
tdrstyle.setTDRStyle()
saveplots = 1
plotData = 1
is_binOpt=False
ch = 'SR'
var = 'btagLR4b'
fname = '../Datasets/ttbb_fit.root'
f = rt.TFile(fname,"READ")

cats = ['prefit','postfit']
processlist = ['data_obs','ttlf','QCD','ttcc','ttb','ttbb','tt2b','ttV','stop','VJ','ttH','VV']
if ch=='ch2': processlist = ['data_obs','QCD','ttlf','ttcc','ttb','ttbb','tt2b','ttV','stop','VJ','ttH','VV']
processlist.reverse()
for cat in cats:
    hstack =  rt.THStack('fit_'+cat,'fit_'+cat)
    fit = {}
    for proc in processlist:
        fit[proc] = f.Get(ch+'_'+cat+'/'+proc)
        if 'data' not in proc:
            fit[proc].SetFillColor(rt.TColor.GetColor(plotCosmetics[proc][1]))

            hstack.Add(fit[proc])
        else:
            fit[proc].SetMarkerColor(1)
            fit[proc].SetMarkerStyle(20)
            fit[proc].SetMarkerSize(1.0)

    c = rt.TCanvas(var,var,5,30,W_ref,H_ref)
    pad1 = rt.TPad("pad1", "pad1", 0.0, 0.15 if plotData else 0.0, 1, 1.0)
    pad1.Draw()
    pad1.cd()
    SetupCanvas(pad1, cat)
    if is_binOpt:
        hframe = rt.TH1F(var,"; {0}; Events ".format(vartitle[var][0]),len(opt_bin)-1,opt_bin)
    else:
        hframe = rt.TH1F(var,"; {0}; Events ".format(vartitle[var][0]),vartitle[var][1][0],vartitle[var][1][1],vartitle[var][1][2])

    herr = fit['data_obs'].Clone('herr')

    herr.Reset()

    hframe.SetAxisRange(0.1, hstack.GetMaximum()*1e4 if vartitle[var][2] == 1 else hstack.GetMaximum()*1.8,"Y");
    xAxis = hframe.GetXaxis()
    xAxis.SetNdivisions(6,5,0)


    yAxis = hframe.GetYaxis()
    yAxis.SetNdivisions(6,5,0)
    yAxis.SetTitleOffset(0.9)
    yAxis.SetMaxDigits(2)
    hframe.Draw()
    c.Update()
    c.Modified()
    hstack.Draw("sameaxis")


    hstack.Draw('histsame')



    for hprocess in fit:
        if 'data' not in hprocess: herr.Add(fit[hprocess])
    herr.SetFillColor( rt.kBlack )
    herr.SetMarkerStyle(0)
    herr.SetFillStyle(3354)
    rt.gStyle.SetHatchesLineWidth(1)
    rt.gStyle.SetHatchesSpacing(2)
    if plotData:
        fit['data_obs'].Draw("esamex0")
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

    if plotData:
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
    if plotData:
        latex.DrawLatex(xx_+1.*bwx_,yy_,"Data")
        nkey=0
    for key in fit:
        if 'data' in key:continue
        box_ = rt.TBox()
        SetupBox(box_,yy_,rt.TColor.GetColor(plotCosmetics[key][1]))
        if nkey %2 == 0:
            xdist = -0.35
        else:
            yy_ -= gap_
            xdist = 0
        box_.DrawBox( xx_-bwx_/2 - xdist, yy_-bwy_/2, xx_+bwx_/2 - xdist, yy_+bwy_/2 )
        box_.SetFillStyle(0)
        box_.DrawBox( xx_-bwx_/2 -xdist, yy_-bwy_/2, xx_+bwx_/2-xdist, yy_+bwy_/2 )
        latex.DrawLatex(xx_+1.*bwx_-xdist,yy_,plotCosmetics[key][0])
        nkey+=1

    box_ = rt.TBox()
    yy_ -= gap_
    xdist = -0.35
    SetupBox(box_,yy_)
    box_.SetFillStyle(3354)
    box_.DrawBox( xx_-bwx_/2 - xdist, yy_-bwy_/2, xx_+bwx_/2- xdist, yy_+bwy_/2 )
    latex.DrawLatex(xx_+1.*bwx_- xdist,yy_,'Stat. Uncert.')
    #yy_ -= gap_
    #latex.SetTextSize(0.07)
    #latex.DrawLatex(xx_,yy_,cat)
    #update the canvas to draw the legend
    c.Update()



    if plotData:
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
        hratio = fit['data_obs'].Clone()

        he = herr.Clone()
        he.SetFillColor( 16 )
        he.SetFillStyle( 1001 )

        for b in range(nxbins):
            nbkg = herr.GetBinContent(b+1)
            ebkg = herr.GetBinError(b+1)

            ndata = fit['data_obs'].GetBinContent(b+1)
            edata = fit['data_obs'].GetBinError(b+1)
            r = ndata / nbkg if nbkg>0 else 0
            rerr = edata / nbkg if nbkg>0 else 0

            hratio.SetBinContent(b+1, r)
            hratio.SetBinError(b+1,rerr)

            he.SetBinContent(b+1, 1)
            he.SetBinError(b+1, ebkg/nbkg if nbkg>0 else 0 )

        hratio.GetYaxis().SetRangeUser(0.5,1.5)

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
        hratio.GetXaxis().SetNdivisions(6,5,0)

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
        #if qcdtop: destination += '_QCD_First'
        if not os.path.exists(destination+"/Postfit"):
            os.makedirs(destination+"/Postfit")
        else:
            print "WARNING: directory already exists. Will overwrite existing files..."
        c.SaveAs(destination+"/Postfit/"+vartitle[var][0]+cat+ch+".png")
