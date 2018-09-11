import os, glob, sys, math
from array import array
from utils import *
from ROOT import *
import pandas as pd
import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-N", "--name", action="store", type="string", dest="name", default="28May_ANv5")
parser.add_option("-m", "--mass", action="store", type="string", dest="mass", default="10")
parser.add_option("-f", "--file", action="store", type="string", dest="file", default="tttDM_MChi1_MPhi10_scalar1b2b_ALL")
(options, args) = parser.parse_args()
from array import array
gROOT.SetBatch(True) 


#def getRateParamPlot(bkg, bins,nominal,binsDown,binsUp,nominalErrDown,nominalErrUp):
def getRateParamPlot(bkg, bParams, sbParams):
    
#    grb = TGraphAsymmErrors(len(bins),bins,nominal,binsDown,binsUp,nominalErrDown,nominalErrUp);
    grb = TGraphAsymmErrors(len(bParams[0]),bParams[0], bParams[1], bParams[2], bParams[3], bParams[4],bParams[5])
    grsb = TGraphAsymmErrors(len(sbParams[0]),sbParams[0], sbParams[1], sbParams[2], sbParams[3], sbParams[4], sbParams[5])
    c = TCanvas(bkg,bkg,600,600)
    grb.Draw("AP")
    grsb.Draw("Psame")
    grsb.SetLineColor(kRed)
    grsb.SetMarkerColor(kRed)
    grsb.SetMarkerStyle(20)
    grb.SetMarkerStyle(22)
    grb.SetMinimum(0)
    grb.SetMaximum(2)
    grb.GetXaxis().SetTitle("MET")
    grb.SetTitle("")

    grb.GetYaxis().SetTitle("Post-fit rate parameter")
    grb.GetYaxis().SetTitleOffset(1.1)
    drawCMS('35.9', "Preliminary")
    c.SetTopMargin(0.06)
    c.SetRightMargin(0.05)
    c.SetTicks(1, 1)
    if 'SL' in bkg:
        grb.GetXaxis().SetRangeUser(160,530);
    else:
        grb.GetXaxis().SetRangeUser(250,550);


    legend = TLegend(0.1454849,0.1689895,0.7842809,0.2700348);
    legend.AddEntry(grb, bkg + " rate parameter, b only fit","lp");
    legend.AddEntry(grsb,bkg + " rate paremeter, s+b fit","lp");
    legend.Draw();
    c.SaveAs(bkg+'_rateParamPlots.pdf')
    return 1


if __name__ == "__main__":

    fileName = "combinedCards_"+options.name+"/fitDiagnostics_"+options.file+".root"
    inFile = TFile(fileName, "READ")
    fit_s  = inFile.Get("fit_s")
    fit_b  = inFile.Get("fit_b")

    fpf_b = fit_b.floatParsFinal()
    fpf_s = fit_s.floatParsFinal()

    bkgs = []

    for i in range(fpf_b.getSize()):
        nuis_b = fpf_b.at(i)
        name   = nuis_b.GetName()
        if 'rate' in name:
            bkg = name[0:name.find('_')]
            bkgs.append(bkg)

    bkgs = set(bkgs)
    print bkgs

    for bkg in bkgs:
        bParams =()
        sbParams =()
        bbins,sbbins, binsUp, binsDown = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
        bnominal, bnominalErrUp, bnominalErrDown = array( 'd' ), array( 'd' ), array( 'd' )
        sbnominal, sbnominalErrUp, sbnominalErrDown = array( 'd' ), array( 'd' ), array( 'd' )
        
        for i in range(fpf_b.getSize()):
            nuis_b = fpf_b.at(i)
            name   = nuis_b.GetName()
            nuis_s = fpf_s.find(name)

            if bkg in name:
                print name,'sb', nuis_s.getValV(), nuis_s.getErrorLo(), nuis_s.getErrorHi()
                print name,'b', nuis_b.getValV(), nuis_b.getErrorLo(), nuis_b.getErrorHi()
                bkg = name[0:name.find('_')]
                bin = name[name.find('_')+1:]
                binLow, binHigh = bin.split('_')
                binLow = float(binLow)
                binHigh = float(binHigh)
                print bkg, binHigh
                if binHigh > 5000 and "SL" in bkg:
                    bbins.append(float(binLow+15))
                    sbbins.append(float(binLow+25))
                    print 'here'
                elif binHigh > 5000 and "AH" in bkg:
                    bbins.append(float(binLow+8))
                    sbbins.append(float(binLow+12))
                    print 'here'
                elif "AH" in bkg:
                    bbins.append(float(binLow+(binHigh-binLow)/2-2))
                    sbbins.append(float(binLow+(binHigh-binLow)/2+2))
                else:
                    bbins.append(float(binLow+(binHigh-binLow)/2-5))
                    sbbins.append(float(binLow+(binHigh-binLow)/2+5))

                binsUp.append(0)
                binsDown.append(0)
                bnominal.append(nuis_b.getValV())
                bnominalErrDown.append(abs(nuis_b.getErrorLo()))
                bnominalErrUp.append(abs(nuis_b.getErrorHi()))

                sbnominal.append(nuis_s.getValV())
                sbnominalErrDown.append(abs(nuis_s.getErrorLo()))
                sbnominalErrUp.append(abs(nuis_s.getErrorHi()))
                
                bParams = [bbins, bnominal, binsDown, binsUp, bnominalErrDown, bnominalErrUp]
                sbParams = [sbbins, sbnominal, binsDown, binsUp, sbnominalErrDown, sbnominalErrUp]


        getRateParamPlot(bkg, bParams, sbParams)
