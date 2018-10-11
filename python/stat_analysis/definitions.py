import CombineHarvester.CombineTools.ch as ch

bkg_processes_mc = [
        'ttlf',
        'ttcc',
        'stop',
        'VJ',
        'VV',
        'ttV',
        'ttH'
    ]

# FIXME
sig_processes = [
        'ttbb',
        # 'ttb',
        # 'tt2b'
]

exp_systs = [
        'CMS_btag_hf',
        'CMS_btag_hfstats1',
        'CMS_btag_hfstats2',
        'CMS_btag_lf',
        'CMS_btag_lfstats1',
        'CMS_btag_lfstats2',
        'CMS_btag_cferr1',
        'CMS_btag_cferr2',
        
        'CMS_qg_Weight',
        'CMS_pu_Weight',
        'CMS_trig_Weight',

        'CMS_AbsoluteStat_j',
        'CMS_AbsoluteScale_j',
        'CMS_AbsoluteMPFBias_j',
        'CMS_Fragmentation_j',
        'CMS_SinglePionECAL_j',
        'CMS_SinglePionHCAL_j',
        'CMS_FlavorQCD_j',
        'CMS_TimePtEta_j',
        'CMS_RelativeJEREC1_j',
        'CMS_RelativeJEREC2_j',
        'CMS_RelativeJERHF_j',
        'CMS_RelativePtBB_j',
        'CMS_RelativePtEC1_j',
        'CMS_RelativePtEC2_j',
        'CMS_RelativePtHF_j',
        # relativebal?
        'CMS_RelativeFSR_j',
        'CMS_RelativeStatFSR_j',
        'CMS_RelativeStatEC_j',
        'CMS_RelativeStatHF_j',
        'CMS_PileUpDataMC_j',
        'CMS_PileUpPtRef_j',
        'CMS_PileUpPtBB_j',
        'CMS_PileUpPtEC1_j',
        # 'CMS_PileUpPtEC2_j', # removed because zero
        'CMS_PileUpPtHF_j',
        
        'CMS_JER_j',
    ]

theory_shape_systs = [
        (['ttbb', 'ttcc', 'ttlf'], 'CMS_top_Weight'),
        
        # FIXME all shapes variations are normalised to the same yield
        # lnN nuisances take care of the yield
        # -> should be a single nuisance
        # FIXME should not correlate QCD scale across ttX processes?
        (['ttbb', 'ttcc', 'ttlf', 'ttV'], 'QCD_scale_tt'),
        (['ttH'], 'QCD_scale_ttH'),
        (['stop'], 'QCD_scale_t'),
        (['VV'], 'QCD_scale_VV'),
        (['VJ'], 'QCD_scale_V'),
        (['ttbb', 'ttcc', 'ttlf', 'ttV'], 'pdf_gg'),
        (['ttV', 'VV', 'VJ'], 'pdf_qqbar'),
        (['stop'], 'pdf_qg'),
        
        # FIXME NOT actual shape uncertainties!
        # -> should have simple lnN
        (['ttbb'], 'ttbb_FSR'),
        (['ttbb'], 'ttbb_ISR'),
        (['ttbb'], 'ttbb_tune'),
        (['ttbb'], 'ttbb_hdamp'),
        (['ttcc'], 'ttcc_FSR'),
        (['ttcc'], 'ttcc_ISR'),
        (['ttcc'], 'ttcc_tune'),
        (['ttcc'], 'ttcc_hdamp'),
        (['ttlf'], 'ttlf_FSR'),
        (['ttlf'], 'ttlf_ISR'),
        (['ttlf'], 'ttlf_tune'),
        (['ttlf'], 'ttlf_hdamp'),
    ]

theory_rate_systs = {
        # FIXME 50% uncertainty on ttcc
        'ttcc_norm': ('lnN', ch.SystMap('process')(['ttcc'], 1.5)),
    }

def getLumiUncertainty(era):
    if era == "13TeV_2016":
        return 1.025
    else:
        raise Exception("Era {} not known".format(era))
