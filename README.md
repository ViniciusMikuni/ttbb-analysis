<h1><b>ttbb analysis repository instructions</b></h1>

The python scripts for this repository  use the ntuples created by the code in the repo:

https://gitlab.cern.ch/jpata/tthbb13/tree/FH_systematics

The code is the based on the analysis of the ttbb croiss section meaurement on the all hadronic channel described on the AN:


<h1><b>Skimming even more</b></h1>

After the creation of the ntuples, we can create skims to further reduce the size, while also adding new useful variables (like our BDTs).
This can be done py running the python script <b> Skim_NoBtagSys.py </b> and changing <b> Skim_cfg.py </b> for input paths, samples and outputs.

In case the BDT variables are already in your ntuples (plus the systematic variations) you can also run the fast version of the code <b> Skim_NoBtagSys_Fast.py </b>.

<h1><b>Plotting</b></h1>

To get a fast check that all the samples are there and to produce control plots <i>after</i> the cuts on the chi2 probability, you can use the <b>Plotting.py</b> script running on the reduced ntuples you created in the previous section. In case you are interested in control plots using the ntuples created directly from the framework, you can use the plotting codes of the framewrok, under the folder Plots/Daniel.

Other plotting tools are available too, like:

<b> Plot_variations.py </b>: Plot in the same canvas a distribution of a given variable and its variations under systematic uncertainties. Uses the root file produces by the Plot_Sys2.py

<b> Plot_correlation.py </b>: Plot a 2D histogram of given variables and calculate the linear correlation factor between each.

<b> Plot_Eff.py </b>: Used to plot the efficiency of the Permutation BDT.

<b> Plot_postfit.py </b>: Plot the prefit and postfit distributions. Requires the root file output from the Combine Harvester.

<b> Plot_regions.py </b>: Plot the normalized distribution of given variables in different regions of the phase space but for the same sample.

<b> Plot_ROC.py </b>: Plot the ROC curve for QCD rejection for different variables in the same canvas.

<b> Plot_same.py </b>: Used to plot a normalized distribution for different samples in the same canvas.


<h1><b>Systematic uncertainties</b></h1>

The variated distributions should already exist in the ntuples for the JECs. The same should apply for the weights and its variations.

To create a root file that stores the systematic variations while also creating the templates with the data driven QCD method you can use the <b> Plot_Sys2.py </b> script. This script loads the configurations from the sys.cfg, in which you can change cuts, samples and which systematic variations to use.
As the name of the script suggests, you can also produce plots. To test if the data driven QCD estimation method works you have the option to plot the distributions on the VR and SR. 


