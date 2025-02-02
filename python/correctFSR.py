#!/usr/bin/env python

import os
import argparse
import numpy as np

import ROOT as R
R.gROOT.SetBatch()

basePath = "root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/vmikuni/tth/"


def get3DHistograms(var, _file, quantity, binning):
    hists = []
    
    chain = R.TChain("tree")
    chain.Add(basePath + _file)

    for bins in binning:
        nBinsX = len(bins["pt"]) - 1
        binsX = np.array(bins["pt"])
        nBinsY = len(bins["eta"]) - 1
        binsY = np.array(bins["eta"])
        nBinsZ = len(bins["discr"]) - 1
        binsZ = np.array(bins["discr"])
        name = "_".join([quantity, var, bins["flav"]])
        htemp = R.TH3D(name, "", nBinsX, binsX, nBinsY, binsY, nBinsZ, binsZ)

        print("Handling {}, file {}, flavour {}...".format(quantity, _file, bins["flav"]))

        chain.Draw(quantity + ":abs(jets_eta):jets_pt>>" + name, bins["cut"], "goff")

        # Normalise along z axis for each x,y bin to get conditional distributions of discriminant value
        proj = htemp.Project3D("yx nuf nof")
        
        for x in range(1, nBinsX+1):
            for y in range(1, nBinsY+1):
                norm = proj.GetBinContent(x, y)
                if norm == 0:
                    print("Warning: projection of {} for {}, flavour {}, pt bin {}, eta bin {}, is zero!".format(quantity, _file, bins["flav"], x, y))
                    continue
                for z in range(1, nBinsZ+1):
                    print("Bin x,y,z={},{},{} -> norm={}, content={}".format(x,y,z,norm, htemp.GetBinContent(x, y, z)))
                    htemp.SetBinContent(x, y, z, htemp.GetBinContent(x, y, z) / norm)
        
        htemp.SetDirectory(0)
        hists.append(htemp)

    return hists

 
def writeRatios(files, quantity, binning, output):

    allHists = { var: get3DHistograms(var, f, quantity, binning) for var, f in files.items() }

    def getRatio(num, den):
        ratio = num.Clone("ratio_" + den.GetName())
        ratio.SetDirectory(0)
        ratio.Divide(den)
        return ratio

    allHists["ratio_down"] = map(getRatio, allHists["nominal"], allHists["down"])
    allHists["ratio_up"] = map(getRatio, allHists["nominal"], allHists["up"])

    outputFile = R.TFile.Open(output, "recreate")

    for hists in allHists.values():
        for hist in hists:
            hist.Write()
            for x in range(1, hist.GetNbinsX()+1):
                for y in range(1, hist.GetNbinsY()+1):
                    hist.ProjectionZ(hist.GetName() + "__bin_{}_{}".format(x, y), x, x, y, y).Write()

    outputFile.Close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--syst', nargs='+', help='Name of the systematic in the files (isr, fsr, ...)')
    parser.add_argument('--output', type=str, help='Output folder (must exist)')
    parser.add_argument('--vars', nargs='+', choices=['csv', 'qgl'], help='Variables to do')
    options = parser.parse_args()

    for syst in options.syst:

        files = {
            "down": "theory/TT_TuneCUETP8M2T4_13TeV-powheg-{}down-pythia8/*.root".format(syst),
            "up": "theory/TT_TuneCUETP8M2T4_13TeV-powheg-{}up-pythia8/*.root".format(syst),
            "nominal": "samples/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/*.root"
        }
        
        ###### CSV ######

        binning_csv = [
                {
                    "flav": "b",
                    "cut": "jets_hadronFlavour==5",
                    "pt": [30., 40., 50., 70., 100., 6500.],
                    "eta": [0., 2.4],
                    "discr": [-15., 0., 0.1356, 0.4069, 0.5731, 0.6342, 0.6954, 0.7566, 0.8178, 0.85895, 0.88, 0.901, 0.922, 0.943, 0.95915, 0.97045, 0.98175, 0.99305, 1.],
                },
                {
                    "flav": "c",
                    "cut": "jets_hadronFlavour==4",
                    "pt": [30., 40., 50., 70., 100., 6500.],
                    "eta": [0., 2.4],
                    "discr": [-15., 0., 0.1356, 0.4069, 0.5731, 0.6342, 0.6954, 0.7566, 0.8178, 0.85895, 0.88, 0.901, 0.922, 0.943, 0.95915, 0.97045, 0.98175, 0.99305, 1.],
                },
                {
                    "flav": "l",
                    "cut": "jets_hadronFlavour==0",
                    "pt": [30., 40., 60., 100., 6500.],
                    "eta": [0., 0.8, 1.6, 2.4],
                    "discr": [-15.] + list(np.linspace(0., 1.0, num=20))
                }
        ]

        if "csv" in options.vars:
            writeRatios(files, "jets_btagCSV", binning_csv, os.path.join(options.output, "csv_{}_corrections.root".format(syst)))
        
        ###### QGL ######
     
        binning_qgl = [
                {
                    "flav": "q",
                    "cut": "abs(jets_mcFlavour)<=5",
                    "pt": [30., 6500.],
                    "eta": [0., 2.4],
                    "discr": [-20., -10.] + list(np.linspace(0., 1., num=25)) + [1.1]
                },
                {
                    "flav": "i",
                    "cut": "jets_mcFlavour == 0",
                    "pt": [30., 6500.],
                    "eta": [0., 2.4],
                    "discr": [-20., -10.] + list(np.linspace(0., 1., num=25)) + [1.1]
                },
                {
                    "flav": "l",
                    "cut": "jets_hadronFlavour == 0",
                    "pt": [30., 6500.],
                    "eta": [0., 2.4],
                    "discr": [-20., -10.] + list(np.linspace(0., 1., num=25)) + [1.1]
                },
                {
                    "flav": "c",
                    "cut": "jets_hadronFlavour==4",
                    "pt": [30., 6500.],
                    "eta": [0., 2.4],
                    "discr": [-20., -10.] + list(np.linspace(0., 1., num=25)) + [1.1]
                },
                {
                    "flav": "b",
                    "cut": "jets_hadronFlavour==5",
                    "pt": [30., 6500.],
                    "eta": [0., 2.4],
                    "discr": [-20., -10.] + list(np.linspace(0., 1., num=25)) + [1.1]
                },
                {
                    "flav": "g",
                    "cut": "jets_mcFlavour==21",
                    "pt": [30., 6500.],
                    "eta": [0., 2.4],
                    "discr": [-20., -10.] + list(np.linspace(0., 1., num=25)) + [1.1]
                },
        ]

        if "qgl" in options.vars:
            writeRatios(files, "jets_qgl", binning_qgl, os.path.join(options.output, "qgl_{}_corrections.root".format(syst)))
