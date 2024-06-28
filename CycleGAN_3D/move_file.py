import os
import shutil
import gzip

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

def prepare_image(flist, warped=False):
	dest_root = '/data/hohokam/Yanxi/Data/mri2pet/adcn_w'
	src_root = '/data/amciilab/jay/datasets/mrpetsyn'

	mri_root = os.path.join(src_root, 'FS7')
	pet_root = os.path.join(src_root, 'PUP_FBP')

	fdict = dict()
	# id_set = set()
	for fname in os.listdir(pet_root):
		# pid = fname[fname.find('FBP') + 3:fname.find('L')]
		finfo = os.path.join(pet_root, fname, 'pet_proc', fname + '_pet.param')
		with open(finfo) as f:
			for line in f:
				if line.startswith('fsdir'):
					mri_id = line.split('/')[-2]
					fdict[mri_id] = fname
			# id_set.add(pid)

	with open(os.path.join(dest_root, 'id_map.csv'), 'w') as f:
		for k, v in fdict.items():
			if warped:
				if 'w_' + k + 'N.nii' in flist:
					src_mri = os.path.join(mri_root, k, 'cat12', 'w_' + k + 'N.nii')
					src_pet = os.path.join(pet_root, v, 'pet_proc', 'w_' + v + '_SUVR.nii')

					dest_mri = os.path.join(dest_root, 'images')
					dest_pet = os.path.join(dest_root, 'labels')

					f.write('w_' + k + 'N.nii,' + 'w_' + v + '_SUVR.nii\n')
					shutil.copy(src_mri, dest_mri)
					shutil.copy(src_pet, os.path.join(dest_pet, 'w_' + k + 'N.nii'))
			else:
				if k + 'N.nii' in flist:
					src_mri = os.path.join(mri_root, k, 'cat12', k + 'N.nii')
					src_pet = os.path.join(pet_root, v, 'pet_proc', v + '_SUVR.nii')

					dest_mri = os.path.join(dest_root, 'images')
					dest_pet = os.path.join(dest_root, 'labels')

					f.write(k + 'N.nii,' + v + '_SUVR.nii\n')
					shutil.copy(src_mri, dest_mri)
					shutil.copy(src_pet, os.path.join(dest_pet, k + 'N.nii'))


def rename_pet():
	fdict = dict()
	with open('/scratch/ychen855/Data/mri2pet/all_sample/id_map.csv') as f:
		for line in f:
			linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
			fdict[linelist[1]] = linelist[0]
	
	for fname in os.listdir('/scratch/ychen855/Data/mri2pet/all_sample/pet'):
		shutil.move(os.path.join('/scratch/ychen855/Data/mri2pet/all_sample/pet', fname), os.path.join('/scratch/ychen855/Data/mri2pet/all_sample/pet', fdict[fname]))

def rename_file(name, epoch):
	check_dir = os.path.join('/scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check', name)
	shutil.move(os.path.join(check_dir, str(epoch) + '_net_G_A.pth'), os.path.join(check_dir, str(epoch) + '_net_G.pth'))


