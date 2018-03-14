import ROOT as rt
import CMS_lumi, tdrstyle
import array
from math import factorial

rt.gROOT.SetBatch(True)

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

def DiffHistcreator(name,nhists):
    ''' create a list with nhists for the differences with simulation''' 
    part_dm_ =[]
    part_dpt_ =[]
    part_deta_ =[]
    part_dphi_ =[]

    for i in range(nhists):
        part_dm_.append(rt.TH1F(name +"_dm"+str(i),"h; [m(" + name + ") - m("+ name +"_{true})](GeV); Events",50,-500,500))
        part_dpt_.append(rt.TH1F(name +"_dpt"+str(i),"h; [p_{t}(" + name + ") - p_{t}("+ name +"_{true})](GeV); Events",50,-500,500))
        part_deta_.append(rt.TH1F(name +"_deta"+str(i),"h; #eta(" + name + ") - #eta("+ name +"_{true}); Events",50,-6,6))
        part_dphi_.append(rt.TH1F(name +"_dphi"+str(i),"h; #phi(" + name + ") - #phi("+ name +"_{true}); Events",50,-6,6))
    return part_dm_, part_dpt_,part_deta_,part_dphi_




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
    if logy:
        hs_[0].SetMaximum(10*max(h.GetMaximum() for h in hs_))
        hs_[0].SetMinimum(1*min(h.GetMinimum() for h in hs_))
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
    yAxis.SetTitleOffset(1)
    if norm: yAxis.SetTitle('Normalized Events')

    
    if norm == 1:

        if hs.Integral() != 0: hs.Scale(1./hs.Integral())

    colorind = ['#1de41a','#0000ff','#ff33ff','#286ba6','#b86637','#af4a4d','#a39d4e']

    color = rt.TColor.GetColorTransparent(rt.TColor.GetColor(colorind[1]),0.5)

    hs.SetMarkerColor(color)
    hs.SetMarkerSize(3)
    hs.SetLineColor(1)
    hs.SetLineWidth(3)
        
    hs.Draw("pl")
    
        
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
#f1 = rt.TFile.Open("Kinematic_Results_2011.root","READ")
f1 = rt.TFile.Open("Datasets/Kinematic_Results_2011_FH_Unconstrained_Ttbar.root","READ")
t = f1.Get("tkin")
#fout = rt.TFile('ttbb_comp_jets_'+ str(njets) +'_bjets_'+ str(nbjets) +'.root','recreate')

chi2_,prob_chi2_ = chi2Histcreator(3)

tt_m_,tt_pt_,tt_eta_,tt_phi_ = PartHistcreator('tt',nhists,250,1200,0,500)
#tt_mcomb_= PartHistcreator('comb_tt',7,250,1200,0,500)[0]
top1_m_,top1_pt_,top1_eta_,top1_phi_ = PartHistcreator('top1',nhists,50,400,0,500)
top2_m_,top2_pt_,top2_eta_,top2_phi_ = PartHistcreator('top2',nhists,50,400,0,500)

delta_tt_m_,delta_tt_pt_,delta_tt_eta_,delta_tt_phi_ = DiffHistcreator('tt',nhists)



ncorrect = 0
ntotal = 0
ntops=0
ncross =0
n2mix = 0
n2mix2b = 0
n2mix1b = 0
n2mix0b =0
n1mix =0
n1mix1b =0
n1mix0b = 0
nmissedtag =0
for e,event in enumerate(t) :
    if t.not_Converged or t.n_jets !=6 : continue
    #or t.n_jets !=6
    #or t.n_bjets !=4 or  t.n_jets !=8
    ntotal +=1
    if t.correct_chi2 >= 0:        ntops +=1
    if t.correct_chi2 < 0 and t.n_topjets ==6 :        nmissedtag+=1

#    for m in t.comb_masses:
#        if t.n_jets < 12: tt_mcomb_[t.n_jets -6].Fill(m)


