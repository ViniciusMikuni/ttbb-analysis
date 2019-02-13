#!/usr/bin/env python

import csv
from subprocess import call
import ROOT as R

from definitions import externalised_nuisances
# externalised_nuisances = ['GluonMoveCRTune']

nominalFit = '../higgsCombineTest.MultiDimFit.mH120.root'
# initialCommand = 'combine -M GenerateOnly --saveToys --toysNoSystematics --expectSignal=1 -t -1 -n _toyAsimov -d ../workspace.root'
# fitCommand = 'combine -M MultiDimFit -d ../workspace.root --algo singles --freezeNuisanceGroups=extern -n _fit_{nuisance}_{dire} --toysFile=higgsCombine_toyAsimov.GenerateOnly.mH120.123456.root --freezeParameters {nuisance} --setParameters {nuisance}={val} --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=99999999999 --robustFit 1 -t -1'
fitCommand = 'combine -M MultiDimFit -d ../workspace.root --algo singles --freezeNuisanceGroups=extern -n _fit_{nuisance}_{dire} --freezeParameters {nuisance} --setParameters {nuisance}={val} --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_MaxCalls=99999999999 --robustFit 1 --cminDefaultMinimizerPrecision 1E-13'

directions = {"up": 1, "down": -1}

# call(initialCommand, shell=True)

def getFitXS(_f):
    tf = R.TFile.Open(_f)
    tt = tf.Get('limit')
    tt.GetEntry(0)
    val = tt.r
    tf.Close()
    return val

nominal = getFitXS(nominalFit)

print("Retrieved nominal best-fit: {}".format(nominal))
    
values = {}

# assumes the nominal fit has been run!
for nuisance in externalised_nuisances:

    values[nuisance] = {}

    for dire, val in directions.items():
        call(fitCommand.format(nuisance=nuisance, dire=dire, val=val), shell=True)
        values[nuisance][dire] = getFitXS('higgsCombine_fit_{}_{}.MultiDimFit.mH120.root'.format(nuisance, dire))

print('\n\n')

with open("extern_systematics.csv", "wb") as _f:
    writer = csv.DictWriter(_f, fieldnames=['source', 'up', 'down'])
    writer.writeheader()

    for nuisance in externalised_nuisances:
        up, down = values[nuisance]['up'], values[nuisance]['down']
        var_up = abs(up-nominal)/nominal
        var_down = abs(down-nominal)/nominal
        writer.writerow({'source': nuisance, 'up': var_up, 'down': var_down})
        print('Effect of {}: +{:.1f}% / -{:.1f}%'.format(nuisance, 100 * var_up, 100 * var_down))

