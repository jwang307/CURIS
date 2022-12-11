import os
import sys

import numpy as np
import pandas as pd


def get_top_rmsds(uniprot):
    all_rmsds = {}
    for root, folder, files in os.walk(uniprot):
        for file in files:
            if file.endswith('.npy'):
                rmsds = np.load(os.path.join(root, file))
                all_rmsds[file] = rmsds

    rmsds_df = pd.DataFrame.from_dict(all_rmsds, orient='index')
    rmsds_df = rmsds_df.transpose()
    rmsds_df.columns = [col.removesuffix('_pv_rmsd_to.npy') for col in rmsds_df.columns]
    rmsds_df.to_csv(f'{uniprot}/compiled_rmsds.csv')

    top_n_compiled = []
    n = [1, 2, 3, 5, 10, 50, 100]
    for lig in rmsds_df.columns:
        top_n = []
        lig_rmsds = rmsds_df[lig]
        for i in n:
            top_n.append(min(lig_rmsds[:min(i, len(lig_rmsds))]))
        top_n_compiled.append(top_n)
    output_top_n = pd.DataFrame(top_n_compiled, rmsds_df.columns, n)
    output_top_n.to_csv(f'{uniprot}/top_rmsds.csv')

    return output_top_n


if __name__ == "__main__":
    os.chdir('/Users/jwang/CURIS/docking/')
    good = {'AF_6A93', 'AF_7E'}
    top_rmsds = []
    for uniprot in os.listdir():
        if os.path.isdir(uniprot) and not uniprot.startswith('.'):
            top_rmsds.append(get_top_rmsds(uniprot))
            print('Finished ' + uniprot)

    compiled_top_rmsds = pd.concat(top_rmsds)
    compiled_top_rmsds.to_csv('top_rmsds.csv')
    print('Finished')