#    if not t.no_Wrong:
#        for i, prob in enumerate(t.all_prob_chi2):
#            if t.n_jets < 12:
#                chi2_[0].Fill(t.all_chi2[i])
#                prob_chi2_[0].Fill(prob)
        
    chi2_[0].Fill(t.chi2)
    prob_chi2_[0].Fill(t.prob_chi2)
    if t.correct_chi2 >= 0:
        chi2_[1].Fill(t.correct_chi2)
        prob_chi2_[1].Fill(t.correct_prob_chi2)
        

    if t.correct_chi2 >= 0:
        if t.correct_chi2 <  t.chi2:
            ncorrect +=1
            chi2_[2].Fill(t.correct_chi2)
            prob_chi2_[2].Fill(t.correct_prob_chi2)
            
        # else :                  
        #     if abs(t.addB_TopMCmatch[0]) == 6 or  abs(t.addB_TopMCmatch[1]) == 6:
        #         if abs(t.addB_TopMCmatch[0]) == 6 and  abs(t.addB_TopMCmatch[1]) == 6:
        #             n2mix +=1
        #             if abs(t.addB_MCid[0]) == 5 or abs(t.addB_MCid[1]) == 5:
        #                 if abs(t.addB_MCid[0]) == 5 and abs(t.addB_MCid[1]) == 5: n2mix2b +=1
        #                 else: n2mix1b +=1
        #             else: n2mix0b +=1
        #         else:
        #             n1mix +=1
        #             if abs(t.addB_TopMCmatch[0]) == 6:
        #                 if abs(t.addB_MCid[0]) == 5: n1mix1b +=1
        #                 else: n1mix0b +=1
        #             else:
        #                 if abs(t.addB_MCid[1]) == 5: n1mix1b +=1
        #                 else: n1mix0b +=1

                
        if 0 not in t.n_sumIDtop and abs(t.n_sumIDtop[0] + t.n_sumIDtop[1] + t.n_sumIDtop[2]) == 6 and abs(t.n_sumIDtop[3] + t.n_sumIDtop[4] + t.n_sumIDtop[5]) == 6: ncross +=1
        chi2_[2].Fill(t.chi2)
        prob_chi2_[2].Fill(t.prob_chi2)

#    if t.n_topjets != 6: continue
    #FillMultipleH(chi2_,[t.chi2,t.correct_chi2])
    #FillMultipleH(prob_chi2_,[t.prob_chi2,t.correct_prob_chi2])
#    if t.no_Correct or t.no_Wrong  : continue
#    if t.correct_chi2 < 0: continue
    # FillMultipleH(tt_m_,[t.tt_m,t.fitted_tt_m,t.correct_tt_m,t.correct_fitted_tt_m ])
    # FillMultipleH(tt_pt_,[t.tt_pt,t.fitted_tt_pt,t.correct_tt_pt,t.correct_fitted_tt_pt ])
    # FillMultipleH(tt_phi_,[t.tt_phi,t.fitted_tt_phi,t.correct_tt_phi,t.correct_fitted_tt_phi ])
    # FillMultipleH(tt_eta_,[t.tt_eta,t.fitted_tt_eta,t.correct_tt_eta,t.correct_fitted_tt_eta ])
#    if abs(t.n_sumIDtop1) == 18 and abs(t.n_sumIDtop2) == 18:
    # FillMultipleH(top1_m_,[t.top1_m,t.fitted_top1_m,t.correct_top1_m,t.correct_fitted_top1_m ])
    # FillMultipleH(top1_pt_,[t.top1_pt,t.fitted_top1_pt,t.correct_top1_pt,t.correct_fitted_top1_pt ])
    # FillMultipleH(top1_phi_,[t.top1_phi,t.fitted_top1_phi,t.correct_top1_phi,t.correct_fitted_top1_phi ])
    # FillMultipleH(top1_eta_,[t.top1_eta,t.fitted_top1_eta,t.correct_top1_eta,t.correct_fitted_top1_eta ])
    
    # FillMultipleH(top2_m_,[t.top2_m,t.fitted_top2_m,t.correct_top2_m,t.correct_fitted_top2_m ])
    # FillMultipleH(top2_pt_,[t.top2_pt,t.fitted_top2_pt,t.correct_top2_pt,t.correct_fitted_top2_pt ])
    # FillMultipleH(top2_phi_,[t.top2_phi,t.fitted_top2_phi,t.correct_top2_phi,t.correct_fitted_top2_phi ])
    # FillMultipleH(top2_eta_,[t.top2_eta,t.fitted_top2_eta,t.correct_top2_eta,t.correct_fitted_top2_eta ])

    
    # FillMultipleH(delta_tt_m_,[t.tt_m - t.ttMC_m,t.fitted_tt_m- t.ttMC_m,t.correct_tt_m - t.ttMC_m,t.correct_fitted_tt_m - t.ttMC_m])
    # FillMultipleH(delta_tt_pt_,[t.tt_pt - t.ttMC_pt,t.fitted_tt_pt- t.ttMC_pt,t.correct_tt_pt - t.ttMC_pt,t.correct_fitted_tt_pt - t.ttMC_pt])
    # FillMultipleH(delta_tt_phi_,[t.tt_phi - t.ttMC_phi,t.fitted_tt_phi- t.ttMC_phi,t.correct_tt_phi - t.ttMC_phi,t.correct_fitted_tt_phi - t.ttMC_phi])
    # FillMultipleH(delta_tt_eta_,[t.tt_eta - t.ttMC_eta,t.fitted_tt_eta- t.ttMC_eta,t.correct_tt_eta - t.ttMC_eta,t.correct_fitted_tt_eta - t.ttMC_eta])
    

