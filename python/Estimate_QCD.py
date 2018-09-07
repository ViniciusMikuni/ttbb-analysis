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

def Calculate_qwfrac(tree,weight='',proc='',cut='qgLR > 0.87'):
    wnom = weight.replace('qgweight*','')
    tree.Draw('qgLR>>hnom'+proc,wnom+'*'+cut)
    n_nom =rt.gDirectory.Get('qgLR>>hnom'+proc).Integral()
    tree.Draw('qgLR>>hwe'+proc,weight+'*'+cut)
    n_qglr =rt.gDirectory.Get('qgLR>>hwe'+proc).Integral()
    qg_fac = float(n_nom)/n_qglr if n_qglr >0 else 1.0
    print  proc,':',qg_fac
    return qg_fac

def Estimate_QCD(sys = '',sysname='',direction='',weight='',bkgs_=[],trees={},saveplots = True,is_overflow = True,verbose = False,fout='QCD_Estimate_0.root'):
    control_var=['n_bjets']
    # control_var = ['lp1_eta','lp2_eta','lq1_eta','lq2_eta','b1_eta','b2_eta',
    # 'top1_m','top2_m','w1_m','w2_m','deltaRp1p2','deltaRq1q2',
    # 'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]',
    # 'deltaRb1b2','deltaRb1w1','deltaRb2w2','deltaPhiw1w2','deltaPhit1t2','p1b1_mass','q1b2_mass','deltaRb1w2','deltaRb2w1',
    # 'mindeltaRb1p','simple_chi2','mindeltaRb2q', 'deltaEtap1p2', 'deltaEtaq1q2','jet_CSV[0]','jet_CSV[1]','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]',
    # 'jet_CSV[5]'] #Other variables to plot with
#'top1_m','top2_m','w1_m','w2_m','deltaRb1b2','btagLR4b',
#'addJet_CSV[0]','addJet_CSV[1]','ht',
#'addJet_CSV[0]','addJet_CSV[1]','ht','b1_pt','top1_m','top2_m','w1_m','w2_m','deltaRb1b2',
    #control_var = []
    #'addJet_eta[0]','addJet_pt[0]','addJet_pt[1]','addJet_eta[1]','addJet_deltaR','addJet_deltaPhi','addJet_deltaEta','addJet_mass'
    plot_control = False
    plot_data = True
    interest_var = [sys]
    if plot_control:
        interest_var+=control_var
        print interest_var
    #cut = 'BDT_Comb> 0.96864'
    #addcut = '(n_jets>=8 && BDT_Comb>0.808274 && BDT_CWoLa > -0.0302476 )'
    #addcut = '(n_jets>=8 && simple_chi2<38.0848 && BDT_Comb >0.834643 )'
    #addcut = '(n_jets>=8 && simple_chi2<34.4046 && BDT_Comb > 0.102203)'
    #addcut = '(n_jets>=8 && simple_chi2<34.4046 && BDT_Comb > 0.102203)'




    fout =  rt.TFile(fout,"UPDATE")
    xdist = -0.35

    # regcuts = [
    #     ['BDT_Comb', '0.829416',0],
    #     ['BDT_CWoLa','0.404494',0]
    #     ]
#####################################################
    # add_cut = '(n_jets>=8  && BDT_CWoLa > 0.3234 && BDT_Comb > -0.971857)' #TMVA 20%
    # regcuts = [
    #     ['simple_chi2', '9.4301',1],
    #     ['qgLR','0.636581',0]
    # ]

    # add_cut = '(n_jets>=8  && BDT_CWoLa > 0.180626)' #TMVA 30% reduced
    # regcuts = [
    #     ['BDT_Comb', '0.857525',0],
    #     ['qgLR','0.378745',0]
    # ]

    # add_cut = '(n_jets>=8 )' #TMVA 20% without BDT_Comb
    # regcuts = [
    #     ['BDT_CWoLa', '0.409077',0],
    #     ['qgLR','0.62846',0]
    # ]

    # add_cut = '(n_jets>=8  && BDT_CWoLa > 0.206721 &&  simple_chi2<19.7491 )' #TMVA 30% No btagLR
    # regcuts = [
    #     ['BDT_Comb', '0.664107',0],
    #     ['qgLR','0.444917',0]
    # ]

    # add_cut = '(n_jets>=8 &&  BDT_CWoLa > 0.335974 && simple_chi2<38.8797)' #TMVA 20% no btagLR

    # regcuts = [
    #     ['BDT_Comb','-0.661968',0],
    #     ['qgLR','0.35119',0]
    # ]

    #add_cut = '(jet_CSV[0]>=0.9535||jet_CSV[1]>=0.9535)' #RGS
    cutvars = {
        'BDT_CWoLa':'BDT_CWoLa'+sysname+direction,
        'qgLR':'qgLR'+sysname+direction,
        'prob_chi2':'prob_chi2'+sysname+direction,
    }
    add_cut = 'n_jets>7 && {0}>6e-2 && {1}>0 && {2}>=-1 && {2}!=0'.format(cutvars['prob_chi2'],cutvars['qgLR'],cutvars['BDT_CWoLa'] ) #RGS
    add_cutnom = 'n_jets>7 && prob_chi2>6e-2'

    regcuts = [
        [cutvars['BDT_CWoLa'],'0.5',0],
        [cutvars['qgLR'],'0.6',1]
    ]
    regcutsnom = [
        ['BDT_CWoLa','0.5',0],
        ['qgLR','0.6',1]
    ]


