import sys
import argparse, csv

args = sys.argv

#dic_file = 'C:\\Users\\ayushi_pandey\\Desktop\\scripts_borrowing_challenge\\module_rhyming\\hin_done_g2p_main_syllables_rhymes.txt'
#dic_file = '../input_files/hin_done_g2p_main_syllables_rhymes.txt'

dic_file = args[1]
out_file = args[2]

vowels = ['a', 'aa', 'ai', 'au', 'e', 'e-', 'ei', 'i', 'ii', 'o', 'o-', 'oo', 'u', 'uu']
consonants= ['b', 'bh', 'ch', 'chh', 'd', 'd:', 'd:h', 'dh',  'dh~', 'd~', 'g', 'gh', 'g~', 'h', 'h:', 'j', 'jh', 'j~', 'k', 'kh', 'kh~', 'k~', 'l', 'l:', 'm', 'n', 'n:', 'nd~', 'ng~', 'nj~', 'p', 'ph', 'ph~', 'r', 'rx', 's', 'sh', 'shh', 't', 't:', 't:h', 'th', 'v', 'y', "just", "fun"]
##defining file open and clustering word-initial and word-final consonants globally
inp = open(dic_file).read().splitlines()  

def syllabify(word):
    letter = 1
    while letter < len(word):
        print word
    #for letter in range(len(word)):
        #print "usual", word
        if len(word) > 1 and word[letter-1] in vowels and word[letter] in vowels:
            word[letter-1:letter+1] = [''.join(word[letter-1:letter+1]) ]
            vowels.append(''.join(word[letter-1:letter]))
        print word, letter
        if len(word) > 0 and letter < len(word) and word[letter] == '':
            print "problem word", word
             #print "such a,", word
            word[letter-1:letter+1] = [''.join(word[letter-1:letter+1])]
            #print "is now,", word
        letter += 1
    if len(word) > 1 and word[0] in consonants and word[1] in consonants:
        word[0:2] = [''.join(word[0:2])]
    if len(word) > 2 and word[len(word)-2] in consonants and word[len(word)-1] in consonants:               
        word[-2:] = [''.join(word[-2:])]
    else:
        pass    

    syll_list = [char for char in word if char in vowels]
    syl_count = len(syll_list)
    ##print word, syll_list, syl_count
    vowel_list = word[1::2]
    vowel_list_init = word[0::2]

    #### case of only one syllable #######
    if syl_count == 1:
        syllable_structure.append("".join(word))
       ##print syllable_structure
        return True
   ########### case of more than one syllable ###################
    else:
        ##print "else"
      if syll_list == vowel_list_init:
          syllable_structure.append(word[0])
          syllabify(word[1:])
      else:
        for char in range(len(word)):

            ########### case of pure CV-CV structure (alternate vowels) ###################    
            if syll_list == vowel_list:
                #  #print word, "i'm here"
               if word[char] in vowels:
                   if char == len(word)-2 and word[len(word)-1] not in vowels:
                       syllable_CVC = word[char-1] + word[char] + word[len(word)-1]
                     #print "solving through CVC..."
                       syllable_structure.append(syllable_CVC)
                   else:
                       syllable_CV = word[char-1] + word[char]
                     #print "solving through CVCV..."
                       syllable_structure.append(syllable_CV)

               #return syllable_structure
                  ##print word, syllable_structure

            elif syll_list != vowel_list:
                #if word[char-1] in vowels and word[char] in vowels:
                   #    print word
                 if char >= 1 and word[char-1] in consonants and word[char] in consonants:
                     ##print word
                    if syl_count == 2:
                        syll_1 = "".join(word[:char])
                        syll_2 = "".join(word[char:])
                       #print "solving through brute force..."
                        syllable_structure.append(syll_1)
                        syllable_structure.append(syll_2)
                        return 1

                    elif syl_count > 2:
                       ##print word, "here"
                         syll_1 = word[:char]
                         syll_2 = word[char:]
                         #syllable_structure.append(syll)
                         #print "solving through recursion.."
                         print syll_1, syll_2, "sending second syllable..."

                         syllabify(syll_1)
                         syllabify(syll_2)
                         return 1
                    else:
                         syllable_structure.append("nothing")        

#              elif word[char-1] in vowels and word[char] in vowels:
#                   #print word
            else:
                syllable_structure.append("nothing")
    #return syllable_structure  

        ##print word, syllable_structure      



            ##print word, syllable_structure



#parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument('-i', '--input', help='Input file', required=True)
#parser.add_argument('-o', '--output', help="Output file")
word_list = []
if __name__ == '__main__':
    for line in inp:
        #word = word[:-1]
        line = line.strip()
        if line:
            print line
            sp = line.split()
            word = sp[0]
            phone_seq = sp[1:]
            syllable_structure = []
            syllabify(phone_seq)
            print syllable_structure
            syllstr = (' '.join(syllable_structure)).strip()
            if not syllstr:
                syllstr = ' '.join(phone_seq)
            word_list.append(word + '\t' + syllstr)

#print word_list
#with open("C:\\Users\\ayushi_pandey\\Desktop\\scripts_borrowing_challenge\\module_rhyming\\syllabified_words_mono.csv", "wb") as f:
with open(out_file, "wb") as f:
    #writer = csv.writer(f)
    #writer.writerows(word_list)
    f.write('\n'.join(word_list))
