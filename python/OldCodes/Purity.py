import ROOT as rt
import CMS_lumi, tdrstyle
import array
from math import factorial,sqrt
from maxcomb import maxComb
import numpy as np


rt.gROOT.SetBatch(True)
def Plot(hs_,legtitles_,savename,logy=0,norm =0):
    if len(hs_) != len(legtitles_): print 'number of histograms and legends not matching!'
    #set the tdr style
    tdrstyle.setTDRStyle()
    
    H_ref = 600; 
    W_ref = 800; 
    W = W_ref
    H  = H_ref
    
        
    # references for T, B, L, R
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref
    
    canvas = rt.TCanvas("c2","c2",50,50,W,H)
    canvas.SetLogy(logy)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)
    
    
    xAxis = hs_[0].GetXaxis()
    xAxis.SetNdivisions(6,5,0)
    xAxis.SetTitleSize(0.05)
    yAxis = hs_[0].GetYaxis()
    yAxis.SetNdivisions(6,5,0)
#    yAxis.SetTitleOffset(1.2)
    yAxis.SetTitleSize(0.03)
    if norm: yAxis.SetTitle('Normalized Events')

    
    if norm == 1:
        for i in range(len(hs_)):
            if hs_[i].Integral() != 0: hs_[i].Scale(1./hs_[i].Integral())
    if logy:hs_[0].SetMaximum(10*max(h.GetMaximum() for h in hs_))
    else: hs_[0].SetMaximum(1.3*max(h.GetMaximum() for h in hs_))
#    colorind =['#7fc97f','#beaed4','#fdc086','#ffff99']
#    colorind2 = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d']
    colorind = ['#1de41a','#0000ff','#ff33ff','#286ba6','#b86637','#af4a4d','#a39d4e']
#    colorind2 =    ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f']

#    colorind2 =['#7fc97f','#beaed4','#fdc086','#ffff99','#386cb0','#f0027f','#bf5b17']
#    colorind = ['#e41a1c','#ff7f00','#ffff33','#a65628','#377eb8','#4daf4a','#984ea3']
    legend =  rt.TLegend(0.65,0.70,0.95,0.95)

#    colorind[i]
    for i in range(len(hs_)):
        color = rt.TColor.GetColor(colorind[i])
#        color = rt.TColor.GetColorTransparent(rt.TColor.GetColor(colorind[i]),0.)
        #colorLine = rt.TColor.GetColor(colorind2[i])
        hs_[i].SetFillColor(0)
        hs_[i].SetLineColor(color)
        hs_[i].SetLineWidth(5)
        
        hs_[i].Draw("histsame")
        legend.AddEntry(hs_[i],legtitles_[i],'f')
        
    if len(hs_) < 3: legend.SetTextSize(0.03)        
    canvas.cd()
    canvas.Update()
    canvas.Modified()
    canvas.RedrawAxis()
    legend.Draw()    
    '''
    latex = rt.TLatex()    
    latex.SetTextFont(42)
    latex.SetTextAngle(0)
    latex.SetTextColor(rt.kBlack)    
    latex.SetTextSize(0.05)    
    latex.SetTextAlign(12)
    latex.SetNDC();
    latex.DrawLatex(0.8,0.7,"bjets: "+str(nbjets))
    latex.DrawLatex(0.8,0.65,"jets: "+str(njets))
    

    latex.SetTextSize(0.04)
    latex.DrawLatex(0.13,0.9,"mean: ")
    latex.SetTextColor(rt.kRed+1)
    latex.DrawLatex(0.21,0.9,str(round(h1.GetMean(),2)))
    latex.SetTextColor(rt.kBlue+1)
    latex.DrawLatex(0.30,0.9,str(round(h2.GetMean(),2)))

    latex.SetTextColor(rt.kBlack)    
    latex.DrawLatex(0.13,0.85,"rms: ")
    latex.SetTextColor(rt.kRed+1)
    latex.DrawLatex(0.21,0.85,str(round(h1.GetRMS(),2)))
    latex.SetTextColor(rt.kBlue+1)
    latex.DrawLatex(0.30,0.85,str(round(h2.GetRMS(),2)))
'''
    #update the canvas to draw the legend
    canvas.Update()
    canvas.SaveAs(savename+'.pdf')
#    raw_input("Press Enter to end")


def Plot1(hs,savename,logy=0,norm =0,axistext =[]):

    #set the tdr style
    tdrstyle.setTDRStyle()
    
    H_ref = 600; 
    W_ref = 800; 
    W = W_ref
    H  = H_ref
    
        
    # references for T, B, L, R
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref
    
    canvas = rt.TCanvas("c2","c2",50,50,W,H)
    canvas.SetLogy(logy)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)
    
    
