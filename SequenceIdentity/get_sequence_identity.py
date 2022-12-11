from Bio.Blast import NCBIXML
import math
import os
from pymol import cmd
import subprocess
import sys

# helper function to computer distance between center of masses
def dist(com_1, com_2):
    return math.sqrt((com_1[0] - com_2[0])**2 + (com_1[1] - com_2[1])**2 + (com_1[2] - com_2[2])**2)

def save_closest_chain(pocket_position, pdb_code):
    cmd.split_chains(pdb_code)
    cmd.select(pdb_code+"_*")
    chain_list = cmd.get_object_list('(sele)')
    if len(chain_list) == 0:
        cmd.save(folder_path + query_code + ".fasta", pdb_code)
    else:
        min_dist = float('inf')
        chain_to_save = None
        for chain in chain_list:
            distance = dist(pocket_position, cmd.centerofmass(chain))
            if distance < min_dist:
                min_dist = distance
                chain_to_save = chain
        cmd.save(folder_path + query_code + ".fasta", chain_to_save)

    for chain in chain_list:
        cmd.delete(chain)
    cmd.delete(pdb_code)


# save the proteins that deliver binding site hits into a folder to be created as a blast database
def save_bs_fastas(af_pdb, pymol_session, path, query_code):
    cmd.load(pymol_session)

    object_list = cmd.get_names("objects")

    if not os.path.exists(path):
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
            save_closest_chain(cmd.centerofmass(object), af_pdb)

# make blast db
def make_db(path, query_code):
    db_fasta = query_code + "_db.fasta"
    if not os.path.exists(db_fasta):
        with open(path + db_fasta, 'w') as outfile:
            for file in os.listdir(path):
                if file != db_fasta:
                    with open(file) as infile:
                        for line in infile:
                            outfile.write(line)

    make_db = subprocess.Popen(['/usr/local/ncbi/blast/bin/makeblastdb',
                                '-in', db_fasta,
                                '-dbtype', 'prot'])
    print(make_db.communicate())

def run_blast(folder_path, query, db, out, eval):
    blastp = subprocess.Popen(['/usr/local/ncbi/blast/bin/blastp',
                               '-query', query,
                               '-db', db,
                               '-out', out,
                               '-evalue', str(eval),
                               '-outfmt', '5'])
    print(blastp.communicate())

    result_handle = open(out)
    result = NCBIXML.read(result_handle)
    with open(folder_path + "_identities.txt", 'w') as outfile:
        for alignment in result.alignments:
            bs_name = alignment.hit_def[0:5]
            identity = alignment.hsps[0].identities/alignment.hsps[0].align_length
            outfile.write(bs_name + ": " + str(identity) +
                          " with alignment length " + str(alignment.hsps[0].align_length) + '\n')

# Press the green button in the gutter to run the script.
# arguments: pdb session path, af pdb code
if __name__ == '__main__':
    af_pdb_code = sys.argv[1]
    pymol_session = sys.argv[2]
    # add e value as argument
    folder_path = "/Users/jwang/CURIS/" if len(sys.argv) <= 3 else sys.argv[3]
    query_code = "AF_" + af_pdb_code
    db_name = query_code + "_db/"
    db_path = os.path.join(folder_path, db_name)
    save_bs_fastas(af_pdb_code, pymol_session, db_path, query_code)

    os.chdir(folder_path + db_name)

    make_db(db_path, query_code)

    os.chdir(folder_path)

    query_prot = query_code + ".fasta"
    db = db_path + query_code + "_db.fasta"
    outfile = query_code + "_results.xml"
    evalue = 100000

    run_blast(folder_path + query_code, query_prot, db, outfile, evalue)

