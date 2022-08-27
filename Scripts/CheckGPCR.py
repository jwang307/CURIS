import json
import sys


def main(db, queries) -> dict:
    results = {}

    for query in queries:
        if query.upper()[0:4] in db:
            results[query] = True
        else:
            results[query] = False
    return results


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        gpcr_db = f.read().splitlines()
    with open(sys.argv[2], 'r') as f:
        queries = f.read().splitlines()
    result = main(gpcr_db, queries)
    with open(sys.argv[3], 'w') as f:
        for key in result.keys():
            f.write(key + ':' + '\t' + str(result[key]) + '\n')
    f.close()
