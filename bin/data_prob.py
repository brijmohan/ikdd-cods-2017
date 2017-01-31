import sys
import numpy as np
import operator

args = sys.argv

gtfile = '../twitter_manip/gt.txt'
gt = {}
with open(gtfile) as gtf:
    for line in gtf.read().splitlines():
        sp = line.split(':')
        w = sp[0].strip()
        proxim = np.array([int(x) for x in sp[1].strip().split(',')])
        gt[w] = np.mean(proxim)
        #gt[w] = np.count_nonzero(proxim)
        #gt[w] = np.median(proxim)

def data_score(ww):
    if ww in gt:
        return gt[ww]
    else:
        return 0

if __name__ == "__main__":
    rank_file = args[2]
    infile = args[1]

    with open(infile) as inp, open(rank_file, 'wb') as rfile:
        words = inp.read().splitlines()
        
        ranked_words = {w: gt[w] for w in words}
        ranked_words = [k for k, v in sorted(ranked_words.items(), key=operator.itemgetter(1), reverse=True)]
        for w in words:
            rfile.write(w + '\t' + str(ranked_words.index(w) + 1) + '\n')
