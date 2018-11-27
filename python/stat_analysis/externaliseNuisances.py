#!/usr/bin/env python

from subprocess import call
import ROOT as R

from definitions import externalised_nuisances
# externalised_nuisances = ['tune', 'isr', 'fsr']

nominalFit = 'higgsCombineTest.MultiDimFit.mH120.root'
initialCommand = 'combine -M GenerateOnly --saveToys --toysNoSystematics --expectSignal=1 -t -1 -n _toyAsimov -d workspace.root'
fitCommand = 'combine -M MultiDimFit -d workspace.root --algo singles --freezeNuisanceGroups=extern -n _fit_{nuisance}_{dire} --toysFile=higgsCombine_toyAsimov.GenerateOnly.mH120.123456.root --freezeParameters {nuisance} --setParameters {nuisance}={val}'

directions = {"up": 1, "down": -1}

call(initialCommand, shell=True)

def getFitXS(_f):
    tf = R.TFile.Open(_f)
    tt = tf.Get('limit')
    tt.GetEntry(0)
    val = tt.r
    tf.Close()
    return val

nominal = getFitXS(nominalFit)
    
values = {}

# assumes the nominal fit has been run!
for nuisance in externalised_nuisances:

    values[nuisance] = {}

    for dire, val in directions.items():
        call(fitCommand.format(nuisance=nuisance, dire=dire, val=val), shell=True)
        values[nuisance][dire] = getFitXS('higgsCombine_fit_{}_{}.MultiDimFit.mH120.root'.format(nuisance, dire))

print('\n\n')

for nuisance in externalised_nuisances:
    up, down = values[nuisance]['up'], values[nuisance]['down']
    print('Effect of {}: +{:.1f}% / -{:.1f}%'.format(nuisance, 100 * abs(up-nominal)/nominal, 100 * abs(down-nominal)/nominal))