def prepare_adni(pet_list, warped=False):
	dest_root = '/data/hohokam/Yanxi/Data/mri2pet/adni'
	src_root = '/data/amciilab/processedDataset/ADNI'

	mri_root = os.path.join(src_root, 'ADNI-FS')
	pet_root = os.path.join(src_root, 'ADNI-PUP', 'FBP')

	fdict = dict()
	# id_set = set()
	for fname in os.listdir(pet_root):
		if fname in pet_list:
			# pid = fname[fname.find('FBP') + 3:fname.find('L')]
			finfo = os.path.join(pet_root, fname, fname + '_pet.param')
			with open(finfo) as f:
				for line in f:
					if line.startswith('fsdir'):
						mri_id = line.split('/')[-2]
						fdict[fname] = mri_id
				# id_set.add(pid)

	with open(os.path.join(dest_root, 'id_map.csv'), 'w') as f:
		for pet in pet_list:
			pet_gz = False
			if warped:
				pass
				# if 'w_' + k + 'N.nii' in flist:
				# 	src_mri = os.path.join(mri_root, k, 'cat12', 'w_' + k + 'N.nii')
				# 	src_pet = os.path.join(pet_root, v, 'pet_proc', 'w_' + v + '_SUVR.nii')

				# 	dest_mri = os.path.join(dest_root, 'images')
				# 	dest_pet = os.path.join(dest_root, 'labels')

				# 	f.write('w_' + k + 'N.nii,' + 'w_' + v + '_SUVR.nii\n')
				# 	shutil.copy(src_mri, dest_mri)
				# 	shutil.copy(src_pet, os.path.join(dest_pet, 'w_' + k + 'N.nii'))
			else:
				if fdict[pet] + 'N.nii' in os.listdir(os.path.join(mri_root, fdict[pet], 'cat12')):
					src_mri = os.path.join(mri_root, fdict[pet], 'cat12', fdict[pet] + 'N.nii')
				else:
					src_mri = os.path.join(mri_root, fdict[pet], 'cat12', fdict[pet] + 'N.nii.gz')
				if pet + '_SUVR.nii' in os.listdir(os.path.join(pet_root, pet, 'pet_proc')):
					src_pet = os.path.join(pet_root, pet, 'pet_proc', pet + '_SUVR.nii')
				else:
					src_pet = os.path.join(pet_root, pet, 'pet_proc', pet + '_SUVR.nii.gz')
					pet_gz = True

				dest_mri = os.path.join(dest_root, 'images')
				dest_pet = os.path.join(dest_root, 'labels')

				f.write(fdict[pet] + 'N.nii,' + pet + '_SUVR.nii\n')
				# shutil.copy(src_mri, dest_mri)
				shutil.copy(src_pet, os.path.join(dest_pet, fdict[pet] + 'N.nii.gz' if pet_gz else fdict[pet] + 'N.nii'))


def move_wmparc():
	src_root = '/data/amciilab/jay/datasets/mrpetsyn/FS7'
	dst_root = '/home/hohokam/Yanxi/Data/mri2pet/682_resample'

	with open(os.path.join(dst_root, 'clinical.csv')) as f:
		f.readline()
		for line in f:
			linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
			pid = linelist[0][:-5]
			if pid not in os.listdir(os.path.join(dst_root, 'wmparc')):
				os.mkdir(os.path.join(dst_root, 'wmparc', pid))
			shutil.copy(os.path.join(src_root, pid, 'mri', 'wmparc.mgz'), os.path.join(dst_root, 'wmparc', pid))

if __name__ == '__main__':

	move_wmparc()

	# pet_list = []
	# id_dict = dict()
	# with open('/data/hohokam/Yanxi/Data/mri2pet/adni/id_map.csv') as f:
	# 	for line in f:
	# 		linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
	# 		id_dict[linelist[1].split('_')[0]] = linelist[0]

	# with open('/scratch/ychen855/clinical_adni.csv') as f:
	# 	with open('/data/hohokam/Yanxi/Data/mri2pet/adni/clinical_adni.csv', 'w') as fout:
	# 		fout.write('image,' + f.readline())
	# 		for line in f:
	# 			linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
	# 			pup = linelist[-2]
	# 			fout.write(id_dict[pup] + ',' + line)

	# normalize_img('/scratch/ychen855/Data/mri2pet/674/warped/raw/test/labels', '/scratch/ychen855/Data/mri2pet/674/warped/normalized/test/labels', False)
	# prepare_image()
	# split_train_val('/scratch/ychen855/Data/mri2pet/200/warped', 160, 20, 20)
	# move_fs()

	# flist = []
	# with open('/data/hohokam/Yanxi/Data/mri2pet/adcn/clinical.csv') as f:
	# 	f.readline()
	# 	for line in f:
	# 		linelist = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
	# 		flist.append('w_' + linelist[0])
	# prepare_image(flist, True)
