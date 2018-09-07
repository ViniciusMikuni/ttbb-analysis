import CMS_lumi
import ROOT as rt
import CMS_lumi
import array
import pandas as pd
import numpy as np

lumi = 35.920026e3

destination = '../Plots'
#opt_bin=np.array([0.0, 0.15663132626525306, 0.16243248649729947, 0.19823964792958593, 0.20184036807361472, 0.22104420884176834, 0.22444488897779555, 0.2654530906181236, 0.26805361072214445, 0.38107621524304863, 0.3836767353470694, 0.4352870574114823, 0.4392878575715143, 0.46929385877175434, 0.47169433886777357, 0.5033006601320265, 0.5057011402280456, 0.7027405481096219, 0.7045409081816363, 0.7115423084616923, 0.7133426685337068, 1.0])
#opt_bin=np.array([0.0, 0.17051705170517054, 0.21212121212121213, 0.24492449244924494, 0.27382738273827384, 0.30113011301130116, 0.3274327432743274, 0.35173517351735173, 0.37533753375337536, 0.39833983398339834, 0.42074207420742077, 0.44214421442144214, 0.46424642464246424, 0.48624862486248627, 0.5074507450745075, 0.5287528752875288, 0.548954895489549, 0.5698569856985699, 0.5916591659165917, 0.6102610261026102, 0.6298629862986299, 0.6487648764876488, 0.6667666766676668, 0.6843684368436844, 0.7012701270127013, 0.7181718171817182, 0.7335733573357336, 0.7493749374937494, 0.7647764776477648, 0.7788778877887789, 0.7925792579257926, 0.8061806180618062, 0.8194819481948195, 0.8307830783078308, 0.8430843084308431, 0.8549854985498551, 0.8658865886588659, 0.8768876887688769, 0.8866886688668867, 0.8963896389638965, 0.9056905690569057, 0.913991399139914, 0.9221922192219222, 0.9304930493049305, 0.937893789378938, 0.9448944894489449, 0.9516951695169518, 0.9574957495749575, 0.9633963396339634, 0.969096
#9096909692, 0.9743974397439744, 0.9792979297929794, 0.9838983898389839, 0.9877987798779878, 0.9911991199119913, 0.993899389938994, 0.9963996399639964, 0.9985998599859987, 1.0])


opt_bin=np.array(
 [ 0.8621862186218622, 0.890889088908891, 0.907890789078908, 0.9206920692069207, 0.9308930893089309, 0.9388938893889389, 0.9458945894589459, 0.9521952195219522, 0.9571957195719573, 0.961896189618962, 0.9660966096609661, 0.9700970097009701, 0.9735973597359736, 0.9767976797679768, 0.9796979697969798, 0.9823982398239824, 0.9847984798479849, 0.986998699869987, 0.9888988898889889, 0.9905990599059906, 0.9920992099209921, 0.9934993499349936, 0.9947994799479948, 0.9960996099609961, 0.9972997299729973, 0.9982998299829984, 0.9991999199919992,1.0]
    )


#histFillColor =['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']

