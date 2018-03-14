
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
import pandas as pd
rt.gROOT.SetBatch(True)
rt.gROOT.LoadMacro("../src/triggerWeightRound.h+")
tdrstyle.setTDRStyle()

plot_overflow = 0
saveplots = 1
nwhichcut = 0
qcdtop = 1
plotnostack = 0


treeplots = ['n_bjets']

#'top1_m','top2_m','w1_m','w2_m',
#treeplots =['BDT_Comb','BDT_ttbar','BDT_ttbarMajo','BDT_QCD']
#'qgLR','top1_m','top2_m','w1_m','w2_m','top1_pt','top2_pt','deltaRb1b2','deltaPhiw1w2','deltaPhit1t2','deltaPhib1b2','b1_csv','b2_csv','simple_chi2','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[0]','addJet_CSV[1]','btagLR4b','btagLR3b','centrality','aplanarity','prob_chi2','meanDeltaRbtag','meanCSV','meanCSVbtag'
#treeplots = ['n_addJets','n_addbjets','simple_chi2','deltaRb1b2','catplot']
cut = ['prob_chi2 >= 0.0','prob_chi2 > 0.004','prob_chi2 > 0.01','prob_chi2 > 0.05','prob_chi2 > 0.1','prob_chi2 > 0.2']
addCut = 'prob_chi2>=0'
#addCut = 'abs(w1_m - 80.4)<70 && abs(w2_m - 80.4)<70 && BDT_QCD != 0'
#addCut = 'BDT_Comb>0.90597 && BDT_CWoLa>0.946569 && prob_chi2>0.53755 ' #0.1 eff
#addCut = 'BDT_Comb>0.43763 && BDT_CWoLa>0.913062 && prob_chi2>0.214522' #0.2 eff
#addCut = 'BDT_Comb>0.632452 && BDT_CWoLa>0.693231 && prob_chi2>0.165256' #0.3 eff
#addCut = 'BDT_Comb> 0.657801 && BDT_CWoLa>0.170504 && prob_chi2>0.125174 ' #0.4 eff
#addCut = 'BDT_Comb>0.564178 && BDT_CWoLa>-0.201408 && prob_chi2> 0.0260956 ' #0.5 eff
#addCut = 'BDT_Comb>0.449587 && BDT_CWoLa>-0.633217 && prob_chi2>0.0014671 ' #0.6 eff
#addCut = 'BDT_Comb>-0.133546 && BDT_CWoLa>-0.252623 && prob_chi2>-0.00229578 ' #0.7 eff
#addCut = 'BDT_Comb>-0.259989  && BDT_CWoLa>-0.678918 && prob_chi2>0 ' #0.8 eff
#addCut = 'BDT_Comb>-0.462216 && BDT_CWoLa>-0.951427 && prob_chi2>0 ' #0.9 eff



#cats = ["n_bjets == 2 && n_jets == 8","n_bjets == 3 && n_jets == 8","n_bjets >= 4 && n_jets == 8","n_bjets == 2 && n_jets == 9","n_bjets == 3 && n_jets == 9","n_bjets >= 4 && n_jets == 9"]
#cats = ["n_bjets>=3","n_bjets == 3 && n_jets == 7","n_bjets >= 4 && n_jets == 7","n_bjets == 3 && n_jets == 8","n_bjets >= 4 && n_jets == 8","n_bjets == 3 && n_jets >= 9","n_bjets >= 4 && n_jets >= 9"]
#shortcats = ["All","3b7j","4b7j","3b8j","4b8j","3b9j","4b9j"]
cats = ["n_bjets>=2","n_bjets == 2","n_bjets == 3","n_bjets == 4","n_bjets >= 5"]
#,"n_bjets == 3","n_bjets == 4","n_bjets >= 5"]
shortcats = ["All","2b","3b","4b","5b or more"]
#,"3b","4b","5b or more"]
#cats = ["n_jets >= 7","n_jets == 7 ","n_jets == 8","n_jets >= 9"]
#shortcats = ["All","7 jets","8 jets","9 jets or more"]



table = {'Process':shortcats}
table['Total bkg.']=np.zeros(len(cats))
table['Total err'] = np.zeros(len(cats))
processlist = ['data','ttbar','diboson','ttV','VJ','s_top','QCD'] if qcdtop else ['data','ttbar','diboson','ttV','VJ','s_top','QCD']

#'diboson','ttV','VJ','s_top',
dcats = {}
for proc in ttplot + ['data', 'QCD','diboson','s_top','ttV','VJ']:
    dcats[proc] = rt.TH1F(proc,proc,10,1,11)