print 'Correct combination found ',100*float(ncorrect)/ntotal, '% of the time\n'
print 'Correct combinations:  ',ncorrect, 'Internal only: ',ncross
print 'Only wrong internal combinations found ',100*float(ncross)/ntotal, '% of the time\n'
print 'The 6 tt jets are all present ',100*float(ntops)/ntotal, '% of the time', ' (Missing',100*(1- float(ntops)/ntotal),' of the time)'
print 'The 6 tt jets are all present but wrongly tagged',100*float(nmissedtag)/ntotal, '% of the time'
print 'for ttbb we have a total of: ',ntotal, ' events.',nmissedtag, ' events had the 6 jets detected, but we never got to pair the 6 at the same time, so there was no correct combination in the end (In the case we b-tagged a non b or not tagged a b). ',ntops, ' events had the 6 correct jets. Out of those, we have ', n2mix + n1mix, ' events in which the additional jets were part of the ttbar system. If everything is right, we should have the following values equal: ',  ncross + ncorrect, ' + ', n2mix + n1mix, ' = ', ntops, '. Out of the events with not selected jets, there are', n1mix, ' events with exactly 1 missed jet and ', n2mix, ' events with exactly 2 missed jets. In the 1 missed category, we had ', n1mix1b, ' events in which the missed jet was a b and ', n1mix0b, ' events which it was something else. In the 2 missed category, ',n2mix2b, ' events were 2 bs, ', n2mix1b, ' 1 b and 1 other non-b, and ', n2mix0b, '2 non b jets'  


legCorr_ = ['#splitline{Wrong combination}{before fit}','#splitline{Wrong combination}{after fit}','#splitline{Correct combination}{before fit}','#splitline{Correct combination}{after fit}']
legN_ = []
for i in range(7): legN_.append(str(i+6)+' jets in the event')


#Plot(tt_mcomb_,legN_,'tt_mass_vs_njets',0,1)

Plot(chi2_[:2],['Wrong Combination','Correct Combination'],'chi2',1)
# Plot([chi2_[2]],['Lowest #chi^{2}'],'chi2_small',1)
# Plot([prob_chi2_[1]],['Correct Combination'],'prob_chi2_corr',1)
# Plot([prob_chi2_[2]],['Lowest #chi^{2}'],'prob_chi2_small',1)
Plot(prob_chi2_[:2],['Wrong Combination','Correct Combination'],'prob_chi2',1)

# Plot(chi2_[1:],['Correct Combination','Lowest #chi^{2}'],'chi2_small_corr',1)
# Plot(prob_chi2_[1:],['Correct Combination','Lowest #chi^{2}'],'prob_chi2_small_corr',1)

# Plot(top1_m_,legCorr_,'top1_m')
# Plot(top1_pt_,legCorr_,'top1_pt')
# Plot(top1_eta_,legCorr_,'top1_eta')
# Plot(top1_phi_,legCorr_,'top1_phi')


# Plot(top1_m_[0:2],legCorr_[0:2],'top1_m_wrong')
# Plot(top1_pt_[0:2],legCorr_[0:2],'top1_pt_wrong')
# Plot(top1_eta_[0:2],legCorr_[0:2],'top1_eta_wrong')
# Plot(top1_phi_[0:2],legCorr_[0:2],'top1_phi_wrong')

