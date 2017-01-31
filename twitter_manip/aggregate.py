#!/usr/bin/env python
import pandas as pd
import json
import math
import numpy as np
import matplotlib.pyplot as plt

cat_file = 'tweet_cat.txt'

cat_dict = {}

with open(cat_file) as cfile:
	for line in cfile.read().splitlines():
		line = line.strip()
		if line:
			sp = line.split('\t')
			cat = sp[2]
			if cat not in cat_dict:
				cat_dict[cat] = []
			langsp = sp[3].split(',')
			en = float(langsp[0].split(':')[1])
			hi = float(langsp[1].split(':')[1])
			cat_dict[cat].append({"id": sp[0], "date": sp[1], "en": en, "hi": hi})

monthly = {}
# Hindi agg
df = pd.read_json(json.dumps(cat_dict['CMEQ']), orient='records', convert_dates=["date"])
#print df.index
df = df.reset_index().set_index('date')

monthly_hi = df.resample('M').mean()

enmean = []
himean = []
months = []
for index, row in monthly_hi.iterrows():
	if not math.isnan(row['en']) and not math.isnan(row['hi']):
		print index.strftime("%B,%Y"), row['en'], row['hi']
		months.append(index.strftime("%B,%Y"))
		enmean.append(row['en'])
		himean.append(row['hi'])

ind = np.arange(len(enmean))
width = 0.35

p1 = plt.bar(ind, enmean, width, color='r')
p2 = plt.bar(ind, himean, width, color='y', bottom=enmean)

#plt.tight_layout()
plt.ylabel('Language probability')
plt.title('Months')
plt.xticks(ind + width/2., months, rotation=70)
plt.yticks(np.arange(0, 1, 0.1))
plt.legend((p1[0], p2[0]), ('English', 'Hindi'))

plt.show()