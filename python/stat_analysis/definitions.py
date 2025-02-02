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
        'tt2b'
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
        'CMS_L1_Weight',

        # 'CMS_Total_j', # TOTAL JEC
        'CMS_AbsoluteStat_j',
        'CMS_AbsoluteScale_j',
        'CMS_AbsoluteMPFBias_j',
        'CMS_Fragmentation_j',
        'CMS_SinglePionECAL_j',
        'CMS_SinglePionHCAL_j',
        'CMS_FlavorQCD_j',
        'CMS_TimePtEta_j',
        # 'CMS_RelativeJEREC1_j', # almost zero?
        # 'CMS_RelativeJEREC2_j', # zero?
        # 'CMS_RelativeJERHF_j', # zero?
        'CMS_RelativePtBB_j',
        'CMS_RelativePtEC1_j',
        # 'CMS_RelativePtEC2_j', # zero?
        # 'CMS_RelativePtHF_j', # zero?
        'CMS_RelativeBal_j',
        'CMS_RelativeFSR_j',
        'CMS_RelativeStatFSR_j',
        'CMS_RelativeStatEC_j',
        # 'CMS_RelativeStatHF_j', # zero?
        'CMS_PileUpDataMC_j',
        'CMS_PileUpPtRef_j',
        'CMS_PileUpPtBB_j',
        'CMS_PileUpPtEC1_j',
        # 'CMS_PileUpPtEC2_j', # not even produced because zero
        # 'CMS_PileUpPtHF_j', # zero?
        
        'CMS_JER_j',
    ]

theory_shape_systs = [
        (tt_bkg + sig_processes, 'CMS_top_Weight'),
        (tt_bkg + sig_processes, 'CMS_LHEscale_Weight'),
        (tt_bkg + sig_processes, 'CMS_LHEPDF_Weight'),
]

theory_rate_systs = {
        # FIXME 50% uncertainty on ttcc?
        'ttcc_norm': ('lnN', ch.SystMap('process')(['ttcc'], 1.5)),

        'pdf_gg': ('lnN', ch.SystMap('process')
                            (['ttV'], 1.03)
                        ),
        
        'pdf_gg_ttH': ('lnN', ch.SystMap('process')
                            (['ttH'], 1.036)
                        ),
        
        'pdf_qg': ('lnN', ch.SystMap('process')
                            (['stop'], 1.03)
                        ),
        
        'pdf_qqbar': ('lnN', ch.SystMap('process')
                            (['VJ'], 1.04)
                            (['VV'], 1.02)
                            (['ttV'], 1.02)
                        ),

        'QCD_scale_ttH': ('lnN', ch.SystMap('process')
                             (['ttH'], (0.908, 1.058))
                        ),
        
        'QCD_scale_t': ('lnN', ch.SystMap('process')
                             (['stop'], (0.98, 1.03))
                        ),
        
        'QCD_scale_V': ('lnN', ch.SystMap('process')
                             (['VJ'], 1.01)
                        ),
        
        'QCD_scale_VV': ('lnN', ch.SystMap('process')
                             (['VV'], 1.02)
                        ),
        
    }

# Will be frozen for all fits!
# Impact estimated by repeating fit while shifting nuisance up and down
externalised_nuisances = [
    'CMS_top_Weight',
    'GluonMoveCRTune',
    'QCDbasedCRTune',
    'GluonMoveCRTune_erdON',
    'erdOn',
    'lumi_13TeV_2016',
]

# Decorrelated theory uncertainties between various ttXX components (separately signals, ttcc and ttjj)
class FactorisedTheory:

    def __init__(self, strategy):
        if strategy is None or strategy == "":
            self.factorised_uncertainties = []
            self.groups = {}
        else:
            self.factorised_uncertainties = [
                "CMS_LHEscale_Weight",
                "fsr",
                "isr",
                "hdamp",
            ]
        
        # common nuisance for all tt(2)b(b), not used anymore
        if strategy == "some":
            self.groups = {
                'ttbb': ['ttbb', 'ttbb_other', 'ttb_other', 'tt2b'],
                'ttcc': ['ttcc'],
                'ttlf': ['ttlf']
            }
        
        elif strategy == "all":
            self.groups = {
                'ttbb': ['ttbb'],
                'ttbb_other': ['ttbb_other'],
                'ttb_other': ['ttb_other'],
                'tt2b': ['tt2b'],
                'ttcc': ['ttcc'],
                'ttlf': ['ttlf']
            }
        
        elif strategy == "all_tt2b":
            self.groups = {
                'ttbb': ['ttbb'],
                'ttbb_other': ['ttbb_other'],
                'ttb': ['ttb_other', 'tt2b'],
                'ttcc': ['ttcc'],
                'ttlf': ['ttlf']
            }
    
        elif strategy == "OOA":
            self.groups = {
                'ttbb': ['ttbb'],
                'ttbb_other': ['tt2b', 'ttb_other', 'ttbb_other'],
                'ttcc': ['ttcc'],
                'ttlf': ['ttlf']
            }

        elif strategy == "none":
            self.groups = { 'all': ['ttbb', 'ttbb_other', 'ttb_other', 'tt2b', 'ttcc', 'ttlf'] }

        self.processes = []
        for gr in self.groups.values():
            for p in gr:
                self.processes.append(p)
        if len(self.processes) != len(set(self.processes)):
            raise Exception

    def getGrouping(self, procs, nuis):
        if nuis not in self.factorised_uncertainties:
            return [(procs, nuis)]

        newNysts = {}
        for proc in procs:
            if proc not in self.processes:
                newNysts.setdefault(nuis, set()).add(proc)
            else:
                for postfix, group in self.groups.items():
                    if proc in group:
                        newNysts.setdefault(nuis + '_' + postfix, set()).add(proc)
        return [ (list(procs), nuis) for nuis,procs in newNysts.items() ]

    def getNewNuisance(self, nuis, proc):
        if nuis in self.factorised_uncertainties:
            for postfix, procList in self.groups.items():
                if proc in procList:
                    return nuis + '_' + postfix
        return nuis

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
