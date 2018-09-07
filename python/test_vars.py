import sys
import os
from Plotting_cfg import *
import ROOT
#ROOT.gROOT.SetBatch(True)
cw_vars = [
    'w1_m', 'w2_m', 'top1_m','top2_m',   'deltaRb1w2',
    'meanDeltaRbtag', 'deltaRb2w1', 'p1b1_mass', 'q1b2_mass',
    'deltaRb1b2','meanCSVbtag','sphericity','centrality','aplanarity',
    'tt_eta','w1_eta',
    'mindeltaRb2q', 'all_mass',
    'deltaRb1top2','jets_dRmax','jets_dRavg',
    'meanCSV','jets_dRmin','simple_chi2','BDT_Comb'
    ]
#'lp2_pt','lq1_pt','lq2_pt','b1_pt',
samples = ['data','ttbar']
# reg1Cut = ROOT.TCut('qgLR<0.4 && simple_chi2 < 10')
# reg1Cutextrap = ROOT.TCut('jet_QGL[2]>0.52 && jet_QGL[4]>0.31')
# reg2Cut = ROOT.TCut('qgLR < 0.4 && simple_chi2 > 10 && simple_chi2 < 11')
# reg2Cutextrap = ROOT.TCut('jet_QGL[2]<0.12 && jet_QGL[4]<0.2')

reg1Cut = ROOT.TCut('qgLR<0.5')
reg1Cutextrap = ROOT.TCut('qgLR<0.5')
reg2Cut = ROOT.TCut('qgLR > 0.5')
reg2Cutextrap = ROOT.TCut('qgLR > 0.5')
extrapCut=ROOT.TCut('jet_CSV[0]>=0.9535||jet_CSV[1]>=0.9535')
notextrapCut=ROOT.TCut('jet_CSV[0]<0.9535&&jet_CSV[1]<0.9535 && (jet_CSV[0]>=0.8484|| jet_CSV[1]>=0.8484)')
#weight = 'weight*puweight*btagweight*qgweight'
topweight = 'weight*puweight*btagweight*qgweight*topweight'
'''
We shall test 2 different things. We need to know if sig/bkg pdfs are similar in reg1 and reg2.
Besides that, we ought to know if the pdf for signal is also similar for the extrapolation
'''
cutlist = {
    'reg1_train':reg1Cut*(notextrapCut), 'reg2_train':reg2Cut*(notextrapCut),
    'reg1_extrap':reg1Cutextrap*(extrapCut),'reg2_extrap':reg2Cutextrap*(extrapCut)
    }
files = []
tree = {}
hvar = {}

for i, sample in enumerate(samples):
    files.append(rt.TFile(processfiles[sample],"READ"))
    tree[sample] = files[i].Get('tree')

    for j, var in enumerate(cw_vars):
        weight = ROOT.TCut('1==1')
        if 'tt' in sample: weight =ROOT.TCut(topweight)
        for key in cutlist:
            tree[sample].Draw(var + '>>'+ 'h'+key+var +str(vartitle[var][1]),weight*cutlist[key])
            hvar[sample+key+var]= ROOT.gDirectory.Get("h"+key+var).Clone()


for j, var in enumerate(cw_vars):
    for key in cutlist:
        hvar['ttbar'+key+var]*dscale['ttbar']
        hvar['data'+key+var].Add(hvar['ttbar'+key+var],-1)
        print key, var
        hvar['ttbar'+key+var].Scale(1.0/hvar['ttbar'+key+var].Integral())
        hvar['data'+key+var].Scale(1.0/hvar['data'+key+var].Integral())

        # if not os.path.exists("Plots/test_vars"):
        #     os.makedirs("Plots/test_vars")
        # else:
        #     print "WARNING: directory already exists. Will overwrite existing files..."
        #
        # hvar['data'+key+var].SaveAs("Plots/test_vars/data"+key+var+".png")
        # hvar['ttbar'+key+var].SaveAs("Plots/test_vars/ttbar"+key+var+".png")


#hvar['datareg1_train'+var].Divide(hvar['datareg2_train'+var])
#hvar['datareg1_train'+var].Draw()
#person = input('Enter your name: ')
for var in cw_vars:
    print 'reg_train bkg',var, hvar['datareg1_train'+var].KolmogorovTest(hvar['datareg2_train'+var])
    print 'reg_train sig',var, hvar['ttbarreg1_train'+var].KolmogorovTest(hvar['ttbarreg2_train'+var])
    print 'reg1_extrap bkg ',var, hvar['datareg1_train'+var].KolmogorovTest(hvar['datareg1_extrap'+var])
    print 'reg2_extrap bkg ',var, hvar['datareg2_train'+var].KolmogorovTest(hvar['datareg2_extrap'+var])
    print 'reg1_extrap sig ',var, hvar['ttbarreg1_train'+var].KolmogorovTest(hvar['ttbarreg1_extrap'+var])
    print 'reg2_extrap sig ',var, hvar['ttbarreg2_train'+var].KolmogorovTest(hvar['ttbarreg2_extrap'+var])
    #hvar['ttbarreg1_train'+var].Divide(hvar['ttbarreg1_extrap'+var])
    #hvar['ttbarreg1_train'+var].Draw()
    #raw_input('Press enter: ')
    print '##########################################################################################'
