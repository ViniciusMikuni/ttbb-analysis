import ConfigParser
import ROOT as rt
import array
from Plotting_cfg import *
from Estimate_QCD2 import Estimate_QCD
import ast
from math import *

rt.gROOT.SetBatch(True)

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read('sys.cfg')
    verbose = config.getboolean('GENERAL','verbose')

    #fname = config['GENERAL']['hfile']
    #interest_var_ = config['GENERAL']['var']

    files = {}
    tree = {}
    do_sys = config.getboolean('GENERAL','do_sys')
    sys_ =ast.literal_eval(config.get('SYSTEMATICS','syslist_'))
    if verbose: print sys_
    directions_ = ['Up','Down']
    processlist = ast.literal_eval(config.get('PROCESSES','processlist'))
    if verbose: print processlist
    for iproc, process in enumerate(processlist): #ntuple files
        if process in processgroup:
            for subprocess in processgroup[process]:
                files[subprocess]=rt.TFile(processfiles[subprocess],"READ")
                tree[subprocess]= files[subprocess].Get('tree')
        elif  'ttbar' in process:
            for tproc in ttplot:
                files[tproc]=rt.TFile(processfiles[process],"READ")
                tree[tproc]= files[tproc].Get('tree')
        else:

            files[process] =rt.TFile(processfiles[process],"READ")
            tree[process] =files[process].Get('tree')

    #add_cut = rt.TCut(config['GENERAL']['cut'])

    Estimate_QCD(config,'','',False,processlist,tree) #remember that if qgLR cut changes so do qwfactor
    if do_sys:
        for sys in sys_:
            for dire in directions_:
                if 'weight' in sys:
                    is_weight = True
                else:
                    is_weight = False
                Estimate_QCD(config,sys,dire,is_weight,processlist,tree)
    do_theory = config.getboolean('GENERAL','do_theory')
    if do_theory:
        print 'Make sure that the fit variable has no under or overflows'
        t_theory={}
        f_theory={}
        weight = config.get('GENERAL','weight')
        cut=''
        for item, val in config.items('CUT'):
            cut+=item+val+'&&'

        var = ast.literal_eval(config.get('GENERAL','var'))

        theory_samples_=[
            'isr',
            'fsr',
            'tune',
            'hdamp'
            ] #PDF and renormalisation/factorisation to be added
        nominal='ttbar'
        f_theory[nominal]= rt.TFile(processfiles[nominal],"READ")
        t_theory[nominal]= f_theory[nominal].Get('tree')
        hlist={}
        nominal_size={}
        for tt_cat in ttplot:
            t_theory[nominal].Draw(var[0]+ '>>'+ 'h'+tt_cat+ str(vartitle[var[0]][1]),weight+"*("+cut+ttCls[tt_cat]+")")
            hnom = rt.gDirectory.Get('h'+tt_cat)
            nominal_size[tt_cat]=hnom.Integral()*dscale[nominal]
        for sample in theory_samples_:
            hlist[sample]={}
            for dire in directions_:
                f_theory[sample+dire]=rt.TFile(processfiles[sample+dire],"READ")
                t_theory[sample+dire]= f_theory[sample+dire].Get('tree')
                hlist[sample][dire]={}
                for tt_cat in ttplot:

                    t_theory[sample+dire].Draw(var[0] + '>>'+ 'h'+sample+dire+tt_cat+ str(vartitle[var[0]][1]),weight+"*("+cut+ttCls[tt_cat]+")")
                    #print var[0] + '>>'+ 'h'+sample+dire+ str(vartitle[var[0]][1]),weight+"*("+cut+ttCls[tt_cat]+")"
                    h=rt.gDirectory.Get('h'+sample+dire+tt_cat)

                    h.Sumw2()

                    h.Scale(dscale[sample+dire])

                    hlist[sample][dire][tt_cat] = (h.Integral(),sqrt(h.GetSumw2().GetSum()))
            print sample
            print '#'*80
            for tt_cat in ttplot:
                cat = 0
                if nominal_size[tt_cat] >= hlist[sample]['Up'][tt_cat][0] and nominal_size[tt_cat] >= hlist[sample]['Down'][tt_cat][0]:
                    down = nominal_size[tt_cat] - min(hlist[sample]['Up'][tt_cat][0],hlist[sample]['Down'][tt_cat][0])
                    cat=1
                    if down < max(hlist[sample]['Up'][tt_cat][1],hlist[sample]['Down'][tt_cat][1]):
                        cat=2
                        down =  max(hlist[sample]['Up'][tt_cat][1],hlist[sample]['Down'][tt_cat][1])
                    up=max(hlist[sample]['Up'][tt_cat][1],hlist[sample]['Down'][tt_cat][1])
                elif nominal_size[tt_cat] <= hlist[sample]['Up'][tt_cat][0] and nominal_size[tt_cat] <= hlist[sample]['Down'][tt_cat][0]:
                    cat=3
                    up = - nominal_size[tt_cat] + max(hlist[sample]['Up'][tt_cat][0],hlist[sample]['Down'][tt_cat][0])
                    if up < max(hlist[sample]['Up'][tt_cat][1],hlist[sample]['Down'][tt_cat][1]):
                        cat=4
                        up =  max(hlist[sample]['Up'][tt_cat][1],hlist[sample]['Down'][tt_cat][1])
                    down=max(hlist[sample]['Up'][tt_cat][1],hlist[sample]['Down'][tt_cat][1])
                else:
                    if nominal_size[tt_cat] > hlist[sample]['Up'][tt_cat][0]:
                        cat=5
                        down = max(nominal_size[tt_cat]- hlist[sample]['Up'][tt_cat][0],hlist[sample]['Up'][tt_cat][1])
                        up = max(-nominal_size[tt_cat]+ hlist[sample]['Down'][tt_cat][0],hlist[sample]['Down'][tt_cat][1])
                        print 'up', -nominal_size[tt_cat]+ hlist[sample]['Down'][tt_cat][0], 'MC' ,hlist[sample]['Down'][tt_cat][1]
                        print 'down',nominal_size[tt_cat]- hlist[sample]['Up'][tt_cat][0],'MC', hlist[sample]['Up'][tt_cat][1]
                    else:
                        cat=6
                        down = max(nominal_size[tt_cat]- hlist[sample]['Down'][tt_cat][0],hlist[sample]['Down'][tt_cat][1])
                        up = max(-nominal_size[tt_cat]+ hlist[sample]['Up'][tt_cat][0],hlist[sample]['Up'][tt_cat][1])
                print tt_cat, "+", 1+ up/nominal_size[tt_cat], "-", 1-down/nominal_size[tt_cat], " cat: ", cat
