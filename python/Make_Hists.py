import ROOT as rt
from Plotting_cfg import *
from math import *
from collections import OrderedDict
rt.gROOT.SetBatch(True)
rt.gROOT.LoadMacro("../src/triggerWeightRound.h+")
from Estimate_QCD import Estimate_QCD
#####################################################
# TO DO:
# fix the plots for all systematics
# propagate topweight to QCD Estimation
#####################################################




def Make_Hists(config,sysname = '',direction='',is_weight = False,tree={}, is_overflow=True):
    fname = config.get('GENERAL','hfile')
    verbose = config.getboolean('GENERAL','verbose')
    calc_qwfac=config.getboolean('GENERAL','calc_qwfac')
    setQCD0error=config.getboolean('GENERAL','setQCD0error')
    QCD_fname = config.get('GENERAL','QCDfile')
    weight = config.get('GENERAL','weight')
    topweight=weight+'&&topweight'
    interest_var=ast.literal_eval(config.get('GENERAL','var'))
    add_cut = ''
    for item, cut in config.items('CUT'):
        add_cut+=item+sysname+direction+cut+'&&'
    add_cut=add_cut[:-2] #Remove last &&
            
    dnames = {'data':'data_obs','ttlf':'ttlf','diboson':'VV','ttV':'ttV','VJ':'VJ','stop':'stop','QCD':'QCD','ttcc':'ttcc','ttbb':'ttbb','tt2b':'tt2b','ttb':'ttb'}
    hname = OrderedDict(sorted(dnames.items(), key=lambda t: t[0]))
    bkgs_ = list(filter(lambda x: x not in ['QCD','data'], processlist))
    hvar = []
    hlist = []


    if is_weight:
        weight_name = sysname[1:].partition('_')[0] #btagweight
        if 'top' not in weight_name:
            weight = weight.replace(weight_name,sysname[1:]+'_'+direction)
        else:
            topweight +=direction

    if verbose: print 'weight: ', weight


    for nvar, var in enumerate(interest_var):
        if is_weight == False and sysname != '':
            var+=sysname+direction
        for proc in hname:
            if sysname != '':
                if is_weight:
                    if 'btag' in sysname: nuis_name = sysname.replace('btagweight','CMS_ttbb')+direction
                    else: nuis_name = '_CMS'+sysname.replace('weight','')+direction
                else:nuis_name='_CMS'+sysname+'_j'+direction
            else:nuis_name=sysname+direction


            if proc == 'QCD':
                Estimate_QCD(var,sysname if is_weight == False else '',direction if is_weight == False else '',weight,bkgs_,tree,fout = QCD_fname)
                f_QCD = rt.TFile(QCD_fname,"READ")
                h = f_QCD.Get('QCD{0}{1}'.format(config['GENERAL']['Reg'],var))
                if setQCD0error:
                    for bin in range(h.GetSize()-1):
                        h.SetBinError(bin+1,0)
                h.SetName(hname[proc]+nuis_name)
                hlist.append(h)
            elif proc in ttplot:
                topweight = weight + "*topweight"
                if 'top' in sysname:
                    topweight = topweight.replace('topweight',sysname[1:]+direction)
                tree[proc].Draw(var + '>>'+ 'h'+proc+ str(vartitle[var.partition('_')[0]][1]),topweight+"*("+add_cut+"&&"+ttCls[proc] + ")")
                h = rt.gDirectory.Get('h'+proc).Clone(hname[proc]+nuis_name)
                if is_overflow: AddOverflow(h)
                h.Scale(dscale['ttbar'])
                # if calc_qwfac: Calculate_qwfrac(tree[proc],weight+"*topweight",proc)
                # else: h.Scale(qwfac[proc])
                hlist.append(h)

            elif proc in processgroup:
                for isub, subprocess in enumerate(processgroup[proc]):
                    tree[subprocess].Draw(var + ">>" + "h"+subprocess+str(vartitle[var.partition('_')[0]][1]),weight+"*("+add_cut+")")
                    if isub == 0:
                        h = rt.gDirectory.Get('h'+subprocess).Clone(hname[proc]+nuis_name)
                        if is_overflow: AddOverflow(h)
                        h.Scale(dscale[subprocess])
                        # if calc_qwfac:Calculate_qwfrac(tree[subprocess],weight,subprocess)
                        # else: h.Scale(qwfac[subprocess])
                    else:
                        hsub = rt.gDirectory.Get('h'+subprocess).Clone(subprocess+nuis_name)
                        if is_overflow: AddOverflow(h)
                        # if calc_qwfac:Calculate_qwfrac(tree[subprocess],weight,subprocess)
                        # else:h.Scale(qwfac[subprocess])
                        hsub.Scale(dscale[subprocess])
                        h.Add(hsub)

                hlist.append(h)
            else:
                if proc == 'data':
                    if sysname == '':
                        tree[proc].Draw(var + '>>'+ 'h'+proc+str(vartitle[var.partition('_')[0]][1]),"("+add_cut+")")
                        print var + '>>'+ 'h'+proc+str(vartitle[var.partition('_')[0]][1]),"("+add_cut+")"
                    else: continue
                else:
                    tree[proc].Draw(var + '>>'+ 'h'+proc+str(vartitle[var.partition('_')[0]][1]),weight+"*("+add_cut+")")
                h = rt.gDirectory.Get('h'+proc).Clone(hname[proc]+nuis_name)
                if is_overflow: AddOverflow(h)
                # if calc_qwfac:Calculate_qwfrac(tree[proc],weight,proc)
                # else:h.Scale(qwfac[proc])
                h.Scale(dscale[proc])
                hlist.append(h)


        nbkg = 0
        ndata = 0
        for h in hlist:
            if h.GetName() == 'data_obs':ndata = h.Integral()
            else: nbkg+=h.Integral()

    fout = rt.TFile(fname,'UPDATE')
    for h in hlist:
        print h.GetName(),
        h.Write()
    for h in hlist:
        print h.Integral(), sqrt(h.GetSumw2().GetSum())
    fout.Close()
