import sys
import ROOT as rt
import CMS_lumi, tdrstyle
import array
from math import factorial,sqrt
from maxcomb import maxComb
import re
rt.gROOT.SetBatch(True)
rt.gROOT.ProcessLine(".L jet_resolutions.C+")
from ROOT import jet_resolutions, TString

def PartHistcreator(name,nhists,m_min,m_max,pt_min,pt_max):
    ''' create a list with nhists for the particle's properties''' 
    part_m_ =[]
    part_pt_ =[]
    part_eta_ =[]
    part_phi_ =[]

    for i in range(nhists):
        part_m_.append(rt.TH1F(name +"_m"+str(i),"h; m(" + name + ")(GeV); Events",50,m_min,m_max))
        part_pt_.append(rt.TH1F(name +"_pt"+str(i),"h; p_{t}(" +name +" )(GeV); Events",50,pt_min,pt_max))
        part_eta_.append(rt.TH1F(name +"_eta"+str(i),"h; #eta(" +name +" ); Events",50,-5,5))
        part_phi_.append(rt.TH1F(name +"_phi"+str(i),"h; #phi(" +name +" ); Events",50,-4,4))
    return part_m_, part_pt_,part_eta_,part_phi_


def Gaussian_resolutions(Et,Eta,Phi):
    return sqrt(0.1*Et),sqrt(0.02*abs(Eta)),sqrt(0.02*abs(Phi))



def ResHist(nhists,name=""):
    ''' create a list with nhists '''
    

    res_et_ =[]
    res_eta_ =[]
    res_phi_ =[]

    for i in range(nhists):
        res_et_.append(rt.TH1F(name+"_et"+str(i),"h; E_{t} [GeV]; #sigma(E_{t})",100,0,500))
        res_eta_.append(rt.TH1F(name+"_eta"+str(i),"h; E_{t} [GeV]; #sigma(#phi)",100,0,500))
        res_phi_.append(rt.TH1F(name+"_phi"+str(i),"h; E_{t} [GeV]; #sigma(#eta)",100,0,500))
    return res_et_,res_eta_,res_phi_

def DiffHistcreator(name,nhists):
    ''' create a list with nhists for the differences with simulation''' 
    part_dm_ =[]
    part_dpt_ =[]
    part_deta_ =[]
    part_dphi_ =[]

    for i in range(nhists):
        part_dm_.append(rt.TH1F(name +"_dm"+str(i),"h; [m(" + name + ") - m("+ name +"_{true})](GeV); Events",50,-500,500))
        part_dpt_.append(rt.TH1F(name +"_dpt"+str(i),"h; [p_{t}(" + name + ") - p_{t}("+ name +"_{true})]; Events",50,-500,500))
        part_deta_.append(rt.TH1F(name +"_deta"+str(i),"h; #eta(" + name + ") - #eta("+ name +"_{true}); Events",50,-6,6))
        part_dphi_.append(rt.TH1F(name +"_dphi"+str(i),"h; #phi(" + name + ") - #phi("+ name +"_{true}); Events",50,-6,6))
    return part_dm_, part_dpt_,part_deta_,part_dphi_

def DiffHistcreatorEt(name,nhists):
    ''' create a list with nhists for the differences with simulation''' 
    part_dm_ =[]
    part_det_ =[]
    part_deta_ =[]
    part_dphi_ =[]
    tsize = 0.03
    for i in range(nhists):
        part_dm_.append(rt.TH1F(name +"_dm"+str(i),"h; [m(" + name + ") - m("+ name +"_{gen})](GeV); Events",50,-0.1,0.1))
        xAxis = part_dm_[i].GetXaxis()
        xAxis.SetTitleSize(tsize)
        part_det_.append(rt.TH1F(name +"_det"+str(i),"h; #frac{[E_{t}(" + name + "_{smeared}) - E_{t}("+ name +"_{fit})]}{#sigma(E_{t})}; Events",50,-3,3))
        xAxis = part_det_[i].GetXaxis()
        xAxis.SetTitleSize(tsize)
        part_deta_.append(rt.TH1F(name +"_deta"+str(i),"h;#frac{[#eta(" + name + "_{smeared}) - #eta("+ name +"_{fit})]}{#sigma(#eta)}; Events",50,-3,3))
        xAxis = part_deta_[i].GetXaxis()
        xAxis.SetTitleSize(tsize)
        part_dphi_.append(rt.TH1F(name +"_dphi"+str(i),"h;#frac{[#phi(" + name + "_{smeared}) - #phi("+ name +"_{fit})]}{#sigma(#phi)}; Events",50,-3,3))
        xAxis = part_dphi_[i].GetXaxis()
        xAxis.SetTitleSize(tsize)
    return part_dm_, part_det_,part_deta_,part_dphi_




