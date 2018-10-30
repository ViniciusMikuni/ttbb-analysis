#!/usr/bin/env python

import os

import ROOT
ROOT.gROOT.SetBatch()

from stat_analysis.HistogramTools import setTDRStyle




            


def plotUpDown(up, down, xTitle, title, output):

    c = ROOT.TCanvas("c", "c", 500, 500)

    up.SetLineWidth(2)
    up.SetLineColor(ROOT.TColor.GetColor('#468966'))
    up.GetYaxis().SetTitleOffset(1.7)
    up.GetYaxis().SetTitle("Ratio: nominal over up/down")
    up.GetXaxis().SetTitle(xTitle)
    up.Draw("hist")

    down.SetLineWidth(2)
    down.SetLineColor(ROOT.TColor.GetColor('#8E2800'))
    down.Draw("hist same")
    
    hist_max = -100
    hist_min = 9999999
    for i in range(1, up.GetNbinsX() + 1):
        hist_max = max(hist_max, up.GetBinContent(i), down.GetBinContent(i))
        hist_min = min(hist_min, max(0, up.GetBinContent(i)), max(0, down.GetBinContent(i)))
    up.GetYaxis().SetRangeUser(hist_min * 0.9, hist_max * 1.1)    

    line = ROOT.TLine(up.GetXaxis().GetBinLowEdge(1), 1, up.GetXaxis().GetBinUpEdge(up.GetXaxis().GetLast()), 1)
    line.Draw("same")

    l = ROOT.TLegend(0.20, 0.82, 0.50, 0.92)
    l.SetTextFont(42)
    l.SetFillColor(ROOT.kWhite)
    l.SetFillStyle(0)
    l.SetBorderSize(0)

    l.AddEntry(up, "FSR up")
    l.AddEntry(down, "FSR down")
    l.Draw("same")

    syst_text = ROOT.TLatex(0.16, 0.96, title)
    syst_text.SetNDC(True)
    syst_text.SetTextFont(42)
    syst_text.SetTextSize(0.035)
    syst_text.Draw("same")

    c.SaveAs(output)

def beautifyCSV(hist):
    bins = hist.GetXaxis().GetXbins()
    bins.SetAt(-0.1, 0)

def plotRatios(path, title, quantity, flavs):

    _tf = ROOT.TFile.Open(path)

    for flav in flavs:
        name_up = "ratio_{}_up_{}".format(quantity, flav)
        th3_up = _tf.Get(name_up)
        name_down = "ratio_{}_down_{}".format(quantity, flav)
        th3_down = _tf.Get(name_down)

        xAxis = th3_up.GetXaxis()
        yAxis = th3_up.GetYaxis()

        for x in range(1, th3_up.GetNbinsX()+1):
            for y in range(1, th3_up.GetNbinsY()+1):
                th1_up = th3_up.ProjectionZ(th3_up.GetName() + "__bin_{}_{}".format(x, y), x, x, y, y)
                th1_down = th3_down.ProjectionZ(th3_down.GetName() + "__bin_{}_{}".format(x, y), x, x, y, y)

                pt_min = xAxis.GetBinLowEdge(x)
                pt_max = xAxis.GetBinUpEdge(x)
                eta_min = yAxis.GetBinLowEdge(y)
                eta_max = yAxis.GetBinUpEdge(y)

                if "CSV" in quantity:
                    beautifyCSV(th1_up)
                    beautifyCSV(th1_down)

                m_title = "Flavour: {} / {} < p_{{T}} < {} / {} < |#eta| < {}".format(flav, pt_min, pt_max, eta_min, eta_max)

                output = os.path.join(os.path.dirname(path), "FSR_{}_{}__bin_{}_{}.pdf".format(quantity, flav, x, y))

                plotUpDown(th1_up, th1_down, title, m_title, output)

    _tf.Close()


if __name__ == "__main__":
    setTDRStyle()

    plotRatios("FSR_corrections/csv_fsr_corrections.root", "Jet CSVv2", "jets_btagCSV", ['b', 'c', 'l'])
    plotRatios("FSR_corrections/qgl_fsr_corrections.root", "Jet QGL", "jets_qgl", ['q', 'c', 'b', 'g'])
