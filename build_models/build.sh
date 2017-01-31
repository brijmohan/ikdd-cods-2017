#!/bin/bash

. ../venv/bin/activate

python syllabify_rhymes_vowinit.py raw_data/hindi_corrected_dictionary_15K.tsv srilm_data/syllabified_words_mono_vwinit.tsv

python text_with_counts.py

bash train_char_model.sh
bash train_phone_model.sh

bash train_prosody_model.sh
bash train_syll_model.sh