#####################################################

    #0.2 eff
    # regcuts = [
    #     ['BDT_CWoLa', '0.3234',0],
    #     ['qgLR','0.636581',0]
    # ]

    # regcuts = [
    #     ['BDT_Comb', '0.102203',0],
    #     ['qgLR','0.722416',0]
    #     ]

    regions = OrderedDict()
    regionsnom = OrderedDict()



    # regions["CR1"]={'cut':'(jet_CSV[0]<0.9535||jet_CSV[1]<0.9535 && (jet_CSV[0]>=0.8484 && jet_CSV[1]>=0.8484))','data':None,'bkg':None,'QCD':None}
    # regions["CR2"]={'cut':'((jet_CSV[0]<0.8484 || jet_CSV[1]<0.8484) && qgLR<0.722416)','data':None,'bkg':None,'QCD':None}
    # regions["VR"]={'cut':'((jet_CSV[0]<0.8484 || jet_CSV[1]<0.8484) && qgLR>0.722416)','data':None,'bkg':None,'QCD':None}
    # regions["SR"]={'cut':'(jet_CSV[0]>=0.9535 && jet_CSV[1]>=0.9535 )','data':None,'bkg':None,'QCD':None}





    regions["CR1"] = {'cut':'('+ regcuts[0][0] + ('<' if regcuts[0][2] else '>') +  regcuts[0][1] + '&&' + regcuts[1][0] + ('>' if regcuts[1][2] else '<') +  regcuts[1][1] + ')','data':None,'bkg':None,'QCD':None}
    regions["CR2"] ={'cut':'('+ regcuts[0][0] + ('>' if regcuts[0][2] else '<') +  regcuts[0][1] + '&&' + regcuts[1][0] + ('>' if regcuts[1][2] else '<') +  regcuts[1][1] + ')','data':None,'bkg':None,'QCD':None}
    regions["VR"] ={'cut':'('+ regcuts[0][0] + ('>' if regcuts[0][2] else '<') +  regcuts[0][1] + '&&' + regcuts[1][0] + ('<' if regcuts[1][2] else '>') +  regcuts[1][1] + ')','data':None,'bkg':None,'QCD':None}
    regions["SR"] ={'cut':'('+ regcuts[0][0] + ('<' if regcuts[0][2] else '>') +  regcuts[0][1] + '&&' + regcuts[1][0] + ('<' if regcuts[1][2] else '>') +  regcuts[1][1] + ')','data':None,'bkg':None,'QCD':None}

    regionsnom["CR1"] = {'cut':'('+ regcutsnom[0][0] + ('<' if regcutsnom[0][2] else '>') +  regcutsnom[0][1] + '&&' + regcutsnom[1][0] + ('>' if regcutsnom[1][2] else '<') +  regcutsnom[1][1] + ')','data':None,'bkg':None,'QCD':None}
    regionsnom["CR2"] ={'cut':'('+ regcutsnom[0][0] + ('>' if regcutsnom[0][2] else '<') +  regcutsnom[0][1] + '&&' + regcutsnom[1][0] + ('>' if regcutsnom[1][2] else '<') +  regcutsnom[1][1] + ')','data':None,'bkg':None,'QCD':None}
    regionsnom["VR"] ={'cut':'('+ regcutsnom[0][0] + ('>' if regcutsnom[0][2] else '<') +  regcutsnom[0][1] + '&&' + regcutsnom[1][0] + ('<' if regcutsnom[1][2] else '>') +  regcutsnom[1][1] + ')','data':None,'bkg':None,'QCD':None}
    regionsnom["SR"] ={'cut':'('+ regcutsnom[0][0] + ('<' if regcutsnom[0][2] else '>') +  regcutsnom[0][1] + '&&' + regcutsnom[1][0] + ('<' if regcutsnom[1][2] else '>') +  regcutsnom[1][1] + ')','data':None,'bkg':None,'QCD':None}

    # add_cut = '(n_jets>=8 )' #TMVA 20%
    # regions["CR1"] = {'cut':'(simple_chi2<38.8797 && BDT_CWoLa > 0.335974 && BDT_Comb > -0.661968 && qgLR < 0.35119)','data':None,'bkg':None,'QCD':None}
    # regions["CR2"] ={'cut':'(simple_chi2<38.8797 && BDT_Comb < -0.661968 && qgLR < 0.35119)','data':None,'bkg':None,'QCD':None}
    # regions["VR"] ={'cut':'(simple_chi2<38.8797 &&  BDT_Comb < -0.661968 && qgLR > 0.35119)','data':None,'bkg':None,'QCD':None}
    # regions["SR"] ={'cut':'(simple_chi2<38.8797 && BDT_CWoLa > 0.335974 && BDT_Comb > -0.661968 && qgLR > 0.35119)','data':None,'bkg':None,'QCD':None}

    # regions["CR1"] = {'cut':'(BDT_CWoLa > 0.402506 && BDT_Comb > -0.540412 && qgLR < 0.685603)','data':None,'bkg':None,'QCD':None}
    # regions["CR2"] ={'cut':'(BDT_Comb < -0.540412 && qgLR < 0.685603)','data':None,'bkg':None,'QCD':None}
    # regions["VR"] ={'cut':'(BDT_Comb < -0.540412 && qgLR > 0.685603)','data':None,'bkg':None,'QCD':None}
    # regions["SR"] ={'cut':'(BDT_CWoLa > 0.402506 && BDT_Comb > -0.540412 && qgLR > 0.685603)','data':None,'bkg':None,'QCD':None}



    print 'Doing QCD Estimate'
    for reg in regions:
        print reg, regions[reg]['cut']


    # r = {
    #     "CR1":{'cut':'(BDT_Comb> 0.829416 && BDT_CWoLa<0.404494 && BDT_CWoLa>0.304494)','data':None,'bkg':None,'QCD':None},
    #     "CR2":{'cut':'(BDT_Comb< 0.829416 && BDT_Comb > 0.729416 && BDT_CWoLa<0.404494)','data':None,'bkg':None,'QCD':None},
    #     "VR":{'cut':'(BDT_Comb< 0.829416  && BDT_Comb > 0.729416 && BDT_CWoLa>0.404494 && BDT_CWoLa>0.304494)','data':None,'bkg':None,'QCD':None},
    #     "SR":{'cut':'(BDT_Comb> 0.829416 && BDT_CWoLa>0.404494)','data':None,'bkg':None,'QCD':None}
    # }



    # r = {
    #     "CR1":{'cut':'(qgLR>0.5 && BDT_CWoLa<0.170504 )','data':None,'bkg':None,'QCD':None},
    #     "CR2":{'cut':'(qgLR<0.5 && BDT_CWoLa<0.170504 )','data':None,'bkg':None,'QCD':None},
    #     "VR":{'cut':'(qgLR<0.5 && BDT_CWoLa>0.170504)','data':None,'bkg':None,'QCD':None},
    #     "SR":{'cut':'(qgLR>0.5 && BDT_CWoLa>0.170504)','data':None,'bkg':None,'QCD':None}
    # }



    t_data = trees['data']

    scaleSR=scaleVR=0
    nregs = {'CR1':0,'CR2':0,'VR':0,'SR':0}
    for ivar, var in enumerate(interest_var):
        rt.gDirectory.GetList().Delete()
        if var in control_var:
            varname = var
        else:
            varname = var.partition('_')[0]
        for reg in regions:

            if verbose: print 'doing ',reg, 'scaleVR = ',scaleVR

            t_data.Draw(varname + '>>'+ 'hdata'+reg+varname+ str(vartitle[varname][1]),"("+add_cutnom+")*"+regionsnom[reg]['cut'])

            hdata = rt.gDirectory.Get('hdata'+reg+varname).Clone('data'+reg+varname)
            if is_overflow: AddOverflow(hdata)
            nregs[reg]+=t_data.Draw("",regionsnom[reg]['cut'])
            if verbose: print var.partition('_')[0] + '>>'+ 'hdata'+reg+ str(vartitle[varname][1]), "("+add_cutnom+")*"+regions[reg]['cut']
            hdata.Sumw2()

            hbkg = hdata.Clone('bkg'+reg)
            hbkg.Reset()
            hbkg.Sumw2()
            for process in bkgs_:
                print process
                if process in processgroup:
                    for subprocess in processgroup[process]:
                        trees[subprocess].Draw(var + '>>'+ 'h'+reg+subprocess+ str(vartitle[varname][1]),weight+"*("+add_cut+")&&"+regions[reg]['cut'])
                        h = rt.gDirectory.Get('h'+reg+subprocess).Clone('h'+reg+subprocess+var)
                        if h.Integral()<0: print process
                        if is_overflow: AddOverflow(h)
                        h.Scale(dscale[subprocess])
                        nregs[reg]+= - trees[subprocess].Draw('',regions[reg]['cut'])*dscale[subprocess]
                        #if reg in ['SR','VR']:h.Scale(qwfac[subprocess])
                        if verbose: print 'subprocess: ',var + '>>'+ 'h'+reg+subprocess+ str(vartitle[varname][1]),weight+"*("+add_cut+")&&"+regions[reg]['cut']
                        #print type(hbkg),type(h)
                        hbkg.Add(h)

                elif process == 'ttbar':
                    for tproc in ttplot:
                        trees[tproc].Draw(var + '>>'+ 'h'+reg+tproc+var+ str(vartitle[varname][1]),weight+"*topweight*("+add_cut+")&&("+ttCls[tproc]+")*"+regions[reg]['cut'])
                        nregs[reg]+= -trees[tproc].Draw('',regions[reg]['cut'])*dscale['ttbar']
                        if verbose: print 'ttbar options: ',var + '>>'+ 'h'+reg+tproc+var+ str(vartitle[varname][1]),weight+"*topweight*("+add_cut+")&&"+ttCls[tproc]+"*"+regions[reg]['cut']
                        h = rt.gDirectory.Get('h'+reg+tproc+var).Clone('h'+reg+tproc+var)
                        if is_overflow: AddOverflow(h)
                        if verbose: print 'tproc before: ',tproc,' ntproc:', h.Integral()
                        h.Scale(dscale['ttbar'])
                        #if reg in ['SR','VR']:h.Scale(qwfac[tproc])
                        if verbose: print 'tproc: ',tproc,' ntproc:', h.Integral()
                        hbkg.Add(h)


                else:
                    trees[process].Draw(var + '>>'+ 'h'+reg+process+ str(vartitle[varname][1]),weight+"*("+add_cut+")*"+regions[reg]['cut'])
                    nregs[reg]+= -trees[process].Draw('',regions[reg]['cut'])*dscale[process]
                    h = rt.gDirectory.Get('h'+reg+process).Clone('h'+reg+process+var)
                    if is_overflow: AddOverflow(h)
                    h.Scale(dscale[process])
                    #if reg in ['SR','VR']:h.Scale(qwfac[process])
                    if h.Integral()<0: print process
                    if verbose: print 'before: ', hbkg.Integral()
                    if verbose: print 'process ',process,' integral: ', h.Integral()
                    hbkg.Add(h)
                    if verbose:print 'after: ', hbkg.Integral()



            hres = hdata.Clone("hbkgsub"+reg)
            if verbose:print 'Data evts: ',hdata.Integral()
            if verbose:print 'background evts: ', hbkg.Integral()
            hres.Add(hbkg,-1)
            regions[reg]['QCD'] = hres
            if verbose:print 'QCD estimate ',hres.Integral()
            regions[reg]['bkg'] = hbkg
            regions[reg]['data']= hdata.Clone('Data'+reg)

            if "CR" not in reg:
                if reg == 'SR':
                    if regions['CR1']['QCD'] == None:
                        print 'Do CRs first!'
                        continue
                    elif scaleVR == 0:
                        print 'Do VR first!'
                        continue
                    else:

                        if ivar == 0:
                            nqcd = regions['CR1']['QCD'].Integral()
                            scaleSR = hres.Integral()/nqcd
                            # nqcd = regions['CR1']['QCD'].GetBinContent(1)
                            # scaleSR = hres.GetBinContent(1)/nqcd
                            #scaleSR = scaleVR
                        print 'scale SR: ',scaleSR, 'nqcd CR1: ',nqcd

                        hSR = regions['CR1']['QCD'].Clone('QCD'+reg+var)
                        hSR.Scale(scaleSR)
                        regions[reg]['QCD'] = hSR
                if reg == 'VR':
                    if regions['CR2']['QCD'] == None:
                        print 'Do CRs first!'
                        continue

                    else:
                        if ivar == 0:
                            nqcd = regions['CR2']['QCD'].Integral()
                            scaleVR = hres.Integral()/nqcd
                            # nqcd = regions['CR2']['QCD'].GetBinContent(1)
                            # scaleVR = hres.GetBinContent(1)/nqcd
                            print 'scale VR: ',scaleVR, 'nqcd CR2: ',nqcd
                        hSR = regions['CR2']['QCD'].Clone('QCD'+reg+var)
                        hSR.Scale(scaleVR)
                        regions[reg]['QCD'] = hSR


        if plot_control:
            for reg in regions:
                colors = {'ttbar':['#2c7fb8','t#bar{t} + Minor Bkgs.'],'Multijet':['#31a354','Multijet']}
                if plot_data:
                    regions[reg]['data'].SetMarkerColor(1)
                    regions[reg]['data'].SetMarkerStyle(20)
                    regions[reg]['data'].SetMarkerSize(1.0)
                regions[reg]['bkg'].SetFillColor(rt.TColor.GetColor(colors['ttbar'][0]))
                regions[reg]['QCD'].SetFillColor(rt.TColor.GetColor(colors['Multijet'][0]))
                hstack =  rt.THStack(vartitle[varname][0]+reg,vartitle[varname][0]+reg)
                hstack.Add(regions[reg]['bkg'])
                hstack.Add(regions[reg]['QCD'])

                c = rt.TCanvas(var+reg+weight,var+reg+weight,5,30,W_ref,H_ref)
                pad1 = rt.TPad("pad1", "pad1", 0.0, 0.15 if plot_data else 0.0, 1, 1.0)
                pad1.Draw()
                pad1.cd()
                SetupCanvas(pad1, vartitle[varname][2])

                hframe = rt.TH1F(var+reg,"h; {0}; Events ".format(vartitle[varname][0]),vartitle[varname][1][0],vartitle[varname][1][1],vartitle[varname][1][2])
                hframe.SetAxisRange(0.1, regions[reg]['data'].GetMaximum()*1e4 if vartitle[varname][2] == 1 else regions[reg]['data'].GetMaximum()*1.8,"Y")
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
                if plot_data:regions[reg]['data'].Draw("esamex0")
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

                if plot_data:
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
                if plot_data:
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
                if plot_data:
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

                    hratio.GetYaxis().SetRangeUser(0.5,1.5)

                    hratio.SetTitle("")

                    hratio.GetXaxis().SetTitle(vartitle[varname][0])
                    hratio.GetXaxis().SetTitleSize(0.156)
                    hratio.GetXaxis().SetLabelSize(0.171)
                    #hratio.GetXaxis().SetTickLength(0.09)


                    #for b in range(hratio.GetNbinsX()):
                    #    hratio.GetXaxis().SetBinLabel(b+1, str(int(hratio.GetBinLowEdge(b+1))) )

                    hratio.GetXaxis().SetLabelOffset(0.02)

                    hratio.GetYaxis().SetTitleSize(0.196)
                    hratio.GetYaxis().SetLabelSize(0.171)
                    hratio.GetYaxis().SetTitleOffset(0.30)
                    hratio.GetYaxis().SetTitle("      Data/MC")
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
                    if not os.path.exists(destination+"/QCD Estimation"):
                        os.makedirs(destination+"/QCD Estimation")
                    else:
                        print "WARNING: directory already exists. Will overwrite existing files..."
                        c.SaveAs(destination+"/QCD Estimation/"+reg+var+".png")





        fout.cd()
        for reg in regions:
            regions[reg]['data'].Write()
            regions[reg]['bkg'].Write()
            regions[reg]['QCD'].Write()
            if verbose:
                print regions[reg]['data'].GetName()
                print regions[reg]['bkg'].GetName()
                print regions[reg]['QCD'].GetName()

    fout.Close()
    #rt.gDirectory.GetList().Delete()
