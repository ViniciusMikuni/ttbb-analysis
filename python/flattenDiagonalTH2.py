#!/usr/bin/env python

import argparse
import os


import ROOT as R

def OpenFileAndGet(path, mode="read"):
    """Open ROOT file in a mode, check if open properly, and return TFile handle."""

    _tf = R.TFile.Open(path, mode)
    if not _tf.IsOpen():
        raise Exception("Could not open file {}".format(path))
    return _tf

def readRecursiveDirContent(content, currTDir):
    """Fill dictionary content with the directory structure of currTDir.
    Every object is read and put in content with their name as the key.
    Sub-folders will define sub-dictionaries in content with their name as the key.
    """

    if not currTDir.InheritsFrom("TDirectory") or not isinstance(content, dict):
        return

    # Retrieve the directory structure inside the ROOT file
    currPath = currTDir.GetPath().split(':')[-1].split('/')[-1]

    if currPath == '':
        # We are in the top-level directory
        thisContent = content
    else:
        thisContent = {}
        content[currPath] = thisContent

    listKeys = currTDir.GetListOfKeys()

    for key in listKeys:
        obj = key.ReadObj()
        if obj.InheritsFrom("TDirectory"):
            print("Entering sub-directory {}".format(obj.GetPath()))
            readRecursiveDirContent(thisContent, obj)
        else:
            name = obj.GetName()
            thisContent[name] = obj
            obj.SetDirectory(0)


def writeRecursiveDirContent(content, currTDir):
    """Write the items in dictionary content to currTDir, respecting the sub-directory structure."""

    if not currTDir.IsWritable() or not isinstance(content, dict):
        return

    for key, obj in content.items():
        if isinstance(obj, dict):
            print("Creating new sub-directory {}".format(key))
            subDir = outTFile.mkdir(key)
            writeRecursiveDirContent(obj, subDir)
        elif isinstance(obj, R.TObject):
            currTDir.WriteTObject(obj, key)

def flattenLowerRightDiagonalTH2(skipRows=0, rebin=1):
    """
    Rebin TH2 along X and Y axes before flattening if needed.
    Start at (xBin,yBin) = (skipRows, skipRows), (AFTER REBINNING) useful if those bins are always empty for some reason.
    """

    def flattenLowerRightDiagonalTH2Impl(th2):
        """Given square TH2 with n*n bins, return TH1 with n*(n+1)/2 bins.
        The bin contents and errors of the lower-right triangle (x>=y) of the TH2 are taken over.
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
            raise Exception(" I don't know what a {} is".format(th2.ClassName()))
        th1 = thClass(name, th2.GetTitle(), nBins, 1., nBins+1.)
        th1.SetDirectory(0)
        th1.Sumw2()

        th1Bin = 1
        # Don't start at the first row if asked
        for y in range(1+skipRows, nBinsX+1):
            for x in range(y, nBinsX+1):
                assert(th1Bin <= nBins)
                # print("Bin {},{}: content = {}".format(x, y, th2.GetBinContent(x, y)))
                th1.SetBinContent(th1Bin, th2.GetBinContent(x, y))
                th1.SetBinError(th1Bin, th2.GetBinError(x, y))
                th1Bin += 1

        return th1
    return flattenLowerRightDiagonalTH2Impl


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flatten all TH2s in the input file to keep the bins including and below the diagonal as a TH1 (does NOT use under- or overflow for now), i.e. x >= y.\nWrite these TH1s in the output file with the same directory structure as the input.')
    
    parser.add_argument('-i', '--input', type=str, required=True, help='Input ROOT file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output ROOT file')
    parser.add_argument('--skip-rows', type=int, default=0, help='Skip first n rows - AFTER REBINNING')
    parser.add_argument('--rebin', type=int, default=1, help='Rebin n times along x and y axis before flattening')

    options = parser.parse_args()
    
    inTFile = OpenFileAndGet(options.input)
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

    outTFile = OpenFileAndGet(options.output, "recreate")
    writeRecursiveDirContent(outContent, outTFile)
    outTFile.Close()
