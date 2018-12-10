#!/usr/bin/env python

import csv
from subprocess import call
from math import sqrt
import ROOT as R

from definitions import exp_systs

nominalFit = '../higgsCombineTest.MultiDimFit.mH120.root'
fitCommand = 'combine -M MultiDimFit -d ../workspace.root --rMin 0 --rMax 3 --expectSignal=1 -t -1 --algo singles --freezeNuisanceGroups=extern --freezeParameters {} -n _{} --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=999999999 --X-rtd MINIMIZER_analytic --robustFit 1 --setCrossingTolerance 1E-5'

jec_systs = [ s for s in exp_systs if ( '_j' in s and s != "CMS_JER_j" ) ]

nuisanceGroups = {
    "MC_stat": "'rgx{prop_.*}'",
    "JER": "CMS_JER_j",
    "JES": ",".join(jec_systs),
    "btag_b": "'rgx{CMS_btag_hf.*}'",
    "btag_c": "'rgx{CMS_btag_lf.*}'",
    "btag_l": "'rgx{CMS_btag_cf.*}'",
    "qg": "CMS_qg_Weight",
    "pu": "CMS_pu_Weight",
    "trigger": "CMS_trig_Weight",
    "ttcc_norm": "ttcc_norm",
    "tune": "tune",
    "hdamp": "'rgx{hdamp_.*}'",
    "pdf": "CMS_LHEPDF_Weight",
    "QCDscale": "'rgx{CMS_LHEscale_Weight_.*}'",
    "fsr_isr": "'rgx{(i|f)sr_.*}'",
    "lumi": "lumi_13TeV_2016"
}

def getFitUncertainties(_f):
    tf = R.TFile.Open(_f)
    tt = tf.Get('limit')
    tt.GetEntry(0)
    nom = tt.r
    tt.GetEntry(1)
    down = tt.r
    tt.GetEntry(2)
    up = tt.r
    tf.Close()
    return nom,down,up

# assumes the nominal fit has been run!
nom,nom_down,nom_up = getFitUncertainties(nominalFit)
nom_rel_down = abs(nom - nom_down) / nom
nom_rel_up = abs(nom - nom_up) / nom
    
values = {}

for source,group in nuisanceGroups.items():

    call(fitCommand.format(group, source), shell=True)
    values[source] = getFitUncertainties('higgsCombine_{}.MultiDimFit.mH120.root'.format(source))

print('\n\n')

with open("broken_systematic_sources.csv", "wb") as _f:
    writer = csv.DictWriter(_f, fieldnames=['source', 'up', 'down'])
    writer.writeheader()

    for source in nuisanceGroups.keys():
        val,var_down,var_up = values[source]
        rel_down = abs(val - var_down) / nom
        rel_up = abs(val - var_up) / nom
        try:
            contrib_down = sqrt(nom_rel_down**2 - rel_down**2)
        except ValueError:
            print("Warning: source {} down has gone wrong. Nominal rel. down: {}, rel. down: {}".format(source, nom_rel_down, rel_down))
            contrib_down = 0
        try:
            contrib_up = sqrt(nom_rel_up**2 - rel_up**2)
        except ValueError:
            print("Warning: source {} up has gone wrong. Nominal rel. up: {}, rel. up: {}".format(source, nom_rel_up, rel_up))
            contrib_up = 0
        writer.writerow({'source': source, 'up': contrib_up, 'down': contrib_down})
        print('Effect of {}: +{:.1f}% / -{:.1f}%'.format(source, 100 * contrib_up, 100 * contrib_down))

