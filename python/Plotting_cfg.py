import CMS_lumi
import ROOT as rt
import CMS_lumi
import array
import pandas as pd

lumi = 35.920026e3

destination = '../Plots'

#histFillColor =['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']

histFillColor =['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#a65628','#f781bf','#999999','#ffff33']
processfiles = {
    # 'data':'../Datasets/Skimmed_Data.root',
    # 'ttbar': '../Datasets/Skimmed_Ttbar.root',
    # 'QCD':'../Datasets/Skimmed_QCD.root',
    'data':'../Datasets/data_MVA_ttbb.root',
    'ttbar':'../Datasets/ttbar_MVA_ttbb.root',
    'QCD':'../Datasets/QCD_MVA_ttbb.root',
    'ttW':'../Datasets/ttW_MVA_ttbb.root',
    'ttZ': '../Datasets/ttZ_MVA_ttbb.root',
    'WJ':'../Datasets/WJ_MVA_ttbb.root',
    'ZJ':'../Datasets/ZJ_MVA_ttbb.root',
    'tW': '../Datasets/tW_MVA_ttbb.root',
    'tbarW':'../Datasets/tbarW_MVA_ttbb.root',
    't':'../Datasets/t_MVA_ttbb.root',
    'tbar': '../Datasets/tbar_MVA_ttbb.root',
    's':'../Datasets/s_MVA_ttbb.root',
    'WW':'../Datasets/WW_MVA_ttbb.root',
    'WZ': '../Datasets/WZ_MVA_ttbb.root',
    'ZZ':'../Datasets/ZZ_MVA_ttbb.root'}



                #'data':'../Datasets/Skimmed_Data.root',
                # 'ttbar': '../Datasets/Skimmed_Ttbar.root',
                # 'QCD':'../Datasets/Skimmed_QCD.root',
                # 'ttW':'../Datasets/Skimmed_ttW.root',
                # 'ttZ': '../Datasets/Skimmed_ttZ.root',
                # 'WJ':'../Datasets/Skimmed_WJ.root',
                # 'ZJ':'../Datasets/Skimmed_ZJ.root',
                # 'tW': '../Datasets/Skimmed_tW.root',
                # 'tbarW':'../Datasets/Skimmed_tbarW.root',
                # 't':'../Datasets/Skimmed_t.root',
                # 'tbar': '../Datasets/Skimmed_tbar.root',
                # 's':'../Datasets/Skimmed_s.root',
                # 'WW':'../Datasets/Skimmed_WW.root',
                # 'WZ': '../Datasets/Skimmed_WZ.root',
                # 'ZZ':'../Datasets/Skimmed_ZZ.root'}







# processfiles = {'data':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_Data.root',
#                 'ttbar': 'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_Ttbar.root',
#                 'QCD':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_QCD.root',
#                 'ttW':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_ttW.root',
#                 'ttZ': 'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_ttZ.root',
#                 'WJ':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_WJ.root',
#                 'ZJ':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_ZJ.root',
#                 'tW': 'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_tW.root',
#                 'tbarW':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_tbarW.root',
#                 't':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_t.root',
#                 'tbar': 'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_tbar.root',
#                 's':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_s.root',
#                 'WW':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_WW.root',
#                 'WZ': 'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_WZ.root',
#                 'ZZ':'Datasets/Kinematic_Results_FH_Constrained_2011_BDT_Simple_ZZ.root'}

dscale = {'ttbar':lumi*831.76/76972928.0 ,
          'ttW':lumi*0.4062/428932,
          'ttZ': lumi*0.5297/346702,
          'WJ':lumi*2788/22370989,
          'ZJ':lumi*5.67/996052,
          'tW': lumi*35.85/991587,
          'tbarW':lumi*35.85/998630,
          't':lumi*136.02/5993152,
          'tbar':lumi*80.95/3928406 ,
          's':lumi*10.32/1872411,
          'WW':lumi*118.7/7981534,
          'WZ':lumi*47.13/3995503,
          'data':1.0,
          'ZZ':lumi*16.523/1988503}
processgroup = {'diboson':['WW','WZ','ZZ'],'s_top':['t','tbar','s','tW'],'ttV':['ttW','ttZ'],'VJ':['WJ','ZJ']}

