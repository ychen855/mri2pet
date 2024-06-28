import os
import numpy as np
import torch

def main():
	warped = False
	diag_dict = dict()

	with open('/home/hohokam/Yanxi/Data/mri2pet/adni/clinical_adni.csv') as f:
		f.readline()
		for line in f:
			linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
			mriid = 'w_' + linelist[0] if warped else linelist[0]
			abeta = linelist[1]
			age = linelist[2]
			sex = linelist[3]
			if sex == 'F':
				sex_res = '0'
			else:
				sex_res = '1'
			diag_dict[mriid] = (abeta, age, sex_res)

	with open('/home/hohokam/Yanxi/Data/mri2pet/adni/data_split.csv') as f:
		with open('/home/hohokam/Yanxi/Data/mri2pet/adni/clinical.csv', 'w') as fout:
			fout.write('image,abeta,age,sex,group\n')
			for line in f:
				linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
				pid = linelist[0]
				group = linelist[-1]
				fout.write(','.join([pid, diag_dict[pid][0], diag_dict[pid][1], diag_dict[pid][2], group]) + '\n')

def n_p():
	root = '/data/amciilab/jay/datasets/mrpetsyn/PUP_FBP'
	id_set = set()
	for f in os.listdir(root):
		pid = f[3:11]
		id_set.add(pid)
	print(len(id_set))

if __name__ == '__main__':
	# main()
	n_p()