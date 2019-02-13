#!/usr/bin/env python

import ROOT
from HistogramTools import setTDRStyle
from math import sqrt
    
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
    # cr1 = tf.Get("CR1/ttcc")
    # cr2 = tf.Get("CR2/ttcc")
    # sr = tf.Get("SR/ttcc")
    # vr = tf.Get("VR/ttcc")
    cr1 = tf.Get("CR1/QCDMC_CR1")
    cr2 = tf.Get("CR2/QCDMC_CR2")
    sr = tf.Get("SR/QCDMC_SR")
    vr = tf.Get("VR/QCDMC_VR")

# sr.Divide(cr1)
# vr.Divide(cr2)
# vr.Multiply(cr1)
cr1.Divide(cr2)
cr1.Multiply(vr)
vr = cr1

# cr1.Divide(sr)
# cr2.Divide(vr)

# ks = sr.KolmogorovTest(vr)
# ks = sr.Chi2Test(vr, "WW")
# ks = cr2.Chi2Test(vr, "WW")
ks = sr.KolmogorovTest(vr)
print(ks)



nBins = sr.GetNbinsX()
ratios = []
for i in range(1, nBins+2):
    if vr.GetBinContent(i) == 0: continue
    r = sr.GetBinContent(i) / vr.GetBinContent(i)
    w = sqrt((sr.GetBinError(i)/sr.GetBinContent(i))**2 + (vr.GetBinError(i)/vr.GetBinContent(i))**2)
    ratios.append(r)
print(ratios)

c = ROOT.TCanvas()
# c.SetLogy(1)

sr.SetTitle("SR")
vr.SetTitle("VR*CR1/CR2")

sr.GetXaxis().SetTitle("Unrolled 2D CSV bins")
sr.SetLineColor(46)
sr.SetMarkerColor(46)
sr.SetLineWidth(2)
vr.SetLineColor(38)
vr.SetMarkerColor(38)
vr.SetLineWidth(2)
sr.Draw("e1")
sr.GetYaxis().SetRangeUser(0, 1400)
vr.Draw("e1 same")

if data:
    title = "QCD estimates in SR (Data)"
else:
    title = "QCD in SR (MC)"
text = ROOT.TLatex(0.16, 0.96, title)
text.SetNDC(True)
text.SetTextFont(42)
text.SetTextSize(0.035)
text.Draw("same")

leg = ROOT.TLegend(0.65, 0.8, 0.95, 0.9)
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
    # c.Print("ttcc_ratios_mc.pdf")
    # c.Print("ttcc_ratios_mc.png")
    c.Print("qcd_ratios_mc.pdf")
    c.Print("qcd_ratios_mc.png")

tf.Close()
