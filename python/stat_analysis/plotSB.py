#!/usr/bin/env python

import ROOT
from HistogramTools import setTDRStyle, CMS_lumi
from math import sqrt
    
tdrStyle = setTDRStyle()

tdrStyle.SetCanvasDefH(600) #Height of canvas
tdrStyle.SetCanvasDefW(540) #Width of canvas
tdrStyle.SetTitleSize(1, "XYZ")
tdrStyle.SetLabelSize(0.1, "XYZ")
tdrStyle.cd()


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
        # ttcc = tf.Get(region + "/ttcc")
        # ttlf = tf.Get(region + "/ttlf")
        # QCD = tf.Get(region + "/QCD_subtr")
        data = tf.Get(region + "/data_obs")

        sig = ttbb.Clone("Signals")
        sig.Add(ttbb_other)
        sig.Add(ttb_other)
        sig.Add(tt2b)

        # bkg = QCD.Clone("Backgrounds")
        # bkg.Add(ttcc)
        # bkg.Add(ttlf)
        bkg = data.Clone("Backgrounds")
        bkg.Add(sig, -1)

        ratio = sig.Clone("S/B")
        ratio.Divide(bkg)

        ratios[region] = ratio

        print("Region: {}".format(region))
        for proc in "ttbb", "ttbb_other", "ttb_other", "tt2b", "ttcc", "ttlf", "QCD_subtr", "VV", "VJ", "ttV", "ttH", "stop", "data_obs":
            print("{}: {}".format(proc, tf.Get(region + "/" + proc).GetBinContent(32)))

    c = ROOT.TCanvas()
    # c.SetLogy(1)

    ratios['SR'].GetXaxis().SetTitle("2DCSV bin")
    ratios['SR'].GetYaxis().SetTitle("S/B")
    ratios['SR'].GetYaxis().SetTitleOffset(1.4)
    ratios['SR'].Draw("hist")
    for reg in ['SR', 'VR', 'CR1', 'CR2']:
        ratios[reg].SetLineWidth(2)

    ratios['SR'].GetXaxis().SetTitleSize(0.045)
    ratios['SR'].GetXaxis().SetLabelSize(0.045)
    ratios['SR'].GetYaxis().SetTitleSize(0.045)
    ratios['SR'].GetYaxis().SetLabelSize(0.045)

    ratios['SR'].SetLineColor(46)
    ratios['CR1'].SetLineColor(38)
    ratios['VR'].SetLineColor(8)
    ratios['CR2'].SetLineColor(9)
    
    for reg in ['VR', 'CR1', 'CR2']:
        ratios[reg].Draw("histsame")
     
    title = "S/B ratios" # (S = incl. ttbb, ttbb (OOA), ttb, tt2b)"
    text = ROOT.TLatex(0.3, 0.96, title)
    text.SetNDC(True)
    text.SetTextFont(42)
    text.SetTextSize(0.035)
    # text.Draw("same")

    leg = ROOT.TLegend(0.2, 0.6, 0.45, 0.8)
    for reg in ['SR', 'CR1', 'CR2', 'VR']:
        if reg == 'VR':
            regN = 'CR3'
        else:
            regN = reg
        leg.AddEntry(ratios[reg], regN)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.Draw()

    # CMS_lumi(c, 4, 10, extraText="Preliminary")
    CMS_lumi(c, 4, 10, extraText="Supplementary")

    c.Print("sb_ratios_new.pdf".format(region))

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
