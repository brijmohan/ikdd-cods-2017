#!/bin/bash
#
# Get phonological score of a list of words
# bash pscore.sh <file with list of words - each word on a new line> <out folder>

#. ../borrowenv/bin/activate

wordlist="$1"
outfolder="$2"
echo "Processing : $wordlist , Out folder: $outfolder"

mkdir -p "$outfolder"

ENGLISH_G2P="../g2p-seq2seq-cmudict"
HINDI_G2P="../hinutf-g2p-64"

g2p-seq2seq --decode "$wordlist" --model "$ENGLISH_G2P" --output "$outfolder/eng.dict"

python transliterate2dev.py "$wordlist" "$outfolder/trans.txt"
g2p-seq2seq --decode "$outfolder/trans.txt" --model "$HINDI_G2P" --output "$outfolder/hin.dict"

python ../build_models/syllabify_rhymes_vowinit.py "$outfolder/hin.dict" "$outfolder/syll.txt"

python v5_compute_partial_rhymes.py "$outfolder/syll.txt" "$outfolder/rhyme.txt"

python score.py "$outfolder"
