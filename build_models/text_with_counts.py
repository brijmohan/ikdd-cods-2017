#!/usr/bin/env python
# *-* enocding: utf8 *-*

import numpy as np

freq_file = 'raw_data/hindi_all_freq.txt'
#dict_file = 'raw_data/hin_done_g2p.dic'
dict_file = 'raw_data/hindi_corrected_dictionary_15K.tsv'

syllable_file = 'srilm_data/syllabified_words_mono_vwinit.tsv'

vowels = ['a', 'aa', 'ai', 'au', 'e', 'e-', 'ei', 'i', 'ii', 'o', 'o-', 'oo', 'u', 'uu']

def strip_consonants(phone_str):
	psp = phone_str.strip().split()
	return ' '.join([x for x in psp if x in vowels])


op = 'max' # freq, tstat, max, damp
damping = 0.0
if op == 'damp':
	damping = 0.4

srilm_train_phone = 'srilm_data/srilm_train_phone_'+op+'.txt'
srilm_train_char = 'srilm_data/srilm_train_char_'+op+'.txt'
srilm_train_pro = 'srilm_data/srilm_train_pro_'+op+'.txt'
srilm_train_syll = 'srilm_data/srilm_train_syll_'+op+'.txt'

srilm_split_phone = 'srilm_data/srilm_split_phone_'+op+'.txt'
srilm_split_char = 'srilm_data/srilm_split_char_'+op+'.txt'

srilm_test_phone = 'srilm_data/srilm_test_phone_'+op+'.txt'
srilm_test_char = 'srilm_data/srilm_test_char_'+op+'.txt'

# Read dictionary
hindict = {}
with open(dict_file) as dfile:
	for line in dfile.read().splitlines():
		line = line.strip()
		if line:
			sp = line.split()
			hindict[sp[0].strip()] = ' '.join(sp[1:])

# Read syllables
sylls = {}
with open(syllable_file) as sfile:
	for line in sfile.read().splitlines():
		line = line.strip()
		if line:
			sp = line.split()
			sylls[sp[0].strip()] = ' '.join(sp[1:])


# Read frequency counts
wcount = {}
with open(freq_file) as frqfile:
	for line in frqfile.read().splitlines():
		line = line.strip()
		if line:
			sp = line.split(',')
			w = sp[0].strip()
			if w:
				words = []
				if '-' in w:
					words = [wseg.strip() for wseg in w.split('-') if wseg.strip()]
				if ' ' in w:
					words = [wseg.strip() for wseg in w.split() if wseg.strip()]
				else:
					words.append(w)

				#print words
				for wseg in words:
					#print wseg
					if wseg not in wcount:
						wcount[wseg] = 0
					if len(sp) > 1:
						wcount[wseg] += int(sp[1].strip())
					else:
						wcount[wseg] += 1

# Calculate max of entire population (assuming count file items represent entire population)
pop = np.array(wcount.values())
pmax = float(np.max(pop))
#pmean = np.mean(pop)
#pstd = np.std(pop)

nkeys = len(hindict.keys())
#test_split_idx = nkeys - int(nkeys / 3)
test_split_idx = nkeys

#with open(srilm_train_phone, 'wb') as phonetrain, open(srilm_train_char, 'wb') as chartrain, open(srilm_split_phone, 'wb') as phonesplit, open(srilm_split_char, 'wb') as charsplit, open(srilm_test_phone, 'wb') as phonetest, open(srilm_test_char, 'wb') as chartest:
with open(srilm_train_phone, 'wb') as phonetrain, open(srilm_train_char, 'wb') as chartrain, open(srilm_train_pro, 'wb') as protrain, open(srilm_train_syll, 'wb') as sylltrain:
	cnt = 0
	for k, v in hindict.items():
		if k in wcount:
			# normalize here
			#wk = str(wcount[k])
			#wk = str((wcount[k] - pmean) / pstd)
			print wcount[k], pmax
			wk = str(damping + (1 - damping) * (wcount[k] / float(pmax)) )
			
			# Split by ortho
			charsp = (' '.join(list(k.split()[0].decode("utf-8")))).encode('utf8')

			if cnt < test_split_idx:
				# write phones
				phonetrain.write(wk + ' ' + v + '\n')
				# Write characters
				chartrain.write(wk + ' ' + charsp + '\n')
				# Write prosody
				protrain.write(wk + ' ' + strip_consonants(v) + '\n')
				# Write syllables
				sylltrain.write(wk + ' ' + sylls[k] + '\n')
			else:
				print "Done"
				# write phones
				#phonesplit.write(wk + ' ' + v + '\n')
				#phonetest.write(v + '\n')
				# Write characters
				#charsplit.write(wk + ' ' + charsp + '\n')
				#chartest.write(charsp + '\n')

		cnt += 1

print "Check file: "+srilm_train_phone
print "Check file: "+srilm_train_char
