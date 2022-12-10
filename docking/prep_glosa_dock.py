import csv
import os
import shutil

from pymol import cmd

'''
def get_names():
    with open('glosa results.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == 0:
                list_uniprot = row
            elif i == 1:
                list_pdb = row
            else:
                list_templates = row
    print(list_uniprot)
    print(list_pdb)
    list_templates = [s.split('.')[0].replace('-BS-', '-lig-') for s in list_templates]
    print(list_templates)
'''


def prep_pairs(oak_path, dock_path, uniprots, pdbs, templates):
    prot_path = oak_path + 'data_vina/'
    crystal_path = oak_path + 'data_min_corrected/'

    for i in range(len(uniprots)):
        uniprot = uniprots[i]
        pdb = pdbs[i]
        af_name = f'{pdb}_prot'
        lig_name = f'{pdb}_lig'
        template = templates[i]
        # copy structure
        print(f'Started {af_name}')
        # structures folder of dock
        structures = f'{dock_path}{uniprot}/structures/'
        # save path for prot and lig
        save_path = f'{structures}raw/'
        # path to mae struct
        struct = f'{prot_path}{uniprot}/structures/raw/{af_name}.mae'
        os.makedirs(save_path, exist_ok=True)
        # open in pymol and save as pdb
        cmd.load(struct)
        cmd.save(f'{save_path}{af_name}.mae', af_name)
        print('Copied prot')
        # copy top template
        pse_path = f'pymol_sessions/{pdb}_8.pse'
        cmd.load(pse_path)
        cmd.save(f'{save_path}{lig_name}.mae', template)
        print('Copied lig')
        '''
        # copy crystal binders
        crystal_structs = f'{crystal_path}{uniprot}/structures/processed/'
        try:
            shutil.copytree(crystal_structs, f'{structures}processed/', dirs_exist_ok=True)
            print('Copied processed')
        except FileNotFoundError:
            print(f'Processed folder doesnt exist for {uniprot}')
        # copy ligands
        try:
            shutil.copytree(f'{crystal_path}{uniprot}/raw/', f'{dock_path}{uniprot}/raw/', dirs_exist_ok=True)
            print(f'Finished {af_name}')
        except FileNotFoundError:
            print(f'Could not copy ligands smiles folder {uniprot}')
        '''

def delete_models(dock_path, uniprots):
    # delete all folders of modeled structs
    model_tags = {'AF', 'prime', '_inactive_', '_active_'}
    for uniprot in uniprots:
        target_path = f'{dock_path}{uniprot}/structures/processed/'
        print(os.listdir(target_path))
        # check folder if it is a modeled structure
        for folder in os.listdir(target_path):
            if os.path.isdir(os.path.join(target_path, folder)):
                for model_tag in model_tags:
                    if model_tag in folder and os.path.exists(os.path.join(target_path, folder)):
                        shutil.rmtree(os.path.join(target_path, folder))
                        print(f'Deleted {folder}')
        print(f'Cleaned {uniprot}')


def get_results(dock_path, uniprots):
    for uniprot in uniprots:
        result_path = f'{dock_path}{uniprot}/docking/'
        save_path = 'docking/'
        shutil.copytree(result_path, save_path, dirs_exist_ok=True)
        print(f'Finished {uniprot}')


if __name__ == '__main__':
    working_dir = '/Users/jwang/CURIS'
    oak_mount = 'af/'
    dock_mount = 'mount/'
    os.chdir(working_dir)

    uniprots = ['PE2R4', 'PTAFR', 'CNR2', '5HT2A', 'PE2R3', 'PD2R2', 'NK1R', 'TA2R', 'ADA2B', 'ADA2A', 'MTR1A', 'MTR1B',
                'SUCR1','CLTR1', 'CLTR2', 'DRD1', 'PE2R2', 'AGRG3', 'GRM2', '5HT1A']
    pdbs = ['AF_5YHL', 'AF_5ZKP', 'AF_5ZTY', 'AF_6A93', 'AF_6AK3', 'AF_6D26', 'AF_6E59', 'AF_6IIU', 'AF_6K41',
            'AF_6KUX', 'AF_6ME2', 'AF_6ME7', 'AF_6RNK', 'AF_6RZ4', 'AF_6RZ6', 'AF_7CKW', 'AF_7CX2', 'AF_7D76',
            'AF_7E9G','AF_7E2Y']
    templates = ['3b85A-lig-1', '5zkqA-lig-1', '5xraA-lig-2', '6bqhA-lig-1', '3dedA-lig-1', '5vblB-lig-2',
                 '4dklA-lig-1','5cufA-lig-10', '3zpqA-lig-6', '3zpqA-lig-6', '4ej4A-lig-1', '3uonA-lig-1', '4kibA-lig-1',
                 '4kibA-lig-1','5zkqA-lig-1', '3d4sA-lig-1', '3pfmA-lig-1', '3h75A-lig-1', '5cgcA-lig-4', '5wiuA-lig-1']

    # prep_pairs(oak_mount, dock_mount, uniprots, pdbs, templates)
    # delete_models(dock_mount, uniprots)
    get_results(dock_mount, uniprots)
    print('Finished')


