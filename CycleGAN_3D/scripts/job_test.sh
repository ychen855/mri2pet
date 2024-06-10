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
IMG_DIR=/scratch/ychen855/Data/mri2pet/200/warped/raw/test/images
RES_DIR=/scratch/ychen855/Data/mri2pet/200/warped/raw/test/gen_baseline
PYTHON_DIR=/scratch/ychen855/mri2pet/CycleGAN_3D/test.py

for subj in `ls ${IMG_DIR}`
do
    python ${PYTHON_DIR} --name amcii_200_baseline_80epoch --image ${IMG_DIR}/${subj} --result ${RES_DIR}/${subj} --workers 4 --checkpoints_dir /scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check --which_epoch ${EPOCH} --netG resnet_6blocks --ngf 8
done
