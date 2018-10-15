import ROOT as R
import os


def extractShapes(input_filename, output_filename, mc_backgrounds, mc_signals, real_data=False):
    """
    Extract the shapes from input_filename and prepare them for combineHarvester in output_filename.
    The output file should contain directories named after the categories, containing histograms named as '$PROCESS' or '$PROCESS_$SYST(Up|Down)'

        - For now all existing templates for data and MC are copied
        - In the CR1 and SR, define 'delta' histograms named 'QCD_bin_{i=1..N}' that will serve to estimate QCD from a combined fit of CR1 and SR. Each histogram is zero everywhere but =1 in bin i.
        - If real_data is False, redefine data_obs in the SR as the sum of all background estimates (with QCD normalised to the total data in the SR)

    Returns:
        - a list of ratios QCD_data/QCD_est (per bin) in the VR, to define the systematic on QCD in the SR
        - the expected yields of QCD in the categories (estimated by subtraction)
        - the expected nominal shape of QCD in the SR
    """

    tf = R.TFile.Open(input_filename)

    # Read all histograms, put them in a dictionary with key = category
    all_histos = {}
    est_QCD_yields = {}

    categories = ['CR1', 'CR2', 'VR', 'SR']
    
    for cat in categories:
        m_dir = tf.GetDirectory(cat)
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
                all_histos[cat][key.GetName()] = th1
    tf.Close()

    Nbins = all_histos['SR']['data_obs'].GetNbinsX()
    
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
        all_histos[cat]['QCD_subtr'] = QCD_subtr
        
        est_QCD_yields[cat] = QCD_subtr.Integral()
        print('QCD yield estimated by subtraction in {}: {}'.format(cat, est_QCD_yields[cat]))

    # Estimate QCD in VR using CR2 (take shape & scale yields)
    QCD_est = all_histos['CR2']['QCD_subtr'].Clone('QCD_est')
    QCD_est.Scale(1./est_QCD_yields['CR2'])
    QCD_shape_CR2 = [ QCD_est.GetBinContent(i) for i in range(1, Nbins+1) ]
    QCD_est.Scale(est_QCD_yields['VR'])
    all_histos['VR']['QCD_est'] = QCD_est
    print("QCD shape in CR2:")
    print(QCD_shape_CR2)

    # Estimate QCD in SR using CR1 (take shape & scale yields)
    QCD_est = all_histos['CR1']['QCD_subtr'].Clone('QCD_est')
    QCD_est.Scale(1./est_QCD_yields['CR1'])
    QCD_shape_CR1 = [ QCD_est.GetBinContent(i) for i in range(1, Nbins+1) ]
    QCD_est.Scale(est_QCD_yields['SR'])
    all_histos['SR']['QCD_est'] = QCD_est
    print("QCD shape in CR1:")
    print(QCD_shape_CR1)

    # If fake data, define data_obs in SR as the sum of MC backgrounds plus QCD estimate
    # (so using shape from CR1 but overall normalisation from data in SR)
    if not real_data:
        data_obs = all_histos['SR']['data_obs']
        data_obs.Reset()
        data_obs.Add(all_histos['SR']['mc_total'])
        data_obs.Add(all_histos['SR']['QCD_est'])

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
    for cat in categories: #['CR1', 'SR']:
        for i in range(1, Nbins + 1):
            name = 'QCD_bin_{}'.format(i)
            delta = total.Clone(name)
            delta.Reset()
            if cat in ['SR', 'VR']:
                delta.SetBinContent(i, all_histos[cat]['QCD_est'].GetBinContent(i))
            if cat in ['CR1', 'CR2']:
                delta.SetBinContent(i, all_histos[cat]['QCD_subtr'].GetBinContent(i))
            delta.SetBinError(i, 0)
            all_histos[cat][name] = delta

    # Write results to output file
    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))
    out_tf = R.TFile(output_filename, 'recreate')

    for cat in all_histos:
        out_tf.mkdir(cat).cd()
        for hist in all_histos[cat].values():
            hist.Write()
        out_tf.cd()

    return QCD_ratios, est_QCD_yields, QCD_shape_CR1, QCD_shape_CR2
