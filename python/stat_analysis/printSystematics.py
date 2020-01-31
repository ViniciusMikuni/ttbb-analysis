#! /bin/env python

from __future__ import print_function
from math import sqrt

import CombineHarvester.CombineTools.ch as ch
import ROOT as R

cb = ch.CombineHarvester()
cb.ParseDatacard("datacard.dat")

bins = cb.bin_set()

chosen_proc = ['ttcc', 'ttlf']
chosen_uncertainties = ['CMS_LHEscale_Weight_{}', 'CMS_LHEPDF_Weight', 'fsr_{}', 'isr_{}', 'hdamp_{}', 'tune']

def getUncStr(u, d):
    str_u = '{:3.1f}\%'.format(100*u)
    str_d = '{:3.1f}\%'.format(100*d)
    if str_u == str_d:
        return r'$\pm$ ' + str_u
    return "+" + str_u + "/-" + str_d

binTotalUncertainties = {}
for p in chosen_proc:
    binTotalUncertainties[p] = {}
    for b in bins:
        binTotalUncertainties[p][b] = {}

procTotalUncertainties = {}
for p in chosen_proc:
    procTotalUncertainties[p] = {}
    for syst in chosen_uncertainties:
        procTotalUncertainties[p][syst] = {}

for p in chosen_proc:
    totalYield = 0.
    totalYields_up = {}
    totalYields_down = {}
    for syst in chosen_uncertainties:
        syst = syst.format(p)
        totalYields_up[syst] = 0.
        totalYields_down[syst] = 0.

    for b in bins:
        thisShape = cb.cp().bin([b]).process([p])
        thisShapeTH = thisShape.GetShape()
        nominal = thisShapeTH.Integral()
        totalYield += nominal
        binTotalUncUp = [0.]
        binTotalUncDown = [0.]

        chosenSysts = thisShape.cp().syst_name([syst.format(p) for syst in chosen_uncertainties])
        
        def addShapeSyst(s):
            syst = s.name()
            
            value_u = s.value_u()
            rel_u = value_u - 1.
            totalYields_up[syst] += nominal * value_u
            binTotalUncUp[0] += rel_u**2
            
            value_d = s.value_d()
            rel_d = 1 - value_d
            totalYields_down[syst] += nominal * value_d
            binTotalUncDown[0] += rel_d**2

            # print("Process {} - bin {} - syst {}: {}".format(p, b, syst, getUncStr(rel_u, rel_d)))
        
        chosenSysts.ForEachSyst(addShapeSyst)

        binTotalUncUp = sqrt(binTotalUncUp[0])
        binTotalUncDown = sqrt(binTotalUncDown[0])

        binTotalUncertainties[p][b] = getUncStr(binTotalUncUp, binTotalUncDown)
        # print("\nProcess {} - bin {} - total: {}\n".format(p, b, getUncStr(binTotalUncUp, binTotalUncDown)))

    totalUncUp = 0.
    totalUncDown = 0.

    for syst_ in chosen_uncertainties:
        syst = syst_.format(p)

        rel_u = totalYields_up[syst] / totalYield - 1
        totalUncUp += rel_u**2

        rel_d = 1 - totalYields_down[syst] / totalYield
        totalUncDown += rel_d**2
        
        # print("\nProcess {} - total - syst {}: {}\n".format(p, syst, getUncStr(rel_u, rel_d)))
        procTotalUncertainties[p][syst_] = getUncStr(rel_u, rel_d)
        
    totalUncUp = sqrt(totalUncUp)
    totalUncDown = sqrt(totalUncDown)

    # print("\nProcess {} - total: {}\n".format(p, getUncStr(totalUncUp, totalUncDown)))
    binTotalUncertainties[p]["Total"] = getUncStr(totalUncUp, totalUncDown)
    procTotalUncertainties[p]["Total"] = getUncStr(totalUncUp, totalUncDown)

bins = ['SR', 'CR1', 'CR2', 'VR', 'Total']
print('Process & ' + ' & '.join(bins) + r'\\')
for p in chosen_proc:
    print(p, end=' & ')
    for b in bins:
        print(binTotalUncertainties[p][b], end=' & ')
    print(r'\\')

print()

print('Source & ' + ' & '.join(chosen_proc) + r'\\')
for s in chosen_uncertainties + ['Total']:
    print(s, end=' & ')
    for p in chosen_proc:
        print(procTotalUncertainties[p][s], end=' & ')
    print(r'\\')