histFillColor =['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#a65628','#f781bf','#999999','#ffff33']
processfiles = {
    # 'dataC_':'../Datasets/data_MVA_CWoLa.root',
    # 'ttbarCW':'../Datasets/ttbar_MVA_CWoLa.root',
    # 'QCDCW':'../Datasets/QCD_MVA_CWoLa.root',
    # 'ttWCW':'../Datasets/ttW_MVA_CWoLa.root',
    # 'ttZCW': '../Datasets/ttZ_MVA_CWoLa.root',
    # 'WJCW':'../Datasets/WJ_MVA_CWoLa.root',
    # 'ZJCW':'../Datasets/ZJ_MVA_CWoLa.root',
    # 'tWCW': '../Datasets/tW_MVA_CWoLa.root',
    # 'tbarWCW':'../Datasets/tbarW_MVA_CWoLa.root',
    # 'tCW':'../Datasets/t_MVA_CWoLa.root',
    # 'tbarCW': '../Datasets/tbar_MVA_CWoLa.root',
    # 'sCW':'../Datasets/s_MVA_CWoLa.root',
    # 'WWCW':'../Datasets/WW_MVA_CWoLa.root',
    # 'WZCW': '../Datasets/WZ_MVA_CWoLa.root',
    # 'ZZCW':'../Datasets/ZZ_MVA_CWoLa.root',


    'ttbarMisc':'../Datasets/ttbar_MVA_Misc.root',
    'QCDMisc':'../Datasets/QCD_MVA_Misc.root',
    'dataMisc':'../Datasets/data_MVA_Test_CWoLa_Misc.root',
    'ttbarT':'../Datasets/ttbar_MVA_CWoLa_Test.root',
    'QCDT':'../Datasets/QCD_MVA_CWoLa_Test.root',
    'ttbarC':'../Datasets/ttbar_MVA_CWoLa.root',
    'dataC':'../Datasets/data_MVA_CWoLa.root',
    'dataT':'../Datasets/data_MVA_CWoLa_Test.root',
    'QCDC':'../Datasets/QCD_MVA_CWoLa.root',
    'ttbarComb': '../Datasets/Combination_train.root',
    'ttbar_tprime': '../Datasets/ttbar_tprime.root',
    'data_tprime':'../Datasets/data_tprime.root',

    # 'data':'../Datasets/data_MVA_CWoLa_Test.root',
    # 'ttbar':'../Datasets/ttbar_MVA_CWoLa_Test.root',
    # 'QCD':'../Datasets/QCD_MVA_CWoLa_Test.root',
    # 'ttW':'../Datasets/ttW_MVA_CWoLa_Test.root',
    # 'ttH':'../Datasets/ttH_MVA_CWoLa_Test.root',
    # 'ttZ': '../Datasets/ttZ_MVA_CWoLa_Test.root',
    # 'WJ':'../Datasets/WJ_MVA_CWoLa_Test.root',
    # 'ZJ':'../Datasets/ZJ_MVA_CWoLa_Test.root',
    # 'tW': '../Datasets/tW_MVA_CWoLa_Test.root',
    # 'tbarW':'../Datasets/tbarW_MVA_CWoLa_Test.root',
    # 't':'../Datasets/t_MVA_CWoLa_Test.root',
    # 'tbar': '../Datasets/tbar_MVA_CWoLa_Test.root',
    # 's':'../Datasets/s_MVA_CWoLa_Test.root',
    # 'WW':'../Datasets/WW_MVA_CWoLa_Test.root',
    # 'WZ': '../Datasets/WZ_MVA_CWoLa_Test.root',
    # 'ZZ':'../Datasets/ZZ_MVA_CWoLa_Test.root'}

    # 'data':'../Datasets/data_MVA_CWoLa.root',
    # 'ttbar':'../Datasets/ttbar_MVA_CWoLa.root',
    # 'QCD':'../Datasets/QCD_MVA_CWoLa.root',
    # 'ttW':'../Datasets/ttW_MVA_CWoLa.root',
    # 'ttH':'../Datasets/ttH_MVA_CWoLa.root',
    # 'ttZ': '../Datasets/ttZ_MVA_CWoLa.root',
    # 'WJ':'../Datasets/WJ_MVA_CWoLa.root',
    # 'ZJ':'../Datasets/ZJ_MVA_CWoLa.root',
    # 'tW': '../Datasets/tW_MVA_CWoLa.root',
    # 'tbarW':'../Datasets/tbarW_MVA_CWoLa.root',
    # 't':'../Datasets/t_MVA_CWoLa.root',
    # 'tbar': '../Datasets/tbar_MVA_CWoLa.root',
    # 's':'../Datasets/s_MVA_CWoLa.root',
    # 'WW':'../Datasets/WW_MVA_CWoLa.root',
    # 'WZ': '../Datasets/WZ_MVA_CWoLa.root',
    # 'ZZ':'../Datasets/ZZ_MVA_CWoLa.root'}



    # 'data':'../Datasets/Skimmed_Data.root',
    # 'ttbar': '../Datasets/Skimmed_Ttbar_Full.root',
    # 'QCD':'../Datasets/Skimmed_QCD.root',
    # 'ttW':'../Datasets/Skimmed_ttW_Full.root',
    # 'ttH':'../Datasets/Skimmed_ttH.root',
    # 'ttZ': '../Datasets/Skimmed_ttZ_Full.root',
    # 'WJ':'../Datasets/Skimmed_WJ_Full.root',
    # 'ZJ':'../Datasets/Skimmed_ZJ_Full.root',
    # 'tW': '../Datasets/Skimmed_tW_Full.root',
    # 'tbarW':'../Datasets/Skimmed_tbarW_Full.root',
    # 't':'../Datasets/Skimmed_t_Full.root',
    # 'tbar': '../Datasets/Skimmed_tbar_Full.root',
    # 's':'../Datasets/Skimmed_s_Full.root',
    # 'WW':'../Datasets/Skimmed_WW_Full.root',
    # 'WZ': '../Datasets/Skimmed_WZ_Full.root',
    # 'ZZ':'../Datasets/Skimmed_ZZ_Full.root',



    'data':'../Datasets/Skimmed_Data.root',
    #'ttbar': '../Datasets/Skimmed_Ttbar_Full.root',
    'ttbar': '../Datasets/Skimmed_Ttbar_Fast.root',
    #'QCD':'../Datasets/Skimmed_QCD.root',
    'QCD300':'../Datasets/Skimmed_QCD300.root',
    'QCD500':'../Datasets/Skimmed_QCD500.root',
    'QCD700':'../Datasets/Skimmed_QCD700.root',
    'QCD1000':'../Datasets/Skimmed_QCD1000.root',
    'QCD1500':'../Datasets/Skimmed_QCD1500.root',
    'QCD2000':'../Datasets/Skimmed_QCD2000.root',
    # 'ttW':'../Datasets/Skimmed_ttW_Full.root',
    # 'ttH':'../Datasets/Skimmed_ttH_Full.root',
    # 'ttZ': '../Datasets/Skimmed_ttZ.root',
    # 'WJ':'../Datasets/Skimmed_WJ_Full.root',
    # 'ZJ':'../Datasets/Skimmed_ZJ_Full.root',
    # 'tW': '../Datasets/Skimmed_tW_Full.root',
    # 'tbarW':'../Datasets/Skimmed_tbarW._Fullroot',
    # 't':'../Datasets/Skimmed_t_Full.root',
    # 'tbar': '../Datasets/Skimmed_tbar_Full.root',
    # 's':'../Datasets/Skimmed_s_Full.root',
    # 'WW':'../Datasets/Skimmed_WW_Full.root',
    # 'WZ': '../Datasets/Skimmed_WZ_Full.root',
    # 'ZZ':'../Datasets/Skimmed_ZZ_Full.root',

    'ttW':'../Datasets/Skimmed_ttW_fast.root',
    'ttH':'../Datasets/Skimmed_ttH_fast.root',
    'ttZ': '../Datasets/Skimmed_ttZ_fast.root',
    'WJ':'../Datasets/Skimmed_WJ_fast.root',
    'ZJ':'../Datasets/Skimmed_ZJ_fast.root',
    'tW': '../Datasets/Skimmed_tW_fast.root',
    'tbarW':'../Datasets/Skimmed_tbarW_fast.root',
    't':'../Datasets/Skimmed_t_fast.root',
    'tbar': '../Datasets/Skimmed_tbar_fast.root',
    's':'../Datasets/Skimmed_s_fast.root',
    'WW':'../Datasets/Skimmed_WW_fast.root',
    'WZ': '../Datasets/Skimmed_WZ_fast.root',
    'ZZ':'../Datasets/Skimmed_ZZ_fast.root',
    'isrUp':'../Datasets/Skimmed_Ttbar_isrUp.root',
    'isrDown':'../Datasets/Skimmed_Ttbar_isrDown.root',
    'fsrUp':'../Datasets/Skimmed_Ttbar_fsrUp.root',
    'fsrDown':'../Datasets/Skimmed_Ttbar_fsrDown.root',
    'hdampUp':'../Datasets/Skimmed_Ttbar_hdampUp.root',
    'hdampDown':'../Datasets/Skimmed_Ttbar_hdampDown.root',
    'tuneUp':'../Datasets/Skimmed_Ttbar_tuneUp.root',
    'tuneDown':'../Datasets/Skimmed_Ttbar_tuneDown.root',
    }


    # 'data':'../Datasets/data_MVA_Multi.root',
    # 'ttbar':'../Datasets/ttbar_MVA_Multi.root',
    # 'QCD':'../Datasets/QCD_MVA_Multi.root',
    # 'ttW':'../Datasets/ttW_MVA_Multi.root',
    # 'ttH':'../Datasets/ttH_MVA_Multi.root',
    # 'ttZ': '../Datasets/ttZ_MVA_Multi.root',
    # 'WJ':'../Datasets/WJ_MVA_Multi.root',
    # 'ZJ':'../Datasets/ZJ_MVA_Multi.root',
    # 'tW': '../Datasets/tW_MVA_Multi.root',
    # 'tbarW':'../Datasets/tbarW_MVA_Multi.root',
    # 't':'../Datasets/t_MVA_Multi.root',
    # 'tbar': '../Datasets/tbar_MVA_Multi.root',
    # 's':'../Datasets/s_MVA_Multi.root',
    # 'WW':'../Datasets/WW_MVA_Multi.root',
    # 'WZ': '../Datasets/WZ_MVA_Multi.root',
    # 'ZZ':'../Datasets/ZZ_MVA_Multi.root'}










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

