#! /bin/env python

import os, sys, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# to prevent pyroot to hijack argparse we need to go around
tmpargv = sys.argv[:] 
sys.argv = []

# ROOT imports
import ROOT
ROOT.gROOT.SetBatch()
ROOT.PyConfig.IgnoreCommandLineOptions = True
sys.argv = tmpargv

from HistogramTools import setTDRStyle

# For systematics computed with alternate samples, draw statistical uncertainties on ratios
alternateSamples = ['isr', 'fsr', 'tune', 'hdamp']

def beautify(s):
    if s == 'ttbar':
        return r't#bar{t}'
    if s == 'dy':
        return 'Drell-Yan'
    if s == 'SingleTop':
        return 'Single top'
    if s == 'others':
        return 'other backgrounds'
    if s == 'ttV':
        return 't#bar{t}V'
    if s == 'wjets':
        return 'W + jets'
    if s == 'VV':
        return 'VV'
    if s == 'SMHiggs':
        return 'SM Higgs'
    if s == 'ggHH':
        return 'SM HH'

    if s == 'CMS_eff_b':
        return 'Jet b-tagging'
    if s == 'CMS_eff_trigger':
        return 'Trigger efficiency'
    if s == 'CMS_scale_j':
        return 'Jet energy scale'
    if s == 'CMS_res_j':
        return 'Jet energy resolution'
    if s == 'CMS_eff_e':
        return 'Electron ID \\& ISO'
    if s == 'CMS_eff_mu':
        return 'Muon ID'
    if s == 'CMS_iso_mu':
        return 'Muon ISO'
    if s == 'CMS_pu':
        return 'Pileup'
    if s == 'pdf':
        return 'Parton distributions'
    if s == 'lumi_13TeV_2015':
        return 'Luminosity'

    if s == 'ttbar_modeling':
        return r'$\ttbar$ modeling'
    if s == 'ttbar_xsec':
        return r'$\ttbar$ cross-section'
    if s == 'dy_modeling':
        return r'Drell-Yan modeling'
    if s == 'dy_xsec':
        return r'Drell-Yan cross-section'
    if s == 'SingleTop_modeling':
        return r'Single top modeling'
    if s == 'SingleTop_xsec':
        return r'Single top cross-section'

    if s == 'MC_stat':
        return 'MC stat.'

    if 'QCDscale' in s:
        return 'QCD scale'

    return s + '**'

