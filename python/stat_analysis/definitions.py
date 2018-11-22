import CombineHarvester.CombineTools.ch as ch
import itertools

tt_bkg = [
        'ttcc',
        'ttlf',
    ]

# FIXME
sig_processes = [
        'ttbb',
        'ttbb_other',
        'ttb_other',
        # 'tt2b'
    ]

other_bkg = [
        'stop',
        'VJ',
        'VV',
        'ttV',
        'ttH'
    ]

exp_systs = [
        'CMS_btag_hf',
        # 'CMS_btag_hfstats1',
        # 'CMS_btag_hfstats2',
        # 'CMS_btag_lf',
        # 'CMS_btag_lfstats1',
        # 'CMS_btag_lfstats2',
        'CMS_btag_cferr1',
        'CMS_btag_cferr2',
        
        'CMS_qg_Weight',
        'CMS_pu_Weight',
        # 'CMS_trig_Weight',

        # 'CMS_AbsoluteStat_j',
        # 'CMS_AbsoluteScale_j',
        # 'CMS_AbsoluteMPFBias_j',
        # 'CMS_Fragmentation_j',
        # 'CMS_SinglePionECAL_j',
        # 'CMS_SinglePionHCAL_j',
        # 'CMS_FlavorQCD_j',
        # 'CMS_TimePtEta_j',
        # # 'CMS_RelativeJEREC1_j', # almost zero?
        # # 'CMS_RelativeJEREC2_j', # zero?
        # # 'CMS_RelativeJERHF_j', # zero?
        # 'CMS_RelativePtBB_j',
        # 'CMS_RelativePtEC1_j',
        # # 'CMS_RelativePtEC2_j', # zero?
        # # 'CMS_RelativePtHF_j', # zero?
        # 'CMS_RelativeBal_j',
        # 'CMS_RelativeFSR_j',
        # 'CMS_RelativeStatFSR_j',
        # 'CMS_RelativeStatEC_j',
        # # 'CMS_RelativeStatHF_j', # zero?
        # 'CMS_PileUpDataMC_j',
        # 'CMS_PileUpPtRef_j',
        # 'CMS_PileUpPtBB_j',
        # 'CMS_PileUpPtEC1_j',
        # # 'CMS_PileUpPtEC2_j', # not even produced because zero
        # # 'CMS_PileUpPtHF_j', # zero?
        
        # 'CMS_JER_j',
    ]

theory_shape_systs = [
        # (tt_bkg + sig_processes, 'CMS_top_Weight'),
        # (tt_bkg + sig_processes + ['ttH'], 'CMS_LHEscale_Weight'),
        # (tt_bkg + sig_processes + ['ttH'], 'CMS_LHEPDF_Weight'),
]

# Only used for "shape_direct" method!
fake_lnN_systs = [        
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
        (['ttbb_other'], 'ttbb_other_FSR'),
        (['ttbb_other'], 'ttbb_other_ISR'),
        (['ttbb_other'], 'ttbb_other_tune'),
        (['ttbb_other'], 'ttbb_other_hdamp'),
        (['ttb_other'], 'ttb_other_FSR'),
        (['ttb_other'], 'ttb_other_ISR'),
        (['ttb_other'], 'ttb_other_tune'),
        (['ttb_other'], 'ttb_other_hdamp'),
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
        # FIXME 50% uncertainty on ttcc?
        'ttcc_norm': ('lnN', ch.SystMap('process')(['ttcc'], 1.5)),

        # All uncorrelated between ttlf, ttcc, ttbb
        # '$PROCESS_FSR': ('lnN', ch.SystMap('process')
                             # (['ttbb'], (0.93, 1.07))
                             # (['ttcc'], (0.91, 1.09))
                             # (['ttlf'], (0.82, 1.09))
                        # ),
        
        # '$PROCESS_ISR': ('lnN', ch.SystMap('process')
                             # (['ttbb'], (0.90, 1.07))
                             # (['ttcc'], (0.96, 1.07))
                             # (['ttlf'], (0.95, 1.07))
                        # ),
        
        # '$PROCESS_tune': ('lnN', ch.SystMap('process')
                             # (['ttbb'], (0.99, 1.02))
                             # (['ttcc'], (0.98, 1.007))
                             # (['ttlf'], (0.99, 1.005))
                        # ),
        
        # '$PROCESS_hdamp': ('lnN', ch.SystMap('process')
                             # (['ttbb'], (0.92, 1.02))
                             # (['ttcc'], (0.92, 1.04))
                             # (['ttlf'], (0.93, 1.03))
                        # ),

        'pdf_gg': ('lnN', ch.SystMap('process')
                            # (['ttbb'], 1.04)
                            # (['ttcc'], 1.04)
                            # (['ttlf'], 1.04)
                            (['ttV'], 1.04)
                        ),
        
        'pdf_qg': ('lnN', ch.SystMap('process')
                            (['stop'], 1.03)
                        ),
        
        'pdf_qqbar': ('lnN', ch.SystMap('process')
                            (['VJ'], 1.04)
                            (['VV'], 1.02)
                            (['ttV'], 1.02)
                        ),

        # 'QCD_scale_tt': ('lnN', ch.SystMap('process')
                             # (['ttbb'], (0.96, 1.04))
                             # (['ttcc'], (0.96, 1.04))
                             # (['ttlf'], (0.96, 1.04))
                             # (['ttV'], (0.88, 1.13))
                        # ),
        
        'QCD_scale_t': ('lnN', ch.SystMap('process')
                             (['stop'], (0.98, 1.04))
                        ),
        
        'QCD_scale_V': ('lnN', ch.SystMap('process')
                             (['VJ'], 1.01)
                        ),
        
        'QCD_scale_VV': ('lnN', ch.SystMap('process')
                             (['VV'], 1.02)
                        ),
        
    }

def getNuisanceFromTemplate(key, syst):
    if '$PROCESS' not in key:
        return [ key ]
    sm = syst[1]
    procs = [ p[0] for p in sm.GetTupleSet() ]
    return [ key.replace('$PROCESS', p) for p in procs ]

theory_rate_list = list(itertools.chain.from_iterable(
                            map(getNuisanceFromTemplate, theory_rate_systs.keys(), theory_rate_systs.values())
                        ))

def getLumiUncertainty(era):
    if era == "13TeV_2016":
        return 1.025
    else:
        raise Exception("Era {} not known".format(era))