#    xAxis = hs.GetXaxis()
#    xAxis.SetNdivisions(6,5,0)
#    yAxis = hs.GetYaxis()
#    yAxis.SetNdivisions(6,5,0)
#    yAxis.SetTitleOffset(1)
#    if norm: yAxis.SetTitle('Normalized Events')


    if norm == 1:

        if hs.Integral() != 0: hs.Scale(1./hs.Integral())

    colorind = ['#1de41a','#0000ff','#ff33ff','#286ba6','#b86637','#af4a4d','#a39d4e']
    if len(axistext) > 0:
        canvas.SetBottomMargin(0.15)
        for i in range(1,len(axistext)+1):
            print 'bin: ', i, ' entries: ', hs.GetBinContent(i)
            hs.GetXaxis().SetBinLabel(i,axistext[i-1])
        hs.GetYaxis().SetTitle('Events')
        hs.Draw('hist') 

    color = rt.TColor.GetColorTransparent(rt.TColor.GetColor(colorind[1]),1)
    hs.SetMarkerStyle(8)
    hs.SetMarkerColor(color)
    hs.SetMarkerSize(1)
#    hs.SetLineColor(1)
#    hs.SetLineWidth(3)
        
    if len(axistext) == 0:    hs.Draw("p")
    
        
    canvas.cd()
    canvas.Update()
    canvas.Modified()
    canvas.RedrawAxis()
    
    #update the canvas to draw the legend
    canvas.Update()
    canvas.SaveAs(savename+'.png')
#    raw_input("Press Enter to end")







nhists = 4

#f1 = rt.TFile.Open("Kinematic_Results_Unconstrained_1CovMatrix.root","READ")
f = rt.TFile.Open("Kinematic_Results_2011_FH_Unconstrained.root","READ")
t = f.Get("tkin")
fout = rt.TFile.Open("Effs.root","RECREATE")
sigma = 832e3
lumi = 35.8
#BR = 0.457
#77081156
ngenevts = 7.697041e7 
#ngenevts =  f.Get('hCount').GetEntries()
hCut =  f.Get('hPass')
print ngenevts
probcut_ = np.arange(0,1,0.01)



hpass = rt.TH1F("hpass","h; Prob(#chi^{2} cut); Events",len(probcut_)-1,probcut_)
htotal = rt.TH1F("htotal","h; Prob(#chi^{2} cut); Events",len(probcut_)-1,probcut_)
hpure = rt.TH1F("purity","h; Prob(#chi^{2} cut); Purity",len(probcut_)-1,probcut_)
hpure.Sumw2()
heff = rt.TH1F("efficiency","h; Prob(#chi^{2} cut); Efficiency",len(probcut_)-1,probcut_)
heff.Sumw2()
hexp = rt.TH1F("nexp","h; Prob(#chi^{2} cut); Expected number of events",len(probcut_)-1,probcut_)
hexp.Sumw2()
hb = rt.TH1F("hb","h; Prob(#chi^{2} cut); b-jet purity",len(probcut_)-1,probcut_)
hb.Sumw2()

for bin, cut in enumerate(probcut_):
    ntotal = 0
    ntops=0
    ncross =0
    minprobchi2 = 0
    ncorrect = 0
    
    for e,event in enumerate(t) :
        if t.not_Converged: continue
        #or t.n_bjets != 4
        if t.correct_chi2 >= 0 and t.correct_chi2 < t.chi2 :
            minprobchi2 = t.correct_prob_chi2
        else:
            minprobchi2 = t.prob_chi2
        if minprobchi2 < cut: continue
        if t.correct_chi2 >= 0 and t.correct_chi2 < t.chi2 :
            ncorrect +=1
        else:
            if 0 not in t.n_sumIDtop and abs(t.n_sumIDtop[0] + t.n_sumIDtop[1] + t.n_sumIDtop[2]) == 6 and abs(t.n_sumIDtop[3] + t.n_sumIDtop[4] + t.n_sumIDtop[5]) == 6: ncross +=1
            
        ntotal +=1

        if t.n_topjets == 6:        ntops +=1
    if ntotal == 0: continue
    hpass.SetBinContent(bin+1,float(ncorrect))
    htotal.SetBinContent(bin+1,float(ntotal))
    hpure.SetBinContent(bin+1,float(ncorrect)/ntotal)
    hpure.SetBinError(bin+1,sqrt(float(ncorrect))/ntotal*sqrt(1+ncorrect/ntotal))
    heff.SetBinContent(bin+1,float(ntotal)/ngenevts)
    heff.SetBinError(bin+1,sqrt(ntotal)/ngenevts)
    hexp.SetBinContent(bin+1,lumi*sigma*float(ncorrect)/ngenevts)
    hexp.SetBinError(bin+1,lumi*sigma*sqrt(ncorrect)/ngenevts)

epure = rt.TEfficiency(hpass,htotal)
epure.Write()


Plot1(hCut,'nEvts_Constrained',0,0,['vLeptons = 0','6 #geq Jets','4 #geq light jets ','2 #geq b-jets ','m_{top1} cut','m_{top2} cut'])
Plot1(hpure,'purity_Unconstrained')
Plot1(heff,'efficiency_Unconstrained')
Plot1(hexp,'expectedN_Unconstrained')
#Plot1(epure,'purity2_Constrained')
#epure->Draw()
fout.Write()

#fout.Write();
