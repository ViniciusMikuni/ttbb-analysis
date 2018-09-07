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
import re
import ast
from collections import OrderedDict
from Plotting_cfg import *
import CMS_lumi
#rt.gROOT.LoadMacro("../src/triggerWeightRound.h+")
tdrstyle.setTDRStyle()
rt.TH1.SetDefaultSumw2()
def Set_Zero(h):
    for bin in range(h.GetSize()-2):
        if h.GetBinContent(bin+1)<0:h.SetBinContent(bin+1,1e-10)

def Calculate_qwfrac(tree,weight='',proc='',cut='qgLR > 0.87'):
    wnom = weight.replace('qgweight*','')
    #print 'qgLR>>hnom'+proc,wnom+'*'+cut
    #print 'qgLR>>hwe'+proc,weight+'*'+cut
    tree.Draw('qgLR>>hnom'+proc,wnom)
    n_nom =rt.gDirectory.Get('hnom'+proc).Integral()
    tree.Draw('qgLR>>hwe'+proc,weight)
    n_qglr =rt.gDirectory.Get('hwe'+proc).Integral()
    print proc
    #print 'nom: ',wnom
    #print 'we :',  weight
    qg_fac = float(n_nom)/n_qglr if n_qglr >0 else 1.0
    print  proc,':',qg_fac
    return qg_fac