# Plot(top1_m_[2:4],legCorr_[2:4],'top1_m_correct')
# Plot(top1_pt_[2:4],legCorr_[2:4],'top1_pt_correct')
# Plot(top1_eta_[2:4],legCorr_[2:4],'top1_eta_correct')
# Plot(top1_phi_[2:4],legCorr_[2:4],'top1_phi_correct')

# Plot([top1_m_[0],top1_m_[2]],[legCorr_[0],legCorr_[2]],'top1_m_comp')
# Plot([top1_pt_[0],top1_pt_[2]],[legCorr_[0],legCorr_[2]],'top1_pt_comp')
# Plot([top1_eta_[0],top1_eta_[2]],[legCorr_[0],legCorr_[2]],'top1_eta_comp')
# Plot([top1_phi_[0],top1_phi_[2]],[legCorr_[0],legCorr_[2]],'top1_phi_comp')

# Plot([top1_m_[1],top1_m_[3]],[legCorr_[1],legCorr_[3]],'top1_m_comp_fit')
# Plot([top1_pt_[1],top1_pt_[3]],[legCorr_[1],legCorr_[3]],'top1_pt_comp_fit')
# Plot([top1_eta_[1],top1_eta_[3]],[legCorr_[1],legCorr_[3]],'top1_eta_comp_fit')
# Plot([top1_phi_[1],top1_phi_[3]],[legCorr_[1],legCorr_[3]],'top1_phi_comp_fit')


# Plot(top2_m_,legCorr_,'top2_m')
# Plot(top2_pt_,legCorr_,'top2_pt')
# Plot(top2_eta_,legCorr_,'top2_eta')
# Plot(top2_phi_,legCorr_,'top2_phi')

# Plot(top2_m_[0:2],legCorr_[0:2],'top2_m_wrong')
# Plot(top2_pt_[0:2],legCorr_[0:2],'top2_pt_wrong')
# Plot(top2_eta_[0:2],legCorr_[0:2],'top2_eta_wrong')
# Plot(top2_phi_[0:2],legCorr_[0:2],'top2_phi_wrong')

# Plot(top2_m_[2:4],legCorr_[2:4],'top2_m_correct')
# Plot(top2_pt_[2:4],legCorr_[2:4],'top2_pt_correct')
# Plot(top2_eta_[2:4],legCorr_[2:4],'top2_eta_correct')
# Plot(top2_phi_[2:4],legCorr_[2:4],'top2_phi_correct')

# Plot([top2_m_[0],top2_m_[2]],[legCorr_[0],legCorr_[2]],'top2_m_comp')
# Plot([top2_pt_[0],top2_pt_[2]],[legCorr_[0],legCorr_[2]],'top2_pt_comp')
# Plot([top2_eta_[0],top2_eta_[2]],[legCorr_[0],legCorr_[2]],'top2_eta_comp')
# Plot([top2_phi_[0],top2_phi_[2]],[legCorr_[0],legCorr_[2]],'top2_phi_comp')

# Plot([top2_m_[1],top2_m_[3]],[legCorr_[1],legCorr_[3]],'top2_m_comp_fit')
# Plot([top2_pt_[1],top2_pt_[3]],[legCorr_[1],legCorr_[3]],'top2_pt_comp_fit')
# Plot([top2_eta_[1],top2_eta_[3]],[legCorr_[1],legCorr_[3]],'top2_eta_comp_fit')
# Plot([top2_phi_[1],top2_phi_[3]],[legCorr_[1],legCorr_[3]],'top2_phi_comp_fit')



# Plot(tt_m_,legCorr_,'tt_m')
# Plot(tt_pt_,legCorr_,'tt_pt')
# Plot(tt_eta_,legCorr_,'tt_eta')
# Plot(tt_phi_,legCorr_,'tt_phi')

# Plot(tt_m_[0:2],legCorr_[0:2],'tt_m_wrong')
# Plot(tt_pt_[0:2],legCorr_[0:2],'tt_pt_wrong')
# Plot(tt_eta_[0:2],legCorr_[0:2],'tt_eta_wrong')
# Plot(tt_phi_[0:2],legCorr_[0:2],'tt_phi_wrong')

