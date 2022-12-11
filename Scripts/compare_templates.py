import collections
import csv
import os

if __name__ == "__main__":

    with open('../../Downloads/glosa_results.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        results_dict = {code.lower(): [] for code in reader.fieldnames}
        for row in reader:
            for k, v in row.items():
                results_dict[k.lower()].append(v[0:4])
    template_folder = '../gpcrdb_templates/'
    results = collections.defaultdict(list)
    for file in os.listdir(template_folder):
        uniprot = file.split("_")[1]
        if uniprot in results_dict.keys() and len(results[uniprot]) == 0:
            with open(f'{template_folder}{file}', 'r') as csvfile:
                match = 0
                total_count = 0
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Template'].lower() in results_dict[uniprot]:
                        match += 1
                        results[uniprot].append(row['Template'].lower())
                    total_count += 1
                # print(f'{uniprot}: {match/total_count}')
                results[uniprot].append(match/total_count)
    with open('common_templates.txt', 'w') as outfile:
        for k, v in results.items():
            outfile.write(f'{k}: {v}')
            print(f'{k}: {v}')
    # for key in results.keys():
    #     print(f'{key}: {results[key]}')



