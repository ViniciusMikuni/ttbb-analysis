vfull = ['lq1_pt','lq2_pt','lp1_pt','lp2_pt','b1_pt','b2_pt', 'w1_m', 'w2_m', 'top1_m','top2_m',   'deltaRb1w2', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1',   'deltaRb2p1','deltaRb2top1', 'p1b2_mass', 'q1b1_mass', 'deltaRb1b2','meanCSVbtag','deltaRq1q2','jet_CSV[0]','jet_CSV[1]','minjetpt','sphericity','centrality','aplanarity','b2_eta', 'lp1_phi','top1_phi','top2_eta','lq1_phi','lq1_eta','tt_eta','b2_phi','top1_eta','w1_eta','tt_phi','w1_phi','lp2_phi','top2_phi','deltaPhit1t2','deltaPhiq1q2','lp1_eta','w2_eta','lq2_phi', 'b1_phi','deltaPhib1b2','jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','mass','tt_pt', 'b2_m', 'lq1_m', 'w1_pt', 'w2_pt', 'w2_phi', 'btagLR3b', 'mindeltaRb1q',  'ht', 'mindeltaRb2p', 'all_mass','jet_CSV[2]','jet_CSV[3]','jet_CSV[4]','jet_CSV[5]', 'b1_eta','lp2_eta', 'deltaRb1top2', 'deltaPhil1l2', 'deltaEtal1l2', 'deltaEtab1b2','jets_dRmax', 'deltaEtat1t2','meanCSV','jets_dRmin','simple_chi2','BDT_Comb']

v1=['lq2_pt','lp1_pt','lp2_pt','b1_pt','b2_pt', 'w1_m', 'w2_m', 'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1', 'p1b2_mass', 'q1b1_mass', 'deltaRb1b2','deltaRq1q2','jet_CSV[0]','jet_CSV[1]','minjetpt','aplanarity', 'jet_MOverPt[0]','jet_MOverPt[1]','jet_MOverPt[2]','jet_MOverPt[3]','jet_MOverPt[4]','jet_MOverPt[5]','tt_pt', 'lq1_m', 'mindeltaRb1q',  'ht', 'mindeltaRb2p', 'all_mass','meanCSV','jets_dRmin','BDT_Comb']

v2=['lq2_pt','lp1_pt','lp2_pt','b1_pt','b2_pt', 'w2_m', 'top1_m','top2_m', 'meanDeltaRbtag',   'deltaRl1l2',   'deltaRb2w1', 'p1b2_mass', 'q1b1_mass', 'deltaRb1b2','jet_CSV[0]','aplanarity','tt_pt',  'ht', 'mindeltaRb2p', 'all_mass','meanCSV','BDT_Comb']

for v in v2:
    v1.remove(v)

print v1

for v in v1:
    vfull.remove(v)

print '         \n'
print vfull


Tested = ['b1_pt','deltaRb1b2','q1b1_m','p1b2_m','top1_m','jet_CSV[1]','jet_CSV[0]','BDT_CWoLa','top2_m','mindeltaRb2p','lp1_pt','lp2_pt','deltaRl1l2','lq2_pt','w2_m','deltaRb2w1','meanDeltaRbtag','','','']
