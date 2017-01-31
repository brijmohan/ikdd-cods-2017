#*-* encoding: utf8 *-*
import os, json

dataset_csv_file = '../../../Datasheet.csv'
twitter_data_folder = '../tweet.sh/twitter_data'

lang_lab_file = 'twitter_lang_label.txt'
eng_vocab_file = 'twitter_english_vocab.txt'

tw_word_dict = {}
english_vocab = set()

tw_lang_label_dict = {}
with open(dataset_csv_file) as dset:
    for line in dset.read().splitlines():
        line = line.strip()
        if line:
            sp = line.split(',')
            twid = sp[0]
            tw_lang_label_dict[twid] = []
            for w in sp[1:]:
                wordsp = w.split(':')
                tw_lang_label_dict[twid].append((int(wordsp[0]),
                    int(wordsp[1]), wordsp[2]))


#with open(lang_lab_file, 'wb') as labfile, open(eng_vocab_file, 'wb') as evocab:
with open(eng_vocab_file, 'wb') as evocab:
    for root, folder, files in os.walk(twitter_data_folder):
        for filename in files:
            print "Reading: "+filename
            with open(os.path.join(root, filename)) as tfile:
                for line in tfile.read().splitlines():
                    line = line.strip()
                    if line:
                        twjson = json.loads(line.strip())
                        if 'created_at' in twjson:
                            try:
                                twid = twjson['id_str']
                                print twid
                                twtext = twjson['text']
                                char_arr = tw_lang_label_dict[twid]
                                #words = []
                                for start, end, lang in char_arr:
                                    w = twtext[start-1:end]
                                    if lang == "EN":
                                        english_vocab.add(w.encode('utf8'))
                                    #words.append(w.encode('utf8')+'/'+lang)

                                #labfile.write(twid + '\t' + (' '.join(words)).encode('utf8') + '\n')
                            except:
                                print "Error."


    evocab.write('\n'.join(english_vocab))



