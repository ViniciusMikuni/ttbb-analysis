#!/usr/bin/env python

import ROOT
from HistogramTools import setTDRStyle
    
setTDRStyle()

ROOT.gROOT.SetBatch(True)

tf = ROOT.TFile.Open("processed_shapes.root")

data = True

if data:
    cr1 = tf.Get("CR1/QCD_subtr")
    cr2 = tf.Get("CR2/QCD_subtr")
    sr = tf.Get("SR/QCD_subtr")
    vr = tf.Get("VR/QCD_subtr")
else:
    cr1 = tf.Get("CR1/QCDMC_CR1")
    cr2 = tf.Get("CR2/QCDMC_CR2")
    sr = tf.Get("SR/QCDMC_SR")
    vr = tf.Get("VR/QCDMC_VR")

sr.Divide(cr1)
vr.Divide(cr2)

# cr1.Divide(sr)
# cr2.Divide(vr)

ks = sr.KolmogorovTest(vr)

c = ROOT.TCanvas()

sr.SetTitle("SR/CR1")
vr.SetTitle("VR/CR2")

sr.GetXaxis().SetTitle("Unrolled 2D CSV bins")
sr.SetLineColor(46)
sr.SetMarkerColor(46)
sr.SetLineWidth(2)
vr.SetLineColor(38)
vr.SetMarkerColor(38)
vr.SetLineWidth(2)
sr.Draw()
sr.GetYaxis().SetRangeUser(0, 1.5)
vr.Draw("same")

if data:
    title = "Ratios of QCD estimates (Data)"
else:
    title = "Ratios of QCD yields (MC)"
text = ROOT.TLatex(0.16, 0.96, title)
text.SetNDC(True)
text.SetTextFont(42)
text.SetTextSize(0.035)
text.Draw("same")

leg = ROOT.TLegend(0.75, 0.8, 0.95, 0.9)
leg.AddEntry(sr)
leg.AddEntry(vr)
leg.SetTextSize(0.04)
leg.SetTextFont(42)
leg.SetFillColor(ROOT.kWhite)
leg.SetBorderSize(0)
leg.Draw()

if data:
    c.Print("qcd_ratios_data.pdf")
    c.Print("qcd_ratios_data.png")
else:
    c.Print("qcd_ratios_mc.pdf")
    c.Print("qcd_ratios_mc.png")

tf.Close()
