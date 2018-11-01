#!/usr/bin/env python

import os
import argparse

import ROOT
ROOT.gROOT.SetBatch()

from stat_analysis.HistogramTools import setTDRStyle

def plotUpDown(nominal, up, down, up_ratio, down_ratio, xTitle, title, syst, output):

    c = ROOT.TCanvas("c", "c")

    hi_pad = ROOT.TPad("pad_hi", "", 0., 0.5, 1, 1)
    hi_pad.Draw()
    hi_pad.SetTopMargin(0.05 / .5)
    hi_pad.SetLeftMargin(0.16)
    hi_pad.SetBottomMargin(0.015)
    hi_pad.SetRightMargin(0.02)

    lo_pad = ROOT.TPad("pad_lo", "", 0., 0., 1, 0.5)
    lo_pad.Draw()
    lo_pad.SetTopMargin(1)
    lo_pad.SetLeftMargin(0.16)
    lo_pad.SetBottomMargin(0.13 / 0.5)
    lo_pad.SetRightMargin(0.02)
    lo_pad.SetTickx(1)

    hi_pad.cd()
    
    up.SetLineWidth(2)
    up.SetLineColor(ROOT.TColor.GetColor('#468966'))
    up.GetYaxis().SetLabelSize(0.02 / 0.5)
    up.GetYaxis().SetTitleSize(0.03 / 0.5)
    up.GetYaxis().SetTitleOffset(1.7 * 0.5)
    up.GetYaxis().SetTitle("Arbitrary units")
    up.GetXaxis().SetLabelSize(0)
    up.Draw("hist")

    nominal.SetLineWidth(2)
    nominal.SetLineStyle(2)
    nominal.SetLineColor(ROOT.TColor.GetColor('#FFB03B'))
    nominal.Draw("hist same")

    up.Draw("hist same")

    down.SetLineWidth(2)
    down.SetLineColor(ROOT.TColor.GetColor('#8E2800'))
    down.Draw("hist same")

    hist_max = -100
    hist_min = 9999999
    for i in range(1, up.GetNbinsX() + 1):
        hist_max = max(hist_max, up.GetBinContent(i), down.GetBinContent(i), nominal.GetBinContent(i))
        hist_min = min(hist_min, up.GetBinContent(i), down.GetBinContent(i), nominal.GetBinContent(i))
    up.GetYaxis().SetRangeUser(hist_min * 0.8, hist_max * 1.4)    
    
    lo_pad.cd()
    lo_pad.SetGrid()

    up_ratio.SetLineWidth(2)
    up_ratio.GetXaxis().SetLabelSize(0.02 / 0.5)
    up_ratio.GetXaxis().SetTitleSize(0.03 / 0.5)
    up_ratio.GetXaxis().SetLabelOffset(0.05)
    up_ratio.GetXaxis().SetTitleOffset(1.5)
    up_ratio.GetXaxis().SetTitle(xTitle)
    up_ratio.GetYaxis().SetLabelSize(0.02 / 0.5)
    up_ratio.GetYaxis().SetTitleSize(0.03 / 0.5)
    up_ratio.GetYaxis().SetTitleOffset(1.7 * 0.5)
    up_ratio.GetYaxis().SetTitle("Ratio nominal over up/down")
    up_ratio.GetYaxis().SetNdivisions(502, True)
    up_ratio.GetYaxis().SetRangeUser(0.5, 1.5)

    up_ratio.SetLineColor(ROOT.TColor.GetColor('#468966'))
    up_ratio.SetMarkerColor(ROOT.TColor.GetColor('#468966'))
    up_ratio.SetMarkerStyle(20)
    up_ratio.SetMarkerSize(0.6)
    up_ratio.Draw("hist")

    line = ROOT.TLine(up_ratio.GetXaxis().GetBinLowEdge(1), 1, up_ratio.GetXaxis().GetBinUpEdge(up_ratio.GetXaxis().GetLast()), 1)
    line.SetLineWidth(2)
    line.Draw("same")

    up_ratio.Draw("histsame")

    down_ratio.SetLineWidth(2)
    down_ratio.SetLineColor(ROOT.TColor.GetColor('#8E2800'))
    down_ratio.SetMarkerColor(ROOT.TColor.GetColor('#8E2800'))
    down_ratio.SetMarkerStyle(20)
    down_ratio.SetMarkerSize(0.6)
    down_ratio.Draw("histsame")

    # Look for min and max of ratio and zoom accordingly
    ratio_max = -100
    ratio_min = 100
    for i in range(1, up_ratio.GetNbinsX() + 1):
        ratio_max = max(ratio_max, up_ratio.GetBinContent(i), down_ratio.GetBinContent(i))
        ratio_min = min(ratio_min, up_ratio.GetBinContent(i), down_ratio.GetBinContent(i))

    # Symetrize
    ratio_range = 1.3 * max(abs(ratio_max - 1), abs(1 - ratio_min))
    up_ratio.GetYaxis().SetRangeUser(max(0, 1 - ratio_range), 1 + ratio_range)
    up_ratio.GetYaxis().SetNdivisions(210)

    c.cd()
    l = ROOT.TLegend(0.20, 0.84, 0.50, 0.94)
    l.SetTextFont(42)
    l.SetFillColor(ROOT.kWhite)
    l.SetFillStyle(0)
    l.SetBorderSize(0)

    l.AddEntry(up, "{} up".format(syst))
    l.AddEntry(down, "{} down".format(syst))
    l.Draw("same")

    syst_text = ROOT.TLatex(0.16, 0.96, title)
    syst_text.SetNDC(True)
    syst_text.SetTextFont(42)
    syst_text.SetTextSize(0.035)
    syst_text.Draw("same")

    c.SaveAs(output)

