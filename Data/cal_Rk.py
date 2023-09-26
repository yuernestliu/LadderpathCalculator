import numpy as np
import pandas as pd

def get_R_value(seq, k = 4):
    # for an elongating sequence, suppose the number of the most k-mer combinations is unsaturate before its length is less than k^20 + k - 1.
    # e.g. a 50-aa sequence has no more than 49 different 2-mers, but a 5000-aa sequence has 400 2-mers.
    com_unsaturate = len(seq) - k + 1

    if com_unsaturate <= 1:
        return 1
    else:
        # sliding k-mer window counts the number of k-mers. 
        p_list = list(pd.DataFrame([seq[i:i+k] for i in range(com_unsaturate)]).value_counts())

        power_list = {1:20,2:400,3:8000}
        
        # the maximised entropy (for n k-mers have identical frequencies) equals np.log2(n)
        if k < 4:
            com_saturate = power_list[k]
            H_max = np.log2(min(com_saturate, com_unsaturate))
        else:
            H_max = np.log2(com_unsaturate)

        return 1 - sum(-p*np.log2(p) for p in [x/sum(p_list) for x in p_list]) / H_max
