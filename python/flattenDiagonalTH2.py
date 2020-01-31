#!/usr/bin/env python

import argparse
import os

import ROOT as R

from stat_analysis.HistogramTools import openFileAndGet, readRecursiveDirContent, writeRecursiveDirContent


def flattenLowerRightDiagonalTH2(skipRows=0, rebin=1):
    """
    Rebin TH2 along X and Y axes before flattening if needed.
    Start at (xBin,yBin) = (skipRows, skipRows), (AFTER REBINNING) useful if those bins are always empty for some reason.
    """

    def flattenLowerRightDiagonalTH2Impl(th2):
        """Given square TH2 with n*n bins, return TH1 with n*(n+1)/2 bins.
        The bin contents and errors of the upper-left triangle (x<=y) of the TH2 are taken over.
        All bins in the TH1 are of uniform size with arbitrary boundaries.
        Overflow and underflow of the TH2 are NOT taken into account.
        Appends '_th2' after the TH2's name, use the original name for the TH1.
        """
        if not th2.InheritsFrom('TH2'):
            raise Exception('Invalid object, not a TH2: {}'.format(th2.GetName()))

        name = th2.GetName()
        th2.SetName(name + '_th2')

        # Rebin, if asked
        th2.Rebin2D(rebin, rebin)

        nBinsX = th2.GetXaxis().GetNbins()
        nBinsY = th2.GetYaxis().GetNbins()
        assert(nBinsX == nBinsY)
        nBins = (nBinsX - skipRows) * (nBinsX - skipRows + 1) / 2

        if "TH2D" in th2.ClassName():
            thClass = R.TH1D
        elif "TH2F" in th2.ClassName():
            thClass = R.TH1F
        else:
            raise Exception("I don't know what a {} is".format(th2.ClassName()))
        th1 = thClass(name, th2.GetTitle(), nBins, 1., nBins+1.)
        th1.SetDirectory(0)
        th1.Sumw2()

        th1Bin = 1
        # Don't start at the first row if asked
        for x in range(1+skipRows, nBinsX+1):
            for y in range(x, nBinsX+1):
                assert(th1Bin <= nBins)
                # print("Bin {},{}: content = {}".format(x, y, th2.GetBinContent(x, y)))
                th1.SetBinContent(th1Bin, th2.GetBinContent(x, y))
                th1.SetBinError(th1Bin, th2.GetBinError(x, y))
                th1Bin += 1

        return th1
    return flattenLowerRightDiagonalTH2Impl


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flatten all TH2s in the input file to keep the bins including and above the diagonal as a TH1 (does NOT use under- or overflow for now), i.e. x<=y.\nWrite these TH1s in the output file with the same directory structure as the input.')
    
    parser.add_argument('-i', '--input', type=str, required=True, help='Input ROOT file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output ROOT file')
    parser.add_argument('--skip-rows', type=int, default=0, help='Skip first n rows - AFTER REBINNING')
    parser.add_argument('--rebin', type=int, default=1, help='Rebin n times along x and y axis before flattening')

    options = parser.parse_args()
    
    inTFile = openFileAndGet(options.input)
    inContent = {}
    readRecursiveDirContent(inContent, inTFile)
    inTFile.Close()

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
    myFlatten = flattenLowerRightDiagonalTH2(options.skip_rows, options.rebin)
    applyAndCopy(inContent, outContent, myFlatten, 'TH2')

    outTFile = openFileAndGet(options.output, "recreate")
    writeRecursiveDirContent(outContent, outTFile)
    outTFile.Close()
