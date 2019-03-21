#! /bin/env python

from __future__ import print_function
from math import sqrt
import numpy as np

import CombineHarvester.CombineTools.ch as ch
import ROOT as R

cb = ch.CombineHarvester()
cb.ParseDatacard("datacard.dat")
bins = cb.bin_set()

nBins = 32

defaultValues = {}
for b in bins:
    defaultValues[b] = {}
    for i in range(1, nBins+1):
        init = cb.cp().bin([b]).process(['QCD_bin_{}'.format(i)]).GetShape().Integral()
        defaultValues[b][i] = init

_tf = R.TFile("fitDiagnostics.root")
fitResult = _tf.Get("fit_s")

nSamples = 1000
sums = {}
for b in bins:
    sums[b] = np.zeros(nSamples)

for n in range(nSamples):
    sample = fitResult.randomizePars()
    thisSum = {}
    for b in bins:
        thisSum[b] = 0.
    # sums[i] = defaultValues['CR1'][32] * sample.at(sample.index("yield_QCD_CR1_bin_32")).getValV()
    for i in range(1, nBins+1):
        yield_CR1 = defaultValues['CR1'][i] * sample.at(sample.index("yield_QCD_CR1_bin_{}".format(i))).getValV()
        yield_CR2 = defaultValues['CR2'][i] * sample.at(sample.index("yield_QCD_CR2_bin_{}".format(i))).getValV()
        yield_VR = defaultValues['VR'][i] * sample.at(sample.index("yield_QCD_VR_bin_{}".format(i))).getValV()
        yield_SR = yield_VR * yield_CR1 / yield_CR2
        thisSum['SR'] += yield_SR
        thisSum['CR1'] += yield_CR1
        thisSum['CR2'] += yield_CR2
        thisSum['VR'] += yield_VR
    for b in bins:
        sums[b][n] = thisSum[b]

for b in bins:
    print(b)
    print("Average: {}".format(sums[b].mean()))
    print("Std. dev.: {}".format(sums[b].std()))
    print("Uncertainty: {:3.1f}%".format(100. * sums[b].std() / sums[b].mean()))
    

_tf.Close()