def RPhiHistcreator(name,nhists):
    ''' create a list with nhists for the #DeltaR and #DeltaPhi variables''' 
    deltaR_ =[]
    deltaPhi_ =[]
    for i in range(nhists):
        deltaR_.append(rt.TH1F(name +"_deltaR_"+str(i),"h; #Delta_{R}("+name+"); Events",50,0,5))
        deltaPhi_.append(rt.TH1F(name +"_deltaphi_"+str(i),"h; #Delta_{#phi}("+name+"); Events",50,-5,5))
    return deltaR_, deltaPhi_


def chi2Histcreator(nhists):
    ''' create a list with nhists for the chi2 and prob(chi2) variable''' 
    chi2_ =[]
    prob_chi2_ =[]

    for i in range(nhists):chi2_.append(rt.TH1F("tt_chi2_"+str(i),"h; #chi^{2}(tt); Events",50,0,15))
    for i in range(nhists):prob_chi2_.append(rt.TH1F("Prob(chi2)_"+str(i),"h; Prob(#chi^{2}); Events",50,0,1))
    return chi2_,prob_chi2_

def FillMultipleH(hlist_,fill_list_):
    for n, content in enumerate(fill_list_):
        hlist_[n].Fill(content)


def Plot(hs_,legtitles_,savename,logy=0,norm =0,fit = 0):
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
#    xAxis.SetTitleSize(0.05)
    yAxis = hs_[0].GetYaxis()
    yAxis.SetNdivisions(6,5,0)
    yAxis.SetTitleOffset(0.8)
    xAxis.SetTitleOffset(1.5)
    yAxis.SetTitleSize(0.06)
    if norm: yAxis.SetTitle('Normalized Events')

    if fit:
        
        for i in range(len(hs_)):
            hs_[i].Fit('gaus')
    if norm == 1:
        for i in range(len(hs_)):
            if hs_[i].Integral() != 0: hs_[i].Scale(1./hs_[i].Integral())
    if logy:hs_[0].SetMaximum(10*max(h.GetMaximum() for h in hs_))
    else: hs_[0].SetMaximum(1.2*max(h.GetMaximum() for h in hs_))
#    colorind =['#7fc97f','#beaed4','#fdc086','#ffff99']
#    colorind2 = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d']
    colorind = ['#1de41a','#0000ff','#ff33ff','#286ba6','#b86637','#af4a4d','#a39d4e']
#    colorind2 =    ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f']

#    colorind2 =['#7fc97f','#beaed4','#fdc086','#ffff99','#386cb0','#f0027f','#bf5b17']
#    colorind = ['#e41a1c','#ff7f00','#ffff33','#a65628','#377eb8','#4daf4a','#984ea3']
    if len(legtitles_) > 0: legend =  rt.TLegend(0.65,0.85,0.95,0.95)

#    colorind[i]
    for i in range(len(hs_)):
        color = rt.TColor.GetColorTransparent(rt.TColor.GetColor(colorind[i]),0.8)
#        colorLine = rt.TColor.GetColor(colorind2[i])
        hs_[i].SetFillColor(color)
        hs_[i].SetLineColor(1)
        hs_[i].SetLineWidth(3)
        
        hs_[i].Draw("histosame")
        if len(legtitles_) > 0: legend.AddEntry(hs_[i],legtitles_[i],'f')
        
    if len(hs_) < 3 and len(legtitles_) > 0: legend.SetTextSize(0.03)        
    canvas.cd()
    canvas.Update()
    canvas.Modified()
    canvas.RedrawAxis()
    if len(legtitles_) > 0: legend.Draw()    
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
    canvas.SaveAs(savename+'.png')
#    raw_input("Press Enter to end")


