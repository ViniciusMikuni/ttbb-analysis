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

plot_overflow = 1
saveplots = 1
useddQCD = 1 #not implemented
nwhichcut = 0
qcdtop = 0
plotnostack = 0
plotData = 1
qg_corr=0

#treeplots = [
    #'lp1_eta','lp2_eta','lq1_eta','lq2_eta','b1_eta','b2_eta',
    #'top1_m','top2_m','w1_m','w2_m','deltaRp1p2','deltaRq1q2',
    #'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]',
    #'deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhiw1w2',
    # 'deltaPhit1t2','p1b1_mass','q1b2_mass','deltaRb1w2','deltaRb2w1',
    # 'mindeltaRb1p','simple_chi2','mindeltaRb2q', 'deltaEtap1p2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]',
    # 'jet_CSV[5]']
treeplots = [
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
                ]
#             #'deltaPhit1t2','p1b1_mass','q1b2_mass','deltaRb1w2','deltaRb2w1',
#             # 'mindeltaRb1p','simple_chi2','mindeltaRb2q', 'deltaEtap1p2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]',
#             # 'jet_CSV[5]'
#             ]
treeplots = ['BDT_CWoLa']
# 'top1_m','top2_m','w1_m','w2_m','deltaRp1p2','deltaRq1q2',
# 'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]',
# 'deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhiw1w2','deltaPhit1t2','p1b1_mass','q1b2_mass','deltaRb1w2','deltaRb2w1',
# 'mindeltaRb1p','simple_chi2','mindeltaRb2q', 'deltaEtap1p2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]',
# 'jet_CSV[5]']
#'addJet_CSV[0]','addJet_CSV[1]','ht','top1_m','top2_m','w1_m','w2_m','deltaRb1b2','btagLR4b'


#'top1_m','top2_m','w1_m','w2_m',
#treeplots =['btagLR4b','top1_m']
#'qgLR','top1_m','top2_m','w1_m','w2_m','top1_pt','top2_pt','deltaRb1b2','deltaPhiw1w2','deltaPhit1t2','deltaPhib1b2','b1_csv','b2_csv','simple_chi2','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_CSV[0]','addJet_CSV[1]','btagLR4b','btagLR3b','centrality','aplanarity','prob_chi2','meanDeltaRbtag','meanCSV','meanCSVbtag'
#treeplots = ['n_addJets','n_addbjets','simple_chi2','deltaRb1b2','catplot']
cut = ['prob_chi2>1e-6','prob_chi2 > 0.004','prob_chi2 > 0.01','prob_chi2 > 0.05','prob_chi2 > 0.1','prob_chi2 > 0.2']
#addCut = 'prob_chi2>=0'
#'jet_CSV[0]>=0.8484 && jet_CSV[1]>=0.8484'

#addCut = 'simple_chi2<38.0848 && BDT_CWoLa > 0.208115 && BDT_Comb > 0.834643 && qgLR > 0.502521' #0.2 eff with all

#addCut = 'simple_chi2<19.4573 && BDT_CWoLa >  0.115104 && BDT_Comb > -0.866382 && qgLR > 0.648321' #tmva
#addCut = 'simple_chi2<34.4046 && BDT_CWoLa > 0.221061 && BDT_Comb > 0.102203 && qgLR > 0.722416' #tmva
#addCut = 'n_jets>0'


####################################################################################
#addCut = 'simple_chi2<23.41 && BDT_CWoLa > 0.27 && BDT_Comb > 0.83 && qgLR > 0.39' #RGS
#addCut = 'simple_chi2<23.0381 && BDT_CWoLa > 0.318789 && BDT_Comb > 0.197704 && qgLR > 0.2655' #TMVA 30%
#addCut = 'simple_chi2<9.4301 && BDT_CWoLa > 0.3234 && BDT_Comb > -0.971857 && qgLR > 0.636581' #TMVA 20%
#addCut = 'simple_chi2<38.8797 && BDT_CWoLa > 0.335974 && BDT_Comb > -0.661968 && qgLR > 0.35119' #TMVA 20% without btagLR info
#addCut = 'simple_chi2<19.7491 && BDT_CWoLa > 0.206721 && BDT_Comb > 0.664107 && qgLR > 0.444917' #TMVA 30% without btagLR info
#addCut ='(n_jets>=8 && simple_chi2<20.54 && BDT_CWoLa > 0.22 && BDT_Comb > 0.8 && qgLR > 0.42)' #RGS
#addCut ='(n_jets>=8 && simple_chi2<20.54 && BDT_CWoLa > 0.22 && BDT_Comb > 0.0 && qgLR > 0.52)' #RGS
#addCut ='(n_jets>=8 && BDT_CWoLa > 0.5 && prob_chi2>6e-2 && qgLR > 0.6 )' #RGS
# && BDT_CWoLa > 0.36 && qgLR > 0.87
addCut ='(n_jets>=8&&nBCSVM>=2&&qgLR>0.87&&BDT_CWoLa>=0.36&&BDT_Comb>=-1)' #RGS





