#!/usr/bin/env python

import ROOT as R

R.gStyle.SetOptStat(0)
R.gStyle.SetOptTitle(0)
R.gROOT.SetBatch(True)

tf = R.TFile.Open("processed_shapes.root")

cr1 = tf.Get("CR1/QCDMC_CR1")
cr2 = tf.Get("CR2/QCD_subtr")
vr = tf.Get("VR/QCD_subtr")
sr = tf.Get("SR/QCDMC_SR")

cr1.Divide(sr)
cr2.Divide(vr)

c = R.TCanvas()

cr1.SetTitle("CR1/SR (MC)")
cr1.GetXaxis().SetTitle("Unrolled 2D CSV bins")
cr1.GetXaxis().SetTitleSize(0.04)
cr1.GetXaxis().SetLabelSize(0.03)
cr1.GetYaxis().SetLabelSize(0.03)
cr2.SetTitle("CR2/VR (data)")
cr1.SetLineColor(46)
cr1.SetMarkerColor(46)
cr2.SetLineColor(38)
cr2.SetMarkerColor(38)
cr1.Draw()
cr2.Draw("same")

R.gPad.SetTitle("Ratios of QCD estimates (data-MC)")
# leg = R.gPad.BuildLegend()
leg = R.TLegend(0.7, 0.8, 0.9, 0.95)
leg.AddEntry(cr1)
leg.AddEntry(cr2)
leg.SetTextSize(0.04)
leg.Draw()

c.Print("qcd_ratios.pdf")
c.Print("qcd_ratios.png")

tf.Close()
