#!/usr/bin/env python

import argparse
import os
import pickle

import ROOT as R

from HistogramTools import openFileAndGet, readRecursiveDirContent, writeRecursiveDirContent
from definitions import tt_bkg, sig_processes, other_bkg

regions = ['SR', 'VR', 'CR1', 'CR2']

def addLists(a, b):
    return [ a[i] + b[i] for i in range(len(a)) ]

def findMapping(hists, thresh):
    # TH1F -> list keeps under- and overflow, we don't want those
    nBins = len(hists[tt_bkg[0]]) - 2

    # new histograms will have bins [ (i,j), (k,l,m), (n), ... ] of the old histograms
    # caution: start indexing at zero
    mapping = [ [n] for n in range(nBins) ]
    
    sig = [0] * nBins
    for proc in sig_processes:
        sig = addLists(sig, list(hists[proc])[1:-1])
    
    # Don't forget QCD!
    bkg = [0] * nBins
    for proc in tt_bkg + other_bkg + ['QCD_subtr']:
        bkg = addLists(bkg, list(hists[proc])[1:-1])

    def getSB():
        return [ sig[i] / bkg[i] for i in range(nBins) ]
    
    print("Sorted S/B before:")
    print(sorted(getSB()))

    sumw2 = [0] * nBins
    for proc in sig_processes + tt_bkg + other_bkg:
        sumw2 = addLists(sumw2, list(hists[proc].GetSumw2())[1:-1])

    while True:
        sb = getSB()
        nEff = [ (sig[i] + bkg[i])**2/sumw2[i] for i in range(nBins) ]
        minNEff = min(nEff)
        if minNEff >= thresh:
            break

        iMinNEff = nEff.index(minNEff)
        sbMinNEff = sb[iMinNEff]

        # Find the bin with the closest S/B value, among *all* bins
        minSBDist = 99999
        iMinSBDist = 0
        for i in range(nBins):
            if i == iMinNEff:
                continue
            sbDist = abs(sb[i] - sbMinNEff)
            if sbDist < minSBDist:
                minSBDist = sbDist
                iMinSBDist = i

        print("Will merge bins {} and {} which have S/B {:.2f} and {:.2f}".format(mapping[iMinNEff], mapping[iMinSBDist], sbMinNEff, sb[iMinSBDist]))

        # merge iMinNEff and iMinSBDist (python indexing)
        nBins -= 1

        sig[iMinNEff] += sig[iMinSBDist]
        sig.pop(iMinSBDist)
        
        bkg[iMinNEff] += bkg[iMinSBDist]
        bkg.pop(iMinSBDist)

        sumw2[iMinNEff] += sumw2[iMinSBDist]
        sumw2.pop(iMinSBDist)

        mapping[iMinNEff] += mapping[iMinSBDist]
        mapping.pop(iMinSBDist)
    
    sb = getSB()
    
    # sort by increasing S/B
    sorting = sorted(range(nBins), key=sb.__getitem__)
    mapping = [ mapping[i] for i in sorting ]

    print("Proposed mapping:")
    print(mapping)
    
    print("Sorted S/B after:")
    print(sorted(sb))

    return mapping


def applyMapping(mapping, hist):
    oldNBins = hist.GetXaxis().GetNbins()
    newBins = len(mapping)
    name = hist.GetName()
    hist.SetName(name + "_old")
    
    if "TH1D" in hist.ClassName():
        thClass = R.TH1D
    elif "TH1F" in hist.ClassName():
        thClass = R.TH1F
    else:
        raise Exception("I don't know what a {} is".format(th2.ClassName()))
    
    newHist = thClass(name, hist.GetTitle(), newBins, 0, newBins)
    newHist.Sumw2()

    for i, merge in enumerate(mapping):
        content = 0.
        sumw2 = 0.
        for b in merge:
            content += hist.GetBinContent(b+1)
            sumw2 += hist.GetSumw2()[b+1]
        newHist.SetBinContent(i+1, content)
        newHist.GetSumw2()[i+1] = sumw2

    return newHist


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Optimise the binning according to S/B and stat uncertainty')
    
    parser.add_argument('-i', '--input', type=str, required=True, help='Input ROOT file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output pkl file containing the mapping')
    parser.add_argument('-t', '--threshold', type=int, default=1000, help='Neff threshold')

    options = parser.parse_args()
    
    inTFile = openFileAndGet(options.input)
    inContent = {}
    readRecursiveDirContent(inContent, inTFile)
    inTFile.Close()

    mapping = findMapping(inContent['SR'], options.threshold)
    
    with open(options.output, 'w') as _f:
        pickle.dump(mapping, _f)
