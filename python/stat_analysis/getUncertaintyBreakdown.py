#!/usr/bin/env python

import csv
from subprocess import call
from math import sqrt
import ROOT as R

from definitions import exp_systs

nominalFit = '../higgsCombineTest.MultiDimFit.mH120.root'
fitCommand = 'combine -M MultiDimFit -d ../workspace.root --rMin 0 --rMax 5 --expectSignal=1 -t -1 --algo singles --freezeNuisanceGroups=extern --freezeParameters {} -n _{} --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=999999999 --X-rtd MINIMIZER_analytic --robustFit 1 --setCrossingTolerance 1E-7'

jec_systs = [ s for s in exp_systs if ( '_j' in s and s != "CMS_JER_j" ) ]

nuisanceGroups = {
    "MC_stat": ("Simulated sample size", "'rgx{prop_.*}'"),
    # "JER": "CMS_JER_j",
    # "JES": ",".join(jec_systs),
    "JES_JER": ("JES \& JER", "'rgx{CMS_.*_j}'"),
    "btag": ("\PQb tagging", "'rgx{CMS_btag_.*}'"),
    # "btag_b": "'rgx{CMS_btag_hf.*}'",
    # "btag_c": "'rgx{CMS_btag_lf.*}'",
    # "btag_l": "'rgx{CMS_btag_cf.*}'",
    "qg": ("Quark-gluon likelihood", "CMS_qg_Weight"),
    "pu": ("Pileup", "CMS_pu_Weight"),
    "trigger": ("Trigger efficiency", "CMS_trig_Weight"),
    "ttcc_norm": (r"\ttbarcc normalisation", "ttcc_norm"),
    "tune": ("UE tune", "tune"),
    "hdamp": ("Shower matching (hdamp)", "'rgx{hdamp_.*}'"),
    "pdf": ("PDFs", "CMS_LHEPDF_Weight"),
    "QCDscale": ("$\mu_{R}$ and $\mu_{F}$ scales", "'rgx{CMS_LHEscale_Weight_.*}'"),
    "fsr_isr": ("Parton shower scale", "'rgx{(i|f)sr_.*}'"),
    "lumi": ("Integrated luminosity", "lumi_13TeV_2016")
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

    call(fitCommand.format(group[1], source), shell=True)
    values[source] = getFitUncertainties('higgsCombine_{}.MultiDimFit.mH120.root'.format(source))

print('\n\n')

csv_f = open("broken_systematic_sources.csv", "wb")
writer = csv.DictWriter(csv_f, fieldnames=['source', 'up', 'down'])
writer.writeheader()

nice_csv_f = open("broken_systematic_sources_nice.csv", "wb")
nice_writer = csv.DictWriter(nice_csv_f, fieldnames=['source', 'up/down', 'order'])
nice_writer.writeheader()

for source in sorted(nuisanceGroups.keys()):
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
    nice_writer.writerow({'source': nuisanceGroups[source][0], 'up/down': '+{:.1f}/-{:.1f}'.format(100 * contrib_up, 100 * contrib_down), 'order': contrib_up})
    print('Effect of {}: +{:.1f}% / -{:.1f}%'.format(source, 100 * contrib_up, 100 * contrib_down))

csv_f.close()
nice_csv_f.close()
