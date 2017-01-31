import sys
from scipy.stats import spearmanr

args = sys.argv
genfile = args[1]
gtfile = args[2]

with open(genfile) as f1, open(gtfile) as f2:
    rl1 = [int(line.split('\t')[1]) for line in f1.read().splitlines()]
    rl2 = [int(line.split('\t')[1]) for line in f2.read().splitlines()]

    print spearmanr(rl1, rl2)
