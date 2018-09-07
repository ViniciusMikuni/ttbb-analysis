#Plotting.py
import os
import ROOT as rt
import  tdrstyle
import CMS_lumi
import array
from Plotting_cfg import *
import numpy as np
from math import *

rt.gROOT.SetBatch(True)
rt.gROOT.LoadMacro("../src/triggerWeightRound.h+")
tdrstyle.setTDRStyle()


plot_tree = 1
saveplots = 1
processlist = ['data','ttbar','QCD']

#addCut = 'w1_m < 100 && w1_m > 60 && w2_m < 100 && w2_m > 60 && qgLR > 0.5'
addCut = 'prob_chi2>1e-6'
#cut = ['(top1_pt<100)','(top1_pt>100 && top1_pt<150)','(top1_pt>150 && top1_pt<200)','(top1_pt>200 && top1_pt<300)','(top1_pt>300)']
#cut = ['(genTopHad_pt[0]<100)','(genTopHad_pt[0]>100 && genTopHad_pt[0]<150)','(genTopHad_pt[0]>150 && genTopHad_pt[0]<200)','(genTopHad_pt[0]>200 && genTopHad_pt[0]<300)','(genTopHad_pt[0]>300)']
#cut = ['(abs(top1_eta)<2.4 && abs(top1_eta)>2.2)','(abs(top1_eta)<2.2 && abs(top1_eta)>1.8)','(abs(top1_eta)<1.8 && abs(top1_eta)>1.5)','(abs(top1_eta)<1.5 && abs(top1_eta)>1.0)','(abs(top1_eta)<1.0)']
cut = ['(ttCls==0)','(ttCls<=46 && ttCls>0)','(ttCls ==51)','(ttCls==52)','(ttCls>52)']

#cut = ['exp(-simple_chi2/4) > 0','exp(-simple_chi2/4) > 0.001','exp(-simple_chi2/4) > 0.01','exp(-simple_chi2/4) > 0.05','exp(-simple_chi2/4) > 0.1','exp(-simple_chi2/4) > 0.2']
#cuttext = ['BDT efficiency']
cuttext = ['ttlf','ttcc','ttb','tt2b','ttbb']
#cuttext = ['2.2 < Leading top |#eta| < 2.4','1.8 < Leading top |#eta|  < 2.2','1.5 < Leading top |#eta|  < 1.8','1.5 < Leading top |#eta| < 1.0','Leading top |#eta| < 1.0']
#,'Prob(#chi^{2}) > 0.0001','Prob(#chi^{2}) > 0.01','Prob(#chi^{2}) > 0.05','Prob(#chi^{2}) > 0.1','Prob(#chi^{2}) > 0.2'
#cuttext = ['No cut','P_{gof} > 0.0001','P_{gof} > 0.01','P_{gof} > 0.05','P_{gof} > 0.1','P_{gof} > 0.2']
#cats = ["1","n_bjets == 3 && n_jets == 7","n_bjets == 3 && n_jets == 8","n_bjets >= 4 && n_jets == 8","n_bjets == 3 && n_jets == 9","n_bjets >= 4 && n_jets == 9"]
#shortcats = ["All","3b7j","3b8j","4b8j","3b9j","4b9j"]
cats = ["1","n_jets == 7 ","n_jets == 8","n_jets >= 9"]
shortcats = ["All","7 jets","8 jets","9 jets or more"]
marker_list=[20,21,33,34]

#treeplots = ['chi2','prob_chi2','wkin','catplot']
nostack = {'sigbkg':[], 'eff':[]}
for i in range(len(cut)):
    nostack['sigbkg'].append(rt.TH1F('sigbkg'+str(i),'sigbkg;;Signal/QCD',len(cats),0,len(cats)))
    nostack['eff'].append(rt.TH1F('eff'+str(i),'eff;;Efficiency',len(cats),0,len(cats)))




