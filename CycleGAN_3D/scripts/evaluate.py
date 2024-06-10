import os
import SimpleITK as sitk
import numpy as np
import nibabel as nib
from scipy.stats import ttest_rel, ttest_ind
from skimage.metrics import structural_similarity, peak_signal_noise_ratio, mean_squared_error
import argparse

def evaluate(gen_path, true_path, map_dict, log_file):
    ssim = []
    psnr = []
    mse = []
    for f in os.listdir(gen_path):
        gen_image = nib.load(os.path.join(gen_path, f)).get_fdata()
        true_image = nib.load(os.path.join(true_path, map_dict[f])).get_fdata()
        np.nan_to_num(gen_image, copy=False, nan=0.0)
        np.nan_to_num(true_image, copy=False, nan=0.0)

        gen_image = (gen_image - np.mean(gen_image)) / np.std(gen_image)
        true_image = (true_image - np.mean(true_image)) / np.std(true_image)
        
        gen_image = gen_image - np.min(gen_image)
        gen_image = gen_image / (np.max(gen_image) - np.min(gen_image)) * 255.0
        true_image = true_image - np.min(true_image)
        true_image = true_image / (np.max(true_image) - np.min(true_image)) * 255.0

        cur_ssim = structural_similarity(true_image, gen_image, data_range=255.0, full=False)
        ssim.append(cur_ssim)
        cur_psnr = peak_signal_noise_ratio(true_image, gen_image, data_range=255.0)
        psnr.append(cur_psnr)
        cur_mse = mean_squared_error(true_image, gen_image)
        mse.append(cur_mse)

    return (ssim, psnr, mse)


if __name__ == '__main__':
    ### evaluate performance

    parser = argparse.ArgumentParser()
    parser.add_argument('--exp', type=str, default='baseline')
    parser.add_argument('--dataset', type=str)
    parser.add_argument('--epoch', type=int)
    parser.add_argument('--map', type=str)

    args = parser.parse_args()

    avg_ssim = []
    avg_psnr = []
    avg_mse = []
    exp_name = args.exp
    print(args.dataset)
    print(exp_name)
    epoch = args.epoch

    mri_pet_map = dict()
    with open(args.map) as f:
        for line in f:
            linelist = line.split('\n')[0].split(',')
            mri_pet_map[linelist[0]] = linelist[1]

    log_file = 'log_' + exp_name + '.txt'
    with open(log_file, 'w') as f:
        f.write('SSIM,PSNR,MSE\n')

        for i in range(5):
            gen_path = '/data/hohokam/Yanxi/Data/mri2pet/' + args.dataset + '/gen/gen_' + exp_name + '_' + str(i) + '_' + str(epoch)
            true_path = '/data/hohokam/Yanxi/Data/mri2pet/' + args.dataset + '/labels'
            # log_file = '/data/hohokam/Yanxi/Data/mri2pet/' + args.dataset + '/gen/log_' + exp_name + '_' + str(i) + '.txt'

            ssim, psnr, mse = evaluate(gen_path, true_path, mri_pet_map, log_file)
            avg_ssim += ssim
            avg_psnr += psnr
            avg_mse += mse

        for i in range(len(avg_ssim)):
            f.write(','.join([str(avg_ssim[i]), str(avg_psnr[i]), str(avg_mse[i])]) + '\n')
        
        f.write('mean ssim: ' + str(np.mean(avg_ssim)) + '\n')
        f.write('std ssim: ' + str(np.std(avg_ssim)) + '\n\n')
        f.write('mean psnr: ' + str(np.mean(avg_psnr)) + '\n')
        f.write('std psnr: ' + str(np.std(avg_psnr)) + '\n\n')
        f.write('mean mse: ' + str(np.mean(avg_mse)) + '\n')
        f.write('std mse: ' + str(np.std(avg_mse)) + '\n')

    print('mean ssim: ', np.mean(avg_ssim), ' | std ssim: ', np.std(avg_ssim))
    print('mean psnr: ', np.mean(avg_psnr), ' | std psnr: ', np.std(avg_psnr))
    print('mean mse: ', np.mean(avg_mse), ' | std mse: ', np.std(avg_mse))