files = []
for iproc, process in enumerate(processlist): #ntuple files
    if process in processgroup:
        files.append([])
        table[plotCosmetics[process][0]]=[]
        for subprocess in processgroup[process]:
            files[iproc].append(rt.TFile(processfiles[subprocess],"READ"))
    else:
        files.append(rt.TFile(processfiles[process],"READ"))
        table[plotCosmetics[process][0]] = []


for mode in ttplot:table[plotCosmetics[mode][0]] = []
if len(treeplots) > 0: 
    for hist in  treeplots: #each variable
        rt.gDirectory.GetList().Delete()
        hframe = rt.TH1F(hist,"h; {0}; Events ".format(vartitle[hist][0]),vartitle[hist][1][0],vartitle[hist][1][1],vartitle[hist][1][2])
        for  ncat, cat in enumerate(cats):
            if  hist == 'catplot' and ncat > 0: continue 
            c = rt.TCanvas(hist,hist,5,30,W_ref,H_ref)
            pad1 = rt.TPad("pad1", "pad1", 0, 0.15, 1, 1.0)
            pad1.Draw()
            pad1.cd()
            SetupCanvas(pad1, vartitle[hist][2])            
                

            nbkg = ndata = 0
            hlist_ = []
            hstack =  rt.THStack(vartitle[hist][0],vartitle[hist][0])

            for num, process in enumerate(processlist): #for each file

                if   hist != 'catplot'  :
                    nprocess = {}
                    nprocerror = {}

                    if process in processgroup:
                        
                        h = hframe.Clone(hist + process)
                        h.Reset()
                        for isub, subprocess in enumerate(processgroup[process]):
                            
                            tvar = files[num][isub].Get('tree')
#                            print subprocess
                            tvar.Draw(hist+">>h"+str(isub)+str(nwhichcut)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")")
                            hsub = rt.gDirectory.Get("h"+str(isub)+str(nwhichcut)).Clone(hist+ process)
                            hsub.Scale(dscale[subprocess])
                            
                            table['Total bkg.'][ncat]+=hsub.Integral()
                            table['Total err'][ncat] += sqrt(hsub.GetSumw2().GetSum())

                            nbkg += hsub.Integral()
                            h.Add(hsub)
                        h.SetFillColor(rt.TColor.GetColor(plotCosmetics[process][1]))
                        if dcats[process].GetBinContent(ncat +1) == 0:
#                            print 'process', process, 'int: ', h.Integral()
                            dcats[process].SetBinContent(ncat+1,h.Integral())

                        hlist_.append(h)
                        table[plotCosmetics[process][0]].append(str(round(h.Integral(),2))+'$#pm$'+str(round(sqrt(h.GetSumw2().GetSum()),2)))
                    else:
                        tvar = files[num].Get('tree')
#                        print process
                        tvar.Draw(hist+">>h"+str(nwhichcut)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")")
                        h = rt.gDirectory.Get("h"+str(nwhichcut)).Clone(hist+ process)
                else:
                    h = dcats[process]
            
                if plot_overflow: AddOverflow(h)
                    
                if process == 'data':
                    if   hist != 'catplot':
                        h.SetMarkerColor(1) 
                        h.SetMarkerStyle(20)
                        h.SetMarkerSize(1.0)
                        ndata = h.Integral()
                        table[plotCosmetics[process][0]].append(str(int(ndata)))
                        print 'Number of Data events: ',ndata, 'category: ',cat
                        if dcats[process].GetBinContent(ncat +1) == 0:
                            dcats[process].SetBinContent(ncat+1,ndata)
                    hdata = h.Clone('hdata')
                    
                if process in processgroup:
                    if hist == 'catplot':
                        h.SetFillColor(rt.TColor.GetColor(plotCosmetics[process][1]))
                        hlist_.append(h)
                    
                if process == 'ttbar':
                    if hist != 'catplot':
                        nbkg += h.Integral()*dscale[process]
                        print 'Number of ttbar events: ',h.Integral()*dscale[process], 'category: ',cat
                        #print 'S/sqrt(B+S): ', h.Integral()*dscale[process]/sqrt(ndata)
                        #print 'S/B: ', h.Integral()*dscale[process]/(ndata - h.Integral()*dscale[process])
                        #print h.Integral()*dscale[process], ndata - h.Integral()*dscale[process]
                        
                        if qcdtop: ttplot.reverse()
                    for i,mode in enumerate(ttplot):
                        if hist != 'catplot':
                            tvar.Draw(hist+">>httbar"+str(vartitle[hist][1]),"("+ttCls[mode]+")*weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")")
                            httbar = rt.gDirectory.Get("httbar").Clone(hist+ mode)
                            httbar.Scale(dscale[process])
                            table[plotCosmetics[mode][0]].append(str(round(httbar.Integral(),2))+'$#pm$'+str(round(sqrt(httbar.GetSumw2().GetSum()),2)))
                            if mode not in ['ttbarbb','ttbar2b','ttbarb']:
                                table['Total bkg.'][ncat]+=httbar.Integral()
                                table['Total err'][ncat] += sqrt(httbar.GetSumw2().GetSum())

                            #print mode, ' yield: ',httbar.Integral(), '$#pm$',sqrt(httbar.GetSumw2().GetSum())


                            if dcats[mode].GetBinContent(ncat +1) == 0:
                                dcats[mode].SetBinContent(ncat+1,httbar.Integral())

                        else: httbar = dcats[mode]        

                        httbar.SetFillColor(rt.TColor.GetColor(plotCosmetics[mode][1]))
                        if plot_overflow: AddOverflow(httbar)
                            
                        hlist_.append(httbar)
                if process == 'QCD':
                    if num != len(processlist)-1:print 'QCD not the last process, the normalization will be wrong!!'
                    h.SetFillColor(rt.TColor.GetColor(plotCosmetics[process][1]))
                    scaleqcd = (ndata - nbkg)/h.Integral() if h.Integral() > 0 else 1

                    if hist != 'catplot':
                        h.Scale(scaleqcd)
                        table[plotCosmetics[process][0]].append(str(round(h.Integral(),2))+'$#pm$'+str(round(sqrt(h.GetSumw2().GetSum()),2)))
                        table['Total bkg.'][ncat]+=h.Integral()
                        table['Total err'][ncat] += sqrt(h.GetSumw2().GetSum())

                        if dcats[process].GetBinContent(ncat+1) == 0:
                            dcats[process].SetBinContent(ncat+1,h.Integral())
                        
                    hlist_.append(h)
            if qcdtop: hlist_.reverse()
            for histtostack in hlist_:
