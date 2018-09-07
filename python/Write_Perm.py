from itertools import permutations, combinations

def JetComb(njets):
    '''return all the combinations for jet and b-jet  positioning'''

    jetpermut_ = list(permutations(range(njets),6))#permutations of all jets 
    completelist_ = []
    for i in range(len(jetpermut_)):
        if (jetpermut_[i][0] > jetpermut_[i][1] or jetpermut_[i][2] > jetpermut_[i][3] or jetpermut_[i][4] > jetpermut_[i][5]): continue
        completelist_.append(jetpermut_[i])
    return completelist_


      

with open('all_perm.cfg','w') as f:
    f.write('[Permutations]\n')
    for i in range(7,15):
        f.write('\t'+str(i)+':')
        to_write =str(JetComb(i))

        f.write(to_write+'\n')






                                                                                    
