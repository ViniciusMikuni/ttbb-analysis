#!/usr/bin/env python

# Python imports
import os, sys, argparse, stat
import json

import ROOT
ROOT.gROOT.SetBatch()
ROOT.PyConfig.IgnoreCommandLineOptions = True

import definitions as defs
import utils
import HistogramTools as ht

components = [ c for c in defs.exp_systs if '_j' in c ]

definitions = ["fiducial", "fiducial_parton", "full"]
categs = ["CR1", "CR2", "SR", "VR"]

processes = defs.tt_bkg + defs.sig_processes + defs.other_bkg

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    
    options = parser.parse_args()

    shape_file = ht.openFileAndGet(options.input)

    shapes = {}
    ht.readRecursiveDirContent(shapes, shape_file)

    rates = {}

    for subf in definitions:
        rates.setdefault(subf, {})
        for cat in categs:
            rates[subf].setdefault(cat, {})
            for syst in components:
                rates[subf][cat].setdefault(syst, {})
                for dire in ["Up", "Down"]:
                    rates[subf][cat][syst].setdefault(dire, {})
                    for proc in processes:
                        if proc not in shapes[subf][cat].keys():
                            continue
                        nominal = shapes[subf][cat][proc].Integral()
                        var_name = proc + "_" + syst + dire
                        var = shapes[subf][cat][var_name].Integral()
                        rates[subf][cat][syst][dire][proc] = var / nominal

    shape_file.Close()

    with open(options.output, 'w') as _f:
        json.dump(rates, _f)


