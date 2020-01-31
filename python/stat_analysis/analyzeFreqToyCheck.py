#!/usr/bin/env python

# NOTE: to be used with recent LCG release

import os
import numpy as np
import argparse
import pickle
import ROOT as R
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import seaborn as sns
# sns.set(style="ticks", font_scale=1.2)

def analyze(inp, outp, number):
    baseFreeAll = "higgsCombine_freeAll_{0}.MultiDimFit.mH120.{0}.root"
    baseFreeCC = "higgsCombine_freeCC_{0}.MultiDimFit.mH120.{0}.root"
    baseFreeJJ = "higgsCombine_freeJJ_{0}.MultiDimFit.mH120.{0}.root"
    baseDefault = "higgsCombine_default_{0}.MultiDimFit.mH120.{0}.root"

    seed = "1234"

    default = -99999.

    fitFreeAll = []
    fitFreeCC = []
    fitFreeJJ = []
    fitDefault = []

    for i in range(1, int(number)+1):
        this = seed + str(i)

        def get(p):
            p = os.path.join(inp, p)
            if os.path.exists(p):
                _tf = R.TFile.Open(p)
                if not _tf.IsOpen() or _tf.IsZombie():
                    print("Could not open properly {}".format(p))
                    return default
                tree = _tf.Get("limit")
                try:
                    tree.GetEntry(0)
                except AttributeError:
                    _tf.Close()
                    print("Could not get TTree in {}".format(p))
                    return default
                fit = tree.r
                _tf.Close()
                return fit
            else:
                print("Could not find {}".format(p))
                return default
            

        thisFreeAll = baseFreeAll.format(this)
        fitFreeAll.append(get(thisFreeAll))
        thisFreeCC = baseFreeCC.format(this)
        fitFreeCC.append(get(thisFreeCC))
        thisFreeJJ = baseFreeJJ.format(this)
        fitFreeJJ.append(get(thisFreeJJ))
        thisDefault = baseDefault.format(this)
        fitDefault.append(get(thisDefault))

    fitFreeAll = np.array(fitFreeAll)
    fitFreeCC = np.array(fitFreeCC)
    fitFreeJJ = np.array(fitFreeJJ)
    fitDefault = np.array(fitDefault)

    results = {
        "fitDefault": fitDefault,
        "freeAll": fitFreeAll,
        "freeCC": fitFreeCC,
        "freeJJ": fitFreeJJ,
        "default": default
    }

    with open(os.path.join(outp, "results.pkl"), "wb") as _f:
        pickle.dump(results, _f)

    freeAllDef = fitFreeAll != default
    freeCCDef = fitFreeCC != default
    freeJJDef = fitFreeJJ != default
    defaultDef = fitDefault != default
    freeAllDiff = (fitDefault - fitFreeAll)[freeAllDef & defaultDef]
    freeCCDiff = (fitDefault - fitFreeCC)[freeCCDef & defaultDef]
    freeJJDiff = (fitDefault - fitFreeJJ)[freeJJDef & defaultDef]

    fig, axes = plt.subplots(2, 2)
    sns.distplot(fitDefault[defaultDef], ax=axes[0][0], axlabel='default')
    sns.distplot(fitFreeCC[freeCCDef], ax=axes[0][1], axlabel='free cc')
    sns.distplot(fitFreeJJ[freeJJDef], ax=axes[1][0], axlabel='free jj')
    sns.distplot(fitFreeAll[freeAllDef], ax=axes[1][1], axlabel='free all')
    fig.tight_layout()
    fig.savefig("plots_sigma.pdf")
    
    fig, axes = plt.subplots(2, 2)
    sns.distplot(fitDefault[defaultDef], ax=axes[0][0], axlabel='default')
    sns.distplot(freeAllDiff, ax=axes[0][1], axlabel='default - free all')
    sns.distplot(freeCCDiff, ax=axes[1][0], axlabel='default - free cc')
    sns.distplot(freeJJDiff, ax=axes[1][1], axlabel='default - free jj')
    fig.tight_layout()
    fig.savefig("plots_diff.pdf")

    print("Have {} fits to use".format(len(fitDefault)))

    print("Default: mean = {}, RMS = {}".format(np.mean(fitDefault[defaultDef]), np.std(fitDefault[defaultDef])))
    print("Free all: mean = {}, RMS = {}".format(np.mean(fitFreeAll[freeAllDef]), np.std(fitFreeAll[freeAllDef])))
    print("Free cc: mean = {}, RMS = {}".format(np.mean(fitFreeCC[freeCCDef]), np.std(fitFreeCC[freeCCDef])))
    print("Free jj: mean = {}, RMS = {}".format(np.mean(fitFreeJJ[freeJJDef]), np.std(fitFreeJJ[freeJJDef])))
    
    print("Default - free all: mean = {}, RMS = {}".format(np.mean(freeAllDiff), np.std(freeAllDiff)))
    print("Default - free cc: mean = {}, RMS = {}".format(np.mean(freeCCDiff), np.std(freeCCDiff)))
    print("Default - free jj: mean = {}, RMS = {}".format(np.mean(freeJJDiff), np.std(freeJJDiff)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='./', help='input folder')
    parser.add_argument('-o', '--output', default='./', help='output folder')
    parser.add_argument('-n', '--number')

    args = parser.parse_args()

    analyze(args.input, args.output, args.number)