#                print histtostack.GetName()
                hstack.Add(histtostack)
            print len(hlist_)
            herr = hlist_[nwhichcut].Clone('herr')
            herr.Reset()
            hframe.SetAxisRange(0.1, hstack.GetMaximum()*1e4 if vartitle[hist][2] == 1 else hstack.GetMaximum()*1.8,"Y");
#            hframe.SetMinimum(0.1)
#            hframe.SetMaximum( hstack.GetMaximum()*1e4 if vartitle[hist][2] == 1 else hstack.GetMaximum()*1.5)
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

            
            for hprocess in hlist_:
                herr.Add(hprocess)
                
            herr.SetFillColor( rt.kBlack )
            herr.SetMarkerStyle(0)
            herr.SetFillStyle(3354)
            rt.gStyle.SetHatchesLineWidth(1)
            rt.gStyle.SetHatchesSpacing(2)
            hdata.Draw("esamex0") 
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

            for nkey, key in enumerate(plotCosmetics):
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

            box_ = rt.TBox()
            #yy_ -= gap_
            xdist = -0.35
            SetupBox(box_,yy_)
            box_.SetFillStyle(3354)
            box_.DrawBox( xx_-bwx_/2 - xdist, yy_-bwy_/2, xx_+bwx_/2- xdist, yy_+bwy_/2 )
            latex.DrawLatex(xx_+1.*bwx_- xdist,yy_,'Stat. Uncert.')
            yy_ -= gap_
            latex.SetTextSize(0.07)    
            latex.DrawLatex(xx_,yy_,cat)
            #update the canvas to draw the legend
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
            hratio = hdata.Clone()
            
            he = herr.Clone()
            he.SetFillColor( 16 )
            he.SetFillStyle( 1001 )
            
            for b in range(nxbins):
                nbkg = herr.GetBinContent(b+1)
                ebkg = herr.GetBinError(b+1)
                
                ndata = hdata.GetBinContent(b+1)
                edata = hdata.GetBinError(b+1)
                r = ndata / nbkg if nbkg>0 else 0
                rerr = edata / nbkg if nbkg>0 else 0
                
                hratio.SetBinContent(b+1, r)
                hratio.SetBinError(b+1,rerr)
                
                he.SetBinContent(b+1, 1)
                he.SetBinError(b+1, ebkg/nbkg if nbkg>0 else 0 )

            hratio.GetYaxis().SetRangeUser(0.7,1.5)

            hratio.SetTitle("")

            hratio.GetXaxis().SetTitle(vartitle[hist][0])
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
                #if qcdtop: destination += '_QCD_First'
                if not os.path.exists(destination+"/"+cut[nwhichcut]):
                    os.makedirs(destination+"/"+cut[nwhichcut])
                else:
                    print "WARNING: directory already exists. Will overwrite existing files..."
                c.SaveAs(destination+"/"+cut[nwhichcut]+"/"+vartitle[hist][0]+shortcats[ncat]+".png")

        rt.gDirectory.GetList().Delete()
        #FormatTable(table)
                              






