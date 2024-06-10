import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

def visualize(mri_path, pet_path, gen_path, mask_path, pid, out_path):
    mri_file = os.path.join(mri_path, pid)
    pet_file = os.path.join(pet_path, pid)
    gen_file = os.path.join(gen_path, pid)
    mask_file = os.path.join(mask_path, pid)

    mri_image = nib.load(mri_file).get_fdata()
    pet_image = nib.load(pet_file).get_fdata()
    gen_image = nib.load(gen_file).get_fdata()
    mask_image = nib.load(mask_file).get_fdata()

    np.nan_to_num(mri_image, copy=False, nan=0.0)
    np.nan_to_num(pet_image, copy=False, nan=0.0)
    np.nan_to_num(gen_image, copy=False, nan=0.0)
    np.nan_to_num(mask_image, copy=False, nan=0.0)

    cols = ['MRI', 'Real PET', 'Synthesized PET', 'Mask']
    rows = ['Axial', 'Coronal', 'Sagital']

    fig, axes = plt.subplots(nrows=3, ncols=4)
    # plt.subplots_adjust(top = 0.7, bottom=0.0, hspace=0.05, wspace=-0.25)

    for ax, col in zip(axes[0], cols):
        ax.set_title(col)

    for ax, row in zip(axes[:,0], rows):
        ax.set_ylabel(row)

    plt.setp(axes, xticks=[], yticks=[])

    plt.subplot(3, 4, 1)
    plt.imshow(np.rot90(mri_image[:, :, 64]), cmap='gray')
    plt.subplot(3, 4, 2)
    plt.imshow(np.rot90(pet_image[:, :, 64]), cmap='gray')
    plt.subplot(3, 4, 3)
    plt.imshow(np.rot90(gen_image[:, :, 64]), cmap='gray')
    plt.subplot(3, 4, 4)
    plt.imshow(np.rot90(mask_image[:, :, 64]), cmap='gray')

    plt.subplot(3, 4, 5)
    plt.imshow(np.rot90(mri_image[:, 64, :]), cmap='gray')
    plt.subplot(3, 4, 6)
    plt.imshow(np.rot90(pet_image[:, 64, :]), cmap='gray')
    plt.subplot(3, 4, 7)
    plt.imshow(np.rot90(gen_image[:, 64, :]), cmap='gray')
    plt.subplot(3, 4, 8)
    plt.imshow(np.rot90(mask_image[:, 64, :]), cmap='gray')

    plt.subplot(3, 4, 9)
    plt.imshow(np.rot90(mri_image[64, :, :]), cmap='gray')
    plt.subplot(3, 4, 10)
    plt.imshow(np.rot90(pet_image[64, :, :]), cmap='gray')
    plt.subplot(3, 4, 11)
    plt.imshow(np.rot90(gen_image[64, :, :]), cmap='gray')
    plt.subplot(3, 4, 12)
    plt.imshow(np.rot90(mask_image[64, :, :]), cmap='gray')

    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(out_path, pid.split('.')[0] + '.png'))
    # plt.savefig('/scratch/ychen855/mri2pet/all.png')
    plt.close()

if __name__ == '__main__':
    mri_path = '/data/hohokam/Yanxi/Data/mri2pet/adni/images'
    pet_path = '/data/hohokam/Yanxi/Data/mri2pet/adni/labels'
    gen_path = '/data/hohokam/Yanxi/Data/mri2pet/adni/gen/gen_abeta_80'
    mask_path = '/data/hohokam/Yanxi/Data/mri2pet/adni/masks'
    out_path = '/data/hohokam/Yanxi/Data/mri2pet/adni/visualization'
    folder = '/data/hohokam/Yanxi/Data/mri2pet/adni/images'
    for pid in os.listdir(folder):
        visualize(mri_path, pet_path, gen_path, mask_path, pid, out_path)