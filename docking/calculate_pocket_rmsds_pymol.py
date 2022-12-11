from pymol import cmd

import numpy as np
import pandas as pd
import os
# import gpcrmining.gpcrdb as db
import math
# import glob
# from pathlib import Path


oak_dir = "/Users/jwang/CURIS/"
data_dir = oak_dir + "mount/"

# not used?
gpcr_db = oak_dir+ "projects/ligand-docking/modeled_structures/scripts/gpcr_db_set.csv"
path_dir = oak_dir+ "projects/ligand-docking/modeled_structures/data/gpcr_pockets/pdbs/"


def align_pv():
    pocket_size = {}
    pocket_dict = {}
    pocket_dict_aligndms = {}
    for protein in os.listdir(data_dir):
        cmd.delete("*")

        print(protein)
        # if "ADA2A" not in protein:
            # continue
        if not os.path.isdir(data_dir+protein+'/docking/'):
            continue
        for pair in os.listdir(data_dir+protein+"/docking/"):
            if 'prime_' in pair:
                continue
            if "lig" not in pair:
                continue
            prot = pair.split("_lig-to-")[0]
            prot2 = pair.split("_lig-to-")[-1]
            if os.path.exists((data_dir+protein+'/docking/'+pair)):
                print(pair)

                if not os.path.exists(data_dir+protein+'/structures/aligned/'+prot+"/rot-"+prot+"_query_to_"+prot2+".mae"):

                    continue
                cmd.load(data_dir+protein+'/structures/aligned/'+prot+"/rot-"+prot+"_query_to_"+prot2+".mae", "aligned_protein")
#               
                cmd.load(data_dir+protein+'/structures/proteins/'+prot2+"_prot.mae", "docked_protein_stuff")

                cmd.select("aligned_ligand", "chain L")
                cmd.select("pocket_aligned", 'not chain L and aligned_protein and br. all within 5 of aligned_ligand')
                

                cmd.select('ref',"pocket_aligned and aligned_protein")
                myspace = {'resis': []}
                cmd.iterate('ref', 'resis.append(resi)', space=myspace)
                # if '6KUY' in prot or '6KUY' in prot2: 
                #i think this was misnumbered, very hacky:
                if 'AF_6KUX' in prot:
                    myspace = {'resis': [str(int(resi)-15) for resi in myspace['resis']]}
                elif "AF_6KUX" in prot2:
                    myspace = {'resis': [str(int(resi)+15) for resi in myspace['resis']]}

                cmd.select('docked_protein_pocket', 'none')
                resset = set(myspace['resis'])
                resset = list(resset)
                pocket_size[pair]= len(myspace['resis'])
                for k in range(0,math.ceil(len(resset)/5)):
                    end_int = min((k+1)*5,len(resset))
                    
                    resis="+".join(resset[k*5:end_int])

                  
                    cmd.select('docked_protein_pocket','( resi ' +resis +' and docked_protein_stuff) or docked_protein_pocket')

#                
                #DO THIS ALIGNMENT for the alignment object not for actual alignment, alignement was done by schrodinger before in combind. 
                cmd.align('ref', 'docked_protein_pocket', transform = 0, cycles = 0,object = 'aln')
                #actual RMS done here:
                results = cmd.rms_cur("ref & aln", "docked_protein_pocket & aln", matchmaker = -1)#, transform = 0, cycles = 0)
                pocket_dict[pair]=results
                #Optional to check alignments later, but don't know that you need this. 
                #cmd.save(data_dir+protein+'/docking/'+pair+"/aligned_lig_"+pair+".mae", "aligned_ligand")
#                 
                #cmd.save(data_dir+protein+'/docking/'+pair+"/aligned_prot_"+pair+".mae", "aligned_protein")

                cmd.delete("*")
        # break 
    df = pd.DataFrame.from_dict(pocket_dict, orient = "index", columns = ['pocket_rmsd'])
#     df_align_rms = pd.DataFrame.from_dict(pocket_dict_aligndms, orient = "index", columns = ['pocket_rmsd_align'])
    df_pocket_res_count = pd.DataFrame.from_dict(pocket_size,orient = 'index', columns = ['pocket_res_count'])
    
    df.to_csv("/Users/jwang/CURIS/docking/pocket_rms_min_corrected.csv")
    df_pocket_res_count.to_csv("/Users/jwang/CURIS/docking/pocket_res_count_min_corrected.csv")
           

    
cmd.extend('align_pv', align_pv)
if __name__ == '__main__':
    align_pv()