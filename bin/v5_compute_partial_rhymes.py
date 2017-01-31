import sys
import argparse, csv, re

args = sys.argv

syllable_file_hindi = open('../build_models/srilm_data/syllabified_words_mono_vwinit.tsv').readlines()
nwords = len(syllable_file_hindi)
#syllable_file_codemix= open('12words_alt_ppos/syll.txt').readlines()
syllable_file_codemix= open(args[1]).readlines()


vowels = ['a', 'aa', 'ai', 'au', 'e', 'e-', 'ei', 'i', 'ii', 'o', 'o-', 'oo', 'u', 'uu']
consonants= ['b', 'bh', 'ch', 'chh', 'd', 'd:', 'd:h', 'dh',  'dh~', 'd~', 'g', 'gh', 'g~', 'h', 'h:', 'j', 'jh', 'j~', 'k', 'kh', 'kh~', 'k~', 'l', 'l:', 'm', 'n', 'n:', 'nd~', 'ng~', 'nj~', 'p', 'ph', 'ph~', 'r', 'rx', 's', 'sh', 'shh', 't', 't:', 't:h', 'th', 'v', 'y', "just", "fun"]

syllable_file_hindi = [re.sub('\n', '', line) for line in syllable_file_hindi]
syllable_file_hindi = [line.split('\t') for line in syllable_file_hindi]
syllables_hindi = [line[1].split(' ') for line in syllable_file_hindi]

syllable_file_codemix = [re.sub('\n', '', line) for line in syllable_file_codemix]
syllable_file_codemix = [line.split('\t') for line in syllable_file_codemix]
syllables_codemix = [line[1].split(' ') for line in syllable_file_codemix]
rhyme_score = []
def compute_partial_rhyme(cm_word, sylls_hin):     
    rhyming_quotient = []
    last_syllable = []
    rcm_word = cm_word[::-1] 
    for hin_word in sylls_hin:     
        
        rhin_word = hin_word[::-1]
    
        if len(rcm_word) == 1 and rcm_word[0] == rhin_word[0]:
           #print "case I: found identical last syllable" 
           #print cm_word, hin_word
           last_syllable.append(hin_word)
     
        elif len(rcm_word) == 1 and rcm_word[0] != rhin_word[0]:         
             vowel_cm = [char for char in list(rcm_word[0]) if char in vowels]
             vowel_hin = [char for char in list(rhin_word[0]) if char in vowels]
             if vowel_cm == vowel_hin and rcm_word[0][-2:] == rhin_word[0][-2:]:
                #print "case II: found partial last syllable" 
                #print cm_word, hin_word
                last_syllable.append(hin_word)

    
        elif len(rcm_word) > 1 and len(rhin_word) > 1 and rcm_word[0] == rhin_word[0]:
              vowel_cm = [char for char in list(rcm_word[1]) if char in vowels]
              vowel_hin = [char for char in list(rhin_word[1]) if char in vowels]
              if vowel_cm == vowel_hin and rcm_word[1][-2:] == rhin_word[1][-2:]:
                 #print "case III: found identical last and partial penultimate syllable" 
                 #print cm_word, hin_word
                 last_syllable.append(hin_word)
                          
    rhyming_quotient.append([cm_word, len(last_syllable)])
    return rhyming_quotient

for cword in syllables_codemix:
   
    rhyme_score_cword=compute_partial_rhyme(cword, syllables_hindi)
    print ' '.join(rhyme_score_cword[0][0]), rhyme_score_cword[0][1]
    rhyme_score.append(' '.join(rhyme_score_cword[0][0]) + '\t' + str(rhyme_score_cword[0][1] / float(nwords)))

with open(args[2], "wb") as f:
    #writer = csv.writer(f)
    #writer.writerows(rhyme_score)
    f.write('\n'.join(rhyme_score))