####################################################################################

#addCut = 'simple_chi2<35.0765  && BDT_CWoLa > 0.150117 && BDT_Comb > 0.773671 && qgLR > 0.271297' #0.3 eff with all
#addCut = 'simple_chi2<12.4717  && BDT_CWoLa > -0.0302476 && BDT_Comb > 0.808274 && qgLR > 0.329137' #0.4 eff with all
#addCut = 'BDT_Comb< 0.625664 && BDT_CWoLa<-0.800936'
#addCut = 'abs(w1_m - 80.4)<70 && abs(w2_m - 80.4)<70 && BDT_QCD != 0'
#addCut = 'BDT_Comb>=0.8226 && BDT_CWoLa>=0.383442 && simple_chi2<= 10.5246 ' #0.1 eff + bjet req
#addCut = 'BDT_Comb>=-0.0888095 && BDT_CWoLa>=0.334826 && simple_chi2<= 7.37905 ' #0.1 eff
#addCut = 'BDT_Comb>=0.834643 && BDT_CWoLa>=0.208115 && simple_chi2<=18.0848 && qgLR < 0.502521' #0.2 eff
#addCut = 'BDT_Comb>0.851269 && BDT_CWoLa>-0.00391129  && prob_chi2>0.0855903' #0.3 eff
#addCut = 'BDT_Comb>0.825743 && BDT_CWoLa>-0.64938 && prob_chi2>0.00857808 ' #0.4 eff
#addCut = 'BDT_Comb>0.713374 && BDT_CWoLa>-0.0495359 && simple_chi2<= 29.9112 && qgLR > 0.350942 ' #0.5 eff
#addCut = 'BDT_Comb> 0.534335 && BDT_CWoLa>-0.0525544 && simple_chi2<= 23.6689 && qgLR > 0.105208 ' #0.6 eff
#addCut = 'BDT_Comb> 0.638816 && BDT_CWoLa>-0.0456259 && simple_chi2<= 33.8038' #0.6 eff
#addCut = 'BDT_Comb>0.34140 && BDT_CWoLa>-0.889451 && prob_chi2>=0.0 ' #0.7 eff
#addCut = 'BDT_Comb>-0.017229  && BDT_CWoLa>-0.960356 && prob_chi2>=0.0 ' #0.8 eff
#addCut = 'BDT_Comb>-0.449498 && BDT_CWoLa>-0.998016  && prob_chi2>=0.0 ' #0.9 eff



#cats = ["n_bjets == 2 && n_jets == 8","n_bjets == 3 && n_jets == 8","n_bjets >= 4 && n_jets == 8","n_bjets == 2 && n_jets == 9","n_bjets == 3 && n_jets == 9","n_bjets >= 4 && n_jets == 9"]
#cats = ["n_bjets>=3","n_bjets == 3 && n_jets == 7","n_bjets >= 4 && n_jets == 7","n_bjets == 3 && n_jets == 8","n_bjets >= 4 && n_jets == 8","n_bjets == 3 && n_jets >= 9","n_bjets >= 4 && n_jets >= 9"]
#shortcats = ["All","3b7j","4b7j","3b8j","4b8j","3b9j","4b9j"]
#cats = ["n_bjets>=2","n_bjets == 2","n_bjets == 3","n_bjets == 4","n_bjets >= 5"]
#cats = ["n_bjets>=2","n_bjets==2","n_bjets==3","n_bjets==4","n_bjets>=5"]
cats = ["nBCSVM>=2"]
#,"n_bjets == 2","n_bjets == 3","n_bjets == 4","n_bjets >= 5"]
#,"n_bjets == 3","n_bjets == 4","n_bjets >= 5"]
#shortcats = ["All(2b8j)","2b","3b","4b","5b or more"]
#shortcats = ["All(2b8j)","2b","3b","4b","5b"]
shortcats = ["All(2b8j)"]

#,"2b","3b","4b","5b or more"]
#,"3b","4b","5b or more"]
#cats = ["n_jets >= 7","n_jets == 7 ","n_jets == 8","n_jets >= 9"]
#shortcats = ["All","7 jets","8 jets","9 jets or more"]



