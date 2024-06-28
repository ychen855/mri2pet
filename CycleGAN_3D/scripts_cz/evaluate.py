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

def evaluate_all(gen_paths, true_path, fmap, log_file):

    map_dict = {}
    with open(fmap) as f:
        for line in f:
            linelist = line.split('\n')[0].split(',')
            map_dict[linelist[0]] = linelist[1]

    ssims = []
    psnrs = []
    mses = []
    for gen_path in gen_paths:
        ssim, psnr, mse = evaluate(gen_path, true_path, map_dict, log_file)
        ssims += ssim
        psnrs += psnr
        mses += mse
    
    ssim_arry = np.array(ssims)
    psnr_arry = np.array(psnrs)
    mse_arry = np.array(mses)

    mean_ssim = np.mean(ssim_arry)
    std_ssim = np.std(ssim_arry)
    mean_psnr = np.mean(psnr_arry)
    std_psnr = np.std(psnr_arry)
    mean_mse = np.mean(mse_arry)
    std_mse = np.std(mse_arry)

    with open(log_file, 'w') as f:
        f.write('mean_ssim,std_ssim,mean_psnr,std_psnr,mean_mes,std_mse\n')
        f.write(','.join([str(ele) for ele in [mean_ssim, std_ssim, mean_psnr, std_psnr, mean_mse, std_mse]]) + '\n')

def get_suvr(petfile, wmparcfile):
    ### petfile is the path of pet image need to calculate MCSUVR:str
    ### wmparcfile is the path of standard pet inage: str
    V_pet=nib.load(petfile).get_fdata()
    np.nan_to_num(V_pet, copy=False, nan=0.0)

    V_wmparc=nib.load(wmparcfile).get_fdata()

    CBmask=np.zeros(V_pet.shape)
    CBWmask=np.array(CBmask,copy=True)
    MCmask=np.array(CBmask,copy=True)

    ##Reference Region ---Cerebellum cortex
    CBmask[V_wmparc == 8]=1
    CBmask[V_wmparc == 47]=1

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

    MC_suvr=np.mean(V_pet[MCmask==1])/np.mean(V_pet[CBmask==1])

    return MC_suvr

def evaluate_suvr():
    pass

if __name__ == '__main__':
    ### evaluate performance

    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str)
    parser.add_argument('--exp', type=str)
    parser.add_argument('--dataset', type=str)
    parser.add_argument('--epoch', type=int)
    parser.add_argument('--map', type=str)
    parser.add_argument('--n_fold', type=int)
    parser.add_argument('--result', type=str)
    parser.add_argument('--all', action='store_true')

    args = parser.parse_args()

    log_file = os.path.join(args.result, 'log_' + args.exp + '_' + str(args.epoch) + '.txt')
    true_path = os.path.join(args.root, args.dataset, 'labels')

    if args.all:
        gen_paths = []
        for i in range(args.n_fold):
            gen_path = os.path.join(args.root, args.dataset, 'gen', 'gen_' + args.exp + '_' + str(i) + '_' + str(args.epoch))
            gen_paths.append(gen_path)
        
        evaluate_all(gen_paths, true_path, args.map, log_file)

        
