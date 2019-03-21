#!/usr/bin/env python

import argparse
import ROOT

from HistogramTools import writeRecursiveDirContent, readRecursiveDirContent, openFileAndGet

def getBinByBinFractions(hists, processes):
    sumHist = hists[processes[0]].Clone("sumHist")

    for proc in processes[1:]:
        sumHist.Add(hists[proc])

    toRet = {}
    for proc in processes:
        ratio = hists[proc].Clone(proc + "_ratio")
        ratio.Divide(sumHist)
        toRet[proc] = ratio

    return toRet


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('--choice', choices=['all', 'tt'])
    args = parser.parse_args()

    input_f = openFileAndGet(args.input)
    content = {}
    readRecursiveDirContent(content, input_f)
    input_f.Close()

    procList = {
        "all": ["ttbb", "ttbb_other", "ttb_other", "tt2b", "ttcc", "ttlf", "stop", "VJ", "VV", "ttV", "ttH"] + [ "QCD_bin_{}".format(i) for i in range(1, 33) ],
        "tt": ["ttbb", "ttbb_other", "ttb_other", "tt2b", "ttcc", "ttlf"],
    }


    toSave = {}
    for cat, hists in content.items():
        toSave[cat] = getBinByBinFractions(hists, procList[args.choice])

    totalHists = {}
    for proc in procList[args.choice]:
        totalHists[proc] = content["SR"][proc].Clone(proc + "_sum")
        totalHists[proc].Reset()
        for cat in content.keys():
            totalHists[proc].Add(content[cat][proc])

    toSave["total"] = getBinByBinFractions(totalHists, procList[args.choice])

    output_f = openFileAndGet(args.output, "recreate")
    writeRecursiveDirContent(toSave, output_f)
    output_f.Close()
