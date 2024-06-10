import os
import shutil
import numpy as np
import nibabel as nib

def prepare_image(warp=False):
	dest_root = '/data/hohokam/Yanxi/Data/mri2pet/adni'
	src_root = '/data/amciilab/processedDataset/ADNI/ADNI-FS'
	dest_mri = os.path.join(dest_root, 'images')
	dest_pet = os.path.join(dest_root, 'labels')

	f_id_map = open(os.path.join(src_root, 'paired.csv'))
	id_map = dict()
	for line in f_id_map:
		linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
		mri_ls = linelist[0].split('/')
		w_mri = '/'.join(mri_ls[:-1] + ['w_' + mri_ls[-1]]) if warp else linelist[0]
		pet_ls = linelist[1].split('/')
		w_pet = '/'.join(pet_ls[:-1] + ['w_' + pet_ls[-1]]) if warp else linelist[1]

		id_map[w_mri] = w_pet

	with open(os.path.join(dest_root, 'id_map.csv'), 'w') as fout_map:
		pid_set = set()
		n_patient = 0
		n_image = 0
		for k, v in id_map.items():
			folder = k.split('/')[1]
			pid = folder[1:folder.find('L')]
			if pid not in pid_set:
				pid_set.add(pid)
				n_patient += 1
				fmri = k.split('/')[-1]
				fpet = v.split('/')[-1]
				shutil.copy(os.path.join(src_root, k), dest_mri)
				shutil.copy(os.path.join(src_root, v), os.path.join(dest_pet, fmri))
				fout_map.write(fmri + ',' + fpet + '\n')
				n_image += 1
		print(n_patient)
		print(n_image)

def split_train_val(data_root, n_train, n_val, n_test):
	# data_root = '/scratch/ychen855/Data/mri2pet/all_sample'
	id_map = dict()
	with open(os.path.join(data_root, 'id_map.csv')) as f:
		n = 0
		for line in f:
			linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
			id_map[linelist[0]] = linelist[1]

	for k, v in id_map.items():
		if n < n_train:
			shutil.move(os.path.join(data_root, 'mri', k), os.path.join(data_root, 'train', 'images'))
			shutil.move(os.path.join(data_root, 'pet', k), os.path.join(data_root, 'train', 'labels'))
		elif n < n_train + n_val:
			shutil.move(os.path.join(data_root, 'mri', k), os.path.join(data_root, 'val', 'images'))
			shutil.move(os.path.join(data_root, 'pet', k), os.path.join(data_root, 'val', 'labels'))
		else:
			shutil.move(os.path.join(data_root, 'mri', k), os.path.join(data_root, 'test', 'images'))
			shutil.move(os.path.join(data_root, 'pet', k), os.path.join(data_root, 'test', 'labels'))
		n += 1

def move_fs():
	dest_root = '/scratch/ychen855/Data/mri2pet'
	src_root = '/data/amciilab/jay/datasets/mrpetsyn'
	dest_mri = os.path.join(dest_root, 'mri')
	dest_pet = os.path.join(dest_root, 'pet')

	f_id_map = open(os.path.join(dest_root, 'fid_map.csv'))
	id_map = dict()
	for line in f_id_map:
		linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
		id_map[linelist[0]] = linelist[1]

	for k, v in id_map.items():
		folder_mri = k.split('.')[0]
		folder_pet = v.split('_')[0]
		os.mkdir(os.path.join(dest_mri, 'fs', folder_mri))
		os.mkdir(os.path.join(dest_mri, 'fs', folder_mri, folder_mri))
		shutil.copy(os.path.join(src_root, 'FS7', folder_mri, 'surf', 'lh.pial'), os.path.join(dest_mri, 'fs', folder_mri, folder_mri))
		shutil.copy(os.path.join(src_root, 'FS7', folder_mri, 'surf', 'lh.white'), os.path.join(dest_mri, 'fs', folder_mri, folder_mri))
		shutil.copy(os.path.join(src_root, 'FS7', folder_mri, 'surf', 'rh.pial'), os.path.join(dest_mri, 'fs', folder_mri, folder_mri))
		shutil.copy(os.path.join(src_root, 'FS7', folder_mri, 'surf', 'rh.white'), os.path.join(dest_mri, 'fs', folder_mri, folder_mri))
		
		os.mkdir(os.path.join(dest_pet, 'nifti', folder_pet))
		shutil.copy(os.path.join(src_root, 'PUP_FBP', folder_pet, 'pet_proc', v), os.path.join(dest_pet, 'nifti', folder_pet))

def prepare_all():
	dest_root = '/scratch/ychen855/Data/mri2pet/all_sample'
	src_root = '/data/amciilab/jay/datasets/mrpetsyn'

	mri_root = os.path.join(src_root, 'FS7')
	pet_root = os.path.join(src_root, 'PUP_FBP')

	fdict = dict()
	for fname in os.listdir(pet_root):
		finfo = os.path.join(pet_root, fname, 'pet_proc', fname + '_pet.param')
		with open(finfo) as f:
			for line in f:
				if line.startswith('fsdir'):
					mri_id = line.split('/')[-2]
					fdict[mri_id] = fname
	n_patient = 0
	n_image = 0
	with open(os.path.join(dest_root, 'id_map.csv'), 'w') as f:
		for k, v in fdict.items():
			src_mri = os.path.join(mri_root, k, 'cat12', 'w_' + k + 'N.nii')
			src_pet = os.path.join(pet_root, v, 'pet_proc', 'w_' + v + '_SUVR.nii')

			dest_mri = os.path.join(dest_root, 'mri')
			dest_pet = os.path.join(dest_root, 'pet')

			f.write('w_' + k + 'N.nii,w_' + v + '_SUVR.nii\n')
			shutil.copy(src_mri, dest_mri)
			shutil.copy(src_pet, dest_pet)

	print(n_patient)
	print(n_image)

