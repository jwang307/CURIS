import os
from pymol import cmd

# script to save the proteins that deliver binding site hits into a folder to be created as a blast database
def save_bs_fastas(af_pdb, folder_path="/Users/jwang/CURIS/"):
    object_list = cmd.get_names("objects")

    db_folder = "AF_" + af_pdb + "_db/"
    path = os.path.join(folder_path, db_folder)
    os.mkdir(path)

    for object in object_list:
        if 'bs' in object.lower():
            code = object[0:5]
            cmd.fetch(code)
            cmd.remove("resi 1000-3000")
            cmd.save(path + code + ".fasta", code)
            cmd.delete(code)
        if 'af' in object.lower():
            cmd.fetch(af_pdb)
            cmd.remove("resi 1000-3000")
            cmd.save(folder_path + af_pdb + ".fasta", af_pdb)
            cmd.delete(af_pdb)



cmd.extend("save_bs_fastas", save_bs_fastas)