def Plot1(hs,savename,logy=0,norm =0):

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
    
    
    xAxis = hs.GetXaxis()
    xAxis.SetNdivisions(6,5,0)
    yAxis = hs.GetYaxis()
    yAxis.SetNdivisions(6,5,0)
    yAxis.SetTitleOffset(.9)
    if norm: yAxis.SetTitle('Normalized Events')

    
    if norm == 1:

        if hs.Integral() != 0: hs.Scale(1./hs.Integral())

    colorind = ['#1de41a','#0000ff','#ff33ff','#286ba6','#b86637','#af4a4d','#a39d4e']

    color = rt.TColor.GetColorTransparent(rt.TColor.GetColor(colorind[1]),0.5)

    hs.SetMarkerColor(color)
    hs.SetMarkerSize(3)
    hs.SetLineColor(1)
    hs.SetLineWidth(3)
        
    hs.Draw("lp")
    
        
    canvas.cd()
    canvas.Update()
    canvas.Modified()
    canvas.RedrawAxis()
    
    #update the canvas to draw the legend
    canvas.Update()
    canvas.SaveAs(savename+'.png')
#    raw_input("Press Enter to end")







nhists = 2

#f1 = rt.TFile.Open("Kinematic_Results_Unconstrained_1CovMatrix.root","READ")
#f1 = rt.TFile.Open("Kinematic_Results_Toy.root","READ")
f2 = rt.TFile.Open("Kinematic_Results_Constrained.root","READ")
#t = f1.Get("tkin")
t2 = f2.Get("tkin")
#fout = rt.TFile('ttbb_comp_jets_'+ str(njets) +'_bjets_'+ str(nbjets) +'.root','recreate')

chi2_,prob_chi2_ = chi2Histcreator(3)

tt_m_,tt_pt_,tt_eta_,tt_phi_ = PartHistcreator('tt',nhists,250,1200,0,500)
top1_m_,top1_pt_,top1_eta_,top1_phi_ = PartHistcreator('top1',nhists,100,300,0,500)
top2_m_,top2_pt_,top2_eta_,top2_phi_ = PartHistcreator('top2',nhists,100,300,0,500)
w1_m_,w1_pt_,w1_eta_,w1_phi_ = PartHistcreator('w1',nhists,50,110,0,500)
w2_m_,w2_pt_,w2_eta_,w2_phi_ = PartHistcreator('w2',nhists,50,110,0,500)
b1_m_,b1_pt_,b1_eta_,b1_phi_ = PartHistcreator('b1',nhists,0,10,0,500)
b2_m_,b2_pt_,b2_eta_,b2_phi_ = PartHistcreator('b2',nhists,0,10,0,500)

delta_tt_m_,delta_tt_pt_,delta_tt_eta_,delta_tt_phi_ = DiffHistcreator('tt',nhists)
delta_top1_m_,delta_top1_pt_,delta_top1_eta_,delta_top1_phi_ = DiffHistcreator('top1',nhists)
delta_top2_m_,delta_top2_pt_,delta_top2_eta_,delta_top2_phi_ = DiffHistcreator('top2',nhists)

delta_b1_m_,delta_b1_et_,delta_b1_eta_,delta_b1_phi_ = DiffHistcreatorEt('b1',1)
delta_b2_m_,delta_b2_et_,delta_b2_eta_,delta_b2_phi_ = DiffHistcreatorEt('b2',1)


