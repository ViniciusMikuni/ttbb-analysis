import ROOT as R
import os
import re

from HistogramTools import getEnvelopeHistograms, equaliseBins, openFileAndGet

def extractShapes(input_filename, output_filename, mc_backgrounds, mc_signals, real_data=False, fact_theory=None, lumi_scale=None, equal_bins=False, sub_folder=None):
    """
    Extract the shapes from input_filename and prepare them for combineHarvester in output_filename.
    The output file should contain directories named after the categories, containing histograms named as '$PROCESS' or '$PROCESS_$SYST(Up|Down)'

        - For now all existing templates for data and MC are copied
        - In the CR1 and SR, define 'delta' histograms named 'QCD_bin_{i=1..N}' that will serve to estimate QCD from a combined fit of CR1 and SR. Each histogram is zero everywhere but in bin i the yield is set as the estimated QCD in that bin (esimated = by subtraction in CR1 and CR2, and in SR and VR it's the from the corresponding CR scaled to the total expected)
        - If real_data is False, redefine data_obs in the SR as the sum of all background estimates (with QCD normalised to the total data in the SR)
        - lumi_scale: use to scale all yields by some factor
        - fact_theory: for given shape uncertainties, will add _process to histogram name for ttbb, ttcc and ttjj
        - equal_bins: if True, will recreate new histograms with equal-size bins (easier for plotting)
        - sub_folder: move into the sub-folder of the input ROOT file

    Returns:
        - a list of ratios QCD_data/QCD_est (per bin) in the VR, to define the systematic on QCD in the SR
        - the expected yields of QCD in the categories (estimated by subtraction)
        - the expected nominal shape of QCD in the SR
    """

    tf = openFileAndGet(input_filename)

    # Read all histograms, put them in a dictionary with key = category
    all_histos = {}
    est_QCD_yields = {}

    categories = ['CR1', 'CR2', 'VR', 'SR']
    
    for cat in categories:
        path = cat
        if sub_folder is not None:
            path = sub_folder + '/' + cat
        m_dir = tf.GetDirectory(path)
        all_histos[cat] = {}
        # print('Moving to {}'.format(cat))
        for key in m_dir.GetListOfKeys():
            th1 = key.ReadObj()
            if th1:
                th1.SetDirectory(R.nullptr)
                # print('Loading {}'.format(key.GetName()))
                # All histos must be positive...
                for i in range(th1.GetNbinsX() + 2):
                    if th1.GetBinContent(i) < 0: th1.SetBinContent(i, 0)
                if equal_bins:
                    myTH1 = equaliseBins(th1)
                else:
                    myTH1 = th1
                all_histos[cat][key.GetName()] = myTH1
                if lumi_scale:
                    myTH1.Scale(lumi_scale)
    tf.Close()

    Nbins = all_histos['SR']['data_obs'].GetNbinsX()

    # QCD scale envelopes
    scaleSyst = 'CMS_LHEscale_Weight'
    for cat in categories:
        variations = {} # maps process to list of variation histograms
        for key in all_histos[cat].keys():
            for proc in mc_backgrounds + mc_signals:
                if re.match("{}_{}[0-9]$".format(proc, scaleSyst), key):
                    variations.setdefault(proc, [])
                    variations[proc].append(all_histos[cat][key])

        to_remove = []
        for key, values in variations.items():
            if len(values) != 6:
                print("Warning: I was expecting 6 scale variations, but I got {} for {}".format(len(values), key))
                to_remove.append(key)

        for n in to_remove:
            del variations[n]
        
        for proc, var in variations.items():
            nominal = all_histos[cat][proc]
            
            up, down = getEnvelopeHistograms(nominal, var)
            
            up.SetName(nominal.GetName() + '_{}Up'.format(scaleSyst))
            down.SetName(nominal.GetName() + '_{}Down'.format(scaleSyst))

            all_histos[cat][up.GetName()] = up
            all_histos[cat][down.GetName()] = down

    # FIXME ugly hardcoded part
    # For theory uncertainties factorised among ttbar components
    if fact_theory is not None:
        for cat in categories:
            for name, hist in all_histos[cat].items():
                for proc in ['ttbb', 'ttbb_other', 'ttb_other', 'ttcc', 'ttlf']:
                    for syst in fact_theory:
                        for dire in ["Up", "Down"]:
                            if name == proc + "_" + syst + dire:
                                # FIXME common nuisance for ttbb templates?
                                if proc in ['ttbb', 'ttbb_other', 'ttb_other']: systProc = syst + "_ttbb"
                                else: systProc = syst + "_" + proc
                                newName = proc + "_" + systProc + dire
                                newHist = hist.Clone(newName)
                                all_histos[cat][newName] = newHist

    for cat in categories:
        # define sum of nominal backgrounds and signals
        total = all_histos[cat]['data_obs'].Clone('total')
        total.Reset()

        for proc in mc_backgrounds + mc_signals:
            total.Add(all_histos[cat][proc])
        all_histos[cat]['mc_total'] = total

        # define initial "nominal" QCD estimate by subtracting total from data
        QCD_subtr = all_histos[cat]['data_obs'].Clone('QCD_subtr')
        QCD_subtr.Add(total, -1)
        # check for negative bins, set to 1 by default
        for i in range(1, Nbins+1):
            if QCD_subtr.GetBinContent(i) <= 0:
                print("WARNING: region {}, bin {}: QCD subtr is negative!".format(cat, i))
                QCD_subtr.SetBinContent(i, 1.)
        all_histos[cat]['QCD_subtr'] = QCD_subtr
 
        est_QCD_yields[cat] = QCD_subtr.Integral()
        print('QCD yield estimated by subtraction in {}: {}'.format(cat, est_QCD_yields[cat]))

    # Estimate QCD in VR using CR2 (take shape & scale yields)
    QCD_est = all_histos['CR2']['QCD_subtr'].Clone('QCD_est')
    QCD_est.Scale(1./est_QCD_yields['CR2'])
    QCD_shape_CR2 = [ QCD_est.GetBinContent(i) for i in range(1, Nbins+1) ]
    QCD_est.Scale(est_QCD_yields['VR'])
    all_histos['VR']['QCD_est'] = QCD_est
    # print("QCD shape in CR2:")
    # print(QCD_shape_CR2)

    # Estimate QCD in SR using CR1 (take shape & scale yields)
    QCD_est = all_histos['CR1']['QCD_subtr'].Clone('QCD_est')
    QCD_est.Scale(1./est_QCD_yields['CR1'])
    QCD_shape_CR1 = [ QCD_est.GetBinContent(i) for i in range(1, Nbins+1) ]
    QCD_est.Scale(est_QCD_yields['SR'])
    all_histos['SR']['QCD_est'] = QCD_est
    # print("QCD shape in CR1:")
    # print(QCD_shape_CR1)

    # If fake data, define data_obs in SR as the sum of MC backgrounds plus QCD estimate
    # (so using shape from CR1 but overall normalisation from data in SR)
    # if not real_data:
        # for cat in ['SR', 'VR']:
            # data_obs = all_histos[cat]['data_obs']
            # data_obs.Reset()
            # data_obs.Add(all_histos[cat]['mc_total'])
            # data_obs.Add(all_histos[cat]['QCD_est'])
    # If fake data, define data_obs in SR as what the ABCD would give, and in the VR as sum of MC bkgs plus QCD est
    if not real_data:
        data_obs = all_histos["VR"]['data_obs']
        data_obs.Reset()
        data_obs.Add(all_histos["VR"]['mc_total'])
        data_obs.Add(all_histos["VR"]['QCD_est'])

        data_obs = all_histos["SR"]['data_obs']
        for i in range(1, Nbins + 1):
            data_obs.SetBinContent(i, all_histos['VR']['QCD_est'].GetBinContent(i) * all_histos['CR1']['QCD_subtr'].GetBinContent(i) / all_histos['CR2']['QCD_subtr'].GetBinContent(i))
        data_obs.Add(all_histos["SR"]['mc_total'])


    # Compute ratios of QCD_subtr over QCD_est for each bin of the VR template
    # NOTE: not used anymore for ABCD setup
    QCD_ratios = []
    for i in range(1, Nbins + 1):
        QCD_est = all_histos['VR']['QCD_est']
        QCD_subtr = all_histos['VR']['QCD_subtr']
        QCD_ratios.append(QCD_subtr.GetBinContent(i) / QCD_est.GetBinContent(i))

    print("QCD ratios in VR:")
    print(QCD_ratios)

    # Define 'delta' histograms for each bin in all categories
    # Yield = estimated yield
    for cat in categories:
        for i in range(1, Nbins + 1):
            name = 'QCD_bin_{}'.format(i)
            delta = total.Clone(name)
            delta.Reset()
            if cat == 'SR':
                if real_data:
                    pred_yield = all_histos['VR']['QCD_subtr'].GetBinContent(i) * all_histos['CR1']['QCD_subtr'].GetBinContent(i) / all_histos['CR2']['QCD_subtr'].GetBinContent(i)
                # if blind, use "estimated" QCD in the VR to extrapolate to SR
                else:
                    pred_yield = all_histos['VR']['QCD_est'].GetBinContent(i) * all_histos['CR1']['QCD_subtr'].GetBinContent(i) / all_histos['CR2']['QCD_subtr'].GetBinContent(i)
                delta.SetBinContent(i, pred_yield)
            if cat in ['CR1', 'CR2', 'VR']:
                delta.SetBinContent(i, all_histos[cat]['QCD_subtr'].GetBinContent(i))
            # if cat in ['SR', 'VR']:
                # delta.SetBinContent(i, all_histos[cat]['QCD_est'].GetBinContent(i))
            # if cat in ['CR1', 'CR2']:
                # delta.SetBinContent(i, all_histos[cat]['QCD_subtr'].GetBinContent(i))
            # delta.SetBinContent(i, 1.)
            delta.SetBinError(i, 0)
            all_histos[cat][name] = delta

    # Write results to output file
    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))
    out_tf = openFileAndGet(output_filename, 'recreate')

    for cat in all_histos:
        out_tf.mkdir(cat).cd()
        for hist in all_histos[cat].values():
            hist.Write()
        out_tf.cd()

    return QCD_ratios, est_QCD_yields, QCD_shape_CR1, QCD_shape_CR2
