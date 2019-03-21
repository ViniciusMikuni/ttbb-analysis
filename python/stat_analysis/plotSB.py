#!/usr/bin/env python

import ROOT
from HistogramTools import setTDRStyle, CMS_lumi
from math import sqrt
    
setTDRStyle()

ROOT.gROOT.SetBatch(True)

tf = ROOT.TFile.Open("processed_shapes.root")

def plotAll():
    """Plot all four regions S/B on one plot"""

    ratios = {}

    for region in ['SR', 'VR', 'CR1', 'CR2']:
        ttbb = tf.Get(region + "/ttbb")
        ttbb_other = tf.Get(region + "/ttbb_other")
        ttb_other = tf.Get(region + "/ttb_other")
        tt2b = tf.Get(region + "/tt2b")
        ttcc = tf.Get(region + "/ttcc")
        ttlf = tf.Get(region + "/ttlf")
        QCD = tf.Get(region + "/QCD_subtr")

        sig = ttbb.Clone("Signals")
        sig.Add(ttbb_other)
        sig.Add(ttb_other)
        sig.Add(tt2b)

        bkg = QCD.Clone("Backgrounds")
        bkg.Add(ttcc)
        bkg.Add(ttlf)

        ratio = sig.Clone("S/B")
        ratio.Divide(bkg)

        ratios[region] = ratio

    c = ROOT.TCanvas()
    # c.SetLogy(1)

    ratios['SR'].GetXaxis().SetTitle("Unrolled 2DCSV bins")
    ratios['SR'].GetYaxis().SetTitle("S/B")
    ratios['SR'].GetYaxis().SetTitleOffset(1.6)
    ratios['SR'].Draw("hist")
    for reg in ['SR', 'VR', 'CR1', 'CR2']:
        ratios[reg].SetLineWidth(2)

    ratios['SR'].SetLineColor(46)
    ratios['CR1'].SetLineColor(38)
    ratios['VR'].SetLineColor(8)
    ratios['CR2'].SetLineColor(9)
    
    for reg in ['VR', 'CR1', 'CR2']:
        ratios[reg].Draw("histsame")
     
    title = "S/B ratios (S = incl. ttbb, ttbb (OOA), ttb, tt2b)"
    text = ROOT.TLatex(0.3, 0.96, title)
    text.SetNDC(True)
    text.SetTextFont(42)
    text.SetTextSize(0.035)
    text.Draw("same")

    leg = ROOT.TLegend(0.2, 0.65, 0.45, 0.85)
    for reg in ['SR', 'VR', 'CR1', 'CR2']:
        leg.AddEntry(ratios[reg], reg)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.Draw()

    CMS_lumi(c, 0, 1)

    c.Print("sb_ratios.pdf".format(region))

def plot(region):
    """Plot S/B distribution for one region"""

    ttbb = tf.Get(region + "/ttbb")
    ttbb_other = tf.Get(region + "/ttbb_other")
    ttb_other = tf.Get(region + "/ttb_other")
    tt2b = tf.Get(region + "/tt2b")
    ttcc = tf.Get(region + "/ttcc")
    ttlf = tf.Get(region + "/ttlf")
    QCD = tf.Get(region + "/QCD_subtr")

    sig = ttbb.Clone("Signals")
    sig.Add(ttbb_other)
    sig.Add(ttb_other)
    sig.Add(tt2b)

    bkg = QCD.Clone("Backgrounds")
    bkg.Add(ttcc)
    bkg.Add(ttlf)

    ratio = sig.Clone("S/B")
    ratio.Divide(bkg)

    c = ROOT.TCanvas()
    # c.SetLogy(1)

    ratio.GetXaxis().SetTitle("Unrolled 2D CSV bins")
    ratio.GetYaxis().SetTitle("S/B")
    ratio.SetLineColor(46)
    ratio.SetMarkerColor(46)
    ratio.SetLineWidth(2)
    ratio.SetLineColor(38)
    ratio.SetMarkerColor(38)
    ratio.SetLineWidth(2)
    ratio.Draw("hist")
     
    title = "S/B ratios in {} (incl. ttbb, ttbb (OOA), ttb, tt2b)".format(region)
    text = ROOT.TLatex(0.3, 0.96, title)
    text.SetNDC(True)
    text.SetTextFont(42)
    text.SetTextSize(0.035)
    text.Draw("same")

    CMS_lumi(c, 0, 1)

    c.Print("sb_ratios_all_{}.pdf".format(region))


# for r in ['SR', 'VR', 'CR1', 'CR2']:
    # plot(r)
plotAll()

tf.Close()
