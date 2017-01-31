#!/usr/bin/env python
#*-* encoding: utf8 *-*
import sys
import os
import operator

import matplotlib.pyplot as plt

from srilm import LM

from litcm import LIT
sys.path.append('../litcm/litcm')
import indictrans as tn

from data_prob import data_score
import numpy as np

args = sys.argv

phonelm = LM("../build_models/models/phone_final_max.wb.lm")
ortholm = LM("../build_models/models/char_final_max.wb.lm")
prosodylm = LM("../build_models/models/prosody_final_max.wb.lm")
sylllm = LM("../build_models/models/syll_final_max.wb.lm")

pronun_file = os.path.join(args[1], "eng.dict")
syll_file = os.path.join(args[1], "syll.txt")
rhyme_file = os.path.join(args[1], "rhyme.txt")


rules_file = 'en2hi.rules'
# word pscore ortho oscore
variant_pscore_file = os.path.join(args[1], "scores.txt")
rank_file = os.path.join(args[1], "ranks.csv")


vowels = ['a', 'aa', 'ai', 'au', 'e', 'e-', 'ei', 'i', 'ii', 'o', 'o-', 'oo', 'u', 'uu']

def strip_consonants(phone_str):
	psp = phone_str.strip().split()
	return ' '.join([x for x in psp if x in vowels])


def recurse(variant_str, buckets, buck_idx, varr):
    if buck_idx == len(buckets):
        #print variant_str
        varr.append(variant_str.strip())
    else:
        for confused_phone in buckets[buck_idx]:
            recurse((variant_str + ' ' + confused_phone), buckets, buck_idx + 1, varr)

phone_confusion_dict = {}
with open(rules_file) as rfile:
    for line in rfile:
        line = line.strip()
        sp = line.split('\t')
        phone_confusion_dict[sp[0]] = [x.strip() for x in sp[2].split(',')]

words = []
pscores = []
oscores = []
proscores = []
syllscores = []
datascores = []

# obtain syllables
sylls = []
with open(syll_file) as sfile:
    for line in sfile.read().splitlines():
        line = line.strip()
        if line:
            sp = line.split('\t')
            sylls.append(sp[1])

# obtain syllables
rhymes = []
with open(rhyme_file) as rfile:
    for line in rfile.read().splitlines():
        line = line.strip()
        if line:
            sp = line.split('\t')
            rhymes.append(np.log10(float(sp[1])))

with open(pronun_file) as pfile, open(variant_pscore_file, 'wb') as vfile:
    for idx, line in enumerate(pfile.read().splitlines()):
        line = line.strip()
        if line:
            sp = line.split(' ')
            w = sp[0]
            foreign_phones = sp[1:]
            confusion_buckets = [phone_confusion_dict[fp] for fp in foreign_phones]
            variants = []
            recurse("", confusion_buckets, 0, variants)

            variance_pscore = {}
            for v in variants:
                #print v
                prob_v = phonelm.total_logprob_strings(v.split(' '))
                variance_pscore[v] = prob_v

            sorted_vp = sorted(variance_pscore.items(), key=operator.itemgetter(1), reverse=True)

            # Uncomment to print all variants with their probability
            #for k, v in sorted_vp:
            #    print k, v

            chosen_variant = sorted_vp[0][0]
            print "Variant with maximum probability is ==> {} : {}".format(chosen_variant, sorted_vp[0][1])

            #vfile.write(w + '\t' + sorted_vp[0][0] + '\t' + str(sorted_vp[0][1]) + '\n')

            # Find transliteration of w
            lit = LIT(labels=['hin', 'eng'], transliteration=True)
            trans_w_wx = wx = tn.RomanConvertor(lit.tree[lit.tag_dct['hin']],
                    w, 'hin').transliterate()
            trans_w = lit.wxp.wx2utf(trans_w_wx, 'hin')
            charsp = list(trans_w.decode('utf8'))
            print charsp
            
            # Find orthographic probability
            oscore = ortholm.total_logprob_strings([x.encode('utf8') for x in
                charsp])

            # Find prosodic probability
            prosody_str = strip_consonants(chosen_variant)
            proscore = prosodylm.total_logprob_strings(prosody_str.split())

            # Find syllables
            syll_str = sylls[idx]
            syllscore = sylllm.total_logprob_strings(syll_str.split())

            print w, trans_w
            words.append(w)
            pscores.append(sorted_vp[0][1])
            oscores.append(oscore)
            proscores.append(proscore)
            syllscores.append(syllscore)
            datascores.append(np.log10(data_score(w)))

            vfile.write(w + '\t' + chosen_variant + '\t' +
                    str(sorted_vp[0][1]) + '\t' + trans_w + '\t' + str(oscore)
                    + '\t' + prosody_str + '\t' + str(proscore)
                    + '\t' + syll_str + '\t' + str(syllscore) + '\n')



# Calculate final ranking
ranked_words = {}
for idx, w in enumerate(words):
    #ranked_words[w] = pscores[idx] + oscores[idx] + proscores[idx]
    ranked_words[w] = pscores[idx] + proscores[idx] + oscores[idx] + syllscores[idx] + rhymes[idx] + datascores[idx]
    #ranked_words[w] = proscores[idx]

ranked_words = [k for k, v in sorted(ranked_words.items(), key=operator.itemgetter(1), reverse=True)]

with open(rank_file, 'wb') as rfile:
    for word in words:
        rfile.write(word + ',' + str(ranked_words.index(word)+1) + '\n')

'''
fig, ax = plt.subplots()
ax.scatter(pscores, oscores)

for i, txt in enumerate(words):
    ax.annotate(txt, (pscores[i],oscores[i]))

plt.show()
'''
