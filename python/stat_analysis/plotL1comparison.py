#!/usr/bin/env python

import argparse
import os
import ROOT
from HistogramTools import setTDRStyle, CMS_lumi
from math import sqrt
    
setTDRStyle()

ROOT.gROOT.SetBatch(True)

def plotComparison(proc, reg, histNoL1, histL1, folder):
    c = ROOT.TCanvas("c", "c")

    hi_pad = ROOT.TPad("pad_hi", "", 0., 0.33333, 1, 1)
    hi_pad.Draw()
    hi_pad.SetTopMargin(0.05 / .6666)
    hi_pad.SetLeftMargin(0.16)
    hi_pad.SetBottomMargin(0.015)
    hi_pad.SetRightMargin(0.02)

    lo_pad = ROOT.TPad("pad_lo", "", 0., 0., 1, 0.33333)
    lo_pad.Draw()
    lo_pad.SetTopMargin(1)
    lo_pad.SetLeftMargin(0.16)
    lo_pad.SetBottomMargin(0.13 / 0.33333)
    lo_pad.SetRightMargin(0.02)
    lo_pad.SetTickx(1)

    hi_pad.cd()

    histNoL1.SetLineWidth(2)
    histNoL1.SetLineColor(ROOT.TColor.GetColor('#468966'))
    histNoL1.GetYaxis().SetLabelSize(0.02 / 0.666)
    histNoL1.GetYaxis().SetTitleSize(0.03 / 0.666)
    histNoL1.GetYaxis().SetTitleOffset(1.7 * 0.666)
    histNoL1.GetYaxis().SetTitle("Events")
    histNoL1.GetXaxis().SetLabelSize(0)
    histNoL1.Draw("hist")

    histL1.SetLineWidth(2)
    histL1.SetLineColor(ROOT.TColor.GetColor('#8E2800'))
    histL1.Draw("hist same")

    hist_max = -100
    hist_min = 9999999
    for i in range(1, histNoL1.GetNbinsX() + 1):
        hist_max = max(hist_max, histL1.GetBinContent(i), histNoL1.GetBinContent(i))
        hist_min = min(hist_min, histL1.GetBinContent(i), histNoL1.GetBinContent(i))
    histNoL1.GetYaxis().SetRangeUser(0, hist_max * 1.4)    
    
    lo_pad.cd()
    lo_pad.SetGrid()

    ratio = histNoL1.Clone()
    ratio.Divide(histL1)

    ratio.GetXaxis().SetLabelSize(0.02 / 0.333)
    ratio.GetXaxis().SetTitleSize(0.03 / 0.333)
    ratio.GetXaxis().SetLabelOffset(0.05)
    ratio.GetXaxis().SetTitleOffset(1.5)
    ratio.GetXaxis().SetTitle("Unrolled 2DCSV bin")
    ratio.GetYaxis().SetLabelSize(0.02 / 0.333)
    ratio.GetYaxis().SetTitleSize(0.03 / 0.333)
    ratio.GetYaxis().SetTitleOffset(1.7 * 0.333)
    ratio.GetYaxis().SetTitle("")
    ratio.GetYaxis().SetNdivisions(502, True)
    ratio.GetYaxis().SetRangeUser(1., 1.05)
    # ratio.GetYaxis().SetRangeUser(0.95, 1.05)

    ratio.SetLineColor(ROOT.TColor.GetColor('#468966'))
    ratio.SetMarkerColor(ROOT.TColor.GetColor('#468966'))
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(0.6)
    ratio.Draw("Phist")
    ratio.GetYaxis().SetNdivisions(210)
    ratio.GetYaxis().SetTitle('Ratio')
    
    line = ROOT.TLine(ratio.GetXaxis().GetBinLowEdge(1), 1, ratio.GetXaxis().GetBinUpEdge(ratio.GetXaxis().GetLast()), 1)
    line.Draw("same")

    c.cd()
    l = ROOT.TLegend(0.20, 0.79, 0.50, 0.92)
    l.SetTextFont(42)
    l.SetFillColor(ROOT.kWhite)
    l.SetFillStyle(0)
    l.SetBorderSize(0)

    # l.AddEntry(histL1, "Averaged")
    # l.AddEntry(histNoL1, "Run-dependent")
    l.AddEntry(histL1, "With reweighting")
    l.AddEntry(histNoL1, "Without reweighting")
    l.Draw("same")

    text = reg + ", " + proc
    syst_text = ROOT.TLatex(0.16, 0.96, text)
    syst_text.SetNDC(True)
    syst_text.SetTextFont(42)
    syst_text.SetTextSize(0.03)
    syst_text.Draw("same")


    name = "{}_{}.pdf".format(reg, proc)
    c.SaveAs(os.path.join(folder, name))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Draw systematics')
    parser.add_argument('--inputNoL1', action='store', type=str, help='Input ROOT file without reweighting')
    parser.add_argument('--inputL1', action='store', type=str, help='Input ROOT file with reweighting')
    parser.add_argument('-o', '--output', action='store', type=str, help='Output directory')

    args = parser.parse_args()

    if not os.path.isdir(args.output):
        os.makedirs(args.output)

    procs = ['ttbb', 'ttbb_other', 'ttb_other', 'tt2b',  'ttcc', 'ttlf']
    regions = ['SR', 'VR', 'CR1', 'CR2']
    subFolder = 'fiducial'

    fileNoL1 = ROOT.TFile.Open(args.inputNoL1)
    fileL1 = ROOT.TFile.Open(args.inputL1)

    for proc in procs:
        histNoL1Tot = fileNoL1.Get(os.path.join(subFolder, "SR", proc)).Clone("totNoL1_" + proc)
        histNoL1Tot.Reset()
        histL1Tot = fileL1.Get(os.path.join(subFolder, "SR", proc)).Clone("totL1_" + proc)
        histL1Tot.Reset()

        for reg in regions:
            histNoL1 = fileNoL1.Get(os.path.join(subFolder, reg, proc))
            histNoL1Tot.Add(histNoL1)
            histL1 = fileL1.Get(os.path.join(subFolder, reg, proc))
            histL1Tot.Add(histL1)

            plotComparison(proc, reg, histNoL1, histL1, args.output)
        
        plotComparison(proc, "Total", histNoL1Tot, histL1Tot, args.output)


    fileNoL1.Close()
    fileL1.Close()
