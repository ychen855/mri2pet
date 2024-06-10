import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

def check_dim(nii_file):
    nii_mtx = nib.load(nii_file).get_fdata()
    nii_mtx = np.squeeze(nii_mtx)
    print(nii_mtx.shape)

def visualize(nii_file):
    image = nib.load(nii_file).get_fdata()
    np.nan_to_num(image, copy=False, nan=0.0)

    plt.subplot(1, 3, 1)
    plt.imshow(np.rot90(image[64, :, :]), cmap='gray')
    plt.subplot(1, 3, 2)
    plt.imshow(np.rot90(image[:, 64, :]), cmap='gray')
    plt.subplot(1, 3, 3)
    plt.imshow(np.rot90(image[:, :, 64]), cmap='gray')

    plt.savefig('/scratch/ychen855/mri2pet/' + nii_file.split('/')[-1].split('.')[0] + '.png')

if __name__ == '__main__':
    nii_file = '/data/hohokam/Yanxi/Data/mri2pet/adni/labels/FBP002S4219L101811M4.nii'
    image = nib.load(nii_file).get_fdata()
    np.nan_to_num(image, copy=False, nan=0.0)

    plt.subplot(1, 3, 1)
    plt.imshow(np.rot90(image[64, :, :]), cmap='gray')
    plt.subplot(1, 3, 2)
    plt.imshow(np.rot90(image[:, 64, :]), cmap='gray')
    plt.subplot(1, 3, 3)
    plt.imshow(np.rot90(image[:, :, 64]), cmap='gray')

    plt.savefig('/scratch/ychen855/mri2pet/image_processing/' + nii_file.split('/')[-1].split('.')[0] + '.png')
    # root = '/data/hohokam/Yanxi/Data/plasma_image/adni_198/images'
    # for f in os.listdir(root):
    #     check_dim(os.path.join(root, f))
    # nii_file = '/data/amciilab/processedDataset/ADNI/ADNI-FS/m082S6283L050218N33TCF/cat12/m082S6283L050218N33TCFN.nii'
    # check_dim(nii_file)
    # visualize(nii_file)