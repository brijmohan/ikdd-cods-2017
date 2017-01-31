from autocorrect import spell
import re

input_file = 'twitter_lang_label.txt'
output_file = 'gt.txt'

gt = {}

with open(input_file) as inp, open(output_file, 'wb') as ofile:
	lines = inp.read().splitlines()
	line_arr = []
	i = 0
	line = ''
	while i < len(lines):
		currline = lines[i].strip()
		if currline:
			if currline[0].isdigit():
				line_arr.append(line.strip())
				line = currline
			else:
				line += (' ' + lines[i])
		i += 1
	print "Done collating lines..."

	lines = []
	for line in line_arr:
		#print line
		line = line.split('\t')

		if len(line) > 1:
			line = line[1]
			sp = line.split()
			warr = []
			larr = []
			for wl in sp:
				if '/' in wl:
					sp1 = wl.split('/')
					warr.append(sp1[0])
					larr.append(sp1[1])

			nlarr = len(larr)
			for idx, lang in enumerate(larr):
				if lang == 'EN':
					bindex = 0
					w = warr[idx].lower()
					w = spell(re.sub(r'(.)\1+', r'\1\1', w))
					if idx == 0 and nlarr > 1:
						if larr[idx+1] == 'HI':
							bindex = 1
					elif idx == nlarr-1 and nlarr > 1:
						if larr[idx-1] == 'HI':
							bindex = 1
					elif idx > 0 and idx < nlarr-1 and nlarr > 1:
						if larr[idx-1] == 'HI' and larr[idx+1] == 'HI':
							bindex = 1

					w = w.lower()
					if w not in gt:
						print w
						gt[w] = []
					gt[w].append(str(bindex))
				
	ofile.write('\n'.join(["{} : {}".format(k, ','.join(v)) for k, v in gt.items()]))