table = {'Process':shortcats}
table['Total bkg.']=np.zeros(len(cats))
table['Total err'] = np.zeros(len(cats))
#processlist = ['data','ttbar','diboson','ttV','VJ','stop','ttH','QCD'] if qcdtop else ['data','ttH','stop','VJ','ttV','diboson','ttbar','QCD']
#processlist = ['data','ttbar','diboson','ttV','VJ','stop','QCD'] if qcdtop else ['data','diboson','ttV','VJ','stop','ttbar','QCD']
processlist = ['data','ttbar','diboson','ttV','VJ','ttH','stop','QCD'] if qcdtop else ['data','diboson','ttV','ttH','VJ','stop','ttbar','QCD']

#'diboson','ttV','ttH','VJ','stop',,
dcats = {}
for proc in ttplot + ['data', 'QCD','diboson','stop','ttV','VJ','ttH']:
#for proc in ttplot + ['data', 'QCD','diboson','stop','ttV','VJ','ttH']:
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
        if 'ttbar' not in process:
            table[plotCosmetics[process][0]] = []


for mode in ttplot:table[plotCosmetics[mode][0]] = []
if len(treeplots) > 0:
    for hist in  treeplots: #each variable
        rt.gDirectory.GetList().Delete()
        hframe = rt.TH1F(hist,"h; {0}; Events ".format(vartitle[hist][0]),vartitle[hist][1][0],vartitle[hist][1][1],vartitle[hist][1][2])
        for  ncat, cat in enumerate(cats):
            if  hist == 'catplot' and ncat > 0: continue
            c = rt.TCanvas(hist,hist,5,30,W_ref,H_ref)
            pad1 = rt.TPad("pad1", "pad1", 0.0, 0.15 if plotData else 0.0, 1, 1.0)
            pad1.Draw()
            pad1.cd()
            SetupCanvas(pad1, vartitle[hist][2])


            nbkg = ndata = 0
            hlist_ = []
            hstack =  rt.THStack(vartitle[hist][0],vartitle[hist][0])

            for num, process in enumerate(processlist): #for each file


                print process
                if 'ttbar' in  process: weight="trigweight*qgweight*weight*puweight*btagweight*topweight*"
                else:
                    weight = "trigweight*qgweight*weight*puweight*btagweight*"
                if   hist != 'catplot'  :
                    nprocess = {}
                    nprocerror = {}

                    if process in processgroup:

                        h = hframe.Clone(hist + process)
                        h.Reset()
                        for isub, subprocess in enumerate(processgroup[process]):
                            print subprocess
                            tvar = files[num][isub].Get('tree')
#                            print subprocess
                            print hist+">>h"+str(isub)+str(nwhichcut)+ str(vartitle[hist][1]),weight+"("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")"
                            tvar.Draw(hist+">>h"+str(isub)+str(nwhichcut)+ str(vartitle[hist][1]),weight+"("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")")
                            hsub = rt.gDirectory.Get("h"+str(isub)+str(nwhichcut)).Clone(hist+ process)
                            hsub.Scale(dscale[subprocess])
                            if process != "QCD":
                                if qg_corr:hsub.Scale(qwfac[subprocess])
                                table['Total bkg.'][ncat]+=hsub.Integral()
                                table['Total err'][ncat] += sqrt(hsub.GetSumw2().GetSum())

                                nbkg += hsub.Integral()
                            h.Add(hsub)
                        h.SetFillColor(rt.TColor.GetColor(plotCosmetics[process][1]))
                        if dcats[process].GetBinContent(ncat +1) == 0:
