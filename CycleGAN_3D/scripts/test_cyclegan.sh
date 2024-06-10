#!/bin/bash

#SBATCH -n 4                        # number of cores
#SBATCH --mem=32G
#SBATCH -p general
#SBATCH -G a100:1
#SBATCH -t 0-04:00:00                 # wall time (D-HH:MM:SS)
#SBATCH -o /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.out             # STDOUT (%j = JobId)
#SBATCH -e /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.err             # STDERR (%j = JobId)
#SBATCH --mail-type=END             # Send a notification when the job starts, stops, or fails
#SBATCH --mail-user=ychen855@asu.edu # send-to address

module purge    # Always purge modules to ensure a consistent environment

module load cuda-11.7.0-gcc-11.2.0

source ~/.bashrc
conda activate cyclegan

EPOCH=80
NAME=200_cross_0_80epoch
IMG_DIR=/scratch/ychen855/Data/mri2pet/200/warped/raw/images
RES_DIR=/scratch/ychen855/Data/mri2pet/200/warped/raw/gen_0_baseline
PYTHON_DIR=/scratch/ychen855/mri2pet/CycleGAN_3D/test.py
for subj in w_m073S4443L122211E73TCFN.nii w_m031S4194L090111M63TCFN.nii w_m068S4217L090611E73TCFN.nii w_m013S4917L080613E63TCFN.nii w_m068S2315L030811E73TCFN.nii w_m016S4121L092115N73TCFN.nii w_m027S4926L092012E63TCFN.nii w_m072S4610L033012E73TCFN.nii w_m029S2395L032018E33TCFN.nii w_m005S4185L091211E73TCFN.nii w_m002S1155L010515M63TCFN.nii w_m027S4966L101312E63TCFN.nii w_m073S0746L020314M63TCFN.nii w_m067S4184L091213E73TCFN.nii w_m073S4360L011314E73TCFN.nii w_m018S4889L081012M63TCFN.nii w_m072S4769L072314M73TCFN.nii w_m023S6369L051818M33TCFN.nii w_m035S0292L042610M715TCFN.nii w_m016S2284L021011E73TCFN.nii w_m018S2180L010213E63TCFN.nii w_m027S0408L051611M715TCFN.nii w_m099S2146L110910E73TCFN.nii w_m072S4445L011712E73TCFN.nii w_m022S2379L060519E33TCFN.nii w_m032S2247L030916E73TCFN.nii w_m035S4785L060613S73TCFN.nii w_m031S4218L091813N63TCFN.nii w_m073S4312L011316E73TCFN.nii w_m005S6427L062518M33TCFN.nii w_m072S4383L120911E73TCFN.nii w_m009S4543L030112M73TCFN.nii w_m072S4226L100413E73TCFN.nii w_m014S2185L121010E73TCFN.nii w_m021S5099L030413E73TCFN.nii w_m068S4061L060311M73TCFN.nii w_m094S4434L020416E73TCFN.nii w_m021S4254L092611N73TCFN.nii w_m002S4251L092611M63TCFN.nii w_m052S4626L040312M73TCFN.nii
do
	python ${PYTHON_DIR} --name ${NAME} --image ${IMG_DIR}/${subj} --result ${RES_DIR}/${subj} --workers 4 --netG resnet_6blocks --ngf 8 --checkpoints_dir /scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check --which_epoch ${EPOCH}
done