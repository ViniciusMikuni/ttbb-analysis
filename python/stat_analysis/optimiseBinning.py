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
    # fixed mapping with 32 bins
    mapping = [[1], [10], [0], [4], [11], [3], [5], [19], [2], [13], [12], [20], [34, 14], [23], [28], [29], [15, 6], [27, 21], [46, 7], [22], [16], [36, 30], [41, 37], [45, 35, 17], [24, 42, 25], [49, 50, 43, 8], [38, 40, 31], [47, 52, 32], [26, 33, 44], [39, 48, 18], [51, 9], [53, 54]]
    return mapping
    
    # TH1F -> list keeps under- and overflow, we don't want those
    nBins = len(hists[tt_bkg[0]]) - 2

    # new histograms will have bins [ [i,j], [k,l,m], [n], ... ] of the old histograms
    # caution: start indexing at zero
    # initial mapping is [ [0] [1] ... [nBins-1] ]
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

        # Find the bin with the closest S/B value, among *all* other bins
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

        # merge iMinNEff and iMinSBDist
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

    print("Proposed mapping: {} bins".format(len(mapping)))
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
        raise Exception("I don't know what a {} is".format(hist.ClassName()))
    
    newHist = thClass(name, hist.GetTitle(), newBins, 0, newBins)
    newHist.SetDirectory(0)
    newHist.Sumw2()

    for i, merge in enumerate(mapping):
        content = 0.
        sumw2 = 0.
        # careful, indexing in mapping starts at zero -> we start at bin nr. 1
        for b in merge:
            content += hist.GetBinContent(b+1)
            sumw2 += hist.GetSumw2()[b+1]
        newHist.SetBinContent(i+1, content)
        newHist.GetSumw2()[i+1] = sumw2

    return newHist


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Optimise the binning according to S/B and stat uncertainty')
    
    parser.add_argument('-i', '--input', type=str, required=True, help='Input ROOT file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output ROOT file where mapping is applied to all input histograms')
    parser.add_argument('-t', '--threshold', type=int, default=1000, help='Neff threshold')

    options = parser.parse_args()
    
    inTFile = openFileAndGet(options.input)
    inContent = {}
    readRecursiveDirContent(inContent, inTFile)
    inTFile.Close()

    mapping = findMapping(inContent['fiducial']['SR'], options.threshold)

    def mappingApplicator(_mapping):
        def impl(hist):
            return applyMapping(_mapping, hist)
        return impl
    
    def applyAndCopy(inDict, outDict, func, inherit):
        for key, obj in inDict.items():
            if isinstance(obj, dict):
                newDict = {}
                outDict[key] = newDict
                applyAndCopy(obj, newDict, func, inherit)
            elif obj.InheritsFrom(inherit):
                outDict[key] = func(obj)
            else:
                outDict[key] = obj

    outContent = {}
    applyAndCopy(inContent, outContent, mappingApplicator(mapping), "TH1")
    
    outTFile = openFileAndGet(options.output, "recreate")
    writeRecursiveDirContent(outContent, outTFile)
    outTFile.Close()