dscale = {
          #'ttbar_fast':lumi*831.76/66063084.0 ,
          #'ttbar_fast':lumi*831.76/(0.48546489*76972928.0) ,
          #'ttbar':lumi*831.76/76972928.0 ,
          'fsrDown':lumi*831.76/62546365.458189,
          'fsrUp':lumi*831.76/51861921.591189,
          'isrUp':lumi*831.76/60126179.631991,
          'isrDown': lumi*831.76/57242047.731827,
          'tuneDown': lumi*831.76/28444383.,
          'tuneUp': lumi*831.76/28647021.0,
          'hdampDown': lumi*831.76/54719183.822190,
          'hdampUp': lumi*831.76/60460885.407178,
          #'ttbar':lumi*831.76/(76972928.0*0.7260574411417471) ,
          'ttbar_tprime':lumi*831.76/(76972928.0*0.7260574411417471) ,
          # 'ttW':lumi*0.4062/428932,
          # 'ttH':lumi*0.29533504/3737487,
          # 'ttZ': lumi*0.5297/346702,
          # 'WJ':lumi*2788/22370989,
          # 'ZJ':lumi*5.67/996052,
          # 'tW': lumi*35.85/991587,
          # 'tbarW':lumi*35.85/998630,
          # 't':lumi*136.02/5993152,
          # 'tbar':lumi*80.95/3928406 ,
          # 's':lumi*10.32/1872411,
          # 'WW':lumi*118.7/7981534,
          # 'WZ':lumi*47.13/3995503,
          # 'data':1.0,
          # 'ZZ':lumi*16.523/1988503,


          'ttbar':lumi*831.76/(66070244.0),
          'ttW':lumi*0.4062/262777.78,
          'ttH':lumi*0.29533504/2349969.7,
          'ttZ': lumi*0.5297/96388.9,
          'WJ':lumi*2788/22337264.0,
          'ZJ':lumi*5.67/236659.25,
          'tW': lumi*35.85/981694.75,
          'tbarW':lumi*35.85/982836.12,
          't':lumi*136.02/5945145.00,
          'tbar':lumi*80.95/3899488.5 ,
          's':lumi*10.32/1437229.5,
          'WW':lumi*118.7/4128682.5,
          'WZ':lumi*47.13/3993778.75,
          'data':1.0,
          'ZZ':lumi*16.523/1920398.0,
          'QCD300':lumi*351300.0/54500812.0,
          'QCD500':lumi*31630.0/62178097.0,
          'QCD700':lumi*6802.0/45018815.0,
          'QCD1000':lumi*1206.0/15112403.0,
          'QCD1500':lumi*0.9*120.4/3970702.0,
          'QCD2000':lumi*0.9*25.25/1979791.0,

          }
