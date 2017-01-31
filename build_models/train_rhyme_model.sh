#!/bin/bash

OP="max"
TRAIN_FILE="srilm_data/srilm_train_char_$OP.txt"
MODEL_FILE="models/char_final_$OP.wb.lm"

ngram-count -debug 1 -order 6 -text-has-weights \
		-text $TRAIN_FILE \
		-wbdiscount1 \
		-wbdiscount2 \
		-wbdiscount3 \
		-wbdiscount4 \
		-wbdiscount5 \
		-wbdiscount6 \
		-lm $MODEL_FILE


#TEST_FILE="srilm_test_char_$OP.txt"

#ngram -debug 2 -order 6 \
#		-lm $MODEL_FILE \
#		-ppl $TEST_FILE > "test_char_final_$OP.wb.ppl"
