# curis-2022

Code written during CURIS 2022 summer program.

## COM

Script used to filter certain ligand binding site templates from a pymol session. 
In pymol session containing an AlphaFold binding site (BS) and several top ligand (lig)/BS template pairs, the script will disable all template pairs that are a certain threshold distance from the center of mass (COM) of the AlphaFold BS.
The script adds a command called ```filter_com``` to the pymol commands list. It takes in three arguments: 

- String ```key```: 'lig' or 'BS' depending on whether the program should measure the distance from the AlphaFold BS COM to the templates' ligand COM or BS COM.
- Float ```threshold``` (optional): The cutoff distance (in Angstroms) to disable templates that are greater than the specified distance from the AlphaFold BS COM. The default distance is 5 ang.
- String ```path``` (optional): Specified path of the output pymol session with filtered results. The default path is (for my computer) "~/jwang/CURIS/pymol_sessions/"

### Examples
 To run the program, first add the command to pymol by running ```run /path/to/script.py```. In my case, this would be ```run ~/CURIS/COM/main.py```.
To run the script and filter all templates greater than 5 angstroms when comparing template ligand COM to AlphaFold BS COM, run the command 
```
filter_com lig
```
To change the threshold distance, run
```
filter_com lig, threshold=[distance]
```
To compare distance using the template BS, run 
```
filter_com BS
```
To change the path of the output session, run
```
filter_com [lig/BS], threshold=[distance], path=[/path/to/output/]
```

## Scripts

A collection of random utility scripts. The only two that may be useful are ```StripPDB``` and ```CheckGPCR```. The other scripts are one-off programs for specific tasks - ```FilterLibrary``` was used to reduce the template library size to a specified range of Binding sites (11-34 residues in size). ```GetScoreStats``` was used to generate statistics on GLoSA results.

### StripPDB

G-LoSA only takes in pdb files that only contain the ```ATOM``` or ```HETsomething``` information. All other metadata in the file will confuse the code that parses the pdb file.
This program will take in a pdb file and output stripped pdb file that will fit G-LoSA requirements. The program takes in 2 arguments. Using ```--help``` will detail information on the parameters:
- [path]: path of the input pdb file
- [key]: 'p' for keeping only atoms of a protein, 'l' for keeping only atoms of a ligand

An example run that will return a protein ready to be run in G-LoSA:
```
javac StripPDB.java
StripPDB /path/to/input.pdb p
```

### CheckGPCR

This script takes in a G-LoSA score result file and returns whether each of the top templates in the score file is from a GPCR or not.
To run the script, you must also have a line-separated text file of PDB codes of every GPCR, taken from GPCRdb. This can be found in the ```Scripts``` folder named ```gpcrs.txt```.
The script takes three arguments: the path to the list of GPCRs, the path to the input G-LoSA result file, and the path to the output file.
Example:
```
CheckGPCR.py gpcrs.txt [glosascore].txt [output].txt
```

## SequenceIdentity

This script takes in a pymol session of G-LoSA results and returns the global sequence identity between the AlphaFold source protein and the source protein of the top templates. 
The alignment program used by the script is ```blastp```. Because of this, downloading ```BLAST+``` from NCBI is a pre-requisite to running this script. The download instructions for
```BLAST+``` can be found at . The script outputs a text file with each top template and the sequence alignment identity of the template to the AlphaFold source protein as well as the length of the alignment.
The script takes in several arguments:
- [pdb_code]: The pdb code of the ligand inserted in the AlphaFold model. This code should be present in the name of the pymol session.
- [path]: The path to the pymol session containing the AlphaFold model with top templates.
### Examples
```
python get_sequence_identity.py [pdb_code] /path/to/pymol_session
```

The output of the program will be a line separated text file with the length of the longest alignment of the two protein sequences (AF protein/template protein) and the sequence identity of the alignment.
The hits are ordered by what blastp thinks is the best match (e. value).
An example output:
```
4zudA_A: 0.2756183745583039 with alignment length 283
4yayA_A: 0.27147766323024053 with alignment length 291
5nddA_A: 0.2818181818181818 with alignment length 330
4ebbA_A: 0.27586206896551724 with alignment length 58
4xcmA_A: 0.29545454545454547 with alignment length 88
1ynfA_A: 0.5384615384615384 with alignment length 13
4kk0A_A: 0.2982456140350877 with alignment length 57
3ic8A_A: 0.3548387096774194 with alignment length 31
4nsnA_A: 0.2857142857142857 with alignment length 35
2o0yA_A: 0.2916666666666667 with alignment length 24
4iuyA_A: 0.32142857142857145 with alignment length 28
3fuyA_A: 0.22826086956521738 with alignment length 92
```