def rename_pet():
	fdict = dict()
	with open('/scratch/ychen855/Data/mri2pet/all_sample/id_map.csv') as f:
		for line in f:
			linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
			fdict[linelist[1]] = linelist[0]
	
	for fname in os.listdir('/scratch/ychen855/Data/mri2pet/all_sample/pet'):
		shutil.move(os.path.join('/scratch/ychen855/Data/mri2pet/all_sample/pet', fname), os.path.join('/scratch/ychen855/Data/mri2pet/all_sample/pet', fdict[fname]))

def normalize_img(src, dst, normalize):
	for f in os.listdir(src):
		img = nib.load(os.path.join(src, f)).get_fdata()
		np.nan_to_num(img, copy=False, nan=0.0)
		if normalize:
			new_img = (img - np.mean(img)) / np.std(img)
		new_img = nib.Nifti1Image(img, np.eye(4))
		nib.save(new_img, os.path.join(dst, f))

def rename_file(name, epoch):
	check_dir = os.path.join('/scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check', name)
	shutil.move(os.path.join(check_dir, str(epoch) + '_net_G_A.pth'), os.path.join(check_dir, str(epoch) + '_net_G.pth'))

def move_tet_good():
	good_set = set()
	with open('/scratch/ychen855/Data/mri2pet/674/warped/good_list.csv') as f:
		for line in f:
			good_set.add(line[:-1])
	src = '/scratch/ychen855/Data/mri2pet/674/warped/tet'
	dst = '/scratch/ychen855/Data/mri2pet/674/warped/tet_510'
	for sample in os.listdir(src):
		if sample in good_set:
			os.mkdir(os.path.join(dst, sample))
			os.mkdir(os.path.join(dst, sample, sample))
			shutil.copy(os.path.join(src, sample, sample, 'lh_combine_final2.1.face'), os.path.join(dst, sample, sample))
			shutil.copy(os.path.join(src, sample, sample, 'lh_combine_final2.1.edge'), os.path.join(dst, sample, sample))
			shutil.copy(os.path.join(src, sample, sample, 'lh_combine_final2.1.ele'), os.path.join(dst, sample, sample))
			shutil.copy(os.path.join(src, sample, sample, 'lh_combine_final2.1.node'), os.path.join(dst, sample, sample))

def move_wmparc():
	dest_root = '/data/hohokam/Yanxi/Data/mri2pet/adni'
	src_root = '/data/amciilab/processedDataset/ADNI/ADNI-FS'
	dest_folder = os.path.join(dest_root, 'wmparc')

	mri_ls = []

	with open(os.path.join(dest_root, 'data_split.csv')) as f:
		for line in f:
			linelist = line.split('\n')[0].split('\t')
			mri_id = linelist[0].split('.')[0]
			mri_ls.append(mri_id)
	
	for mri_id in mri_ls:
		if mri_id in os.listdir(src_root):
			if mri_id not in os.listdir(dest_folder):
				os.mkdir(os.path.join(dest_folder, mri_id))
			shutil.copy(os.path.join(src_root, mri_id, 'mri', 'wmparc.mgz'), os.path.join(dest_folder, mri_id))
		elif mri_id + 'CF' in os.listdir(src_root):
			mri_id_n = mri_id + 'CF'
			if mri_id_n not in os.listdir(dest_folder):
				os.mkdir(os.path.join(dest_folder, mri_id_n))
			shutil.copy(os.path.join(src_root, mri_id_n, 'mri', 'wmparc.mgz'), os.path.join(dest_folder, mri_id_n))
		else:
			print(mri_id)

def move_mask():
	src = '/data/hohokam/Yanxi/Data/mri2pet/adni/wmparc'
	dst = '/data/hohokam/Yanxi/Data/mri2pet/adni/masks'

	for f in os.listdir(src):
		mri_id = f.split('T')[0] + 'T'
		shutil.move(os.path.join(src, f, 'wmparc.nii'), os.path.join(dst, mri_id + '.nii'))

if __name__ == '__main__':
	move_mask()
	# move_wmparc()
	# normalize_img('/scratch/ychen855/Data/mri2pet/674/warped/raw/test/labels', '/scratch/ychen855/Data/mri2pet/674/warped/normalized/test/labels', False)
	# prepare_image()
	# split_train_val('/scratch/ychen855/Data/mri2pet/200/warped', 160, 20, 20)
	# move_fs()
	# prepare_all()
	# rename_pet()
	# move_tet_good()

	# datasets = ['200']
	# groups = 5
	# epoch = 80
	# for dataset in datasets:
	# 	for i in range(groups):
	# 		rename_file(dataset + '_baseline_cross_' + str(i) + '_' + str(epoch) + 'epoch', epoch)