dnames = {
    'data':'data_obs',
    'ttlf':'ttlf',
    'diboson':'VV',
    'ttV':'ttV',
    'VJ':'VJ',
    'stop':'stop',
    'QCD':'QCD',
    'ttcc':'ttcc',
    'ttbb':'ttbb',
    'tt2b':'tt2b',
    'ttb':'ttb',
    'ttH':'ttH'} #Dataset names and their names in the datacards

# qwfac = { #prob_chi2>0.2
#     'WJ': 0.891208134818,
#     'ZJ': 0.933228907651,
#     'data': 1.0,
#     'WW': 0.921460659524,
#     'WZ': 0.945803465884,
#     'ZZ': 0.869776428127,
#     't': 0.896437171747,
#     'tbar': 0.921653019887,
#     's': 0.899637474409,
#     'tW': 0.875191845524,
#     'tt2b': 0.894844861029,
#     'ttH': 0.937842962103,
#     'ttW': 0.877582806907,
#     'ttZ': 0.901969884209,
#     'ttb': 0.902584058126,
#     'ttbb': 0.918964950004,
#     'ttcc': 0.906415849292,
#     'ttlf': 0.875414399205,
#
# }

qwfac = { #prob_chi2>1e-6
    'WJ': 0.909270336878,
    'ZJ': 0.923232387569,
    'data': 1.0,
    'QCD300': 1.0,
    'QCD500': 1.0,
    'QCD700': 1.0,
    'QCD1000': 1.0,
    'QCD1500': 1.0,
    'QCD2000': 1.0,
    'WW': 0.773832381864,
    'WZ': 0.848429300043,
    'ZZ': 0.912756292761,
    't':  0.909784244006,
    'tbar': 0.938400174879,
    's': 0.933086054052,
    'tW': 0.865644971649,
    'tt2b': 0.914409892575,
    'ttH': 0.944726916294,
    'ttW': 0.86931371544,
    'ttZ': 0.903248349429,
    'ttb':  0.916836322217,
    'ttbb': 0.927125951203,
    'ttcc': 0.918830943334,
    'ttlf': 0.890859279148,

}

# qwfac = { #3bs
#     'WJ': 0.913501612827,
#     'ZJ': 0.890945016621,
#     'data': 1.0,
#     'WW': 0.748665695891,
#     'WZ': 0.62204479258,
#     'ZZ':  0.84521596196,
#     't': 0.912202108736,
#     'tbar': 0.941838030321,
#     's': 1.02275575709,
#     'tW': 0.894446907321,
#     'tt2b': 0.921891102397,
#     'ttH': 0.949556331538,
#     'ttW': 0.900034490446,
#     'ttZ': 0.951695329837,
#     'ttb': 0.919050040246,
#     'ttbb': 0.931040158441,
#     'ttcc': 0.924329225225,
#     'ttlf': 0.900362305412,
#
# }

# qwfac = { #prob_chi2 > 0.2
#     'WJ': 1.10947368421,
#     'ZJ': 1.06189751395,
#     'data': 1.0,
#     'WW': 0.975945017182,
#     'WZ': 1.04049844237,
#     'ZZ': 0.975138121547,
#     't': 1.03058579575,
#     'tbar': 1.05762987013,
#     's': 1.01131541726,
#     'tW': 1.02949208083,
#     'tt2b': 1.04099432943,
#     'ttH': 1.06368516666,
#     'ttW': 1.05996290954,
#     'ttZ': 1.07525799868,
#     'ttb': 1.04099432943,
#     'ttbb': 1.04099432943,
#     'ttcc': 1.04099432943,
#     'ttlf': 1.04099432943,
#
# }
#