def drawSystematicImpl(nominal, s):

    if s.type() != 'shape':
        return

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

    up = s.shape_u()
    down = s.shape_d()

    up.Scale(nominal.Integral() * s.value_u())
    down.Scale(nominal.Integral() * s.value_d())

    up.SetLineWidth(2)
    up.SetLineColor(ROOT.TColor.GetColor('#468966'))
    up.GetYaxis().SetLabelSize(0.02 / 0.666)
    up.GetYaxis().SetTitleSize(0.03 / 0.666)
    up.GetYaxis().SetTitleOffset(1.7 * 0.666)
    up.GetYaxis().SetTitle("Events")
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
    # up.GetYaxis().SetRangeUser(hist_min * 0.9, hist_max * 1.4)    
    up.GetYaxis().SetRangeUser(0, hist_max * 1.4)    
    
    lo_pad.cd()
    lo_pad.SetGrid()

    up_ratio = up.Clone()
    up_ratio.Divide(nominal)

    ratio_style = "P"
    if s.name().lower() in alternateSamples:
        ratio_style += "E"
    else:
        ratio_style += "hist"

    up_ratio.GetXaxis().SetLabelSize(0.02 / 0.333)
    up_ratio.GetXaxis().SetTitleSize(0.03 / 0.333)
    up_ratio.GetXaxis().SetLabelOffset(0.05)
    up_ratio.GetXaxis().SetTitleOffset(1.5)
    up_ratio.GetXaxis().SetTitle("Unrolled 2DCSV bin")
    up_ratio.GetYaxis().SetLabelSize(0.02 / 0.333)
    up_ratio.GetYaxis().SetTitleSize(0.03 / 0.333)
    up_ratio.GetYaxis().SetTitleOffset(1.7 * 0.333)
    up_ratio.GetYaxis().SetTitle("")
    up_ratio.GetYaxis().SetNdivisions(502, True)
    up_ratio.GetYaxis().SetRangeUser(0.5, 1.5)

    up_ratio.SetLineColor(ROOT.TColor.GetColor('#468966'))
    up_ratio.SetMarkerColor(ROOT.TColor.GetColor('#468966'))
    up_ratio.SetMarkerStyle(20)
    up_ratio.SetMarkerSize(0.6)
    up_ratio.Draw(ratio_style)

    line = ROOT.TLine(up_ratio.GetXaxis().GetBinLowEdge(1), 1, up_ratio.GetXaxis().GetBinUpEdge(up_ratio.GetXaxis().GetLast()), 1)
    line.Draw("same")

    up_ratio.Draw(ratio_style + "same")

    down_ratio = down.Clone()
    down_ratio.Divide(nominal)

    down_ratio.SetLineColor(ROOT.TColor.GetColor('#8E2800'))
    down_ratio.SetMarkerColor(ROOT.TColor.GetColor('#8E2800'))
    down_ratio.SetMarkerStyle(20)
    down_ratio.SetMarkerSize(0.6)
    down_ratio.Draw(ratio_style + "same")

    # Look for min and max of ratio and zoom accordingly
    ratio_max = -100
    ratio_min = 100
    for i in range(1, up_ratio.GetNbinsX() + 1):
        ratio_max = max(ratio_max, up_ratio.GetBinContent(i), down_ratio.GetBinContent(i))
        ratio_min = min(ratio_min, up_ratio.GetBinContent(i), down_ratio.GetBinContent(i))

    def halfRound(r):
        """Round up to closest half-decimal:
            0.04 -> 0.05
            0.009 -> 0.01
        """
        power = 0
        while r < 1:
            r *= 10
            power -= 1
        if r >= 5:
            return pow(10., power+1)
        else:
            return 5. * pow(10., power)


    # Symetrize
    ratio_range = halfRound(max(abs(ratio_max - 1), abs(1 - ratio_min)))
    up_ratio.GetYaxis().SetRangeUser(max(0, 1 - ratio_range), 1 + ratio_range)
    up_ratio.GetYaxis().SetNdivisions(210)
    up_ratio.GetYaxis().SetTitle('Ratio')

    c.cd()
    l = ROOT.TLegend(0.20, 0.79, 0.50, 0.92)
    l.SetTextFont(42)
    l.SetFillColor(ROOT.kWhite)
    l.SetFillStyle(0)
    l.SetBorderSize(0)

    l.AddEntry(nominal, "Nominal")
    l.AddEntry(up, "+1 std. deviation")
    l.AddEntry(down, "-1 std. deviation")
    l.Draw("same")

    text = "%s, %s, systematic: %s" % (s.bin(), s.process(), s.name().lower())
    # text = "%s, systematic: %s" % (beautify(s.process()), beautify(s.name()).lower())
    syst_text = ROOT.TLatex(0.16, 0.96, text)
    syst_text.SetNDC(True)
    syst_text.SetTextFont(42)
    syst_text.SetTextSize(0.03)
    syst_text.Draw("same")


    name = "%s_%s_%s.pdf" % (s.bin(), s.process(), s.name())
    c.SaveAs(os.path.join(options.output, name))

def drawSystematic(nominal):
    def work(s):
        return drawSystematicImpl(nominal, s)
    return work

# Options

parser = argparse.ArgumentParser(description='Draw systematics')
parser.add_argument('-i', '--input', action='store', type=str, help='Input datacard')
parser.add_argument('-o', '--output', action='store', type=str, help='Output directory')

options = parser.parse_args()

if not os.path.isdir(options.output):
    os.makedirs(options.output)

import CombineHarvester.CombineTools.ch as ch

cb = ch.CombineHarvester()
cb.ParseDatacard(options.input)

bins = cb.bin_set()

backgrounds = cb.cp().backgrounds()

# Wanted? FIXME
# backgrounds.FilterSysts(lambda s: 'bin_' in s.name())

processes = backgrounds.process_set()

chosen_bkg_processes = ['ttcc', 'ttlf', 'QCD']

setTDRStyle()

for b in bins:
    for p in processes:
        if p not in chosen_bkg_processes:
            continue
        print("Working on %r process" % p)
        # Select only the process
        c = backgrounds.cp().bin([b]).process([p])
        nominal = c.GetShape()
        c.ForEachSyst(drawSystematic(nominal))

signals = cb.cp().signals()

# Wanted? FIXME
# signals.FilterSysts(lambda s: 'bin_' in s.name())

processes = signals.process_set()

setTDRStyle()

for b in bins:
    for p in processes:
        print("Working on %r process" % p)
        # Select only the process
        c = signals.cp().bin([b]).process([p])
        nominal = c.GetShape()
        c.ForEachSyst(drawSystematic(nominal))
