#!/usr/bin/env python

import ROOT as R

R.gStyle.SetOptStat(0)
R.gStyle.SetOptTitle(0)
R.gROOT.SetBatch(True)

tf = R.TFile.Open("fitDiagnostics.root")
fit = tf.Get("fit_s")
cov = fit.correlationHist()
cov.GetXaxis().SetLabelSize(0.004)
cov.GetYaxis().SetLabelSize(0.004)

c = R.TCanvas("c", "c", 2500, 2500)

cov.Draw("colz")

c.Print("correlation.pdf")

n = cov.GetNbinsX()

cov_list = []

for i in range(1, n+1):
    for j in range(1, n-i+1):
        cov_list.append((cov.GetXaxis().GetBinLabel(i), cov.GetYaxis().GetBinLabel(j), cov.GetBinContent(i, j)))

cov_list.sort(key=lambda i: abs(i[2]), reverse=True)

output = ""
for p1,p2,c in cov_list:
    output += "{:^25} -- {:^25}: {: .3f}\n".format(p1, p2, c)

with open("correlation.txt", "a") as f:
    f.write(output)

tf.Close()