def beautify(quantity, hist):
    bins = hist.GetXaxis().GetXbins()
    if "csv" in quantity.lower():
        bins.SetAt(-0.1, 0)
    elif "qgl" in quantity.lower():
        bins.SetAt(-0.2, 0)
        bins.SetAt(-0.1, 1)

def plotRatios(syst, path, title, quantity, flavs):

    _tf = ROOT.TFile.Open(path)

    for flav in flavs:
        ratio_th3_up = _tf.Get("ratio_{}_up_{}".format(quantity, flav))
        ratio_th3_down = _tf.Get("ratio_{}_down_{}".format(quantity, flav))

        th3_nominal = _tf.Get("{}_nominal_{}".format(quantity, flav))
        th3_up = _tf.Get("{}_up_{}".format(quantity, flav))
        th3_down = _tf.Get("{}_down_{}".format(quantity, flav))

        xAxis = ratio_th3_up.GetXaxis()
        yAxis = ratio_th3_up.GetYaxis()

        for x in range(1, ratio_th3_up.GetNbinsX()+1):
            for y in range(1, ratio_th3_up.GetNbinsY()+1):
                def getProj(hist3):
                    return hist3.ProjectionZ(hist3.GetName() + "__bin_{}_{}".format(x, y), x, x, y, y)

                th1_nominal = getProj(th3_nominal)
                th1_up = getProj(th3_up)
                th1_down = getProj(th3_down)

                ratio_th1_up = getProj(ratio_th3_up)
                ratio_th1_down = getProj(ratio_th3_down)

                pt_min = xAxis.GetBinLowEdge(x)
                pt_max = xAxis.GetBinUpEdge(x)
                eta_min = yAxis.GetBinLowEdge(y)
                eta_max = yAxis.GetBinUpEdge(y)

                beautify(quantity, th1_nominal)
                beautify(quantity, th1_up)
                beautify(quantity, th1_down)
                beautify(quantity, ratio_th1_up)
                beautify(quantity, ratio_th1_down)

                m_title = "Flavour: {}   /   {} < p_{{T}} < {}   /   {} < |#eta| < {}".format(flav, pt_min, pt_max, eta_min, eta_max)

                output = os.path.join(os.path.dirname(path), "{}_{}_{}__bin_{}_{}.pdf".format(syst.upper(), quantity, flav, x, y))

                plotUpDown(th1_nominal, th1_up, th1_down, ratio_th1_up, ratio_th1_down, title, m_title, syst.upper(), output)

    _tf.Close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--syst', nargs='+', help='Name of the systematics')
    parser.add_argument('--vars', nargs='+', choices=['csv', 'qgl'], help='Variables to plot')
    parser.add_argument('--folder', type=str, help='Folder with the ROOT files')
    options = parser.parse_args()
    
    setTDRStyle()

    for syst in options.syst:

        if 'csv' in options.vars:
            plotRatios(syst, os.path.join(options.folder, "csv_{}_corrections.root".format(syst)), "Jet CSVv2", "jets_btagCSV", ['b', 'c', 'l'])
        if 'qgl' in options.vars:
            plotRatios(syst, os.path.join(options.folder, "qgl_{}_corrections.root".format(syst)), "Jet QGL", "jets_qgl", ['q', 'i', 'l', 'c', 'b', 'g'])
