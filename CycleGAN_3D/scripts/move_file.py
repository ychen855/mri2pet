import os
import shutil

def prepare_image(warp=False):
	dest_root = '/home/hohokam/Yanxi/Data/mri2pet/1463/warped/raw'
	src_root = '/data/amciilab/jay/datasets/mrpetsyn'
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
			if pid not in pid_set and n_patient < 200:
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
	dest_root = '/home/hohokam/Yanxi/Data/mri2pet/1463/warped/raw'
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

			dest_mri = os.path.join(dest_root, 'images')
			dest_pet = os.path.join(dest_root, 'labels')

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

if __name__ == '__main__':
	# normalize_img('/scratch/ychen855/Data/mri2pet/674/warped/raw/test/labels', '/scratch/ychen855/Data/mri2pet/674/warped/normalized/test/labels', False)
	# prepare_image()
	# split_train_val('/scratch/ychen855/Data/mri2pet/200/warped', 160, 20, 20)
	# move_fs()
	prepare_all()
	# rename_pet()
	# datasets = ['200']
	# groups = 5
	# epoch = 80
	# for dataset in datasets:
	# 	for i in range(groups):
	#		rename_file(dataset + '_baseline_cross_' + str(i) + '_' + str(epoch) + 'epoch', epoch)
