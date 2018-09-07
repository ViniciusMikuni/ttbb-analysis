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


def Calculate_qwfrac(tree,weight='',proc='',cut='qgLR > 0.636581'):
    wnom = weight.replace('qgweight*','')
    n_nom = tree.Draw('',wnom+'*'+cut)
    n_qglr = tree.Draw('',weight+'*'+cut)
    qg_fac = float(n_nom)/n_qglr if n_qglr >0 else 1.0
    print  proc,':',qg_fac
    return qg_fac


def Make_Hists(interest_var=[],sysname = '',direction='',is_weight = False, processlist=[],tree={},add_cut='', is_overflow=True,fname = 'hCard_0.root',verbose = True):
    #addCut = 'n_jets >=8 && simple_chi2<34.4046 && BDT_CWoLa > 0.221061 && BDT_Comb > 0.102203 && qgLR > 0.722416'
    calc_qwfac=True
    setQCD0error = False
    QCD_fname = 'QCD_Estimate_CR.root'

    dnames = {'data':'data_obs','ttlf':'ttlf','diboson':'VV','ttV':'ttV','VJ':'VJ','stop':'stop','QCD':'QCD','ttcc':'ttcc','ttbb':'ttbb','tt2b':'tt2b','ttb':'ttb'}
    hname = OrderedDict(sorted(dnames.items(), key=lambda t: t[0]))
    bkgs_ = list(filter(lambda x: x not in ['QCD','data'], processlist))
    hvar = []
    hlist = []


    weight = 'weight*puweight*btagweight*qgweight*trigWeight(ht,jet5pt,nBCSVM)'
    if is_weight:
        weight_name = sysname[1:].partition('_')[0]
        if 'top' not in weight_name:
            weight = weight.replace(weight_name,sysname[1:]+'_'+direction)

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
                h = f_QCD.Get('QCDSR'+var)
                if setQCD0error:
                    for bin in range(h.GetSize()-1):
                        h.SetBinError(bin+1,0)
                h.SetName(hname[proc]+nuis_name)
                hlist.append(h)
            elif proc in ttplot:
                topweight = weight + "*topweight"
                if 'top' in sysname:
                    topweight = topweight.replace('topweight',sysname[1:]+'_'+direction)
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