def Estimate_QCD(config,sysname='',direction='',is_weight=False,processlist=[],trees={},is_overflow = True):
    fname = config.get('GENERAL','hfile')
    verbose = config.getboolean('GENERAL','verbose')
    calc_qwfac=config.getboolean('GENERAL','calc_qwfac')
    apply_qwfac=config.getboolean('GENERAL','apply_qwfac')
    setQCD0error=config.getboolean('GENERAL','setQCD0error')
    weight = config.get('GENERAL','weight')
    test_nominal = config.getboolean('GENERAL','test_nominal')
    use_bin_opt = config.getboolean('GENERAL','use_bin_opt')
    interest_var=ast.literal_eval(config.get('GENERAL','var'))
    hname = OrderedDict(sorted(dnames.items(), key=lambda t: t[0]))
    bkgs_ = list(filter(lambda x: x not in ['QCD','data'], processlist))
    hvar = []
    hlist = []
    #CR_add_cut = '(top1_m < 150 ||top1_m > 200)'
    SR_add_cut = '(1==1)'
    CR_add_cut = '(1==1)'
    if 'shape' in sysname:
        is_shape=True
        shapelist=ast.literal_eval(config.get('SYSTEMATICS','shapelist'))
    else: is_shape=False
    if 'lN' in sysname:
        is_lN=True
        lNlist=ast.literal_eval(config.get('SYSTEMATICS','lNlist'))
    else:is_lN=False
    if is_weight:
        print 'is_weight'
        weight_name = sysname[1:].partition('_')[0] #btagweight
        if 'top' not in weight_name and 'LHE' not in weight_name:
            weight = weight.replace(weight_name,sysname[1:]+'_'+direction)
            topweight=weight+'*topweight'
            #+'*topweight'
        else:
            print 'LHE or top'
            if 'top' in weight_name:
                topweight=weight+'*topweight_'+direction
            else:
                topweight=weight+'*topweight*{0}_{1}*{2}'.format(sysname[1:],direction,LHE_fac[sysname+'_'+direction])
                print topweight
                print '*'*80


    else:topweight=weight+'*topweight'
    #+'*topweight'

    if verbose: print 'weight: ', weight

    interest_var=ast.literal_eval(config.get('GENERAL','var'))
    control_var=ast.literal_eval(config.get('QCD_ESTIMATION','control_vars'))
    plot_control = config.getboolean('QCD_ESTIMATION','plot_control')
    qcd_first = config.getboolean('QCD_ESTIMATION','qcd_first')
    plot_data = config.getboolean('QCD_ESTIMATION','plot_data')
    save_plots = config.getboolean('QCD_ESTIMATION','save_plots')

    if plot_control:
        interest_var+=control_var
        print interest_var, 'interest_vars'


    fout =  rt.TFile(fname,"UPDATE")
    xdist = -0.35
    add_cut=''
    regcuts = []
    add_cut_nom=''
    regcutsnom = []
    for item, cut in config.items('CUT'):
        if item not in ast.literal_eval(config.get('QCD_ESTIMATION','CR_vars')):
            add_cut+=item+sysname+direction+cut+'&&'
            add_cut_nom+=item+cut+'&&'
        else:
            if 'qgLR' not in item:
                add_cut+=item+sysname+direction+'>=-1&&'
                add_cut_nom+=item+'>=-1&&'
            else:
                add_cut+=item+sysname+direction+'>0&&'
                add_cut_nom+=item+'>0&&'
            if '>'in cut or '>=' in cut:SRdir = 0
            else:SRdir=1
            regcuts.append(
                [item+sysname+direction,
                 [s for s in re.findall(r'-?\d+\.?\d*', cut)][0],
                 SRdir
                ]
            )
            regcutsnom.append(
                [item,
                 [s for s in re.findall(r'-?\d+\.?\d*', cut)][0],
                 SRdir
                ]
            )


    add_cut_nom=add_cut_nom[:-2] #Remove last &&
    add_cut=add_cut[:-2] #Remove last &&

    if verbose:
        print add_cut, add_cut_nom, 'cuts for qcd est'
        print regcuts, regcutsnom, 'regcuts'
    #print 'other cuts: ',add_cut


    regions = OrderedDict()
    regionsnom = OrderedDict()



    # regions["CR1"]={'cut':'(jet_CSV[0]<0.9535||jet_CSV[1]<0.9535 && (jet_CSV[0]>=0.8484 && jet_CSV[1]>=0.8484))','data':None,'bkg':None,'QCD':None}
    # regions["CR2"]={'cut':'((jet_CSV[0]<0.8484 || jet_CSV[1]<0.8484) && qgLR<0.722416)','data':None,'bkg':None,'QCD':None}
    # regions["VR"]={'cut':'((jet_CSV[0]<0.8484 || jet_CSV[1]<0.8484) && qgLR>0.722416)','data':None,'bkg':None,'QCD':None}
    # regions["SR"]={'cut':'(jet_CSV[0]>=0.9535 && jet_CSV[1]>=0.9535 )','data':None,'bkg':None,'QCD':None}





    regions["CR1"] = {'cut':'('+ regcuts[0][0] + ('<' if regcuts[0][2] else '>') +  regcuts[0][1] + '&&' + regcuts[1][0] + ('>' if regcuts[1][2] else '<') +  regcuts[1][1] + ')'+ '&&' + CR_add_cut ,'data':None,'bkg':None,'QCD':None}
    regions["CR2"] ={'cut':'('+ regcuts[0][0] + ('>' if regcuts[0][2] else '<') +  regcuts[0][1] + '&&' + regcuts[1][0] + ('>' if regcuts[1][2] else '<') +  regcuts[1][1] + ')'+ '&&' + CR_add_cut,'data':None,'bkg':None,'QCD':None}
    regions["VR"] ={'cut':'('+ regcuts[0][0] + ('>' if regcuts[0][2] else '<') +  regcuts[0][1] + '&&' + regcuts[1][0] + ('<' if regcuts[1][2] else '>') +  regcuts[1][1] + ')'+ '&&' + SR_add_cut,'data':None,'bkg':None,'QCD':None}
    regions["SR"] ={'cut':'('+ regcuts[0][0] + ('<' if regcuts[0][2] else '>') +  regcuts[0][1] + '&&' + regcuts[1][0] + ('<' if regcuts[1][2] else '>') +  regcuts[1][1] + ')'+ '&&' + SR_add_cut,'data':None,'bkg':None,'QCD':None}

    regionsnom["CR1"] = {'cut':'('+ regcutsnom[0][0] + ('<' if regcutsnom[0][2] else '>') +  regcutsnom[0][1] + '&&' + regcutsnom[1][0] + ('>' if regcutsnom[1][2] else '<') +  regcutsnom[1][1] +')'+ '&&' + CR_add_cut  ,'data':None,'bkg':None,'QCD':None}
    regionsnom["CR2"] ={'cut':'('+ regcutsnom[0][0] + ('>' if regcutsnom[0][2] else '<') +  regcutsnom[0][1] + '&&' + regcutsnom[1][0] + ('>' if regcutsnom[1][2] else '<') +  regcutsnom[1][1] + ')'+ '&&' + CR_add_cut ,'data':None,'bkg':None,'QCD':None}
    regionsnom["VR"] ={'cut':'('+ regcutsnom[0][0] + ('>' if regcutsnom[0][2] else '<') +  regcutsnom[0][1] + '&&' + regcutsnom[1][0] + ('<' if regcutsnom[1][2] else '>') +  regcutsnom[1][1] + ')'+ '&&' + SR_add_cut,'data':None,'bkg':None,'QCD':None}
    regionsnom["SR"] ={'cut':'('+ regcutsnom[0][0] + ('<' if regcutsnom[0][2] else '>') +  regcutsnom[0][1] + '&&' + regcutsnom[1][0] + ('<' if regcutsnom[1][2] else '>') +  regcutsnom[1][1] + ')'+ '&&' + SR_add_cut,'data':None,'bkg':None,'QCD':None}


    if is_weight or test_nominal or is_lN or is_shape:
        regions = regionsnom
        add_cut = add_cut_nom

    print 'Doing QCD Estimate'
    for reg in regions:
        print reg, regions[reg]['cut']



    t_data = trees['data']

    scaleSR=scaleVR=0

    for ivar, var in enumerate(interest_var):
        rt.gDirectory.GetList().Delete()
        varnom=var
        if is_weight == False and sysname != '' and is_lN==False and is_shape == False:
            var+=sysname+direction
        for proc in hname:
            if sysname != '':
                if is_weight:
                    if 'btag' in sysname: nuis_name = sysname.replace('btagweight','CMS_btag')+direction
                    else: nuis_name = '_CMS'+sysname.replace('weight','_Weight')+direction
                elif is_lN:
                    nuis_name = sysname.replace('lN','')
                elif is_shape:
                    nuis_name = sysname.replace('shape','')
                else:nuis_name='_CMS'+sysname+'_j'+direction
            else:nuis_name=sysname+direction
        #print nuis_name
        #print is_lN
        for reg in regions:
            if verbose: print reg
            if not fout.GetDirectory(reg):
                fout.mkdir(reg)
            fout.cd(reg)

            if verbose: print 'doing ',reg, 'scaleVR = ',scaleVR
            if use_bin_opt:
                hopt=rt.TH1F('hdata'+reg+varnom+sysname,'hdata'+reg+varnom+sysname,len(opt_bin)-1,opt_bin)
                t_data.Draw(varnom + '>>'+ 'hdata'+reg+varnom+sysname,"("+add_cut_nom+")*"+regionsnom[reg]['cut'])

                hdata=hopt.Clone('data_obs')
            else:
                t_data.Draw(varnom + '>>'+ 'hdata'+reg+varnom+sysname+ str(vartitle[varnom][1]),"("+add_cut_nom+")*"+regionsnom[reg]['cut'])
                print varnom + '>>'+ 'hdata'+reg+varnom+sysname+ str(vartitle[varnom][1]),"("+add_cut_nom+")*"+regionsnom[reg]['cut']
                #print reg, varnom + '>>'+ 'hdata'+reg+varnom+sysname+ str(vartitle[varnom][1]),"("+add_cut_nom+")*"+regionsnom[reg]['cut']
                #print 'data: ',"("+add_cut_nom+")*"+regionsnom[reg]['cut']
                hdata = rt.gDirectory.Get('hdata'+reg+varnom+sysname).Clone('data_obs')

            if is_overflow: AddOverflow(hdata)
            if sysname == '':hdata.Write()

            if verbose: print var.partition('_')[0] + '>>'+ 'hdata'+reg+ str(vartitle[varnom][1]), "("+add_cut_nom+")*"+regions[reg]['cut']
            hdata.Sumw2()

            hbkg = hdata.Clone('bkg'+reg)
            hbkg.Reset()
            for process in bkgs_:
                #print process
                if process in processgroup and process != 'QCD':
                    for isub, subprocess in enumerate(processgroup[process]):
                        #print subprocess
                        if use_bin_opt:
                            hopt=rt.TH1F('h'+reg+subprocess+sysname,'h'+reg+subprocess+sysname,len(opt_bin)-1,opt_bin)
                            trees[subprocess].Draw(var + '>>'+ 'h'+reg+subprocess+sysname ,weight+"*("+add_cut+"&&"+regions[reg]['cut']+')')
                        else:
                            trees[subprocess].Draw(var + '>>'+ 'h'+reg+subprocess+sysname+ str(vartitle[varnom][1]),weight+"*("+add_cut+"&&"+regions[reg]['cut']+')')

                        if isub == 0:
                            if use_bin_opt:
                                h=hopt.Clone(hname[process]+nuis_name)
                            else:
                                h = rt.gDirectory.Get('h'+reg+subprocess+sysname).Clone(hname[process]+nuis_name)

                            if calc_qwfac and (reg=='SR'): Calculate_qwfrac(trees[subprocess],weight+"*("+add_cut+')',subprocess)
                            if is_overflow: AddOverflow(h)
                            h.Sumw2()
                            h.Scale(dscale[subprocess])
                            if apply_qwfac:h.Scale(qwfac[subprocess])
                            # if calc_qwfac:Calculate_qwfrac(tree[subprocess],weight,subprocess)
                            # else: h.Scale(qwfac[subprocess])
                        else:
                            if use_bin_opt:
                                hsub=hopt.Clone(hname[process]+nuis_name)
                            else:
                                hsub = rt.gDirectory.Get('h'+reg+subprocess+sysname).Clone(hname[process]+nuis_name)

                            if calc_qwfac and (reg=='SR'): Calculate_qwfrac(trees[subprocess],weight+"*("+add_cut+')',subprocess)
                            if is_overflow: AddOverflow(hsub)
                            # if calc_qwfac:Calculate_qwfrac(tree[subprocess],weight,subprocess)
                            # else:h.Scale(qwfac[subprocess])
                            hsub.Sumw2()
                            hsub.Scale(dscale[subprocess])
                            if apply_qwfac:hsub.Scale(qwfac[subprocess])
                            h.Add(hsub)
                        if verbose: print 'subprocess: ',var + '>>'+ 'h'+reg+subprocess+ str(vartitle[varnom][1]),weight+"*("+add_cut+"&&"+regions[reg]['cut']+')'
                        #print type(hbkg),type(h)
                    if is_lN:
                        #print nuis_name[1:]
                        #print dnames[process]
                        if lNlist[dnames[process]].has_key(nuis_name[1:]):
                            if direction == 'Up':
                                h.Scale(lNlist[dnames[process]][nuis_name[1:]][0])
                                h.SetName(h.GetName()+direction)
                            elif direction == 'Down':
                                h.Scale(lNlist[dnames[process]][nuis_name[1:]][1])
                                h.SetName(h.GetName()+direction)
                            else: print 'wtf mate'
                    hbkg.Add(h)
                    if direction in h.GetName() or sysname=='':
                        #print h.GetName()
                        #print reg
                        h.Write()

                elif 'ttbar' in process:
                    for tproc in ttCls:
                        if use_bin_opt:
                            hopt=rt.TH1F('h'+reg+tproc+var+sysname,'h'+reg+tproc+var+sysname,len(opt_bin)-1,opt_bin)
                            trees[tproc].Draw(var + '>>'+ 'h'+reg+tproc+var+sysname ,topweight+"*("+add_cut+"&&"+ttCls[tproc]+"&&"+regions[reg]['cut']+')')
                        else:
                            trees[tproc].Draw(var + '>>'+ 'h'+reg+tproc+var+sysname+ str(vartitle[varnom][1]),topweight+"*("+add_cut+"&&"+ttCls[tproc]+"&&"+regions[reg]['cut']+')')
                            print var + '>>'+ 'h'+reg+tproc+var+sysname+ str(vartitle[varnom][1]),topweight+"*("+add_cut+"&&"+ttCls[tproc]+"&&"+regions[reg]['cut']+')'

                        #print var + '>>'+ 'h'+reg+tproc+var+sysname+ str(vartitle[varnom][1]),topweight+"*("+add_cut+"&&"+ttCls[tproc]+"&&"+regions[reg]['cut']+')'
                        if verbose: print 'ttbar options: ',var + '>>'+ 'h'+reg+tproc+var+sysname+ str(vartitle[varnom][1]),topweight+"*("+add_cut+"&&"+ttCls[tproc]+"&&"+regions[reg]['cut']+')'
                        if use_bin_opt:
                            h=hopt.Clone(hname[tproc]+nuis_name)
                        else:
                            h = rt.gDirectory.Get('h'+reg+tproc+var+sysname).Clone(hname[tproc]+nuis_name)
                        if calc_qwfac and (reg=='SR'):
                             Calculate_qwfrac(trees[tproc],topweight+"*("+add_cut+"&&"+ttCls[tproc]+')',tproc)
                        if is_overflow: AddOverflow(h)
                        #print h.Integral()
                        if verbose: print 'tproc before: ',tproc,' ntproc:', h.Integral()
                        h.Sumw2()
                        h.Scale(dscale[process])
                        if apply_qwfac:h.Scale(qwfac[tproc])
                        if is_lN:
                            if lNlist[tproc].has_key(nuis_name[1:]):
                                if direction == 'Up':
                                    h.Scale(lNlist[tproc][nuis_name[1:]][0])
                                    h.SetName(h.GetName()+direction)
                                elif direction == 'Down':
                                    h.Scale(lNlist[tproc][nuis_name[1:]][1])
                                    h.SetName(h.GetName()+direction)
                                else: print 'wtf mate'


                        #if not is_weight and direction == 'Up':
                            #h.SetBinContent(1,h.GetBinContent(1)*1.02)

                        #rint 'tproc: ',tproc,' ntproc:', h.Integral()
                        #if reg in ['SR','VR']:h.Scale(qwfac[tproc])
                        if verbose: print 'tproc: ',tproc,' ntproc:', h.Integral()
                        hbkg.Add(h)
                        if direction in h.GetName() or sysname=='':
                            h.Write()

                else:
                    if use_bin_opt:
                        hopt=rt.TH1F('h'+reg+process+sysname,'h'+reg+process+sysname,len(opt_bin)-1,opt_bin)
                        trees[process].Draw(var + '>>'+ 'h'+reg+process+sysname,weight+"*("+add_cut+"&&"+regions[reg]['cut']+')')
                        h=hopt.Clone(hname[process]+nuis_name)
                    else:
                        trees[process].Draw(var + '>>'+ 'h'+reg+process+sysname+ str(vartitle[varnom][1]),weight+"*("+add_cut+"&&"+regions[reg]['cut']+')')

                        h = rt.gDirectory.Get('h'+reg+process+sysname).Clone(hname[process]+nuis_name)
                    if calc_qwfac and (reg=='SR'):
                        Calculate_qwfrac(trees[process],weight+"*("+add_cut+')',process)
                    if is_overflow: AddOverflow(h)
                    h.Sumw2()
                    h.Scale(dscale[process])
                    if apply_qwfac:h.Scale(qwfac[process])
                    if is_lN:
                        if lNlist[dnames[process]].has_key(nuis_name[1:]):
                            if direction == 'Up':
                                h.Scale(lNlist[dnames[process]][nuis_name[1:]][0])
                                h.SetName(h.GetName()+direction)
                            elif direction == 'Down':
                                h.Scale(lNlist[dnames[process]][nuis_name[1:]][1])
                                h.SetName(h.GetName()+direction)
                            else: print 'wtf mate'
                    #if reg in ['SR','VR']:h.Scale(qwfac[process])
                    if h.Integral()<0: print process
                    if verbose: print 'before: ', hbkg.Integral()
                    if verbose: print 'process ',process,' integral: ', h.Integral()
                    hbkg.Add(h)
                    if verbose:print 'after: ', hbkg.Integral()
                    if direction in h.GetName() or sysname=='':
                        h.Write()




            hres = hdata.Clone("hbkgsub"+reg)
            print 'Data evts: ',hdata.Integral()
            print 'background evts without QCD: ', hbkg.Integral()
            hres.Add(hbkg,-1)
            #Set_Zero(hres)
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
                        print 'SR/CR1: ',scaleSR, 'nqcd CR1: ',nqcd

                        hSR = regions['CR1']['QCD'].Clone('QCD'+nuis_name)
                        hSR.Scale(scaleSR)
                        if is_shape: #hot fix for shape extrapolation uncertainty
                            correction = shapelist['QCD']['bkg_extrap']
                            if direction == 'Down':
                                correction = [2 - bin for bin in shapelist['QCD']['bkg_extrap']]
                            for bin, corr in enumerate(correction):
                                hSR.SetBinContent(bin+1,hSR.GetBinContent(bin+1)*corr)
                            hSR.SetName('QCD'+nuis_name+direction)

                        regions[reg]['QCD'] = hSR
                        if is_lN:hSR.SetName('QCD'+nuis_name+direction)
                        hSR.Write()

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
                            print 'VR/CR2: ',scaleVR, 'nqcd CR2: ',nqcd
                        hSR = regions['CR2']['QCD'].Clone('QCD'+nuis_name)
                        hSR.Scale(scaleVR)
                        regions[reg]['QCD'] = hSR
                        if is_lN:hSR.SetName('QCD'+nuis_name+direction)
                        hSR.Write()
            else:
                hres.SetName('QCD'+nuis_name)
                if is_lN:hres.SetName('QCD'+nuis_name+direction)
                hres.Write()
            fout.cd("../")

        if plot_control:
            for reg in regions:
                colors = {'ttbar':['#2c7fb8','t#bar{t} + Minor Bkgs.'],'Multijet':['#31a354','Multijet']}
                if plot_data:
                    regions[reg]['data'].SetMarkerColor(1)
                    regions[reg]['data'].SetMarkerStyle(20)
                    regions[reg]['data'].SetMarkerSize(1.0)
                regions[reg]['bkg'].SetFillColor(rt.TColor.GetColor(colors['ttbar'][0]))
                regions[reg]['QCD'].SetFillColor(rt.TColor.GetColor(colors['Multijet'][0]))
                hstack =  rt.THStack(vartitle[varnom][0]+reg,vartitle[varnom][0]+reg)
                if qcd_first:
                    hstack.Add(regions[reg]['bkg'])
                    hstack.Add(regions[reg]['QCD'])
                else:
                    hstack.Add(regions[reg]['QCD'])
                    hstack.Add(regions[reg]['bkg'])

                c = rt.TCanvas(var+reg+weight,var+reg+weight,5,30,W_ref,H_ref)
                pad1 = rt.TPad("pad1", "pad1", 0.0, 0.15 if plot_data else 0.0, 1, 1.0)
                pad1.Draw()
                pad1.cd()
                SetupCanvas(pad1, vartitle[varnom][2])
                if use_bin_opt:
                    hframe = rt.TH1F(var+reg,"h; {0}; Events ".format(vartitle[varnom][0]),len(opt_bin)-1,opt_bin)
                else:
                    hframe = rt.TH1F(var+reg,"h; {0}; Events ".format(vartitle[varnom][0]),vartitle[varnom][1][0],vartitle[varnom][1][1],vartitle[varnom][1][2])
                hframe.SetAxisRange(0.1, regions[reg]['data'].GetMaximum()*1e4 if vartitle[varnom][2] == 1 else regions[reg]['data'].GetMaximum()*1.8,"Y")
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
                    print reg
                    for b in range(nxbins):
                        nbkg = herr.GetBinContent(b+1)
                        ebkg = herr.GetBinError(b+1)

                        ndata = regions[reg]['data'].GetBinContent(b+1)
                        edata = regions[reg]['data'].GetBinError(b+1)
                        r = ndata / nbkg if nbkg>0 else 0

                        #print 'bin: ',b+1,  ' r: ',r
                        #print str(r) + '\t'
                        rerr = edata / nbkg if nbkg>0 else 0

                        hratio.SetBinContent(b+1, r)
                        hratio.SetBinError(b+1,rerr)

                        he.SetBinContent(b+1, 1)
                        he.SetBinError(b+1, ebkg/nbkg if nbkg>0 else 0 )

                    hratio.GetYaxis().SetRangeUser(0.0,2.0)

                    hratio.SetTitle("")

                    hratio.GetXaxis().SetTitle(vartitle[varnom][0])
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
                    hratio.GetYaxis().SetNdivisions(3,2,0,rt.kTRUE) #was 402
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
                if save_plots:
                    if not os.path.exists(destination+"/QCD Estimation"):
                        os.makedirs(destination+"/QCD Estimation")
                    else:
                        print "WARNING: directory already exists. Will overwrite existing files..."
                        c.SaveAs(destination+"/QCD Estimation/"+reg+var+".pdf")





        # fout.cd()
        # for reg in regions:
        #     regions[reg]['data'].Write()
        #     regions[reg]['bkg'].Write()
        #     regions[reg]['QCD'].Write()
        #     if verbose:
        #         regions[reg]['data'].GetName()
        #         print regions[reg]['bkg'].GetName()
        #         print regions[reg]['QCD'].GetName()


    fout.Close()


    #rt.gDirectory.GetList().Delete()