def singlePlot(h,saveplots):
    rt.gStyle.SetLegendFont(42)
    c = rt.TCanvas('mycv'+h[0].GetName(),'mycv'+h[0].GetName(),5,30,W_ref,H_ref)
    SetupCanvas(c, 0)
    legend = rt.TLegend(x0_l-0.25,y0_l+0.1,x1_l, y1_l )
    #legend.SetTextSize(2)
    h[0].SetMarkerColor(rt.TColor.GetColor(histFillColor[0]))
    h[0].SetMarkerStyle(23)
    h[0].SetMarkerSize(2)
    #h[0].SetMaximum(h[len(h)-1].GetMaximum()*1.5)
    h[0].SetMaximum(1.2)
    h[0].SetMinimum(0)
    for i in range(len(shortcats)): h[0].GetXaxis().SetBinLabel(i+1,shortcats[i])
    # xAxis = h.GetXaxis()
    # xAxis.SetNdivisions(6,5,0)
    yAxis = h[0].GetYaxis()
    yAxis.SetNdivisions(6,5,0)
    yAxis.SetTitleOffset(1)
    yAxis.SetTitleSize(0.05)
    legend.AddEntry(h[0],cuttext[0],'p')
    h[0].Draw('esamex0')
    CMS_lumi.CMS_lumi(c, iPeriod, iPos)
    print 'lumi'
    for i in range(len(h)-1):
        h[i+1].SetMarkerSize(1)
        h[i+1].SetMarkerStyle(marker_list[i])
        h[i+1].SetMarkerColor(rt.TColor.GetColor(histFillColor[i+1]))
        h[1+i].SetMarkerSize(2)
        legend.AddEntry(h[i+1],cuttext[i+1],'p')
        h[i+1].Draw("esamex0")
    c.cd()
    legend.Draw('same')
    c.Update()
    c.RedrawAxis()
    if saveplots:
        if not os.path.exists(destination+ "/"+addCut):
            os.makedirs(destination+ "/"+addCut)
        else:
            print "WARNING: directory already exists. Will overwrite existing files..."
        c.SaveAs(destination+ "/"+addCut+"/"+h[0].GetName()+".pdf")



files = []
hist = 'prob_chi2'
for process in processlist: #ntuple files
    if process in processgroup:
        for subprocess in processgroup[process]:
            files.append(rt.TFile(processfiles[subprocess],"READ"))
    else: files.append(rt.TFile(processfiles[process],"READ"))


for  ncat, cat in enumerate(cats):
    print cat
    ncorr_ = np.zeros(len(cut))
    nttbar_ = np.zeros(len(cut))
    ndata_ =  np.zeros(len(cut))
    nqcd_ =  np.zeros(len(cut))

    for num, process in enumerate(processlist): #for each file
        tvar = files[num].Get('tree')
        for i in range(len(cut)):
            tvar.Draw(hist+">>h"+str(i)+ str(vartitle[hist][1]),"puweight*btagweight*qgweight*topweight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cut[i]+"&&"+cat+"&& hasCorrect)")
            if process == 'data':
                ndata_[i] = rt.gDirectory.Get("h"+str(i)).Integral()

            elif process == 'ttbar':
                nttbar_[i] =rt.gDirectory.Get("h"+str(i)).Integral()
                tvar.Draw(hist+">>hcorr"+str(vartitle[hist][1]),"puweight*btagweight*qgweight*topweight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cut[i]+" && "+cat+ " && isCorrect && hasCorrect)")
                ncorr_[i] =rt.gDirectory.Get("hcorr").Integral()

            elif process == 'QCD':
                tvar.Draw(hist+">>hqcd"+str(i)+ str(vartitle[hist][1]),"weight*trigWeight(ht,jet5pt,n_bjets)*("+addCut+"&&"+cut[i]+"&&"+cat+")")
                nqcd_[i] =rt.gDirectory.Get("hqcd"+str(i)).Integral()


    for i in range(len(cut)):
        nostack['eff'][i].SetBinContent(ncat+1,float(ncorr_[i])/nttbar_[i] if nttbar_[i] > 0 else 0.0 )
        nostack['eff'][i].SetBinError(ncat+1,sqrt(ncorr_[i])/nttbar_[i]if nttbar_[i] > 0 else 0.0)
        scaleqcd = (ndata_[i] - dscale['ttbar']*nttbar_[i])/nqcd_[i] if nqcd_[i] > 0 else 1.0
        print 'scaleqcd ',scaleqcd
        print 'hascorrect: ', nttbar_[0]
        print 'iscorrect: ', ncorr_[0]
        nostack['sigbkg'][i].SetBinContent(ncat+1,dscale['ttbar']*nttbar_[i]/(ndata_[i] - dscale['ttbar']*nttbar_[i]) if (ndata_[i] - dscale['ttbar']*nttbar_[i]) > 0 else 0.0)
        print 'ttbar/qcd', dscale['ttbar']*nttbar_[i]/(ndata_[i] - dscale['ttbar']*nttbar_[i])
        nostack['sigbkg'][i].SetBinError(ncat+1,sqrt(dscale['ttbar']*nttbar_[i])/(ndata_[i] - dscale['ttbar']*nttbar_[i]) if (ndata_[i] - dscale['ttbar']*nttbar_[i]) > 0 else 0.0)


for key in nostack:
    singlePlot(nostack[key],saveplots)
    #raw_input("Press Enter to end")