ttplot=['ttbb', 'tt2b', 'ttb', 'ttcc', 'ttlf']
#plotCosmetics ={'ttbar':['t#bar{t}+lf','#fcbba1'], 'ttbarcc':['t#bar{t}+c#bar{c}','#fc9272'], 'ttbarb':['t#bar{t}+b','#fb6a4a'], 'ttbar2b':['t#bar{t}+2b','#ef3b2c'], 'ttbarbb':['t#bar{t}+b#bar{b}','#cb181d'],'QCD':['Multijet','#1b9e77']}
plotCosmetics ={'ttlf':['t#bar{t}+lf','#fcbba1'],'ttbar':['t#bar{t}','#fcbba1'], 'ttcc':['t#bar{t}+c#bar{c}','#fc9272'], 'ttb':['t#bar{t}+b','#fb6a4a'], 'tt2b':['t#bar{t}+2b','#ef3b2c'], 'ttbb':['t#bar{t}+b#bar{b}','#cb181d'],'diboson':['Diboson','#e7e1ef'],'s_top':['Single Top','#c51b8a'],'ttV':['t#bar{t}+V','#ffeda0'],'VJ':['V+jets','#feb24c'],'QCD':['Multijet','#1b9e77'],'data':['Data','#1b9e77']}
ttCls = {'ttbb':'ttCls>52','tt2b':'ttCls==52','ttb':'ttCls==51','ttcc':'ttCls>0 && ttCls<46','ttlf':'ttCls==0'}
vartitle = {'chi2': ['#chi^{2}', (50, 0, 20),1],
            'prob_chi2': ['Prob(#chi^{2})', (50, 0, 1),1],
            'n_jets': ['Jet Multiplicity', (8, 6, 14),1],
            'wkin': ['W_{Kin}', (20, 0, 1),1],
            'ht': ['HT (GeV)', (20, 200, 2200),1],
            'catplot':['',(10,1,11),1],
            'delta_w1M':['#Delta_{m}(W_{fit}, W_{rec})',(20,-200,60),1],
            'top1_m':['leading top mass (GeV)',(50,120,250),0],
            'top2_m':['second leading top mass (GeV)',(20,120,270),0],
            'w1_m':['leading w mass (GeV)',(20,20,120),0],
            'w2_m':['second leading w mass (GeV)',(20,20,120),0],
            'q1b1_mass':['l1 + b1 invariant mass (GeV)',(20,20,120),1],
            'p1b2_mass':['l3 + b2 invariant mass (GeV)',(20,20,120),1],
            'b1_pull_Et':['leading b-jet pull for Et',(20,-5,5),1],
            'b1_pt':['leading b-jet pt',(20,30,300),1],
            'b2_pt':['second leading b-jet pt',(20,30,300),1],
            'simple_chi2':['K^{2}',(1000,0,40),1],
            'bdtComb':['BDT',(20,-0.5,0.5),1],
            'mindeltaRb1q':['Min. #Delta_{R}(b_{1},l_{1}, l_{2})',(20,0.4,5),1],
            'mindeltaRb2p':['Min. #Delta_{R}(b_{2},l_{3}, l_{4})',(20,0.4,5),1],
            'deltaRb1b2':['#Delta_{R}(b_{1},b_{2})',(20,0.4,5),1],
            'deltaRb1top2':['#Delta_{R}(b_{1},top_{2})',(20,0.4,5),1],
            'deltaRb2top1':['#Delta_{R}(b_{2},top_{1})',(20,0.4,5),1],
            'deltaRb2q1':['#Delta_{R}(b_{2},l_{3})',(20,0.4,5),1],
            'deltaRb1w1':['#Delta_{R}(b_{1},W_{1})',(20,0.4,5),1],
            'deltaRb1q1':['#Delta_{R}(b_{1},l_{1})',(20,0.4,5),1],
            'deltaRb2w2':['#Delta_{R}(b_{2},W_{2})',(20,0.4,5),1],
            'deltaRb1w2':['#Delta_{R}(b_{1},W_{2})',(20,0.4,5),1],
            'deltaRb2w1':['#Delta_{R}(b_{2},W_{1})',(20,0.4,5),1],
            'deltaRb2p1':['#Delta_{R}(b_{2},l_{1})',(20,0.4,5),1],
            'deltaRl1l2':['#Delta_{R}(l_{1},l_{2})',(20,0.4,5),1],
            'deltaRq1q2':['#Delta_{R}(q_{1},q_{2})',(20,0.4,5),1],
            'jets_dRavg':['Average #Delta_{R} between all jets',(20,0.4,5),1],
            'jets_dRmax':['Max #Delta_{R} between all jets',(20,0.4,5),1],
            'jets_dRmin':['Min #Delta_{R} between all jets',(20,0.4,5),1],
            'n_bjets':['b-jet Multiplicity',(6,2,8),1],
            'exp(-chi2/4)':['P_{gof}',(20,0,0.001),1],
            'b1_csv':['leading top b CSV',(20,0.8484,1),1],
            'b2_csv':['second leading top b CSV',(20,0.8484,1),1],
            'addJet_CSV[0]':['leading additional jet CSV',(50,0.0,1),0],
            'addJet_CSV[1]':['second leading additional jet CSV',(50,0.0,1),0],
            'addJet_deltaR':['#Delta_{R}(add_{1},add_{2})',(20,0,5),1],
            'n_addJets':['Number of additional jets',(9,0,9),1],
            'n_addbjets':['Number of additional b-jets',(5,0,5),1],
            'BDT_Class[0]':['BDT for ttbar classification',(3,0,3),1],
            'BDT_ClassMajo[0]':['Majority vote BDT for ttbar classification',(3,0,3),1],
            'BDT_QCD':['BDT for QCD rejection',(50,-1,1),1],
            'BDT_FullQCD':['Combined BDT for QCD rejection',(1000,-1,1),1],
            'PyDNN_FullQCD':['Combined DNN for QCD rejection',(1000,0,1),1],
            'BDT_QCDData':['Data driven BDT for QCD rejection',(20,-1,1),0],
            'BDT_CWoLa':['Data driven BDT ',(50,-1,1),0],
            'BDT_QCDCWoLa2':['Data driven BDT for QCD rejection 2 ',(1000,-1,1),0],
            'Fish_QCDCWoLa':['Data driven LD for QCD rejection ',(20,-1,1),0],
            'BDT_Comb':['BDT for permutations',(50,-1,1),0],
            'BDT_ttbar':['BDT for ttbar rejection',(50,-1,1),1],
            'BDT_ttcc':['BDT for ttcc rejection',(5,-1,1),1],
            'LH_ttall':['Likelihood for ttbar inc. rejection',(5,-1,1),1],
            'PyDNN_CWoLa':['Data driven DNN ',(2000,0,1),1],
            'BDT_QCD_avg':['Average BDT for QCD rejection',(5,-1,1),1],
            'BDT_ttall_avg':['Average BDT for ttbar inc. rejection',(5,-1,1),1],
            'BDT_ttbar_avg':['Average BDT for ttbar rejection',(5,-1,1),1],
            'BDT_ttbarMajo':['Average BDT for ttbar rejection',(50,-1,1),1],
            'BDT_ttcc_avg':['Average BDT for ttcc rejection',(5,-1,1),1],
            'LH_ttall_avg':['Average Likelihood for ttbar inc. rejection',(5,-1,1),1],
            'qgLR':['QGLR',(20,0,1),1],
            'memttbb':['mem',(50,0,1),1],
            'girth':['girth',(50,0,0.5),1],
            'top1_pt':['leading top p_{t}',(20,40,400),1],
            'top2_pt':['second leading top p_{t}',(20,40,400),1],
            'deltaRb1b2':['#Delta_{R}(b_{1},b_{2})',(20,0.4,5),1],
            'deltaRaddb1':['#Delta_{R}(add.{1},b_{1})',(20,0.4,5),1],
            'deltaRaddb2':['#Delta_{R}(add.{1},b_{2})',(20,0.4,5),1],
            'deltaRaddtop2':['#Delta_{R}(add.{1},top_{2})',(20,0.4,5),1],
            'deltaRaddtop1':['#Delta_{R}(add.{1},top_{1})',(20,0.4,5),1],
            'deltaPhiw1w2':['#Delta_{#phi}(W_{1},W_{2})',(20,0,3),1],
            'deltaPhit1t2':['#Delta_{#phi}(t_{1},t_{2})',(20,0,3),1],
            'deltaPhib1b2':['#Delta_{#phi}(b_{1},b_{2})',(20,0,3),1],
            'deltaPhil1l2':['#Delta_{#phi}(l_{1},l_{2})',(20,0,3),1],
            'deltaPhiq1q2':['#Delta_{#phi}(l_{3},l_{4})',(20,0,3),1],
            'addJet_deltaPhi':['#Delta_{#phi}(add_{1},add_{2})',(20,0,3),1],
            'addJet_deltaEta':['#Delta_{#eta}(add_{1},add_{2})',(20,0,3),1],
            'deltaEtal1l2':['#Delta_{#eta}(l_{1},l_{2})',(20,0,3),1],
            'deltaEtaq1q2':['#Delta_{#eta}(q_{1},q_{2})',(20,0,3),1],
            'deltaEtab1b2':['#Delta_{#eta}(b_{1},b_{2})',(20,0,3),1],
            'deltaEtat1t2':['#Delta_{#eta}(top_{1},top_{2})',(20,0,3),1],
            'deltaEtaw1w2':['#Delta_{#eta}(W_{1},W_{2})',(20,0,3),1],
            'addJet_pt[1]':['leading additional jet p_{t}',(20,40,400),1],
            'btagLR4b':['btagLR4b',(10,0.75,1),0],
            'btagLR3b':['btagLR3b',(10,0.75,1),0],
            'centrality':['Centrality',(20,0.2,1.2),1],
            'aplanarity':['Aplanarity',(20,-0.5,0.5),1],
            'meanDeltaRbtag':['mean #Delta_{R} tagged jets',(20,0.4,4),1],
            'meanCSV':['mean CSV',(20,0.84,1),1],
            'meanCSVbtag':['mean CSV tagged jets',(20,0.4,0.9),1],
            'jet_CSV[0]':['CSV of jet 1',(20,0.4,0.9),1],
            'jet_CSV[1]':['CSV of jet 2',(20,0.4,0.9),1],
            'jet_CSV[2]':['CSV of jet 3',(20,0.4,0.9),1],
            'jet_CSV[3]':['CSV of jet 4',(20,0.4,0.9),1],
            'jet_CSV[4]':['CSV of jet 5',(20,0.4,0.9),1],
            'jet_CSV[5]':['CSV of jet 6',(20,0.4,0.9),1],
            'jet_QGL[0]':['QGL of jet 1',(20,0.4,0.9),1],
            'jet_QGL[1]':['QGL of jet 2',(20,0.4,0.9),1],
            'jet_QGL[2]':['QGL of jet 3',(20,0.4,0.9),1],
            'jet_QGL[3]':['QGL of jet 4',(20,0.4,0.9),1],
            'jet_QGL[4]':['QGL of jet 5',(20,0.4,0.9),1],
            'jet_QGL[5]':['QGL of jet 6',(20,0.4,0.9),1],
            'all_mass':['Invariant mass of all jets (GeV)',(50,400,2000),1],
            'tt_m':['Invariant mass of ttbar system (GeV)',(50,400,2000),1],
            'lq1_m':['Invariant mass of light jet 1 (GeV)',(50,400,2000),1],
            'lq2_m':['Invariant mass of light jet 2 (GeV)',(50,400,2000),1],
            'lp1_m':['Invariant mass of light jet 3 (GeV)',(50,400,2000),1],
            'lp2_m':['Invariant mass of light jet 4 (GeV)',(50,400,2000),1],
            'lq1_eta':['light jet 1 eta',(20,0,3),1],
            'lq2_eta':['light jet 2 eta',(20,0,3),1],
            'lp1_eta':['light jet 3 eta',(20,0,3),1],
            'lp2_eta':['light jet 4 eta',(20,0,3),1],
            'BDT_ttbb_All':['BDT for ttbar inc. rejection',(5,0,5),1],
            'BDT_ttbb3b':['Multiclass BDT',(5,0,5),1],
            'BDT_ttbb7j':['Multiclass BDT 7j',(5,0,5),1],
            'BDT_ttbb8j':['Multiclass BDT 8j',(5,0,5),1],
            'BDT_ttbb9j':['Multiclass BDT 9j',(5,0,5),1],
            'PyDNN_ttbb7j':['Multiclass DNN 7j',(5,0,5),1],
            'PyDNN_ttbb8j':['Multiclass DNN 8j',(5,0,5),1],
            'PyDNN_ttbb9j':['Multiclass DNN 9j',(5,0,5),1],

            'lq1_pt':['light jet 1 pt',(50,30,200),1],
            'lq2_pt':['light jet 2 pt',(50,30,200),1],
            'lp1_pt':['light jet 3 pt',(50,30,200),1],
            'lp2_pt':['light jet 4 pt',(50,30,200),1],
            'jet5pt':['5th pt',(50,30,200),1],
            'w1_pt':['leading w pt',(50,30,200),1],
            'w2_pt':['second leading w pt',(50,30,200),1],
            'w1_eta':['leading w eta',(20,0,3),1],
            'w2_eta':['second leading w eta',(20,0,3),1],
            'top1_eta':['leading top eta',(20,0,3),1],
            'top2_eta':['second leading top eta',(20,0,3),1],
            'deltaEtaaddb1':['delta eta add. and leading b',(20,0,3),1],
            'deltaEtaaddb2':['delta eta add. and leading b',(20,0,3),1],
            'tt_pt':['ttbar system pt (GeV/c)',(50,100,2000),1],
            'tt_eta':['ttbar system eta',(20,0,3),1],
            'b1_eta':['leading b-jet eta',(20,0,3),1],
            'b2_eta':['second leading b-jet eta',(20,0,3),1],
            'closest_mass':['Invariant mass of closes jet pair (GeV)',(20,20,120),1],
            'jet_MOverPt[0]':['jet 1 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[1]':['jet 2 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[2]':['jet 3 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[3]':['jet 4 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[4]':['jet 5 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[5]':['jet 6 mass/Pt',(20,0.0,0.4),1],


}




histLineColor = rt.kBlack
markerSize  = 1.0

#CMS Style
iPeriod = 0
iPos = 11
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "35.9 fb^{-1} (13 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
if( iPos==0 ): CMS_lumi.relPosX = 0.12
H_ref = 600; 
W_ref = 540; 
x1_l = 0.95
y1_l = 0.90
dx_l = 0.30
dy_l = 0.28
x0_l = x1_l-dx_l
y0_l = y1_l-dy_l
ar_l = dy_l/dx_l
W = W_ref
H  = H_ref
# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

n_ = (len(plotCosmetics) + 4)/2
gap_ = 1./(n_+1)
bwx_ = 0.12/2
bwy_ = gap_/1.5

x_l = [1.2*bwx_]
            
y_l = [1-gap_]
ex_l = [0]
ey_l = [0.04/ar_l]


x_l = array.array("f",x_l)
ex_l = array.array("f",ex_l)
y_l = array.array("f",y_l)
ey_l = array.array("f",ey_l)
xx_ = x_l[0]





def SetupBox(box_,yy_,fill = rt.kBlack):
    
    box_.SetLineStyle( rt.kSolid )
    box_.SetLineWidth( 1 )
    box_.SetLineColor( rt.kBlack )
    box_.SetFillColor(fill)






def SetupCanvas(c,logy):
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
    c.SetLeftMargin( L/W_ref )
    c.SetRightMargin( R/W_ref )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )
    c.SetTickx(0)
    c.SetTicky(0)
    if logy: c.SetLogy()


def AddOverflow(h):
    b0 = h.GetBinContent(0)
    e0 = h.GetBinError(0)
    nb = h.GetNbinsX()
    bn = h.GetBinContent(nb + 1)
    en = h.GetBinError(nb + 1)
    
    h.SetBinContent(0, 0)
    h.SetBinContent(nb+1, 0)
    h.SetBinError(0, 0)
    h.SetBinError(nb+1, 0)
    
    h.SetBinContent(1, h.GetBinContent(1) + b0)
    h.SetBinError(1, (h.GetBinError(1)**2 + e0**2)**0.5 )
    
    h.SetBinContent(nb, h.GetBinContent(nb) + bn)
    h.SetBinError(nb, (h.GetBinError(nb)**2 + en**2)**0.5 )


def FormatTable(table):
    rows = table.keys()
    rows.remove('Process')
    rows.remove('Total err')
    rows.remove('Total bkg.')
    print rows
    col = table['Process']
    newlist = []
    mc = []
    for key in rows:
        newlist.append(table[key])

    dummy = []
    for i, s in enumerate(table['Total bkg.']):
        dummy+= [str(round(table['Total bkg.'][i],2)) + '$#pm$'+str(round(table['Total err'][i],2))]
        

    pframe= pd.DataFrame(data=newlist,
                 index=rows,
                 columns=col)
            
    pframe.loc['Total bkg.']=dummy
    nindex = ['t#bar{t}+lf', 't#bar{t}+c#bar{c}', 'Multijet','Single Top','t#bar{t}+V','V+jets','Diboson','Total bkg.', 't#bar{t}+b#bar{b}','t#bar{t}+2b', 't#bar{t}+b', 'Data']




    
    pframe = pframe.reindex(index = nindex)

    # pbkg= pd.DataFrame(data=mc,
    #                      index=['Total Simulation'],
    #                      columns=col)
    # pframe.append(pbkg)
    
    print pframe.to_latex()
    
