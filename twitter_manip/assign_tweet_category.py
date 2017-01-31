#!/usr/bin/env python

import os, json

dataset_csv_file = '../../../Datasheet.csv'
twitter_data_folder = '../tweet.sh/twitter_data'

tw_date_dict = {}
for root, folder, files in os.walk(twitter_data_folder):
	for filename in files:
		print "Reading: "+filename
		with open(os.path.join(root, filename)) as tfile:
			for line in tfile.read().splitlines():
				line = line.strip()
				if line:
					twjson = json.loads(line.strip())
					if 'created_at' in twjson:
						tw_date_dict[twjson['id_str']] = twjson['created_at']


with open(dataset_csv_file) as dset, open('tweet_cat.txt', 'wb') as tcat:
	print "Reading:"+dataset_csv_file
	for line in dset.read().splitlines():
		sp = line.split(',')
		twid = sp[0]
		if twid in tw_date_dict:
			lang_arr = []
			for word in sp[1:]:
				spw = word.split(':')
				lang = spw[2]
				if lang == 'EN':
					lang_arr.append(0)
				elif lang == 'HI':
					lang_arr.append(1)


			# Do aggregation of tweets category and lang count
			encnt = lang_arr.count(0) / float(len(lang_arr))
			hicnt = lang_arr.count(1)  / float(len(lang_arr))
			twcat = ''
			if encnt >= 0.9:
				twcat = 'EN'
			if hicnt >= 0.9:
				twcat = 'HI'
			if encnt >= 0.5 and encnt < 0.9:
				twcat = 'CME'
			if hicnt >= 0.5 and hicnt < 0.9:
				twcat = 'CMH'
			if encnt == hicnt:
				twcat = 'CMEQ'

			tcat.write(twid + '\t' + tw_date_dict[twid] + '\t' + twcat + '\t' + 'en:'+str(encnt)+','+'hi:'+str(hicnt) + '\n')

		



