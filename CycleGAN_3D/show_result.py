import SimpleITK as sitk
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

ori_file = 'rec_1_50/train/images/189.nii'
gen_file = 'rec_1_50/train/labels/189.nii'

ori_image = nib.load(ori_file).get_fdata()
print(ori_image.shape)
print(np.nanmax(ori_image))
print(np.nanmin(ori_image))

# for i in range(16):
#     plt.subplot(4, 4, i+1)
#     plt.imshow(ori_image[:, :, ori_image.shape[-1] // 16 * i])
#     plt.gcf().set_size_inches(10, 10)
# plt.show()

gen_image = nib.load(gen_file).get_fdata()
print(gen_image.shape)
print(np.nanmax(ori_image))
print(np.nanmin(ori_image))

# for i in range(16):
#     plt.subplot(4, 4, i+1)
#     plt.imshow(gen_image[:, :, gen_image.shape[-1] // 16 * i])
#     plt.gcf().set_size_inches(10, 10)
# plt.show()