ntotal =0
ncorrect =  0
for e,event in enumerate(t) :
    #if t.ttMC_m == -10: continue
    if t.not_Converged: continue



    
    ntotal +=1
    chi2_[0].Fill(t.chi2)
    prob_chi2_[0].Fill(t.prob_chi2)

    chi2_[1].Fill(t.correct_chi2)
    prob_chi2_[1].Fill(t.correct_prob_chi2)

    if t.chi2 < t.correct_chi2:
        chi2_[2].Fill(t.chi2)
        prob_chi2_[2].Fill(t.prob_chi2)
    else:
        ncorrect +=1
        chi2_[2].Fill(t.correct_chi2)
        prob_chi2_[2].Fill(t.correct_prob_chi2)
        
    FillMultipleH(tt_m_,[t.tt_m,t.gen_tt_m ])
    FillMultipleH(tt_pt_,[t.tt_pt,t.gen_tt_pt ])
    FillMultipleH(tt_eta_,[t.tt_eta,t.gen_tt_eta ])
    FillMultipleH(tt_phi_,[t.tt_phi,t.gen_tt_phi ])

    FillMultipleH(top1_m_,[t.top1_m,t.gen_top1_m ])
    FillMultipleH(top1_pt_,[t.top1_pt,t.gen_top1_pt ])
    FillMultipleH(top1_eta_,[t.top1_eta,t.gen_top1_eta ])
    FillMultipleH(top1_phi_,[t.top1_phi,t.gen_top1_phi ])

    FillMultipleH(top2_m_,[t.top2_m,t.gen_top2_m ])
    FillMultipleH(top2_pt_,[t.top2_pt,t.gen_top2_pt ])
    FillMultipleH(top2_eta_,[t.top2_eta,t.gen_top2_eta ])
    FillMultipleH(top2_phi_,[t.top2_phi,t.gen_top2_phi ])

    FillMultipleH(b2_m_,[t.b2_m,t.gen_b2_m ])
    FillMultipleH(b2_pt_,[t.b2_pt,t.gen_b2_pt ])
    FillMultipleH(b2_eta_,[t.b2_eta,t.gen_b2_eta ])
    FillMultipleH(b2_phi_,[t.b2_phi,t.gen_b2_phi ])

    FillMultipleH(b1_m_,[t.b1_m,t.gen_b1_m ])
    FillMultipleH(b1_pt_,[t.b1_pt,t.gen_b1_pt ])
    FillMultipleH(b1_eta_,[t.b1_eta,t.gen_b1_eta ])
    FillMultipleH(b1_phi_,[t.b1_phi,t.gen_b1_phi ])

    FillMultipleH(w1_m_,[t.w1_m,t.gen_w1_m ])
    FillMultipleH(w1_pt_,[t.w1_pt,t.gen_w1_pt ])
    FillMultipleH(w1_eta_,[t.w1_eta,t.gen_w1_eta ])
    FillMultipleH(w1_phi_,[t.w1_phi,t.gen_w1_phi ])

    FillMultipleH(w2_m_,[t.w2_m,t.gen_w2_m ])
    FillMultipleH(w2_pt_,[t.w2_pt,t.gen_w2_pt ])
    FillMultipleH(w2_eta_,[t.w2_eta,t.gen_w2_eta ])
    FillMultipleH(w2_phi_,[t.w2_phi,t.gen_w2_phi ])


    
    FillMultipleH(delta_tt_m_,[t.tt_m - t.ttMC_m,t.gen_tt_m - t.ttMC_m])
    FillMultipleH(delta_tt_pt_,[t.tt_pt - t.ttMC_pt,t.gen_tt_pt - t.ttMC_pt])
    FillMultipleH(delta_tt_eta_,[t.tt_eta - t.ttMC_eta,t.gen_tt_eta - t.ttMC_eta])
    FillMultipleH(delta_tt_phi_,[t.tt_phi - t.ttMC_phi,t.gen_tt_phi - t.ttMC_phi])

    FillMultipleH(delta_top2_m_,[t.top2_m - t.top2MC_m,t.gen_top2_m - t.top2MC_m])
    FillMultipleH(delta_top2_pt_,[t.top2_pt - t.top2MC_pt,t.gen_top2_pt - t.top2MC_pt])
    FillMultipleH(delta_top2_eta_,[t.top2_eta - t.top2MC_eta,t.gen_top2_eta - t.top2MC_eta])
    FillMultipleH(delta_top2_phi_,[t.top2_phi - t.top2MC_phi,t.gen_top2_phi - t.top2MC_phi])

    FillMultipleH(delta_top1_m_,[t.top1_m - t.top1MC_m,t.gen_top1_m - t.top1MC_m])
    FillMultipleH(delta_top1_pt_,[t.top1_pt - t.top1MC_pt,t.gen_top1_pt - t.top1MC_pt])
    FillMultipleH(delta_top1_eta_,[t.top1_eta - t.top1MC_eta,t.gen_top1_eta - t.top1MC_eta])
    FillMultipleH(delta_top1_phi_,[t.top1_phi - t.top1MC_phi,t.gen_top1_phi - t.top1MC_phi])


