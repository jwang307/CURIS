import collections
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    os.chdir('/Users/jwang/CURIS/SequenceIdentity/')
    mount_path = sys.argv[1]
    dir_list = [dir for dir in os.listdir() if os.path.isdir(dir) if dir.startswith('AF')]
    print(dir_list)

    plot_points = {}
    for pocket in dir_list:
        if pocket == 'AF_5ZTY' or pocket == 'AF_7E2Y':
            continue
        with open(os.path.join(pocket, pocket + '_identities.txt'), 'r') as infile:
            with open(os.path.join(mount_path, pocket + '/top_scores.txt'), 'r') as ga_file:
                ga_scores = collections.defaultdict(float)
                for hit in ga_file:
                    info = hit.split('\t')
                    ga_scores[info[0][0:5]] = float(info[1])

                for line in infile:
                    info = line.split(" ")
                    align_len = int(info[5])
                    if align_len > 50:
                        hit_code = info[0][0:5]
                        identity = float(info[1])
                        ga_score = ga_scores[hit_code]
                        if ga_score > 0.6 and identity < 0.95:
                            plot_points[hit_code + '_' + pocket] = [identity, ga_score]
    print(plot_points)
    df = pd.DataFrame.from_dict(plot_points, orient='index', columns=['sequence identity', 'ga-score'])
    print(df.to_string())
    scatter = df.plot.scatter(x='ga-score', y='sequence identity')
    plt.savefig('ga_score_vs_identity.jpeg')

