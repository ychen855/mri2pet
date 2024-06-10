import os
import SimpleITK as sitk
import numpy as np
import nibabel as nib

def binarize(input, output):
	image = nib.load(input)
	V_wmparc = image.get_fdata()

	MCmask=np.zeros_like(V_wmparc)

	##Reference Region ---Cerebellum cortex
	MCmask[V_wmparc == 8]=1
	MCmask[V_wmparc == 47]=1

	##Target Region -- Mean cortical Regions
	MCmask[V_wmparc==1012]=1 #lh-LOF (lateral-orbital-frontal)
	MCmask[V_wmparc==2012]=1 #rh-LOF
	MCmask[V_wmparc==1014]=1 #lh-MOF (medial-orbital-frontal)
	MCmask[V_wmparc==2014]=1 #rh-MOF
	MCmask[V_wmparc==1015]=1 #lh-MT  (middle-temporal)
	MCmask[V_wmparc==2015]=1 #rh-MT
	MCmask[V_wmparc==1030]=1 #lh-ST  (superior-temporal)
	MCmask[V_wmparc==2030]=1 #rh-ST
	MCmask[V_wmparc==1025]=1 #lh-PREC (precuneus)
	MCmask[V_wmparc==2025]=1 #rh-PREC
	MCmask[V_wmparc==1027]=1 #lh-RMF (rostral-middle-frontal)
	MCmask[V_wmparc==2027]=1 #rh-RMF
	MCmask[V_wmparc==1028]=1 #lh-SF  (superior-frontal)
	MCmask[V_wmparc==2028]=1 #rh-SF

	new_image = nib.Nifti1Image(MCmask, image.affine, image.header)
	nib.save(new_image, output)

if __name__ == '__main__':
	src = '/data/hohokam/Yanxi/Data/mri2pet/adni/masks'
	dst = '/data/hohokam/Yanxi/Data/mri2pet/adni/masks_b'

	for f in os.listdir(src):
		binarize(os.path.join(src, f), os.path.join(dst, f))