#    FillMultipleH(delta_b1_m_,[t.smear_b1_m - t.gen_b1_m])
#    res_ = jet_resolutions(t.gen_b1_et,t.gen_b1_eta,t.gen_b1_phi,'b')
#    FillMultipleH(delta_b1_et_,[(t.smear_b1_et - t.gen_b1_et)/sqrt(res_[0])])
#    FillMultipleH(delta_b1_eta_,[(t.smear_b1_eta - t.gen_b1_eta)/sqrt(res_[1])])
#    FillMultipleH(delta_b1_phi_,[(t.smear_b1_phi - t.gen_b1_phi)/sqrt(res_[2])])

#    FillMultipleH(delta_b2_m_,[t.smear_b2_m - t.gen_b2_m])
#    FillMultipleH(delta_b2_et_,[(t.smear_b2_et - t.gen_b2_et)/sqrt(0.1*t.gen_b2_et)])
#    FillMultipleH(delta_b2_eta_,[(t.smear_b2_eta - t.gen_b2_eta)/sqrt(0.02*abs(t.gen_b2_eta))])
#    FillMultipleH(delta_b2_phi_,[(t.smear_b2_phi - t.gen_b2_phi)/sqrt(0.02*abs(t.gen_b2_phi))])

'''

    FillMultipleH(delta_b1_m_,[t.smear_b1_m - t.fit_b1_m])
    FillMultipleH(delta_b1_et_,[(t.smear_b1_et - t.fit_b1_et)/sqrt(0.1*t.fit_b1_et)])
    FillMultipleH(delta_b1_eta_,[(t.smear_b1_eta - t.fit_b1_eta)/sqrt(0.02*abs(t.fit_b1_eta))])
    FillMultipleH(delta_b1_phi_,[(t.smear_b1_phi - t.fit_b1_phi)/sqrt(0.02*abs(t.fit_b1_phi))])

    FillMultipleH(delta_b2_m_,[t.smear_b2_m - t.fit_b2_m])
    FillMultipleH(delta_b2_et_,[(t.smear_b2_et - t.fit_b2_et)/sqrt(0.1*t.fit_b2_et)])
    FillMultipleH(delta_b2_eta_,[(t.smear_b2_eta - t.fit_b2_eta)/sqrt(0.02*abs(t.fit_b2_eta))])
    FillMultipleH(delta_b2_phi_,[(t.smear_b2_phi - t.fit_b2_phi)/sqrt(0.02*abs(t.fit_b2_phi))])
'''



legFit_ = ['Wrong combination','Correct combination']



Plot(chi2_[:2],['Wrong Combination','Correct Combination'],'chi2')
Plot([chi2_[2]],['Lowest #chi^{2}'],'chi2_small')
Plot([prob_chi2_[1]],['Correct Combination'],'prob_chi2_corr')
Plot([prob_chi2_[2]],['Lowest #chi^{2}'],'prob_chi2_small')
Plot(prob_chi2_[:2],['Wrong Combination','Correct Combination'],'prob_chi2')

Plot(chi2_[1:],['Correct Combination','Lowest #chi^{2}'],'chi2_small_corr')
Plot(prob_chi2_[1:],['Correct Combination','Lowest #chi^{2}'],'prob_chi2_small_corr')


Plot(top1_m_,legFit_,'top1_m')
Plot(top1_pt_,legFit_,'top1_pt')
Plot(top1_eta_,legFit_,'top1_eta')
Plot(top1_phi_,legFit_,'top1_phi')

Plot(b1_m_,legFit_,'b1_m')
Plot(b1_pt_,legFit_,'b1_pt')
Plot(b1_eta_,legFit_,'b1_eta')
Plot(b1_phi_,legFit_,'b1_phi')

Plot(b2_m_,legFit_,'b2_m')
Plot(b2_pt_,legFit_,'b2_pt')
Plot(b2_eta_,legFit_,'b2_eta')
Plot(b2_phi_,legFit_,'b2_phi')

Plot(w1_m_,legFit_,'w1_m',1)
Plot(w1_pt_,legFit_,'w1_pt')
Plot(w1_eta_,legFit_,'w1_eta')
Plot(w1_phi_,legFit_,'w1_phi')

Plot(w2_m_,legFit_,'w2_m',1)
Plot(w2_pt_,legFit_,'w2_pt')
Plot(w2_eta_,legFit_,'w2_eta')
Plot(w2_phi_,legFit_,'w2_phi')


Plot(top2_m_,legFit_,'top2_m')
Plot(top2_pt_,legFit_,'top2_pt')
Plot(top2_eta_,legFit_,'top2_eta')
Plot(top2_phi_,legFit_,'top2_phi')


