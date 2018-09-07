<h1><b>ttbb analysis repository instructions</b></h1>

The python scripts for this repository  use the ntuples created by the code in the repo:

https://gitlab.cern.ch/jpata/tthbb13/tree/FH_systematics

<h1><b>Skimming even more</b></h1>

After the creation of the ntuples, we can create skims to further reduce the size, while also adding new useful variables (like our BDTs).
This can be done py running the python script <b> Skim_NoBtagSys.py </b> and changing <b> Skim_cfg.py </b> for input paths, samples and outputs.

In case the BDT variables are already in your ntuples (plus the systematic variations) you can also run the fast version of the code <b> Skim_NoBtagSys.py </b>.
