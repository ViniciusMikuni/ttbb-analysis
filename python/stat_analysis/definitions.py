
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
        'ttb',
        'tt2b'
]

exp_systs = [
        'CMS_btag_hf',
        'CMS_btag_lf',
        'CMS_btag_cferr2',
        'CMS_qg_Weight'
    ]



def getLumiUncertainty(era):
    if era == "13TeV_2016":
        return 1.025
    else:
        raise Exception("Era {} not known".format(era))