LHE_fac={
    '_LHEPDFweight_Up':108448.13/112067.03,
    '_LHEPDFweight_Down':108448.13/104891.77,
    '_LHE_factweight_Up':52973.871/50933.928,
    '_LHE_factweight_Down':52973.871/55511.524,
    '_LHE_renormweight_Up':52973.871/46472.543,
    '_LHE_renormweight_Down':52973.871/60858.439,

}
processgroup = {'diboson':['WW','WZ','ZZ'],'stop':['t','tbar','s','tW'],'ttV':['ttW','ttZ'],'VJ':['WJ','ZJ'],'QCD':['QCD300','QCD300','QCD500','QCD700','QCD1000','QCD1500']}

ttplot=['ttbb', 'tt2b', 'ttb', 'ttcc', 'ttlf']
#plotCosmetics ={'ttbar':['t#bar{t}+lf','#fcbba1'], 'ttbarcc':['t#bar{t}+c#bar{c}','#fc9272'], 'ttbarb':['t#bar{t}+b','#fb6a4a'], 'ttbar2b':['t#bar{t}+2b','#ef3b2c'], 'ttbarbb':['t#bar{t}+b#bar{b}','#cb181d'],'QCD':['Multijet','#1b9e77']}
plotCosmetics ={'ttlf':['t#bar{t}+lf','#fcbba1'], 'ttcc':['t#bar{t}+c#bar{c}','#fc9272'], 'ttb':['t#bar{t}+b','#fb6a4a'], 'tt2b':['t#bar{t}+2b','#ef3b2c'], 'ttbb':['t#bar{t}+b#bar{b}','#cb181d'],'diboson':['Diboson','#e7e1ef'],'stop':['Single Top','#c51b8a'],'ttV':['t#bar{t}+V','#ffeda0'],'VJ':['V+jets','#feb24c'],'QCD':['Multijet','#1b9e77'],'data':['Data','#1b9e77'],'ttH':['ttH','#1b239e']}
ttCls = {'ttbb':'ttCls>52','tt2b':'ttCls==52','ttb':'ttCls==51','ttcc':'ttCls>0 && ttCls<46','ttlf':'ttCls==0'}
#ttCls = {'ttbb':'ttCls>=51','ttcc':'ttCls>0 && ttCls<46','ttlf':'ttCls==0'}
vartitle = {'chi2': ['#chi^{2}', (20, 0, 20),1],
            'prob_chi2': ['Prob(#chi^{2})', (100, 0, 1),1],
            'trigweight': ['Trigger scale factor', (10, 0.9, 1.08),1],
            'h1_m': ['H1 mass', (20, 50, 200),1],
            'h2_m': ['H2 mass', (20, 50, 200),1],
            'tprime1_m': ['T1 mass', (20, 500, 800),0],
            'tprime2_m': ['T2 mass', (20, 500, 800),0],
            'n_jets': ['Jet Multiplicity', (6, 8, 14),1],
            'wkin': ['W_{Kin}', (20, 0, 1),1],
            'ht': ['HT (GeV)', (20, 500, 2200),1],
            'catplot':['',(10,1,11),1],
            'delta_w1M':['#Delta_{m}(W_{fit}, W_{rec})',(20,-200,60),1],
            'top1_m':['leading top mass (GeV)',(20,100,250),1],
            'top2_m':['second leading top mass (GeV)',(20,100,250),0],
            'w1_m':['leading w mass (GeV)',(20,40,120),0],
            'w2_m':['second leading w mass (GeV)',(20,40,120),0],
            'q1b2_mass':['l1 + b1 invariant mass (GeV)',(20,20,120),1],
            'p1b1_mass':['j1 + b1 invariant mass (GeV)',(20,20,250),1],
            'b1_pull_Et':['leading b-jet pull for Et',(20,-5,5),1],
            'b1_pt':['leading b-jet pt',(20,30,300),1],
            'b2_pt':['second leading b-jet pt',(20,30,300),1],
            'simple_chi2':['#chi^{2}',(20,0,38),1],
            'bdtComb':['BDT',(20,-0.5,0.5),1],
            'mindeltaRb1p':['Min. #Delta_{R}(b_{1},l_{1}, l_{2})',(20,0.4,5),1],
            'mindeltaRb2q':['Min. #Delta_{R}(b_{2},l_{3}, l_{4})',(20,0.4,5),1],
            'deltaRb1b2':['#Delta_{R}(b_{1},b_{2})',(20,0.4,5),0],
            'deltaRb1top2':['#Delta_{R}(b_{1},top_{2})',(20,0.4,5),1],
            'deltaRb2top1':['#Delta_{R}(b_{2},top_{1})',(20,0.4,5),1],
            'deltaRb2q1':['#Delta_{R}(b_{2},l_{3})',(20,0.4,5),1],
            'deltaRb1w1':['#Delta_{R}(b_{1},W_{1})',(20,0.4,5),1],
            'deltaRb1q1':['#Delta_{R}(b_{1},l_{1})',(20,0.4,5),1],
            'deltaRb2w2':['#Delta_{R}(b_{2},W_{2})',(20,0.4,5),1],
            'deltaRb1w2':['#Delta_{R}(b_{1},W_{2})',(20,0.4,5),1],
            'deltaRb2w1':['#Delta_{R}(b_{2},W_{1})',(20,0.4,5),1],
            'deltaRb2p1':['#Delta_{R}(b_{2},l_{1})',(20,0.4,5),1],
            'deltaRp1p2':['#Delta_{R}(p_{1},p_{2})',(20,0.4,5),1],
            'deltaRq1q2':['#Delta_{R}(q_{1},q_{2})',(20,0.4,5),1],
            'jets_dRavg':['Average #Delta_{R} between all jets',(20,0.4,5),1],
            'jets_dRmax':['Max #Delta_{R} between all jets',(20,0.4,5),1],
            'jets_dRmin':['Min #Delta_{R} between all jets',(20,0.4,5),1],
            'n_bjets':['b-jet Multiplicity',(4,2,6),1],
            'nBCSVM':['b-jet Multiplicity',(4,2,6),1],
            'exp(-chi2/4)':['P_{gof}',(20,0,0.001),1],
            'b1_csv':['leading top b CSV',(20,0.8484,1),1],
            'b2_csv':['second leading top b CSV',(20,0.8484,1),1],
            'addJet_CSV[0]':['leading additional jet CSV',(15,0.0,1),0],
            'addJet_CSV[1]':['second leading additional jet CSV',(15,0.0,1),0],
            'addJet_deltaR':['#Delta_{R}(add_{1},add_{2})',(20,0.4,5),0],

            'n_addJets':['Number of additional jets',(9,0,9),1],
            'n_addbjets':['Number of additional b-jets',(5,0,5),1],
            'BDT_Class[0]':['BDT for ttbar classification',(3,0,3),1],
            'BDT_ClassMajo[0]':['Majority vote BDT for ttbar classification',(3,0,3),1],
            'BDT_QCD':['BDT for QCD rejection',(20,-1,1),1],
            'BDT_FullQCD':['Combined BDT for QCD rejection',(1000,-1,1),1],
            'PyDNN_FullQCD':['Combined DNN for QCD rejection',(1000,0,1),1],
            'BDT_QCDData':['Data driven BDT for QCD rejection',(20,-1,1),0],
            'BDT_CWoLa':['CWoLa BDT ',(30,-0.4,0.7),0],
            'BDT_CWoLa_Sec':['Data driven BDT ',(1000,-0.4,0.7),1],
            'BDTFish_CWoLa':['Data driven BDT ',(1000,-0.4,0.7),1],
            'PyForest_CWoLa':['Data driven RF ',(2000,-0.4,0.7),1],
            'BDT_QCDCWoLa2':['Data driven BDT for QCD rejection 2 ',(1000,-1,1),0],
            'Fish_CWoLa':['Data driven LD for QCD rejection ',(2000,-1,1),0],
            'BDT_Comb':['BDT for permutations',(30,-1,1),1],
            'BDT_ttbar':['BDT for ttbar rejection',(20,-1,1),1],
            'BDT_ttcc':['BDT for ttcc rejection',(5,-1,1),1],
            'LH_ttall':['Likelihood for ttbar inc. rejection',(5,-1,1),1],
            'PyDNN_CWoLa':['Data driven DNN ',(2000,0,1),1],
            'BDT_QCD_avg':['Average BDT for QCD rejection',(5,-1,1),1],
            'BDT_ttall_avg':['Average BDT for ttbar inc. rejection',(5,-1,1),1],
            'BDT_ttbar_avg':['Average BDT for ttbar rejection',(5,-1,1),1],
            'BDT_ttbarMajo':['Average BDT for ttbar rejection',(20,-1,1),1],
            'BDT_ttcc_avg':['Average BDT for ttcc rejection',(5,-1,1),1],
            'LH_ttall_avg':['Average Likelihood for ttbar inc. rejection',(5,-1,1),1],
            'qgLR':['QGLR(4udcs,0udcs)',(20,0,1),1],
            'memttbb':['mem',(20,0,1),1],
            'girth':['girth',(20,0,0.5),1],
            'top1_pt':['leading top p_{t}',(20,40,800),1],
            'top2_pt':['second leading top p_{t}',(20,40,800),1],
            'deltaRb1b2':['#Delta_{R}(b_{1},b_{2})',(20,0.4,5),1],
            'deltaRaddb1':['#Delta_{R}(add.{1},b_{1})',(20,0.4,5),1],
            'deltaRaddb2':['#Delta_{R}(add.{1},b_{2})',(20,0.4,5),1],
            'deltaRaddtop2':['#Delta_{R}(add.{1},top_{2})',(20,0.4,5),1],
            'deltaRaddtop1':['#Delta_{R}(add.{1},top_{1})',(20,0.4,5),1],
            'deltaPhiw1w2':['#Delta_{#phi}(W_{1},W_{2})',(20,0,3),1],
            'deltaPhit1t2':['#Delta_{#phi}(t_{1},t_{2})',(20,0,3),1],
            'deltaPhib1b2':['#Delta_{#phi}(b_{1},b_{2})',(20,0,3),1],
            'deltaPhip1p2':['#Delta_{#phi}(l_{1},l_{2})',(20,0,3),1],
            'deltaPhiq1q2':['#Delta_{#phi}(l_{3},l_{4})',(20,0,3),1],
            'addJet_deltaPhi':['#Delta_{#phi}(add_{1},add_{2})',(20,0,3),1],
            'addJet_deltaEta':['#Delta_{#eta}(add_{1},add_{2})',(20,-2.5,2.5),1],
            'addJet_mass':['#mass(add_{1},add_{2})',(20,10,100),1],
            'addJet_eta[0]':['leading additional jet eta)',(20,-2.5,2.5),1],
            'addJet_eta[1]':['second leading additional jet eta',(20,0,3),1],
            'deltaEtap1p2':['#Delta_{#eta}(l_{1},l_{2})',(20,-2.5,2.5),1],
            'deltaEtaq1q2':['#Delta_{#eta}(q_{1},q_{2})',(20,-2.5,2.5),1],
            'deltaEtab1b2':['#Delta_{#eta}(b_{1},b_{2})',(20,0,3),1],
            'deltaEtat1t2':['#Delta_{#eta}(top_{1},top_{2})',(20,0,3),1],
            'deltaEtaw1w2':['#Delta_{#eta}(W_{1},W_{2})',(20,0,3),1],
            'addJet_pt[0]':['leading additional jet p_{t}',(20,40,400),1],
            'addJet_pt[1]':['second leading additional jet p_{t}',(20,40,400),1],
            'btagLR4b':['BLR(4b,2b)',(20,0.1,1),1],
            'btagLR3b':['btagLR3b',(20,0.1,1),0],
            'centrality':['Centrality',(20,0.2,1.2),1],
            'aplanarity':['Aplanarity',(20,0.0,0.5),1],
            'meanDeltaRbtag':['mean #Delta_{R} tagged jets',(20,0.4,4),1],
            'meanCSV':['mean CSV tagged jets',(20,0.84,1),1],
            'meanCSVbtag':['mean CSV ',(20,0.4,0.9),1],
            'jet_CSV[0]':['CSV of jet 1',(20,0.4,0.9),1],
            'jet_CSV[1]':['CSV of jet 2',(20,0.4,0.9),1],
            'jet_CSV[2]':['CSV of jet 3',(20,0.4,0.9),1],
            'jet_CSV[3]':['CSV of jet 4',(20,0.4,0.9),1],
            'jet_CSV[4]':['CSV of jet 5',(20,0.4,0.9),1],
            'jet_CSV[5]':['CSV of jet 6',(20,0.4,0.9),1],
            'jet_DeepCSV[0]':['Deep CSV of jet 1',(20,0.4,0.9),1],
            'jet_DeepCSV[1]':['Deep CSV of jet 2',(20,0.4,0.9),1],
            'jet_DeepCSV[2]':['Deep CSV of jet 3',(20,0.4,0.9),1],
            'jet_DeepCSV[3]':['Deep CSV of jet 4',(20,0.4,0.9),1],
            'jet_DeepCSV[4]':['Deep CSV of jet 5',(20,0.4,0.9),1],
            'jet_DeepCSV[5]':['Deep CSV of jet 6',(20,0.4,0.9),1],

            'jet_QGL[0]':['QGL of jet 1',(20,0.4,0.9),1],
            'jet_QGL[1]':['QGL of jet 2',(20,0.4,0.9),1],
            'jet_QGL[2]':['QGL of jet 3',(20,0.4,0.9),1],
            'jet_QGL[3]':['QGL of jet 4',(20,0.4,0.9),1],
            'jet_QGL[4]':['QGL of jet 5',(20,0.4,0.9),1],
            'jet_QGL[5]':['QGL of jet 6',(20,0.4,0.9),1],
            'all_mass':['Invariant mass of all jets (GeV)',(20,400,2000),1],
            'tt_m':['Invariant mass of ttbar system (GeV)',(20,400,2000),1],
            'tt_phi':['tt phi',(20,-3,3),1],
            'lq1_m':['Invariant mass of light jet 1 (GeV)',(20,0,100),1],
            'lq2_m':['Invariant mass of light jet 2 (GeV)',(20,0,100),1],
            'lp1_m':['Invariant mass of light jet 3 (GeV)',(20,0,100),1],
            'lp2_m':['Invariant mass of light jet 2 (GeV)',(20,0,100),1],
            'lq1_eta':['light jet 5 eta',(20,-2.5,2.5),1],
            'lq2_eta':['light jet 6 eta',(20,-2.5,2.5),1],
            'lp1_eta':['light jet 3 eta',(20,-2.5,2.5),1],
            'lp2_eta':['light jet 4 eta',(20,-2.5,2.5),1],
            'lq1_phi':['light jet 1 phi',(20,-3,3),1],
            'lq2_phi':['light jet 2 phi',(20,-3,3),1],
            'lp1_phi':['light jet 3 phi',(20,-3,3),1],
            'lp2_phi':['light jet 4 phi',(20,-3,3),1],

            'BDT_ttbb_All':['BDT for ttbar inc. rejection',(5,0,5),1],
            'BDT_ttbb3b':['Multiclass BDT',(5,0,5),1],
            'BDT_ttbb7j':['Multiclass BDT 7j',(5,0,5),1],
            'BDT_ttbb8j':['Multiclass BDT 8j',(5,0,5),1],
            'BDT_ttbb9j':['Multiclass BDT 9j',(5,0,5),1],
            'PyDNN_ttbb7j':['Multiclass DNN 7j',(5,0,5),1],
            'PyDNN_ttbb8j':['Multiclass DNN 8j',(5,0,5),1],
            'PyDNN_ttbb9j':['Multiclass DNN 9j',(5,0,5),1],

            'lq1_pt':['light jet 1 pt',(20,30,200),1],
            'lq2_pt':['light jet 2 pt',(20,30,200),1],
            'lp1_pt':['light jet 3 pt',(20,30,200),1],
            'lp2_pt':['light jet 4 pt',(20,30,200),1],
            'jet5pt':['5th pt',(20,30,200),1],
            'minjetpt':['min pt',(20,30,200),1],
            'w1_pt':['leading w pt',(20,30,300),1],
            'w2_pt':['second leading w pt',(20,30,300),1],
            'w1_eta':['leading w eta',(20,0,3),1],
            'w1_phi':['leading w phi',(20,-3,3),1],
            'w2_phi':['second leading w phi',(20,-3,3),1],
            'w2_eta':['second leading w eta',(20,0,3),1],
            'top1_eta':['leading top eta',(20,0,3),1],
            'top2_eta':['second leading top eta',(20,0,3),1],
            'top1_phi':['leading top phi',(20,-3,3),1],
            'top2_phi':['second leading top phi',(20,-3,3),1],

            'deltaEtaaddb1':['delta eta add. and leading b',(20,0,3),1],
            'deltaEtaaddb2':['delta eta add. and leading b',(20,0,3),1],
            'tt_pt':['ttbar system pt (GeV/c)',(20,100,2000),1],
            'tt_eta':['ttbar system eta',(20,0,3),1],
            'b1_eta':['jet 1 eta',(20,-2.5,2.5),1],
            'b2_eta':['jet 2 eta',(20,-2.5,2.5),1],
            'b1_phi':['leading b-jet phi',(20,-3,3),1],
            'b1_m':['leading b-jet m',(20,0,20),],
            'b2_m':['second leading b-jet m',(20,0,20),1],
            'b2_phi':['second leading b-jet phi',(20,-3,3),1],

            'closest_mass':['Invariant mass of closes jet pair (GeV)',(20,20,120),1],
            'jet_MOverPt[0]':['jet 1 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[1]':['jet 2 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[2]':['jet 3 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[3]':['jet 4 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[4]':['jet 5 mass/Pt',(20,0.0,0.4),1],
            'jet_MOverPt[5]':['jet 6 mass/Pt',(20,0.0,0.4),1],
            'mass':['Generalized angularity mass',(20,0.0,1.0),1],
            'width':['Generalized angularity width',(20,0.0,1.0),1],
            'ptD':['Generalized angularity ptD',(20,0.0,1.0),1],
            'LHA':['Generalized angularity LHA',(20,0.0,1.0),1],
            'soft_eta1':['Generalized angularity soft_eta1',(20,0.0,1.0),1],
            'soft_eta2':['Generalized angularity soft_eta2',(20,0.0,1.0),1],
            'sphericity':['sphericity',(20,0.0,1.0),1]


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
    col = table['Process']

    newlist = []
    mc = []
    for key in rows:
        newlist.append(table[key])

    dummy = []
    for i, s in enumerate(table['Total bkg.']):
        dummy+= [str(round(table['Total bkg.'][i],2)) + '$pm$'+str(round(table['Total err'][i],2))]

    pframe= pd.DataFrame(data=newlist,
                 index=rows,
                 columns=col)

    pframe.loc['Total bkg.']=dummy
    nindex = ['Multijet','ttH','t#bar{t}+lf', 't#bar{t}+c#bar{c}', 'Single Top','t#bar{t}+V','V+jets','Diboson','Total bkg.', 't#bar{t}+b#bar{b}','t#bar{t}+2b', 't#bar{t}+b', 'Data']





    pframe = pframe.reindex(index = nindex)

    # pbkg= pd.DataFrame(data=mc,
    #                      index=['Total Simulation'],
    #                      columns=col)
    # pframe.append(pbkg)

    table_text =  pframe.to_latex()
    print table_text
