import nibabel as nib
import numpy as np
import os

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

def suvr(flist):
    res = []
    for f in flist:
        res.append(get_suvr())

if __name__ == '__main__':
    wmparc_folder = '/data/hohokam/Yanxi/Data/mri2pet/adni/masks'
    pet_folder = '/data/hohokam/Yanxi/Data/mri2pet/adni/gen/gen_baseline_80'

    with open('/scratch/ychen855/mri2pet/suvr_baseline.csv', 'w') as f:
        for pid in os.listdir(pet_folder):
            suvr = get_suvr(os.path.join(pet_folder, pid), os.path.join(wmparc_folder, pid[:-5], 'wmparc.nii'))
            f.write(pid[:-5] + ',' + str(suvr) + '\n')