Plot(tt_m_,legFit_,'tt_m')
Plot(tt_pt_,legFit_,'tt_pt')
Plot(tt_eta_,legFit_,'tt_eta')
Plot(tt_phi_,legFit_,'tt_phi')


Plot(delta_tt_m_,legFit_,'delta_tt_m')
Plot(delta_tt_pt_,legFit_,'delta_tt_pt')
Plot(delta_tt_eta_,legFit_,'delta_tt_eta')
Plot(delta_tt_phi_,legFit_,'delta_tt_phi')

Plot(delta_top1_m_,legFit_,'delta_top1_m')
Plot(delta_top1_pt_,legFit_,'delta_top1_pt')
Plot(delta_top1_eta_,legFit_,'delta_top1_eta')
Plot(delta_top1_phi_,legFit_,'delta_top1_phi')

Plot(delta_top2_m_,legFit_,'delta_top2_m')
Plot(delta_top2_pt_,legFit_,'delta_top2_pt')
Plot(delta_top2_eta_,legFit_,'delta_top2_eta')
Plot(delta_top2_phi_,legFit_,'delta_top2_phi')

Plot(delta_b1_m_,[],'delta_b1_m')
Plot(delta_b1_et_,[],'delta_b1_et',0,0,1)
Plot(delta_b1_eta_,[],'delta_b1_eta',0,0,1)
Plot(delta_b1_phi_,[],'delta_b1_phi',0,0,1)

Plot(delta_b2_m_,[],'delta_b2_m')
Plot(delta_b2_et_,[],'delta_b2_et',0,0,1)
Plot(delta_b2_eta_,[],'delta_b2_eta',0,0,1)
Plot(delta_b2_phi_,[],'delta_b2_phi',0,0,1)
print 'Correct combination found ',float(ncorrect)/ntotal, '% of the time'

'''
Res_leg_ = ['0.000 < #eta < 0.087','1.218 < #eta < 1.305','2.322 < #eta < 2.500']
hEt_,hPhi_, hEta_ =  ResHist(3)
hbEt_,hbPhi_, hbEta_ =  ResHist(3,'b')
hgEt = rt.TH1F("g_et","h; E_{t} [GeV]; #sigma(E_{t})",100,0,500)
hgEta = rt.TH1F("g_eta","h; #eta; #sigma(#eta)",100,-2.4,2.4)
hgPhi =  rt.TH1F("_phi","h; #phi; #sigma(#phi)",100,-3.14,3.14)
eta_val_ = [0.08,1.23 ,2.4]




center_ = []
for i in range(1,101):
    xcenter = hEt_[0].GetBinCenter(i)
    center_.append(hgEt.GetBinCenter(i))
    center_.append(hgEta.GetBinCenter(i))
    center_.append(hgPhi.GetBinCenter(i))
    for j in range(3):
        resg_ = Gaussian_resolutions(center_[0],center_[1],center_[2])
        res_ = jet_resolutions(xcenter,eta_val_[j],0,"udsc")
        hgEt.SetBinContent(i,resg_[0])
        hgEta.SetBinContent(i,resg_[1])
        hgPhi.SetBinContent(i,resg_[2])

        hEt_[j].SetBinContent(i,res_[0])
        hEta_[j].SetBinContent(i,res_[1])
        hPhi_[j].SetBinContent(i,res_[2])


        resb_ = jet_resolutions(xcenter,eta_val_[j],0,"b")
#        print resb_[0], '    ', res_[0] 
        hbEt_[j].SetBinContent(i,resb_[0])
        hbEta_[j].SetBinContent(i,resb_[1])
        hbPhi_[j].SetBinContent(i,resb_[2])
    center_ = []
Plot1(hgEt, 'gEt_resolution')
Plot1(hgEta,'gEta_resolution')
Plot1(hgPhi,'gPhi_resolution')

Plot(hEt_, Res_leg_,'Et_resolution')
Plot(hEta_, Res_leg_,'Eta_resolution')
Plot(hPhi_, Res_leg_,'Phi_resolution')
Plot(hbEt_, Res_leg_,'Et_resolutionB')
Plot(hbEta_, Res_leg_,'Eta_resolutionB')
Plot(hbPhi_, Res_leg_,'Phi_resolutionB')
#fout.Write();
'''
