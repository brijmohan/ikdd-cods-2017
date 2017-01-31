import sys
from litcm import LIT
sys.path.append('../litcm/litcm')
import indictrans as tn
import re

args = sys.argv

def trans2dev(w):
    # Find transliteration of w
    lit = LIT(labels=['hin', 'eng'], transliteration=True)
    trans_w_wx = wx = tn.RomanConvertor(lit.tree[lit.tag_dct['hin']],
        w, 'hin').transliterate()
    print trans_w_wx
    trans_w = lit.wxp.wx2utf(trans_w_wx, 'hin')
    if 'M' in trans_w:
        trans_w = trans_w.replace('M', u'\u0902'.encode('utf8'))
    trans_w = re.sub(r'[a-zA-Z]', '', trans_w)
    return trans_w

with open(args[1]) as inp, open(args[2], 'wb') as out:
    for line in inp.read().splitlines():
        line = line.strip()
        if line:
            out.write(trans2dev(line) + '\n')