# Plot(tt_m_[2:4],legCorr_[2:4],'tt_m_correct')
# Plot(tt_pt_[2:4],legCorr_[2:4],'tt_pt_correct')
# Plot(tt_eta_[2:4],legCorr_[2:4],'tt_eta_correct')
# Plot(tt_phi_[2:4],legCorr_[2:4],'tt_phi_correct')


# Plot([tt_m_[0],tt_m_[2]],[legCorr_[0],legCorr_[2]],'tt_m_comp')
# Plot([tt_pt_[0],tt_pt_[2]],[legCorr_[0],legCorr_[2]],'tt_pt_comp')
# Plot([tt_eta_[0],tt_eta_[2]],[legCorr_[0],legCorr_[2]],'tt_eta_comp')
# Plot([tt_phi_[0],tt_phi_[2]],[legCorr_[0],legCorr_[2]],'tt_phi_comp')

# Plot([tt_m_[1],tt_m_[3]],[legCorr_[1],legCorr_[3]],'tt_m_comp_fit')
# Plot([tt_pt_[1],tt_pt_[3]],[legCorr_[1],legCorr_[3]],'tt_pt_comp_fit')
# Plot([tt_eta_[1],tt_eta_[3]],[legCorr_[1],legCorr_[3]],'tt_eta_comp_fit')
# Plot([tt_phi_[1],tt_phi_[3]],[legCorr_[1],legCorr_[3]],'tt_phi_comp_fit')

# Plot(delta_tt_m_,legCorr_,'delta_tt_m')
# Plot(delta_tt_pt_,legCorr_,'delta_tt_pt')
# Plot(delta_tt_eta_,legCorr_,'delta_tt_eta')
# Plot(delta_tt_phi_,legCorr_,'delta_tt_phi')

# Plot(delta_tt_m_[0:2],legCorr_[0:2],'delta_tt_m_wrong')
# Plot(delta_tt_pt_[0:2],legCorr_[0:2],'delta_tt_pt_wrong')
# Plot(delta_tt_eta_[0:2],legCorr_[0:2],'delta_tt_eta_wrong')
# Plot(delta_tt_phi_[0:2],legCorr_[0:2],'delta_tt_phi_wrong')

# Plot(delta_tt_m_[2:4],legCorr_[2:4],'delta_tt_m_correct')
# Plot(delta_tt_pt_[2:4],legCorr_[2:4],'delta_tt_pt_correct')
# Plot(delta_tt_eta_[2:4],legCorr_[2:4],'delta_tt_eta_correct')
# Plot(delta_tt_phi_[2:4],legCorr_[2:4],'delta_tt_phi_correct')


# Plot([delta_tt_m_[0],delta_tt_m_[2]],[legCorr_[0],legCorr_[2]],'delta_tt_m_comp')
# Plot([delta_tt_pt_[0],delta_tt_pt_[2]],[legCorr_[0],legCorr_[2]],'delta_tt_pt_comp')
# Plot([delta_tt_eta_[0],delta_tt_eta_[2]],[legCorr_[0],legCorr_[2]],'delta_tt_eta_comp')
# Plot([delta_tt_phi_[0],delta_tt_phi_[2]],[legCorr_[0],legCorr_[2]],'delta_tt_phi_comp')

# Plot([delta_tt_m_[1],delta_tt_m_[3]],[legCorr_[1],legCorr_[3]],'delta_tt_m_comp_fit')
# Plot([delta_tt_pt_[1],delta_tt_pt_[3]],[legCorr_[1],legCorr_[3]],'delta_tt_pt_comp_fit')
# Plot([delta_tt_eta_[1],delta_tt_eta_[3]],[legCorr_[1],legCorr_[3]],'delta_tt_eta_comp_fit')
# Plot([delta_tt_phi_[1],delta_tt_phi_[3]],[legCorr_[1],legCorr_[3]],'delta_tt_phi_comp_fit')
#
#hcomb = rt.TH1F("hcomb","hc; total number of jets; Max number of combinations",14,6,20)
#for i in range(14):
#    hcomb.SetBinContent(i+1,6*maxComb(i+6))
#

#Plot1(hcomb,'max_comb',1)
#fout.Write();