#                            print 'process', process, 'int: ', h.Integral()
                            dcats[process].SetBinContent(ncat+1,h.Integral())

                        hlist_.append(h)
                        if process != 'QCD':
                            table[plotCosmetics[process][0]].append(str(round(h.Integral(),2))+'$pm$'+str(round(sqrt(h.GetSumw2().GetSum()),2)))
                    else:
                        tvar = files[num].Get('tree')
                        #print process
                        #print hist+">>h"+str(nwhichcut)+ str(vartitle[hist][1]),(weight if process != 'data' else '1*')+"("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")"
                        tvar.Draw(hist+">>h"+str(nwhichcut)+ str(vartitle[hist][1]),(weight if process != 'data' else '1*')+"("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")")
                        print hist+">>h"+str(nwhichcut)+ str(vartitle[hist][1]),(weight if process != 'data' else '1*')+"("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")"

                        h = rt.gDirectory.Get("h"+str(nwhichcut)).Clone(hist+ process)
                        if process == 'ttH':
                            h.Scale(dscale[process])
                            if qg_corr:h.Scale(qwfac[process])
                            h.SetFillColor(rt.TColor.GetColor(plotCosmetics[process][1]))
                            hlist_.append(h)
                            table[plotCosmetics[process][0]].append(str(round(h.Integral(),2))+'$pm$'+str(round(sqrt(h.GetSumw2().GetSum()),2)))
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
                        #print 'Number of Data events: ',ndata, 'category: ',cat
                        if dcats[process].GetBinContent(ncat +1) == 0:
                            dcats[process].SetBinContent(ncat+1,ndata)
                    hdata = h.Clone('hdata')

                if process in processgroup:
                    if hist == 'catplot':
                        h.SetFillColor(rt.TColor.GetColor(plotCosmetics[process][1]))
                        hlist_.append(h)

                if 'ttbar' in process:
                    if hist != 'catplot':
                        #nbkg += h.Integral()*dscale[process]
                        #print 'Number of ttbar events: ',h.Integral()*dscale[process], 'category: ',cat
                        #print 'S/sqrt(B+S): ', h.Integral()*dscale[process]/sqrt(ndata)
                        #print 'S/B: ', h.Integral()*dscale[process]/(ndata - h.Integral()*dscale[process])
                        #print h.Integral()*dscale[process], ndata - h.Integral()*dscale[process]

                        if qcdtop: ttplot.reverse()
                    for i,mode in enumerate(ttplot):
                        if hist != 'catplot':
                            tvar.Draw(hist+">>httbar"+str(vartitle[hist][1]),"("+ttCls[mode]+")*"+weight+"("+addCut+"&&"+cut[nwhichcut]+"&&"+cat+")")
                            httbar = rt.gDirectory.Get("httbar").Clone(hist+ mode)
                            httbar.Scale(dscale[process])
                            if qg_corr:httbar.Scale(qwfac[mode])
                            table[plotCosmetics[mode][0]].append(str(round(httbar.Integral(),2))+'$pm$'+str(round(sqrt(httbar.GetSumw2().GetSum()),2)))
                            nbkg+=httbar.Integral()
                            if mode not in ['ttbb','tt2b','ttb']:

                                table['Total bkg.'][ncat]+=httbar.Integral()
                                table['Total err'][ncat] += sqrt(httbar.GetSumw2().GetSum())

                            #print mode, ' yield: ',httbar.Integral(), '$pm$',sqrt(httbar.GetSumw2().GetSum())


                            if dcats[mode].GetBinContent(ncat +1) == 0:
                                dcats[mode].SetBinContent(ncat+1,httbar.Integral())

                        else: httbar = dcats[mode]

                        httbar.SetFillColor(rt.TColor.GetColor(plotCosmetics[mode][1]))
                        if plot_overflow: AddOverflow(httbar)

                        hlist_.append(httbar)
                if process == 'QCD':
                    if num != len(processlist)-1:print 'QCD not the last process, the normalization will be wrong!!'
                    h.SetFillColor(rt.TColor.GetColor(plotCosmetics[process][1]))
                    print 'ndata',ndata,' nbkg ',nbkg,' int ',h.Integral()
                    scaleqcd = (ndata - nbkg)/h.Integral() if h.Integral() > 0 else 1

                    if hist != 'catplot':
                        h.Scale(scaleqcd)
                        table[plotCosmetics[process][0]].append(str(round(h.Integral(),2))+'$pm$'+str(round(sqrt(h.GetSumw2().GetSum()),2)))
                        table['Total bkg.'][ncat]+=h.Integral()
                        table['Total err'][ncat] += sqrt(h.GetSumw2().GetSum())

                        if dcats[process].GetBinContent(ncat+1) == 0:
                            dcats[process].SetBinContent(ncat+1,h.Integral())

                    #hlist_.append(h)
            if qcdtop: hlist_.reverse()
            for histtostack in hlist_:
                #print histtostack.GetName()
                hstack.Add(histtostack)
            #print len(hlist_)
            herr = hlist_[nwhichcut].Clone('herr')
            herr.Reset()
            hframe.SetAxisRange(1.0, hstack.GetMaximum()*1e4 if vartitle[hist][2] == 1 else hstack.GetMaximum()*1.8,"Y");
#            hframe.SetMinimum(0.1)
#            hframe.SetMaximum( hstack.GetMaximum()*1e4 if vartitle[hist][2] == 1 else hstack.GetMaximum()*1.5)
            xAxis = hframe.GetXaxis()
            xAxis.SetNdivisions(6,5,0)


            yAxis = hframe.GetYaxis()
            yAxis.SetNdivisions(6,5,0)
            yAxis.SetTitleOffset(0.9)
            yAxis.SetMaxDigits(3)
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
            if plotData:
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
            for key in plotCosmetics:
                if key == 'data':continue
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
                c.SaveAs(destination+"/"+cut[nwhichcut]+"/"+hist+shortcats[ncat]+".pdf")

        rt.gDirectory.GetList().Delete()
        if len(treeplots)==1:FormatTable(table)
